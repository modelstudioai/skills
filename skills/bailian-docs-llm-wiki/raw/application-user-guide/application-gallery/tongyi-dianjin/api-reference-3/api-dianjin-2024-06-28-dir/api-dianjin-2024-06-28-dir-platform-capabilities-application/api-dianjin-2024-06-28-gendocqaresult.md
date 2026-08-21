# GenDocQaResult - 根据文档解析问答QA

根据文档解析问答QA，可在API UpdateQaLibrary进行QA对的更新。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GenDocQaResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GenDocQaResult)

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

dianjin:GenDocQaResult

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/virtualHuman/qa/parse HTTP/1.1
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

业务空间 Id

llm-xxxxx

body

object

否

请求体。

docId

string

是

文档 ID

182364872346

libraryId

string

是

文档库 ID

sjdgdsfg

requestId

string

是

请求 ID。该请求 ID 作为请求的唯一标识，首次请求会进行问答 QA 的解析，后续请求，相同的请求 ID 会查询对应的解析状态和结果。

0FC6636E-380A-5369-AE01-D1C15BB9B254

## 返回参数

名称

类型

描述

示例值

object

QA 对

success

boolean

是否成功

true

dataType

string

数据类型

null

time

string

时间戳

2024-04-24 11:54:34

errCode

string

错误码

0

message

string

错误信息

ok

data

object

响应数据

libraryId

string

文档库 ID

7wxwrjpabj

docId

string

文档 ID

873648346573245

currentStatus

string

当前状态\[INIT(初始化),PROCESSING(处理中),COMPLETED(已结束),FAIL(失败)\]

PROCESSING

parseQaResults

array<object>

问答解析的 QA 结果

parseQaResult

object

question

string

问题

今天的天气怎么样？

answer

string

解答

今天的天气不错，多云转晴。

requestId

string

请求 id

44BD277A-87F9-5310-8D63-3E6645F1DA85

cost

long

耗时

null

## 示例

正常返回示例

`JSON`格式

```
{
  "success": true,
  "dataType": null,
  "time": "2024-04-24 11:54:34",
  "errCode": 0,
  "message": "ok",
  "data": {
    "libraryId": "7wxwrjpabj",
    "docId": 873648346573245,
    "currentStatus": "PROCESSING",
    "parseQaResults": [
      {
        "question": "今天的天气怎么样？",
        "answer": "今天的天气不错，多云转晴。\n"
      }
    ]
  },
  "requestId": "44BD277A-87F9-5310-8D63-3E6645F1DA85",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
