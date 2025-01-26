import requests
import json
import time
from utility import log
import os, sys
import datetime

# show info
print("base path : {}".format(os.path.dirname(sys.argv[0])))
log_main = log("getDatafromGISDA_log", 30, 30)

log_main.log("{}".format(os.path.abspath(os.path.dirname(sys.argv[0]))), "INFO")
mainPath = "{}".format(os.path.abspath(os.path.dirname(sys.argv[0]))[:-4])
srcPath = "{}/src".format(mainPath)
dataPath = "{}/data".format(mainPath)
imgPath = "{}/image".format(mainPath)

log_main.log("mainPath : {}".format(mainPath), "INFO")
log_main.log("srcPath : {}".format(srcPath), "INFO")
log_main.log("dataPath : {}".format(dataPath), "INFO")
log_main.log("imgPath : {}".format(imgPath), "INFO")

# get data from GISDA

# Defining parameter to get data from GISDA
# URL strucute : https://disaster.gistda.or.th/api/v2/file/download?f=filename
# Data file name : Fire/y{year}/80_Report/{fileType}/{typeData}/{typeName}_{year}{month}{day}.{fileType}
# Image file name : Fire/y{year}/80_Report/{fileType}/{typeData}/{typename}_{year}{month}{day}.{fileType}
str_GISDAURL = "https://disaster.gistda.or.th/api/v2/file/download"

dict_type_xlsx = {
"N_Vi1_Day":"N_Vi1",
"N_Mod_Day":"N_Mod",
"N_Vi2_Day":"N_Vi2"
}

dict_type_jpg = {
"N_Vi1_Day_Thai":"N_Vi1_Day_Thai",
"N_Mod_Day_Thai":"N_Mod_Day_Thai",
"N_Vi2_Day_Thai":"N_Vi2_Day_Thai"
}

dict_type_file = {
"xlsx":"Excel",
"jpg":"Map"
}

# Defining function to get data from GISDA

def getDatafromGISDA(url = None, params = None, dataPath = None, filename = None):
    # get data from GISDA
    url = "https://disaster.gistda.or.th/api/v2/file/download"
    response = requests.get(url, params = params)
    file_Path = '{}/{}.pdf'.format(dataPath,filename)
    log_main.log('File {} downloaded response'.format(response.content), "INFO")
    if response.status_code == 200:
        with open(file_Path, 'wb') as file:
            file.write(response.content)
        log_main.log('File {} downloaded successfully'.format(filename), "INFO")
    else:
        log_main.log('Failed to download file {}'.format(filename), "INFO")    

    # show info
    log_main.log("get data {} from GISDA".format(filename), "INFO")
    log_main.log("save data to {}/{}.xlsx".format(dataPath,filename), "INFO")

# Defining main function
def main():
    log_main.log("run on main : {}".format(datetime.datetime.now), "INFO")


# Using the special variable 
# __name__
if __name__=="__main__":
    main()