# GetSmartAuditResult - 查询智能审校结果

查询智能审核结果

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult)

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

aimiaobi:GetSmartAuditResult

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

3f7045e099474ba28ceca1b4eb6d6e21

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

xxxxx

Success

boolean

此次请求是否成功

true

Code

string

错误码

DataNotExists

Message

string

错误消息

错误消息

HttpStatusCode

integer

http 错误码

400

Data

object

审核结果

Status

string

任务执行状态，PENDING-待执行、RUNNING-执行中、SUCCESSED-成功、SUSPENDED-暂停、FAILED-失败、CANCELLED-取消

SUCCESSED

ErrorItemDetails

array<object>

审核错误明细列表

errorItemDetails

object

Context

string

原文片段

原文片段

MajorCodeDesc

string

主错误描述

内容准确性

ErrorWord

string

错误单词

”xxx“

MajorCode

string

主错误码

ContentAccuracy

RightWord

string

推荐修改的单词

“xxx”

Reason

string

错误说明

中文双引号应成对正确使用，先左双引号，后右双引号

Url

string

图片审核场景下，返回命中审核的可访问的图片的公网地址

http://www.example.com/xxxx.jpg

Offset

integer

错误单词在全文的偏移索引

0

CheckId

string

审核项唯一标识。

审核项唯一标识。

SubClassCode

string

子错误码

PunctuationError

ErrorLevel

integer

错误等级（1-严重，2-警告，3-提示，4-建议）

2

SubClassDesc

string

子错误描述

标点符号错误

ContextOffset

integer

错误单词在上下文（Context）中的偏移索引。

0

ErrorMessage

string

Status 最终状态 不为 SUCCESSED 时，需要读取此错误信息，判断错误

审核被取消

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "xxxxx",
  "Success": true,
  "Code": "DataNotExists",
  "Message": "错误消息",
  "HttpStatusCode": 400,
  "Data": {
    "Status": "SUCCESSED",
    "ErrorItemDetails": [
      {
        "Context": "原文片段",
        "MajorCodeDesc": "内容准确性",
        "ErrorWord": "”xxx“",
        "MajorCode": "ContentAccuracy",
        "RightWord": "“xxx”",
        "Reason": "中文双引号应成对正确使用，先左双引号，后右双引号",
        "Url": "http://www.example.com/xxxx.jpg",
        "Offset": 0,
        "CheckId": "审核项唯一标识。\n\n",
        "SubClassCode": "PunctuationError",
        "ErrorLevel": 2,
        "SubClassDesc": "标点符号错误\n",
        "ContextOffset": 0
      }
    ],
    "ErrorMessage": "审核被取消"
  }
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
