# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Headless Utility
#
#       This Utility contains functions and methods to git commit new Manifest Files.
#       These functions are intended for use by the Github Workflows process.
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
#                        Module Logging Instantiation                        #
#                                                                            #
##############################################################################



import logging



#######################  Always Log / Always Save  #######################



LOG = logging.getLogger('utilities.logging_utility')



##############################################################################
#                                                                            #
#                Setup Local Git Username and Email Function                 #
#                                                                            #
##############################################################################



from utilities.subprocess_utility import run_subprocess_p_open



#######################  Git Local | Username and Email  #######################



def setup_local_git_username_and_email():
    input_command =  'git config --local user.name "Reverse Telnet"'
    git_set_username_output = run_subprocess_p_open(input_command)
    input_command =  'git config --local user.email "56200159+ReverseTelnet@users.noreply.github.com"'
    git_set_email_output = run_subprocess_p_open(input_command)
    return git_set_username_output, git_set_email_output



##############################################################################
#                                                                            #
#                 Run Git Status Porcelain Command Function                  #
#                                                                            #
##############################################################################



#######################  Git Status | With Easier Parsing  #######################



def run_git_status_porcelain_command():
    input_command = f'git status --porcelain=v1'
    git_status_output = run_subprocess_p_open(input_command)
    return git_status_output



##############################################################################
#                                                                            #
#             Parse Git Status Output for File Renames Function              #
#                                                                            #
##############################################################################



from pathlib import Path
from utilities.common_utilities import two_spaces



#######################  Porcelain-Style --> In | Plumbing-Style Conversion | Validation --> Out  #######################



def validate_git_status_output(git_status_output, pwd_absolute_path, filename):
    relative_path = Path(filename).relative_to(pwd_absolute_path)
    expected_result = f'A{two_spaces}{str(relative_path)}'
    output_split = git_status_output.split('\n')
    output_stripped = [s.strip() for s in output_split]
    output_cleaned = list(filter(None, output_stripped))
    output_checked = [item for item in output_cleaned if item == expected_result]
    if output_checked == [expected_result]:
        output_validated = True
    else:
        output_validated = False
    return output_validated



##############################################################################
#                                                                            #
#                        Git Status Workflow Function                        #
#                                                                            #
##############################################################################



#######################  A Unique Solution to a Complex Problem  #######################



def git_status_workflow(pwd_absolute_path, filename):
    git_status_output = run_git_status_porcelain_command()
    output_validated = validate_git_status_output(git_status_output, pwd_absolute_path, filename)
    return output_validated, git_status_output



##############################################################################
#                                                                            #
#                    Compile Git Commit Message Function                     #
#                                                                            #
##############################################################################



#######################  Git Commit Message  #######################



def compile_git_commit_message(filename):
    version_and_signature = filename.rsplit('/', 1)[-1].strip().replace('.upm', '')
    release_version, signature = version_and_signature.split('__')
    git_commit_message = f'Check-In Commit | Release Version: {release_version} | Signature: {signature}'
    return git_commit_message



##############################################################################
#                                                                            #
#                    Compile Git Commit Command Function                     #
#                                                                            #
##############################################################################



from utilities.common_utilities import get_utc_now_iso_8601_timestamp



#######################  Git Commit Command  #######################



def compile_git_commit_command(git_commit_message):
    git_commit_timestamp = get_utc_now_iso_8601_timestamp()
    git_committer_date = f'GIT_COMMITTER_DATE="{git_commit_timestamp}"'
    commit_command = f'git commit --date="{git_commit_timestamp}" -m "{git_commit_message}"'
    git_commit_command = f'{git_committer_date} {commit_command}'
    return git_commit_command, git_commit_timestamp



##############################################################################
#                                                                            #
#                 Compile Git Commit Amend Command Function                  #
#                                                                            #
##############################################################################



#######################  Git Author Amend Command  #######################



def compile_git_commit_amend_command(git_timestamp):
    git_author = 'Reverse Telnet'
    git_email = '56200159+ReverseTelnet@users.noreply.github.com'
    git_committer_date = f'GIT_COMMITTER_DATE="{git_timestamp}"'
    author_amend_command = f'''git commit --date="{git_timestamp}" --amend --author="{git_author} <{git_email}>" --no-edit'''
    git_commit_amend_command = f'{git_committer_date} {author_amend_command}'
    return git_commit_amend_command



##############################################################################
#                                                                            #
#                   Git Commit Headless Workflow Function                    #
#                                                                            #
##############################################################################



#######################  Headless Mode | Putting It All Together  #######################



def git_commit_headless_workflow(pwd_absolute_path, new_manifest_files):
    git_set_username_output, git_set_email_output = setup_local_git_username_and_email()
    for filename in new_manifest_files:
        input_command = f'git add {filename} -f'
        git_add_result = run_subprocess_p_open(input_command)
        output_validated, git_status_output = git_status_workflow(pwd_absolute_path, filename)
        if output_validated:
            git_commit_message = compile_git_commit_message(filename)
            git_commit_command, git_commit_timestamp = compile_git_commit_command(git_commit_message)
            git_commit_result = run_subprocess_p_open(git_commit_command)
                    #
            git_commit_amend_command = compile_git_commit_amend_command(git_commit_timestamp)
            git_commit_amend_result = run_subprocess_p_open(git_commit_amend_command)
                    #
            LOG.info(f'\n\n{git_commit_result}\n\n')
            LOG.info(f'\n\n{git_commit_amend_result}\n\n')
        else:
            LOG.error(f'\n\n{git_add_result}\n\n')
            LOG.error(f'\n\n{git_status_output}\n\n')


