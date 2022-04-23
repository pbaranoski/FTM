
import os
import os.path
import pathlib
import datetime
import shutil
import sys
import pandas as pd

lastSavedTS = "2022-04-22-13:00:00"
setChangedDirs = set()

backupDriveLetter = "D"


#######################################
# Build List from items in directory 
#######################################
def buildDirList(curDir):

    listDir = []

    # Get list of items in directory   
    if os.path.isdir(curDir): 
        dirItems = os.listdir(curDir)
    else:
        return listDir    

    #iterate thru items in directory to build list
    for dirItem in dirItems:

        fullPathDirItem = os.path.join(curDir,dirItem)

        # Build list items
        drive = fullPathDirItem[0:1]
        fullPathDirItemSansDrive = fullPathDirItem[2:]
        typeDirItem = ""
        if os.path.isdir(fullPathDirItem):
            typeDirItem = 'D'
        else:
            typeDirItem = 'F'   

        # Drive, DirSansDriveLetter, dirItem
        l = [drive, fullPathDirItemSansDrive, typeDirItem]
        listDir.append(l)

    # return list of dir items to load into data Frame
    return listDir


########################################
# recursive function
# NOTE: curDir == fullPath
########################################
def processDir(curDir):

    listC = []
    listD = []

    ##########################################
    # Create List of Items in directory
    ##########################################
    listC = buildDirList(curDir)
    curDirD = curDir.replace("C:",f"{backupDriveLetter}:")
    listD = buildDirList(curDirD)

    ##########################################
    # Create DateFrames from Lists
    ##########################################
    dataFrameC =  pd.DataFrame(listC,columns=["Drive","DirItem","Type"])
    #print(dataFrameC)
    dataFrameD =  pd.DataFrame(listD,columns=["Drive","DirItem","Type"])

    #########################################################
    # Join Data Frames by Key: ()
    #########################################################
    dfDiffs = dataFrameC.merge(dataFrameD, left_on="DirItem", right_on="DirItem", how="outer")
    #print("dfDiffs:")
    #print (dfDiffs)

    #########################################################
    # Remove items from D: that do NOT exist on C:
    #########################################################
    print("\n*******************************")    
    print(f"Items to remove from {backupDriveLetter}:")
    dfCMissing = dfDiffs.loc[dfDiffs["Drive_x"].isnull()]

    #print("What is not on C:\ drive")
    #print(dfCMissing)

    for row in dfCMissing.itertuples():
        # remove directory on D: that is NOT on C:
        if row.Type_y == 'D':
            dir2Remove = f"{backupDriveLetter}:" + row.DirItem
            if os.path.exists(dir2Remove):
                print(dir2Remove)
                shutil.rmtree(dir2Remove)
                    
        if row.Type_y == 'F':
            file2Remove = f"{backupDriveLetter}:" + row.DirItem
            if os.path.exists(file2Remove):
                print(file2Remove)
                os.remove(file2Remove)


    #########################################################
    # Add items to D: that exist on C: 
    #########################################################
    print("\n*******************************")
    print(f"Items to Add to {backupDriveLetter}:")
    dfDMissing = dfDiffs.loc[dfDiffs["Drive_y"].isnull()]

    #print("What is missing on D:\ drive")
    #print(dfDMissing)

    for row in dfDMissing.itertuples():
        # remove directory on D: that is NOT on C:
        if row.Type_x == 'D':
            dir2Add = f"{backupDriveLetter}:" + row.DirItem
            if not os.path.exists(dir2Add):
                print(dir2Add)
                os.mkdir(dir2Add)
                    
        if row.Type_x == 'F':
            file2Add = "C:" + row.DirItem
            destFile = f"{backupDriveLetter}:" + row.DirItem
            if os.path.exists(file2Add):
                print(destFile)
                shutil.copyfile(file2Add, destFile)

    #########################################################
    # Process dirItems 2nd time to navigate to next directory.
    #########################################################
    dirItems = os.listdir(curDir)
    for dirItem in dirItems:
        fullPathDirItem = os.path.join(curDir,dirItem)

        if os.path.isdir(fullPathDirItem):
            processDir(fullPathDirItem)


def main():

    curDir = r"C:\Polish Archives\Nur"
    #curDir = r"C:\Polish Archives\Kuczyn"    
    #curDir = r"C:\Polish Archives\Boguty"
    #curDir = r"C:\Polish Archives\Czyżew"
    #curDir = r"C:\Polish Archives\Zuzela"

    processDir(curDir)
        

if __name__ == "__main__":  # confirms that the code is under main function

    main()    
