from aide_design.units import unit_registry as u
from aide_render.builder_classes import DP, HP


class BottomBaffles_Assembly:
  """This is a baffle assembly class. It's called by the flocculator class so
  that the hierarchy of objects in Python is the same as in Fusion.

  Attributes
  ----------
  These are the default values for a baffle assembly. To overwrite, pass these
  into the bod (Basis Of Design) variable into the constructor.

  """

  def __init__(self, L_bottom_baffle, baffle_thickness, W_chan, num_chan,
               num_baffles_chan_1, num_baffles_chan_n, baffle_spacing):
    """This is where the "instantiation" occurs. Think of this as "rendering the
    template" or "using the cookie-cutter to make the cookie". Here is where we
    call all the methods that determine design qualities of the specific
    flocculator we are building.

    Parameters
    ----------


    """

    self.Num_Exit = DP(num_baffles_chan_1.magnitude)
    self.Num_Inlet = DP(num_baffles_chan_n.magnitude)
    self.Spacing = DP(baffle_spacing.magnitude, baffle_spacing.units)
    self.Spacing = DP(baffle_spacing.magnitude, baffle_spacing.units)
    self.Thickness = DP(baffle_thickness.magnitude, baffle_thickness.units)
    self.TotalNum = DP(num_chan.magnitude)
    self.W_chan = DP(W_chan.magnitude, W_chan.units)
