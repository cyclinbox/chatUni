#!/usr/bin/env python
#coding=utf-8
# chat Universary bot CLI.
# 鉴于百度千帆大模型平台升级到了v2版本的API格式，这一格式和openai、通义千问等的API格式几乎相同，因此做出下面的合并处理。
# 本脚本支持Qwen系列模型和文心ERNIE系列模型，并借助文心千帆大模型平台实现对DeepSeek-R1的支持。
# 阿里巴巴通义千问的聊天API
# reference: 
#   https://help.aliyun.com/zh/dashscope/developer-reference/api-details
#   https://help.aliyun.com/zh/dashscope/developer-reference/quick-start
#   https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-thousand-questions-metering-and-billing
# 百度文心一言的聊天API
# reference: 
#   https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2
#   https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Nlks5zkzu
#   https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clntwmv7t
# 2025-2-12
# 2025-2-17 update: add `replay` function.

import requests,json,datetime,os,sys,platform
import readline

proxies={
    'http' : 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}
headers_qwen = {
    'Content-Type': 'application/json',
    'Accept'    : 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Authorization': f"Bearer sk-82b3bfa35dce4e93877d7a54841d157d" 
}
headers_wenx = {
    'Content-Type': 'application/json',
    'Accept'    : 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Authorization': 'Bearer bce-v3/ALTAK-Zqc4DPImZxWj36xtXUNqE/4c8100c76a3864196c246ebd729775a1d816454d'
}


qwen_model_list = ["deepseek-r1(ernie)","deepseek-r1(qwen)",
        "deepseek-v3(ernie)","deepseek-v3(qwen)",
        "ernie-4.0-8k",
        "ernie-4.0-turbo-8k",
        "ernie-3.5-128k",
        "ernie-3.5-8K",
        "ernie-speed-128k",
        "ernie-speed-8K",
        "ernie-char-8k",
        "ernie-lite-8k",
        "ernie-tiny-8k",'qwen-max','qwen-plus','qwen-turbo','qwen-long',
        'qwen-max-longcontext','qwen1.5-72b-chat',
        'qwen1.5-72b-chat','qwen1.5-14b-chat',
        'qwen1.5-7b-chat','qwen-1.8b-chat']
qwen_model_id = 0 # 这个数字对应`qwen_model_list`的数组下标，表明调用的模型是哪一个
#track_reasoning = False # 是否在history message中记录reasoning的内容。


def get_response_with_stream(messages):
    model_name = qwen_model_list[qwen_model_id]
    model_name_1 = model_name.split("(")[0]
    data_payload_dt = {
        "model":model_name_1,
        "stream":True,
        "messages":messages
    }
    payload = json.dumps(data_payload_dt)
    
    if("qwen" in model_name): 
        url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        try:    response = requests.request("POST", url, headers=headers_qwen, data=payload, stream=True)
        except: response = requests.request("POST", url, proxies=proxies, headers=headers_qwen, data=payload, stream=True)
    else:                     
        url = "https://qianfan.baidubce.com/v2/chat/completions"
        try:    response = requests.request("POST", url, headers=headers_wenx, data=payload, stream=True)
        except: response = requests.request("POST", url, proxies=proxies, headers=headers_wenx, data=payload, stream=True)

    full_content = ""
    reasoning = False # a flag indicate if we are reasoning or not.
    have_reasoned = False # a flag indicate if we have done reasoning or not.
    for line in response.iter_lines():
        txt = line.decode("UTF-8")
        txt = txt.strip()
        left_trunc_pos = txt.find('{')
        left_trunc_pos = left_trunc_pos if(left_trunc_pos>0) else 0 # 防止找不到左大括号返回-1这个数字，导致后续处理出错
        txt = txt[left_trunc_pos:] # 按左大括号位置进行截断。包含左大括号
        if(txt=="data: [DONE]"): continue
        try:
            obj = json.loads(txt)
            #print("+ >>> ",json.dumps(obj,ensure_ascii=False,indent="\t"))#debug
            try:
                response_msg_con = obj["choices"][0]["delta"]["content"]
            except:
                response_msg_con = ""
            try:
                response_msg_res = obj["choices"][0]["delta"]["reasoning_content"]
            except:
                response_msg_res = ""
            if(response_msg_con==None or len(response_msg_con)==0):
                response_msg = response_msg_res if response_msg_res!=None else ""
                if(reasoning==False and have_reasoned==False):
                    print("<think>")
                    full_content += "<reasoning>"
                    reasoning = True
                full_content += response_msg
            else:
                response_msg = response_msg_con
                if(reasoning):
                    print("</think>")
                    full_content += "</reasoning>"
                    have_reasoned = True
                reasoning = False
                full_content += response_msg
            print(response_msg,end="")
        except Exception as e:
            #print("Error:",e)#debug
            print(txt,end="")
            full_content += txt
    return full_content


# 与ChatBot交互的方法
hist_msg = [] # history of messages
def chat(msg):
    global hist_msg
    refresh_token=["开始新对话","开始新话题","新对话","新话题","重新开始","restart"]
    if(msg in refresh_token):
        hist_msg = []
        return "消息队列已清空！现在开始新话题吧\n\n"
    else:
        hist_msg.append({"role":"user","content":msg})
        message = get_response_with_stream(hist_msg)
        if(len(message)==0): message="I don't understand this question." # 如果因为各种原因导致对话出错，此时message是空值。为了避免后续对话出现异常，此时人为给对话message赋值。
        hist_msg.append({"role":"assistant","content":message})
        #return message
        # 和文心一言的调用方法不同，QWen提供了流式调用的方法。
        # 因此在使用过程中，message随着response响应过程一起打印，
        # 此处就不需要再把完整信息再返回一次了。
        # 因此返回值设置为空字符串+两个换行符（用于新消息的换行）。
        return "\n\n" 

def replay(): # replay history message.
    global hist_msg
    print("------ replay start ------")
    for msg in hist_msg:
        role    = msg["role"]
        content = msg["content"]
        print(f"\n[{role}]:\t{content}\n")
    print("------- replay end -------")

# some commands
help_txt = """
Help:
    Basic commands:
        /help   Print this help message.
        /exit   Exit program.
        /chmod  Change model API.
        /replay Replay history messages.
    
    New chat commands:
        /clear  Clean both screen and history message.
        /hide   Only Clean screen, don't clean history.
        /reset  Clean history message.
    
    Export and import commands:
        /export [file name]
                Export all history message as an json file.
                `file name` parameter is optional. 
                If user don't specify a file name, the program 
                will use 'chatUni-history-YY-mm-dd_HHMMSS.json' 
                as file name, while 'YY-mm-dd_HHMMSS' represent
                current date and time.
                Please do not include any space characters in 
                the file name.
        /import <file name>
                Import history message from a json file.
                `file name` parameter is necessary. 
                If user don't specify a file name, the program 
                won't do anything.
                Please do not include any space characters in 
                the file name.
    Use \"\"\" to begin a multi-line message.
""".strip()
def command(cmd):
    global hist_msg
    if  (cmd=="/exit"): sys.exit(0);        return "Bye~"
    elif(cmd=="/help"): return help_txt    
    elif(cmd=="/clear"):
        hist_msg = []
        if(platform.platform()=="Windows"): os.system("cls")
        else:                               os.system("clear")
        return "All cleaned! Start new topic now~"
    elif(cmd=="/hide"):
        if(platform.platform()=="Windows"): os.system("cls")
        else:                               os.system("clear")
        return ""
    elif(cmd=="/reset"): 
        hist_msg = []     
        return "All reset! Start new topic now~"
    elif(cmd=="/replay"): 
        replay() 
        return "All history message replayed."
    elif(cmd[0:7]=="/export"):
        if(len(cmd)<8): filename = "chatUni-history-{}.json".format(datetime.datetime.now().strftime("%y-%m-%d_%H%M%S"))
        else:           filename = cmd[8:].strip()
        json_text = json.dumps(hist_msg, ensure_ascii=False, indent="\t")
        try:
            f = open(filename,'w',encoding="utf-8"); f.write(json_text); f.close()
            return "Exported chat history as '{}'.".format(filename)
        except: return "ERROR: file name may not legal."
    elif(cmd[0:7]=="/import"):
        if(len(cmd)<8): return "Please specify a file name!\nUsage: `/import <file name>`"
        filename = cmd[8:].strip()
        try:
            with open(filename,'r',encoding="utf-8") as f: history_text = f.read()
        except: return "ERROR in reading file: please check if file exist."
        try:
            hist_msg = json.loads(history_text)
            return "Imported chat history from '{}'.".format(filename)
        except: return "ERROR in load history from file: please check file format."
    elif(cmd=="/chmod"): # 切换模型
        #qwen_model_list = ['qwen-max','qwen-plus',
        #'qwen-turbo','qwen1.5-72b-chat',
        #'qwen1.5-72b-chat','qwen1.5-14b-chat','qwen1.5-7b-chat']
        #qwen_model_id = 0 # 这个数字对应`qwen_model_list`的数组下标，表明调用的模型是哪一个
        global qwen_model_id
        print(f"Current model id={qwen_model_id}.\nAll available models:")
        for i in range(len(qwen_model_list)):
            print(f"[{i}]:\t{qwen_model_list[i]}")
        new_id = input("Type new model id:")
        try:
            new_id_int = int(new_id)
            if(new_id_int<0 or new_id_int>=len(qwen_model_list)):
                return "Illegal id number. Change failed."
            else:
                qwen_model_id = new_id_int
                return "Model change succeed!"
        except:
            return "Nothing change."
        
    elif(cmd=="/debug"):
        debug_info = json.dumps(hist_msg, ensure_ascii=False, indent="\t")
        return "[Secret debug info]: {}\n".format(debug_info)
    else: return help_txt



if(__name__=="__main__"):
    print("+-----------------------+")
    print("|  chatUni-CLI version  |")
    print("+-----------------------+")
    print("2025.02.12 modified.")
    print("Type `/exit` to exit program.\n")
    while(1):
        #text = sys.argv[1]
        #print("[User]:\n{}\n".format(text))
        text = input("[User]:\t").strip()
        if(len(text)==0):continue
        if(text[0]=='/'): 
            resp = command(text)
            print(f"\n[{qwen_model_list[qwen_model_id]}]:\t{resp}\n\n")
        else:
            long_text_model=False
            text1 = text
            if(text[0:3]=='"""'):
                long_text_model = True
                while(long_text_model):
                    text = input("> ").strip()
                    text1 += "\n" # 这里记得插入换行符。
                    text1 += text
                    if(text[-3:]=='"""'):
                        long_text_model=False
            print(f"\n[{qwen_model_list[qwen_model_id]}]:\t",end="")
            resp = chat(text1)
            print(resp)





