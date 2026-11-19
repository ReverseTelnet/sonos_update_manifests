# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     Desktop Versions Utility                                                                                                       │
# │                                                                                                                                    │
# │         This Utility File contains common functions related to downloading desktop versions of Sonos Software.                     │
# │         It is used by both the repository root script `download_specific_desktop_version` and the Maintenance                      │
# │         Utilities `update_known_macos_versions` and `update_known_windows_versions`.                                               │
# │                                                                                                                                    │
# │                                                                                                                                    │
# ╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                      Get Manifest File List Function                     │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from pathlib import Path



#  ──────────────────────────  Manifest File List  ──────────────────────────



def get_manifest_file_list(directory='manifest_files'):
    manifests_directory = directory
    manifest_files = [item for item in Path(manifests_directory).rglob('*') if item.suffix in ('.upm', '.xml')]
    return manifest_files



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                           URL Validity Function                          │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from urllib.parse import urlparse



#  ──────────────────────────  Is This a Real URL?  ──────────────────────────



def is_valid_url(url):
    '''  Very Basic Check to Ensure Parsed Value is a Valid URL  '''
    try:
        parsed = urlparse(url)
        result = all([parsed.scheme, parsed.netloc])
        return result
    except:
        return False



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                Parse Image Entity Installer Links Function               │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from bs4 import BeautifulSoup



#  ────────────  Manifest File --> In | Installer Links --> Out  ────────────



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



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │              Parse Manifest Files For Links Workflow Function            │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from natsort import ns
from natsort import natsorted
from alive_progress import alive_bar
from utilities.common_utilities import open_text_file



#  ──────────  Manifest Files and Links | Putting It All Together  ──────────



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



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                  Extract System Version from URL Function                │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



#  ────────────────────────  Sorting Helper Function  ────────────────────────



def extract_version(url):
    filename = url.rsplit('/', 1)[-1]
    version = filename.replace('-1-3.exe', '').replace('-1-4.dmg', '').strip()
    return version



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │         Construct Operating System Installer Dictionaries Function       │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



#  ───────────  Install File Dictionary | {version: download_url}  ───────────



def construct_os_installer_dictionaries(all_installer_links):
    macos_links = [item for item in all_installer_links if item.endswith('dmg')]
    windows_links = [item for item in all_installer_links if item.endswith('exe')]
    macos_installers = {extract_version(link): link for link in macos_links}
    windows_installers = {extract_version(link): link for link in windows_links}
    return macos_installers, windows_installers


