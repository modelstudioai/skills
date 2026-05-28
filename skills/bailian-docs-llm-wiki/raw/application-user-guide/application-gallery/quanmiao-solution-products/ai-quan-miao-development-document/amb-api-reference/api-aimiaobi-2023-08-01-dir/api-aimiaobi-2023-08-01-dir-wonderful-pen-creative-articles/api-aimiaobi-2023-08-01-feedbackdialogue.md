# FeedbackDialogue - 反馈对话

反馈模型生成的内容质量。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FeedbackDialogue)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/FeedbackDialogue)

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

aimiaobi:FeedbackDialogue

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

fcb14f25c9ee41ccad33a049de8f941b\_p\_outbound\_public

TaskId

string

否

整个页面的 ID

3f7045e099474ba28ceca1b4eb6d6e21

SessionId

string

是

单轮对话的 ID

75bf82fa-b71b-45d7-ae40-0b00e496cd9e

Rating

string

否

thumbsDown:点踩、thumbsUp:点赞

thumbsDown

RatingTags

array

否

标签

RatingTag

string

否

反馈标签，任意字符，长度小于 20 字

生成内容跟要求不符（跟主题不符）

ModifiedResponse

string

否

修改后的生成结果

test

CustomerResponse

string

否

反馈信息

test

GoodText

string

否

认为好的生成内容

test

## 返回参数

名称

类型

描述

示例值

object

BaseResult

Code

string

状态码

successful

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

3f7045e099474ba28ceca1b4eb6d6e21

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
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
