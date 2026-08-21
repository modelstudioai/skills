# RunPptOutlineGeneration - 生成PPT大纲内容

生成PPT大纲内容

## 接口说明

接入说明：

-   当前接口为 HTTP-SSE 协议。
    
-   由于 OpenAPI 门户目前对 SSE 推理协议不兼容（无法直接调试），接口 SDK 方式调用示例（支持 Java、Python 版本的 sdk）请参考 [PPT 生成最佳实践文档](https://help.aliyun.com/zh/model-studio/ppt-generation-best-practices)。
    
-   其中获取 Java 异步 SDK 的最新版本： [请点击链接获取](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?spm=a2c4g.11186623.0.0.4cd3170d7rccDC&version=2023-08-01&language=java-async-tea&tab=primer-doc)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunPptOutlineGeneration)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunPptOutlineGeneration)

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

aimiaobi:RunPptOutlineGeneration

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /pop/ppt/runPptOutlineGeneration HTTP/1.1
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

llm-8v8a5mfpxffrj1pn

Prompt

string

是

用户问题

帮我生成一个消防安全主题的PPT

ExternalUserId

string

否

abc

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Header

object

响应头

ErrorCode

string

错误码

Success

ErrorMessage

string

错误信息

xxx

Event

string

SSE 事件。task-started:开始，task-finished:结束，task-failed:失败

task-started

SessionId

string

会话 ID。

1a3d7c9f-3a6d-4e49-b176-2d8721a27397

StatusCode

integer

状态码。

200

TaskId

string

任务 ID

8996314ce5514867943c71935e6a45af

TraceId

string

全链路 ID

0bc1ec3a17435601877224179ecc8a

Payload

object

响应体

Output

object

输出

Text

string

输出内容

文本生成结果

RequestId

string

请求唯一标识

F2F366D6-E9FE-1006-BB70-2C650896AAB5

HttpStatusCode

string

http 状态码

200

Code

string

状态码

success

Message

string

信息

successful

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "Success",
    "ErrorMessage": "xxx",
    "Event": "task-started",
    "SessionId": "1a3d7c9f-3a6d-4e49-b176-2d8721a27397",
    "StatusCode": 200,
    "TaskId": "8996314ce5514867943c71935e6a45af",
    "TraceId": "0bc1ec3a17435601877224179ecc8a"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果"
    }
  },
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "HttpStatusCode": "200",
  "Code": "success",
  "Message": "successful",
  "Success": true
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

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunPptOutlineGeneration#workbench-doc-change-demo)。
