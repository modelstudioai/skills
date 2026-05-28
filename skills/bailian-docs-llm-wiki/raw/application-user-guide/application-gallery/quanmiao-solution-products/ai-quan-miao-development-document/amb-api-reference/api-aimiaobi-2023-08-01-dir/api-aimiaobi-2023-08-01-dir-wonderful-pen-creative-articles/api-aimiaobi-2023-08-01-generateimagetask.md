# GenerateImageTask - 生成智能配图任务

根据文字异步生成图片。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GenerateImageTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GenerateImageTask)

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

aimiaobi:GenerateImageTask

create

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

e1be065b-adc3-435e-bd01-1c18c5ed75d3

ParagraphList

array<object>

是

段落内容

ParagraphList

object

是

Content

string

是

段落内容

一直忧伤的猫

Id

long

是

段落 ID

1

TaskId

string

否

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

e1be065b-adc3-435e-bd01-1c18c5ed75d3

TaskStatus

string

否

当前任务状态

-   PENDING：任务排队中
-   RUNNING：任务处理中
-   SUSPENDED：任务挂起
-   SUCCEEDED：任务执行成功
-   FAILED：任务执行失败
-   UNKNOWN：任务不存在或状态未知

SUCCESSED

Style

string

是

风格

枚举值：

-   <portrait>：人像写真。
-   <auto>：默认风格。
-   <3d cartoon>：3D卡通。
-   watercolor：水彩。
-   <photography>：摄影。
-   <flat illustration>：扁平插画。
-   <sketch>：素描。
-   <oil painting>：油画。
-   <chinese painting>：中国画。
-   <anime>：动画。

'<auto>'

Size

string

是

生成图片尺寸

枚举值：

-   1024\*1024：1024\*1024。
-   720\*1280：720\*1280。
-   1280\*720：1280\*720。

1024\*1024

ArticleTaskId

string

是

文章 taskId，如目前没有，可以赋值为 UUID

e1be065b-adc3-435e-bd01-1c18c5ed75d3

## 返回参数

名称

类型

描述

示例值

object

PlainResult

Code

string

状态码

successful

Data

object

业务数据

TaskList

array<object>

段落任务信息，根据输入的段落 ID 进行关联

TaskList

object

段落对象

Content

string

段落内容

一直忧伤的猫

Id

long

段落 ID

1

TaskId

string

任务 ID 任务唯一标识

e1be065b-adc3-435e-bd01-1c18c5ed75d3

TaskStatus

string

当前任务状态 SUCCESSED=任务执行成功 ，FAILED=任务执行失败 ，CANCELED=任务被取消 ，PENDIN=任务排队中 ，SUSPENDE=任务挂起 RUNNIN=任务处理中

SUCCESSED

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

F2F366D6-E9FE-1006-BB70-2C650896AAB5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Data": {
    "TaskList": [
      {
        "Content": "一直忧伤的猫",
        "Id": 1,
        "TaskId": "e1be065b-adc3-435e-bd01-1c18c5ed75d3",
        "TaskStatus": "SUCCESSED"
      }
    ]
  },
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
