# GetGeneratedContent - 获取文档

获取文档：用来查询妙笔中创作的文章历史。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetGeneratedContent)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetGeneratedContent)

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

aimiaobi:GetGeneratedContent

get

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

xxxxx\_p\_efm

Id

long

是

文档唯一标识

1

## 返回参数

名称

类型

描述

示例值

object

响应结果

Code

string

状态码

NoData

Data

object

业务数据

Content

string

正文：富文本

杭州亚运会

ContentDomain

string

内容生成的领域-media:新闻、government:政务

media

ContentText

string

正文：纯文本

杭州亚运会

CreateTime

string

创建日期

2024-01-04 11:46:07

CreateUser

string

创建者

"1"

DeviceId

string

设备 ID

xxx

Id

long

文档唯一标识

86

KeywordList

array

关键词

KeywordList

string

关键词

观点

Keywords

string

关键词（string）

\[\\"教师\\",\\"乡村\\"\]

Prompt

string

最后一次生成的提示词

创作xxx文章

TaskId

string

会话任务唯一标识

3f7045e099474ba28ceca1b4eb6d6e21

Title

string

标题

杭州亚运会

UpdateTime

string

更新日期

2024-01-04 11:46:07

UpdateUser

string

更新者

"1"

Uuid

string

UUID 溯源唯一标识

0961a514-2e26-4aa6-b22b-f592d145fe47

IgnoreContentAuditWords

string

审核忽略的单词对象列表(json 字符串)

"\[{}\]"

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "NoData",
  "Data": {
    "Content": "杭州亚运会",
    "ContentDomain": "media",
    "ContentText": "杭州亚运会",
    "CreateTime": "2024-01-04 11:46:07",
    "CreateUser": 1,
    "DeviceId": "xxx",
    "Id": 86,
    "KeywordList": [
      "观点"
    ],
    "Keywords": "[\\\"教师\\\",\\\"乡村\\\"]",
    "Prompt": "创作xxx文章",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "Title": "杭州亚运会",
    "UpdateTime": "2024-01-04 11:46:07",
    "UpdateUser": 1,
    "Uuid": "0961a514-2e26-4aa6-b22b-f592d145fe47",
    "IgnoreContentAuditWords": [
      {}
    ]
  },
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
