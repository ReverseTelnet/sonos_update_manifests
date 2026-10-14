# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Write and Save Utilities
#
#       This Utility File contains functions used to save content to files.
#
# ------------------------------------------------------------------------------------------------------------------------------------



##############################################################################
#                                                                            #
#                         chmod 600 Opener Function                          #
#                                                                            #
##############################################################################



#######################  rw------- | Owner Read / Owner Write  #######################



def chmod_600_opener(path, flags):
    from os import open
    return open(path, flags, 0o600)



##############################################################################
#                                                                            #
#           Standard Last Index - Write List to Text File Function           #
#                                                                            #
##############################################################################



'''
Function Notes:

    Used to Write a List to a text file.
    Each Index in the List is written on a separate line.
    No special treatment is given to the last index.
'''



#######################  Always Log / Always Save  #######################



def save_list_to_text_file(filename, a_variable, write_mode='w', opener=None):
    with open(filename, write_mode, encoding='utf-8', opener=opener) as f:
        for line in a_variable:
            f.write(f'{line}')



##############################################################################
#                                                                            #
#                     Write String to Text File Function                     #
#                                                                            #
##############################################################################



'''
Function Notes:

    Used to Write a Pure String to a text file.
    This function should be used when the string has carriage returns already present in the text.
'''



#######################  Always Log / Always Save  #######################



def save_string_to_text_file(filename, a_variable, write_mode='w', opener=None):
    with open(filename, write_mode, encoding='utf-8', opener=opener) as f:
        f.write(a_variable)



##############################################################################
#                                                                            #
#                    Write Variable to JSON File Function                    #
#                                                                            #
##############################################################################



'''
Function Notes:

    Used to Write a Variable to a JSON File.
    This function assumes the variable can be converted to JSON.
    It provides an Indent of Four (4) for readability.
'''


import json



#######################  Always Log / Always Save  #######################



def save_to_json_file(filename, a_variable, opener=None):
    with open(filename, mode = 'w', opener=opener) as f:
        json_payload = json.dumps(a_variable, indent=4)
        f.write(json_payload)



##############################################################################
#                                                                            #
#                   Write Binary Variable to File Function                   #
#                                                                            #
##############################################################################



'''
Function Notes:

    Used to Write Raw Bytes to a File.
'''



#######################  Always Log / Always Save  #######################



def save_bytes_to_file(filename, a_variable, write_mode='wb', opener=None):
    with open(filename, write_mode, opener=opener) as f:
        f.write(a_variable)


