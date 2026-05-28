# ApplyFileUploadLease - 申请文件上传租约

请求一个上传租约用于上传知识库文件，或智能体应用会话交互的文件。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ApplyFileUploadLease 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/ApplyFileUploadLease)

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

sfm:ApplyFileUploadLease

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/datacenter/category/{CategoryId} HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

CategoryId

string

是

上传用于构建[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)的文件时：

-   该字段代表上传文件所属类目 ID，即 **AddCategory** 接口返回的`CategoryId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目名称旁的 ID 图标获取。此处允许传入 default，即使用系统创建的“默认类目”。

**说明** 如需新增数据表并上传数据，请使用阿里云百炼控制台，API 不支持。

上传用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的文件时：

-   此处传入 default 即可，系统会自动创建或者匹配默认类目，后续会开放动态文件类目接口及控制台管理页面。

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

FileName

string

是

上传用于构建[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)的文件：

-   该字段代表上传文件的名称，注意后缀需要带上文件格式类型，支持格式：
    -   文档：doc、docx、wps、ppt、pptx、pdf。
    -   表格（建议 10MB 以内，10 万行以内）：xls、xlsx。
    -   纯文本（建议不要超过 10MB）：md、txt。
    -   图片（小于 20MB，最短边 > 15px， 长边 < 8192px，长宽比 < 50）：png、jpg、jpeg、bmp、gif。
    -   音频：aac、amr、flac、flv、m4a、mp3、mpeg、ogg、opus、wav、webm、wma。
    -   视频：mp4、mkv、avi、mov、wmv。
-   文件名称长度限制 4-128 个字符。其它限制请参考[知识库配额与限制](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-specifications)。

**说明** 如需新增数据表并上传数据，请使用阿里云百炼控制台，API 不支持。

上传用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的文件：

-   该字段代表上传文件的名称，注意后缀需要带上文件格式类型。支持格式：
    -   文档：doc、docx、wps、ppt、pptx、xls、xlsx、md、txt、pdf。
    -   图片：png、jpg、jpeg、bmp、gif。
    -   音频：aac、amr、flac、flv、m4a、mp3、mpeg、ogg、opus、wav、webm、wma。
    -   视频：mp4、mkv、avi、mov、wmv。
-   文件名称长度限制 4-128 个字符。

XXXX产品清单.pdf

Md5

string

是

上传文件的 MD5 值，服务端会验证该字段（当前暂未开启），请正确填写。

19657c391f6c70bcea63c154d8606bb3

SizeInBytes

string

是

上传文件的大小，单位字节，服务端会验证该字段（当前暂未开启），请正确填写。取值范围：1B-100M。

1000

WorkspaceId

string

是

上传文件所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

CategoryType

string

否

类目类型，不传入该参数时，默认值为 UNSTRUCTURED。取值范围：

UNSTRUCTURED：类目，用于构建[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)场景。

SESSION\_FILE：上传用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的文件。

**说明** 如需新增数据表并上传数据，请使用阿里云百炼控制台，API 不支持。

UNSTRUCTURED

UseInternalEndpoint

boolean

否

若您使用了[阿里云百炼安全存储空间](https://help.aliyun.com/zh/model-studio/configure-resources-in-private-network)，需要生成仅阿里云同地域内网可访问的租约 URL 链接时，此处可传入 true，以提高安全性。不传入该参数时，默认值为 false，即生成公网可访问的租约 URL。

**说明** 若您未开通阿里云百炼安全存储空间，或不确定是否在使用，此处请勿传入 true（会上传失败）。

false

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

DataCenter.FileTooLarge

Data

object

接口业务数据字段。

FileUploadLeaseId

string

租约唯一 ID，后续调用 **AddFile** 接口时，需要使用该参数。

1e6a159107384782be5e45ac4759b247.1719325231035

Param

object

用于上传文件的 HTTP 请求参数。

Headers

any

需要放到 Header 中的 K-V 字段，K 和 V 均为字符串。

**说明** 返回的 Content-Type 可能为空值，后续按照空值上传即可。

"X-bailian-extra":"MTAwNTQyNjQ5NTE2OTE3OA==", "Content-Type":"application/pdf"

Method

string

HTTP 调用方法，可能值为：

-   PUT
-   POST

PUT

Url

string

文件的上传 URL 地址。

**说明** 该 URL 为预签名 URL，不支持 FormData 方式上传，需使用二进制方式上传。

https://bailian-datahub-data-origin-prod.oss-cn-hangzhou.aliyuncs.com/1005426495169178/10024405/68abd1dea7b6404d8f7d7b9f7fbd332d.1716698936847.pdf?Expires=1716699536&OSSAccessKeyId=TestID&Signature=HfwPUZo4pR6DatSDym0zFKVh9Wg%3D

Type

string

文件的上传方式，可能值为：

-   OSS.PreSignedURL
-   HTTP

HTTP

Message

string

错误信息。

User not authorized to operate on the specified resource

RequestId

string

请求 ID。

778C0B3B-xxxx-5FC1-A947-36EDD13606AB

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
  "Code": "DataCenter.FileTooLarge",
  "Data": {
    "FileUploadLeaseId": "1e6a159107384782be5e45ac4759b247.1719325231035",
    "Param": {
      "Headers": "\"X-bailian-extra\":\"MTAwNTQyNjQ5NTE2OTE3OA==\",\n\"Content-Type\":\"application/pdf\"",
      "Method": "PUT",
      "Url": "https://bailian-datahub-data-origin-prod.oss-cn-hangzhou.aliyuncs.com/1005426495169178/10024405/68abd1dea7b6404d8f7d7b9f7fbd332d.1716698936847.pdf?Expires=1716699536&OSSAccessKeyId=TestID&Signature=HfwPUZo4pR6DatSDym0zFKVh9Wg%3D"
    },
    "Type": "HTTP"
  },
  "Message": "User not authorized to operate on the specified resource",
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
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

暂无变更历史
