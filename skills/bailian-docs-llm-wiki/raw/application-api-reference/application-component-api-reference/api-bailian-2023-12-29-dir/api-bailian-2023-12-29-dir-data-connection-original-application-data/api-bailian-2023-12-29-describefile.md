# DescribeFile - 查询文件状态

查询应用数据中文件的基本信息，包括文件名称、类型、状态等。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（`AliyunBailianDataFullAccess`或`AliyunBailianDataReadOnlyAccess`均可，已包括 sfm:DescribeFile 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/DescribeFile)

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

sfm:DescribeFile

none

\*全部资源

`*`

无

无

## 请求语法

```
GET /{WorkspaceId}/datacenter/file/{FileId}/ HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

文件所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

FileId

string

是

文件 ID，即 **AddFile** 接口返回的`FileId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击文件名称旁的 ID 图标获取。

file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Code

string

错误状态码。

Success

Data

object

接口业务数据字段。

CategoryId

string

文件所属类目 ID。

cate\_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx

CreateTime

string

文件实际添加到阿里云百炼中的时间戳，格式: yyyy-MM-dd HH:mm:ss，时区：UTC + 8。

2024-09-09 12:45:43

FileId

string

文件 ID。

file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx

FileName

string

文件名称。

XXX产品介绍.pdf

FileType

string

文件类型，扩展名。可能值为： pdf、docx、doc、txt、md、pptx、ppt、xlsx、xls、html、png、jpg、jpeg、bmp、gif。

pdf

Parser

string

解析该文件使用的解析器类型。可能值为：

-   DASHSCOPE\_DOCMIND：默认文档解析器。

DASHSCOPE\_DOCMIND

SizeInBytes

long

文件大小，单位字节 Byte。

1234

Status

string

用于文档类知识库的文件（类型为 UNSTRUCTURED），状态可能值为：

-   INIT: 待解析。
-   IN\_PARSE\_QUEUE：解析队列排队中。
-   PARSING: 解析中。
-   PARSE\_SUCCESS：解析完成。
    
    **说明** 必须等到状态为 PARSE\_SUCCESS 才能将文档导入知识库。
    
-   PARSE\_FAILED：解析失败。

用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的文件（类型为 SESSION\_FILE），状态可能值为：

-   INIT: 待解析。
-   IN\_PARSE\_QUEUE：解析队列排队中。
-   PARSING: 解析中。
-   PARSE\_SUCCESS：解析完成。
-   PARSE\_FAILED：解析失败。
-   SAFE\_CHECKING: 安全检测中。
-   SAFE\_CHECK\_FAILED: 安全检测失败。
-   INDEX\_BUILDING：索引构建中。
-   INDEX\_BUILD\_SUCCESS：索引构建成功。
-   INDEX\_BUILDING\_FAILED：索引构建失败。
-   INDEX\_DELETED：文件索引已删除。
-   FILE\_IS\_READY：文件准备完毕。
    
    **说明** 必须等到状态为 FILE\_IS\_READY 才能进行问答。
    
-   FILE\_EXPIRED：文件过期。
    
    **说明** 仅用户当前会话有效，用户关闭会话后文件过期（最长有效期为 7 天），不支持长期保存。
    

PARSE\_SUCCESS

Tags

array

文件关联的标签列表，一个文件支持关联多个标签。

Tags

string

文件的标签。

产品介绍

Message

string

错误信息。

Requests throttling triggered.

RequestId

string

请求 ID。

17204B98-xxxx-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

boolean

接口调用是否成功，可能值为：

-   true：成功。
-   false：失败。

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "Success",
  "Data": {
    "CategoryId": "cate_cdd11b1b79a74e8bbd675c356a91ee3xxxxxxxx",
    "CreateTime": "2024-09-09 12:45:43",
    "FileId": "file_9a65732555b54d5ea10796ca5742ba22_xxxxxxxx",
    "FileName": "XXX产品介绍.pdf",
    "FileType": "pdf",
    "Parser": "DASHSCOPE_DOCMIND",
    "SizeInBytes": 1234,
    "Status": "PARSE_SUCCESS",
    "Tags": [
      "产品介绍"
    ],
    "ParseResultDownloadUrl": ""
  },
  "Message": "Requests throttling triggered.",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Status": 200,
  "Success": true
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-01-15

OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/bailian/2023-12-29/DescribeFile?updateTime=2026-01-15#workbench-doc-change-demo)
