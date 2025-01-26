# getFireDatafromGISDA
Target Get data firespot from GISDA

### Target Get data firespot from GISDA
Link : 
https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2025/80_Report/Excel/N_Vi1_Day/N_Vi1_20250102.xlsx

https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2024/80_Report/Excel/N_Mod_Day/N_Mod_20240123.xlsx

https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2024/80_Report/Excel/N_Vi2_Day/N_Vi2_20240123.xlsx

so structure of data is
common url is https://disaster.gistda.or.th/api/v2/file/download?
first parameter is f=Fire/y{year}/80_Report/Excel/{typeData}/{typeName}_{year}{month}{day}.xlsx

type data and type Name like this table
N_Vi1_Day - N_Vi1
N_Mod_Day - N_Mod
N_Vi2_Day - N_Vi2


#### for picture is likely same
https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2024/80_Report/Map/N_Vi1_Day_Thai/N_Vi1_Day_Thai_20240123.jpg

https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2024/80_Report/Map/N_Mod_Day_Thai/N_Mod_Day_Thai_20240123.jpg

https://disaster.gistda.or.th/api/v2/file/download?f=Fire/y2024/80_Report/Map/N_Vi2_Day_Thai/N_Vi2_Day_Thai_20240123.jpg

so structure of data is
common url is https://disaster.gistda.or.th/api/v2/file/download?
first parameter is f=Fire/y{year}/80_Report/Map/{typeData}/{typename}_{year}{month}{day}.jpg

type data and type Name like this table
N_Vi1_Day_Thai - N_Vi1_Day_Thai
N_Mod_Day_Thai - N_Mod_Day_Thai
N_Vi2_Day_Thai - N_Vi2_Day_Thai
