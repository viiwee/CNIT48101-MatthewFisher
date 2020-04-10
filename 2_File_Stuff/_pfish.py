#
# pfish support functions, where all the real work gets done
#
# Display Message() ParseCommandLine() WalkPath()
# HashFile() class _CVSWriter
# ValidateDirectory() ValidateDirectoryWritable()
#
import os
import stat
import time
import hashlib
import argparse
import csv

import logging  # test

log = logging.getLogger('main._pfish')


#
# Name: ParseCommand() Function
#
# Desc: Process and Validate the command line arguments
# use Python Standard Library module argparse
#
# Input: none
#
# Actions:
# Uses the standard library argparse to process the
# establishes a global variable gl_args where any of the
# obtain argument information
#
def ParseCommandLine():
    parser = argparse.ArgumentParser('Python file system hashing ..p-fish')
    parser.add_argument('-v', '—verbose', help='allows progress messages to be displayed', action='store_true')
    # setup a group where the selection is mutually exclusive and

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--md5', help='specifies MD5 algorithm', action='store_true')
    group.add_argument('--sha256', help='specifies SHA256 algorithm', action='store_true')
    group.add_argument('--sha512', help='specifies SHA512 algorithm', action='store_true')
    parser.add_argument('-d', '--rootPath', type=ValidateDirectory, required=True,
                        help="specify the root path for hashing")
    parser.add_argument('-r', '--reportPath', type=ValidateDirectoryWritable, required=True,
                        help="specify the path for reports and logs will be written")
    # create a global object to hold the validated arguments, these will be available then
    # to all the Functions within the _pfish.py module
    global gl_args
    global gl_hashType
    gl_args = parser.parse_args()

    if gl_args.md5:
        gl_hashType = 'MD5'
    elif gl_args.sha256:
        gl_hashType = 'SHA256'
    elif gl_args.sha512:
        gl_hashType = 'SHA512'
    else:
        gl_hashType = "Unknown"
        logging.error('Unknown Hash Type Specified')
    DisplayMessage("Command line processed: Successfully")
    return


# End ParseCommandLine
#
# Name: WalkPath() Function
#
# Desc: Walk the path specified on the command line
# use Python Standard Library module os and sys
#
# Input: none, uses command line arguments
#
# Actions:
# Uses the standard library modules os and sys
# to traverse the directory structure starting a root
# path specified by the user. For each file discovered, WalkPath
# will call the Function HashFile() to perform the file hashing
#
def WalkPath():
    process_count = 0
    error_count = 0
    ocvs = _CSVWriter(gl_args.reportPath + 'fileSystemReport.csv', gl_hashType)
    # Create a loop that process all the files starting
    # at the rootPath, all sub-directories will also be
    # processed
    log.info('Root Path:' + gl_args.rootPath)
    for root, dirs, files in os.walk(gl_args.rootPath):
        # for each file obtain the filename and call the HashFile Function
        for file in files:
            fname = os.path.join(root, file)
        result = HashFile(fname, file, ocvs)
        # if hashing was successful then increment the ProcessCount
        if result is True:
            process_count += 1
        # if not successful, the increment the ErrorCount
        else:
            error_count += 1
    ocvs.writerClose()
    return process_count


# End WalkPath
#
# Name: HashFile Function
#
# Desc: Processes a single file which includes performing a hash of the file
# and the extraction of metadata regarding the file processed
# use Python Standard Library modules hashlib, os, and sys
#
# Input: the_file ¼ the full path of the file
# simpleName ¼ just the filename itself
#
# Actions:
# Attempts to hash the file and extract metadata
# Call GenerateReport for successful hashed files
#
def HashFile(the_file, simple_name, o_result):
    # Verify that the path is valid
    if os.path.exists(the_file):
        # Verify that the path is not a symbolic link
        if not os.path.islink(the_file):
            # Verify that the file is real
            if os.path.isfile(the_file):
                try:
                    # Attempt to open the file
                    f = open(the_file, 'rb')
                except IOError:
                    # if open fails report the error
                    log.warning('Open Failed:' + the_file)
                    return
                else:
                    try:
                        # Attempt to read the file
                        rd = f.read()
                    except IOError:
                        # if read fails, then close the file and report error
                        f.close()
                        log.warning('Read Failed:' + the_file)
                        return
                    else:
                        # success the file is open and we can read from it
                        # lets query the file stats

                        the_file_stats = os.stat(the_file)
                        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(the_file)
                        # Print the simple file name
                        DisplayMessage("Processing File: " + the_file)
                        # print the size of the file in Bytes
                        fileSize = str(size)
                        # print MAC Times
                        modifiedTime = time.ctime(mtime)
                        accessTime = time.ctime(atime)
                        createdTime = time.ctime(ctime)
                        ownerID = str(uid)
                        groupID = str(gid)
                        fileMode = bin(mode)
                        # process the file hashes
                        if gl_args.md5:
                            # Calcuation and Print the MD5
                            hash = hashlib.md5()
                            hash.update(rd)
                            hexMD5 = hash.hexdigest()
                            hashValue = hexMD5.upper()
                        elif gl_args.sha256:
                            hash = hashlib.sha256()
                            hash.update(rd)
                            hexSHA256 = hash.hexdigest()
                            hashValue = hexSHA256.upper()
                        elif gl_args.sha512:
                            # Calculate and Print the SHA512
                            hash = hashlib.sha512()
                            hash.update(rd)
                            hexSHA512 = hash.hexdigest()
                            hashValue = hexSHA512.upper()
                        else:
                            log.error('Hash not Selected')
                        # File processing completed
                        # Close the Active File
                        print("==========================")
                        f.close()
                        # write one row to the output file
                        o_result.writeCSVRow(simple_name, the_file, fileSize, modifiedTime, accessTime, createdTime,
                                             hashValue, ownerID, groupID, mode)
                        return True
            else:
                log.warning('[' + repr(simple_name) + ', Skipped NOT a File' + ']')
                return False
        else:
            log.warning('[' + repr(simple_name) + ', Skipped Link NOT a File' + ']')
            return False
    else:
        log.warning('[' + repr(simple_name) + ', Path does NOT exist' + ']')
        return False


# End HashFile Function ¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼
#
# Name: ValidateDirectory Function
#
# Desc: Function that will validate a directory path as
# existing and readable. Used for argument validation only
#
# Input: a directory path string
#
# Actions:
# if valid will return the Directory String
#
# if invalid it will raise an ArgumentTypeError within argparse
# which will in turn be reported by argparse to the user
#
def ValidateDirectory(theDir):
    # Validate the path is a directory
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')
    # Validate the path is readable
    if os.access(theDir, os.R_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not readable')


# End ValidateDirectory ¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼
#
# Name: ValidateDirectoryWritable Function
#
# Desc: Function that will validate a directory path as
# existing and writable. Used for argument validation only
#
# Input: a directory path string
#
# Actions:
# if valid will return the Directory String
#
# if invalid it will raise an ArgumentTypeError within argparse
# which will in turn be reported by argparse to the user
#
def ValidateDirectoryWritable(theDir):
    # Validate the path is a directory
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory does not exist')
    # Validate the path is writable
    if os.access(theDir, os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')


# End ValidateDirectoryWritable ¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼
# ¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼
#
# Name: DisplayMessage() Function
#
# Desc: Displays the message if the verbose command line option is present
#
# Input: message type string
#
# Actions:
# Uses the standard library print function to display the message
#
def DisplayMessage(msg):
    if gl_args.verbose:
        print(msg)
    return


# End DisplayMessage¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼¼
#
# Class: _CSVWriter
#
# Desc: Handles all methods related to comma separated value operations
#
# Methods constructor: Initializes the CSV File
# writeCVSRow: Writes a single row to the csv file
# writerClose: Closes the CSV File
class _CSVWriter:
    def __init__(self, fileName, hashType):
        try:
            # create a writer object and then write the header row
            self.csvFile = open(fileName, 'wb')
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
            self.writer.writerow(('File', 'Path', 'Size', 'Modified Time',
                                  'Access Time', 'Created Time', hashType, 'Owner', 'Group', 'Mode'))
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod):
        self.writer.writerow((fileName, filePath, fileSize, mTime, aTime, cTime, hashVal, own, grp, mod))

    def writerClose(self):
        self.csvFile.close()
