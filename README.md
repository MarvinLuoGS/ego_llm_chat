### 代理服务器
OpenAI的官方API无法直连，**需要挂梯子**然后修改代理设置
在GPTThread.py文件中，加入以下两行代码
```python
os.environ["http_proxy"] = "http://127.0.0.1:7890" 
os.environ["https_proxy"] = "http://127.0.0.1:7890"
```

### 第三方API
一般不需要挂梯子，需要修改base_url
在GPTThread.py文件中，修改OpenAI的参数：
```python
client = openai.OpenAI(api_key="",base_url="https://api.chatanywhere.tech")
```
或者从环境变量中获取

### GPTThread的修改
- OPENAI_KEY命名改为OPENAI_API_KEY，和openai库保持一致

### otree.py的修改
- otree.py里面的metadata部分修改，将更多的session和participant信息保存下来
- 101行的link()
```python
····
metadata = dict(otree_session=instance.session.code)
metadata["otree_session_label"] = instance.session.label
····
if "BasePlayer" in super_names:
    ····
    metadata["participant_code"] = instance.participant.code
    metadata["participant_label"] = instance.participant.label
    ····
```

### system文件的修改
- stytem.txt文件是发送给模型的默认信息，修改为中文的话，alter_ego的源码需要修改
- 在D:\ego-llm\ego\Lib\site-packages\alter_ego\utils\\\_\_init\_\_.py文件中，修改以下代码，给open添加encoding参数：
```python
def from_file(file_name: str) -> str:

    with open(file_name,encoding="utf-8") as f:
        return f.read().strip()
```