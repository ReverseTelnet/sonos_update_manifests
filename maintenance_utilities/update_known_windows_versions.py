# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     Update Known Windows Versions                                                                                                  │
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



baseline_utility = f'{pwd_absolute_path}/utilities/known_windows_versions.py'



#  ───────────────────────────  Starting Variable  ───────────────────────────



starting_variable = 'known_windows_versions'



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



# ╭────────────────────────────────────────────────────────────────────────╮
# │                                                                        │
# │      Prevent 90.0-75190 Windows Desktop URL Change Churn Function      │
# │                                                                        │
# ╰────────────────────────────────────────────────────────────────────────╯



'''
Development Note:

    In Manifest File `90.0-75190-v17.2.3-lDpGfsxQdy-RC-5__6130426172307471`,
    the URL for the Windows Desktop Installer is listed as:

        >>> http://update-firmware.sonos.com/firmware/Prod/90.0-75190-v17.2.3-lDpGfsxQdy-RC-4/90.0-75190-1-3.exe

    This URL is not correct, as the actual URL is `RC-5`, which is reflected in:

        >>> manifest_files/c6f38e9f884349afba786f630ead94ca__5fc545f7374e62ed.upm
        >>> manifest_files/95.0-77060-v18.4-HwYJSN97Ae-RC-2__342f60d32391dc22.upm
        >>> manifest_files/95.0-77060-v18.4-HwYJSN97Ae-RC-2__4e277bb39174c0ea.upm
        >>> manifest_files/96.0-75280-v18.6-0DE12E5D85D1A66D-Alpha-1__5fc545f7374e62ed.upm

    This clear mistake in the Manifest URL is causing constant churn to the `known_windows_versions` utility,
    with the `RC-5` URL being replaced with the `RC-4` URL and vice-versa.

    The purpose of the following function is to stop the churn.
'''



import copy



#  ─────────────────────  RC-4 --> In | RC-5 --> Out  ─────────────────────



def prevent_90_0_75190_churn(windows_installers):
    deep_copy = copy.deepcopy(windows_installers)
    for version, exe_url in windows_installers.items():
        if '90.0-75190' in exe_url:
            correct_url = exe_url.replace('lDpGfsxQdy-RC-4', 'lDpGfsxQdy-RC-5')
            deep_copy[version] = correct_url
    return deep_copy



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                          Putting It All Together                         │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



import re
import ast
from utilities.common_utilities import open_text_file
from utilities.common_utilities import sort_dictionary_by_key
from utilities.common_utilities import three_carriage_returns
from utilities.common_utilities import repr_format_a_dictionary
from utilities.write_and_save_utility import save_string_to_text_file
from utilities.desktop_versions_utility import get_manifest_file_list
from utilities.desktop_versions_utility import parse_manifest_files_for_links
from utilities.desktop_versions_utility import construct_os_installer_dictionaries
from maintenance_utilities.maintenance_common_utility import utility_file_git_commit_headless_workflow



#  ───────────────  Update Known Windows Installers Workflow  ───────────────



def update_known_windows_installers_workflow():



    #  ─────────────────────────  Open, Read, and Split  ─────────────────────────



    data = open_text_file(baseline_utility)
    data_split = re.split(f'^{starting_variable}', data, flags=re.M)



    #  ──────────────────────────  Python String Magic  ──────────────────────────



    dict_as_string = data_split[1].replace(' = ', '')
    literal_dict = sort_dictionary_by_key(ast.literal_eval(dict_as_string))



    #  ────────────────────────  Enumerate and Populate  ────────────────────────



    manifest_files = get_manifest_file_list()
    all_installer_links = parse_manifest_files_for_links(manifest_files)
    _, windows_installers = construct_os_installer_dictionaries(all_installer_links)



    #  ─────────────────────────  Compare and Contrast  ─────────────────────────



    exact_match, sorted_installers = dict_comparison(prevent_90_0_75190_churn(windows_installers), literal_dict)



    #  ──────────────────────────  Substitute and Save  ──────────────────────────



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


