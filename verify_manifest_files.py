# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Verify Manifest Files
#
#       This script is used to validate one or more manifest files.
#
#       The Manifest File Validation Public Key Files must be present in the
#       directory `manifest_public_keys`.  They must be valid, in that their
#       MD5 hash matches the known-good value reference MD5 hash.
#
#       Missing one or more Public Key?
#           See: `extract_manifest_validator_public_keys.py`
#
#       This script uses `sys.argv` to determine which file or directory to
#       validate. If not argument is supplied, the script validates the
#       Manifest Files in the `manifest_files` directory.
#
# ------------------------------------------------------------------------------------------------------------------------------------



'''
Script Usage:

    1. Validate a Single File:

        $ python verify_manifest_files.py /Users/ReverseTelnet/Downloads/latest.upm

    2. Validate All UPM Files in a Directory:

        $ python verify_manifest_files.py /Users/ReverseTelnet/manifest_file_collection

    3. Validate All Repository UPM Files (in `manifest_files` directory):

        $ python verify_manifest_files.py
'''



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



#######################  Manifest Keys Directory  #######################



public_keys_directory = f'{pwd_absolute_path}/manifest_public_keys'



#######################  MD5 Reference Hashes  #######################



reference_md5_hash_0202 = 'ba1ef4a6396676aca6282bef83763392'
reference_md5_hash_0203 = '26e85c66aadb0b56a90261430d643ecd'
reference_md5_hash_0096 = '13a0e91343acceb103898a3a3dde1ca5'



#######################  Output Filenames  #######################



filename_0096 = f'{public_keys_directory}/ZZ0096.der'
filename_0202 = f'{public_keys_directory}/ZZ0202.der'
filename_0203 = f'{public_keys_directory}/ZZ0203.der'



##############################################################################
#                                                                            #
#                   Create Public Key Dictionary Function                    #
#                                                                            #
##############################################################################



from Crypto.PublicKey import RSA



#######################  Public Keys --> In | {filename: RSA} --> Out  #######################



def create_public_keys_dictionary():
    public_keys_dictionary = {
        'ZZ0096': RSA.import_key(open('manifest_public_keys/ZZ0096.der', 'rb').read()),
        'ZZ0202': RSA.import_key(open('manifest_public_keys/ZZ0202.der', 'rb').read()),
        'ZZ0203': RSA.import_key(open('manifest_public_keys/ZZ0203.der', 'rb').read())
    }
    return public_keys_dictionary



##############################################################################
#                                                                            #
#                   Construct Manifest File List Function                    #
#                                                                            #
##############################################################################



from pathlib import Path



#######################  Input Object --> In | Manifest Files --> Out  #######################



def construct_manifest_file_list(input_object):
    if Path(input_object).is_file():
        manifest_files = [input_object]
    elif Path(input_object).is_dir():
        manifest_files = [item for item in Path(input_object).rglob('*') if item.suffix in ('.upm', '.xml')]
    return manifest_files



##############################################################################
#                                                                            #
#                      Find Body and Signature Function                      #
#                                                                            #
##############################################################################



from rich import print as rich_print



#######################  Finds Body, Signature | Handles Exceptions  #######################



def find_body_and_signature(file, contents):
    body = None
    sig_comment = None
    signature = None
    # No Signature Line
    if b'<!-- SIGNATURE:' not in contents:
        rich_print(f'[#C21858]Signature Line Not Found[/#C21858] --> {file}')
    else:
        try:
            body, sig_comment = contents.rsplit(b'<!-- SIGNATURE:', 1)
            signature = bytes.fromhex(sig_comment.split(b'-->')[0].strip().decode())
            # Empty Signature
            if signature == b'':
                rich_print(f'[#C21858]Signature Value Empty[/#C21858] --> {file}')
            # Empty Body
            if body == b'':
                rich_print(f'[#C21858]Body Value Empty[/#C21858] --> {file}')
        # Signature Invalid Characters
        except ValueError as error:
            rich_print(f'[#C21858]{error}[/#C21858] --> {file}')
    return body, signature



##############################################################################
#                                                                            #
#                        If Name Equals Main Function                        #
#                                 ¯\_(ツ)_/¯                                 #
#                                                                            #
##############################################################################



from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from utilities.common_utilities import open_file_as_bytes



#######################  ᕦ_(ツ)_ᕤ  #######################



def if_name_equals_main(manifest_files):
    while manifest_files:
        file = manifest_files[0]
        contents = open_file_as_bytes(file)
        body, signature = find_body_and_signature(file, contents)
        if all((body, signature)):
            validated = False
            hashed_body = SHA256.new(body)
            for der_file, pub_key in public_keys_dictionary.items():
                try:
                    pkcs1_15.new(pub_key).verify(hashed_body, signature)
                    print(f'Validated by {der_file} --> {file}')
                    _ = manifest_files.pop(0)
                    validated = True
                except ValueError:
                    continue
            if not validated:
                rich_print(f'[#C21858]Manifest Could Not Be Validated[/#C21858] --> {file}')
                _ = manifest_files.pop(0)
        else:
            _ = manifest_files.pop(0)



##############################################################################
#                                                                            #
#                          Putting It All Together                           #
#                                                                            #
##############################################################################



import sys
from utilities.common_utilities import does_file_exist
from utilities.common_utilities import does_folder_exist
from utilities.common_utilities import open_file_as_bytes
from utilities.common_utilities import get_md5_hash_of_file



#######################  File and Directory Check  #######################



public_keys_directory_exists = does_folder_exist(public_keys_directory)
zz0096_exists = does_file_exist(filename_0096)
zz0202_exists = does_file_exist(filename_0202)
zz0203_exists = does_file_exist(filename_0203)



#######################  Dump and Run - Part I  #######################



if not public_keys_directory_exists:
    print('Error: Manifest Public Keys Directory Does Not Exist.\n\n')
    sys.exit(1)



if not zz0096_exists:
    print('Error: ZZ0096.der File Not Found in Manifest Public Keys Directory.\n\n')
    sys.exit(96)


if not zz0202_exists:
    print('Error: ZZ00202.der File Not Found in Manifest Public Keys Directory.\n\n')
    sys.exit(202)



if not zz0203_exists:
    print('Error: ZZ00203.der File Not Found in Manifest Public Keys Directory.\n\n')
    sys.exit(203)



#######################  Hash Public Keys  #######################



md5_hash_zz0096 = get_md5_hash_of_file(filename_0096)
md5_hash_zz0202 = get_md5_hash_of_file(filename_0202)
md5_hash_zz0203 = get_md5_hash_of_file(filename_0203)



#######################  Dump and Run - Part II  #######################



if md5_hash_zz0096 != reference_md5_hash_0096:
    print(f'MD5 Hash of ZZ0096.der Does Not Match Reference MD5 Hash')
    print(f'{md5_hash_zz0096} <--> {reference_md5_hash_0096}')
    sys.exit(1)



if md5_hash_zz0202 != reference_md5_hash_0202:
    print(f'MD5 Hash of ZZ0202.der Does Not Match Reference MD5 Hash')
    print(f'{md5_hash_zz0202} <--> {reference_md5_hash_0202}')
    sys.exit(1)



if md5_hash_zz0203 != reference_md5_hash_0203:
    print(f'MD5 Hash of ZZ0203.der Does Not Match Reference MD5 Hash')
    print(f'{md5_hash_zz0203} <--> {reference_md5_hash_0203}')
    sys.exit(1)



#######################  Where Should I Look?  #######################



input_object = sys.argv[1] if len(sys.argv) > 1 else 'manifest_files'



#######################  If You Build It -> They Will Check Their Manifests  #######################



public_keys_dictionary = create_public_keys_dictionary()
manifest_files = construct_manifest_file_list(input_object)



####################### ..·´¯·.´¯·...·´¯·.. go, gO, GO!! ..·´¯·.´¯·...·´¯·..  #######################



if_name_equals_main(manifest_files)



PRINT_NEWLINES(3)


