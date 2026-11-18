# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Download Specific Desktop Version (Sonos Desktop Software)
#
#       When you run this script, you will be presented with two choices.
#           • Operating System (macOS or Windows)
#           • Software Version
#
#       The Software Versions available depend on the selected Operating System.
#       After Selecting the Software Version, the script will open a new tab in the default browser with the download URL.
#
#       For most browsers, this means the file will automatically begin downloading.
#
# ------------------------------------------------------------------------------------------------------------------------------------



##############################################################################
#                                                                            #
#          Clear Screen, Bump to Top, And Drop Two Lines Functions           #
#                                                                            #
##############################################################################



from utilities.common_utilities import PRINT_NEWLINES
from utilities.common_utilities import get_clear_function_by_platform



#######################  Bump Console Output to the Top  #######################



CLEAR = get_clear_function_by_platform()
CLEAR()
PRINT_NEWLINES(2)



##############################################################################
#                                                                            #
#                      Select Operating System Function                      #
#                                                                            #
##############################################################################



import questionary
from utilities.common_utilities import QMARK
from utilities.common_utilities import PANACHE
from utilities.common_utilities import FINGER
from utilities.common_utilities import PRINT_NEWLINES
from utilities.common_utilities import new_line_string



#######################  Operating System Value  #######################



def select_operating_system():
    PRINT_NEWLINES(1)
    instructions = f'  (Use arrow keys to move. Use <enter> to confirm selection.){new_line_string}'
    question_text = f'Which Operating System? {new_line_string}'
    choices = ['macOS', 'Windows']
    operating_system = questionary.select(question_text, instruction=instructions, pointer=FINGER, qmark=QMARK, style=PANACHE, choices=choices).ask()
    PRINT_NEWLINES(1)
    return operating_system



##############################################################################
#                                                                            #
#                    Select Version to Download Function                     #
#                                                                            #
##############################################################################



#######################  Download Version Value  #######################



def select_version_and_get_download_url():
    PRINT_NEWLINES(1)
    instructions = f'  (Use arrow keys to move. Use <enter> to confirm selection.){new_line_string}'
    question_text = f'Which Version Do You Want to Download? {new_line_string}'
    installers = macos_installers if operating_system == 'macOS' else windows_installers
    choices = natsorted(installers.keys())
    selected_version = questionary.select(question_text, instruction=instructions, pointer=FINGER, qmark=QMARK, style=PANACHE, choices=choices).ask()
    download_url = installers[selected_version]
    PRINT_NEWLINES(1)
    return download_url



##############################################################################
#                                                                            #
#                          Putting It All Together                           #
#                                                                            #
##############################################################################



import webbrowser



#######################  if __name__ == '__main__'  #######################



operating_system = select_operating_system()
manifest_files = get_manifest_file_list()
all_installer_links = parse_manifest_files_for_links(manifest_files)
macos_installers, windows_installers = construct_os_installer_dictionaries(all_installer_links)
download_url = select_version_and_get_download_url()
webbrowser.open(download_url)


