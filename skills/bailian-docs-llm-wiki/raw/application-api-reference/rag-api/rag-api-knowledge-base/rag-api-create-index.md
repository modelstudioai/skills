# 创建知识库并导入

一步完成创建知识库和导入文件（合并了 CreateIndex 和 SubmitIndexJob）。创建成功后返回知识库 ID（data.pipelineId）和导入任务 ID（data.ingestionId）。

<a id="前提"></a>

<a id="h-ragapi-create-index-prereq"></a>

## 前提

已获取 API Key 和业务空间 ID，并完成鉴权配置，详见[API 总览](../rag-api-overview.md)与[鉴权说明](../rag-api-authentication.md)。

<a id="接口"></a>

<a id="h-ragapi-create-index-endpoint"></a>

## 接口

**POST** `/api/v1/indices/rag/index/create_v2`

一步完成创建知识库和导入文件（合并了 CreateIndex 和 SubmitIndexJob）。

<a id="请求体"></a>

<a id="h-ragapi-create-index-req"></a>

## 请求体

> **警告**
>
> 文件 ID 参数名为 `docIds`，不是 `file_ids` 或 `fileIds`。但校验失败时错误信息中的参数名为 `file_ids`。

<a id="基本参数"></a>

<a id="h-ragapi-create-index-basic"></a>

### 基本参数

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `name` | 是 | string | 知识库名称，1-20 字符，业务空间内唯一 |
| `description` | 否 | string | 知识库描述，0-500 字符，默认为空 |
| `structureType` | 是 | string | 结构类型：`unstructured`（非结构化）或 `structured`（结构化）。`document`、`image`、`multimedia` 搭配 `unstructured`，`table` 搭配 `structured` |
| `knowledgeType` | 否 | string | 知识库类型：`document`（文档搜索）、`table`（数据查询）、`image`（图片问答）、`multimedia`（音视频搜索）。必须与 `knowledgeScene` 同时提供或同时省略；同时省略时，系统按 `structureType` 采用默认配置。场景约束见下表 |
| `knowledgeScene` | 否 | string | 使用场景，取值取决于 `knowledgeType`，必须与 `knowledgeType` 同时提供或同时省略。注意：`lite_document_qa` 要求 `sinkType=BUILT_IN`；`visual_perception_qa` 和 `image_qa` 要求通过 `multimodalEmbeddingModelName` 指定多模态向量模型。此外 `document` 还接受 `visual_document_qa`（图文并茂回复），但控制台已不再提供该入口 |
| `sinkType` | 是 | string | 向量存储类型。`DEFAULT`、`BUILT_IN` 均表示平台内置向量存储；`ADB` 表示 AnalyticDB for PostgreSQL，需同时传 `sinkInstanceId` 和 `sinkRegion`。`lite_document_qa` 仅支持 `BUILT_IN` |
| `sourceType` | 是 | string | 导入模式。`DATA_CENTER_FILE`：按指定文件导入，必须传 `docIds`；`DATA_CENTER_CATEGORY`：按类目导入，必须传 `categoryIds`；`DATA_CENTER_STRUCTURED_TABLE`：按结构化数据表导入，必须传 `tableIds` 和 `columns`。顶层 `sourceType` 决定参数校验分支，`dataSources` 中的同名字段不能替代它 |
| `embeddingModelName` | 否 | string | 向量嵌入模型名称，如 `text-embedding-v3`、`text-embedding-v4`、`qwen3.7-text-embedding`。基础文档问答未传时默认为 `text-embedding-v3` |
| `multimodalEmbeddingModelName` | 条件必填 | string | 多模态向量模型名称，如 `qwen3-vl-embedding`。`knowledgeScene` 为 `visual_perception_qa` 或 `image_qa` 时必填，缺失或取值非法会返回 `invalid multi embedding model`；音视频搜索场景可选传 |
| `docIds` | 条件必填 | `array<string>` | `sourceType=DATA_CENTER_FILE` 时必填的文件 ID 列表；仅传 `categoryIds` 不能替代。值来自 [addFile](../rag-api-data-import/rag-api-add-file.md) 注册文件后返回的 `fileId`，或通过 [listFile](../rag-api-data-import/rag-api-list-file.md) 查询已有文件获取。建议导入不超过 10000 个。注意参数名为 `docIds`，不是 `file_ids` 或 `fileIds`；但校验失败时错误信息中的参数名为 `file_ids` |
| `categoryIds` | 条件必填 | `array<string>` | `sourceType=DATA_CENTER_CATEGORY` 时必填的类目 ID 列表；仅传 `docIds` 不能替代。通过指定类目 ID，可导入对应类目下的所有文件，建议导入不超过 10000 个。类目 ID 通过 [listCategory](../rag-api-data-import/rag-api-list-category.md) 获取 |
| `dataSources` | 否 | `array<object>` | 数据源配置列表，可不传。子字段 `sourceType`（string，数据源类型）不能替代顶层 `sourceType` 决定导入模式；如填写，建议与顶层 `sourceType` 保持一致 |
| `pipelineCommercialType` | 否 | string | 规格类型：`standard`（标准版，默认）或 `enterprise`（旗舰版） |
| `pipelineCommercialCu` | 条件必填 | integer | RCU 数量，取值范围 1-200。`pipelineCommercialType=enterprise` 时必填，否则返回 `Required parameter(index_commercial_cu) missing or invalid` |
| `pipelineRetrieveRateLimitStrategy` | 否 | string | 知识库依赖链路限流处理策略，仅旗舰版使用。当前支持 `downgrade`（降级为轻量级链路检索），默认为 `downgrade` |

<a id="切片与解析参数"></a>

<a id="h-ragapi-create-index-chunking"></a>

### 切片与解析参数

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `chunkMode` | 否 | string | 切片模式，默认为 `auto`（智能切分）。可选 `length`（按长度）、`page`（按页）、`regex`（按正则）及 `h1`~`h5`（按对应层级标题） |
| `chunkSize` | 否 | integer | 切片大小（字符数），基础文档问答默认为 500，取值范围 1-6000。建议值 300-800。小于 100 时必须同时设置小于该值的 `overlapSize` |
| `overlapSize` | 否 | integer | 相邻切片重叠长度（字符数），默认为 100，取值范围 0-1024，且必须小于 `chunkSize`。控制台报文中的 `chunkOverlap` 与该字段等价，二者均可使用 |
| `separator` | 条件必填 | string | 分句标识符，仅 `chunkMode=regex` 时生效且必填，如 `(?<=。)`；其他模式下无需传入 |
| `enableHeaders` | 否 | boolean | 是否将 xlsx、xls 文件首行作为表头并拼接到每个数据切片中，默认为 `false`。仅建议表格含表头时开启 |
| `metaExtractColumns` | 否 | `array<object>` | 元数据抽取配置，最多 5 个字段。仅在创建知识库时生效，创建后不能通过更新知识库补配。数组元素字段见 [Metadata 抽取配置](#h-ragapi-create-index-metadata) |

<a id="检索与重排参数"></a>

<a id="h-ragapi-create-index-retrieval"></a>

### 检索与重排参数

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `enableRewrite` | 否 | boolean | 是否开启多轮对话改写，基础文档问答默认为 `true` |
| `rerankModelName` | 否 | string | 排序模型。基础文档问答默认为 `qwen3-rerank`。也支持 `qwen3-rerank-hybrid`、`gte-rerank`、`gte-rerank-hybrid`；后两者后续停止更新，不建议使用 |
| `rerankMinScore` | 否 | number | 相似度阈值，基础文档问答默认为 0.01，取值范围 0.01-1.00 |
| `rerankTopN` | 否 | integer | 重排序后的默认返回条数，默认为 5，取值范围 1-20。创建时设置会作为后续 Retrieve 的默认值，Retrieve 请求中的 `RerankTopN` 可覆盖它 |
| `sparseSimilarityTopK` | 否 | integer | 关键词检索 TopK，默认为 100，取值范围 0-100。与 `denseSimilarityTopK` 之和不超过 200 |
| `denseSimilarityTopK` | 否 | integer | 向量检索 TopK，默认为 100，取值范围 0-100。与 `sparseSimilarityTopK` 之和不超过 200；基础文档问答中，两者之和还必须不小于 `rerankTopN`，确保候选数量覆盖返回条数 |
| `rerankMode` | 否 | string | 排序模型的指令干预模式：`qa`（问答，默认）、`similar`（相似匹配）或 `custom`（自定义） |
| `rerankInstruct` | 否 | string | 自定义排序指令，仅 `rerankMode=custom` 时生效 |

<a id="结构化数据与外部存储参数"></a>

<a id="h-ragapi-create-index-structured"></a>

### 结构化数据与外部存储参数

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `tableIds` | 条件必填 | `array<string>` | 数据查询类知识库必填的数据表 ID 列表；包含多个 ID 时仅取第一个。ID 在数据连接的表格列表中获取 |
| `columns` | 条件必填 | `array<object>` | 数据查询类知识库必填的列配置。元素包含 `name`（列名）、`type`（列类型：`string`、`double`、`long`、`datetime`、`image_url`）、`isSearch`（是否参与检索，默认 `true`）、`isRecall`（是否参与模型回复，默认 `true`） |
| `connectId` | 否 | string | 自定义数据库连接器 ID，替代旧字段 `datasourceCode`，与 `table` 配合使用。通过数据中心已有 `tableIds` 导入时无需传入，且不能用 `connectId + table` 替代本接口要求的 `tableIds` |
| `datasourceCode` | 否 | string | 旧版数据源 Code，建议改用 `connectId`。仅使用自定义数据库来源时需要，与 `database`、`table` 配合使用 |
| `database` | 否 | string | 自定义数据库名称，仅使用自定义数据库来源时需要，与 `datasourceCode` 或 `connectId`、`table` 配合使用 |
| `table` | 否 | string | 自定义数据表名称，仅使用自定义数据库来源时需要，与 `datasourceCode` 或 `connectId`、`database` 配合使用 |
| `sinkInstanceId` | 条件必填 | string | AnalyticDB for PostgreSQL 实例 ID，`sinkType=ADB` 时必填，否则返回 `Required parameter(db_instance_id) missing or invalid` |
| `sinkRegion` | 条件必填 | string | AnalyticDB for PostgreSQL 实例地域，`sinkType=ADB` 时必填 |

> **说明**
>
> -   通过数据中心已有数据表创建数据查询知识库时，最小参数组合为 `sourceType=DATA_CENTER_STRUCTURED_TABLE`、`tableIds` 和 `columns`。`connectId`、`datasourceCode`、`database`、`table` 仅用于自定义数据库来源，不是该路径的必填项。
> -   `createIndexType`、`channelType` 暂不开放，请勿传入。
> -   控制台浏览器中的网络请求使用控制台内部网关和专用参数，与公开 API 的鉴权、端点和参数契约不同。请以本页为准，不要直接照抄控制台报文调用公开 API。
> -   本接口不支持通过 `dataSync` 开启控制台的“自动同步知识索引”，额外传入 `dataSync:true` 不生效。类目新增文件后，需调用[提交导入任务](../rag-api-sync-jobs/rag-api-submit-sync-job.md)按类目追加导入；在数据集中同名重新上传可能生成新的文件 ID，不会自动替换知识库中的旧文档；该操作也不会删除知识库中已从数据集移除的文档，删除文件需在数据集和知识库中分别进行。
> -   控制台报文中的 `dataType` 对应 `structureType`，`cornerstoneParam` 为控制台内部字段，均不属于本接口的独立公开参数。

<a id="wiki-配置参数"></a>

<a id="h-ragapi-create-index-wiki"></a>

### Wiki 配置参数

旗舰版知识库（`pipelineCommercialType=enterprise`）且知识场景为基础文档问答（`knowledgeScene=basic_document_qa`）时，可在创建知识库的同时开启 Wiki 与本体知识图谱。功能与计费说明见[Wiki 与本体知识图谱](../../../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)。

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `wikiEnabled` | 是 | boolean | 是否在创建知识库的同时开启 Wiki。不传或传 `null` 按不开启处理；开启须设为 `true` |
| `wikiAutoUpdate` | 条件必填 | boolean | Wiki 自动更新开关。`wikiEnabled` 为 `true` 时必填；当前仅支持自动更新模式，只能传 `true`。开启后存量文档自动提交生成，新导入文档完成后自动提交 |
| `wikiConfig.extraction.synthesisModelId` | 条件必填 | string | Wiki 抽取模型。开启 Wiki 时必传、不可为空白且区分大小写，可选 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus` |
| `wikiConfig.extraction.extractionGranularity` | 条件必填 | string | 提取粒度。开启 Wiki 时必传，无默认值，可选 `focused`（聚焦）、`standard`（标准）、`exhaustive`（详尽） |
| `wikiConfig.extraction.contentInstructions` | 否 | string | Wiki 内容生成要求，控制摘要、页面和首页的表达重点。长度按 Unicode 字符计，不超过 4000 字符 |
| `wikiConfig.extraction.extractionInstructions` | 否 | string | Wiki 提取重点，指定优先识别的领域实体和概念。长度按 Unicode 字符计，不超过 4000 字符 |

> **说明**
>
> `wikiEnabled` 为 `true` 时，`wikiConfig` 必填且必须提供 `extraction` 组。Wiki 配置校验不通过时创建请求直接失败，知识库不会创建；校验通过后知识库先创建成功，Wiki 开启随后异步完成，返回成功只代表开启请求已受理。配置校验失败时，`message` 中的字段名为 snake\_case。开启与生成均为异步且暂无状态查询接口，建议通过[查询 Agent 列表](../rag-api-agents/rag-api-agent-list.md)（`search_type=wiki`）确认服务已发布后再试检索。

<a id="知识库类型与使用场景"></a>

<a id="h-ragapi-create-index-scene"></a>

## 知识库类型与使用场景

`knowledgeType` 和 `knowledgeScene` 对应控制台创建知识库第 1 步的知识库类型和使用场景。两者必须**同时提供或同时省略**，只传一个会报 `knowledgeType and knowledgeScene cannot be empty`；同时省略时，系统按 `structureType` 采用默认配置。

控制台仅在文档搜索类型下提供使用场景选项，其余三种类型的场景由控制台自动填入。API 创建时可同时省略这两个字段，由系统按 `structureType` 采用默认配置；仅在需要指定非默认类型或场景时，才必须成对传入。

| knowledgeType | 控制台名称 | structureType | 可用的 knowledgeScene |
| --- | --- | --- | --- |
| `document` | 文档搜索 | `unstructured` | `basic_document_qa`（基础文档问答）<br>`visual_perception_qa`（视觉理解，富文本文档）<br>`lite_document_qa`（极速问答） |
| `table` | 数据查询 | `structured` | `basic_table_qa`（固定） |
| `image` | 图片问答 | `unstructured` | `image_qa`（固定） |
| `multimedia` | 音视频搜索 | `unstructured` | `basic_multimedia_qa`（固定） |

> **说明**
>
> -   `knowledgeType` 与 `structureType` 不匹配时会报 `knowledgeType and structureType do not match`；`knowledgeScene` 不属于该类型时会报 `knowledgeType and knowledgeScene do not match`。
> -   `lite_document_qa`（极速问答）要求 `sinkType` 为 `BUILT_IN`，使用默认的 `DEFAULT` 会报 `Lite Rag only supports BUILT_IN sink type`。
> -   `visual_perception_qa` 和 `image_qa` 必须通过 `multimodalEmbeddingModelName` 指定多模态向量模型（如 `qwen3-vl-embedding`），否则报 `invalid multi embedding model`。
> -   `document` 类型下还有一个 `visual_document_qa`（图文并茂回复）场景，接口仍接受该取值，但控制台已不再提供该入口，不建议在新建知识库时使用。

图片问答的请求体示例：

<a id="code-block"></a>

```json
{
  "name": "image-kb",
  "description": "图片问答知识库",
  "structureType": "unstructured",
  "knowledgeType": "image",
  "knowledgeScene": "image_qa",
  "sinkType": "BUILT_IN",
  "sourceType": "DATA_CENTER_FILE",
  "multimodalEmbeddingModelName": "qwen3-vl-embedding",
  "docIds": ["your-file-id"],
  "dataSources": [{ "sourceType": "DATA_CENTER_FILE" }]
}
```

<a id="metadata-抽取配置"></a>

<a id="h-ragapi-create-index-metadata"></a>

## Metadata 抽取配置

`metaExtractColumns` 用于在创建知识库、构建索引时为文档生成 Meta 信息。每个数组元素支持以下字段：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `key` | 是 | string | 元数据字段名，长度为 1-50 个字符，仅支持英文和下划线 |
| `desc` | 否 | string | 元数据字段的中文描述，长度为 0-1000 个字符，默认为空。支持中文、英文、数字、下划线（\_）、短划线（-）、半角句号（.）和半角冒号（:） |
| `type` | 是 | string | 取值方法：`constant`（常量）、`variable`（变量）、`custom_prompt`（大模型）、`regular`（正则）或 `keywords`（关键词搜索） |
| `value` | 是 | string | 与 `type` 对应的取值规则，具体要求见下表 |
| `enableSearch` | 否 | boolean | 是否让元数据字段和值随文本切片参与知识库检索，默认为 `false` |
| `enableLlm` | 否 | boolean | 是否将元数据字段和值作为大模型回答的输入，默认为 `false` |

| `type` | `value` 说明 | 示例 |
| --- | --- | --- |
| `constant` | 为知识库中的所有文件设置相同的固定值 | `meta_test` |
| `variable` | 文件变量：`file_name` 表示文件名称，`cat_name` 表示文件所在类目的名称 | `file_name` |
| `custom_prompt` | 实体描述，大模型据此从每个文件中抽取相关信息 | `文档主产品的产品名称，只提取一个完整产品名` |
| `regular` | 用于匹配并提取文档内容的正则表达式 | `星澜 X1` |
| `keywords` | 预设关键词，多个关键词使用英文逗号分隔；仅返回文档中实际匹配的关键词 | `智能手机,续航,防水` |

以下请求体片段与 `name`、`docIds` 等创建参数同级：

<a id="code-block-2"></a>

```json
{
  "metaExtractColumns": [
    {
      "key": "source_file_name",
      "desc": "源文件名",
      "type": "variable",
      "value": "file_name",
      "enableSearch": true,
      "enableLlm": true
    },
    {
      "key": "product_name",
      "desc": "产品名称",
      "type": "custom_prompt",
      "value": "文档主产品的产品名称，只提取一个完整产品名",
      "enableSearch": true,
      "enableLlm": true
    }
  ]
}
```

> **说明**
>
> `enableSearch`、`enableLlm` 与查询时的 `metadata_filter` 作用不同。通过 API 调用应用时，如需按元数据过滤文档，应在 `rag_options` 中同时指定 `pipeline_ids` 和 `metadata_filter`，详见[应用调用参数](../../../_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)。索引构建完成后，可通过[查询文件详情](../rag-api-documents/rag-api-list-file-details.md) API 的 `meta_extract_info` 检查实际抽取结果。

<a id="请求示例"></a>

<a id="h-ragapi-create-index-eg"></a>

## 请求示例

<a id="code-block-3"></a>

```bash
curl -X POST "$BASE_URL/api/v1/indices/rag/index/create_v2" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "your-kb-name",
    "description": "your-kb-description",
    "structureType": "unstructured",
    "sinkType": "DEFAULT",
    "sourceType": "DATA_CENTER_FILE",
    "embeddingModelName": "text-embedding-v4",
    "chunkSize": 600,
    "docIds": ["your-file-id-1", "your-file-id-2"],
    "dataSources": [{"sourceType": "DATA_CENTER_FILE"}]
  }'
```

按类目导入时，顶层 `sourceType` 必须改为 `DATA_CENTER_CATEGORY`，并传入 `categoryIds`。无需传 `docIds`，也可不传 `dataSources`：

<a id="code-block-4"></a>

```bash
curl -X POST "$BASE_URL/api/v1/indices/rag/index/create_v2" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "your-kb-name",
    "description": "your-kb-description",
    "structureType": "unstructured",
    "sinkType": "DEFAULT",
    "sourceType": "DATA_CENTER_CATEGORY",
    "embeddingModelName": "text-embedding-v4",
    "chunkSize": 600,
    "categoryIds": ["your-category-id"]
  }'
```

创建旗舰版时，还需在请求体同级传入以下字段；不传 `pipelineCommercialType` 时默认为 `standard`：

<a id="code-block-5"></a>

```json
{
  "pipelineCommercialType": "enterprise",
  "pipelineCommercialCu": 1
}
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-ragapi-create-index-resp"></a>

## 响应示例

创建成功返回 200。

<a id="code-block-6"></a>

```json
{
  "code": "Success",
  "status_code": 200,
  "success": true,
  "message": "success",
  "data": {
    "pipelineId": "h6a85zj8oc",
    "ingestionId": "7f90991a5ec24ad28c8d309ac37e6dd3",
    "status": "PENDING",
    "created_at": 1783657930436,
    "updated_at": 1783657930436
  },
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "status": "SUCCESS"
}
```

<a id="响应字段"></a>

<a id="h-ragapi-create-index-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 响应码，成功时为 `Success` |
| `status_code` | integer | HTTP 状态码 |
| `success` | boolean | 请求是否成功，成功时为 `true` |
| `message` | string | 响应消息，成功时为 `success` |
| `request_id` | string | 请求唯一标识，排查问题时请提供此 ID |
| `status` | string | 请求状态，成功时为 `SUCCESS` |
| `data` | object | 响应数据。子字段 `pipelineId`（string，知识库 ID，后续接口的知识库标识均使用该值）、`ingestionId`（string，本次导入任务 ID，可通过[查询导入任务状态](../rag-api-sync-jobs/rag-api-get-sync-job-status.md)接口跟踪导入进度）、`status`（string，导入任务状态，创建成功时为 `PENDING`）、`created_at`（integer，知识库创建时间，Unix 毫秒时间戳）、`updated_at`（integer，知识库最近更新时间，Unix 毫秒时间戳） |

<a id="错误码"></a>

<a id="h-ragapi-create-index-err"></a>

## 错误码

| HTTP 状态码 | 错误码（`code`） | 说明 |
| --- | --- | --- |
| 400 | `Index.InvalidParameter` | `description` 超过 500 字符：`Required parameter(description length range[1-500]) missing or invalid, please check the request parameters.` |
| 400 | `Index.InvalidParameter` | `sourceType=DATA_CENTER_FILE` 时未传 `docIds` 或传入空数组；仅传 `categoryIds` 仍会报此错：`Required parameter(file_ids) missing or invalid, please check the request parameters.` |
| 400 | `Index.InvalidParameter` | `sourceType=DATA_CENTER_CATEGORY` 时未传 `categoryIds`；仅传 `docIds` 或将类目参数误写为 `source_ids` 均会报此错：`Required parameter(source_ids) missing or invalid, please check the request parameters.` |
| 400 | `Index.InvalidParameter` | 未传顶层 `sourceType`，即使已传 `dataSources` 也会报此错：`Required parameter(data_sources) missing or invalid, please check the request parameters.` |
| 400 | `Index.FileEmptyError` | `docIds` 中的文件 ID 不存在：`fetch empty file list from data center.` |
| 401 | `InvalidApiKey` | API Key 无效或缺失：`Invalid API-key provided.` |
| 400 | `Index.WikiEditionNotSupported` | 开启 Wiki 时知识库不是旗舰版（未指定规格时按标准版处理） |
| 400 | `Index.WikiSceneNotSupported` | 开启 Wiki 时 `knowledgeScene` 不是 `basic_document_qa` |
| 400 | `Index.WikiConfigInvalid` | Wiki 配置键非法，如缺少 `extraction` 组、`synthesisModelId` 缺失或不在候选清单、`extractionGranularity` 取值非法、指令超长，按 `message` 里的字段名定位 |
| 400 | `Index.InvalidParameter` | 开启 Wiki 时 `wikiAutoUpdate` 缺失或不为 `true` |

> **警告**
>
> 缺少顶层 `sourceType` 导致的 400 可能同时留下同名空知识库。重试前请通过[查询知识库列表](rag-api-list-indices.md)检查并清理，避免积累重复空库。
