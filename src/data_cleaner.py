import csv
from pydoc import text  # 导入 csv 模块（Python 自带的工具箱，专门处理 CSV 表格文件）

# with open(...) as f 是"安全打开文件"的固定句式：
# 打开文件并起个别名叫 f，用完会自动关闭，不用你操心
# encoding="utf-8" 是告诉 Python 文件里有中文，按 UTF-8 编码来读（不写会乱码报错）
with open("data/raw/employees_dirty.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # 用 DictReader 读取：每一行自动变成一个字典，列名做 key
    rows = list(reader)         # 把所有行装进一个列表，方便后面反复使用

print(f"总行数: {len(rows)}")  # len() 数列表长度；f"..." 是把变量嵌进文字的写法


print(rows[0])                 # 打印第 1 行（下标从 0 开始数），看看它长什么样
# ===== 里程碑 2：统计每一列的空值数量 =====
columns = rows[0].keys()          # 取出所有列名（id、name、age……）
null_counts = {}                  # 准备一个空字典，存放统计结果

for col in columns:               # 逐列循环（col 就是当前列名）
    count = 0                     # 这一列的空值计数器，先归零
    for row in rows:              # 把每一行都检查一遍
        value = row[col].strip()  # 取出这一格的值，.strip() 去掉首尾空格
        if value == "":           # 去掉空格后是空字符串，就算空值
            count += 1            # 计数器加 1（等同 count = count + 1）
    null_counts[col] = count      # 这一列查完了，结果存进字典

print("每列空值统计:")
for col, count in null_counts.items():  # .items() 把字典按 (键, 值) 一对对取出来
    print(f"  {col}: {count}")          # 逐列打印统计结果



# ===== 里程碑 3：找出重复登记的行 =====

see={}
duplicates=[]
for i, row in enumerate(rows):
    fingerprint = (row["name"].strip(), row["age"].strip(),
                   row["city"].strip(),row["email"].strip() )
    
    if fingerprint in see :
        duplicates.append((i+2,row["name"]))
    else:
        see[fingerprint] = i+2
print(f"重复行数量: {len(duplicates)}")
for line_no, name in duplicates:
    print(f"  第 {line_no} 行: {name}")


    # ===== 里程碑 4：校验日期格式 =====

from datetime import datetime  # 导入 datetime 模块，专门处理日期时间
invalid_dates = []  # 准备一个空列表，存放日期格式不对的行号
for i, row in enumerate(rows):  # 逐行循环
    date_text = row["join_date"].strip()  # 取出 join_date 列的值，去掉首尾空格
    if date_text == "":  # 如果这一格是空的，就跳过
        continue
    try:
        # 尝试把字符串按 "YYYY-MM-DD" 格式解析成日期对象
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        # 如果解析失败，就说明格式不对，把行号记下来（+2 是因为 CSV 文件有表头，行号从 1 开始）
        invalid_dates.append((i + 2, date_text))
print(f"非法日期数量: {len(invalid_dates)}")
for line_no, date_str in invalid_dates:
    print(f"  第 {line_no} 行: {date_str}")


    # ===== 里程碑 5：把结果写成 JSON 报告 =====


import json  # 导入 json 模块，专门处理 JSON 数据格式
#先把重复行和非法日期行整理成列表，方便写入 JSON 文件
dup_jist=[]
for line_no, name in duplicates:
    dup_jist.append({"line_no": line_no, "name": name})

import json    # 搬出 JSON 工具箱
date_jist=[]
for line_no, text in invalid_dates:
    date_jist.append(f"第 {line_no} 行:{text}")
#把所有结果装进一个大字典这就是一个报告的结构
report = {
    "file": "data/raw/employees_dirty.csv",#检查的是哪个文件
    "total_rows": len(rows),#总行数
    "null_counts": null_counts,#每列空值统计
    "duplicates_rows": {
        "count": len(duplicates),#重复行数量
        "details": dup_jist#重复行详情
    },
    "invalid_dates": {
        "count": len(invalid_dates),#非法日期数量
        "details": date_jist#非法日期详情
    }
}
#写入文件:w是写入模式，encoding="utf-8"是告诉Python文件里有中文，按UTF-8编码来写
with open("cleaning_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)  # 把 report 字典写入 JSON 文件，ensure_ascii=False 让中文正常显示，indent=2 美化缩进
print("报告已生成: cleaning_report.json")
