# GetParseResult - 获取文档解析结果

获取文档解析结果。可查询文档的解析状态以及获取文档的解析结果。

## 接口说明

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetParseResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetParseResult)

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

dianjin:GetParseResult

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/library/document/getParseResult HTTP/1.1
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

路径参数，业务空间 id。

llm-xxxxx

body

object

否

请求 body。

docId

string

是

文档 id

873648346573245

libraryId

string

是

文档库 id

sjdgdsfg

useUrlResult

boolean

否

是否以 URL 形式返回结果。为 true 时，返回的解析结果在 resultUrl 中，result 为空。为 false 时，返回的解析结果在 result 中，resultUrl 为空。

false

## 返回参数

名称

类型

描述

示例值

object

ResultCode

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

fileType

string

文件类型

pdf

providerType

string

供应商类型

null

requestId

string

请求 id

b0a202e2-5031-4589-a6d7-39185f0d8d01

result

object

解析结果

{ "Status": "Success", "Data": {}, "Message": null, "TaskId": "docmind-20240601-123abc" }

status

string

文档解析状态

WaitRefresh

resultUrl

string

以 URL 形式返回的解析结果，可直接下载。注意：仅 pdf、doc、docx、ppt、pptx 类型文件会有解析结果。

https://xxx.oss-cn-beijing.aliyuncs.com/library/3mjeoywx7z/1826661605606129665.json

requestId

string

请求 id

0abb793617204049360065953ec6dd

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
    "fileType": "pdf",
    "providerType": null,
    "requestId": "b0a202e2-5031-4589-a6d7-39185f0d8d01",
    "result": {
      "Status": "Success",
      "Data": {},
      "Message": null,
      "TaskId": "docmind-20240601-123abc"
    },
    "status": "WaitRefresh",
    "resultUrl": "https://xxx.oss-cn-beijing.aliyuncs.com/library/3mjeoywx7z/1826661605606129665.json"
  },
  "requestId": "0abb793617204049360065953ec6dd",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
