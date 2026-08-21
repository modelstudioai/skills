# RunTopicSelectionMerge - 选题热点融合

妙策选题策划聚合

## 接口说明

全妙产品支持 iframe 嵌入 具体请参考文档： [客户对接\_全妙公有云 iframe 定制方案](https://help.aliyun.com/zh/model-studio/iframe-embedding-scheme)

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTopicSelectionMerge)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunTopicSelectionMerge)

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

aimiaobi:RunTopicSelectionMerge

create

\*全部资源

`*`

无

无

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

Prompt

string

否

自定义融合 prompt

请从xxxx的角度，分析xxxx事件

Topics

array

是

待融合的选题视角列表

[TopicSelection](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-struct-topicselection)

否

待融合的选题视角

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

BaseLlmResponse

Header

object

响应头

ErrorCode

string

错误码

错误码

ErrorMessage

string

错误信息

错误信息

Event

string

SSE 事件。task-started:开始，task-finished:结束，task-failed:失败

task-started

OriginSessionId

string

父会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

StatusCode

integer

http 响应码

400

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

TraceId

string

全链路 ID

全链路ID

Payload

object

响应体

Output

object

输出

Text

string

文本生成结果

文本生成结果

Topic

[TopicSelection](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-struct-topicselection)

融合后的选题策划对象

Usage

object

token 用量

InputTokens

integer

输入 Token 数量

78

OutputTokens

integer

输出使用的 Token 数量

34

TokenMap

object

token 消耗明细

integer

token 消耗量

44

TotalTokens

integer

本次调用使用的所有 Token 数总和

38

RequestId

string

请求 ID

3f7045e099474ba28ceca1b4eb6d6e21

End

boolean

响应包是否结束

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "OriginSessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TraceId": "全链路ID"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果",
      "Topic": {
        "Point": "选题视角\n\n",
        "Summary": "摘要",
        "Outlines": [
          {
            "Outline": "大纲",
            "Summary": "摘要"
          }
        ]
      }
    },
    "Usage": {
      "InputTokens": 78,
      "OutputTokens": 34,
      "TokenMap": {
        "key": 44
      },
      "TotalTokens": 38
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "End": true
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunTopicSelectionMerge#workbench-doc-change-demo)。
