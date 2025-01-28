import requests
import json
import time
from utility import log
import os, sys
import datetime
from datetime import date, timedelta

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
# Data file name : Fire/y{year}/80_Report/{Type}/{typeData}/{typeName}_{year}{month}{day}.{fileType}
# Image file name : Fire/y{year}/80_Report/{Type}/{typeData}/{typename}_{year}{month}{day}.{fileType}
str_GISDAURL = "https://disaster.gistda.or.th/api/v2/file/download"
str_Offset_params = "Fire/y"
dict_fileStructure = {
"excel":{
    "Type":"Excel", 
    "FileType":"xlsx", 
    "TypeData":{
        "VIIRS":"N_Vi1_Day", 
        "MODIS":"N_Mod_Day", 
        "NOAA20":"N_Vi2_Day"}, 
    "TypeName":{
        "VIIRS":"N_Vi1", 
        "MODIS":"N_Mod", 
        "NOAA20":"N_Vi2"}
        },
"image":{
    "Type":"Map", 
    "FileType":"jpg",
    "TypeData":{
        "VIIRS":"N_Vi1_Day_Thai", 
        "MODIS":"N_Mod_Day_Thai", 
        "NOAA20":"N_Vi2_Day_Thai"}, 
    "TypeName":{
        "VIIRS":"N_Vi1_Day_Thai", 
        "MODIS":"N_Mod_Day_Thai", 
        "NOAA20":"N_Vi2_Day_Thai"}
        }
}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0', 'referer': 'https://disaster.gistda.or.th/', 'origin': 'https://disaster.gistda.or.th'}

# Defining function to get data from GISDA

def getDatafromGISDA(url = None, params = None, dataPath = None, filename = None, headers = None):
    # get data from GISDA
    log_main.log("get data {} from GISDA".format(filename), "INFO")
    response = requests.get(url, params = params, headers = headers)
    log_main.log('response {} - header {}'.format(response.status_code, response.headers), "INFO")
    file_Path = '{}/{}'.format(dataPath,filename)
    log_main.log('File {} downloaded response {}'.format(filename, response.status_code), "INFO")
    if response.status_code == 200:
        with open(file_Path, 'wb') as file:
            file.write(response.content)
        log_main.log('File {} downloaded successfully'.format(filename), "INFO")
    else:
        log_main.log('Failed to download file {}'.format(filename), "INFO")    

    # show info
    log_main.log("save data to {}/{}.xlsx".format(dataPath,filename), "INFO")
    return response.status_code

def startDownloadData(filename = None, thisPath = None, thisName = None):
    params = {"f":"{}{}".format(str_Offset_params, filename)}
    log_main.log("filename : {} - thisName : {}".format(filename, thisName), "INFO")
    log_main.log("params : {}".format(params), "INFO")
    try:
        code = getDatafromGISDA(url = str_GISDAURL, params = params, dataPath = thisPath, filename = thisName, headers = headers)
        with open("{}/datalist.txt".format(srcPath), "a") as file:
            file.writelines("{} - {} - completed\n".format(thisName, code))
    except Exception as e:  
        log_main.log("Error on get data from GISDA : {}".format(e), "ERROR")
        with open("{}/datalist.txt".format(srcPath), "a") as file:
            file.writelines("{} - {} - Error : {}\n".format(thisName, code, e))
    time.sleep(10)

# Defining main function
def main():
    # get data from GISDA
    # get today date
    list_args = sys.argv
    nextCheck = datetime.datetime.now()
    while True:
        thisDay = datetime.datetime.now()
        year = thisDay.year
        month = thisDay.month
        day = thisDay.day
        firstTime = False
        log_main.log("today : {}-{}-{}".format(year, month, day), "INFO")
        log_main.log("args : {}".format(list_args), "INFO")
        log_main.log("run on main : {}".format(datetime.datetime.now), "INFO")

        if "firstTime" in list_args:
            sys.argv = sys.argv.remove("firstTime")
            firstTime = True

        if firstTime:
            list_Day = list()
            startDay = datetime.datetime(year-1, month, day)
            log_main.log("get data from : {}-{}-{}".format(year, month, day), "INFO")
            lengthday = thisDay - startDay
            firstTime = False
            for day in range(0, lengthday.days):
                list_Day.append(startDay + timedelta(days = day))
            log_main.log("list_Day : {}".format(list_Day), "INFO")

            for day in list_Day:
                year = day.year
                month = day.month
                day = day.day 
                thisPath = None  
                thisName = None
                for key, value in dict_fileStructure.items():
                    if key == "excel":
                        for keyData, valueData in value["TypeData"].items():
                            thisPath = dataPath
                            thisName = "{}_{}{:02d}{:02d}.{}".format(keyData, year, month, day, value["FileType"])
                            filename = "{}/80_Report/{}/{}/{}_{}{:02d}{:02d}.{}".format(year, value["Type"], valueData, value["TypeName"][keyData], year, month, day, value["FileType"])
                            startDownloadData(filename = filename, thisPath = thisPath, thisName = thisName)
                    elif key == "image":
                        for keyData, valueData in value["TypeData"].items():
                            thisPath = imgPath
                            thisName = "{}_{}{:02d}{:02d}.{}".format(keyData, year, month, day, value["FileType"])
                            filename = "{}/80_Report/{}/{}/{}_{}{:02d}{:02d}.{}".format(year, value["Type"], valueData, value["TypeName"][keyData], year, month, day, value["FileType"])
                            startDownloadData(filename = filename, thisPath = thisPath, thisName = thisName)
            firstTime = False
        elif thisDay > nextCheck:
            log_main.log("run on update data : {}".format(thisDay), "INFO")
            with open("{}/datalist.txt".format(srcPath)) as file:
                lastline = (list(file)[-1])
                log_main.log("last line : : {}".format(lastline), "INFO")
                lastline_index = lastline.find("_")
            if lastline_index != -1:
                lastline_index += 1
                lastline = lastline[lastline_index:lastline_index+8]
            lastDate = datetime.datetime.strptime(lastline, "%Y%m%d")
            log_main.log("lastDate : {} - {}".format(lastDate, lastline), "INFO")
            if (thisDay - lastDate) < timedelta(days = 1):
                log_main.log("last update to : {}".format(lastDate), "INFO")
                nextCheck = thisDay + timedelta(days = 1)
                log_main.log("next update to : {}".format(nextCheck), "INFO")
            else:
                getDate = lastDate + timedelta(days = 1)
                year = getDate.year
                month = getDate.month
                day = getDate.day
                thisPath = None
                thisName = None
                for key, value in dict_fileStructure.items():
                    if key == "excel":
                        for keyData, valueData in value["TypeData"].items():
                            thisPath = dataPath
                            thisName = "{}_{}{:02d}{:02d}.{}".format(keyData, year, month, day, value["FileType"])
                            filename = "{}/80_Report/{}/{}/{}_{}{:02d}{:02d}.{}".format(year, value["Type"], valueData, value["TypeName"][keyData], year, month, day, value["FileType"])
                            startDownloadData(filename = filename, thisPath = thisPath, thisName = thisName)
                    elif key == "image":
                        for keyData, valueData in value["TypeData"].items():
                            thisPath = imgPath
                            thisName = "{}_{}{:02d}{:02d}.{}".format(keyData, year, month, day, value["FileType"])
                            filename = "{}/80_Report/{}/{}/{}_{}{:02d}{:02d}.{}".format(year, value["Type"], valueData, value["TypeName"][keyData], year, month, day, value["FileType"])
                            startDownloadData(filename = filename, thisPath = thisPath, thisName = thisName)
                nextCheck = thisDay + timedelta(minutes = 1)
        else:
            log_main.log("next check : {}".format(nextCheck), "INFO")
            time.sleep(7200)

# Using the special variable 
# __name__
if __name__=="__main__":
    main()