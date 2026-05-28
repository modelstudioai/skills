# AddFilesFromAuthorizedOss - 从已授权OSS Bucket中导入文件

将已授权OSS Bucket中的文件导入阿里云百炼应用数据中。

## 接口说明

-   请确保该 OSS Bucket 与阿里云百炼同属一个阿里云账号（主账号），并已按[从 OSS 导入数据配置说明](https://help.aliyun.com/zh/model-studio/data-import-instructions)完成授权。
    
    -   支持的 Bucket 存储类型不包括归档、冷归档或深度冷归档。支持内容加密的 Bucket。支持公共读写/公共读/私有的 Bucket。
    -   如需使用开启 [Referer 防盗链](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)的 Bucket，须参考[仅允许受信任的网站访问](https://help.aliyun.com/zh/oss/configure-referer-policy-to-prevent-other-websites-from-referring-to-oss-files)将域名`*.console.aliyun.com`添加到白名单 Referer 中。
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:AddFilesFromAuthorizedOss 权限点）并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   本接口不具有幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 5 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/AddFilesFromAuthorizedOss)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/AddFilesFromAuthorizedOss)

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

sfm:AddFilesFromAuthorizedOss

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/datacenter/file/fromoss HTTP/1.1
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

业务空间 ID，将文件导入至该业务空间。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vxxxx

CategoryId

string

是

用于指定文件导入目标类目。即 AddCategory 接口返回的`CategoryId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目名称旁的 ID 图标获取类目 ID。此处允许传入 default，即使用系统创建的“默认类目”。

cate\_cdd11b1b79a74e8bbd675c356a91ee35xxxxxxxx

CategoryType

string

是

类目类型，可选，默认值为 UNSTRUCTURED，取值范围：

-   UNSTRUCTURED：类目，用于构建知识库场景。

**说明** 本接口不支持导入用于智能体应用[会话交互](https://help.aliyun.com/zh/model-studio/user-guide/file-interaction)的 SESSION\_FILE，请使用 **AddFile** 接口从本地上传 SESSION\_FILE。

UNSTRUCTURED

OssRegionId

string

是

OSS Bucket 的地域 ID。获取方式请参见 [OSS 地域和访问域名](https://help.aliyun.com/zh/oss/user-guide/regions-and-endpoints)。

cn-beijing

OssBucketName

string

是

OSS Bucket 名称，详见[存储空间](https://help.aliyun.com/zh/oss/user-guide/oss-bucket-overview)。

bucketNamexxxxx

FileDetails

array<object>

是

导入文件列表。一次最多可上传 10 个文件。

**说明** 一次最多可上传 10 个文件。

object

是

文件对象。

FileName

string

是

导入文件的名称，注意后缀需要带上文件格式类型。

-   支持格式：pdf、docx、doc、txt、md、pptx、ppt、xlsx、xls、html、png、jpg、jpeg、bmp、gif。
-   文件名称长度限制 4-128 个字符。
-   对文件上传要求限制，请参见[知识库配额与限制](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-specifications)。

**说明** 如需新增数据表并上传数据，请使用阿里云百炼控制台，API 不支持。

this\_is\_temp\_xxxx.pdf

OssKey

string

是

导入文件在 OSS Bucket 中的键名（Key），详见[对象命名](https://help.aliyun.com/zh/oss/user-guide/object-naming-conventions)。

root/path/this\_is\_temp\_xxxx.pdf

Tags

array

否

文件关联的标签列表。默认值为空，即文件不关联任何标签。最多传入 10 个标签。

string

否

文件的标签。每个标签最多 12 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等），下划线\_，中划线-。

产品介绍

OverWriteFileByOssKey

boolean

否

是否按照 OssKey 覆盖类目中的相同文件，默认值为 false，即不覆盖。

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

success

Data

object

接口业务数据字段。

AddFileResultList

array<object>

文件导入结果列表。

AddFileResultList

object

FileId

string

文件 ID，请妥善保管该值，它将用于后续与此文件相关的所有 API 操作。

file\_809f469a59ac449586ec692576xxxxx\_102248XXX

OssKey

string

导入文件在 OSS Bucket 中的键名（Key）。

root/path/this\_is\_temp\_xxxx.pdf

Status

string

文件导入状态。状态可能值为：

-   SUCCESS：导入（应用数据）完成。
-   FAILED：导入（应用数据）失败。

**说明** 状态为 SUCCESS 的文件才能用于创建/更新知识库。

SUCCESS

Msg

string

文件导入失败时返回错误信息。

size too large

Message

string

错误信息。

Cant find out category for category\_id param.

RequestId

string

请求 ID。

17204B98-xxxx-4F9A-8464-2446A84821CA

Status

string

接口返回的状态码。

200

Success

string

接口调用是否成功，可能值为：

-   true：成功 。
-   false：失败。

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "success",
  "Data": {
    "AddFileResultList": [
      {
        "FileId": "file_809f469a59ac449586ec692576xxxxx_102248XXX",
        "OssKey": "root/path/this_is_temp_xxxx.pdf",
        "Status": "SUCCESS",
        "Msg": "size too large"
      }
    ]
  },
  "Message": "Cant find out category for category_id param.",
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

暂无变更历史
