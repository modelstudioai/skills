# ListIndices - 查询知识库列表

获取指定业务空间下知识库列表。

## 接口说明

-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:ListIndex 权限点），然后才能调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
-   本接口具有幂等性。

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/ListIndices)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/bailian/2023-12-29/ListIndices)

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

sfm:ListIndex

list

\*全部资源

`*`

无

无

## 请求语法

```
GET /{WorkspaceId}/index/list_indices HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

IndexName

string

否

知识库的名称。支持通过名称查找知识库。长度为 1~20 个字符，支持 Unicode 中 letter 分类下的字符（其中包括英文、中文和数字等）。可以包含半角冒号（:）、下划线（\_）、半角句号（.）或者短划线（-）。

默认值为空，即查询指定业务空间下的所有知识库。

idx\_status\_score

PageNumber

string

否

指定要查询的页码。起始值为 1。默认值为 1。

1

PageSize

string

否

指定分页查询时每页展示的知识库数量。最大值不限。 默认值为 10。

10

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oq6xxxx

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

17204B98-xxxx-4F9A-8464-2446A84821CA

Data

object

返回数据。

PageNumber

integer

返回指定的页码。

1

PageSize

integer

返回指定的每页条数。

10

TotalCount

integer

返回结果的总条数。

48

Indices

array<object>

知识库列表。

rows

object

知识库对象。

Id

string

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

lecxr5xxxx

Name

string

知识库名称。

XXXX产品清单

Description

string

知识库描述。

清单中产品主要面向海外客户。

StructureType

string

知识库类型。可能值：

-   UNSTRUCTURED：文档搜索类。

UNSTRUCTURED

ChunkSize

integer

分段预估长度。可能值范围\[1-2048\]。

5

OverlapSize

integer

分段重叠长度。可能值范围\[0-1024\]。

10

Separator

string

分句标识符。如果有多个分句标识符，则用 ｜ 分隔。可能值：

-   \\n：换行
-   ，：中文逗号
-   ,：英文逗号
-   。：中文句号
-   .：英文句号
-   ！:中文叹号
-   !：英文叹号
-   ；：中文分号
-   ;：英文分号
-   ？：中文问号
-   ?：英文问号

\\n

EmbeddingModelName

string

Embedding 模型名称。可能值：

-   text-embedding-v4：text-embedding-v4 模型。
-   text-embedding-v3：text-embedding-v3 模型。
-   text-embedding-v2：text-embedding-v2 模型。

text-embedding-v2

RerankModelName

string

Rank 模型名称。可能值：

-   qwen3-rerank-hybrid：qwen3-rerank(hybrid)排序。
-   qwen3-rerank：qwen3-rerank 排序。
-   gte-rerank-hybrid：gte-rerank(hybrid)排序。
-   gte-rerank：gte-rerank 排序。

gte-rerank-hybrid

RerankMinScore

string

相似度阈值。范围\[0.01-1.00\]。

0.01

SourceType

string

阿里云百炼[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)的数据类型。

对于文档搜索/音视频搜索类知识库，可能值：

-   DATA\_CENTER\_CATEGORY：类目类型。
-   DATA\_CENTER\_FILE：文件类型。

对于数据查询/图片问答类知识库，可能值：

-   DATA\_CENTER\_STRUCTURED\_TABLE：数据表类型。

DATA\_CENTER\_FILE

DocumentIds

array

文件 ID 列表。

docIds

string

文件 ID。

file\_8c67b438043848199ffaa903d29addd4\_xxxxxxxx

SinkType

string

知识库的向量存储类型。可能值：

-   ES：内置的向量数据库。
-   BUILT\_IN：内置的向量数据库。
-   ADB：AnalyticDB for PostgreSQL 数据库。

BUILT\_IN

SinkInstanceId

string

知识库的向量存储的实例 ID。

gp-bp1gq62t1788yxxxx

SinkRegion

string

知识库的向量存储的实例地域。

cn-hangzhou

ConfgModel

string

此知识库采用的配置模式。可能值：

-   recommend：推荐配置。
-   user-defined：自定义。

recommend

EnableRewrite

boolean

此知识库是否开启了[多轮对话改写](https://help.aliyun.com/model-studio/use-cases/rag-optimization#b7031e2ad6cji)。可能值：

-   true：已开启。
-   false：未开启。

false

Code

string

错误状态码。

Index.InvalidParameter

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

Status

string

接口返回的状态码。

200

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA",
  "Data": {
    "PageNumber": 1,
    "PageSize": 10,
    "TotalCount": 48,
    "Indices": [
      {
        "Id": "lecxr5xxxx",
        "Name": "XXXX产品清单",
        "Description": "清单中产品主要面向海外客户。",
        "StructureType": "UNSTRUCTURED",
        "ChunkSize": 5,
        "OverlapSize": 10,
        "Separator": "\\n",
        "EmbeddingModelName": "text-embedding-v2",
        "RerankModelName": "gte-rerank-hybrid",
        "RerankMinScore": 0.01,
        "SourceType": "DATA_CENTER_FILE",
        "DocumentIds": [
          "file_8c67b438043848199ffaa903d29addd4_xxxxxxxx"
        ],
        "SinkType": "BUILT_IN",
        "SinkInstanceId": "gp-bp1gq62t1788yxxxx",
        "SinkRegion": "cn-hangzhou",
        "ConfgModel": "recommend",
        "EnableRewrite": false
      }
    ]
  },
  "Code": "Index.InvalidParameter",
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Success": true,
  "Status": 200
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/bailian/2023-12-29/errorCode>)查看更多错误码。
