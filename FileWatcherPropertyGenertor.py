#################################
#                               #
# @author: Pradeep CH           #
#                               #
#################################

import argparse
import configparser
from configparser import ConfigParser
from genericpath import isdir
from importlib.resources import path
import os
import uuid

#constants
DEFAULT_WATCHER_FILE_NAME='Watcher.ini'
DEFAULT_SECTION = 'DEFAULT'
DEFAULT_LOG_LEVEL = 'INFO'
DEFALUT_INTERVAL = '60'
LOG_SECTION = 'LOG'

IDENTIFIER = 'IDENTIFIER'
WATCH_DIRECTORY = 'WATCH_DIRECTORY'
WHITE_LIST_FILE_NAMES = 'WHITE_LIST_FILE_NAMES'
LEVEL = 'LEVEL'
DIRECTORY = 'DIRECTORY'
INTERVAL = 'INTERVAL'

def extractFileNames(directory):
    filenames = []
    dirCount =0
    for filename in os.listdir(directory):
        if os.path.isdir( os.path.join ( directory, filename)):
            dirCount +=1
            continue
        filenames.append(filename)

    print(f"Number of file(s) identified : {len(filenames)}")
    print(f"Number of directories skipped : {dirCount}")
    return filenames

def validateOutFile(outputPath,fileCount):
    print(f'Validating created file :{outputPath}')
    config =  configparser.ConfigParser()
    config.read(outputPath)  
    assert len(config.sections())==1, 'Missing sections'
    assert config[LOG_SECTION][DIRECTORY],'Missing log directory'
    assert config[LOG_SECTION][LEVEL],'Missing log level'
    assert config[DEFAULT_SECTION][IDENTIFIER],'Missing log watcher IDENTIFIER'
    assert config[DEFAULT_SECTION][WATCH_DIRECTORY],'Missing log watcher WATCH_DIRECTORY'
    if fileCount:
        assert config[DEFAULT_SECTION][WHITE_LIST_FILE_NAMES],'Missing log watcher WHITE_LIST_FILE_NAMES'
    print(f'Validation completed')

def prepareConfig(sourcePath:str, logPath:str,filenames:list):
    config = configparser.ConfigParser()
    config.add_section(LOG_SECTION)
    config[LOG_SECTION][DIRECTORY] = logPath
    config[LOG_SECTION][LEVEL]  =  DEFAULT_LOG_LEVEL
    config[DEFAULT_SECTION][IDENTIFIER] = str(uuid.uuid4().hex)
    config[DEFAULT_SECTION][WATCH_DIRECTORY] = sourcePath
    config[DEFAULT_SECTION][INTERVAL] = DEFALUT_INTERVAL
    config[DEFAULT_SECTION][WHITE_LIST_FILE_NAMES] = ",".join(filenames)
    return config

def writeConfig(outputPath:str, config:ConfigParser):
    with open(outputPath, 'w') as configfile:
        config.write(configfile)

def parseArgs():
    print('Parsing passed arguements')
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--sourceDir', type=str, required=True, help='Source directory')
    parser.add_argument('-o', '--output',type=str, required=True, help='Output directory')
    parser.add_argument('-l', '--logDir',type=str, required=True, help='Log directory')
    return parser.parse_args()

def main():
    args = parseArgs()
    
    sourcePath = os.path.abspath(args.sourceDir)
    outputPath = os.path.abspath(args.output)
    logDir = os.path.abspath(args.logDir)

    print(f'Generating file watcher property file...')
    print(f'Output directory:{sourcePath}')
    print(f'Source directory:{outputPath}')
    print(f'Log  directory:{logDir}')

    if os.path.isdir(outputPath):
        print(f'Setting output file as {DEFAULT_WATCHER_FILE_NAME}')
        outputPath = os.path.join(outputPath, DEFAULT_WATCHER_FILE_NAME)
        
    filenames = extractFileNames(sourcePath)

    if(outputPath == os.path.join(sourcePath, DEFAULT_WATCHER_FILE_NAME)):
        print(f'Adding filename {DEFAULT_WATCHER_FILE_NAME} to white listed file names')
        filenames.append(DEFAULT_WATCHER_FILE_NAME)

    print(f"Source directory:{sourcePath} with white listed files {len(filenames)}")
    print(f"Writing config file at location :{outputPath}")

    config = prepareConfig(sourcePath, logDir,filenames)
    writeConfig(outputPath, config)  
    validateOutFile(outputPath, len(filenames))

    print("File watcher file created successfully.")
if __name__ == '__main__':
    main()