# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# R_factor.py
# Created on: 2023-10-10 
#
# This script is used to calculat the rainfall-runoff erosivity factor
# Description: Python 3.x environment is required.
# ---------------------------------------------------------------------------

# General import
import os
import time
import pandas as pd
import numpy as np


# Folder of rainfall data
PRE_folder_in = r"H:\Document\GIS_Data\meteorology\PRE"

# station ID
station_file = r"H:\Document\GIS_Data\meteorology\selected.csv"

# out folder
R_folder = r"H:\SoilErosion_TGR\Datasets\R_factor\R_factor"
PRE_folder_out = r"H:\SoilErosion_TGR\Datasets\R_factor\Rainfall"

# Precipitation station ID within research area
with open(station_file, 'r') as st:
    line = st.readlines()
    station_id = [int(i[:5]) for i in line[1:]]

station_coord = pd.read_csv(station_file)   # DataFrame

# get excle file name
file_list = [i[2] for i in os.walk(PRE_folder_in)][0]

for name in file_list:
    print(time.asctime(time.localtime(time.time())), end='')
    print("  ", end="")
    print(name)
    pre_file = PRE_folder_in + '\\' + name
    pre_data = pd.read_excel(pre_file)

    # 选取特定目标列
    col_name = ["区站号", "年", "月", "20-20时累计降水量(0.1mm)"]  # target col
    select_col = pre_data[col_name].copy()

    # 更改列标签
    select_col.columns=["ID", "Year", "Month", "0.1mm_PRE"]

    # 选取特定目标行， 基于站点ID
    target_data = select_col.query('ID in @station_id').copy()

    # 处理异常值，如32700,99999等，替换为0
    target_data.loc[target_data["0.1mm_PRE"] > 30000, "0.1mm_PRE"]=0

    # 转化降雨数据，0.1mm转化为1mm，并删除原始数据
    target_data["Rain"] = target_data["0.1mm_PRE"]*0.1
    del target_data["0.1mm_PRE"]

    # write out rain-fall data
    PRE_file_out = PRE_folder_out + "\\" + name
    target_data.to_excel(PRE_file_out, sheet_name="PRE", index=False)  # 写出Excel文件，不带行标签

    # 根据各站点，计算R-factor值：：数据透视
    # target_data.drop(["Year", "Month", "Rain"], axis=1, inplace=True)
    R_factor = pd.pivot_table(target_data, index="Month", aggfunc=np.sum)

    # write out R-factor data
    R_factor_out = R_folder + "\\" + name
    R_factor.to_excel(R_factor_out, sheet_name="R_factor", index=False)

    print("R factor was successfully calculted!!!")

print(time.asctime(time.localtime(time.time())), end='')
print("  ", end="")
print("Script performed successfully!!!")