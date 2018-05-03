from aide_design.units import unit_registry as u
from top_baffle import *
from aide_render.builder_classes import DP, HP


class TopBaffles_Assembly:
    """This is a top baffle assembly class. It's called by the flocculator
    class so that the hierarchy of objects in Python is the same as in Fusion.

    """

    def __init__(self, L_top_baffle, baffle_thickness, W_chan, num_chan,
                 num_baffles_chan_1, num_baffles_chan_n, baffle_spacing,
                 wall_thickness):
        """This is where the "instantiation" occurs. Think of this as "rendering the
        template" or "using the cookie-cutter to make the cookie". Here is where we
        call all the methods that determine design qualities of the specific
        flocculator we are building.

        Parameters
        ----------

        L_bottom_baffle : float
            Length of the baffles on the bottom of the flocculator

        baffle_thickness : float
            Thickness of a baffle

        W_chan : float
            Width of each flocculator channel

        num_chan : int
            Number of flocculator channels

        num_baffles_chan_1 : int
            Number of baffles in the first channel

        num_baffles_chan_n : int
            Number of baffles in every channel but the first

        baffle_spacing : float
            The spacing between baffles

        wall_thickness : float
            Thickness of the walls in the flocculator

        """

        self.Num_Exit = DP(num_baffles_chan_n.magnitude)
        self.Num_Inlet = DP(num_baffles_chan_1.magnitude)
        self.Spacing = DP(baffle_spacing.magnitude, baffle_spacing.units)
        self.Thickness = DP(baffle_thickness.magnitude, baffle_thickness.units)
        self.TotalNum = DP(num_chan.magnitude)
        self.WallThickness = DP(wall_thickness.magnitude, wall_thickness.units)
        self.Width = DP(W_chan.magnitude, W_chan.units)

        self.TopBaffle = TopBaffle(L_top_baffle, baffle_thickness, W_chan)
