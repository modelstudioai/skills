# RunStyleFeatureAnalysis - 内容特点分析

内容特点分析。

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunStyleFeatureAnalysis)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunStyleFeatureAnalysis)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

aimiaobi:RunStyleFeatureAnalysis

get

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaobi/runStyleFeatureAnalysis HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-2setzb9x4ewsd

Contents

array

否

自定义内容文本集合

string

否

自定义内容文本

生活是一种律动，须有光有影，有左有右，有晴有雨，趣味就在这变而不猛的曲折里，微微暗些，再明起来，则暗得有趣，而明乃更明。——老舍

MaterialIds

array

否

素材库 ID 集合

integer

否

素材库 ID

1

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

End

boolean

输出是否完成，true 表示完成

Header

object

流式输出 header 头，包含返回通用信息

ErrorCode

string

异常错误码

403

ErrorMessage

string

异常错误信息

Pop sign mismatch, please check.

Event

string

事件类型

result-generated

EventInfo

string

事件描述

模型生成事件

SessionId

string

一次会话 ID

3cd10828-0e42-471c-8f1a-931cde20b035

TaskId

string

一次生成任务 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

TraceId

string

链路 traceid

2150451a17191950923411783e2927

Payload

object

返回结果的 payload,json 结构

Output

object

输出内容对象

Text

string

输出内容

这是测试输出

Usage

object

大模型 token 用量信息

InputTokens

integer

输入 Token 数量

100

OutputTokens

integer

输出 Token 数量

100

TotalTokens

integer

总 oken 数量

200

RequestId

string

请求唯一 ID

d3be9981-ca2d-4e17-bf31-1c0a628e9f99

## 示例

正常返回示例

`JSON`格式

```
{
  "End": true,
  "Header": {
    "ErrorCode": "403",
    "ErrorMessage": "Pop sign mismatch, please check.",
    "Event": "result-generated",
    "EventInfo": "模型生成事件",
    "SessionId": "3cd10828-0e42-471c-8f1a-931cde20b035",
    "TaskId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99",
    "TraceId": "2150451a17191950923411783e2927"
  },
  "Payload": {
    "Output": {
      "Text": "这是测试输出"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "d3be9981-ca2d-4e17-bf31-1c0a628e9f99"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunStyleFeatureAnalysis#workbench-doc-change-demo)。
