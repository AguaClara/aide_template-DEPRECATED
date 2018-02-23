from aide_design.play import*
from aide_design.unit_process_design import lfom

# expansion minor loss coefficient for 180 degree bend
K_e = (1 / pc.RATIO_VC_ORIFICE**2 - 1)**2

# these inputs will come from constants.py or optional_inputs.py
PI_HS_min = 3
PI_HS_max = 6
width_min_const = 45*u.cm

@u.wraps(1/u.s, [u.m, None, u.degK], False)
def G_avg(hl, Gt, T):
    """Return the average velocity gradient of a flocculator given head
    loss, collision potential and temperature. """
    G = (pc.gravity.magnitude * hl) / (Gt * pc.viscosity_kinematic(T).magnitude)
    return G

@u.wraps(u.m**3, [u.m**3/u.s, u.m, None, u.degK], False)
def vol_floc(q_plant, hl, Gt, T):
    """Return the total volume of the flocculator using plant flow rate, head
    loss, collision potential and temperature.

    Uses an estimation of flocculator residence time (ignoring the decrease
    in water depth caused by head loss in the flocculator.) Volume does not take
    into account the extra volume that the flocculator will have due to changing
    water level caused by head loss."""
    vol = (Gt / G_avg(hl, Gt, T).magnitude)*q_plant
    return vol

@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def width_HS_min(q_plant, hl, Gt, T, depth_end):
    """Return the minimum channel width required to achieve H/S > 3.

    The channel can be wider than this, but this is the absolute minimum width
    for a channel. The minimum width occurs when there is only one expansion per
    baffle and thus the distance between expansions is the same as the depth of
    water at the end of the flocculator."""
    nu = pc.viscosity_kinematic(T).magnitude

    w = PI_HS_min*((K_e/(2 * depth_end * (G_avg(hl, Gt, T).magnitude**2) * nu))**(1/3))*q_plant/depth_end
    return w

@u.wraps(u.cm, [u.m**3/u.s, u.m, None, u.degK], False)
def width_floc_min(q_plant, hl, Gt, T):
    """Return the minimum channel width required.

    This takes the maximum of the minimum required to achieve H/S > 3 and the
    minimum required for constructability based on the width of the human hip.
    """
    return max(width_HS_min(q_plant, hl, Gt, T).magnitude, width_min_const.magnitude)

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def num_channel(q_plant, hl, Gt, T, W_tot):
    """Return the number of channels in the entrance tank/flocculator (ETF).

    This takes the total width of the flocculator and divides it by the minimum
    channel width. A floor function is used to ensure that there are an even
    number of channels."""
    num = W_tot/(width_floc_min(q_plant, hl, Gt, T).magnitude)
# floor function with step size 2
    num = np.floor(num/2)*2
    return int(max(num,2))

def area_ent_tank(q_plant, hl, Gt, T, depth_end):
    """Return the planview area of the entrance tank.

    This uses an iterative method to calculate the entrance tank area repeatedly
    until it stabilizes to within 1% of the previous iteration."""
    # guess the planview area before starting iteration
    A_new = 1*u.m**2
    A_ratio = 0

    while (A_ratio) > 1.01 and (A_ET_PV/A_new) < 0.99:
        A_ET_PV = A_new

        vol_floc = vol_floc(q_plant, hl, Gt, T)
        A_floc_PV = vol_floc/(depth_end + hl/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        W_min = width_floc_min(q_plant, hl, Gt, T)

        W_tot = A_ETF_PV/opt.L_sed

        num_chan = num_channel(q_plant, hl, Gt, T, W_tot)
        W_chan = W_tot/num_chan

        A_new = opt.L_ET_max*W_chan

        A_ratio = A_new/A_ET_PV

    return A_new

### Baffle calculations
@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def exp_dist_max(q_plant, hl, Gt, T, W_chan):
    """"Return the maximum distance between expansions for the largest
    allowable H/S ratio."""
    g_avg = G_avg(hl, Gt, T).magnitude
    nu = pc.viscosity_kinematic(T).magnitude
    term1 = (K_e/(2 * (g_avg**2) * nu))**(1/4)
    term2 = (Pi_HS_max*q_plant/W_chan)**(3/4)
    exp_dist_max = term1*term2
    return exp_dist_max

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def num_expansions(q_plant, hl, Gt, T, depth_end):
    """"Return the minimum number of expansions per baffle space."""
    return int(np.ceil(depth_end/(exp_dist_max(q_plant, hl, Gt, T)).magnitude))

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def height_exp(q_plant, hl, Gt, T, depth_end):
    """Return the actual distance between expansions given the integer
    requirement for the number of expansions per flocculator depth."""
    return depth_end/num_expansions(q_plant, hl, Gt, T)

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def baffle_spacing(q_plant, hl, Gt, T, W_chan):
    """Return the spacing between baffles based on the target velocity gradient
    ."""
    g_avg = G_avg(hl, Gt, T).magnitude
    nu = pc.viscosity_kinematic(T).magnitude
    term1 = (K_e/(2 * exp_dist_max(q_plant, hl, Gt, T).magnitude * (g_avg**2) * nu))**(1/3)
    return term1 * q_plant/W_chan

@u.wraps(None, [u.m**3/u.s, u.m, None, u.degK, u.m, u.m], False)
def num_baffles(q_plant, hl, Gt, T, L, baffle_thickness):
    """Return the number of baffles that would fit in the channel given the
    channel length and spacing between baffles."""
    num = round((L / (baffle_spacing(q_plant, hl, Gt, T).magnitude + baffle_thickness)
    # the one is subtracted because the equation for num gives the number of
    # baffle spaces and there is always one less baffle than baffle spaces due to geometry
    return int(num) - 1

#### Entrance tank
@u.wraps(u.inch, [u.m**3/u.s, u.degK, u.m, None], False)
def drain_OD(q_plant, T, depth_end, SDR):
    """Return the nominal diameter of the entrance tank drain pipe. Depth at the
    end of the flocculator is used for headloss and length calculation inputs in
    the diam_pipe calculation."""
    nu = pc.viscosity_kinematic(T)
    Kminor = con.K_MINOR_PIPE_ENTRANCE + con.K_MINOR_PIPE_EXIT + con.K_MINOR_EL90
    drain_ID = pc.diam_pipe(q_plant, depth_end, depth_end, nu, mat.PIPE_ROUGH_PVC, KMinor)
    drain_ND = pipe.ND_SDR_available(drain_ID, SDR)
    return pipe.OD(drain_ND).magnitude

@u.wraps(None, [u.m**3/u.s, u.m], False)
def num_plates_ET(q_plant, W_chan):
    """Return the number of plates in the entrance tank.

    This number minimizes the total length of the plate settler unit."""
    num_plates = np.ceil(np.sqrt(q_plant/(con.DIST_CENTER_ENT_TANK_PLATE.magnitude
    * W_chan * con.VEL_ENT_TANK_CAPTURE_BOD.magnitude * np.sin(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude))))
    return num_plates

@u.wraps(u.m, [u.m**3/u.s, u.m], False)
def L_plate_ET(q_plant, W_chan):
    """Return the length of the plates in the entrance tank."""
    L_plate = (q_plant/(num_plates_ET(q_plant, W_chan).magnitude * W_Chan *
    con.VEL_ENT_TANK_CAPTURE_BOD.magnitude * np.cos(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude)))
    - (con.SPACE_ENT_TANK_PLATE.magnitude * np.tan(con.AN_ENT_TANK_PLATE.to(u.rad).magnitude))
    return L_plate

###### LFOM
