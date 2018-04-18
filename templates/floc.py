import aide_design.materials_database as mat
import aide_design.pipedatabase as pipe
import aide_design.constants as con
import numpy as np
from aide_design.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class Floc:
    r""" This is an example class for an LFOM. It already has a lot of features built in,
    such as constants that go in the class attribute section (defaults), and methods.
    As well as an instantiation process that can be used to set custom values.

    Attributes
    ----------
    These are the default values for an LFOM. To overwrite, pass these into the bod
    (Basis Of Design) variable into the constructor.

    L_ent_tank_max : float
        The maximum length of the entrance tank

    L_sed : float
        The length of the sedimentation tank

    hl : float
        Headloss through the flocculator

    coll_pot : int
        Desired collision potential in the flocculator

    freeboard: float
        The height between the water and top of the flocculator channels

    ratior_HS_min : int
        Minimum allowable ratio between the water depth and edge to edge distance
        between baffles

    ratio_HS_max : int
        Maximum allowable ratio between the water depth and edge to edge distance
        between baffles

    W_min_construct : float
        Minimum width of a flocculator channel based on the width of the human hip

    baffle_thickness : float
        Thickness of a baffle


    Methods
    -------
    All these methods are just imported from the aide_design flocculator.
    This would replace that.



    Examples
    --------


    """

    ent_tank: dict = aide_render.yaml.load("ent_tank.yaml")
    sed: dict = aide_render.yaml.load("sed.yaml")
    materials: dict = aide_render.yaml.load("materials.yaml")

    ############## ATTRIBUTES ################
    L_ent_tank_max = DP(ent_tank['L'])
    L_sed = DP(sed['L'])
    hl = HP(40, u.cm)
    coll_pot = HP(37000)
    freeboard = DP(10, u.cm)
    ratio_HS_min = HP(3)
    ratio_HS_min = HP(6)
    W_min_construct = DP(45)
    baffle_thickness = DP(materials['thickness_PVC_sheet'])

    ############### METHODS #################
    from aide_design.unit_process_design.floc import (
        area_ent_tank,
        vol_floc,
        width_floc_min,
        num_channel,
        baffle_spacing,
        num_baffles,
    )

    area_ent_tank = staticmethod(area_ent_tank)
    vol_floc = staticmethod(vol_floc)
    width_floc_min = staticmethod(width_floc_min)
    num_channel = staticmethod(num_channel)
    baffle_spacing = staticmethod(baffle_spacing)
    num_baffles = staticmethod(num_baffles)

    # Aggregates the floc tank functions into a single function which
    # outputs a dictionary of all the necessary design parameters.
    @staticmethod
    @u.wraps(None, [u.m**3/u.s, u.degK, u.m, None], False)
    def floc_agg(Q_plant, temp, depth_end, floc_inputs=floc_dict):
        # calculate planview area of the entrance tank
        A_ET_PV = Floc.area_ent_tank(Q_plant, temp, depth_end, floc_inputs).magnitude

        # now calculate planview area of entrance tank + flocculator combined
        volume_floc = Floc.vol_floc(Q_plant, temp, floc_inputs).magnitude
        A_floc_PV = volume_floc/(depth_end + floc_inputs['hl'].to(u.m).magnitude/2)
        A_ETF_PV = A_ET_PV + A_floc_PV

        L_tank = floc_inputs['L_sed'].to(u.m).magnitude

        # calculate width of the flocculator channels and entrance tank
        W_min = Floc.width_floc_min(Q_plant, temp, depth_end, floc_inputs).to(u.m).magnitude
        W_tot = A_ETF_PV/L_tank
        num_chan = Floc.num_channel(Q_plant, temp, depth_end, W_tot, floc_inputs)
        W_chan = W_tot/num_chan

        # calculate the height of the channel using depth at the end of the
        # flocculator, headloss, and freeboard
        h_chan = depth_end + floc_inputs['hl'].to(u.m).magnitude + floc_inputs['freeboard'].to(u.m).magnitude

        # calculate baffle spacing and number of baffles in the Flocculator
        baffle_spacing_ = baffle_spacing(Q_plant, temp, W_chan, floc_inputs).magnitude
        num_baffles_chan_1 = num_baffles(Q_plant, temp, W_chan, L_tank, floc_inputs)
        num_baffles_chan_n = num_baffles(Q_plant, temp, W_chan, L_tank - floc_inputs['L_ent_tank_max'].to(u.m).magnitude, floc_inputs)

        # calculate the length of the baffles. The top baffle is set to the top of the
        # channel wall and the bottom baffle is set to the bottom of the channel.
        # The distance between baffles is the same as the vertical distance between
        # the top baffle and the bottom of the channel, which is the same vertical
        # distance as the bottom baffle and the free surface at the end of the flocculator
        L_top_baffle = h_chan - baffle_spacing_
        L_bottom_baffle = depth_end - baffle_spacing_

        # determine if there are obstacles in the flocculator
        if Q_plant > 0.05:
            obstacles_bool = 0
        else:
            obstacles_bool = 1

        # update the floc dictionary with outputs
        floc_inputs.update({'W_chan': W_chan, 'num_chan': num_chan,
            'h_chan': h_chan, 'baffle_spacing': baffle_spacing_,
            'num_baffles_chan_1': num_baffles_chan_1, 'num_baffles_chan_n': num_baffles_chan_n,
            'obstacles_bool': obstacles_bool, 'L_top_baffle': L_top_baffle,
            'L_bottom_baffle': L_bottom_baffle})
        return floc_inputs

    def __init__(self, q, temp, bod=None):
        """
        This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific LFOM
        we are building.

        Parameters
        ----------
        bod (Basis of Design) : dict: optional
            A dict of values that will override or add any attributes of the LFOM
            component.
        q : float
            The max flow rate the LFOM can handle
        temp : float
            The design temperature
        """

        # add bod as instance fields:
        if bod:
            for k, v in bod.items():
                setattr(self, k, v)

        self.q = HP(q)
        self.temp = HP(temp)
