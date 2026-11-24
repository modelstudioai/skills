# Wiki API

通过 API 在创建或更新旗舰版知识库时开启并配置 Wiki 与本体知识图谱，查询关联的 Wiki 检索服务，并使用 Wiki 检索。

Wiki API 支持在创建或更新旗舰版知识库时开启并配置 Wiki 与本体知识图谱，查询知识库关联的 Wiki 检索服务，并使用 Wiki 检索服务检索 Wiki 页面。功能的控制台操作与计费说明见[Wiki 与本体知识图谱](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)。

**说明**Wiki 与本体知识图谱仅支持旗舰版知识库（规格为 `enterprise`），且知识场景须为基础文档问答（`basic_document_qa`）。本文接口与 RAG API 使用相同的业务空间 Endpoint 和 API Key 鉴权方式。Wiki 页面管理、历史版本回滚与本体图谱查询接口暂未公开，本文不涉及。

## 前提

-   已获取 API Key 和业务空间 ID，详见[认证](raw/application-api-reference/rag-api/rag-api-authentication.md)。
-   已通过[申请上传租约](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-upload-lease.md)和[注册文件](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md)准备待导入的文件，取得 `docIds`。
-   请求使用 HTTPS 和 UTF-8 编码的 JSON。

示例统一使用以下变量：

```
export BAILIAN_API_KEY="sk-xxxxxxxxxxxxxxxx"
export BASE_URL="https://{workspace_id}.cn-beijing.maas.aliyuncs.com"
```

请将 `{workspace_id}` 替换为实际业务空间 ID，格式为 `llm-xxxxxxxxxxxx`。以下示例中的 `your-kb-id`、`your-file-id` 和 `your-agent-id` 分别表示知识库 ID、文件 ID 和检索服务 ID。

## 创建知识库并开启 Wiki

**POST** `/api/v1/indices/rag/index/create_v2`

在[创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)的请求体中增加以下 Wiki 配置，即可在创建知识库的同时开启 Wiki。接口返回 `pipelineId` 和 `ingestionId`。

字段

必填

类型

说明

`pipelineCommercialType`

是

string

知识库规格。开启 Wiki 必须为 `enterprise`；未指定规格时按标准版处理，无法开启 Wiki

`pipelineCommercialCu`

是

integer

RCU 数量，示例为 `1`

`knowledgeScene`

是

string

知识场景。开启 Wiki 必须为 `basic_document_qa`

`wikiEnabled`

是

boolean

是否在创建知识库的同时开启 Wiki。不传或传 `null` 按不开启处理；开启须设为 `true`

`wikiAutoUpdate`

条件必填

boolean

Wiki 自动更新开关。`wikiEnabled` 为 `true` 时必填；当前仅支持自动更新模式，只能传 `true`。开启后存量文档自动提交生成，新导入文档完成后自动提交

`wikiConfig.extraction.synthesisModelId`

条件必填

string

Wiki 抽取模型。开启 Wiki 时必传且不可为空白，可选 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus`

`wikiConfig.extraction.extractionGranularity`

条件必填

string

提取粒度。开启 Wiki 时必传，无默认值，可选 `focused`（聚焦）、`standard`（标准）、`exhaustive`（详尽）

`wikiConfig.extraction.contentInstructions`

否

string

Wiki 内容生成要求，控制摘要、页面和首页的表达重点。长度按 Unicode 字符计，不超过 4000 字符

`wikiConfig.extraction.extractionInstructions`

否

string

Wiki 提取重点，指定优先识别的领域实体和概念。长度按 Unicode 字符计，不超过 4000 字符

**说明**`wikiEnabled` 为 `true` 时，`wikiConfig` 必填且必须提供 `extraction` 组。Wiki 配置校验不通过时创建请求直接失败，知识库不会创建；校验通过后知识库先创建成功，Wiki 开启随后异步完成，返回成功只代表开启请求已受理。配置校验失败时，`message` 中的字段名为 snake\_case。

**说明**

-   **就绪判断**：Wiki 开启与内容生成均为异步，且暂无状态查询接口。建议先通过[查询关联服务](#h-ragapi-wiki-app-list)确认 `search_type=wiki` 的服务已发布（`agent_status` 为 `deployed`），再发起一次试检索确认就绪。
-   **抽取模型精确匹配**：`synthesisModelId` 区分大小写，仅接受 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus` 三个值，`Qwen3.8-Max` 等大小写变体或 `qwen3-max` 等非白名单值会报 `WikiConfigInvalid`。

```
curl -X POST "$BASE_URL/api/v1/indices/rag/index/create_v2" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-wiki-kb",
    "description": "产品文档 Wiki 知识库",
    "structureType": "unstructured",
    "knowledgeType": "document",
    "knowledgeScene": "basic_document_qa",
    "sinkType": "BUILT_IN",
    "sourceType": "DATA_CENTER_FILE",
    "docIds": ["your-file-id"],
    "embeddingModelName": "qwen3.7-text-embedding",
    "chunkSize": 600,
    "pipelineCommercialType": "enterprise",
    "pipelineCommercialCu": 1,
    "wikiEnabled": true,
    "wikiAutoUpdate": true,
    "wikiConfig": {
      "extraction": {
        "synthesisModelId": "qwen3.8-max",
        "extractionGranularity": "standard",
        "contentInstructions": "",
        "extractionInstructions": ""
      }
    }
  }'
```
```
{
  "code": "Success",
  "status_code": 200,
  "data": {
    "ingestionId": "your-ingestion-id",
    "pipelineId": "your-kb-id",
    "status": "PENDING"
  },
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

## 更新知识库 Wiki 配置

**POST** `/api/v1/indices/rag/index/update`

通过[更新知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)接口开启、关闭 Wiki 或修改 Wiki 配置。请求体以 `id` 指定知识库 ID，Wiki 字段使用 camelCase 命名。

字段

必填

类型

说明

`id`

是

string

知识库 ID。注意参数名为 `id`，不是 `index_id` 或 `indexId`

`wikiEnabled`

否

boolean

Wiki 开关。不传或传 `null` 表示不改变开关状态；传 `true` 开启（要求知识库为 `enterprise` 且知识场景为 `basic_document_qa`），传 `false` 关闭。开启与关闭均为异步

`wikiAutoUpdate`

条件必填

boolean

Wiki 自动更新开关。不传或传 `null` 表示不修改；当前仅支持自动更新模式，只能传 `true`；`wikiEnabled` 为 `true` 时必填

`wikiConfig.extraction.synthesisModelId`

条件必填

string

Wiki 抽取模型。开启时必传，可选 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus`；已开启状态下修改时缺省即不修改，带来时不可为空白

`wikiConfig.extraction.extractionGranularity`

条件必填

string

提取粒度。开启时必传，无默认值，可选 `focused`、`standard`、`exhaustive`；已开启状态下修改时缺省即不修改

`wikiConfig.extraction.contentInstructions`

否

string

Wiki 内容生成要求。空串表示清空该项，不传表示不修改；不超过 4000 字符

`wikiConfig.extraction.extractionInstructions`

否

string

Wiki 提取重点。空串表示清空该项，不传表示不修改；不超过 4000 字符

**说明**开启 Wiki 时 `wikiConfig` 必填且必须提供 `extraction` 组。已开启状态下的修改只改带来的键，未带的键保留原值，不会重复开启，配置修改立即生效。Wiki 键都没带或全为 `null` 时返回成功但配置不变。开启中要求关闭、关闭中要求开启，或降配时 Wiki 正在开启中，会返回 `WikiOperationConflict`。

注意以下几种易踩的组合（均已实测）：

-   **关闭后重新开启**：`wikiEnabled` 置回 `true` 时，必须重新提供完整 `wikiConfig.extraction`（关闭不会保留原配置），否则报 `WikiConfigInvalid`。
-   **未开启状态下只传 `wikiConfig` 不传 `wikiEnabled`**：返回成功但 Wiki 不会开启（静默无效）。
-   **`wikiConfig` 传空对象 `{}`**：报 `BadRequest.EmptyInput`；都不传或全为 `null` 才表示不修改。

```
curl -X POST "$BASE_URL/api/v1/indices/rag/index/update" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "your-kb-id",
    "wikiConfig": {
      "extraction": {
        "synthesisModelId": "qwen3.8-max",
        "extractionGranularity": "standard",
        "contentInstructions": "使用简洁中文，优先展示核心组件和处理流程。"
      }
    }
  }'
```
```
curl -X POST "$BASE_URL/api/v1/indices/rag/index/update" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "your-kb-id",
    "wikiEnabled": false
  }'
```

**警告**关闭 Wiki 会删除该知识库已生成的全部 Wiki Page 与本体知识图谱，包含人工编辑内容和版本历史，删除后无法恢复；再次开启需对全部文档重新生成并再次产生模型 Token 费用。详见[Wiki 与本体知识图谱](https://help.aliyun.com/zh/model-studio/rag-wiki#h-ragwiki-disable)。

重新开启后，Page 使用新的 Page ID 并从 V1 开始（不恢复关闭前的版本历史）；已创建的 Wiki 检索服务实例及其 `agent_id` 会保留，重新开启完成后原 `agent_id` 自动恢复可用（关闭期间调用返回 `WikiNotEnabled`）。

## 查询关联的 Wiki 检索服务

**POST** `/api/v1/indices/rag/app/list`

知识库开启 Wiki 后，系统会自动创建对应的 **Wiki 检索** 服务。通过[查询 Agent 列表](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)接口按知识库 ID 查询关联服务，并用 `search_type` 区分 Chunk 检索与 Wiki 检索，取得 Wiki 检索服务的 `agent_id`。

字段

必填

类型

说明

`agent_scene`

是

string

服务场景，查询知识检索服务时传 `search`

`pipeline_id`

否

string

知识库 ID，用于筛选关联服务

`search_type`

否

string

检索类型，仅在 `agent_scene` 为 `search` 时有意义，可选 `chunk`（向量检索）或 `wiki`（Wiki 检索）；不传即不按类型过滤

`page_number`

否

integer

页码，从 1 开始

`page_size`

否

integer

每页数量

```
curl -X POST "$BASE_URL/api/v1/indices/rag/app/list" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_scene": "search",
    "pipeline_id": "your-kb-id",
    "search_type": "wiki",
    "page_number": 1,
    "page_size": 20
  }'
```
```
{
  "code": "Success",
  "status_code": 200,
  "data": {
    "page_number": 1,
    "total_count": 1,
    "rows": [
      {
        "agent_id": "your-agent-id",
        "agent_name": "my-wiki-kb_知识检索",
        "agent_scene": "search",
        "agent_status": "deployed",
        "search_type": "wiki",
        "pipeline_list": [
          {
            "pipeline_id": "your-kb-id",
            "pipeline_name": "my-wiki-kb"
          }
        ]
      }
    ],
    "page_size": 20
  },
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

`search_type` 为 `wiki` 表示 Wiki 检索服务，为 `chunk` 表示 Chunk 检索服务；`agent_status` 为 `deployed` 表示服务已发布。关闭 Wiki 不会删除已创建的 Wiki 检索服务。

## 使用 Wiki 检索

**POST** `/api/v1/indices/knowledge/search`

使用 Wiki 检索服务的 `agent_id` 调用[知识检索](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)接口，可检索 Wiki 页面。Wiki 检索要求服务绑定的知识库均已开启 Wiki。`agent_id` 是已发布知识检索服务的唯一标识，只是接口沿用字段名；调用知识检索服务不需要创建 Agent 应用。检索类型在服务创建时确定，调用时不可切换。

**警告**`agent_id` 是**知识检索服务 ID**，从[查询关联服务](#h-ragapi-wiki-app-list)（`search_type=wiki`）返回的 `agent_id` 获取，**不是**知识库 ID（`pipelineId`）。误传知识库 ID 会报 `RagAgentGroupNotExist`（`Agent application not found.`）。

字段

必填

类型

说明

`query`

是

string

检索意图。Wiki 检索缺失或为空串时返回 `InvalidParameter`

`agent_id`

是

string

Wiki 检索服务 ID。Wiki 检索必填

`agent_version`

否

string

服务版本，不传时使用已发布版本

`kb_search_configs`

否

`array<object>`

各知识库的检索配置，`search_filters` 在此传入。Wiki 检索仅支持 `page_type`、`folder_id`、`category_path` 过滤字段

Wiki 检索不支持 `file_id_list`，也不支持向量检索的 `doc_id`、`tags` 与自定义元数据过滤。Wiki 过滤字段说明：

**说明**Wiki 检索中，`file_id_list` 传空数组 `[]` 等同不传（不增加范围限制），仅传入非空值时报错。过滤字段的**值**非法（如 `page_type` 拼写错误）不会报错，而是返回空结果，请以返回的 `page_type` 等枚举值为准。

过滤字段

说明

`page_type`

页面类型，字符串或字符串数组，支持 `SUMMARY`、`ENTITY`、`CONCEPT`、`INDEX`、`SYNTHESIS`、`COMPARISON`，大小写不敏感

`folder_id`

目录 ID，字符串，空串表示根目录

`category_path`

从根目录到当前目录的名称路径

```
curl -X POST "$BASE_URL/api/v1/indices/knowledge/search" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "检索服务的处理流程是什么？",
    "agent_id": "your-agent-id",
    "kb_search_configs": [
      {
        "id": "your-kb-id",
        "search_filters": [
          {"page_type": ["ENTITY", "CONCEPT"]}
        ]
      }
    ]
  }'
```
```
{
  "code": "Success",
  "status_code": 200,
  "data": {
    "total": 1,
    "nodes": [
      {
        "score": 0.9555,
        "metadata": {
          "pipeline_id": "your-kb-id",
          "wiki_page_id": "your-page-id",
          "slug": "entity/jiansuo-fuwu",
          "aliases": [],
          "title": "检索服务",
          "summary": "检索服务是知识库的核心组件，负责处理用户查询。",
          "page_type": "ENTITY",
          "folder_id": "your-folder-id",
          "category_path": ["产品知识库", "核心组件"],
          "wiki_path": "entity/产品知识库/核心组件/检索服务",
          "depth": 2,
          "sort_order": 0,
          "source_doc_ids": ["your-file-id"],
          "version": 1,
          "source_type": "WIKI_PAGE",
          "_score_with_weight": 0.9555,
          "_knowledge_type": "document",
          "_knowledge_scene": "basic_document_qa"
        },
        "text": "检索服务\n检索服务是知识库的核心组件，负责处理用户查询。"
      }
    ],
    "cost_time": 363
  },
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

`metadata.source_type` 为 `WIKI_PAGE` 时，表示命中的是 Wiki 页面，未赋值的元数据字段可能省略。返回文本可能是 Page 摘要或检索片段，不保证是完整正文；关键内容请核对来源文档（`source_doc_ids`）。

## 错误码

Wiki 相关错误码如下，通用鉴权与参数错误遵循 [RAG API 通用响应格式](https://help.aliyun.com/zh/model-studio/rag-api-overview#h-ragapi-overview-response)。

**说明**实际响应中 `code` 可能带服务名前缀，如 `Index.WikiConfigInvalid`、`Index.InvalidParameter`，与下表的错误码一一对应。Wiki 配置的请求字段一律使用 camelCase（如 `wikiAutoUpdate`、`synthesisModelId`），但校验失败时 `message` 中的字段名为 snake\_case（如 `wiki_auto_update`、`synthesis_model_id`），需注意映射。

code

status\_code

触发场景

`WikiNotEnabled`

400

Wiki 检索时服务绑定的知识库未全部开启 Wiki

`WikiPreconditionNotMet`

400

知识库不存在、不属于当前账号、已被删除，或知识库服务尚未就绪

`WikiEditionNotSupported`

400

开启 Wiki 时知识库不是旗舰版；或降配为标准版的同时要求开启

`WikiSceneNotSupported`

400

开启 Wiki 时知识场景不是 `basic_document_qa`

`WikiOperationConflict`

409

开启中要求关闭、关闭中要求开启，或有其他 Wiki 操作进行中

`WikiConfigInvalid`

400

Wiki 配置键非法，如缺少 `extraction` 组、`synthesisModelId` 缺失或不在候选清单、`extractionGranularity` 取值非法、指令超长，按 `message` 里的字段名定位

`InvalidParameter`

400

开启时 `wikiAutoUpdate` 缺失或不为 `true`；Wiki 检索 `query` 缺失、传入非空 `file_id_list`、使用不支持的过滤字段；Agent 列表 `search_type` 取值非法

`PipelineNotExist`

400

知识库不存在或不在当前业务空间

删除知识库后继续调用原问答服务时，流式响应中的检索工具可能返回 `PipelineNotExist`，表示原知识库已不存在。删除知识库后，请检查其关联的知识检索和知识问答服务，并按需解绑或删除不再使用的服务与 API Key。

## 调用注意事项

-   请从对应服务的**发布渠道 → API 调试**获取当前环境的请求地址、服务 ID 和最新请求示例，不要复用其他环境的域名或服务 ID。
-   知识问答采用流式响应时，响应中可能包含工具调用、工具返回和中间消息。调用方需按事件及消息类型解析，不能简单拼接全部内容作为最终答案。当前知识问答链路会同时使用普通知识检索和 Wiki 检索，不应假设答案只来自 Wiki Page。
-   外层 HTTP 200 不代表内部检索一定成功。请同时检查流式事件中的工具状态、错误码和最终答案。
-   API Key 仅在创建时展示明文，请妥善保管；测试完成后及时删除不再使用的 Key。
-   Wiki Page 和问答回答均包含模型生成内容。用于合同、财务、医疗、合规等高风险业务时，应结合来源文档进行人工复核，不要将生成结果作为唯一决策依据。

## 相关文档

-   [Wiki 与本体知识图谱](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)
-   [创建知识库并导入](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md)
-   [更新知识库](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-update-index.md)
-   [查询 Agent 列表](raw/application-api-reference/rag-api/rag-api-agents/rag-api-agent-list.md)
-   [知识检索](raw/application-api-reference/rag-api/knowledge/knowledgesearch.md)
