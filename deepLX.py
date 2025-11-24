
import os
import requests
import json

from PyDeepLX import PyDeepLX

current_folder = os.path.dirname(os.path.abspath(__file__))
key_json = os.path.join(current_folder, "key.txt")

class DeepLX_Free:
 
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""},),
                "source":   (["ZH","EN"],{"default":"ZH"} ),
                "target":   (["ZH","EN"],{"default":"EN"} ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "DeepLX"

    def gen(self, text:str,source,target):
        try:
            outStr = PyDeepLX.translate(text, source, target) 
        except :
            outStr = PyDeepLX.translate(text, source, target)     
            
        return (outStr,)

class DeepLX_translate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""},),
                "source": (["auto", "ZH","EN","DE","JA"],{"default":"auto"}),
                "target":  (["PASS", "ZH","EN","DE","JA"],{"default":"EN"}),
                "url":("STRING", {"multiline": False, "default": "https://api.deeplx.org/<api-key>/translate"},),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("out",)
    FUNCTION = "gen"
    OUTPUT_NODE = False
    CATEGORY = "DeepLX"

    def gen(self, text:str,source,target,url):
        if target == "PASS":
            return (text,)

        with open(key_json, 'r', encoding='utf-8') as file:
            key = file.read()
            print(key)
        
        if not key or key =="":
            print("No key provided!")

        url = url.replace("<api-key>", key)

        try:
            payload = json.dumps({
            "text": text,
            "source_lang": source,
            "target_lang": target
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            # 检查请求是否成功  
            if response.status_code == 200:  
                # 将响应的JSON内容解析为Python字典  
                data = response.json()  
                # 从字典中获取alternatives  
                result = data.get('data', " ")  
            else:  
                print("请求失败，状态码：", response.status_code)
                result = response.status_code
        except:
            result = "error"
                        
        return (result,)
