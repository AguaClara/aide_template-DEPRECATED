from aide_design.play import*
from aide_design.unit_process_design.prefab import lfom_prefab_functional as lfom

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


### This section is for Entrance Tank and LFOM calculations
#### We need to look at Mathcad files "FlocculatorEntranceTank" and "LFOM"

#### LFOM - should use the lfom_prefab_functional functions whenever possible
@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def ND_lfomhigh(q_plant, hl, Gt, T, W_tot):
    """Return the area of the LFOM pipe required for the flow rate, safety
    factor, and velocity."""
    SDR = 26
    ND_lfomhigh = ND_SDR_available(ID, SDR)
     return hl_lfom


@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def ND_lfomhigh(q_plant, hl, Gt, T, W_tot):
    """Return the nominal pipe diameter corresponding to the calculated minimum
    diameter."""
    SDR = 26
    ND_lfomhigh = ND_SDR_available(ID, SDR)
     return hl_lfom


@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def hl_lfom(q_plant, hl, Gt, T, W_tot):
    """Return the headloss through the LFOM."""
    i = 0
    while :
     return hl_lfom

@u.wraps(u.m, [u.m**3/u.s, u.m, None, u.degK, u.m], False)
def l_tpext(q_plant, hl, Gt, T, W_tot):
    """Return the length of the entrance tank (ET) for the "Top Plate Extension"
    ."""
    l_tpext = hl_lfom / np.sin(AN_EtPlate) + 5 * u.cm
     return l_tpext