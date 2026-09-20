# 更新切片

更新指定切片的内容。

## 前提

已完成 Endpoint 与鉴权配置，详见 [API 总览](raw/application-api-reference/rag-api/rag-api-overview.md)和[认证](raw/application-api-reference/rag-api/rag-api-authentication.md)。

## 接口

**POST** `/api/v1/indices/rag/index/chunk/update`

更新指定切片的内容。

**说明**切片内容长度需在 10-6000 字符之间。

## 请求体

字段

必填

类型

说明

`pipelineId`

是

string

知识库 ID，即 [createIndex](raw/application-api-reference/rag-api/rag-api-knowledge-base/rag-api-create-index.md) 接口返回的 `data.id`

`chunkId`

是

string

待修改的切片 ID，可通过 [listChunks](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md) 接口获取，取返回结果中 `node.metadata._id` 字段

`dataId`

是

string

文件 ID，即 [addFile](raw/application-api-reference/rag-api/rag-api-data-import/rag-api-add-file.md) 接口返回的 `fileId`，也可通过 [listChunks](raw/application-api-reference/rag-api/rag-api-chunks/rag-api-list-chunks.md) 的 `node.metadata.doc_id` 获取

`content`

是

string

切片内容，长度需在 10-6000 字符之间，且不能超过创建知识库时设定的最大分段长度

`title`

否

string

切片标题，长度 0~50 字符。传入空字符串可清空标题；不传此参数则保持原标题不变

`isDisplayedChunkContent`

是

boolean

是否参与知识库检索。`true`：参与检索；`false`：不参与检索

## 请求示例

```
curl -X POST "$BASE_URL/api/v1/indices/rag/index/chunk/update" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "pipelineId": "your_index_id",
    "chunkId": "chunk_abc123",
    "dataId": "data_xyz789",
    "content": "更新后的切片内容，长度需在 10-6000 字符之间。",
    "title": "更新后的标题",
    "isDisplayedChunkContent": true
  }'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

## 响应示例

更新成功返回 200。

```
{
  "code": "Success",
  "status_code": 200,
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

### 响应字段

字段

类型

说明

`code`

string

响应码，成功时为 `Success`

`status_code`

integer

HTTP 状态码

`request_id`

string

请求唯一标识，排查问题时请提供此 ID

`success`

boolean

操作是否成功

`message`

string

响应消息，成功时为 `success`

`status`

string

请求状态：`SUCCESS` 或 `FAILED`

## 错误码

HTTP 状态码

错误码

错误信息

说明

400

`Index.InvalidParameter`

`Required parameter missing or invalid.`

请求参数无效

401

`InvalidApiKey`

`Invalid API-key provided.`

鉴权失败，API Key 无效或缺失
