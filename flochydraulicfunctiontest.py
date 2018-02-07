from aide_design.play import*

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
    minimum required for constructability based on the width of the human hip."""
    return max(width_HS_min(flow_plant, headloss_floc_BOD, Gt_BOD, T_BOD).magnitude,width_min_const.magnitude)
