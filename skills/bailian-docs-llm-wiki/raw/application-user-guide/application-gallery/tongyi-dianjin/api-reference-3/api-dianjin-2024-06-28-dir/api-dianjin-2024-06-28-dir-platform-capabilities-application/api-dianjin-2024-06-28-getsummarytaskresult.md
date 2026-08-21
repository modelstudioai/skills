# GetSummaryTaskResult - 获取财报总结任务结果

获取财报总结任务结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetSummaryTaskResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetSummaryTaskResult)

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

dianjin:GetSummaryTaskResult

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/task/summary/result HTTP/1.1
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

业务空间 Id

llm-xxxx

taskId

string

是

任务 Id

17071319

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

object

响应数据

choices

array<object>

模型生成内容的详情。

choice

object

对话消息

finishReason

string

模型生成内容结束原因。

stop

index

integer

生成的结果序列编号，默认为 0。

0

message

object

模型输出的消息。

content

string

模型生成的文本。

\### \*\*报告期经营业绩概述\*\*\\n截至2024年3月31日止三个月的未经审核综合业绩显示强劲增长.

role

string

模型的角色，固定为 assistant。

assistant

toolCalls

array<object>

工具调用

toolCall

object

工具调用

null

created

long

创建时间

1726285125915

id

string

系统生成的标识本次调用的 id。

1202

modelId

string

本次调用的模型名。

qwen-max

requestId

string

请求 id

0bc13a9517168617617186457e401f

time

string

时间

2024-04-24 11:54:34

totalTokens

integer

token 量

300

usage

object

消耗 token 量

imageCount

integer

图片数量,wanx 等模型

0

imageTokens

integer

图片 token 量,qwen-vl 等模型

0

inputTokens

integer

输入 token 量

100

outputTokens

integer

输出 token 量

200

totalTokens

integer

总 token 量

300

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

ok

requestId

string

请求 id

0bc13a9517168617617186457e401f

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": {
    "choices": [
      {
        "finishReason": "stop",
        "index": 0,
        "message": {
          "content": "### **报告期经营业绩概述**\\n截至2024年3月31日止三个月的未经审核综合业绩显示强劲增长.",
          "role": "assistant",
          "toolCalls": [
            null
          ]
        }
      }
    ],
    "created": 1726285125915,
    "id": 1202,
    "modelId": "qwen-max",
    "requestId": "0bc13a9517168617617186457e401f",
    "time": "2024-04-24 11:54:34",
    "totalTokens": 300,
    "usage": {
      "imageCount": 0,
      "imageTokens": 0,
      "inputTokens": 100,
      "outputTokens": 200,
      "totalTokens": 300
    }
  },
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "0bc13a9517168617617186457e401f",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
