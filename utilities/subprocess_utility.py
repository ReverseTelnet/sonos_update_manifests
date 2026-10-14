# ------------------------------------------------------------------------------------------------------------------------------------
#   Subprocess Utilities
#
#       This Utility File contains functions and methods used to run terminal commands via the subprocess module.
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



#######################################################################################################################################################
#                                                                                                                                                     #
#                                                         Various Subprocess-Related Functions                                                        #
#                                                                                                                                                     #
#######################################################################################################################################################



'''
Further Details:

    The following Stack Overflow post provides interesting context and details on various subprocess methods.

        https://stackoverflow.com/questions/38088631/what-is-a-practical-difference-between-check-call-check-output-call-and-popen-m


    For the Official documentation:

        https://docs.python.org/3/library/subprocess.html
'''



##############################################################################
#                                                                            #
#                          Run Subprocess Function                           #
#                                                                            #
##############################################################################



'''
Development Notes:

    The following function immediately prints its output to the terminal.
    There is no option or ability to store the output in a variable.


            >>> run_subprocess('ls -al')
            total 1672
            drwxr-xr-x@  84 reversetelnet  staff    2688 Mar  3 22:10 .
            drwxr-xr-x@  59 reversetelnet  staff    1888 Nov 19 17:11 ..
            -rw-r--r--@   1 reversetelnet  staff   22532 Mar  2 19:44 .DS_Store
            drwxr-xr-x   18 reversetelnet  staff     576 Mar  3 22:04 .git


    It has basic exception catches, mostly to catch incorrect commands


        >>> run_subprocess('ls -zzzz')
        ls: invalid option -- z
        usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
        Command 'ls -zzzz' returned non-zero exit status 1.
        >>>
'''



from rich import print as rich_print



#######################  Run Terminal Shell Commands  #######################



def run_subprocess(input_command):
    import subprocess
    try:
        subprocess.run(input_command, shell=True, check=True, stderr=subprocess.STDOUT)
    except (subprocess.CalledProcessError, TypeError) as e:
        rich_print(e)



##############################################################################
#                                                                            #
#                       Run Subprocess P-Open Function                       #
#                                                                            #
##############################################################################



'''
Development Note:

    Many Subprocess methods in Python are simply a wrapper function around
    the `Popen` method. Using this method provides granularity in that
    stdin, stdout, and stderr can call be explicitly defined.

    The result is returned as bytes, so it must be decoded.
    This function decodes the bytes as UTF-8 (as a text-string).

    In the event that the command does not have an output, a static result is given.
    This is so that when this function is called, there is a clear indicator
    that the function was called and that some action occurred.  A static None
    value is nebulous, as it does not indicate if anything occurred.


Development Notes On Output Capturing:

    When capturing the output of Subprocess in any method, there is a limitation
    in the amount of output (in bytes).  Underneath the hood, stdout and stderr
    are assigned to an internal variable, and that variable has a maximum size.

    By default, if the output is over that size, text is truncated so it fits in the
    the internal variable.
'''



#######################  Run Terminal Shell Commands  #######################



def run_subprocess_p_open(input_command):
    import subprocess
    process = subprocess.Popen(input_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if output != b'' and error == b'':      # Command Result sent to stdout
        result = output.decode('utf-8')
    elif output == b'' and error != b'':    # Command Result sent to stderr
        result = error.decode('utf-8')
    elif output != b'' and error != b'':    # Command Result sent to stdout and stderr
        result = f"{output.decode('utf-8')}{error.decode('utf-8')}"
    elif output == b'' and error == b'':    # No Command Result
        result = 'Literal None - Nothing Returned'
    return result



##############################################################################
#                                                                            #
#                 Run Subprocess With Output Check Function                  #
#                                                                            #
##############################################################################



'''
Development Notes:

    Both stderr is redirected to stdout, and stdout is assigned to a variable.
    Of note, from the Official Documentation:

        The actual encoding of the output data may depend on the command being invoked,
        so the decoding to text will often need to be handled at the application level.

    Because this command is invoked by this repository using commands that have a known,
    expected output, the decoding method is included in the function call with the
    `universal_newlines` which instructs Python to interpret (decode) the output as text.

    However, a non-zero exit code will cause a traceback.
'''



#######################  Run Terminal Shell Commands  #######################



def run_subprocess_check_output(input_command):
    import subprocess
    output = subprocess.check_output(input_command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    return output


