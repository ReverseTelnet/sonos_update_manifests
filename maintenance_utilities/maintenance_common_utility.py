# ╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
# │                                                                                                                                    │
# │     Maintenance Common Utilities                                                                                                   │
# │                                                                                                                                    │
# │         This Utility File contains common functions used by Maintenance Utilities in this repository.                              │
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
# │                    Compile Git Commit Message Function                   │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



import time
from pathlib import Path



#  ──────────────────────────  Git Commit Message  ──────────────────────────



def compile_utility_git_commit_message(pwd_absolute_path, baseline_utility):
    relative_path = Path(baseline_utility).relative_to(f'{pwd_absolute_path}/utilities')
    no_suffix = relative_path.with_suffix('')
    name_split = no_suffix.name.split('_')
    conjoined = ' '.join([item.title() for item in name_split])
    git_commit_message = f'Updated {conjoined} | {int(time.time())} | {conjoined} Utility'
    return git_commit_message



# ╭──────────────────────────────────────────────────────────────────────────╮
# │                                                                          │
# │                   Git Commit Headless Workflow Function                  │
# │                                                                          │
# ╰──────────────────────────────────────────────────────────────────────────╯



from utilities.headless_utility import git_status_workflow
from utilities.subprocess_utility import run_subprocess_p_open
from utilities.headless_utility import compile_git_commit_command
from utilities.headless_utility import compile_git_commit_amend_command
from utilities.headless_utility import setup_local_git_username_and_email



#  ───────────  Headless Mode | Utility File Git Commit Workflow  ───────────



def utility_file_git_commit_headless_workflow(pwd_absolute_path, baseline_utility):
    git_set_username_output, git_set_email_output = setup_local_git_username_and_email()
    input_command = f'git add {baseline_utility} -f'
    git_add_result = run_subprocess_p_open(input_command)
    output_validated, git_status_output = git_status_workflow(pwd_absolute_path, baseline_utility, 'MODIFY')
    if output_validated:
        git_commit_message = compile_utility_git_commit_message(pwd_absolute_path, baseline_utility)
        git_commit_command, git_commit_timestamp = compile_git_commit_command(git_commit_message)
        git_commit_result = run_subprocess_p_open(git_commit_command)
                #
        git_commit_amend_command = compile_git_commit_amend_command(git_commit_timestamp)
        git_commit_amend_result = run_subprocess_p_open(git_commit_amend_command)
                #
        result_01 = git_commit_result
        result_02 = git_commit_amend_result
        error = False
    else:
        result_01 = git_add_result
        result_02 = git_status_output
        error = True
    return result_01, result_02, error


