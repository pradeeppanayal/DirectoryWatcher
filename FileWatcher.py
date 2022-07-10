import sys
import configparser
import time
import logging
import os
import fnmatch
from datetime import datetime
import logging

#################################
#                               #
# @author: Pradeep CH           #
#                               #
#################################

class Watcher(object):
    def __init__(self, directory,whiteList,interval) :
        self.directory = directory;
        self.whiteList = whiteList;
        self.interval = interval;
        self.active = False;
        self.validatedFiles = [];

    def watch(self):
        logging.info('Watching {}'.format(self.directory));
        try:
            while True:
                if(not self.active):
                    try:
                        self._performAction();
                    except Exception as ex:
                        logging.error("The execution failed with cause {}".format(str(ex)));
                else:
                    logging.warning("Skipped execution as the previouse one is not completed.")
                # Set the thread sleep time
                time.sleep(self.interval);
        except Exception as e:
            logging.info("Stoping.. Cause:"+ e)
        logging.info('Completed');

    def _markAsAllowed(self, fileName):
        self.validatedFiles.append(fileName);
        logging.debug("Entry {} added. Current cache size: {}".format(fileName, len(self.validatedFiles)));

    def _isAllowedInPast(self, fileName):
        return fileName in self.validatedFiles;

    def _performAction(self):
        logging.debug("Executing watcher...");
        self.active= True
        dir_list = os.listdir(self.directory)
        for fileName in dir_list:
            if(self._isAllowedInPast(fileName)):
                continue;
            if(self._isWhiteListed(fileName)):
                self._markAsAllowed(fileName);
                continue;
            filePath = CommonUtils.pathJoin(self.directory,fileName);
            try:
                os.remove(filePath);
                logging.info("File deleted :{}".format(fileName));
            except Exception as ex:
                logging.error("Could not delete file: {} ".format(filePath))
        self.active = False;

    def _isWhiteListed(self, fileName):
        for listEntry in self.whiteList:
            if(fnmatch.fnmatch(fileName, listEntry)):
                return True;            
        return False;

COMMA = ",";

#This class contains basic utility functions
class CommonUtils(object):
    @staticmethod
    def initLogging(logFile, level):
        #logging.basicConfig(filename=logFile, filemode='w', format='%(name)s - %(levelname)s - %(message)s');
        loggingLevel = logging.INFO;
        if(level=='DEBUG'):
            loggingLevel = logging.DEBUG;
        logging.basicConfig(filename=logFile, level=loggingLevel,format='%(asctime)s %(levelname)s %(message)s');
        #logging.basicConfig(level=logging.DEBUG)

    @staticmethod
    def prepareLogFileName(runIdentifier):
        return 'log_{}_{}.log'.format(datetime.now().strftime('%Y%m%d'), str(runIdentifier));

    @staticmethod
    def pathJoin(path1, path2):
        return "{}{}{}".format(path1,os.sep,path2);

#The main function perform basoc actions and trigger the watcher
def main():
    configFileName =sys.argv[1];

    config = configparser.ConfigParser();
    config.sections();
    config.read(configFileName);

    #run identifier
    runIdentifier = config['DEFAULT']['IDENTIFIER'];
    
    #Log file details
    logDir = config['LOG']['DIRECTORY']
    level = config['LOG']['LEVEL']
    
    #Prepare the log file
    logFileName = CommonUtils.prepareLogFileName(runIdentifier);
    logFilePath = CommonUtils.pathJoin(logDir, logFileName)
    CommonUtils.initLogging(logFilePath, level);
    
    #Fetch watcher info
    watchDirectory = config['DEFAULT']['WATCH_DIRECTORY']
    whiteListFileNames = config['DEFAULT']['WHITE_LIST_FILE_NAMES'];
    interval = int(config['DEFAULT']['INTERVAL']);

    #Intilize watcher
    watcher = Watcher(watchDirectory,whiteListFileNames.split(COMMA),interval);

    #Run watcher, it is a never ending action
    watcher.watch();

#The program starts here
if __name__=='__main__':
    main();