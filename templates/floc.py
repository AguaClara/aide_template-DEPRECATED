from aide_design.units import unit_registry as u
from bottom_baffle_assembly import *
from floc_concrete_chan import *
from ent_floc_baffle_support import *
from main_floc_baffle_support import *
from obstacle_assembly import *
from top_baffle_assembly import *
from aide_render.builder_classes import DP, HP


class Flocculator:
    """This is a flocculator class. It already has a lot of features built in,
    such as constants that go in the class attribute section (defaults), and methods.
    As well as an instantiation process that can be used to set custom values.

    Attributes
    ----------
    These are the default values for a flocculator. To overwrite, pass these
    into the bod (Basis Of Design) variable into the constructor.

    temp : float
        Design temperature

    L_ent_tank_max : float
        The maximum length of the entrance tank

    L_sed : float
        The length of the sedimentation unit process, including channels

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

    area_ent_tank(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3,
                  W_min_construct=45*u.cm, L_sed=7.35*u.m, L_ent_tank_max=2.2*u.m)
        Return the planview area of the entrance tank given plant flow rate,
        headloss, target collision potential, design temperature, and depth of
        water at the end of the flocculator

    vol_floc(Q_plant, temp, hl, coll_pot)
        Return the total volume of the flocculator using plant flow rate, head
        loss, collision potential and temperature

    width_floc_min(Q_plant, temp, depth_end, hl, coll_pot, ratio_HS_min=3,
                   W_min_construct=45*u.cm)
        Return the minimum channel width required

    num_channel(Q_plant, temp, depth_end, hl, coll_pot, W_tot, ratio_HS_min=3,
                W_min_construct=45*u.cm)
        Return the number of channels in the entrance tank/flocculator (ETF)

    baffle_spacing(Q_plant, temp, W_chan, hl, coll_pot, ratio_HS_max=6)
        Return the spacing between baffles based on the target velocity gradient

    num_baffles(Q_plant, temp, W_chan, L, hl, coll_pot, ratio_HS_max=6,
                baffle_thickness=2*u.mm)
        Return the number of baffles that would fit in the channel given the
        channel length and spacing between baffles

    Examples
    --------

    >>> my_floc = Flocculator(HP(20, u.L/u.s), HP(2, u.m))
    >>> from aide_render.builder import extract_types
    >>> floc_design_dict = extract_types(my_floc, [DP], [dict])
    >>> from aide_render.yaml import load, dump
    >>> dump(floc_design_dict)
    "BottomBaffles_Assembly: {Num_Exit: !DP '18 ', Num_Inlet: !DP '26 ', Spacing: !DP '0.272\n    meter', Thickness: !DP '2 millimeter', TotalNum: !DP '2 ', WallThickness: !DP '0.15\n    meter', Width: !DP '0.3134 meter'}\nConcreteChannels: {EntTank_Length: !DP '2.2 meter', FirstLength: !DP '5.786 meter',\n  FloorThickness: !DP '0.2 meter', Height: !DP '2.5 meter', Length: !DP '7.35 meter',\n  TotalNum: !DP '2 ', WallThickness: !DP '0.15 meter', Width: !DP '0.3134 meter'}\nEntFlocBaffleSupport: {bafflethickness: !DP '2 millimeter', numberbaffles: !DP '18 ',\n  numberentbaffles: !DP '26 '}\nMainFlocBaffleSupport: {bafflethickness: !DP '2 millimeter', numberbaffles: !DP '18 ',\n  numberentbaffles: !DP '26 '}\nObstacles_Assembly: {Num_Exit: !DP '26 ', Num_Inlet: !DP '18 ', Spacing: !DP '0.272\n    meter', Thickness: !DP '2 millimeter', TotalNum: !DP '2 ', WallThickness: !DP '0.15\n    meter', Width: !DP '0.3134 meter'}\nTopBaffles_Assembly: {Num_Exit: !DP '18 ', Num_Inlet: !DP '26 ', Spacing: !DP '0.272\n    meter', Thickness: !DP '2 millimeter', TotalNum: !DP '2 ', WallThickness: !DP '0.15\n    meter', Width: !DP '0.3134 meter'}\nnumberrows: !DP '1 '\n"

    """

    #ent_tank: dict = aide_render.render.("ent_tank.yaml")
    #sed: dict = aide_render.yaml.load("sed.yaml")
    #materials: dict = aide_render.yaml.load("materials.yaml")

    ############## ATTRIBUTES ################
    hl = HP(40, u.cm)
    coll_pot = HP(37000)
    freeboard = HP(10, u.cm)
    ratio_HS_min = HP(3)
    ratio_HS_max = HP(6)
    W_min_construct = HP(45, u.cm)
    #L_ent_tank_max = DP(ent_tank['L'])
    #L_sed = DP(sed['L'])
    #baffle_thickness = DP(materials['thickness_plate'])
    #temp = DP(plant['temp'])
    #wall_thickness = DP(plant['wall_thickness'])
    #floor_thickness = DP(plant['floor_thickness'])

    # will take these out later when we get the imports from other classes to work
    L_ent_tank_max = HP(2.2, u.m)
    L_sed = HP(7.35, u.m)
    baffle_thickness = HP(2, u.mm)
    temp = HP(15, u.degC)
    wall_thickness = HP(0.15, u.m)
    floor_thickness = HP(0.2, u.m)
    ent_tank_overhang_length = HP(0.6363, u.m)

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

    def __init__(self, q, depth_end, bod=None):
        """
        This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------
        bod (Basis of Design) : dict: optional
            A dict of values that will override or add any attributes of the Floc
            component.
        q : float
            The flow rate through the flocculator
        temp : float
            The design temperature
        depth_end : float
            The depth of water at the end of the flocculator
        """

        # add bod as instance fields:
        if bod:
            for k, v in bod.items():
                setattr(self, k, v)

        # calculate planview area of the entrance tank
        A_ET_PV = self.area_ent_tank(q, self.temp, depth_end, self.hl, self.coll_pot,
                                     self.ratio_HS_min, self.W_min_construct,
                                     self.L_sed, self.L_ent_tank_max)

        # now calculate planview area of entrance tank + flocculator combined
        volume_floc = self.vol_floc(q, self.temp, self.hl, self.coll_pot)
        A_floc_PV = volume_floc/(depth_end + self.hl/2)
        A_ETF_PV = (A_ET_PV + A_floc_PV).to(u.m**2)

        # calculate width of the flocculator channels and entrance tank
        W_min = self.width_floc_min(q, self.temp, depth_end, self.hl, self.coll_pot,
                                    self.ratio_HS_min, self.W_min_construct).to(u.m)
        W_tot = A_ETF_PV/self.L_sed
        self.num_chan = HP(self.num_channel(q, self.temp, depth_end, self.hl,
                                            self.coll_pot, W_tot,
                                            self.ratio_HS_min, self.W_min_construct))
        self.W_chan = HP((W_tot/self.num_chan).to(u.m).magnitude, u.m)

        # calculate the height of the channel using depth at the end of the
        # flocculator, headloss, and freeboard
        self.h_chan = HP((depth_end + self.hl + self.freeboard).to(u.m).magnitude, u.m)

        # calculate baffle spacing and number of baffles in the flocculator
        self.baffle_spacing_ = HP(self.baffle_spacing(q, self.temp, self.W_chan, self.hl,
                                              self.coll_pot, self.ratio_HS_max).magnitude, u.m)
        self.num_baffles_chan_1 = HP(self.num_baffles(q, self.temp, self.W_chan, self.L_sed,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))
        self.num_baffles_chan_n = HP(self.num_baffles(q, self.temp, self.W_chan,
                                                   self.L_sed - self.L_ent_tank_max,
                                                   self.hl, self.coll_pot,
                                                   self.ratio_HS_max, self.baffle_thickness))

        # calculate the length of the baffles. The top baffle is set to the top of the
        # channel wall and the bottom baffle is set to the bottom of the channel.
        # The distance between baffles is the same as the vertical distance between
        # the top baffle and the bottom of the channel, which is the same vertical
        # distance as the bottom baffle and the free surface at the end of the flocculator
        self.L_top_baffle = HP((self.h_chan - self.baffle_spacing_).to(u.m).magnitude, u.m)
        self.L_bottom_baffle = HP((depth_end - self.baffle_spacing_).to(u.m).magnitude, u.m)

        # determine if there are obstacles in the flocculator
        if q.to(u.m**3/u.s).magnitude > 0.05:
            self.obstacles_bool = HP(0)
        else:
            self.obstacles_bool = HP(1)

        self.BottomBaffles_Assembly = dict(vars(BottomBaffles_Assembly(self.L_bottom_baffle,
            self.baffle_thickness, self.W_chan, self.num_chan, self.num_baffles_chan_1,
            self.num_baffles_chan_n, self.baffle_spacing_, self.wall_thickness)))

        self.ConcreteChannels = dict(vars(ConcreteChannels(self.num_chan, self.L_ent_tank_max,
            self.h_chan, self.L_sed, self.W_chan, self.ent_tank_overhang_length,
            self.wall_thickness, self.floor_thickness)))

        self.EntFlocBaffleSupport = dict(vars(EntFlocBaffleSupport(self.L_bottom_baffle,
            self.L_top_baffle, self.baffle_thickness, self.W_chan,
            self.num_baffles_chan_1, self.num_baffles_chan_n)))

        self.MainFlocBaffleSupport = dict(vars(MainFlocBaffleSupport(self.baffle_thickness,
            self.num_baffles_chan_1, self.num_baffles_chan_n)))

        self.Obstacles_Assembly = dict(vars(Obstacles_Assembly(self.obstacles_bool,
            self.baffle_thickness, self.W_chan, self.num_chan, self.num_baffles_chan_1,
            self.num_baffles_chan_n, self.baffle_spacing_, self.wall_thickness)))

        self.TopBaffles_Assembly = dict(vars(TopBaffles_Assembly(self.L_top_baffle,
            self.baffle_thickness, self.W_chan, self.num_chan, self.num_baffles_chan_1,
            self.num_baffles_chan_n, self.baffle_spacing_, self.wall_thickness)))

        self.numberrows = DP(self.num_chan.magnitude - 1)
