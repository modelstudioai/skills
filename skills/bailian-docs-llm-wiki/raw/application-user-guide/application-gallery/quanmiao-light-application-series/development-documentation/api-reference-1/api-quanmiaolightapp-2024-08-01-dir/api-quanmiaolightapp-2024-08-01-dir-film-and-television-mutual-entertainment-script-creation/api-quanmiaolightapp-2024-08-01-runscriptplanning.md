# RunScriptPlanning - 影视互娱剧本创作-剧本策划

影视互娱乐剧本创作-剧本策划。

## 接口说明

根据用户对剧本前要的简单输入，就可得到剧本梗概及分镜头的简要描述，帮助编辑人员快速构思剧本框架

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptPlanning)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptPlanning)

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

quanmiaolightapp:RunScriptPlanning

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runScriptPlanning HTTP/1.1
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

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-e9zzbkg0aj2mlXX

scriptName

string

否

自然语言输入剧本名称

都市战神

scriptTypeKeyword

string

否

剧本类型关键词：用户针对该剧本类型进行定性描述，如历史架空、科幻、爱情、玄幻等描述

现代，都市，爱情，玄幻

scriptSummary

string

是

剧本梗概：用户针对该剧本进行简短的故事说明

在一个宁静的小镇上，每个家庭都在同一天收到一个神秘的、没有标记的包裹。

scriptShotCount

integer

否

剧本的分镜数量：单个剧本内用户可以定义生成对应的镜头描述数量，取值范围为 1~10 个

3

dialogueInScene

boolean

否

是否需要具体分镜对白，default=false

plotConflict

boolean

否

可读性：用户可以勾选是否增加剧情冲突、反转情节的策划内容，勾选后可自动生成在剧情中

additionalNote

string

否

其他补充：用户可以在文本输入框中，通过自然语言的描述进行开放性调整，例如增加紧张刺激时刻的描述等等，帮助用户进行效果调整

故事尽可能狗血

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

end

boolean

输出是否完成，true 表示完成

header

object

流式输出 header 头，包含返回通用信息

errorCode

string

异常错误码

403

errorMessage

string

异常错误信息

Pop sign mismatch, please check.

event

string

事件类型

result-generated

eventInfo

string

事件描述

模型生成事件

requestId

string

请求 ID

0EB27AE3-CA53-5FAE-83C6-EE66CA4DF5DF

sessionId

string

一次会话 ID

3cd10828-0e42-471c-8f1a-931cde20b035

taskId

string

一次生成任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

traceId

string

链路 traceid

2150451a17191950923411783e2927

payload

object

返回结果的 payload,json 结构

output

object

输出内容对象

text

string

输出内容

这是测试输出

usage

object

大模型 token 用量信息

inputTokens

long

输入 Token 数量

100

outputTokens

long

输出 Token 数量

100

totalTokens

long

总 oken 数量

200

## 示例

正常返回示例

`JSON`格式

```
{
  "end": true,
  "header": {
    "errorCode": 403,
    "errorMessage": "Pop sign mismatch, please check.",
    "event": "result-generated",
    "eventInfo": "模型生成事件",
    "requestId": "0EB27AE3-CA53-5FAE-83C6-EE66CA4DF5DF",
    "sessionId": "3cd10828-0e42-471c-8f1a-931cde20b035",
    "taskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "traceId": "2150451a17191950923411783e2927"
  },
  "payload": {
    "output": {
      "text": "这是测试输出"
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

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode>)查看更多错误码。
