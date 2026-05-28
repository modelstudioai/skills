# GetBiddingDocInfo - 获得标书写作结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetBiddingDocInfo)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetBiddingDocInfo)

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

aimiaobi:GetBiddingDocInfo

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

WorkspaceId

string

否

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

TaskId

string

否

任务 ID

7AA2AE16-D873-5C5F-9708-15396C382EB1

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

F2F366D6-E9FE-1006-BB70-2C650896AAB5

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

此次请求是否成功

true

Data

object

业务数据

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

Step

string

当前所处状态

analysis writing

Status

integer

任务状态

0-waiting、1-running、2-success、3-pause、4-fail

Content

string

标书内容

文章内容

ContentType

string

文件类型。

outline bidding

ContentFormat

string

格式

markdown html

TenderDocUrl

string

招标书地址

http://xxx

TenderFileType

string

招标书文件类型

pdf docx

Code

string

状态码

successful

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true,
  "Data": {
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "Step": "analysis\nwriting",
    "Status": 0,
    "Content": "文章内容",
    "ContentType": "outline\nbidding",
    "ContentFormat": "markdown\nhtml",
    "TenderDocUrl": "http://xxx",
    "TenderFileType": "pdf\ndocx"
  },
  "Code": "successful"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
