# ListIndexFileDetails - 查询知识库下的文件详情

获取指定知识库中的文件，以及它们的详细信息。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListIndexFiles 权限点），然后才能调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
-   本接口具有幂等性。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ListIndexFileDetails)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/ListIndexFileDetails)

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

sfm:ListIndexFileDetails

list

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/list_index_file_detail HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

IndexId

string

否

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

79c0alxxxx

DocumentStatus

string

否

即通过文件导入状态对接口返回的文件列表进行过滤。取值范围：

-   INSERT\_ERROR：文件导入失败。
-   RUNNING：文件导入中。
-   DELETED：文件已删除。
-   FINISH：文件导入成功。

默认值为空，即不使用文件导入状态对结果进行过滤。

FINISH

DocumentName

string

否

即通过文件名称对接口返回的文件详情列表进行过滤。默认值为空，即不使用文件名称对结果进行过滤。

翻译平台运维文档

PageNumber

integer

否

指定要查询的页码。起始值为 1。默认值为 1。

1

PageSize

integer

否

指定分页查询时每页展示的文件数量 ，最大值 10。

10

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

EnableNameLike

string

否

是否开启文件名称的模糊匹配，与`DocumentName`参数配合使用。取值范围：

-   true：根据文件名称对接口返回的文件列表进行模糊匹配。
-   false：默认根据文件名称进行精确匹配。

默认值为 false。

枚举值：

-   true：开启。
-   false：不开启。

false

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

请求 ID。

35A267BF-xxxx-54DB-8394-AA3B0742D833

Code

string

错误状态码。

InvalidParameter

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

Success

boolean

接口调用是否成功，可能值：

-   true：成功。
-   false：失败。

true

Data

object

接口业务数据字段。

Documents

array<object>

返回知识库中的文件列表，按文件导入时间倒序排序（与控制台一致）。

rows

object

文件对象。

Status

string

文件导入状态。可能值为：

-   INSERT\_ERROR：文件导入失败。
-   RUNNING：文件导入中。
-   DELETED：文件已删除。
-   FINISH：文件导入成功。

RUNNING

EnableHeaders

string

Excel 文件表头是否支持拼装。

true

OverlapSize

string

分段重叠长度。

100

Message

string

文件导入错误信息。

check fileUrlKey\[file\_path\] / fileNameKey\[null\] / fileExtensionKey\[file\_extension\] is invalid

Size

integer

文件大小，单位字节 Byte。

996764

SourceId

string

类目 ID。

cate\_21a407a3372c4ba7aedc649709143f0cxxxxxxxx

GmtModified

long

文件导入知识库的时间，采用 Unix timestamp 格式。

1744856423000

DocumentType

string

文件格式类型。可能值为： pdf、docx、doc、txt、md、pptx、ppt、png、jpg、jpeg、bmp、gif、EXCEL。

pdf

ChunkMode

string

自定义切分。

DashSplitter

Code

string

文件导入错误状态码。

110002

separator

string

分句标识符。

" "

Name

string

文件名称。

翻译平台运维文档

ChunkSize

string

分段长度，即文本切片的字符数。

600

Id

string

文件 ID。

doc\_c134aa2073204a5d936d870bf960f56axxxxxxxx

IndexId

string

知识库 ID。

79c0alxxxx

TotalCount

long

返回结果的总条数。

2437

PageNumber

integer

返回指定的页码。

1

PageSize

integer

返回指定的每页条数。

10

Status

string

接口返回的状态码。

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "35A267BF-xxxx-54DB-8394-AA3B0742D833",
  "Code": "InvalidParameter\n",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Data": {
    "Documents": [
      {
        "Status": "RUNNING",
        "EnableHeaders": true,
        "OverlapSize": 100,
        "Message": "check fileUrlKey[file_path] / fileNameKey[null] / fileExtensionKey[file_extension] is invalid",
        "Size": 996764,
        "SourceId": "cate_21a407a3372c4ba7aedc649709143f0cxxxxxxxx\n",
        "GmtModified": 1744856423000,
        "DocumentType": "pdf",
        "ChunkMode": "DashSplitter",
        "Code": 110002,
        "separator": " ",
        "Name": "翻译平台运维文档\n",
        "ChunkSize": 600,
        "Id": "doc_c134aa2073204a5d936d870bf960f56axxxxxxxx\n"
      }
    ],
    "IndexId": "79c0alxxxx",
    "TotalCount": 2437,
    "PageNumber": 1,
    "PageSize": 10
  },
  "Status": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
