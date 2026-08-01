import pandas as pd # ← 读取 CSV 靠它
import json# ← 最后写报告靠它（不是读！）
from datetime import datetime# ← 报告里加时间戳
df = pd.read_csv("data/raw/employees_dirty.csv")# ← 读取 CSV 靠它
print("="*40)
print("原始数据预览(前五行):")
print("="*40)
print(df.head())
print("每列空值数量:")
print(df.isnull().sum())#检查每列有没有空值,将空值的数量统计出来
#抓重复行
print("重复行数量:",df.duplicated(subset=["name","age","city","email"]).sum())#检查重复行,将重复行的数量统计出来
print(df[df.duplicated(subset=["name","age","city","email"], keep=False)])#打印重复行

#校验日期格式
dates = pd.to_datetime(df['join_date'], format="mixed", errors='coerce')#将日期列转换为日期格式,错误的会变成NaT
print("日期翻译结果:")  
print(dates)
bad=dates.isna()&df['join_date'].notna()#找出原本有值但是转换失败的行
print("妖怪数量日期:",bad.sum())#打印妖怪数量
print(df.loc[bad, ['name','join_date']])#打印妖怪行
#=====生成JSON报告=====
report= {
    "file":"data/raw/employees_dirty.csv",#检查的是哪个文件
    "total_rows":len(df),#总行数
    "null_counts":df.isnull().sum().to_dict(),#每列空值统计
    "duplicates_rows": int(df.duplicated(subset=["name","age","city","email"]).sum()),#重复行数量
    "invalid_dates": df.loc[bad,"join_date"].to_list(),#非法日期详情
    "generated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}
with open("data/cleaning_report.json","w",encoding="utf-8") as f:
    json.dump(report,f,ensure_ascii=False,indent=2)
print("JSON报告已生成: data/cleaning_report.json")