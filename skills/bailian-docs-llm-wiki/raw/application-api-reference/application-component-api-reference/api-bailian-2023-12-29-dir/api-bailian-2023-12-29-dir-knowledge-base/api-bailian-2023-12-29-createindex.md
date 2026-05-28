# CreateIndex - 创建知识库

使用此API可创建两类知识库：基于文档或音视频的非结构化知识库，以及用于数据查询或图片问答的结构化知识库。

## 接口说明

-   **权限要求**：
    -   **RAM 用户（子账号）**：需先获取阿里云百炼的 [API 权限](https://help.aliyun.com/zh/model-studio/grant-data-access-permission-to-ram-user)（可使用`AliyunBailianDataFullAccess`策略，该策略已包含本接口所需的 sfm:CreateIndex 权限点），并[加入一个业务空间](https://help.aliyun.com/zh/model-studio/grant-the-business-space-permission-to-ram-users)后，才能调用本接口。
        
    -   **阿里云账号（主账号）**：默认拥有权限，可直接调用。
        
-   **调用方式**：推荐使用最新版[阿里云百炼 SDK](https://api.aliyun.com/api-tools/sdk/bailian?version=2023-12-29)调用，SDK 已封装复杂的签名计算逻辑，可简化您的调用过程。
    
-   **后续操作**：本接口仅初始化知识库创建作业。完成调用后，必须调用 **SubmitIndexJob** 接口以完成创建（否则，您将得到一个空的知识库）。相应代码示例请参见[知识库 API 指南](https://help.aliyun.com/zh/model-studio/rag-knowledge-base-api-guide)。
    
-   **幂等性**：本接口不具有幂等性，重复调用可能会创建多个同名知识库。建议通过“先查询、后创建”的逻辑实现幂等调用。
    

**限流说明：** 本接口频繁调用会被限流，频率请勿超过 10 次/秒。如遇限流，请稍后重试。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/bailian/2023-12-29/CreateIndex)

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

sfm:CreateIndex

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{WorkspaceId}/index/create HTTP/1.1
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

业务空间 ID，即在该业务空间中创建知识库。获取方式请参见[如何使用业务空间](https://help.aliyun.com/zh/model-studio/use-workspace)。

llm-3z7uw7fwz0vexxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

Name

string

是

知识库名称。长度为 1~20 个字符，支持中文、英文、数字、下划线（\_）、短划线（-）、半角句号（.）和半角冒号（:）。

企业帮助文档库

StructureType

string

是

知识库类型。

**取值范围**：

-   unstructured：文档搜索或音视频类知识库。文档搜索类型的使用场景默认为基础文档问答。如需创建其他场景还需传递 knowledgeType 和 knowledgeScene 参数。
    
-   structured：数据查询或图片问答类知识库。
    

**说明**

请注意，知识库创建后将无法更改其类型。

**枚举值：**

-   unstructured :
    
    unstructured
    

unstructured

EmbeddingModelName

string

否

知识库使用的向量模型。向量模型用于将原始输入 prompt 和知识文本转换为数值化向量，以便对二者进行相似度比较。text-embedding-v4 模型在语种支持、代码片段向量化效果和向量维度选择等方面，相比 text-embedding-v3 模型进行了全面升级，适用于大部分场景。更多信息，请参见[向量化](https://help.aliyun.com/zh/model-studio/embedding)。取值范围：

-   text-embedding-v4
    
-   text-embedding-v3
    

默认值为空，此时使用 text-embedding-v3 模型。

-   text-embedding-v2
    

默认值为空，此时使用 text-embedding-v2 模型。

RerankModelName

string

否

知识库使用的排序模型。排序模型是位于知识库外部的评分系统，它会计算用户问题与知识库中每个文本切片的相似度分数并按此降序排列，并返回分数最高的前 K 个文本切片。取值范围：

-   qwen3-rerank-hybrid：qwen3-rerank(hybrid)排序。
    
-   qwen3-rerank：qwen3-rerank 排序。
    
-   gte-rerank-hybrid：gte-rerank(hybrid)排序
    
-   gte-rerank：gte-rerank 排序。
    

默认值为空，此时使用 qwen3-rerank。

**说明**

如仅需语义排序，可使用`qwen3-rerank`；若同时需要语义排序和文本匹配特征以确保相关性，建议使用`qwen3-rerank-hybrid`。

**说明**

`gte-rerank-hybrid`与`gte-rerank`后续停止更新，不建议使用。

**枚举值：**

-   gte-rerank-hybrid :
    
    官方排序
    
-   gte-rerank :
    
    gte-rerank 排序
    

gte-rerank-hybrid

RerankMinScore

number

否

相似度阈值，仅相似度分数超过此数值的文本切片才会被召回，用于筛选排序模型返回的文本切片。取值范围\[0.01-1.00\]。

若未指定，默认采用 0.01。

0.20

ChunkSize

integer

否

分段长度，即每个文本切片的字符数上限。超过该长度时：

-   **智能切分**（未指定`chunkMode`）：文本很可能会被截断。
    
-   **自定义切分**（指定了`chunkMode`）：文本将被强制截断。
    

取值范围\[1-6000\]。若未指定，默认采用 500。

**说明**

若设置了`ChunkSize`且小于 100，则必须同时设置`OverlapSize`。您也可以不指定这 2 个参数，系统将使用默认值。

128

OverlapSize

integer

否

分段重叠长度，表示当前文本切片与前一个文本切片的重叠字符数。取值范围\[0-1024\]。

若未指定，默认采用 100。

**说明**

`OverlapSize`必须小于`ChunkSize`，否则将导致切分异常。

16

Separator

string

否

分句标识符，仅在`chunkMode`\=**regex** 时生效（其他模式下即使传入也不生效）。可传入一个正则表达式（不支持多个），用于将文件分割为小段的文本切片。

使用智能切分（未指定`chunkMode`）时，保持默认空值即可。

(?<=。)

SourceType

string

否

**重要** 此参数在最新版 SDK 中已改为必传，否则调用 SubmitIndexJob 接口将报错：Required parameter(data\_sources) missing or invalid。

导入数据来源。取值范围：

-   DATA\_CENTER\_CATEGORY：类目类型，即导入[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)中指定类目下的所有文件，可同时导入多个类目。
    
-   DATA\_CENTER\_FILE：文件类型，即导入[应用数据](https://bailian.console.aliyun.com/?tab=app#/data-center)下的指定文件，可同时导入多个文件。
    

**说明**

如果本参数传入 DATA\_CENTER\_CATEGORY，则必须指定`CategoryIds`参数；如果本参数传入 DATA\_CENTER\_FILE，则必须指定`DocumentIds`参数。

**说明**

要创建空知识库，可使用不含文件的空类目：本参数传入 DATA\_CENTER\_CATEGORY，`CategoryIds`传入空类目 ID。

**枚举值：**

-   DATA\_CENTER\_CATEGORY :
    
    类目类型
    
-   DATA\_CENTER\_FILE :
    
    文件类型
    

DATA\_CENTER\_FILE

DocumentIds

array

否

创建知识库时可同步导入文件。此处可指定需要导入的文件列表（传入文件 ID，建议导入不超过 10000 个。如有剩余文件，后续可调用 **SubmitIndexAddDocumentsJob** 接口继续导入）。

string

否

文件 ID，即 **AddFile** 接口返回的`FileId`，或者在[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)的文件连接器\-文件页签，单击文件名称旁的 ID 图标获取。

file\_9a65732555b54d5ea10796ca5742ba22\_xxxxxxxx

CategoryIds

array

否

创建知识库时可同步导入文件。此处通过指定类目 ID，可导入对应类目下的所有文件（建议导入不超过 10000 个。如有剩余文件，后续可调用 **SubmitIndexAddDocumentsJob** 接口继续导入）。

string

否

类目 ID，即 **AddCategory** 接口返回的`CategoryId`。或者在[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)的文件连接器\-文件页签，单击类目旁的 ID 图标获取。

ca\_hiu2383nfxxxx

TableIds

array

否

在[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)\-表格连接器的表格页签，单击表格名称旁的 ID 图标获取。若列表包含多个 ID 时，只取第一个。

string

否

SinkType

string

是

知识库的向量存储类型。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。取值范围：

-   BUILT\_IN：将向量数据托管在阿里云百炼平台中。
    
-   ADB：AnalyticDB for PostgreSQL 数据库。如需高级功能，如管理、审计和监控数据库，推荐选择 ADB。
    

**说明**

若您尚未在阿里云百炼上使用过 ADB 存储，可前往[创建知识库](https://bailian.console.aliyun.com/#/knowledge-base/create)页面选择向量存储类型为 ADB-PG，并按界面提示完成授权。如果您传入了 ADB，则必须指定`SinkInstanceId`和`SinkRegion`参数。

**枚举值：**

-   BUILT\_IN :
    
    BUILT\_IN
    
-   ADB :
    
    ADB
    

BUILT\_IN

SinkInstanceId

string

否

AnalyticDB for PostgreSQL 实例 ID（仅在`SinkType`指定 ADB 时才需要传入）。请前往[AnalyticDB for PostgreSQL 数据实例列表](https://gpdbnext.console.aliyun.com/gpdb/list)页面获取此 ID。

gp-bp32109xxxx

SinkRegion

string

否

AnalyticDB for PostgreSQL 实例所在地域（仅在`SinkType`指定 ADB 时才需要传入）。您可调用 [DescribeRegions](https://help.aliyun.com/zh/analyticdb-for-postgresql/developer-reference/api-gpdb-2016-05-03-describeregions) 获取地域列表。

cn-hangzhou

Columns

array<object>

否

数据表的结构（列名、类型等）。

object

否

**说明**

该参数暂不开放，请勿传入。

Column

string

否

**说明**

该参数暂不开放，请勿传入。

school

IsRecall

boolean

否

是否参与模型回复。开启后表示本列的检索结果将作为大模型生成回答时的输入信息。取值范围：

-   true：开启。
    
-   false：不开启。
    

true

IsSearch

boolean

否

是否参与知识库检索。开启后表示允许知识库在此列数据中进行搜索。取值范围：

-   true：开启。
    
-   false：不开启。
    

true

Name

string

否

字段名称。必须与应用数据中创建的数据表的表头一致。

学校

Type

string

否

字段类型。必须与应用数据中创建的数据表的表头一致。取值范围：

-   string
    
-   double
    
-   long
    
-   datetime
    
-   image\_url
    

string

Description

string

否

知识库描述。长度为 0~1000 个英文或中文字符。 默认值为空。

企业帮助文档库包括了公司制度、产品清单等重要资料。

metaExtractColumns

array<object>

否

元数据提取配置。元数据是与非结构化数据内容相关的一系列附加属性，这些属性以 key-value 键值对的形式集成到文本切片中。更多信息，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

object

否

Key

string

否

元数据字段，长度为 1~50 个字符，必须为英文或下划线。如果指定本参数，则必须指定`Value`和`Type`参数。

author

Value

string

否

元数据字段的值。

Tim

Type

string

否

元数据字段的取值方法。取值范围：

-   constant：常量。
    
-   variable：变量。
    
-   custom\_prompt：大模型。
    
-   regular：正则。
    
-   keywords：关键词搜索。
    

**枚举值：**

-   constant :
    
    常量抽取
    
-   keywords :
    
    关键词抽取
    
-   custom\_prompt :
    
    大模型
    
-   variable :
    
    变量抽取
    
-   regular :
    
    正则
    

constant

Desc

string

否

元数据字段的中文描述。长度为 0~1000 个字符，支持中文、英文、数字、下划线（\_）、短划线（-）、半角句号（.）和半角冒号（:）。默认值为空。

作者名

EnableLlm

boolean

否

开启后表示该元数据字段和值将和文本切片的内容一同参与大模型的回答生成过程。取值范围：

-   true：开启。
    
-   false：不开启。
    

默认值为 false。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

false

EnableSearch

boolean

否

开启后表示该元数据字段和值将和文本切片的内容一同参与知识库检索。取值范围：

-   true：开启。
    
-   false：不开启。
    

默认值为 false。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

false

enableHeaders

boolean

否

是否将所有 xlsx、xls 格式文件的第一行数据作为表头，并拼接到每个文本切片中，避免大模型误将表头当作普通数据行来处理。

**说明**

建议仅在导入文件均为 .xlsx、.xls 格式且包含表头时启用该功能，否则无需开启。

取值范围：

-   true：开启。
    
-   false：不开启。
    

若未指定，默认不开启。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

false

chunkMode

string

否

启用自定义切分，并指定切分策略。更多说明，请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

可能取值（不支持同时传入多个值）：

-   **length**：按长度切分。严格按照您指定的`ChunkSize`和`OverlapSize`切分。 若您未传入这两个参数，系统将采用默认值（`ChunkSize`为 500，`OverlapSize`为 100）。按长度切分不支持`Separator`（即使传入也不生效）。
    
-   **page**：按页切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按页切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **h1**：按照一级标题切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按照一级标题切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **h2**：按照二级标题切分。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按照二级标题切分不支持`OverlapSize`和`Separator`（即使传入也不生效）。
    
-   **regex**：按照正则切分，此时必须指定`Separator`参数。如果指定了`ChunkSize`，切分时将一并考虑（未传入时，将使用默认值 500）。按正则切分不支持`OverlapSize`（即使传入也不生效）。
    

若未指定，默认采用智能切分。

**枚举值：**

-   regex :
    
    按照正则切分
    
-   length :
    
    按长度切分
    
-   h1 :
    
    按照一级标题切分
    
-   h2 :
    
    按照二级标题切分
    
-   page :
    
    按页切分
    

regex

EnableRewrite

boolean

否

是否开启多轮对话改写。取值范围：

-   true：开启。
    
-   false：不开启。
    

若未指定，默认为开启。

**枚举值：**

-   true :
    
    开启
    
-   false :
    
    不开启
    

true

CreateIndexType

string

否

**说明**

该参数暂不开放，请勿传入。

standard

pipelineCommercialType

string

否

知识库的[规格类型](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。取值范围：

-   standard：标准版
    
-   enterprise：旗舰版
    

standard

pipelineCommercialCu

integer

否

指定知识库的 RCU 数量（仅当 pipelineCommercialType 指定 enterprise 时才需要传入）。取值范围：\[1-200\]。

1

pipelineRetrieveRateLimitStrategy

string

否

知识库依赖链路限流处理策略（仅当 pipelineCommercialType 指定 enterprise 时才需要传入）。 取值： downgrade：降级处理（改为使用轻量级链路检索）。 若未指定，默认 downgrade。

downgrade

datasourceCode

string

否

数据源 Code。创建数据查询类知识库时必填，与 table、database 配合使用。

建议使用新参数 connectId，可在[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)页面的数据连接器卡片上获取。 当前参数仍可兼容使用，但未来将不再维护。

**说明**

-   本接口不支持关联自定义数据库，请使用阿里云百炼控制台创建。
    

260xxx

table

string

否

数据表名称。创建数据查询类知识库时必填。

该数据表必须存在于由 connectId 或 datasourceCode 指定的数据源内。

lance

database

string

否

数据库名称。创建数据查询知识库时必填。

该数据库必须存在于由 datasourceCode 指定的数据源内。

database\_a6eacabe6

knowledgeType

string

否

具体的知识类型，用于进一步指明知识库处理的数据种类。

**重要** 此参数与 knowledgeScene 必须一同提供或一同省略，不可单独设置。如果一同省略，系统将根据 structureType 采用默认配置。

**设置约束**: 此参数的取值必须与您选择的 structureType 匹配，并决定了 knowledgeScene 的可用值。

**取值范围**：

-   document: 文档搜索。需与 structureType: unstructured 配合使用。
    
-   table: 数据查询。需与 structureType: structured 配合使用。
    
-   image: 图片问答。需与 structureType: structured 配合使用。
    
-   multimedia: 音视频搜索。需与 structureType: unstructured 配合使用。
    

document

knowledgeScene

string

否

知识库的具体使用场景。

**重要** 此参数与 knowledgeType 必须一同提供或一同省略，不可单独设置。如果一同省略，系统将根据 structureType 采用默认配置。

**设置约束**: 此参数的取值完全依赖于您所设置的 knowledgeType。

**取值与联动关系**:

-   当 knowledgeType 为 document 时，knowledgeType 可设置为 basic\_document\_qa（基础文档问答）、visual\_document\_qa（图文并茂回复）或 lite\_document\_qa（极速问答）、visual\_perception\_qa（视觉理解）。
    
-   当 knowledgeType 为 table 时，knowledgeType 设置为 basic\_table\_qa（基础表格问答）。
    
-   当 knowledgeType 为 image 时，knowledgeType 设置为 image\_qa（图片问答）。
    
-   当 knowledgeType 为 multimedia 时，knowledgeType 设置为 basic\_multimedia\_qa（音视频搜索问答）。
    

basic\_document\_qa

connectId

string

否

连接器标识符，可在[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)页面的数据连接器卡片上获取。该参数替换了 datasourceCode 参数，后续需统一使用 connectId。 创建数据查询类知识库时还需填写 table 参数。

conn\_mysql\_xxx\_xxx

channelType

string

否

该参数暂不开放，请勿传入。

connector

RerankMode

string

否

指定重排序模型的指令干预模式，以决定其评分偏好。

**可选值：**

-   **qa**:（默认值） 问答模式。模型倾向于为能直接回答查询（Query）的候选项赋予更高分。建议在问答场景使用。
    
-   **similar**: 相似模式。模型倾向于为与查询内容一致性高的候选项赋予更高分。建议在匹配检索场景使用。
    
-   **custom**: 自定义模式。模型的排序行为由 rerank\_instruct 参数中的指令决定。
    

**枚举值：**

-   similar: 相似模式。 :
    
    similar: 相似模式。
    
-   custom: 自定义模式。 :
    
    custom: 自定义模式。
    
-   qa:（默认值） 问答模式。 :
    
    qa:（默认值） 问答模式。
    

qa

RerankInstruct

string

否

提供一个自然语言指令，用于精细化控制重排序模型的行为。

**重要** 此参数仅在 rerank\_mode 设置为 "custom" 时生效。

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

Code

string

错误状态码

Data

object

请求成功时返回的业务数据

Id

string

知识库 ID，又称`IndexId`，创建的知识库唯一标识

**说明**

请妥善保管该值，它将用于后续所有与此知识库相关的 API 操作。

jkurxhxxxx

Message

string

错误信息

RequestId

string

请求 ID

17204B98-xxxx-4F9A--2446A84821CA

Status

string

接口返回的状态码

"200"

Success

boolean

请求是否成功，可能值为：

-   true：成功
    
-   false：失败
    

true

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "",
  "Data": {
    "Id": "jkurxhxxxx"
  },
  "Message": "",
  "RequestId": "17204B98-xxxx-4F9A--2446A84821CA",
  "Status": "\"200\"",
  "Success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/bailian/2023-12-29/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/bailian/2023-12-29/CreateIndex#workbench-doc-change-demo)。
