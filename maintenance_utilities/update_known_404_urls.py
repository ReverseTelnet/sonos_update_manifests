# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     Update Known 404 URLs Utility                                                                                                  │
# │                                                                                                                                    │
# │         This Utility contains functions and methods to git commit new Manifest Files.                                              │
# │         These functions are intended for use by the Github Workflow process.                                                       │
# │                                                                                                                                    │
# ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                Absolute Path Imports - Enablement Function               │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



#  ─────────────────────  Enables Absolute Path Imports  ─────────────────────



def enable_absolute_imports():
    import sys
    from os import getcwd
    PWD = getcwd()
    if PWD in sys.path:
        pass
    else:
        sys.path.append(PWD)



enable_absolute_imports()



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                        Module Logging Instantiation                      │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



import logging



#  ───────────────────────  Always Log / Always Save  ───────────────────────



LOG = logging.getLogger('utilities.logging_utility')



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                   Directory, File, and String Constants                  │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from utilities.common_utilities import get_pwd_absolute_path



#  ────────────────────────  Where Am I? Absolutely  ────────────────────────



pwd_absolute_path = get_pwd_absolute_path()



#  ─────────────────────────  Baseline Utility File  ─────────────────────────



baseline_utility = f'{pwd_absolute_path}/utilities/known_404_urls.py'



#  ───────────────────────────  Starting Variable  ───────────────────────────



starting_variable = 'known_404_url_list'



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                      List Comparison Helper Function                     │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from natsort import natsorted, ns



#  ─────────────  Compare New List Against Known Existing List  ─────────────



def list_comparison(known_404_url_set, literal_list):
    known_404_list = natsorted(known_404_url_set, alg=ns.IC)
    exact_match = known_404_list == literal_list
    return exact_match, known_404_list



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                          Putting It All Together                         │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



import re
import ast
from utilities.common_utilities import open_text_file
from utilities.common_utilities import repr_format_a_list
from utilities.common_utilities import three_carriage_returns
from utilities.write_and_save_utility import save_string_to_text_file
from maintenance_utilities.maintenance_common_utility import utility_file_git_commit_headless_workflow



#  ────────────────────  Update Known 404 URLs Workflow  ────────────────────



def update_known_404_urls_workflow(known_404_url_set):



    #  ─────────────────────────  Open, Read, and Split  ─────────────────────────



    data = open_text_file(baseline_utility)
    data_split = re.split(f'^{starting_variable}', data, flags=re.M)



    #  ──────────────────────────  Python String Magic  ──────────────────────────



    list_as_string = data_split[1].replace(' = ', '')
    literal_list = natsorted(ast.literal_eval(list_as_string), alg=ns.IC)



    #  ─────────────────────────  Compare and Contrast  ─────────────────────────



    exact_match, known_404_list = list_comparison(known_404_url_set, literal_list)



    #  ─────────────────────  Substitute, Save, and Commit  ─────────────────────



    if not exact_match:
        repr_formatted = repr_format_a_list(known_404_list)
        final_text_template = f'{data_split[0]}{starting_variable} = updated_list'
        final_text = re.sub('updated_list', f'{repr_formatted}{three_carriage_returns}', final_text_template)
        save_string_to_text_file(baseline_utility, final_text)
        result_01, result_02, error = utility_file_git_commit_headless_workflow(pwd_absolute_path, baseline_utility)



        if not error:
            LOG.info(f'\n\n{result_01}\n\n')
            LOG.info(f'\n\n{result_02}\n\n')
        elif error:
            LOG.error(f'\n\n{result_01}\n\n')
            LOG.error(f'\n\n{result_02}\n\n')


