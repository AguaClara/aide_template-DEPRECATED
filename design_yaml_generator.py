import yaml
import jinja2
from aide_design.units import unit_registry as u
import aide_design
import numpy as np
import os
import flochydraulicfunctiontest as floctest

# This will be passed in from aide_gui and represents all the variables that
# the user has designed.
user_parameters_dict = {"q_plant": 20 * u.L/u.s, "temp": 20 * u.degC}

# These are the modules we want to make available within the template environment.
modules_dict = {"u": u, "aide_design": aide_design, "np": np, "floctest": floctest}

# We tell jinja to look within the design_templates folder
folder_path = os.path.dirname(os.path.abspath(__file__))+"/design_templates"
env = jinja2.Environment(
    loader=jinja2.loaders.FileSystemLoader(folder_path),
    trim_blocks=True,
    lstrip_blocks=True
)

# Load the environment with the modules specified above.
env.globals.update(modules_dict)

template = env.get_template('plant.yaml')
#template = env.get_template('test.yaml.j2')

# Run the Jinja engine on the template and print the resulting string
rendered_template = template.render(user_parameters_dict)
print("############## Here is the yaml file after Jinja has processed it: ")
print(rendered_template)

dictionary = yaml.load(rendered_template)
print("############## The dictionary that pyYaml has loaded into Python from yaml: ")
print(dictionary)


# ############## Here is the yaml file after Jinja has processed it:
# # This is a template to build an AguaClara water treatment plant.
#
# # Globals that define plant-wide parameters are passed in from the gui through
# # the user_parameters_dict.
#
# # Unit processes are imported with context to provide access to the variables
# # To print a unit process, include it.
#
# # The goal is to have a filled-out set of parameters to feed to Fusion that can
# # tell Fusion how to build the plant.
#
#
# - hp: # hydraulic parameters do not show up in the Fusion environment (like gt and q_plant)
#   - q:
#   - temp : 20 degC
# - dp: # design parameters are put into Fusion... only parameters related to the physical construction.
#   - n_sed_tanks: 4 dimensionless
# - sed:
#
#     - hp :
#       - q : 6 liter / second
# - floc:
#
#     - hp :
#       - q :
#       - temp :
#       - gt : (37, 0) # collision potential... a constant
#       - hl :  40 centimeter #headloss
#       - hs_min : 3 # min h/s ratio
#       - hs_max : 6 # max h/s ratio
#       - min_floc_width :  45 centimeter # for construction purposes, needs to be larger than a human hip
#     - floc_tank :
#       - hp :
#         - volume :  TODO
#       - dp :
#         - L :  TODO
# ############## The dictionary that pyYaml has loaded into Python from yaml:
# [{'hp': [{'q': None}, {'temp': '20 degC'}]}, {'dp': [{'n_sed_tanks': '4 dimensionless'}]}, {'sed': [{'hp': [{'q': '6 liter / second'}]}]}, {'floc': [{'hp': [{'q': None}, {'temp': None}, {'gt': '(37, 0)'}, {'hl': '40 centimeter'}, {'hs_min': 3}, {'hs_max': 6}, {'min_floc_width': '45 centimeter'}]}, {'floc_tank': [{'hp': [{'volume': 'TODO'}]}, {'dp': [{'L': 'TODO'}]}]}]}]
