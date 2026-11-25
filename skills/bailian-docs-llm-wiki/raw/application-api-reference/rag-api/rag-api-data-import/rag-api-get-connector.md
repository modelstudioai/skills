# 查询数据集

查询指定数据集的详细信息。可通过数据集 ID 或名称查询，至少传入其中一个参数。

<a id="前提"></a>

<a id="h-ragapi-get-connector-prereq"></a>

## 前提

已获取阿里云百炼 API Key（[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)）并完成鉴权配置，详见 [Knowledge（原RAG） API 概览](../rag-api-overview.md)与[鉴权](../rag-api-authentication.md)。数据导入接口与其他 Knowledge API（原RAG API） 使用相同的 Base URL 与鉴权方式，路径前缀为 `/api/v1/connector/dash/`。

<a id="接口"></a>

<a id="h-ragapi-get-connector-endpoint"></a>

## 接口

**POST** `/api/v1/connector/dash/getConnector`

查询指定数据集的详细信息。可通过数据集 ID 或名称查询，至少传入其中一个参数。

> **说明**
>
> `connectorId` 和 `connectorName` 至少需要传入一个。两者都传入时，以 `connectorId` 为准。

<a id="请求体"></a>

<a id="h-ragapi-get-connector-req"></a>

## 请求体

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `connectorId` | 否 | string | 数据集 ID，与 connectorName 至少传入一个。 |
| `connectorName` | 否 | string | 数据集名称，与 connectorId 至少传入一个，最长 20 个字符。 |

<a id="请求示例"></a>

<a id="h-ragapi-get-connector-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X POST "$BASE_URL/api/v1/connector/dash/getConnector" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "connectorId": "conn_abc123"
  }'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-ragapi-get-connector-resp"></a>

## 响应示例

成功返回 200。

<a id="code-block-2"></a>

```json
{
  "code": "Success",
  "message": "",
  "messageUnmodified": false,
  "requestId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "data": {
    "connectorId": "conn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx_xxxxxx",
    "connectorName": "默认文件数据集",
    "connectorType": "FILE",
    "connectorSubType": "UNSTRUCTURED",
    "description": "默认文件类型数据集",
    "gmtCreate": "2026-03-16 16:13:26",
    "gmtModified": "2026-03-16 16:13:26"
  },
  "status": 200
}
```

<a id="响应字段"></a>

<a id="h-ragapi-get-connector-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 响应码，成功时为 `Success`。 |
| `message` | string | 错误或提示信息，成功时为空字符串。 |
| `requestId` | string | 请求唯一标识，排查问题时请提供此 ID。 |
| `data` | object | 数据集详情。子字段 `connectorId`（string，数据集 ID）、`connectorType`（string，数据集类型，当前仅支持 FILE）、`connectorName`（string，数据集名称）、`description`（string，数据集描述）、`connectorSubType`（string，数据集子类型，如 `UNSTRUCTURED`）、`gmtCreate`（string，创建时间，格式 `YYYY-MM-DD HH:mm:ss`）、`gmtModified`（string，最后修改时间，格式 `YYYY-MM-DD HH:mm:ss`）。 |
| `status` | integer | 业务状态码。成功为 `200`，参数错误等失败场景为 `400`。注意失败时 HTTP 状态码仍为 200，需根据本字段与 `code` 判断结果。 |

<a id="错误码"></a>

<a id="h-ragapi-get-connector-err"></a>

## 错误码

| HTTP 状态码 | 错误码 `code` | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | 请求参数无效。`message` 示例：`Required parameter missing or invalid.` |
| 401 | `InvalidApiKey` | 鉴权失败，API Key 无效或缺失。`message` 示例：`Invalid API-key provided.` |

业务失败时 HTTP 状态码仍为 200，需根据响应体中的 `status` 与 `code` 判断结果。
