# Qwen-Deep-Research API 参考

本文介绍通过 DashScope API 调用 Qwen-Deep-Research 模型的输入与输出参数。

> 相关文档：[深入研究（Qwen-Deep-Research）](https://help.aliyun.com/zh/model-studio/qwen-deep-research)

**重要**

本文档仅适用于**中国大陆版**（北京）。如需使用模型，需使用**中国大陆版**（北京）的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

**说明**

模型当前仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 OpenAI 兼容接口。

## DashScope

> 您需要已[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过DashScope SDK进行调用，需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk#f3e80b21069aa)。

### 请求体

## Python

```
import os
import dashscope

# 第一步：模型反问确认
messages = [{'role': 'user', 'content': '研究一下人工智能在教育中的应用'}]

responses = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-deep-research",
    messages=messages,
    stream=True
)

# 获取模型反问内容
step1_content = ""
for response in responses:
    if hasattr(response, 'output') and response.output:
        message = response.output.get('message', {})
        content = message.get('content', '')
        if content:
            step1_content += content
            print(content, end='', flush=True)

# 第二步：深入研究
messages = [
    {'role': 'user', 'content': '研究一下人工智能在教育中的应用'},
    {'role': 'assistant', 'content': step1_content},
    {'role': 'user', 'content': '我主要关注个性化学习和智能评估这两个方面'}
]

responses = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-deep-research",
    messages=messages
)

# 流式输出研究结果
for response in responses:
    if hasattr(response, 'output') and response.output:
        message = response.output.get('message', {})
        content = message.get('content', '')
        if content:
            print(content, end='', flush=True)
```

## curl

```
echo "第一步：模型反问确认"
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'X-DashScope-SSE: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "messages": [
            {
                "content": "研究一下人工智能在教育中的应用", 
                "role": "user"
            }
        ]
    },
    "model": "qwen-deep-research"
}'

echo -e "\n\n" 
echo "第二步：深入研究"
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'X-DashScope-SSE: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "input": {
        "messages": [
            {
                "content": "研究一下人工智能在教育中的应用", 
                "role": "user"
            },
            {
                "content": "请告诉我您希望重点研究人工智能在教育中的哪些具体应用场景？", 
                "role": "assistant"
            },
            {
                "content": "我主要关注个性化学习方面", 
                "role": "user"
            }
        ]
    },
    "model": "qwen-deep-research"
}'
```

**model** `_string_` **（必选）**

模型名称。支持的模型：qwen-deep-research。

**messages** `_array_` **（必选）**

传递给大模型的上下文，按对话顺序排列。

**消息类型**

User Message `_object_`**（必选）**

用户消息，用于向模型传递问题、指令或上下文。在 Qwen-Deep-Research 的两阶段调用流程中，用户消息起到不同作用：

-   **第一步（模型反问确认）**：用户消息用于发起初始的研究请求，提出一个较为宽泛的研究主题。
    
-   **第二步（深入研究）**：用户消息用于回答模型提出的澄清式问题，帮助模型聚焦研究方向，进行更具针对性的深入分析。
    

**属性**

**content** `_string_`**（必选）**

消息内容。

**role** `_string_` **（必选）**

系统消息的角色，固定为user。

Assistant Message `_object_` （可选）

模型对用户消息的回复。在第二步（深入研究）的API调用中，此参数用以传入模型在第一步（反问确认）中返回的澄清式问题，作为对话历史的一部分，从而引导模型进行更具针对性的分析。

**content** `_string_` （可选）

消息内容。

**role** `_string_` **（必选）**

固定为`assistant`。

**output\_format** `_string_` （可选）

指定输出研究报告的格式和详细程度。支持以下取值：

-   `model_detailed_report`（默认） 生成一份结构完整、内容详尽的深度研究报告，篇幅约6000 Token，适合需要全面深入分析的场景。
    
-   `model_summary_report` 生成一份核心观点突出、内容精炼的摘要式研究报告，篇幅约1500-2000 Token，适合快速了解关键信息和结论的场景。
    

### 响应对象

## 研究规划阶段

```
{
  "status_code": 200,
  "request_id": "2a6187f0-7e7b-40bb-a87e-xxx",
  "code": "",
  "message": "",
  "output": {
        "text": null, 
        "finish_reason": null, 
        "choices": null, 
        "message": {
            "phase": "ResearchPlanning",
            "role": "assistant",
            "content": "",
            "extra": {
                "deep_research": {}
            },
            "status": "typing"
        },
        "fininshed": false,
        "fininshed_reason": "null"
    },
    "usage": {
        "input_tokens": 694,
        "output_tokens": 0
    },
    "request_id": "2a6187f0-7e7b-40bb-xxx"
}
```

## 网络搜索阶段

```
{
  "status_code": 200,
  "request_id": "2a6187f0-7e7b-40bb-a87e-xxx",
  "code": "",
  "message": "",
  "output": {
    "message": {
      "phase": "WebResearch",
      "role": "assistant",
      "content": "",
      "extra": {
        "deep_research": {
          "query": {
            "researchGoal": "通过查找",
            "query": "",
            "id": 1
          }
        }
      },
      "status": "streamingQueries"
    },
    "fininshed": false,
    "fininshed_reason": "null"
  },
  "usage": {
    "input_tokens": 694,
    "output_tokens": 0
  }
}
```

## 连接保持阶段

```
{
  "status_code": 200,
  "request_id": "2a6187f0-7e7b-40bb-a87e-xxx",
  "code": "",
  "message": "",
  "output": {
    "message": {
      "phase": "KeepAlive",
      "role": "assistant",
      "content": "",
      "extra": {
        "deep_research": {}
      },
      "status": "typing"
    },
    "fininshed": false,
    "fininshed_reason": "null"
  },
  "usage": {
    "input_tokens": 694,
    "output_tokens": 0
  }
}
```

## 反问确认与回答阶段

```
{
  "status_code": 200,
  "request_id": "2a6187f0-7e7b-40bb-a87e-xxx",
  "code": "",
  "message": "",
  "output": {
    "message": {
      "phase": "answer",
      "role": "assistant",
      "content": "，这些承诺相互",
      "extra": {
        "deep_research": {
          "references": [
            {
              "icon": "",
              "index_number": 1,
              "description": "计划中设想的两个xxx从未在 ",
              "title": "历史和背景| 联合国 - the United Nations",
              "url": "https://www.un.org/xxx"
            }
          ]
        }
      },
      "status": "typing"
    },
    "fininshed": false,
    "fininshed_reason": "null"
  },
  "usage": {
    "input_tokens": 694,
    "output_tokens": 0
  }
}
```

**status\_code** `_string_`

本次请求的状态码。200 表示请求成功，否则表示请求失败。

> 调用失败会抛出异常，异常信息为**status\_code**和**message**的内容。

**request\_id** `_string_`

本次调用的唯一标识符。

**code** `_string_`

错误码，调用成功时为空值。

> 只有Python SDK返回该参数。

**message** `_string_`

错误提示信息，调用成功时为空值。

**output** `_object_`

调用结果信息。

**属性**

**text** `_string_`

该参数当前固定为`null`。

**finish\_reason** `_string_`

模型结束生成的原因。有以下情况：

-   正在生成时为`null`；
    
-   模型输出自然结束为`stop`；
    
-   因生成长度过长而结束为`length`
    

**choices** `_array_`

模型的输出信息。

**属性**

**finish\_reason** `_string_`

有以下情况：

-   正在生成时为`null`；
    
-   因模型输出自然结束为`stop`；
    
-   因生成长度过长而结束为`length`
    

**message** `_object_`

模型输出的消息对象。

**属性**

**属性**

**phase** `_string_`

当前所处阶段，其中包含：

-   answer：反问确认与回答阶段;
    
-   ResearchPlanning：研究规划阶段
    
-   WebResearch：网络搜索阶段
    
-   KeepAlive：连接保持阶段
    

**role** `_string_`

输出消息的角色，固定为`assistant`。

**content** `_string_`

模型的输出内容。

**extra** `_array_`

模型获取的网络搜索与参考信息。

**deep\_research** `_object_`

仅在`answer`与`WebResearch`阶段包含获取的网络搜索与参考信息，其余阶段均为null。

**research** `_object_`

模型的研究过程与内容信息。

**属性**

**researchGoal** `_string_`

研究目标。

**query** `_string_`

研究过程中的搜索内容。

**id** `_integer_`

搜索的轮数_，_取值范围 \[1-15\]。

**learningMap** `_object_`

从调用工具总结获取到的内容，和调用工具相关联。

**references** `_object_`

模型生成答案所引用的内容，仅回答阶段包含此参数。

**属性**

**icon** `_string_`

参考内容URL的网页图标链接。

**index\_number** `_integer_`

参考内容的索引。

**description** `_string_`

参考内容的简介。

**title** `_string_`

参考内容的网页标题。

**url** `_string_`

参考内容的网页URL。

**webSites** `_object_`

模型研究过程中所参考的内容，仅网络搜索阶段包含此参数。

**属性**

**icon** `_string_`

参考内容URL的网页图标链接。

**index\_number** `_integer_`

参考内容的索引。

**description** `_string_`

参考内容的简介。

**title** `_string_`

参考内容的网页标题。

**url** `_string_`

参考内容的网页URL。

**status** `_string_`

模型输出过程中不同阶段的状态：

-   typing：正在生成该阶段内容。
    
-   finished：阶段已完成。
    
-   streamingQueries：正在生成研究目标和搜索查询
    
-   streamingWebResult：正在执行搜索、网页阅读和代码执行
    
-   WebResultFinished：网络搜索阶段完成
    

**finished** `_boolean_`

标识模型的内容流式输出是否已全部完成。有以下情况：

-   内容仍在持续输出中为`false`；
    
-   内容已全部输出完毕，当前为最后一个响应为`true`
    

**finished\_reason** `_string_`

标识模型的内容流式输出结束的原因。有以下情况：

-   正在生成时为`null`；
    
-   模型内容流式输出自然结束为`stop`
    

**usage** `_object_`

本次请求使用的Token信息。

**属性**

**input\_tokens** `_integer_`

输入 Token 数。

**output\_tokens** `_integer_`

输出 Token 数。
