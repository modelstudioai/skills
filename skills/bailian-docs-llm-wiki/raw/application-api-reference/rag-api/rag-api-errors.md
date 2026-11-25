# Knowledge（原RAG） API 错误码

RAG API 的错误响应结构、HTTP 状态码、业务错误码与重试策略。

所有错误响应使用统一结构：

<a id="code-block"></a>

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "字段 knowledge_base_id 不能为空",
    "param": "knowledge_base_id"
  },
  "request_id": "req_xxx"
}
```

<a id="http-状态码"></a>

<a id="h-ragapi-errors-http"></a>

## HTTP 状态码

| 状态码 | 含义 | 处理建议 |
| --- | --- | --- |
| 400 | 请求参数错误 | 校对参数 |
| 401 | 鉴权失败 | 检查 API Key |
| 403 | 无权限 | 申请对应权限范围 |
| 404 | 资源不存在 | 校对 ID |
| 409 | 资源冲突 | 通常为名称重复 |
| 413 | 请求体过大 | 拆分请求 |
| 429 | 限流 | 退避重试 |
| 500 | 服务内部错误 | 重试,持续失败联系支持 |
| 503 | 服务不可用 | 退避重试 |

<a id="业务错误码"></a>

<a id="h-ragapi-errors-codes"></a>

## 业务错误码

| code | HTTP | 说明 |
| --- | --- | --- |
| INVALID\_PARAMETER | 400 | 参数缺失或格式错误 |
| UNAUTHORIZED | 401 | API Key 缺失或无效 |
| FORBIDDEN | 403 | 无操作权限 |
| KB\_NOT\_FOUND | 404 | 知识库不存在 |
| DOCUMENT\_NOT\_FOUND | 404 | 文档不存在 |
| DATA\_SOURCE\_NOT\_FOUND | 404 | 数据源不存在 |
| KB\_NAME\_CONFLICT | 409 | 知识库名称已存在 |
| QUOTA\_EXCEEDED | 429 | 超出租户配额 |
| RATE\_LIMITED | 429 | 接口限流 |
| EMBEDDING\_FAILED | 500 | 嵌入服务异常 |
| RETRIEVAL\_TIMEOUT | 504 | 检索超时,建议降低 top\_k 或启用更小的重排模型 |
| SYNC\_SOURCE\_UNREACHABLE | 502 | 数据源连接失败 |

<a id="wiki-相关错误码"></a>

<a id="h-ragapi-errors-wiki"></a>

## Wiki 相关错误码

旗舰版知识库开启 Wiki 与 Wiki 检索相关错误码如下。实际响应中 `code` 可能带服务名前缀（如 `Index.WikiConfigInvalid`）。Wiki 配置的请求字段使用 camelCase（如 `wikiAutoUpdate`、`synthesisModelId`），但校验失败时 `message` 中的字段名为 snake\_case（如 `wiki_auto_update`、`synthesis_model_id`），需注意映射。

| code | HTTP | 说明 |
| --- | --- | --- |
| `WikiNotEnabled` | 400 | Wiki 检索时服务绑定的知识库未全部开启 Wiki |
| `WikiPreconditionNotMet` | 400 | 知识库不存在、不属于当前账号、已被删除，或知识库服务尚未就绪 |
| `WikiEditionNotSupported` | 400 | 开启 Wiki 时知识库不是旗舰版；或降配为标准版的同时要求开启 |
| `WikiSceneNotSupported` | 400 | 开启 Wiki 时知识场景不是 `basic_document_qa` |
| `WikiOperationConflict` | 409 | 开启中要求关闭、关闭中要求开启，或有其他 Wiki 操作进行中 |
| `WikiConfigInvalid` | 400 | Wiki 配置键非法，如缺少 `extraction` 组、`synthesisModelId` 缺失或不在候选清单、`extractionGranularity` 取值非法、指令超长，按 `message` 里的字段名定位 |

<a id="重试策略"></a>

<a id="h-ragapi-errors-retry"></a>

## 重试策略

| 错误类型 | 是否重试 | 间隔 |
| --- | --- | --- |
| 4xx(限流除外) | 否 | — |
| 429 限流 | 是 | `Retry-After` 头给出,或 1s/2s/4s 指数退避 |
| 5xx | 是 | 1s/2s/4s,最多 3 次 |
| 504 超时 | 是 | 直接重试,最多 2 次 |

<a id="排错"></a>

<a id="h-ragapi-errors-troubleshoot"></a>

## 排错

每个响应都带 `request_id`。联系支持时附上该 ID，可快速定位日志。

> **重要**
>
> 看看具体接口，从[查询知识库列表](rag-api-knowledge-base/rag-api-list-indices.md)开始。
