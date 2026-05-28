# RunChatResultGeneration - 对话结果生成

对话结果生成，可选择模型进行对话，支持流式和非流式。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RunChatResultGeneration)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RunChatResultGeneration)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

dianjin:RunChatResultGeneration

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/run/chat/generation HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

路径参数，业务空间 id。

llm-xxxxx

body

object

否

请求体参数。

inferenceParameters

object

否

推理使用的超参数

{"topP": 0.8}

messages

array<object>

是

输入模型的消息

Message

object

否

content

string

否

消息的内容

你是一个信息处理专家

role

string

否

消息的角色

user

modelId

string

是

模型服务种类，请通过/api/app/config 接口获取，对应的字段 llmHelperTypeList

qwen-max

sessionId

string

否

sessionId，可用于标记对话

237645726354

stream

boolean

否

是否流式: true，流式返回答案；false，全量返回答案。不填默认为 false

false

tools

array<object>

否

输入的工具信息. 用于指定可供模型调用的工具列表。当输入多个工具时，模型会选择其中一个生成结果。

Tool

object

否

工具信息

function

object

否

类型为 object，键值包括 name，description 和 parameters

description

string

否

类型为 string，表示工具函数的描述，供模型选择何时以及如何调用工具函数

工具函数的描述

name

string

否

类型为 string，表示工具函数的名称，必须是字母、数字，可以包含下划线和短划线，最大长度为 64

get\_time

parameters

object

否

类型为 object，表示工具的参数描述，需要是一个合法的 JSON Schema。

properties

object

否

属性

{ "location": { "type": "string", "description": "The city and state, e.g. San Francisco, CA" }, "unit": { "type": "string", "enum": \[ "celsius", "fahrenheit" \] } }

type

string

否

类型

object

required

array

否

必填参数列表

Required

string

否

必填参数

location

type

string

否

类型为 string，表示 tools 的类型，当前仅支持 function

function

## 返回参数

名称

类型

描述

示例值

object

choices

array<object>

模型生成内容的详情。

choice

object

模型生成内容的详情。

finishReason

string

有三种情况：

-   正在生成时为 null；
    
-   因触发输入参数中的 stop 条件而结束为 stop；
    
-   因生成长度过长而结束为 length。
    

null

index

integer

生成的结果序列编号，默认为 0。

0

message

object

对话消息

content

string

对话内容

你是谁

role

string

角色

user

toolCalls

array<object>

工具调用列表

toolCall

object

工具调用

{ "type": "function", "function": { "name": "get\_current\_weather", "arguments": "{\\"location\\": \\"长沙\\", \\"unit\\": \\"celsius\\"}" }, "id": "" }

created

long

创建时间

1720602203

id

string

请求标识

eb2b6139-ddf1-91a0-a47f-df7617ae9032

modelId

string

大模型 ID。

qwen-max

requestId

string

请求 id

eb2b6139-ddf1-91a0-a47f-df7617ae9032

time

string

时间戳

2024-04-24 11:54:34

totalTokens

integer

Tokens 总量

500

usage

object

用量

imageCount

integer

图片数，wanx 等模型返回

0

imageTokens

integer

图片 Tokens，qwen-vl 等模型返回

0

inputTokens

integer

输入 Tokens

200

outputTokens

integer

输出 Tokens

300

totalTokens

integer

Tokens 总量

500

## 示例

正常返回示例

`JSON`格式

```
{
  "choices": [
    {
      "finishReason": null,
      "index": 0,
      "message": {
        "content": "你是谁",
        "role": "user",
        "toolCalls": [
          {
            "type": "function",
            "function": {
              "name": "get_current_weather",
              "arguments": {
                "location": "长沙",
                "unit": "celsius"
              }
            },
            "id": ""
          }
        ]
      }
    }
  ],
  "created": 1720602203,
  "id": "eb2b6139-ddf1-91a0-a47f-df7617ae9032",
  "modelId": "qwen-max",
  "requestId": "eb2b6139-ddf1-91a0-a47f-df7617ae9032\n",
  "time": "2024-04-24 11:54:34",
  "totalTokens": 500,
  "usage": {
    "imageCount": 0,
    "imageTokens": 0,
    "inputTokens": 200,
    "outputTokens": 300,
    "totalTokens": 500
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
