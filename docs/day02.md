# Day 2：数据清洗实战（2026-07-31）

## 今日目标

- [x] 读 Python 文件读写文档
- [x] 写 `data_cleaner.py`：读取 CSV，检测空值 / 重复值 / 格式异常
- [x] 输出 JSON 清洗报告
- [x] 环境补课：安装 Git、配置 PATH、安装 VS Code 与 Python 扩展

## 今日产出

| 文件 | 说明 |
|------|------|
| `data/raw/employees_dirty.csv` | 30 行测试数据，故意埋了 6 类脏数据 |
| `src/data_cleaner.py` | 数据清洗脚本（5 个里程碑，99 行） |
| `cleaning_report.json` | 程序自动生成的数据质量报告 |

## 数据里埋的 6 类坑（检测结果）

| 问题类型 | 数量 | 例子 |
|----------|------|------|
| 空值 | age×4、email×1、join_date×1、salary×1 | 空格也要算空值（.strip()） |
| 重复登记 | 2 行 | 忽略 id，其余字段相同即重复（第 11、21 行） |
| 日期格式混乱 | 5 种格式 | `2024-01-05` / `2024/01/06` / `2024.01.07` / `2024年1月9日` / `01/13/2024` |
| 非法日期 | 2 行 | `2024-13-19`（13月）、`2024-02-30`（2月30日） |
| 数值异常 | 3 行 | 年龄 `abc`、`-5`、`200` |
| 文本不规范 | 若干 | `北京市`/`beijing`/`BeiJing` 混用、首尾空格 |

## 今天掌握的技能

1. **文件读写**：`with open(...) as f` 固定句式、`encoding="utf-8"` 防中文乱码、写模式 `"w"`
2. **CSV 处理**：`csv.DictReader` 每行变字典，列名做 key
3. **嵌套循环**：逐列 × 逐行统计空值
4. **查重思路**：把多个字段拼成"指纹"（元组），用字典记录首次出现位置
5. **异常处理**：`try...except ValueError` + `datetime.strptime` 校验日期合法性
6. **JSON 输出**：`json.dump(report, f, ensure_ascii=False, indent=2)`
7. **PowerShell**：`cd` 切换目录、`dir` 查看内容、`mkdir` 建文件夹
8. **Git 工作流**：`git add .` → `git commit -m "说明"` → `git log --oneline`；理解"本地 commit ≠ 云端 push"

## 踩坑记录（最有价值的部分）

| 报错 | 原因 | 教训 |
|------|------|------|
| `KeyError: 'eamil'` | email 拼错成 eamil | 报错最后一行直接点名问题，先读最后一行 |
| `NameError: 'text'` | 循环变量改名改一半 | 改名字要全文统一改 |
| `from pydoc import text` | 自动补全误插入的垃圾 import | 补全框是双刃剑，敲注释时注意 |
| `not a git repository` | 在桌面目录执行 git 命令 | git 命令必须站在仓库目录里执行 |
| `git 不是内部或外部命令` | Git 未安装 / PATH 未刷新 | 改完 PATH 要重开终端 |

## 明日计划（Day 3）：pandas 登场

- 安装 pandas：`pip install pandas`
- 用 pandas 重写今天的清洗逻辑（体会 99 行 → 5 行的差距）
- 学习 `DataFrame`、`read_csv`、`drop_duplicates`、`isnull().sum()`

## 我的心得（自己补充）

> 在这里写几句话：今天哪个瞬间最有成就感？哪个坑卡你最久？怎么解决的？

（待补充）
