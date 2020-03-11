# Walk through a folder tree and search for exceptionally large files or folders (larger than 100MB)
# os.path.getsize() finds file size
# Print files with absolute path to screen

import os


def findFiles(startfolder, notify_size):
    tree = os.walk(startfolder)
    for folderName, subfolders, filenames in tree:
        for subfolder in subfolders:
            subfolder = folderName + '\\' + subfolder
            size = (os.path.getsize(subfolder) / 1024) / 1024
            if size > notify_size:
                print(subfolder + ': ' + str(size) + ' MB')

        for filename in filenames:
            filename = folderName + '\\' + filename
            size = (os.path.getsize(filename) / 1024) / 1024
            if size > notify_size:
                print(filename + ': ' + str(size) + ' MB')


findFiles(input('What directory would you like to search?: '),
          int(input('What size (in MB) would you like to be notified for?')))

