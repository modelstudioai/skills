# RunScriptContinue - 影视互娱剧本创作-剧本续写

影视互娱乐剧本创作-剧本续写。

## 接口说明

根据用户输入剧本上文描述，即可快速生产下文，扩展编辑人员续写思路。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptContinue)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptContinue)

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

quanmiaolightapp:RunScriptContinue

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runScriptContinue HTTP/1.1
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

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-e9zzbkg0aj2mlXX

scriptTypeKeyword

string

否

剧本类型关键词：用户针对该剧本类型进行定性描述，如历史架空、科幻、爱情、玄幻等描述

悬疑，都市，惊悚

scriptSummary

string

否

剧本梗概：用户针对该剧本进行简短的故事说明

一队全副武装的执法人员和消防员闯入了一间明显已被遗弃多日、门窗紧闭并用胶带封死的公寓，面对着屋内令人作呕的恶臭和门厅里的混乱场面，他们似乎在寻找某种隐藏的真相或危险源，而一封日期为16号的信件成为了揭开谜团的关键线索，随着便衣探员深入探索，一系列封闭的房间暗示着这里曾发生过不为人知的秘密事件。

userProvidedContent

string

是

上文补充描述：用户针对某一段小说内容续写，需要用户提供上文补充

门厅一片狼藉。朝向天井的窗户开着。公寓门突然被撞开了。\\n一名便衣探员、两名穿制服的警察和几位消防员———也身着工作服———进来，四下张望。他们都戴着手套以及盖住口鼻的面罩。在他们身后，门房和他妻子也挤进门厅。他们都捂着鼻子。门房的另一只手里拿着一叠信件和促销广告单。他们身后，跟着一位女邻居。\\n便衣探员（对门房和邻居）：请在外面等候。\\n他向一名警察示意，警察正忙着把好奇的旁观者请出门外。\\n警察（对门房，指着那一叠信件）：最近的一封是哪天的？\\n门房（查对信件）：最近的一封似乎是16号的......等一下......\\n便衣探员想打开左侧的门，却是徒劳。门用胶带封上了。\\n便衣探员（对消防员）：你来试一下好吗？\\n消防员摆弄门的时候，便衣探员进了卧室隔壁的餐厅。他迅速打开窗，转身，想经过对开门进左侧的房间。这两扇门也锁着，门缝被贴上了胶带。他右转进入起居室，也打开了窗户

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
