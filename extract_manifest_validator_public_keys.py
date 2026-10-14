# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Extract Manifest Validator Public Keys
#
#       This code is used to extract three Public Keys from a Sonos Android APK file.
#       These public keys are then saved to the `manifest_public_keys` directory.
#       They can be used to verify any past or present Manifest File Signature.
#
#       The Public Keys are present in the both the Windows and macOS Desktop
#       Applications and the Android and Apple Mobile Applications.  In macOS,
#       they can be extracted without installing the Application, while on Windows,
#       the executable must be installed.  For compatibility across Operating
#       Systems, this script uses the Sonos-provided Android APK as the source.
#
#       The APK Files have an average size of around ~300 MB.
#
#       The script will give you an option to save the APK files or not.
#       The entire file has to be downloaded and unzipped in memory in order
#       to extract the Public Key File.  However, the downloaded contents do
#       not necessarily have to be saved for the purposes of Manifest File Validation.
#
#       If you select the option to save the APK file, it is written to the
#       directory `apk_files`.
#
#       The script will loop through known-specific Sonos-provided APK File URLs.
#       If the URL has been taken down or if the Public Keys cannot be extracted
#       from a given APK file, the script will loop to the next URL. If none of
#       the known-specific URLs yield the Public Keys, the script will attempt
#       the generic APK URL: `https://www.sonos.com/redir/controller_software_android2`
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
#                        Validator-Related Constants                         #
#                                                                            #
##############################################################################



from utilities.common_utilities import get_pwd_absolute_path



#######################  HERE - (Absolutely) Here  #######################



pwd_absolute_path = get_pwd_absolute_path()



#######################  Output Directories  #######################



apk_files_directory = f'{pwd_absolute_path}/apk_files'
public_keys_directory = f'{pwd_absolute_path}/manifest_public_keys'



#######################  Hex Patterns  #######################



hex_pattern_0096 = '30 81 9f 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 81 8d 00 30 81 89 02 81 81 00 9f f7 ec 43 6b 11 a7'
hex_pattern_0202 = '30 82 01 22 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0f 00 30 82 01 0a 02 82 01 01 00 d2 3c 47'
hex_pattern_0203 = '30 82 01 22 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0f 00 30 82 01 0a 02 82 01 01 00 d3 70 8c'



#######################  Byte Patterns  #######################



pattern_0096 = bytes.fromhex(hex_pattern_0096)
pattern_0202 = bytes.fromhex(hex_pattern_0202)
pattern_0203 = bytes.fromhex(hex_pattern_0203)



#######################  Byte Sizes  #######################



byte_size_0096 = 162
byte_size_0202 = 294
byte_size_0203 = 294



#######################  MD5 Reference Hashes  #######################



reference_md5_hash_0202 = 'ba1ef4a6396676aca6282bef83763392'
reference_md5_hash_0203 = '26e85c66aadb0b56a90261430d643ecd'
reference_md5_hash_0096 = '13a0e91343acceb103898a3a3dde1ca5'



#######################  Output Filenames  #######################



filename_0096 = f'{public_keys_directory}/ZZ0096.der'
filename_0202 = f'{public_keys_directory}/ZZ0202.der'
filename_0203 = f'{public_keys_directory}/ZZ0203.der'



#######################  Known APK File Sizes and Links  #######################



apk_sizes_and_links = {
    # '88204582':  'https://update-beta.sonos.com/software/2rZ4DF8eqv/Sonos_80.1-56190_64bit.apk',  # No `libsonoscrypto.so`
    # '88188198':  'https://update-beta.sonos.com/software/dmCadce79S/Sonos_83.1-61210_64bit.apk',  # No `libsonoscrypto.so`
    '272448205': 'https://update-beta.sonos.com/software/d278c50f-723f-494c-aab7-b3760c35ac96/Sonos_80.28.33.apk',
    '273688149': 'https://update-beta.sonos.com/software/56777aba-6ed1-40c2-8af3-baa919ed366c/Sonos_80.32.29.apk',
    '304910262': 'https://update-beta.sonos.com/software/b934f64c-66e9-4f98-8447-c311ca80b7c6/Sonos_83.00.36.apk',
    '339757559': 'https://update-beta.sonos.com/software/76c26d7b-8406-4bcc-ba6a-fda233a64235/Sonos_85.00.12.apk',
    '341211232': 'https://update-beta.sonos.com/software/78962754-cd03-411a-9305-418a6521c79e/Sonos_85.00.31.apk',
    '339022164': 'https://update-beta.sonos.com/software/8c19852f-4ac8-45ca-91bd-a50c4c9e9aca/Sonos_88.01.9.apk',
    '327874794': 'https://update-beta.sonos.com/software/542ce839-0855-4d1a-ba48-9454ee1df149/Sonos_89.00.49.apk',
    '248921485': 'https://update-software.sonos.com/software/63a302da-752e-4cf3-92f9-ced0d5992d36/Sonos_90.00.43.apk',
    'UNKNOWN':   'https://www.sonos.com/redir/controller_software_android2'
}



##############################################################################
#                                                                            #
#                Select If APK Files Should Be Saved Function                #
#                                                                            #
##############################################################################



import questionary
from utilities.common_utilities import QMARK
from utilities.common_utilities import FINGER
from utilities.common_utilities import PANACHE
from utilities.common_utilities import PRINT_NEWLINES
from utilities.common_utilities import new_line_string
from utilities.common_utilities import yes_no_to_boolean



#######################  Save Downloaded APK Files?  #######################



def select_if_apk_should_be_saved():
    PRINT_NEWLINES(1)
    instructions = f'  (Use arrow keys to move. Use <enter> to confirm selection.){new_line_string}'
    question_text = f'Save the Download APK Files? {new_line_string}'
    choices = ['Yes', 'No']
    selection = questionary.select(question_text, instruction=instructions, pointer=FINGER, qmark=QMARK, style=PANACHE, choices=choices).ask()
    save_apk_files = yes_no_to_boolean(selection)
    PRINT_NEWLINES(1)
    return save_apk_files



##############################################################################
#                                                                            #
#                      Download Sonos APK File Function                      #
#                                                                            #
##############################################################################



import requests
from rich import print as rich_print



#######################  Basic Requests Handler  #######################



def download_sonos_apk_file(url):
    PRINT_NEWLINES(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:157.0) Gecko/20100101 Firefox/157.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'close',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    try:
        response = requests.get(url, headers=headers, timeout=7)
        status_code = response.status_code
    except Exception as e: # Timeout, ConnectionError, RequestException
        rich_print(f'Request Failed: {e}')
        response = None
    else: # No Exception Hit; Check Status Code
        if status_code != 200:
            rich_print(f'HTTP Error: {status_code}')
            response = None
    return response



##############################################################################
#                                                                            #
#                      APK File Save Workflow Function                       #
#                                                                            #
##############################################################################



from utilities.write_and_save_utility import save_bytes_to_file



#######################  Response --> In | File Saved!  #######################



def apk_file_save_workflow(response):
    apk_file = response.content
    apk_name = response.url.rsplit('/', 1)[-1].strip()
    output_file = f'{apk_files_directory}/{apk_name}'
    save_bytes_to_file(output_file, apk_file)
    rich_print(f'Saved: {apk_name}\n\n')



##############################################################################
#                                                                            #
#                 Extract Crypto File From APK File Function                 #
#                                                                            #
##############################################################################



import zipfile
from io import BytesIO
from natsort import ns
from natsort import natsorted



#######################  Response --> In | Crypto File --> Out  #######################



def extract_crypto_file(response):
    response_content = BytesIO(response.content)
    with zipfile.ZipFile(response_content, 'r') as apk:
        file_list = apk.namelist()
        lib_sonos_crypto_files = natsorted([item for item in file_list if 'libsonoscrypto.so' in item], alg=ns.IGNORECASE)
        if lib_sonos_crypto_files:
            crypto_file = apk.read(lib_sonos_crypto_files[0])
        else:
            crypto_file = None
    return crypto_file



##############################################################################
#                                                                            #
#           Extract Public Key Contents From Crypto File Function            #
#                                                                            #
##############################################################################



#######################  Crypto File --> In | Public Keys Out --> Out  #######################



def extract_public_key_contents(crypto_file):
    extracted_0096 = b''
    extracted_0202 = b''
    extracted_0203 = b''
            #
    index_0096 = crypto_file.find(pattern_0096)
    index_0202 = crypto_file.find(pattern_0202)
    index_0203 = crypto_file.find(pattern_0203)
            #
    if index_0096 != -1:
        extracted_0096 = crypto_file[index_0096:index_0096 + byte_size_0096]
    if index_0202 != -1:
        extracted_0202 = crypto_file[index_0202:index_0202 + byte_size_0202]
    if index_0203 != -1:
        extracted_0203 = crypto_file[index_0203:index_0203 + byte_size_0203]
    return extracted_0096, extracted_0202, extracted_0203



##############################################################################
#                                                                            #
#                  Check Extracted DER File Hashes Function                  #
#                                                                            #
##############################################################################



from utilities.common_utilities import get_md5_hash_of_bytes



#######################  Extracted DER --> In | Validity --> Out  #######################



def check_extracted_der_hashes(extracted_0096, extracted_0202, extracted_0203):
    md5_extracted_0096 = get_md5_hash_of_bytes(extracted_0096)
    md5_extracted_0202 = get_md5_hash_of_bytes(extracted_0202)
    md5_extracted_0203 = get_md5_hash_of_bytes(extracted_0203)
    valid_0096 = True if md5_extracted_0096 == reference_md5_hash_0096 else False
    valid_0202 = True if md5_extracted_0202 == reference_md5_hash_0202 else False
    valid_0203 = True if md5_extracted_0203 == reference_md5_hash_0203 else False
    return valid_0096, valid_0202, valid_0203



##############################################################################
#                                                                            #
#                     Save Public Keys Workflow Function                     #
#                                                                            #
##############################################################################



'''
Development Notes:

    If the extracted Public Key is valid (its MD5 hash
    matches the reference MD5 hash), then it is good
    to be saved.  However, if the file has already been
    saved, it doesn't make sense to save it again.

    The use case or conditions around this occurring
    would be where the APK was downloaded, the crypto file
    was found, but not all three Public Key files could
    be successfully extracted.

    The script would then need to move onto the next
    APK URL so that the final result is that all three
    Public Keys have been extracted and saved.
'''



#######################  Validity Check --> In | If Validity Save Key/Update Global  #######################



def save_public_key_workflow(valid_0096, valid_0202, valid_0203, saved_0096, saved_0202, saved_0203):
    if valid_0096 and not saved_0096:
        save_bytes_to_file(filename_0203, extracted_0203)
        rich_print('Success! Saved: ZZ0096.der\n\n')
        saved_0096 = True
            #
    if valid_0202 and not saved_0202:
        save_bytes_to_file(filename_0202, extracted_0202)
        rich_print('Success! Saved: ZZ0202.der\n\n')
        saved_0202 = True
            #
    if valid_0203 and not saved_0203:
        save_bytes_to_file(filename_0096, extracted_0096)
        rich_print('Success! Saved: ZZ0203.der\n\n')
        saved_0203 = True
    return saved_0096, saved_0202, saved_0203



##############################################################################
#                                                                            #
#                          Putting It All Together                           #
#                                                                            #
##############################################################################



from os import makedirs
from alive_progress import alive_bar



#######################  User Input Required  #######################



save_apk_files = select_if_apk_should_be_saved()



#######################  Variables Instantiation  #######################



saved_0096 = False
saved_0202 = False
saved_0203 = False



#######################  Output Directory Creation  #######################



makedirs(public_keys_directory, exist_ok=True)
if save_apk_files:
    makedirs(apk_files_directory, exist_ok=True)



#######################  Alive Progress And URL List Setup  #######################



bar_tile = 'Downloading Sonos Android APK File'
sonos_apk_urls = list(apk_sizes_and_links.values())



#######################  if __name__ == '__main__'  #######################



PRINT_NEWLINES(1)



while not all((saved_0096, saved_0202, saved_0203)):
    with alive_bar(bar='filling', spinner='waves', dual_line='true', title=bar_tile) as bar:
        for apk_url in sonos_apk_urls:
            rich_print(f'{apk_url}\n\n')
            response = download_sonos_apk_file(apk_url)
            bar()
            if response:
                if save_apk_files:
                    apk_file_save_workflow(response)
                crypto_file = extract_crypto_file(response)
                if crypto_file:
                    extracted_0096, extracted_0202, extracted_0203 = extract_public_key_contents(crypto_file)
                    valid_0096, valid_0202, valid_0203 = check_extracted_der_hashes(extracted_0096, extracted_0202, extracted_0203)
                    saved_0096, saved_0202, saved_0203 = save_public_key_workflow(valid_0096, valid_0202, valid_0203, saved_0096, saved_0202, saved_0203)
                    if all((saved_0096, saved_0202, saved_0203)):
                        break



PRINT_NEWLINES(1)


