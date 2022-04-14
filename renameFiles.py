
import os
import os.path
import pathlib
from natsort import natsorted
import re


########################################
# recursive function
########################################
def processDir(curDir, sParish):

    print("\n******************")

    bGenetekaFilename = False

    #######################################
    # Get Document Type from dir Path
    #######################################
    iSeqNum = 0
    sPathBasename = os.path.basename(curDir)

    sDocType = sPathBasename
    sDocTypeNoS = sPathBasename[:-1]
    #print(sPathBasename)

    ##########################################
    # sort directory items like File Explorer
    ##########################################
    dirItems = natsorted(os.listdir(curDir))

    for dirItem in dirItems:
        #print(dirItem)
        fullPathDirItem = os.path.join(curDir,dirItem)

    ##############################################################
    # if Dir --> recursive call to drill-down into directory
    # if file --> Rename file 
    ##############################################################
        if os.path.isdir(fullPathDirItem):

            processDir(fullPathDirItem, sParish)

        else:
            # process files

            if os.path.isfile(fullPathDirItem):
                #####################################################
                # Only process jpg files
                #####################################################
                if pathlib.Path(fullPathDirItem).suffix != ".jpg":
                    continue

                #####################################################
                # Determine directory year
                #####################################################
                dirParts = os.path.split(curDir)
                sYear = os.path.basename(dirParts[0])
                #print(sYear)

                #####################################################
                # If file has already been renamed --> skip renaming
                # Ex: new filename contains "1870_Nur_Birth"
                #####################################################
                sSearchStr = f"{sYear}_{sParish}_{sDocTypeNoS}"
                if dirItem.find(sSearchStr) != -1:
                    continue

                # DocType is all lower case --> upper case it
                sDocTypeNoSLower = sDocTypeNoS.lower()
                sSearchStr = f"{sYear}_{sParish}_{sDocTypeNoSLower}"
                if dirItem.find(sSearchStr) != -1:
                    # rename file 
                    fullPathNewFilename = fullPathDirItem
                    fullPathNewFilename = fullPathNewFilename.replace(sDocTypeNoSLower,sDocTypeNoS)  
                      
                    print(f"rename {fullPathDirItem} as {fullPathNewFilename}")
                    os.rename(fullPathDirItem, fullPathNewFilename)

                    continue
                
                #####################################################
                # Identify current filename as 
                # 1) Polish Archives filename
                # 2) Geneteka filename
                #####################################################
                if len(dirItem) >= 12:
                    bGenetekaFilename = False
                else:
                    bGenetekaFilename = True

                #####################################################
                # Build appropriate new filename
                #####################################################
                if bGenetekaFilename:
                    filenameNoExt = dirItem.replace(".jpg","")
                    #print(filenameNoExt)

                    # is it a non-index?
                    if re.match("^[0-9]+[-]{1}[0-9]+",filenameNoExt) or re.match("^[0-9]+",filenameNoExt): 
                        sDocRange = filenameNoExt.replace("-","_") 
                        #print(sDocRange)
                        sNewFilename = f"{sYear}_{sParish}_{sDocType}_{sDocRange}.jpg"

                    # is it an index?
                    elif re.match("^Sk[UMZP]+[0-9]+",filenameNoExt):
                        idx = re.search("[0-9]",filenameNoExt).start()
                        #print(idx)
                        sIndexNum = filenameNoExt[idx:]
                        sNewFilename = f"{sYear}_{sParish}_{sDocTypeNoS}_index_{sIndexNum}.jpg"

                    # is it a single index?
                    elif re.match("^Sk[UMZP]+",filenameNoExt):
                        sNewFilename = f"{sYear}_{sParish}_{sDocTypeNoS}_index.jpg"

                    else:    
                    # Ex. 1890_Nur_Births_01_02.jpg    
                        sNewFilename = f"{sYear}_{sParish}_{sDocType}_{dirItem}"

                else:
                    iSeqNum += 1        
                    sSeqNum = f'{iSeqNum:03}'
                    sNewFilename = f"{sYear}_{sParish}_{sDocType}_{sSeqNum}.jpg"


                #####################################################
                # rename file
                #####################################################
                print(f"rename {fullPathDirItem} as {sNewFilename}")
                #print(sNewFilename)

                fullPathNewFilename = os.path.join(curDir,sNewFilename)
                #print(fullPathNewFilename)
                os.rename(fullPathDirItem, fullPathNewFilename)


def main():

    #curDir = r"C:\Polish Archives\Nur\1810s\1810_1811"
    #curDir = r"C:\Polish Archives\Nur\1890s\1897"
    curDir = r"C:\Polish Archives\Nur\1900s"
    #sFilenameStem = "1870_Nur"
    sParish = "Nur"
 
    processDir(curDir, sParish)
        

if __name__ == "__main__":  # confirms that the code is under main function

    main()    

