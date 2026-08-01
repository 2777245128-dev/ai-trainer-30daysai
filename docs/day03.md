# Day 3：pandas 重写数据清洗（2026-08-01）

## 今日目标

- [x] `pd.read_csv()` 读取 CSV + `df.head()` 预览
- [x] `df.isnull().sum()` 两行替代双层 for 循环统计空值
- [x] `df.duplicated(subset=...)` 用"业务指纹"查重复登记
- [x] `pd.to_datetime(format="mixed", errors="coerce")` 批量校验日期
- [x] 生成带时间戳的 JSON 清洗报告
- [x] 建立私人练习场 `D:\github\practice`，自造电商订单练习数据

## 今日产出

| 文件 | 说明 |
|------|------|
| `src/pandas_cleaner.py` | pandas 版清洗脚本（33 行，对比纯 Python 版 99 行） |
| `data/cleaning_report.json` | 自动生成的数据质量报告（带时间戳） |
| `D:\github\practice\orders_dirty.csv` | 私人练习数据：电商订单 26 行，自埋 7 类坑 |

## 检测结果

| 问题类型 | 数量 | 例子 |
|----------|------|------|
| 空值 | age×4、email×1、join_date×1、salary×1 | pandas 空值显示为 `NaN` |
| 重复登记 | 2 行（张三、李四各登记两次） | `subset` 指定四列指纹才抓得到 |
| 非法日期 | 3 行 | `2024年1月9日`（中文妖）、`2024-13-19`（13月妖）、`2024-02-30`（2月30日妖） |

## 今天掌握的技能

1. **pandas 三板斧**：`read_csv` 读表 → `head()` 预览 → `df[条件]` 筛选
2. **空值统计**：`df.isnull().sum()`；空值叫 `NaN`（Not a Number），日期空值叫 `NaT`（Not a Time）
3. **业务查重**：`duplicated()` 默认全列比对（工号不同就漏网），`subset=["name","age","city","email"]` 才是业务指纹；`keep=False` 原件复印件一起示众
4. **日期翻译官**：`to_datetime` 批量翻译；`format="mixed"` 吃混合格式；`errors="coerce"` 失败的强塞 NaT
5. **组合条件**：`dates.isna() & df["join_date"].notna()` = "翻译挂了 并且 原本不是空的" = 真妖怪；pandas 连接条件用 `&` 不用 `and`
6. **报关手续**：pandas 结果进 JSON 前要先 `to_dict()` / `int()` / `tolist()` 转原生类型
7. **时间戳**：`datetime.now().strftime("%Y-%m-%d %H:%M:%S")`；`strftime` 写出去 ↔ `strptime` 读进来

## 踩坑记录（最有价值的部分）

| 报错/现象 | 原因 | 教训 |
|------|------|------|
| `duplicated()` 返回 0 | 默认全列比对，重复登记的 id 不同 | 工具给默认值，脑子给业务值——指纹列要自己选 |
| `SyntaxError: Perhaps you forgot a comma?` | 字典里一行末尾漏逗号 | 报错直接给答案时，先信它 |
| `rename src/__init__.py => docs/day03.md` | 空文件删除 + 空文件新建，Git 误判为改名 | Git 靠内容相似度猜 rename，空文件会闹乌龙 |
| `warning: LF will be replaced by CRLF` | Windows 与 Unix 换行符不同 | 纯提醒零危害，Windows 用户天天见 |

## 明日计划（Day 4）：提示词工程入门（对齐计划清单 Week 1）

- 阅读 Prompt Engineering Guide 基础章节
- 学指令数据格式：instruction / input / output
- 用清洗后的干净员工数据，写 Prompt 生成第一批指令数据

## 我的心得

今天最大的震撼是 99 行变 33 行。昨天我手写双层 for 循环数空值、手写指纹查重，觉得那才是"真本事"；今天 pandas 一行 `isnull().sum()` 全干完，一开始有点失落，后来想通了：昨天练的是"看得懂"，今天练的是"用得上"，两件事不矛盾。

收获最大的一课是 `duplicated()` 返回 0 那次。工具没坏，是它的默认指纹（全列）和我的业务判断（四列）不一样。老程那句"工具给默认值，脑子给业务值"我记下了——以后用任何工具，先问一句"它默认假设是什么"。

`isna()` 和 `notna()` 放一起我一开始以为是矛盾，问了才明白是"译完后"和"译之前"两个时间点。敢问"这俩不矛盾吗"比闷头抄代码有用。

最后那个 `SyntaxError: Perhaps you forgot a comma?` 让我第一次觉得报错是朋友——它连答案都告诉我了。现在看到红字不慌了，先看最后一行。
