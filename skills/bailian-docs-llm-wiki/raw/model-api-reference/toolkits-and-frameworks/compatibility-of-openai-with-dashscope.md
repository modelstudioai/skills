# OpenAI Chat接口兼容

阿里云百炼的千问模型支持 OpenAI 兼容接口，您只需调整 API Key、BASE\_URL 和模型名称，即可将原有 OpenAI 代码迁移至阿里云百炼服务使用。

## **兼容OpenAI需要信息**

### **BASE\_URL**

BASE\_URL表示模型服务的网络访问点或地址。通过该地址，您可以访问服务提供的功能或数据。在Web服务或API的使用中，BASE\_URL通常对应于服务的具体操作或资源的URL。当您使用OpenAI兼容接口来使用阿里云百炼模型服务时，需要配置BASE\_URL。

-   当您通过OpenAI SDK或其他OpenAI兼容的SDK调用时，需要配置的BASE\_URL如下：
    
    ```
    北京：https://dashscope.aliyuncs.com/compatible-mode/v1
    弗吉尼亚：https://dashscope-us.aliyuncs.com/compatible-mode/v1
    新加坡：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    ```
    
-   当您通过HTTP请求调用时，需要配置的完整访问endpoint如下：
    
    ```
    北京：POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
    弗吉尼亚：POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
    新加坡：POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
    ```
    

**重要**

中国香港地域的旧版URL `https://cn-hongkong.dashscope.aliyuncs.com/compatible-mode/v1` 即将下线，请及时迁移到新版路径 `https://{WorkspaceId}.cn-hongkong.maas.aliyuncs.com/compatible-mode/v1`。

### **支持的模型列表**

当前OpenAI兼容接口支持的千问系列模型如下表所示。

## 中国内地

-   **商业版**
    
    -   **千问Max系列**：qwen3.7-max、qwen3.7-max-2026-05-20、qwen3.6-max-preview、qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版模型、qwen-max、qwen-max-latest、qwen-max-2024-04-28及之后的快照版模型
        
    -   **千问Plus系列**：qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest、qwen-plus-2024-12-20及之后的快照版模型
        
    -   **千问Flash系列**：qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版模型；qwen-flash、qwen-flash-2025-07-28
        
    -   **千问Turbo系列**：qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-11-01及之后的快照版模型
        
    -   **千问Coder系列**：qwen3-coder-plus、qwen3-coder-plus-2025-07-22及之后的快照模型、qwen3-coder-flash、qwen3-coder-flash-2025-07-28及之后的快照模型、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19
        
    -   **千问Long系列**：qwen-long、qwen-long-latest、qwen-long-2025-01-25
        
    -   **QwQ系列**：qwq-plus、qwq-plus-latest、qwq-plus-2025-03-05
        
    -   **千问数学模型**：qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-2024-08-16及之后的快照版模型、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-2024-09-19
        
-   **开源版**
    
    -   qwen3.6-35b-a3b、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
        
    -   qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct、qwen3-235b-a22b-thinking-2507、qwen3-235b-a22b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-30b-a3b-instruct-2507、qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b、qwen3-4b、qwen3-1.7b、qwen3-0.6b
        
    -   qwq-32b、qwq-32b-preview、qwen2.5-14b-instruct-1m、qwen2.5-7b-instruct-1m、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct
        
    -   codeqwen1.5-7b-chat
        

## 美国

-   **商业版**
    
    -   **千问Plus系列**：qwen-plus-us、qwen-plus-2025-12-01-us及之后的快照版模型
        
    -   **千问Flash系列**：qwen-flash-us、qwen-flash-2025-07-28-us
        

## 国际

-   **商业版**
    
    -   **千问Max系列**：qwen3.7-max、qwen3.7-max-2026-05-20、qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版模型、qwen-max、qwen-max-latest、qwen-max-2025-01-25
        
    -   **千问Plus系列**：qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版模型、qwen-plus、qwen-plus-latest、qwen-plus-2025-01-25及之后的快照版模型
        
    -   **千问Flash系列**：qwen3.6-flash、qwen3.6-flash-2026-04-16、qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版模型；qwen-flash、qwen-flash-2025-07-28
        
    -   **千问Turbo系列**：qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-11-01及之后的快照版模型
        
    -   **千问Coder系列**：qwen3-coder-plus、qwen3-coder-plus-2025-07-22及之后的快照模型、qwen3-coder-flash、qwen3-coder-flash-2025-07-28及之后的快照模型
        
    -   **QwQ系列**：qwq-plus
        
-   **开源版**
    
    -   qwen3.6-35b-a3b、qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b
        
    -   qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct、qwen3-235b-a22b-thinking-2507、qwen3-235b-a22b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-30b-a3b-instruct-2507、qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b、qwen3-4b、qwen3-1.7b、qwen3-0.6b
        
    -   qwen2.5-14b-instruct-1m、qwen2.5-7b-instruct-1m、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct
        

## 全球

-   **商业版**
    
    -   **千问Max系列**：qwen3.7-max、qwen3.7-max-2026-05-20、qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版模型
        
    -   **千问Plus系列**：qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.5-plus、qwen3.5-plus-2026-02-15、qwen-plus、qwen-plus-latest、qwen-plus-2024-12-20及之后的快照版模型
        
    -   **千问Flash系列**：qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版模型；qwen-flash、qwen-flash-2025-07-28
        
-   **开源版**
    
    -   qwen3.5-397b-a17b、qwen3.5-122b-a10b、qwen3.5-27b、qwen3.5-35b-a3b、qwen3-next-80b-a3b-thinking、qwen3-next-80b-a3b-instruct、qwen3-235b-a22b-thinking-2507、qwen3-235b-a22b-instruct-2507、qwen3-30b-a3b-thinking-2507、qwen3-30b-a3b-instruct-2507、qwen3-235b-a22b、qwen3-32b、qwen3-30b-a3b、qwen3-14b、qwen3-8b
        

## 通过OpenAI SDK调用

### **前提条件**

-   请确保您的计算机上安装了Python环境。
    

-   请安装最新版OpenAI SDK。
    
    ```
    # 如果下述命令报错，请将pip替换为pip3
    pip install -U openai
    ```
    
-   您需要开通阿里云百炼模型服务并获得API-KEY，详情请参考：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    

-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄露风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，**但是泄露风险会提高**。
    
-   请选择您需要使用的模型：[支持的模型列表](#eadfc13038jd5)。
    

### **使用方式**

您可以参考以下示例来使用OpenAI SDK访问百炼服务上的千问模型。

#### **非流式调用示例**

```
from openai import OpenAI
import os

def get_response():
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下是北京地域base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': '你是谁？'}]
        )
    print(completion.model_dump_json())

if __name__ == '__main__':
    get_response()
```

运行代码可以获得以下结果：

```
{
    "id": "chatcmpl-xxx",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null,
            "message": {
                "content": "我是来自阿里云的超大规模预训练模型，我叫千问。",
                "role": "assistant",
                "function_call": null,
                "tool_calls": null
            }
        }
    ],
    "created": 1716430652,
    "model": "qwen-plus",
    "object": "chat.completion",
    "system_fingerprint": null,
    "usage": {
        "completion_tokens": 18,
        "prompt_tokens": 22,
        "total_tokens": 40
    }
}
```

#### **流式调用示例**

```
from openai import OpenAI
import os

def get_response():
    client = OpenAI(
        # 如果您没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下是北京地域base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[{'role': 'system', 'content': 'You are a helpful assistant.'},
                  {'role': 'user', 'content': '你是谁？'}],
        stream=True,
        # 通过以下设置，在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": True}
        )
    for chunk in completion:
        print(chunk.model_dump_json())

if __name__ == '__main__':
    get_response()
```

运行代码可以获得以下结果：

```
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"","function_call":null,"role":"assistant","tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"我是","function_call":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"来自","function_call":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"阿里","function_call":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"云的大规模语言模型","function_call":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"，我叫千问。","function_call":null,"role":null,"tool_calls":null},"finish_reason":null,"index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[{"delta":{"content":"","function_call":null,"role":null,"tool_calls":null},"finish_reason":"stop","index":0,"logprobs":null}],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":null}
{"id":"chatcmpl-xxx","choices":[],"created":1719286190,"model":"qwen-plus","object":"chat.completion.chunk","system_fingerprint":null,"usage":{"completion_tokens":16,"prompt_tokens":22,"total_tokens":38}}
```

#### **function call示例**

此处以天气查询工具与时间查询工具为例，向您展示通过OpenAI接口兼容实现function call的功能。示例代码可以实现多轮工具调用。

```
from openai import OpenAI
from datetime import datetime
import json
import os

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            # 因为获取当前时间无需输入参数，因此parameters为空字典
            "parameters": {}
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": { 
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]

# 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
def get_current_weather(location):
    return f"{location}今天是雨天。 "

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

# 封装模型响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        tools=tools
        )
    return completion.model_dump()

def call_with_messages():
    print('\n')
    messages = [
            {
                "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
                "role": "user"
            }
    ]
    print("-"*60)
    # 模型的第一轮调用
    i = 1
    first_response = get_response(messages)
    assistant_output = first_response['choices'][0]['message']
    print(f"\n第{i}轮大模型输出信息：{first_response}\n")
    if  assistant_output['content'] is None:
        assistant_output['content'] = ""
    messages.append(assistant_output)
    # 如果不需要调用工具，则直接返回最终答案
    if assistant_output['tool_calls'] == None:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        print(f"无需调用工具，我可以直接回复：{assistant_output['content']}")
        return
    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while assistant_output['tool_calls'] != None:
        # 如果判断需要调用查询天气工具，则运行查询天气工具
        if assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
            tool_info = {"name": "get_current_weather", "role":"tool"}
            # 提取位置参数信息
            location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
            tool_info['content'] = get_current_weather(location)
        # 如果判断需要调用查询时间工具，则运行查询时间工具
        elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
            tool_info = {"name": "get_current_time", "role":"tool"}
            tool_info['content'] = get_current_time()
        print(f"工具输出信息：{tool_info['content']}\n")
        print("-"*60)
        messages.append(tool_info)
        assistant_output = get_response(messages)['choices'][0]['message']
        if  assistant_output['content'] is None:
            assistant_output['content'] = ""
        messages.append(assistant_output)
        i += 1
        print(f"第{i}轮大模型输出信息：{assistant_output}\n")
    print(f"最终答案：{assistant_output['content']}")

if __name__ == '__main__':
    call_with_messages()
```

当输入：`杭州和北京天气怎么样？现在几点了？`时，程序会进行如下输出：

![2024-06-26\_10-04-56 (1).gif](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8001739171/p814524.gif)

### **输入参数配置**

输入参数与OpenAI的接口参数对齐，当前已支持的参数如下：

**参数**

**类型**

**默认值**

**说明**

model

_string_

\-

用户使用model参数指明对应的模型，可选的模型请见[支持的模型列表](#eadfc13038jd5)。

messages

_array_

\-

用户与模型的对话历史。array中的每个元素形式为`{"role":角色, "content": 内容}`。角色当前可选值：system、user、assistant，其中，仅`messages[0]`中支持role为system，一般情况下，user和assistant需要交替出现，且messages中最后一个元素的role必须为user。

top\_p（可选）

_float_

\-

生成过程中的核采样方法概率阈值，例如，取值为0.8时，仅保留概率加起来大于等于0.8的最可能token的最小集合作为候选集。取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越小，生成的确定性越高。

temperature（可选）

_float_

\-

用于控制模型回复的随机性和多样性。具体来说，temperature值控制了生成文本时对每个候选词的概率分布进行平滑的程度。较高的temperature值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的temperature值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。

取值范围： \[0, 2)，不建议取值为0，无意义。

presence\_penalty

（可选）

_float_

\-

用户控制模型生成时整个序列中的重复度。提高presence\_penalty时可以降低模型生成的重复度，取值范围\[-2.0, 2.0\]。

**说明**

目前仅在千问商业模型和qwen1.5及以后的开源模型上支持该参数。

n（可选）

_integer_

1

生成响应的个数，取值范围是`1-4`。对于需要生成多个响应的场景（如创意写作、广告文案等），可以设置较大的 n 值。

> 设置较大的 n 值不会增加输入 Token 消耗，会增加输出 Token 的消耗。

> 当前仅支持 qwen-plus 模型，且在传入 tools 参数时固定为1。

max\_tokens（可选）

_integer_

\-

指定模型可生成的最大token个数。例如模型最大输出长度为2k，您可以设置为1k，防止模型输出过长的内容。

不同的模型有不同的输出上限，具体请参见模型列表。

seed（可选）

_integer_

\-

生成时使用的随机数种子，用于控制模型生成内容的随机性。seed支持无符号64位整数。

stream（可选）

_boolean_

False

用于控制是否使用流式输出。当以stream模式输出结果时，接口返回结果为generator，需要通过迭代获取结果，每次输出为当前生成的增量序列。

stop（可选）

_string or array_

None

stop参数用于实现内容生成过程的精确控制，在模型生成的内容即将包含指定的字符串或token\_id时自动停止。stop可以为string类型或array类型。

-   string类型
    
    当模型将要生成指定的stop词语时停止。
    
    例如将stop指定为"你好"，则模型将要生成“你好”时停止。
    
-   array类型
    
    array中的元素可以为token\_id或者字符串，或者元素为token\_id的array。当模型将要生成的token或其对应的token\_id在stop中时，模型生成将会停止。以下为stop为array时的示例（tokenizer对应模型为qwen-turbo）：
    
    1.元素为token\_id：
    
    token\_id为108386和104307分别对应token为“你好”和“天气”，设定stop为`[108386,104307]`，则模型将要生成“你好”或者“天气”时停止。
    
    2.元素为字符串：
    
    设定stop为`["你好","天气"]`，则模型将要生成“你好”或者“天气”时停止。
    
    3.元素为array：
    
    token\_id为108386和103924分别对应token为“你好”和“啊”，token\_id为35946和101243分别对应token为“我”和“很好”。设定stop为`[[108386, 103924],[35946, 101243]]`，则模型将要生成“你好啊”或者“我很好”时停止。
    
    **说明**
    
    stop为array类型时，不可以将token\_id和字符串同时作为元素输入，比如不可以指定stop为`["你好",104307]`。
    

tools（可选）

_array_

None

用于指定可供模型调用的工具库，一次function call流程模型会从中选择其中一个工具。tools中每一个tool的结构如下：

-   type，类型为string，表示tools的类型，当前仅支持function。
    
-   function，类型为object，键值包括name，description和parameters：
    
    -   name：类型为string，表示工具函数的名称，必须是字母、数字，可以包含下划线和短划线，最大长度为64。
        
    -   description：类型为string，表示工具函数的描述，供模型选择何时以及如何调用工具函数。
        
    -   parameters：类型为object，表示工具的参数描述，需要是一个合法的JSON Schema。JSON Schema的描述可以见[链接](https://json-schema.org/understanding-json-schema)。如果parameters参数为空，表示function没有入参。
        
        parameters中各属性的`type`支持JSON Schema定义的常见类型，包括`string`、`number`、`integer`、`boolean`、`array`和`object`等。当属性类型为`array`时，需要通过`items`字段指定数组元素的类型。示例如下：
        
        ```
        {
            "type": "object",
            "properties": {
                "command": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "要执行的命令，例如['ls', '-l']"
                }
            },
            "required": ["command"]
        }
        ```
        

在function call流程中，无论是发起function call的轮次，还是向模型提交工具函数的执行结果，均需设置tools参数。当前支持的模型包括qwen-turbo、qwen-plus和qwen-max。

**说明**

tools暂时无法与stream=True同时使用。

stream\_options（可选）

_object_

None

该参数用于配置在流式输出时是否展示使用的token数目。只有当stream为True的时候该参数才会激活生效。若您需要统计流式输出模式下的token数目，可将该参数配置为`stream_options={"include_usage":True}`。

enable\_search

_boolean_

False

用于控制模型在生成文本时是否使用互联网搜索结果进行参考。取值如下：

-   True：启用互联网搜索，模型会将搜索结果作为文本生成过程中的参考信息，但模型会基于其内部逻辑判断是否使用互联网搜索结果。
    
    > 若开启后未联网搜索，可优化提示词，或设置`search_options`中的`forced_search`参数开启强制搜索。
    
-   False（默认）：关闭互联网搜索。
    

> qwen-long暂不支持此参数。

配置方式为：`extra_body={"enable_search": True}`。

### **返回参数说明**

**返回参数**

**数据类型**

**说明**

**备注**

id

_string_

系统生成的标识本次调用的id。

无

model

_string_

本次调用的模型名。

无

system\_fingerprint

_string_

模型运行时使用的配置版本，当前暂时不支持，返回为空字符串“”。

无

choices

_array_

模型生成内容的详情。

无

choices\[i\].finish\_reason

_string_

有三种情况：

-   正在生成时为null；
    
-   因触发输入参数中的stop条件而结束为stop；
    
-   因生成长度过长而结束为length。
    

choices\[i\].message

_object_

模型输出的消息。

choices\[i\].message.role

_string_

模型的角色，固定为assistant。

choices\[i\].message.content

_string_

模型生成的文本。

choices\[i\].index

_integer_

生成的结果序列编号，默认为0。

created

_integer_

当前生成结果的时间戳（s）。

无

usage

_object_

计量信息，表示本次请求所消耗的token数据。

无

usage.prompt\_tokens

_integer_

用户输入文本转换成token后的长度。

无

usage.completion\_tokens

_integer_

模型生成回复转换为token后的长度。

无

usage.total\_tokens

_integer_

usage.prompt\_tokens与usage.completion\_tokens的总和。

无

## 通过langchain\_openai SDK调用

### **前提条件**

-   请确保您的计算机上安装了Python环境。
    

-   通过运行以下命令安装langchain\_openai SDK。
    
    ```
    # 如果下述命令报错，请将pip替换为pip3
    pip install -U langchain_openai
    ```
    

-   您需要开通阿里云百炼模型服务并获得API-KEY，详情请参考：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄露风险，详情可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，**但是泄露风险会提高**。
    
-   请选择您需要使用的模型：[支持的模型列表](#eadfc13038jd5)。
    

### **使用方式**

您可以参考以下示例来通过langchain\_openai SDK使用阿里云百炼的千问模型。

#### **非流式输出**

非流式输出使用invoke方法实现，请参考以下示例代码：

```
from langchain_openai import ChatOpenAI
import os

def get_response():
    llm = ChatOpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下是北京地域base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"    # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        )
    messages = [
        {"role":"system","content":"You are a helpful assistant."}, 
        {"role":"user","content":"你是谁？"}
    ]
    response = llm.invoke(messages)
    print(response.json())

if __name__ == "__main__":
    get_response()
```

运行代码，可以得到以下结果：

```
{
    "content": "我是来自阿里云的大规模语言模型，我叫千问。",
    "additional_kwargs": {},
    "response_metadata": {
        "token_usage": {
            "completion_tokens": 16,
            "prompt_tokens": 22,
            "total_tokens": 38
        },
        "model_name": "qwen-plus",
        "system_fingerprint": "",
        "finish_reason": "stop",
        "logprobs": null
    },
    "type": "ai",
    "name": null,
    "id": "run-xxx",
    "example": false,
    "tool_calls": [],
    "invalid_tool_calls": []
}
```

#### **流式输出**

流式输出使用stream方法实现，无需在参数中配置stream参数。

```
from langchain_openai import ChatOpenAI
import os

def get_response():
    llm = ChatOpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下是北京地域base_url
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", 
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        stream_usage=True
        )
    messages = [
        {"role":"system","content":"You are a helpful assistant."}, 
        {"role":"user","content":"你是谁？"},
    ]
    response = llm.stream(messages)
    for chunk in response:
        print(chunk.model_dump_json())

if __name__ == "__main__":
    get_response()
```

运行代码，可以得到以下结果：

```
{"content": "", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "我是", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "来自", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "阿里", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "云", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "的大规模语言模型", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "，我叫通", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "义千问。", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "", "additional_kwargs": {}, "response_metadata": {"finish_reason": "stop"}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": {"input_tokens": 22, "output_tokens": 16, "total_tokens": 38}, "tool_call_chunks": []}
```

关于输入参数的配置，可以参考[输入参数配置](#d553cbbee6mxk)，相关参数在ChatOpenAI对象中定义。

## **通过HTTP接口调用**

您可以通过HTTP接口来调用阿里云百炼服务，获得与通过HTTP接口调用OpenAI服务相同结构的返回结果。

### **前提条件**

-   您需要开通阿里云百炼模型服务并获得API-KEY，详情请参考：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄露风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，**但是泄露风险会提高**。
    

### **提交接口调用**

```
北京：POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
美国（弗吉尼亚）：POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
新加坡：POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
```

### **请求示例**

以下示例展示通过`cURL`命令来调用API的脚本。

**说明**

如果您没有配置API-KEY为环境变量，需将$DASHSCOPE\_API\_KEY更改为您的API-KEY_。_

#### **非流式输出**

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url
# === 执行时请删除该注释 ===
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-plus",  
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "你是谁？"
        }
    ]
}'
```

运行命令可得到以下结果：

```
{
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "我是来自阿里云的大规模语言模型，我叫千问。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
        }
    ],
    "object": "chat.completion",
    "usage": {
        "prompt_tokens": 11,
        "completion_tokens": 16,
        "total_tokens": 27
    },
    "created": 1715252778,
    "system_fingerprint": "",
    "model": "qwen-plus",
    "id": "chatcmpl-xxx"
}
```

#### **流式输出**

如果您需要使用流式输出，请在请求体中指定stream参数为true。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url
# === 执行时请删除该注释 ===
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-plus",  
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user", 
            "content": "你是谁？"
        }
    ],
    "stream":true
}'
```

运行命令可得到以下结果：

```
data: {"choices":[{"delta":{"content":"","role":"assistant"},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"finish_reason":null,"delta":{"content":"我是"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"delta":{"content":"来自"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"delta":{"content":"阿里"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"delta":{"content":"云的大规模语言模型"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"delta":{"content":"，我叫千问。"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: {"choices":[{"delta":{"content":""},"finish_reason":"stop","index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1715931028,"system_fingerprint":null,"model":"qwen-plus","id":"chatcmpl-3bb05cf5cd819fbca5f0b8d67a025022"}

data: [DONE]
```

输入参数的详情请参考[输入参数配置](#d553cbbee6mxk)。

### **异常响应示例**

在访问请求出错的情况下，输出的结果中会通过 code 和 message 指明出错原因。

```
{
    "error": {
        "message": "Incorrect API key provided. ",
        "type": "invalid_request_error",
        "param": null,
        "code": "invalid_api_key"
    }
}
```

## **状态码说明**

**错误码**

**说明**

400 - Invalid Request Error

输入请求错误，细节请参见具体报错信息。

401 - Incorrect API key provided

API key不正确。

429 - Rate limit reached for requests

QPS、QPM等超限。

429 - You exceeded your current quota, please check your plan and billing details

额度超限或者欠费。

500 - The server had an error while processing your request

服务端错误。

503 - The engine is currently overloaded, please try again later

服务端负载过高，可重试。
