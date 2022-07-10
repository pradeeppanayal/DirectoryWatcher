# DirectoryWatcher
This script watches a directory and deletes any files which are not in the predefined white-listed filenames. 

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
# Execution
    python FileWatcher.py <config file>

Example:

    python FileWatcher.py Watcher.ini
# Code
Intilize logging
    
    CommonUtils.initLogging(logFilePath, level);
Intilize the watcher 

    watcher = Watcher(watchDirectory,whiteListFileNames,interval);
Start the watcher

    watcher.watch();
