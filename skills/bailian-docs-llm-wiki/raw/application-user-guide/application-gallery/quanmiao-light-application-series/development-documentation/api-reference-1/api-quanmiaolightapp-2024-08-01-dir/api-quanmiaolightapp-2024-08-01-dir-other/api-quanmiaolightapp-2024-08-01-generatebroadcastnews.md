# GenerateBroadcastNews - 播报单（热榜）热点推荐

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单热点推荐：理解用户意图，获取对应频道下热点列表。

## 接口说明

理解用户意图，获取对应频道下热点列表，比如“播报体育新闻”。历史接口，建议走“播报单（热榜）问答接口 RunHotTopicChat”，完全覆盖了当前接口的能力。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

通过 SDK 方式调用 API 可参考控制台“API”下的 java、python 示例。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GenerateBroadcastNews)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/GenerateBroadcastNews)

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

quanmiaolightapp:GenerateBroadcastNews

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/GenerateBroadcastNews HTTP/1.1
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

[业务空间唯一标识](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

prompt

string

是

用户意图

帮我播报体育热点

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

code

string

状态码

xx

data

object

分类和新闻热点数据

hotTopicSummaries

array<object>

新闻热点数据列表

hotTopicSummaries

object

新闻热点数据

category

string

热点话题分类

体育

hotTopic

string

热点话题名称

热点

hotTopicVersion

string

热点话题版本

2024-09-13\_08

hotValue

double

热度

1000000

id

string

热点话题 ID

1458tb3bjo7531kap42a

images

array<object>

相关图片列表

images

object

相关图片

url

string

图片 url

http://xxx.com/xxx.jpeg

textSummary

string

热点话题文本摘要

xxx

sessionId

string

对话 ID

2bb0ea82dafd48a8817fadc4c90e2b52

taskId

string

任务 ID

3feb69ed02d9b1a17d0f1a942675d300

text

string

理解结果

体育

usage

object

token 消耗

inputTokens

long

输入 token 数

1

outputTokens

long

输出 Token 数量

2

totalTokens

long

总 token 量

3

httpStatusCode

integer

http 状态码

200

message

string

错误说明

success

requestId

string

请求唯一标识

117F5ABE-CF02-5502-9A3F-E56BC9081A64

success

boolean

是否成功：true 成功，false 失败

True

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "xx",
  "data": {
    "hotTopicSummaries": [
      {
        "category": "体育",
        "hotTopic": "热点",
        "hotTopicVersion": "2024-09-13_08",
        "hotValue": 1000000,
        "id": "1458tb3bjo7531kap42a",
        "images": [
          {
            "url": "http://xxx.com/xxx.jpeg"
          }
        ],
        "textSummary": "xxx"
      }
    ],
    "sessionId": "2bb0ea82dafd48a8817fadc4c90e2b52",
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300",
    "text": "体育",
    "usage": {
      "inputTokens": 1,
      "outputTokens": 2,
      "totalTokens": 3
    }
  },
  "httpStatusCode": 200,
  "message": "success",
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
