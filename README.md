# Directory Watcher
This script allows the user to monitor a directory, and automatically deletes files which are not defined in the configurable file masks. No third party libraries are used in this implementation.

# Sample Config
    [DEFAULT]

    #This should be UNIQUE in order to support multiple run  on same machine
    IDENTIFIER=SampleDirectory1

    #The directory we need watcher for
    WATCH_DIRECTORY=C:\Users\Pradeep\Documents\sample

    #Comma seperated file masks. Example 1*.txt, 2.txt, will allow all the "".txt" files starts with "1" and file "2.txt"
    WHITE_LIST_FILE_NAMES=1*.txt,2.txt

    #Provide the interval in seconds, this defins the time interval to perform the watch in the WATCH_DIRECTORY
    INTERVAL=60

    #Log specific config
    [LOG]
    #Logging level
    DIRECTORY =  D:\work\directorywatcher
    #LEVEL=DEBUG
    LEVEL=DEBUG
# How to Run 
    python FileWatcher.py <config file>

Example:

    python FileWatcher.py Watcher.ini
# Basics
Intilize logging
    
    CommonUtils.initLogging(logFilePath, level);
Intilize the watcher 

    watcher = Watcher(watchDirectory,whiteListFileNames,interval);
Start the watcher

    watcher.watch();

# Logging
Uses the `logging` module to log. The log file will be auto created in the `[LOG].DIRCETORY` specified in the `config.ini` file. 

Log file name will be of below format,

    log_<date in yyyyMMdd format>_<identifier specified in ini file>.log
Sample,

    log_20220710_testrun.log
