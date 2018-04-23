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
    ratio_HS_max = HP(6)
    W_min_construct = DP(45)
    baffle_thickness = DP(materials['thickness_plate'])

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

    def __init__(self, q, temp, depth_end, bod=None):
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

        A_ET_PV = self.area_ent_tank(q, temp, depth_end, self.hl, self.coll_pot,
                                     self.ratio_HS_min, self.W_min_construct,
                                     self.L_sed, self.L_ent_tank_max)

        # now calculate planview area of entrance tank + flocculator combined
        volume_floc = self.vol_floc(q, temp, self.hl, self.coll_pot)
        A_floc_PV = volume_floc/(depth_end + self.hl/2)
        A_ETF_PV = (A_ET_PV + A_floc_PV).to(u.m**2)

        # calculate width of the flocculator channels and entrance tank
        W_min = self.width_floc_min(q, temp, depth_end, self.hl, self.coll_pot
                                    self.ratio_HS_min, self.W_min_construct).to(u.m)
        W_tot = A_ETF_PV/self.L_sed
        self.num_chan = DP(self.num_channel(q, temp, depth_end, self.hl,
                                            self.coll_pot, W_tot,
                                            self.ratio_HS_min, self.W_min_construct))
        self.W_chan = DP(W_tot/self.num_chan)

        # calculate the height of the channel using depth at the end of the
        # flocculator, headloss, and freeboard
        self.h_chan = DP((depth_end + self.hl + self.freeboard).magnitude, u.m)

        # calculate baffle spacing and number of baffles in the Flocculator
        self.baffle_spacing_ = DP(self.baffle_spacing(q, temp, self.W_chan, self.hl,
                                              self.coll_pot, self.ratio_HS_max))
        self.num_baffles_chan_1 = DP(self.num_baffles(q, temp, self.W_chan, self.L_sed,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))
        self.num_baffles_chan_n = DP(self.num_baffles(q, temp, self.W_chan,
                                                   self.L_sed - self.L_ent_tank_max,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))

        # calculate the length of the baffles. The top baffle is set to the top of the
        # channel wall and the bottom baffle is set to the bottom of the channel.
        # The distance between baffles is the same as the vertical distance between
        # the top baffle and the bottom of the channel, which is the same vertical
        # distance as the bottom baffle and the free surface at the end of the flocculator
        self.L_top_baffle = DP(h_chan - baffle_spacing_)
        self.L_bottom_baffle = DP(depth_end - baffle_spacing_)

        # determine if there are obstacles in the flocculator
        if q > 0.05*u.m**3/u.s:
            self.obstacles_bool = DP(0)
        else:
            self.obstacles_bool = DP(1)
