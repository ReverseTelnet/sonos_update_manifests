# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     Update Known macOS Versions                                                                                                    │
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



baseline_utility = f'{pwd_absolute_path}/utilities/known_macos_versions.py'



#  ───────────────────────────  Starting Variable  ───────────────────────────



starting_variable = 'known_macos_versions'



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                      List Comparison Helper Function                     │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from utilities.common_utilities import sort_dictionary_by_key



#  ─────────────  Compare New List Against Known Existing List  ─────────────



def dict_comparison(installers, literal_dict):
    sorted_installers = sort_dictionary_by_key(installers)
    exact_match = sorted_installers == literal_dict
    return exact_match, sorted_installers



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                          Putting It All Together                         │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



import re
import ast
from utilities.common_utilities import open_text_file
from utilities.common_utilities import three_carriage_returns
from utilities.common_utilities import repr_format_a_dictionary
from utilities.write_and_save_utility import save_string_to_text_file
from utilities.desktop_versions_utility import get_manifest_file_list
from utilities.desktop_versions_utility import parse_manifest_files_for_links
from utilities.desktop_versions_utility import construct_os_installer_dictionaries
from maintenance_utilities.maintenance_common_utility import utility_file_git_commit_headless_workflow



#  ────────────────  Update Known macOS Installers Workflow  ────────────────



def update_known_macos_installers_workflow():



    #  ─────────────────────────  Open, Read, and Split  ─────────────────────────



    data = open_text_file(baseline_utility)
    data_split = re.split(f'^{starting_variable}', data, flags=re.M)



    #  ──────────────────────────  Python String Magic  ──────────────────────────



    dict_as_string = data_split[1].replace(' = ', '')
    literal_dict = sort_dictionary_by_key(ast.literal_eval(dict_as_string))



    #  ────────────────────────  Enumerate and Populate  ────────────────────────



    manifest_files = get_manifest_file_list()
    all_installer_links = parse_manifest_files_for_links(manifest_files)
    macos_installers, _ = construct_os_installer_dictionaries(all_installer_links)



    #  ─────────────────────────  Compare and Contrast  ─────────────────────────



    exact_match, sorted_installers = dict_comparison(macos_installers, literal_dict)



    #  ─────────────────────  Substitute, Save, and Commit  ─────────────────────



    if not exact_match:
        repr_formatted = repr_format_a_dictionary(sorted_installers)
        final_text_template = f'{data_split[0]}{starting_variable} = updated_dict'
        final_text = re.sub('updated_dict', f'{repr_formatted}{three_carriage_returns}', final_text_template)
        save_string_to_text_file(baseline_utility, final_text)
        result_01, result_02, error = utility_file_git_commit_headless_workflow(pwd_absolute_path, baseline_utility)



        if not error:
            LOG.info(f'\n\n{result_01}\n\n')
            LOG.info(f'\n\n{result_02}\n\n')
        elif error:
            LOG.error(f'\n\n{result_01}\n\n')
            LOG.error(f'\n\n{result_02}\n\n')


