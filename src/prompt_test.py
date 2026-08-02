# #========里程碑1 零样本======
# import requests
# import json
# url = "http://localhost:11434/api/generate"

# data={
#     "model":"qwen2.5",
#     "prompt": "把'今天天气真好,翻译成英文",
#     "stream":False
    
# }
# response=requests.post(url, json=data)
# result=response.json()
# print(result["response"])
# # ======== 里程碑2 少样本（Few-shot）对比实验 ========
# import requests
# url = "http://localhost:11434/api/generate"
# import time   # 时间库，用来让程序"睡几秒"，加到文件最上面

# def ask(prompt):
#     data = {"model": "qwen2.5", "prompt": prompt, "stream": False}
#     for i in range(3):                       # 最多试 3 次
#         result = requests.post(url, json=data).json()
#         if result["response"] != "":         # 有回答就立刻交卷
#             return result["response"]
#         print("(调试) Ollama 正在加载模型，睡3秒再试...")
#         time.sleep(3)
#     return "（重试3次都没回答）"              # 3次都失败才放弃
# #零样本:直接下达命令,不举例
# zero = "判断这条评论是好评还是差评,只回答两个字:\n评论:物流太慢了,等一周才到"
# #少样本:给出两个例子,再下达命令
# few ="""
# 判断这条评论是好评还是差评,只回答两个字.
# 评论:质量非常好,下次还买
# 答案:好评
# 评论:用了一天就坏了,真失望
# 答案:差评
# 评论:物流太慢了,等一周才到
# """
# print("零样本:",ask(zero))
# print("少样本:",ask(few))
                            #=========里程碑4 多轮对话=======
import requests
url = "http://localhost:11434/api/chat"#chat是多轮对话接口
messages=[
    {"role": "user", "content": "你好,我叫小贾,是一名AI训练师学徒"}
]
data = {"model":"qwen2.5","messages":messages,"stream":False}
reply = requests.post(url,json=data).json()["message"]["content"]
print("AI:",reply)
messages.append({"role":  "assistant", "content": reply})
messages.append({"role": "user", "content": "我叫什么名字?我是做什么的?"})
data = {"model":"qwen2.5","messages":messages,"stream":False}
reply2 = requests.post(url,json=data).json()["message"]["content"]
print("AI:",reply2)