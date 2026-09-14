# bailian application calling

百炼平台支持通过 API 方式调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的集成。调用过程需使用有效的 API Key 和应用 ID，并遵循统一的 HTTP 接口规范。所有调用均通过 `POST /v1/applications/{app_id}/call` 端点发起，请求体为 JSON 格式。

## 支持的模型/功能

- **智能体应用**：支持单步推理、多轮对话（需显式维护 `session_id`）、工具调用（如知识库检索、代码解释器等）；详见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。  
- **工作流应用**：支持串行/并行节点编排、条件分支、自定义函数节点；输入参数可透传至各子节点，输出结构由工作流定义决定；该能力在 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 中有基础说明，但完整节点行为请参考 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 的官方链接指引。  
- 不支持直接调用未发布状态的应用，也不支持跨地域调用（应用与调用方需处于同一 Region）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入内容，结构由应用 Schema 定义；若应用启用参数校验，非法字段将被拒绝 |
| `session_id` | string | 否 | 用于多轮对话上下文保持；同一 `session_id` 下的历史消息默认保留 30 分钟（超时后自动清理） |
| `stream` | boolean | 否 | 设为 `true` 时返回 SSE 流式响应；注意流式模式下不支持 `session_id` 的自动续期（需客户端主动维护） |

> **注意**：原始文档中 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md) 提到“`input` 支持任意嵌套对象”，但实际接口校验严格遵循应用创建时配置的 OpenAPI Schema。若 Schema 定义为 `{"type": "object", "properties": {"query": {"type": "string"}}}`，则传入 `{"query": "hi", "extra": 123}` 将被静默过滤 `extra` 字段——此行为与文档字面描述存在偏差，以实际接口响应为准。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建或复用已有密钥；  
2. 构造请求：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/applications/{app_id}/call" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"query": "今天天气如何？"},
           "session_id": "sess_abc123"
         }'
   ```
3. 解析响应：成功时返回 `200 OK`，`output` 字段包含应用执行结果；错误时返回标准 `error.code` 与 `error.message`（如 `InvalidInput`, `SessionExpired`）。

## 限制和注意事项

- 单次调用 `input` 总大小上限为 1MB；`output` 响应体上限为 4MB；  
- 智能体应用默认最大响应长度为 4096 tokens，可通过应用配置页调整（需重新发布生效）；  
- 工作流应用中若某节点超时（默认 60 秒），整个调用失败，不会部分返回；  
- 所有调用均计入账号配额，具体 QPS/TPM 限制请查阅当前套餐规格；  
- 若发现 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling.md) 文档中关于 session 过期时间描述为“24 小时”，而实际接口返回 `X-Session-Expires-In: 1800`（即 30 分钟），请以接口响应头及实时控制台配额页说明为准。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


