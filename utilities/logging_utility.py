# ------------------------------------------------------------------------------------------------------------------------------------
#
#   Logging Utility
#
#       This Utility creates a Custom Root Logger.
#
#       Console, Null, and File Handler are created.
#           • Rich is used for the Console Handler.
#           • Null Handlers are used to prevent propagation from other modules.
#           • Both a File Handler and a TimedRotatingFileHandler are created.
#
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
#                          Date and Time Constants                           #
#                                                                            #
##############################################################################



from datetime import datetime
from datetime import timezone



#######################  Date and Time  #######################



now = datetime.now()                                        # Example: datetime.datetime(2026, 3, 29, 4, 42, 21, 991813)
utc_now = datetime.now(timezone.utc)                        # datetime.datetime(2026, 3, 29, 4, 42, 21, 991813), tzinfo=datetime.timezone.utc)
utc_iso_format = utc_now.strftime('%Y_%m_%d_%H_%M_%S')      # Example: 2026_03_29_04_42_21



#######################  Log Date Folder  #######################



log_date_folder = now.strftime('%Y-%m-%d')                  # Example: 2026-03-29



##############################################################################
#                                                                            #
#                    Logging Directory Creation Function                     #
#                                                                            #
##############################################################################



from os import makedirs



#######################  Terminal Log Directory Creation  #######################



def create_terminal_log_directory(terminal_log_directory):
    makedirs(terminal_log_directory, exist_ok=True)



#########################################################################################################################################################
#                                                                                                                                                       #
#                                                    Terminal Console Logger and Terminal File Logger                                                   #
#                                                                                                                                                       #
#########################################################################################################################################################



##############################################################################
#                                                                            #
#                        Custom Root Logger Function                         #
#                                                                            #
##############################################################################



import time
import logging
from os import getcwd
from os.path import abspath
from rich.logging import RichHandler
from logging.handlers import TimedRotatingFileHandler



#######################  Custom Root Logger  #######################



def instantiate_logger(current_script):



    '''
    Terminal Log Folder and File:
        /logs/2026-04-02/{script_name}/terminal_log_{script_name}_2026_03_29_04_42_21.log

    Rotating Log Folder and File:
        /logs/rotating_debug_logs/rotating_debug_log.log
    '''



    pwd = getcwd()
    pwd_absolute_path = abspath(pwd)



    ###############  Terminal Log Folder and Filename  ###############



    terminal_log_directory = f'{pwd_absolute_path}/logs/{log_date_folder}/{current_script}'
    terminal_log_filename = f'{terminal_log_directory}/terminal_log_{current_script}_{utc_iso_format}.log'
    create_terminal_log_directory(terminal_log_directory)



    ###############  Rotating Terminal Log Folder and Filename  ###############



    debug_log_directory = f'{pwd_absolute_path}/logs/rotating_debug_logs/'
    debug_log_filename = f'{debug_log_directory}/rotating_debug_log.log'
    create_terminal_log_directory(debug_log_directory)



    ###############  Date Formats  ###############



    console_log_date_format = '%Y-%m-%d %H:%M:%S'       # Example: '2026-03-29 04:42:21'
    file_log_date_format    = '%Y-%m-%d %H:%M:%S %Z'    # Example: '2026-03-29 04:42:21 UTC'
    debug_log_date_format   = '%Y-%m-%d %H:%M:%S %Z'    # Example: '2026-03-29 04:42:21 UTC'



    ###############  Logger Base Configuration  ###############



    LOG = logging.getLogger(__name__)
    LOG.setLevel(logging.DEBUG)
    LOG.propagate = False



    ###############  Console Handler Configuration  ###############



    console_handler = RichHandler(show_time=False, locals_max_string=119)
    console_handler.setLevel(logging.INFO)
    console_format = '%(message)s'
    console_formatter = logging.Formatter(console_format, datefmt=console_log_date_format)
    console_handler.setFormatter(console_formatter)
    LOG.addHandler(console_handler)



    ###############  File Handler Configuration  ###############



    file_handler = logging.FileHandler(terminal_log_filename, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_format = '%(asctime)s --> [%(filename)s:%(lineno)d] %(message)s'
    file_formatter = logging.Formatter(file_format, datefmt=file_log_date_format)
    file_handler.setFormatter(file_formatter)
    file_formatter.converter = time.gmtime
    LOG.addHandler(file_handler)



    ###############  Time Rotating Logger Configuration  ###############



    debug_handler = TimedRotatingFileHandler(debug_log_filename, when='midnight', interval=1, backupCount=7)
    debug_handler.setLevel(logging.DEBUG)
    debug_format = '%(asctime)s --> [%(filename)s:%(lineno)d] %(message)s'
    debug_formatter = logging.Formatter(debug_format, datefmt=debug_log_date_format)
    debug_handler.setFormatter(debug_formatter)
    debug_formatter.converter = time.gmtime
    LOG.addHandler(debug_handler)



    ###############  Null Handler Configuration  ###############



    LOG.addHandler(logging.NullHandler())



    return LOG


