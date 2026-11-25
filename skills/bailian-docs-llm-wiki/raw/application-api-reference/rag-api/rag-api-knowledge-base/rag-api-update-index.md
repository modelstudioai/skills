# 更新知识库

修改指定知识库的名称、描述、重排序最低分数等基本信息。

<a id="前提"></a>

<a id="h-ragapi-update-index-prereq"></a>

## 前提

已获取 API Key 和业务空间 ID，并完成鉴权配置，详见[API 总览](../rag-api-overview.md)与[鉴权说明](../rag-api-authentication.md)。

<a id="接口"></a>

<a id="h-ragapi-update-index-endpoint"></a>

## 接口

**POST** `/api/v1/indices/rag/index/update`

修改指定知识库的名称、描述、重排序最低分数等基本信息。`DenseSimilarityTopK`、`SparseSimilarityTopK`、`PipelineCommercialType` 等字段为 POP 专有，REST 接口不支持，请勿传入。

> **警告**
>
> 参数名为 `id`，不是 `index_id` 或 `indexId`。请注意与其他接口的命名差异。

<a id="请求体"></a>

<a id="h-ragapi-update-index-req"></a>

## 请求体

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `id` | 是 | string | 知识库 ID。注意参数名为 `id`，不是 `index_id` 或 `indexId` |
| `name` | 否 | string | 知识库名称。长度 1~20 字符，支持 Unicode letter 分类字符（含英文、中文、数字等），可含半角冒号(:)、下划线(\_)、半角句号(.)或短划线(-) |
| `description` | 否 | string | 知识库描述信息 |
| `rerankMinScore` | 否 | number | 重排序最低分数阈值，取值范围 \[0, 1\]。分数低于该值的切片会被过滤 |

<a id="wiki-配置参数"></a>

<a id="h-ragapi-update-index-wiki"></a>

### Wiki 配置参数

通过本接口可开启、关闭 Wiki 或修改 Wiki 配置。开启 Wiki 要求知识库为旗舰版（`enterprise`）且知识场景为基础文档问答（`basic_document_qa`）。功能与计费说明见[Wiki 与本体知识图谱](../../../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)。

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `wikiEnabled` | 否 | boolean | Wiki 开关。不传或传 `null` 表示不改变开关状态；传 `true` 开启，传 `false` 关闭。开启与关闭均为异步 |
| `wikiAutoUpdate` | 条件必填 | boolean | Wiki 自动更新开关。不传或传 `null` 表示不修改；当前仅支持自动更新模式，只能传 `true`；`wikiEnabled` 为 `true` 时必填 |
| `wikiConfig.extraction.synthesisModelId` | 条件必填 | string | Wiki 抽取模型。开启时必传，可选 `qwen3.8-flash`、`qwen3.8-max`、`qwen3.7-plus`；已开启状态下修改时缺省即不修改，带来时不可为空白 |
| `wikiConfig.extraction.extractionGranularity` | 条件必填 | string | 提取粒度。开启时必传，无默认值，可选 `focused`、`standard`、`exhaustive`；已开启状态下修改时缺省即不修改 |
| `wikiConfig.extraction.contentInstructions` | 否 | string | Wiki 内容生成要求。空串表示清空该项，不传表示不修改；不超过 4000 字符 |
| `wikiConfig.extraction.extractionInstructions` | 否 | string | Wiki 提取重点。空串表示清空该项，不传表示不修改；不超过 4000 字符 |

> **说明**
>
> 开启 Wiki 时 `wikiConfig` 必填且必须提供 `extraction` 组。已开启状态下的修改只改带来的键，未带的键保留原值，不会重复开启，配置修改立即生效。以下组合易踩（均已实测）：**关闭后重新开启**须重新提供完整 `wikiConfig.extraction`（关闭不保留原配置），否则报 `WikiConfigInvalid`；**未开启状态下只传 `wikiConfig` 不传 `wikiEnabled`** 返回成功但 Wiki 不开启（静默无效）；**`wikiConfig` 传空对象 `{}`** 报 `BadRequest.EmptyInput`，都不传或全为 `null` 才表示不修改。

<a id="请求示例"></a>

<a id="h-ragapi-update-index-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X POST "$BASE_URL/api/v1/indices/rag/index/update" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "your-kb-id",
    "name": "your-kb-name",
    "description": "your-kb-description",
    "rerankMinScore": 0.01
  }'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

修改 Wiki 配置：

<a id="code-block-2"></a>

```bash
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

关闭 Wiki：

<a id="code-block-3"></a>

```bash
curl -X POST "$BASE_URL/api/v1/indices/rag/index/update" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "your-kb-id",
    "wikiEnabled": false
  }'
```

<a id="响应示例"></a>

<a id="h-ragapi-update-index-resp"></a>

## 响应示例

更新成功返回 200。

<a id="code-block-4"></a>

```json
{
  "code": "Success",
  "status_code": 200,
  "data": {
    "updated_at": 1782191157000,
    "created_at": 1782180218000,
    "id": "your-kb-id"
  },
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "status": "SUCCESS"
}
```

<a id="响应字段"></a>

<a id="h-ragapi-update-index-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 响应码，成功时为 `Success` |
| `status_code` | integer | HTTP 状态码 |
| `request_id` | string | 请求唯一标识，排查问题时请提供此 ID |
| `success` | boolean | 请求是否成功 |
| `message` | string | 提示信息，成功时为 `success` |
| `status` | string | 请求状态：`SUCCESS` 或 `FAILED` |
| `data` | object | 响应数据。子字段 `id`（string，知识库 ID）、`updated_at`（integer，更新时间，毫秒级 Unix 时间戳）、`created_at`（integer，创建时间，毫秒级 Unix 时间戳） |

<a id="错误码"></a>

<a id="h-ragapi-update-index-err"></a>

## 错误码

Wiki 相关错误码如下，通用错误见 [Knowledge API 错误码](../rag-api-errors.md)。

| HTTP 状态码 | 错误码（`code`） | 说明 |
| --- | --- | --- |
| 400 | `Index.WikiEditionNotSupported` | 开启时知识库不是旗舰版；或降配为标准版的同时要求开启 |
| 400 | `Index.WikiSceneNotSupported` | 开启时知识场景不是 `basic_document_qa` |
| 400 | `Index.WikiConfigInvalid` | Wiki 配置键非法，按 `message` 里的字段名定位 |
| 409 | `Index.WikiOperationConflict` | 开启中要求关闭、关闭中要求开启，或降配时 Wiki 正在开启中 |
| 400 | `Index.InvalidParameter` | 开启时 `wikiAutoUpdate` 缺失或不为 `true` |
| 400 | `Index.BadRequest.EmptyInput` | `wikiConfig` 传了空对象 `{}` |

> **警告**
>
> 关闭 Wiki 会删除该知识库已生成的全部 Wiki Page 与本体知识图谱（含人工编辑内容和版本历史），无法恢复；再次开启需重新提供完整配置、对全部文档重新生成并再次计费，Page 使用新的 Page ID 并从 V1 开始。已创建的 Wiki 检索服务实例及其 `agent_id` 保留，重新开启完成后原 `agent_id` 自动恢复可用。详见[关闭 Wiki](../../../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md#h-ragwiki-disable)。
