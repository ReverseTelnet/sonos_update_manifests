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
#                      Get Manifest File List Function                       #
#                                                                            #
##############################################################################



from pathlib import Path



#######################  Manifest File List  #######################



def get_manifest_file_list(directory='update_manifests'):
    manifests_directory = directory
    manifest_files = [item for item in Path(manifests_directory).rglob('*') if item.suffix in ('.upm', '.xml')]
    return manifest_files



##############################################################################
#                                                                            #
#                           URL Validity Function                            #
#                                                                            #
##############################################################################



from urllib.parse import urlparse



#######################  Is This a Real URL?  #######################



def is_valid_url(url):
    '''  Very Basic Check to Ensure Parsed Value is a Valid URL  '''
    try:
        parsed = urlparse(url)
        result = all([parsed.scheme, parsed.netloc])
        return result
    except:
        return False



##############################################################################
#                                                                            #
#                Parse Image Entity Installer Links Function                 #
#                                                                            #
##############################################################################



from bs4 import BeautifulSoup



#######################  Manifest File --> In | Installer Links --> Out  #######################



def parse_image_entity_installer_links(data):
    '''  Parses Manifest file for `<image model>` entity.  '''
    soup = BeautifulSoup(data, features='xml')
    all_links = soup.find_all('image')
    installer_links = set()
    for link in all_links:
        link_text = link.text
        if is_valid_url(link_text) and link_text.endswith(('exe', 'dmg')):
            installer_links.add(link_text)
    return installer_links



##############################################################################
#                                                                            #
#              Parse Manifest Files For Links Workflow Function              #
#                                                                            #
##############################################################################



from natsort import ns
from natsort import natsorted
from alive_progress import alive_bar
from utilities.common_utilities import open_text_file



#######################  Manifest Files and Links | Putting It All Together  #######################



def parse_manifest_files_for_links(manifest_files):
    all_installer_links = set()
    sorted_list = natsorted(manifest_files, alg=ns.IGNORECASE)
    bar_tile = 'Parsing Manifest Files for Desktop Downloads'
    with alive_bar(bar='filling', spinner='waves', dual_line='true', title=bar_tile) as bar:
        for file in sorted_list:
            data = open_text_file(file)
            installer_links = parse_image_entity_installer_links(data)
            for item in installer_links:
                all_installer_links.add(item)
            bar()
    return all_installer_links



##############################################################################
#                                                                            #
#                  Extract System Version from URL Function                  #
#                                                                            #
##############################################################################



#######################  Sorting Helper Function  #######################



def extract_version(url):
    filename = url.rsplit('/', 1)[-1]
    version = filename.replace('-1-3.exe', '').replace('-1-4.dmg', '').strip()
    return version



##############################################################################
#                                                                            #
#         Construct Operating System Installer Dictionaries Function         #
#                                                                            #
##############################################################################



#######################  Install File Dictionary | {version: download_url}  #######################



def construct_os_installer_dictionaries(all_installer_links):
    macos_links = [item for item in all_installer_links if item.endswith('dmg')]
    windows_links = [item for item in all_installer_links if item.endswith('exe')]
    macos_installers = {extract_version(link): link for link in macos_links}
    windows_installers = {extract_version(link): link for link in windows_links}
    return macos_installers, windows_installers



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


