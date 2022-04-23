
import os
import os.path
import pathlib
import datetime
import shutil
import sys

lastSavedTS = "2022-04-22-18:09:00"
setChangedDirs = set()

backupDriveLetter = "D"

########################################
# recursive function
########################################
def processDir(curDir):

    #######################################
    # Get list of items in directory
    #######################################
    dirItems = os.listdir(curDir)
    #print(len(dirItems))

    for dirItem in dirItems:

        fullPathDirItem = os.path.join(curDir,dirItem)

    ##############################################################
    # if Dir --> recursive call to drill-down into directory
    # if file --> 1) Get file timestamp
    #             2) Only process jpg files
    #             3) If file is new --> copy file to backup dir 
    ##############################################################
        if os.path.isdir(fullPathDirItem):
            ####################################
            # Make sure dest Directory exists
            ####################################
            destDir = fullPathDirItem.replace("C:",f"{backupDriveLetter}:")
            if not os.path.exists(destDir):
                os.mkdir(destDir)

            processDir(fullPathDirItem)

        else:
            if os.path.isfile(fullPathDirItem):

                #####################################################
                # Only process jpg files
                #####################################################
                if pathlib.Path(fullPathDirItem).suffix != ".jpg":
                    continue

                # last modified time of C: drive file    
                dttm = pathlib.Path(fullPathDirItem).stat().st_mtime
                #dttm = pathlib.Path(fullPathDirItem).stat().st_atime
                CDriveFileFmtTS = datetime.datetime.fromtimestamp(dttm).strftime("%Y-%m-%d-%H:%M:%S")

                #####################################################
                # File has changed --> copy to back-up destination
                #####################################################
                if CDriveFileFmtTS > lastSavedTS:

                    # D: drive filename
                    fullPathDestFile = fullPathDirItem.replace("C:",f"{backupDriveLetter}:")

                    # if D: drive file exists --> only copy if C: drive version is newer                                
                    if os.path.isfile(fullPathDestFile):
                        dttm = pathlib.Path(fullPathDestFile).stat().st_mtime
                        DDriveFileFmtTS = datetime.datetime.fromtimestamp(dttm).strftime("%Y-%m-%d-%H:%M:%S")
                        if CDriveFileFmtTS > DDriveFileFmtTS:
                            print(fullPathDirItem)
                            print(fullPathDestFile)
                            shutil.copyfile(fullPathDirItem, fullPathDestFile)

                    else:
                        print(fullPathDirItem)
                        print(fullPathDestFile)

                        ####################################
                        # Copy file to destination
                        ####################################
                        shutil.copyfile(fullPathDirItem, fullPathDestFile)



def main():

    curDir = r"C:\Polish Archives\Nur"
    #curDir = r"C:\Polish Archives\Boguty"
    #curDir = r"C:\Polish Archives\Czyżew"
 
    processDir(curDir)
        

if __name__ == "__main__":  # confirms that the code is under main function

    main()    

#    sortedChangedDirs = sorted(setChangedDirs)
#    #print(len(setChangedDirs))
#    for changedDir in sortedChangedDirs:
#        print(changedDir)