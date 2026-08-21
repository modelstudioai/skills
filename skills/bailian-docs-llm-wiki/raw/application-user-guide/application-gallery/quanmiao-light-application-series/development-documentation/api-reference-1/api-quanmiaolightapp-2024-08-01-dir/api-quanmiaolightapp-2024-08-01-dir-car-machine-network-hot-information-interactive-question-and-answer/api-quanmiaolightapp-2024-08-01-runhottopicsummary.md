# RunHotTopicSummary - 播报单热点自定义摘要生成

阿里云百炼轻应用-车机/内容平台新闻热榜互动-播报单热点自定义摘要生成：流式生成自定义风格的热点摘要。

## 接口说明

通过此接口，可以流式生成播报单热点下自定义风格的热点摘要。

欢迎前往[控制台](https://bailian.console.aliyun.com/#/app/app-market/quanmiao/news-broadcast)体验。

通过 SDK 方式调用 API 可参考控制台“API”下的示例。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunHotTopicSummary)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunHotTopicSummary)

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

quanmiaolightapp:RunHotTopicSummary

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runHotTopicSummary HTTP/1.1
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

路径参数，[业务空间 id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxx

hotTopicVersion

string

是

热点播报单版本号

2024-10-16\_8

topicIds

array

是

要进行摘要热点话题 ID 列表

string

是

热点 ID

xxxx

stepForCustomSummaryStyleConfig

object

是

自定义输出风格配置

summaryImageCount

integer

否

摘要图片数量

2

summaryModel

string

否

摘要模型

qwen-max

summaryPrompt

string

否

自定义摘要 Prompt

xxxx

## 返回参数

名称

类型

描述

示例值

object

响应

header

object

消息头

errorCode

string

错误码 code

AccessForbidden

errorMessage

string

错误描述

错误信息

event

string

事件

task-finished

sessionId

string

会话唯一标识

xxxx

taskId

string

任务唯一标识

xxxx

traceId

string

全链路唯一标识

xxxxx

payload

object

消息体

output

object

输出结果

text

string

输出摘要文本

这是测试输出

topicId

string

热点 ID

xxx

usage

object

token 消耗

inputTokens

long

输入 token

100

outputTokens

long

输出 token

100

totalTokens

long

总 token

200

requestId

string

Id of the request

5D0E915E-655D-59A8-894F-93873F73AAE5

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "AccessForbidden",
    "errorMessage": "错误信息",
    "event": "task-finished",
    "sessionId": "xxxx",
    "taskId": "xxxx",
    "traceId": "xxxxx"
  },
  "payload": {
    "output": {
      "text": "这是测试输出",
      "topicId": "xxx"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "5D0E915E-655D-59A8-894F-93873F73AAE5"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
