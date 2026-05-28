# OpenAI Vision接口兼容

阿里云百炼的通义千问视觉模型兼容OpenAI接口规范。将原有 OpenAI 应用迁移至阿里云百炼只需调整三个参数：

-   base\_url：替换为 https://dashscope.aliyuncs.com/compatible-mode/v1
    
    > 若使用弗吉尼亚地域模型，需要将base\_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1，若使用新加坡地域的模型，需要将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    
-   api\_key：替换为[阿里云百炼API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
    
-   model: 替换为以下模型列表中的名称
    

## **支持的模型**

## 中国内地（北京）

-   通义千问VL 系列模型
    
    -   qwen3-vl-plus、qwen3-vl-plus-2025-12-19、qwen3-vl-plus-2025-09-23、qwen3-vl-flash、qwen3-vl-flash-2025-10-15、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct、qwen3-vl-32b-instruct、qwen3-vl-30b-a3b-thinking、qwen3-vl-30b-a3b-instruct、qwen3-vl-8b-thinking、qwen3-vl-8b-instruct
        
    -   qwen-vl-max、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-08-13、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2025-01-25、qwen-vl-max-2024-12-30、qwen-vl-max-2024-11-19、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-08-15、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-01-25、qwen-vl-plus-2025-01-02、qwen2.5-vl-72b-instruct 、qwen2.5-vl-32b-instruct
        
-   QVQ系列模型：qvq-max、qvq-max-latest、qvq-max-2025-05-15、qvq-max-2025-03-25、qvq-plus、qvq-plus-latest、qvq-plus-2025-05-15
    
-   通义千问OCR系列模型：qwen-vl-ocr、qwen-vl-ocr-latest、qwen-vl-ocr-2025-11-20、qwen-vl-ocr-2025-08-28、qwen-vl-ocr-2025-04-13、qwen-vl-ocr-2024-10-28
    

## 国际（新加坡）

-   Qwen-VL 系列模型：
    
-   qwen3-vl-plus、qwen3-vl-plus-2025-12-19、qwen3-vl-plus-2025-09-23、qwen3-vl-flash、qwen3-vl-flash-2025-10-15、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct、qwen3-vl-32b-instruct、qwen3-vl-30b-a3b-thinking、qwen3-vl-30b-a3b-instruct、qwen3-vl-8b-thinking、qwen3-vl-8b-instruct
    
-   qwen-vl-max、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-08-13、qwen-vl-max-2025-04-08、qwen-vl-max-2025-04-02、qwen-vl-max-2025-01-25、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2025-08-15、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-05-07、qwen-vl-plus-2025-01-25、qwen2.5-vl-72b-instruct 、qwen2.5-vl-32b-instruct、qwen2.5-vl-7b-instruct、qwen2.5-vl-3b-instruct
    
-   QVQ系列模型：qvq-max、qvq-max-latest、qvq-max-2025-03-25
    
-   通义千问OCR系列模型：qwen-vl-ocr、qwen-vl-ocr-2025-11-20
    

## 模型调用

### **调用示例**

本章节提供Python（OpenAI SDK与LangChain\_OpenAI SDK）和cURL（HTTP接口）的流式调用示例，更多编程语言或输入方式示例请参考：[视觉理解请求示例](https://help.aliyun.com/zh/model-studio/vision#7a7077f8a9r6o)。

> QVQ模型仅支持流式输出，具体使用方法请参见[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)。

## 使用OpenAI SDK调用

```
from openai import OpenAI
import os

def get_response():
    client = OpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
        # 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=[
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "这是什么"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                  }
                }
              ]
            }
          ],
        stream=True,
        stream_options={"include_usage":True}
        )
    for chunk in completion:
        print(chunk.model_dump())

if __name__=='__main__':
    get_response()
```

运行代码可以获得以下结果：

```
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '', 'function_call': None, 'refusal': None, 'role': 'assistant', 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '这张', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '照片', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '展示', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}

......

{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '瞬间', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '。', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': None, 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [{'delta': {'content': '', 'function_call': None, 'refusal': None, 'role': None, 'tool_calls': None}, 'finish_reason': 'stop', 'index': 0, 'logprobs': None}], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': None}
{'id': 'chatcmpl-31042a05-c968-4fc6-ba28-c3aa471258dc', 'choices': [], 'created': 1765780318, 'model': 'qwen-vl-plus', 'object': 'chat.completion.chunk', 'service_tier': None, 'system_fingerprint': None, 'usage': {'completion_tokens': 230, 'prompt_tokens': 1259, 'total_tokens': 1489, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None, 'text_tokens': 230}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}}
```

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
    

### **使用方式**

您可以参考以下示例来通过langchain\_openai SDK使用通义千问视觉模型。

#### **非流式输出**

非流式输出使用invoke方法实现，请参考以下示例代码：

```
from langchain_openai import ChatOpenAI
import os

def get_response():
    llm = ChatOpenAI(
      # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      # 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
      # 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      model="qwen3-vl-plus",
      )
    messages= [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "这是什么"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                  }
                }
              ]
            }
          ]
    response = llm.invoke(messages)
    print(response.content)

if __name__ == "__main__":
    get_response()
```

运行代码，可以得到以下结果：

```
{
  "content": "这张照片展示了一位女性和一只狗在海滩上的温馨互动。以下是照片的详细描述：\n\n1. **场景**：\n   - 照片拍摄于海滩，背景是大海和天空。\n   - 太阳即将落山或刚刚升起，阳光洒在沙滩上，营造出温暖的金色光线。\n\n2. **人物**：\n   - 一位女性坐在沙滩上，穿着格子衬衫和深色裤子。\n   - 她面带微笑，显得非常开心和放松。\n\n3. **动物**：\n   - 一只黄色的拉布拉多犬坐在女性旁边。\n   - 狗戴着彩色的胸背带，看起来很健康和友好。\n   - 狗用前爪轻轻搭在女性的手上，仿佛在进行“握手”动作。\n\n4. **互动**：\n   - 女性和狗之间的互动显得非常亲密和愉快。\n   - 这种互动展示了人与宠物之间的深厚感情。\n\n5. **氛围**：\n   - 整体氛围非常宁静和美好，给人一种放松和幸福的感觉。\n   - 海浪的声音和夕阳的美景为这个场景增添了浪漫的气息。\n\n这张照片捕捉了一个简单而美好的瞬间，展示了人与宠物之间的和谐关系，以及大自然带来的宁静与美好。",
  "additional_kwargs": {
    "refusal": null
  },
  "response_metadata": {
    "token_usage": {
      "completion_tokens": 267,
      "prompt_tokens": 1259,
      "total_tokens": 1526,
      "completion_tokens_details": {
        "accepted_prediction_tokens": null,
        "audio_tokens": null,
        "reasoning_tokens": null,
        "rejected_prediction_tokens": null,
        "text_tokens": 267
      },
      "prompt_tokens_details": {
        "audio_tokens": null,
        "cached_tokens": 0
      }
    },
    "model_provider": "openai",
    "model_name": "qwen-vl-plus",
    "system_fingerprint": null,
    "id": "chatcmpl-9f3eba85-4f7a-4f73-b254-220a650xxxxx",
    "finish_reason": "stop",
    "logprobs": null
  },
  "type": "ai",
  "name": null,
  "id": "lc_run--019b1191-f411-7153-ac51-b8b0410xxxxx-0",
  "tool_calls": [],
  "invalid_tool_calls": [],
  "usage_metadata": {
    "input_tokens": 1259,
    "output_tokens": 267,
    "total_tokens": 1526,
    "input_token_details": {
      "cache_read": 0
    },
    "output_token_details": {}
  }
}
```

#### **流式输出**

> 以下示例不适用QVQ模型，QVQ调用方法请参见[视觉推理](https://help.aliyun.com/zh/model-studio/visual-reasoning)。

```
from langchain_openai import ChatOpenAI
import os

def get_response():
    llm = ChatOpenAI(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1
        # 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen3-vl-plus",
        # 通过以下设置，在流式输出的最后一行展示token使用信息
        stream_options={"include_usage": True}
    )
    messages= [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "这是什么"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
                  }
                }
              ]
            }
          ]
    response = llm.stream(messages)
    for chunk in response:
        print(chunk.content)

if __name__ == "__main__":
    get_response()
```

运行以上代码，可得到以下示例结果：

```
{"content": "", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "这张", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "图片", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "中", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "有一", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "只狗和一个小", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "女孩。狗看起来", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "很友好，可能是", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "宠物，而小女孩", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "似乎在与狗", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "互动或玩耍。", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "这是一幅展示", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "人与动物之间", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "温馨关系的画面。", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "", "additional_kwargs": {}, "response_metadata": {"finish_reason": "stop"}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": null, "tool_call_chunks": []}
{"content": "", "additional_kwargs": {}, "response_metadata": {}, "type": "AIMessageChunk", "name": null, "id": "run-xxx", "example": false, "tool_calls": [], "invalid_tool_calls": [], "usage_metadata": {"input_tokens": 23, "output_tokens": 40, "total_tokens": 63}, "tool_call_chunks": []}
```

关于输入参数的配置，可以参考[输入参数配置](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#d553cbbee6mxk)，相关参数在ChatOpenAI对象中定义。

## **通过HTTP接口调用**

您可以通过HTTP接口来调用通义千问视觉模型，获得与通过HTTP接口调用OpenAI服务相同结构的返回结果。

### **前提条件**

-   您需要开通阿里云百炼模型服务并获得API-KEY，详情请参考：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。
    
-   我们推荐您将API-KEY配置到环境变量中以降低API-KEY的泄露风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，**但是泄露风险会提高**。
    

### **提交接口调用**

```
北京：POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
新加坡：POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
弗吉尼亚：POST https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
```

### **请求示例**

以下示例展示通过`CURL`命令来调用API的脚本。

**说明**

如果您没有配置API-KEY为环境变量，需将$DASHSCOPE\_API\_KEY更换为您的API-KEY_。_

#### **非流式输出**

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
# 若使用新加坡地域的模型，需将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "这些是什么"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
          }
        }
      ]
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
        "content": "图1中是一名女子和她的宠物狗在沙滩上互动，狗狗抬起前爪似乎想要握手。\n图2是CG渲染的一张老虎的图片。",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 2509,
    "completion_tokens": 34,
    "total_tokens": 2543
  },
  "created": 1724729556,
  "system_fingerprint": null,
  "model": "qwen-vl-plus",
  "id": "chatcmpl-1abb4eb9-f508-9637-a8ba-ac7fc6f73e53"
}
```

#### **流式输出**

如果您需要使用流式输出，请在请求体中指定stream参数为true。

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://dashscope-us.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3-vl-plus",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "这是什么"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
          }
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{"include_usage":true}
}'
```

运行命令可得到以下结果：

```
data: {"choices":[{"delta":{"content":"","role":"assistant"},"index":0,"logprobs":null,"finish_reason":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"finish_reason":null,"delta":{"content":"图"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"中"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"是一名"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"女子和她的狗在"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"沙滩上互动。狗狗坐在地上，"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"伸出爪子像是要握手或者击"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"掌的样子。这名女士穿着格子"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"衬衫，似乎正在与狗狗进行亲密"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"的接触，并且面带微笑。"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"背景是海洋和日出或日"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"落时分的天空。这是一"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"delta":{"content":"张充满温馨感的照片，展现了人"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[{"finish_reason":"stop","delta":{"content":"与宠物之间的友谊时刻。"},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":1276,"completion_tokens":79,"total_tokens":1355},"created":1724729595,"system_fingerprint":null,"model":"qwen-vl-plus","id":"chatcmpl-4c83f437-303f-907b-9de5-79cac83d6b18"}

data: [DONE]
```

输入参数的详情请参考[输入参数配置](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#d553cbbee6mxk)。

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

相关状态错误码信息参考：[状态码说明](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope#8dd39ae94bygm)。
