# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Check For New Manifest Files
#
#       This script is used to download new manifest files.
#       Because every unique manifest file must have a unique Signature,
#       that Signature can be used to determine if the file already exists
#       in the local directory.
#
#
#       Master Queue Building Logic:
#           1. Get Manifest Files from Manifest Directory
#           2. Create a Dictionary of Signatures and Filenames
#           3. Parse Each Manifest File for URLs
#           4. Add URLs to a Master Queue
#           5. Swap 'Dev' and 'Prod' words in URLs
#           6  Add Swapped URLs to the Queue
#           7. Add Seed URLS to Master Queue
#
#
#       Queue Processing Logic:
#           1. Use Requests To Download The Manifest File
#           2. Check the Response Location Headers for Seed URLs
#           3. Add Location to Master Queue
#           4. Parse the Manifest File for the Signature
#           5. If the Signature is New:
#           6. Processes Manifest File for URLs
#           7. Add URLs to Master Queue
#           8. Save Manifest File
#           9. Log all the Processed Manifest (Yes, save a second time) (Verbose Mode)
#
#
#       Filename Logic:
#           Many times, Sonos will release a manifest file to a specific URL,
#           then make modifications to that manifest file.  Many times this is
#           because of some mistake (or change) needed in in a link.
#
#           Rather than keep "latest", this script keeps everything.
#           You never know what might accidentally find.
#
#           This "manifest file patching" results in the same release version
#           having multiple manifest files, though at access time, a device
#           updating would only get "latest".  The script needs to differentiate
#           between these iterations somehow, as the release version is not unique.
#
#           To that end, the first sixteen characters of manifest file's Signature
#           are appended to the release version separated by a double underscore.
#
#           A double underscore is used because of releases such as `92.0-72090-v17.7-WVKe8SuGri-RC-2-SP_1`
#           Clear a mistake in that it used an underscore instead of hyphen, but it was published this way.
#
# ------------------------------------------------------------------------------------------------------------------------------------



'''
Script Usage:

    1. Check For New Manifest Files:

        $ python check_for_new_manifest_files.py

    2. Verbose Mode

        $ python check_for_new_manifest_files.py verbose

            All Fetched Manifests will be bulk-logged as the last action in the script.
            This log is processed by both the console and file log.

    3. Validate All Repository UPM Files (in `manifest_files` directory):

        $ python check_for_new_manifest_files.py headless

            This is intended to for use by the GitHub Actions Workflow.
            It activates the `git_commit_headless_workflow` which engages
            subprocess and calls git commands.

            You should not use this mode.
    Note:

    UPM Files are ignored by .gitignore.
    A new Manifest File will not show up in `Changes not staged for commit` in `git status`.
    This is intentional.
'''



##############################################################################
#                                                                            #
#                    Derive Current Script Name Function                     #
#                                                                            #
##############################################################################



from os import path



#######################  What is the Name of the Current Running Script?  #######################



def derive_current_script_name():
    base_filename = path.basename(__file__)
    current_script, extension = path.splitext(base_filename)
    return current_script



#########################################################################################################################################################
#                                                                                                                                                       #
#                                                    Helping Relieve Sore Necks One Script at a Time                                                    #
#                                                                                                                                                       #
#########################################################################################################################################################



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



#######################################################################################################################################################
#                                                                                                                                                     #
#                                                             Functions Related to Logging                                                            #
#                                                                                                                                                     #
#######################################################################################################################################################



##############################################################################
#                                                                            #
#                               Create Logger                                #
#                                                                            #
##############################################################################



from utilities.logging_utility import instantiate_logger



#######################  Always Log / Always Save  #######################



LOG = instantiate_logger(derive_current_script_name())



##############################################################################
#                                                                            #
#                            Directory Constants                             #
#                                                                            #
##############################################################################



from utilities.common_utilities import get_pwd_absolute_path



#######################  Where Am I? Absolutely  #######################



pwd_absolute_path = get_pwd_absolute_path()



#######################  Simplifying Strings to Variables  #######################



manifests_directory = f'{pwd_absolute_path}/manifest_files'



##############################################################################
#                                                                            #
#                           Is URL Valid Function                            #
#                                                                            #
##############################################################################



from urllib.parse import urlparse



#######################  Ensure Parsed Value is a Valid URL  #######################



def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        result = all([parsed_url.scheme, parsed_url.netloc])
        return result
    except:
        return False



##############################################################################
#                                                                            #
#                 Parse Manifest Text for Signature Function                 #
#                                                                            #
##############################################################################



import re



#######################  Signature and Manifest Dictionary  #######################



def parse_manifest_text_for_signature(manifest_text, filename):
    global signatures_and_filenames
    signature = re.findall('!-- SIGNATURE:(.*) -->', manifest_text)[0]
    if signature in signatures_and_filenames:
        LOG.info(f'Existing File With Same Signature: {filename}')
    signatures_and_filenames[signature] = filename



##############################################################################
#                                                                            #
#                 Parse Response Text for Signature Function                 #
#                                                                            #
##############################################################################



#######################  Manifest Text --> In | Signature --> Out  #######################



def parse_response_text_for_signature(manifest_text):
    signature = None
    signature_matches = re.findall('!-- SIGNATURE:(.*) -->', manifest_text)[0]
    if signature_matches in signatures_and_filenames:
        known_file = signatures_and_filenames.get(signature_matches)
        LOG.info(f'Signature Already Exists In: {known_file}\n\n')
    else:
        signature = signature_matches
    return signature



##############################################################################
#                                                                            #
#                  Normalize Base Path to Base URL Function                  #
#                                                                            #
##############################################################################



#######################  Base Path --> In | Base URL --> Out  #######################



def normalize_base_path_to_base_url(base_path):
    if '^' in base_path:
        split_stripped = base_path.split('^')[0].rstrip('/')
        base_url = f'{split_stripped}/update.upm'
    else:
        base_url = base_path
    return base_url



##############################################################################
#                                                                            #
#           Normalize Broken Base Path to Valid Base Path Function           #
#                                                                            #
##############################################################################



'''
Development Notes:

    Some manifest files do not have a true URL in the Base URL entity.

    Example:

        >>> base_url="^90.0-68190"

    Rather than trying to turn this into a URL, this function
    mostly just removes the `^`.

    It doesn't really need to be a separate function, as the
    replacement could be done at the call site, but
    in case there are some other variations yet unseen as of
    this writing, the normalization is function wrapped.
'''



#######################  ^90.0-68190"--> In | 90.0-68190 --> Out  #######################



def normalize_broken_base_path_to_valid_base_path(base_path):
    base_path = base_path.replace('^', '')
    return base_path



##############################################################################
#                                                                            #
#               Normalize Base Path to Master Version Function               #
#                                                                            #
##############################################################################



'''
Development Reminder:


    >>> base_path
    'http://update-firmware.sonos.com/firmware/Prod/97.1-80312-v18.8-jZ0oXJNpeN-RC-6/^97.1-80312'

    >>> base_path.rsplit('/', 1)
    ['http://update-firmware.sonos.com/firmware/Prod/97.1-80312-v18.8-jZ0oXJNpeN-RC-6', '^97.1-80312']

    >>> base_path.rsplit('/', 1)[0]
    'http://update-firmware.sonos.com/firmware/Prod/97.1-80312-v18.8-jZ0oXJNpeN-RC-6'

    >>> base_path.rsplit('/', 1)[0].strip()
    'http://update-firmware.sonos.com/firmware/Prod/97.1-80312-v18.8-jZ0oXJNpeN-RC-6'

    >>> split_stripped.rsplit('/', 1)
    ['http://update-firmware.sonos.com/firmware/Prod', '97.1-80312-v18.8-jZ0oXJNpeN-RC-6']

    >>> split_stripped.rsplit('/', 1)[-1]
    '97.1-80312-v18.8-jZ0oXJNpeN-RC-6'

    >>> split_stripped.rsplit('/', 1)[-1].strip()
    '97.1-80312-v18.8-jZ0oXJNpeN-RC-6'

'''



#######################  Base Path --> In | Base URL --> Out  #######################



def normalize_base_path_to_master_version(base_path):
    split_stripped = base_path.rsplit('/', 1)[0].strip()
    master_version = split_stripped.rsplit('/', 1)[-1].strip()
    return master_version



##############################################################################
#                                                                            #
#                 Normalize Image Path to Image URL Function                 #
#                                                                            #
##############################################################################



#######################  Used to Identify URL Split Location  #######################



include_these = ['.bin', '.dmg', '.exe', '.upd']



#######################  Image Path --> In | Image URL --> Out  #######################



def normalize_image_path_to_url(image_path):
    if '^' in image_path:
        split_stripped = image_path.split('^')[0].rstrip('/')
        image_url = f'{split_stripped}/update.upm'
    elif any(substring in image_path for substring in include_these):
        split_stripped = image_path.rsplit('/', 1)[0].strip()
        image_url = f'{split_stripped}/update.upm'
    else:
        image_url = image_path
    return image_url



##############################################################################
#                                                                            #
#                    Parse Image Links Workflow Function                     #
#                                                                            #
##############################################################################



#######################  Exclude URL If It Contains This Text  #######################



exclude_these = ['market://', '.html', 'appstore', 'testflight', 'Roundhouse', 'Duke']



#######################  Image URL Parse and Normalize Workflow  #######################



def parse_image_links_workflow(soup):
    global to_investigate
    image_links   = soup.find_all('image')
    image_texts   = set([item.text for item in image_links])
    exclude_texts = set([item for item in image_texts if any(substring in item for substring in exclude_these)])
    clean_texts   = set([item for item in image_texts if not any(substring in item for substring in exclude_these)])
    valid_texts   = set([item for item in clean_texts if is_valid_url(item)])
    parsed_texts  = set([normalize_image_path_to_url(item) for item in valid_texts])
    to_investigate.update(exclude_texts)
    return parsed_texts



##############################################################################
#                                                                            #
#                Parse Manifest Text for Hyperlinks Function                 #
#                                                                            #
##############################################################################



from bs4 import BeautifulSoup



#######################  Manifest Text --> In | Hyperlinks --> Out  #######################



def parse_manifest_text_for_hyperlinks(manifest_text):
    hyperlinks = set()
    soup = BeautifulSoup(manifest_text, features='xml')
    base_path = soup.update_manifest.get('base_url')
            #
    if base_path and is_valid_url(base_path):
        base_url = normalize_base_path_to_base_url(base_path)
        hyperlinks.add(base_url)
    elif base_path and not is_valid_url(base_path):
        base_path = normalize_broken_base_path_to_valid_base_path(base_path)
    else:
        base_path = None
            #
    parsed_texts = parse_image_links_workflow(soup)
    if parsed_texts:
        for item in parsed_texts:
            hyperlinks.add(item)
    return hyperlinks, base_path



##############################################################################
#                                                                            #
#                 Swap Prod and Dev Words - Helper Function                  #
#                                                                            #
##############################################################################



#######################  Prod ⤺⤻ Dev | The Switcheroo  #######################



def swap_prod_and_dev_words(text):
    if 'Prod' in text:
        result = text.replace('Prod', 'Dev')
    elif 'Dev' in text:
        result = text.replace('Dev', 'Prod')
    else:
        result = text
    return result



##############################################################################
#                                                                            #
#                              Headers Constant                              #
#                                                                            #
##############################################################################



#######################  A Constant, but Lower Case  #######################



request_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'close',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:154.0) Gecko/20100101 Firefox/154.0'
}



##############################################################################
#                                                                            #
#                        Fetch Manifest URL Function                         #
#                                                                            #
##############################################################################



import requests



#######################  URL --> In | Response --> Out  #######################



def fetch_manifest_url(url):
    try:
        response = requests.get(url, headers=request_headers, timeout=5)
        if response.status_code == 200:
            return response
    except Exception as e:
        LOG.error(f'  ERROR fetching {url}: {e}')
    return None



##############################################################################
#                                                                            #
#                             Seed URL Constants                             #
#                                                                            #
##############################################################################



'''
Development Notes:

    Some of these URLs are in the Known 404 URL List.

    However, they are included to ensure all the possible public URL variations are listed
    for regular, stage, perf, and test for both Software Gen 1 and Software Gen 2 Links.
'''



#######################  Gen 1 and Gen 2 Master Links  #######################



SEED_URLS = [
    'http://update.sonos.com/firmware/swgen/1/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=25&cmin=0&cbld=34',
    'http://update-stage.sonos.com/firmware/swgen/1/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=25&cmin=0&cbld=34',
    'http://update-perf.sonos.com/firmware/swgen/1/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=25&cmin=0&cbld=34',
    'http://update-test.sonos.com/firmware/swgen/1/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=25&cmin=0&cbld=34',
            #
    'http://update.sonos.com/firmware/swgen/2/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=81&cmin=0&cbld=52',
    'http://update-stage.sonos.com/firmware/swgen/2/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=81&cmin=0&cbld=52',
    'http://update-perf.sonos.com/firmware/swgen/2/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=81&cmin=0&cbld=52',
    'http://update-test.sonos.com/firmware/swgen/2/latest/update.upm?sonosid=Anonymous&householdid=nohhid&cmaj=81&cmin=0&cbld=52',
]



##############################################################################
#                                                                            #
#        Parse Saved Manifest Files for Hyperlinks Workflow Function         #
#                                                                            #
##############################################################################



from natsort import ns
from natsort import natsorted
from utilities.common_utilities import open_text_file



#######################  Manifest Files --> In | Parsed Hyperlinks --> Out  #######################



def parse_saved_manifests_for_hyperlinks_workflow(manifests_sorted):
    hyperlinks_set = set()
    for file in manifests_sorted:
        text_data = open_text_file(file)
        parse_manifest_text_for_signature(text_data, file.name)
        hyperlinks, _ = parse_manifest_text_for_hyperlinks(text_data)
        for item in hyperlinks:
            hyperlinks_set.add(item)
            hyperlinks_set.add(swap_prod_and_dev_words(item))
    parsed_hyperlinks = natsorted(hyperlinks_set, alg=ns.IGNORECASE)
    return parsed_hyperlinks



##############################################################################
#                                                                            #
#                    Construct Manifest Filename Function                    #
#                                                                            #
##############################################################################



import time



#######################  Signature and Base Path --> In | Manifest Filename --> Out  #######################



def construct_manifest_filename(signature, base_path):
    first_sixteen = signature[0:16]
    if base_path:
        master_version = normalize_base_path_to_master_version(base_path)
        filename = f'{manifests_directory}/{master_version}__{first_sixteen}.upm'
    else:
        master_version = 'unknown_version'
        epoch_timestamp = int(time.time())
        filename = f'{manifests_directory}/{master_version}_{epoch_timestamp}__{first_sixteen}.upm'
    return filename



##############################################################################
#                                                                            #
#                 Process Request Response Workflow Function                 #
#                                                                            #
##############################################################################



'''
Development Notes:

    The Gen 2 Seed URLs will have a Content Location in the response headers.
    Other URLs might, potentially, but the Seed URLs will.

    The Content Location URL must be used for the Manifest's Filename for Seed URLs.

    Function Logic:

        1. Check Response Headers for Content Location
            - Add to Queue
        2. Parse for Signature
            - If Signature
                - Save File
                - Add Links to Queue

        The Master Queue logic is also tracking a `already_visited` set.
        So even if this function adds an item to the Master Queue,
        it will ultimately get skipped because it's already been visited.
'''



from utilities.write_and_save_utility import save_string_to_text_file



#######################  Parse Signature and Links | Add to Master Queue  #######################



def process_response_workflow(response, is_seed=False):
    global master_queue
    global all_responses
    filename = None
    cl_headers = response.headers.get('Content-Location', '')
    if is_valid_url(cl_headers):
        content_location = cl_headers
        master_queue.append(content_location)
    else:
        content_location = None
    response_log_text = f'\n\n# {response.url}\n\n{response.text}\n\n'
    all_responses.append(response_log_text)
    signature = parse_response_text_for_signature(response.text)
    if signature: # It's New, So Save It and Parse It.
        LOG.info('New Signature Found!')
        hyperlinks, base_path = parse_manifest_text_for_hyperlinks(response.text)
        if not is_seed:
            filename = construct_manifest_filename(signature, base_path)
        elif is_seed:
            if content_location:
                filename = construct_manifest_filename(signature, base_path=content_location)
            elif not content_location:
                filename = construct_manifest_filename(signature, base_path=None)
        save_string_to_text_file(filename, response.text)
        for item in hyperlinks:
            master_queue.append(item)
            master_queue.append(swap_prod_and_dev_words(item))
    return filename, response.text



##############################################################################
#                                                                            #
#                          Putting It All Together                           #
#                                                                            #
##############################################################################



import sys
import time
from pathlib import Path
from rich import print as rich_print
from utilities.known_404_urls import known_404_url_list
from utilities.headless_utility import git_commit_headless_workflow



#######################  Headless Mode  #######################



headless_mode = True if len(sys.argv) > 1 and sys.argv[1] == 'headless' else False
verbose_mode  = True if len(sys.argv) > 1 and sys.argv[1] == 'verbose'  else False



#######################  Manifest Files Workflow  #######################



manifest_files = [item for item in Path(manifests_directory).glob('*') if item.suffix in ('.upm', '.xml')]
manifests_sorted = natsorted(manifest_files, alg=ns.IGNORECASE)



#######################  Signatures, Filenames, and Parsed Hyperlinks Workflow  #######################



to_investigate = set()
signatures_and_filenames = {}
parsed_hyperlinks = parse_saved_manifests_for_hyperlinks_workflow(manifests_sorted)



#######################  Build Queue Workflow  #######################



master_queue = SEED_URLS + parsed_hyperlinks



#######################  Objects Instantiation  #######################



all_responses = []
already_visited = set()
new_manifest_files = set()
known_404_url_set = set(known_404_url_list)
good_urls = set()



#######################  if __name__ == '__main__':  #######################



while master_queue:
    queue_length = len(master_queue)
    url = master_queue.pop(0)
    rich_print(f'\n{"-" * 130}\n\n')
    rich_print(f'Queue Length: {queue_length}')
    rich_print(f'On: {url}')
    if url in known_404_url_set:
        print('Skipping UR: - Known Invalid URL\n\n')
    else:
        if url not in already_visited:
            print('\n\n')
            already_visited.add(url)
            response = fetch_manifest_url(url)
            if response:
                good_urls.add(url)
                if url in SEED_URLS:
                    manifest_filename, response_text = process_response_workflow(response, is_seed=True)
                else:
                    manifest_filename, response_text = process_response_workflow(response)
                if manifest_filename:
                    new_manifest_files.add((manifest_filename, response_text))
            elif not response:
                print('No Response from URL\n\n')
                known_404_url_set.add(url)
        elif url in already_visited:
            print('Skipping URL, Already Visited\n\n')



#######################  Verbose Mode Operations  #######################



if verbose_mode:
    LOG.removeHandler(LOG.handlers[0]) # Remove Console Handler
    for item in all_responses:
        LOG.info(f'\n\n{item}\n\n')



#######################  Headless Mode | Github Workflow  #######################



if headless_mode:
    for item in all_responses:
        LOG.info(f'\n\n{item}\n\n')
        time.sleep(.3)
    if new_manifest_files:
        new_manifest_filenames = [item[0] for item in new_manifest_files]
        git_commit_headless_workflow(pwd_absolute_path, new_manifest_filenames)
    elif not new_manifest_files:
        LOG.info(f'No New Manifest Files')


