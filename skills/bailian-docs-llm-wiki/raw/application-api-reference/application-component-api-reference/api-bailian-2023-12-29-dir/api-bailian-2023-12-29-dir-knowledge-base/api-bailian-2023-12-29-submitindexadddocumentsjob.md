# SubmitIndexAddDocumentsJob - 提交知识库追加任务

向指定知识库中追加导入已解析的文件。

## 接口说明

-   本接口不支持数据查询/图片问答类知识库。关于如何更新数据查询/图片问答类知识库，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)一文中关于更新知识库的说明。
    
-   RAM 用户（子账号）需要首先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（需要`AliyunBailianDataFullAccess`，已包括 sfm:SubmitIndexAddDocumentsJob 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，方可调用本接口。阿里云账号（主账号）可直接调用无须授权。建议您通过最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)来调用本接口。
    
-   调用本接口前，请确保您的知识库已经创建完成且未被删除（即知识库 ID`IndexId`有效）。
    
-   调用该接口前，请先调用 **AddFile** 接口将您需要追加导入的文件上传至阿里云百炼。
    
-   调用本接口后，任务需一定时间执行，高峰期可能耗时数小时。任务完成前请勿重复发起请求。如果需要查询任务的执行状态，可调用 **GetIndexJobStatus** 接口查询。此接口返回的文件列表`Documents`为您本次追加（由您提供的`job_id`唯一确定）全部文件，您可以查看每个文件是否导入（解析）成功。注意频繁调用 GetIndexJobStatus 接口会被限流，频率请勿高于 20 次/分钟。
    
-   本接口调用成功后，将执行一段时间，请求返回前请勿重复发起请求。本接口不具备幂等性。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/SubmitIndexAddDocumentsJob)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

sfm:SubmitIndexAddDocumentsJob

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/add_documents_to_index HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

知识库所属的业务空间 ID。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3shx2gu255oqxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

IndexId

string

是

知识库 ID，即 **CreateIndex** 接口返回的`Data.Id`。

79c0alxxxx

SourceType

string

是

数据来源类型。取值范围：

-   DATA\_CENTER\_CATEGORY：类目类型，即导入[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)中指定类目下的所有文档，支持导入多个类目。
    
-   DATA\_CENTER\_FILE：文档类型，即导入[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)下的指定文件，支持导入多个文件。
    

**说明**

如果本参数传入 DATA\_CENTER\_CATEGORY，则必须指定`CategoryIds`参数；如果本参数传入 DATA\_CENTER\_FILE，则必须指定`DocumentIds`参数。

**枚举值：**

-   DATA\_CENTER\_CATEGORY :
    
    类目类型
    
-   DATA\_CENTER\_FILE :
    
    文档类型
    

DATA\_CENTER\_FILE

DocumentIds

array

否

文件 ID 列表。

string

否

文件 ID，即 **AddFile** 接口返回的`FileId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)页面，单击文件名称旁的 ID 图标获取。

doc\_ea4a504d9ce545508d8aa6d90371bf54xxxxxxxx

CategoryIds

array

否

类目 ID 列表。

string

否

类目 ID，即 **AddCategory** 接口返回的`CategoryId`。您也可以在[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)\-文件页签，单击类目旁的 ID 图标获取。

cate\_21a407a3372c4ba7aedc649709143f0cxxxxxxxx

ChunkMode

string

否

启用自定义切分（仅对您本次追加的文件生效）。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。可能取值（不支持同时传入多个值）：

-   **length**：按长度切分。严格按照您指定的`ChunkSize`和`OverlapSize`切分。 若您未传入这两个参数，系统将采用默认值（`ChunkSize`为 500，`OverlapSize`为 100）。按长度切分不支持`Separator`（即使传入也不生效）。
    
-   **page**：按页切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按页切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **h1**：按照一级标题切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按照一级标题切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **h2**：按照二级标题切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按照二级标题切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **regex**：按照正则切分，此时必须指定`Separator`参数。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按正则切分不支持`OverlapSize`（即使传入也不生效）。
    

默认值为空，采用智能切分。

length

Separator

string

否

分句标识符，仅在`chunkMode`\=**regex** 时生效（否则即使传入也不生效）。可传入一个正则表达式（不支持多个），用于将文件分割为小段的文本切片。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

使用智能切分（未指定`chunkMode`）时，保持默认空值即可。

(?<=。)

ChunkSize

integer

否

分段长度，即您希望每个文本切片的字符数上限（仅对您本次追加的文件生效）。超过该长度时：

-   **智能切分**（未指定`chunkMode`）：文本很可能会被截断。
    
-   **自定义切分**（指定了`chunkMode`）：文本将被强制切割。
    

取值范围\[1-6000\]。如果未传入本参数，将使用默认值 500。

更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

**说明**

请注意，如果您指定了`ChunkSize`参数且小于 100，则必须指定`OverlapSize`参数。您也可以不指定这 2 个参数（系统将采用默认值）。

128

OverlapSize

integer

否

分段重叠长度（仅对您本次追加的文件生效）。它表示当前文本切片与上一个文本切片的重叠字符数。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。取值范围\[0-1024\]。

如果未传入本参数，将使用默认值 100。

**说明**

请注意，`OverlapSize`的值必须小于`ChunkSize`的值，否则会导致切分异常。

16

EnableHeaders

boolean

否

Excel 文件表头是否支持拼装。开启后，知识库会将所有 xlsx、xls 格式文件的首行数据视为表头，并自动拼接到每个文本切片中（数据行），避免大模型误将表头视为普通数据行来处理。

**说明**

建议仅在导入文件均为 xlsx、xls 格式且含表头时开启，否则无需开启。

取值范围：

-   true：开启。
    
-   false：不开启。
    

默认值为 false，即不开启。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

false

Extra

object

否

uniqueId

string

否

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

RequestId

string

请求 ID。

778C0B3B-xxxx-5FC1-A947-36EDD13606AB

Data

object

接口返回的业务字段。

Id

string

任务 ID，又称`JobId`。

42687eb254a34802bed398357f5498ae

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

Message

string

错误信息。

Required parameter(%s) missing or invalid, please check the request parameters.

Code

string

错误状态码。

Index.InvalidParameter

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "778C0B3B-xxxx-5FC1-A947-36EDD13606AB",
  "Data": {
    "Id": "42687eb254a34802bed398357f5498ae"
  },
  "Status": "200",
  "Success": true,
  "Message": "Required parameter(%s) missing or invalid, please check the request parameters.",
  "Code": "Index.InvalidParameter"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

400

IdempotentParameterMismatch

The request uses the same client token as a previous, but non-identical request. Do not reuse a client token with different requests, unless the requests are identical.

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/SubmitIndexAddDocumentsJob#workbench-doc-change-demo)。
