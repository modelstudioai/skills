# RunScriptRefine - 影视互娱剧本创作-剧本整理

剧本对话内容的整理。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptRefine)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunScriptRefine)

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

quanmiaolightapp:RunScriptRefine

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runScriptRefine HTTP/1.1
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

llm-zna577pdximvztk5

taskId

string

否

任务唯一标识

**说明**-   taskId 默认无需填写，系统将自动生成。当后续任务填写的 taskId 相同时，表示这些任务属于同一组对话。
-   建议手动赋值 taskId，以便关联上下文。

a3d1c2ac-f086-4a21-9069-f5631542f5a2

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

Pop sign mismatch, please check log.

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

F8A35034-EDCF-5C50-95A5-1044316F36E3

sessionId

string

一次会话 ID

17dc8bcd-f34a-46d1-a7a3-0fa3d1ce3824

taskId

string

一次生成任务 ID

14356391-6c6c-40d5-b80a-8ecd03b69d72

traceId

string

链路 traceid

2150432017236011824686132ecdbc

payload

object

返回结果的 payload，json 结构，不同 event 结构不同

output

object

输出内容对象

text

string

输出内容

xx

role

string

角色身份

用户角色信息

scene

string

故事场面，保留字段

保留字段，暂无赋值

summary

string

故事梗概

在充满机遇与挑战的大都市，平凡女孩林苏怀揣梦想却处处碰壁。一次偶然的机会

outline

string

剧本大纲

在繁华都市的夜晚，林苏因面试失败心情低落时意外撞上了沈逸

content

array<object>

正文

content

object

正文

string

正文，剧幕内容

{"第一幕":" 幕次: 第一幕\\n\\n 场面描述"}

usage

object

大模型 Token 用量信息

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

总 Token 数量

200

## 示例

正常返回示例

`JSON`格式

```
{
  "end": true,
  "header": {
    "errorCode": 403,
    "errorMessage": "Pop sign mismatch, please check log.",
    "event": "result-generated",
    "eventInfo": "模型生成事件",
    "requestId": "F8A35034-EDCF-5C50-95A5-1044316F36E3",
    "sessionId": "17dc8bcd-f34a-46d1-a7a3-0fa3d1ce3824",
    "taskId": "14356391-6c6c-40d5-b80a-8ecd03b69d72",
    "traceId": "2150432017236011824686132ecdbc"
  },
  "payload": {
    "output": {
      "text": "xx",
      "role": "用户角色信息",
      "scene": "保留字段，暂无赋值",
      "summary": "在充满机遇与挑战的大都市，平凡女孩林苏怀揣梦想却处处碰壁。一次偶然的机会",
      "outline": "在繁华都市的夜晚，林苏因面试失败心情低落时意外撞上了沈逸",
      "content": [
        {
          "key": {
            "第一幕": " 幕次: 第一幕\n\n 场面描述"
          }
        }
      ]
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
