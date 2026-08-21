# RunMarketingInformationExtract - 电商零售内容实体抽取

电商零售内容实体抽取。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunMarketingInformationExtract)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunMarketingInformationExtract)

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

quanmiaolightapp:RunMarketingInformationExtract

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runMarketingInformationExtract HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

否

路径参数，[业务空间 id](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

w-08a4a3ba7104917c

modelId

string

否

大模型 ID。

qwen-max qwen-plus

extractType

string

否

抽取类型

point-商品卖点 introduce-商品介绍中的要素 article-营销文案中的要素 comment-对商品看法中的要素 feature-feature

customPrompt

string

否

抽取指令

你是一位商品广告设计师，根据下面的产品介绍，生成一句话来描述该产品的卖点。

sourceMaterials

array

否

要进行抽取的内容

string

否

要抽取的文章内容

ps5是sony新一代的游戏机，他创新性的...

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

end

boolean

是否结束

{'TimeZone': 'Asia/Shanghai', 'DateTime': '2024-03-07T17:00:09+08:00'}

header

object

返回结果的 header

event

string

event 名称

result-generated

eventInfo

string

事件描述

可空

requestId

string

请求 RequestId

F08C71C0-9399-548C-838B-1DA01DE211B0

sessionId

string

sessionId，可用于标记对话

121dlsga4o7golrl1hojazg0u9lvytjc17ebgzzj2u4zukgh122tfg7wj1e6a1vcowy1ewzinauxriai9atcr6r323mm9ddbr0bg5m61ij8hxnf8664tstlfkfol6m8luc4shs3gums7l46uauyy0xndqmhdjtdon6coyhb4x17bo762bg9e3tb2geufg2

taskId

string

任务 ID

12826092918145

traceId

string

日志轨迹 ID

2150432017236011824686132ecdbc

payload

object

返回结果的 payload,json 结构，不同 event 结构不同

output

object

页面展示信息

text

string

抽取内容返回

playstation 5新一代的...

usage

object

token 描述

inputTokens

long

输入 token 数

100

outputTokens

long

输出 token 数

100

totalTokens

long

总 token 数

200

## 示例

正常返回示例

`JSON`格式

```
{
  "end": true,
  "header": {
    "event": "result-generated",
    "eventInfo": "可空",
    "requestId": "F08C71C0-9399-548C-838B-1DA01DE211B0",
    "sessionId": "121dlsga4o7golrl1hojazg0u9lvytjc17ebgzzj2u4zukgh122tfg7wj1e6a1vcowy1ewzinauxriai9atcr6r323mm9ddbr0bg5m61ij8hxnf8664tstlfkfol6m8luc4shs3gums7l46uauyy0xndqmhdjtdon6coyhb4x17bo762bg9e3tb2geufg2",
    "taskId": 12826092918145,
    "traceId": "2150432017236011824686132ecdbc"
  },
  "payload": {
    "output": {
      "text": "playstation 5新一代的..."
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
