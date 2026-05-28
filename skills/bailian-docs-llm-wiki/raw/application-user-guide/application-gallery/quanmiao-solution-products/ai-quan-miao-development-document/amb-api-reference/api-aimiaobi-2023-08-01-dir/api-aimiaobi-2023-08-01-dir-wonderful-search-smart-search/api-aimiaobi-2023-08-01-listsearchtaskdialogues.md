# ListSearchTaskDialogues - 查询妙搜搜索生成任务详情列表

查询妙搜搜索生成任务详情列表。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListSearchTaskDialogues)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListSearchTaskDialogues)

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

aimiaobi:ListSearchTaskDialogues

list

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

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

PageSize

integer

否

返回结果数量

10

TaskId

string

否

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxxx

PageNumber

integer

否

当前页码

1

## 返回参数

名称

类型

描述

示例值

object

响应结果

Data

array<object>

业务数据

Data

object

业务数据

SessionId

string

单轮对话唯一标识

xxxx

OriginSessionId

string

原始的 SessionId

xxxx

TaskId

string

任务唯一标识

xxxx

Rating

string

点赞点踩

thumbsUp

Tags

array

标签

Tag

string

标签信息

xx

Text

string

客户反馈意见

xxx

GoodText

string

客户认为好的生成内容

xxx

Prompt

string

输入

xxx

CreateTime

string

创建日期

2024-11-25 13:33:01

DialogueType

integer

生成类型

24

ResponseBodyStr

string

响应结果字符串

{}

ChatConfig

object

配置

GenerateTechnology

string

生成类型

copilotReference

SearchParam

object

SearchSources

array<object>

搜索源

SearchSource

object

搜索源

Code

string

类型

x'x

Name

string

描述

x

DatasetName

string

唯一标识

xx

DialogueType

integer

请求类型

24

GenerateLevel

string

生成级别

concise

EndToEnd

boolean

是否端到端

SearchModels

array

搜索类型

SearchModel

string

搜索类型

TextGenerate

PageNumber

integer

当前页码

1

PageSize

integer

每页记录条数

10

TotalCount

integer

总记录条数

100

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

Code

string

状态码

NoData

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": [
    {
      "SessionId": "xxxx",
      "OriginSessionId": "xxxx",
      "TaskId": "xxxx",
      "Rating": "thumbsUp",
      "Tags": [
        "xx"
      ],
      "Text": "xxx",
      "GoodText": "xxx",
      "Prompt": "xxx",
      "CreateTime": "2024-11-25 13:33:01",
      "DialogueType": 24,
      "ResponseBodyStr": {},
      "ChatConfig": {
        "GenerateTechnology": "copilotReference",
        "SearchParam": {
          "SearchSources": [
            {
              "Code": "x'x",
              "Name": "x",
              "DatasetName": "xx"
            }
          ],
          "EndTime": "",
          "StartTime": "",
          "MultimodalSearchTypes": [
            ""
          ]
        },
        "DialogueType": 24,
        "GenerateLevel": "concise",
        "EndToEnd": true,
        "SearchModels": [
          "TextGenerate"
        ]
      }
    }
  ],
  "PageNumber": 1,
  "PageSize": 10,
  "TotalCount": 100,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
