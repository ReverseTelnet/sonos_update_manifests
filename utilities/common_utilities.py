# ------------------------------------------------------------------------------------------------------------------------------------
#   Common Utilities
#
#       This Utility File contains common functions used by scripts in this repository.
#
# ------------------------------------------------------------------------------------------------------------------------------------



##############################################################################
#                                                                            #
#                Absolute Path Imports - Enablement Function                 #
#                                                                            #
##############################################################################



#######################  Enables Absolute Path Imports  #######################



def enable_absolute_imports():
    import sys
    from os import getcwd
    PWD = getcwd()
    if PWD in sys.path:
        pass
    else:
        sys.path.append(PWD)



enable_absolute_imports()



##############################################################################
#                                                                            #
#                           White-Spacing Function                           #
#                                                                            #
##############################################################################



#######################  Carriage Return ('New Line String') Function  #######################



def PRINT_NEWLINES(number: int):
    for _ in range(number):
        print()



##############################################################################
#                                                                            #
#                        Lower Case Spacer Constants                         #
#                                                                            #
##############################################################################



#######################  Variables Are Better Than Blank Spaces  #######################



zero_spaces = ''
one_space = ' '
two_spaces = '  '
three_spaces = '   '
four_spaces = '    '
eight_spaces = '        '
twelve_spaces = '            '
sixteen_spaces = '                '
twenty_four_spaces = '                        '
twenty_eight_spaces = '                            '
thirty_two_spaces   = '                                '
new_line_string = '\n'
ascii_waves = '..·´¯·.´¯·...·´¯·..'
reverse_ascii_waves = '..·¯´·...·¯´.·¯´·.'



##############################################################################
#                                                                            #
#                      Open and Load JSON File Function                      #
#                                                                            #
##############################################################################



import json



#######################  Open File | Read as JSON  #######################



def open_json_file(filename):
    with open (filename, mode = 'r') as f:
        data = json.load(f)
    return data



##############################################################################
#                                                                            #
#                    Open and Load File as Bytes Function                    #
#                                                                            #
##############################################################################



#######################  Open File | Read as Bytes  #######################



def open_file_as_bytes(filename):
    with open (filename, mode = 'rb') as f:
        contents = f.read()
    return contents



##############################################################################
#                                                                            #
#                      Open and Load Text File Function                      #
#                                                                            #
##############################################################################



#######################  Open File | Read as Text | Ignore Errors  #######################



def open_text_file(filename):
    with open(filename, 'r', encoding='utf-8-sig', errors='ignore') as f:
        text_data = f.read()
    return text_data



##############################################################################
#                                                                            #
#                       Get MD5 Hash of Bytes Function                       #
#                                                                            #
##############################################################################



import hashlib



#######################  Bytes --> In | MD5 Hash --> Out  #######################



def get_md5_hash_of_bytes(some_bytes):
    md5_hash = hashlib.md5(some_bytes).hexdigest()
    return md5_hash



##############################################################################
#                                                                            #
#                       Get MD5 Hash of File Function                        #
#                                                                            #
##############################################################################



#######################  Filename --> In | File MD5 Hash --> Out  #######################



def get_md5_hash_of_file(filename):
    with open(filename, 'rb', buffering=0) as f:
        md5_hash = hashlib.file_digest(f, 'md5').hexdigest()
        return md5_hash



##############################################################################
#                                                                            #
#                Get Present Working Directory (PWD) Function                #
#                                                                            #
##############################################################################



from os import getcwd



#######################  HERE - Literally (Actually)  #######################



PWD = getcwd()



##############################################################################
#                                                                            #
#          Get Absolute Path for Present Working Directory Function          #
#                                                                            #
##############################################################################



from os import path



#######################  HERE - (Absolutely) Here  #######################



def get_pwd_absolute_path():
    PWD = getcwd()
    pwd_absolute_path = path.abspath(PWD)
    return pwd_absolute_path



##############################################################################
#                                                                            #
#                Clear Screen and Preserve Rollback Function                 #
#                                                                            #
##############################################################################



# https://stackoverflow.com/questions/22885780/python-clear-the-screen
# https://apple.stackexchange.com/questions/31872/how-do-i-reset-the-scrollback-in-the-terminal-via-a-shell-command/113168#113168



#######################  macOS and Linux  #######################



def macos_clear_and_keep_roll_back():
    print('\033c\033[1J')



#######################  Windows  #######################



def windows_clear_and_keep_roll_back():
    print('\033[2J\033[H')



##############################################################################
#                                                                            #
#                   Get Clear Screen By Platform Function                    #
#                                                                            #
##############################################################################



#######################  Bumps Console to the Top of Screen  #######################



def get_clear_function_by_platform():
    from sys import platform
    if platform == 'darwin':
        CLEAR = macos_clear_and_keep_roll_back
    elif platform == 'win32':
        CLEAR = windows_clear_and_keep_roll_back
    elif platform == 'linux' or platform == 'linux2':
        CLEAR = macos_clear_and_keep_roll_back
    else:
        def clear_for_unknown_platform():
            print('\n\n\n\n\n\n')
        CLEAR = clear_for_unknown_platform
    return CLEAR



##############################################################################
#                                                                            #
#                              Pointer Constant                              #
#                                                                            #
##############################################################################



import emoji



#######################  ---> But in Emoji  #######################



FINGER = emoji.emojize(':backhand_index_pointing_right:')



##############################################################################
#                                                                            #
#                             Style and Panache                              #
#                                                                            #
##############################################################################



# https://questionary.readthedocs.io/en/stable/pages/advanced.html#themes-styling



from questionary import Style as Q_STYLE



#######################  Textual Accoutrements - Part 1  #######################



PANACHE = Q_STYLE(
    [
        ('qmark', 'fg:#0087FF bold'),       # Token in Front of the Question
        ('question', 'bold'),               # Question Text
        ('pointer', 'fg:#87FF00 bold'),     # Pointer Used in Select and Checkbox Prompts
        ('highlighted','fg:#87FF00 bold')   # Pointed-At Choice in Select and Checkbox Prompts
    ]
)



#######################  Textual Accoutrements - Part 2  #######################



MAKE_IT_POP = Q_STYLE(
    [
        ('qmark', 'fg:#0087FF bold'),       # Token in Front of the Question
        ('question', 'fg:#FC24E1 bold')    # Question Text
    ]
)



#######################  Textual Accoutrements - Questionary Token Constant  #######################



QMARK = '??'



##############################################################################
#                                                                            #
#                         File Exists Check Function                         #
#                                                                            #
##############################################################################



#######################  Does The File Exist?  #######################



def does_file_exist(file_path):
    file_exists = path.isfile(file_path)
    return file_exists



##############################################################################
#                                                                            #
#                        Folder Exists Check Function                        #
#                                                                            #
##############################################################################



#######################  Does The Folder Exist?  #######################



def does_folder_exist(folder_path):
    folder_exists = path.exists(folder_path)
    return folder_exists



##############################################################################
#                                                                            #
#                      True / False Normalizer Function                      #
#                                                                            #
##############################################################################



#######################  Returns a Boolean From None-Boolean Input  #######################



def yes_no_to_boolean(value):
    if value == 'Yes':
        result = True
    elif value == 'No':
        result = False
    return result



##############################################################################
#                                                                            #
#                  Get UTC Now ISO 8601 Timestamp Function                   #
#                                                                            #
##############################################################################



from datetime import datetime
from datetime import timezone



#######################  UTC Timestamp in ISO 8601 With Time Zone Offset  #######################



def get_utc_now_iso_8601_timestamp():
    utc_now = datetime.now(timezone.utc)                        # Example: datetime.datetime(2026, 3, 3, 23, 14, 48, 179397, tzinfo=datetime.timezone.utc)
    iso_timestamp = utc_now.strftime('%Y-%m-%d %H:%M:%S %z')    # Example: '2026-03-03 23:14:48 +0000'
    return iso_timestamp



##############################################################################
#                                                                            #
#           Convert Epoch Timestamp to ISO 8601 Timestamp Function           #
#                                                                            #
##############################################################################



# https://stackoverflow.com/a/27506674



#######################  ISO 8601 From Unix Epoch Timestamp  #######################



def convert_epoch_to_iso8601(epoch_timestamp):
    '2025-10-31 15:17:42 +0000'
    date_time_object = datetime.fromtimestamp(epoch_timestamp, timezone.utc)
    iso_timestamp = date_time_object.strftime('%Y-%m-%d %H:%M:%S %z')
    return iso_timestamp


