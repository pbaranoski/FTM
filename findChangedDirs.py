
import os
import os.path
import pathlib
import datetime
import shutil
import sys

lastSavedTS = "2022-02-20-23:59:59"
setChangedDirs = set()

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
    # if Dir --> recursive call to get list or items
    # if file --> 1) Get file timestamp
    #             2) Only process jpg files
    #             3) If file is new --> copy file to backup dir 
    ##############################################################
        if os.path.isdir(fullPathDirItem):
            ####################################
            # Make sure dest Directory exists
            ####################################
            destDir = fullPathDirItem.replace("C:","D:")
            if not os.path.exists(destDir):
                os.mkdir(destDir)

            processDir(fullPathDirItem)

        else:
            if os.path.isfile(fullPathDirItem):
                dttm = pathlib.Path(fullPathDirItem).stat().st_mtime
                fmtTS = datetime.datetime.fromtimestamp(dttm).strftime("%Y-%m-%d-%H:%M:%S")
                #print(fullPathDirItem)
                #print(fmtTS)

                #####################################################
                # Only process jpg files
                #####################################################
                if pathlib.Path(fullPathDirItem).suffix != ".jpg":
                    continue

                #####################################################
                # File has changed --> copy to back-up destination
                #####################################################
                if fmtTS > lastSavedTS:
                    #setChangedDirs.add(curDir)

                    print(fullPathDirItem)
                    destFile = fullPathDirItem.replace("C:","D:")
                    print(destFile)

                    #destFile = os.path.join("C:\Test",dirItem)
                    #print(destFile)

                    ####################################
                    # Copy file to destination
                    ####################################
                    shutil.copyfile(fullPathDirItem, destFile)
                    #sys.exit(0)

def main():

    #curDir = r"C:\Polish Archives\Nur\1810s\1810_1811"
    curDir = r"C:\Polish Archives\Zuzela"
 
    processDir(curDir)
        

if __name__ == "__main__":  # confirms that the code is under main function

    main()    

#    sortedChangedDirs = sorted(setChangedDirs)
#    #print(len(setChangedDirs))
#    for changedDir in sortedChangedDirs:
#        print(changedDir)