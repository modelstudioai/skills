# bailian application calling

百炼平台支持通过 API 方式调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的集成。调用过程需使用有效的 API Key 和应用 ID，并遵循统一的 HTTP 接口规范。所有调用均通过 `POST /v1/applications/{app_id}/call` 端点发起，请求体为 JSON 格式。

## 支持的模型/功能

- **智能体应用**：支持单步推理、多轮对话（需显式维护 `session_id`）、工具调用（如知识库检索、代码解释器等）；适用于客服助手、技术问答等场景。  
- **工作流应用**：支持多节点编排（如条件分支、并行执行、子流程嵌套），可接入自定义函数节点与外部 API；适用于审批流、数据处理流水线等复杂逻辑场景。  
- 两类应用均支持流式响应（`stream: true`），但工作流应用的[流式输出](../concepts/streaming.md)粒度取决于节点配置，详见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入内容，结构由应用定义；智能体应用通常为 `{ "query": "..." }`，工作流应用需严格匹配入参 Schema |
| `session_id` | string | 否 | 用于维持多轮上下文；同一 `session_id` 下的历史消息将被自动注入（仅对智能体应用生效） |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应，适用于长响应或实时渲染场景 |
| `parameters` | object | 否 | 覆盖应用发布时设置的默认参数（如温度、最大 token 数），具体字段以 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md) 为准 |

> **注意**：`parameters` 中的 `top_p`、`temperature` 等采样参数对工作流应用无效，仅作用于底层 LLM 节点；若工作流中包含多个 LLM 节点，需在节点级单独配置，而非通过顶层 `parameters` 统一覆盖 —— 此行为与 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 文档描述一致，但与旧版文档中“全局参数透传”的说法存在偏差，请以当前控制台实际行为为准。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建并启用密钥；
2. 构造请求：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/v1/applications/{app_id}/call" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "input": {"query": "今天北京天气如何？"},
           "session_id": "sess_abc123",
           "stream": false
         }'
   ```
3. 解析响应：成功时返回 `200 OK`，响应体含 `output` 字段（结构由应用定义）及 `usage`（token 消耗统计）；流式响应需按 SSE 协议解析 `data:` 行。

## 限制和注意事项

- 单次请求 `input` 内容长度上限为 100,000 字符，超出将返回 `400 Bad Request`；
- `session_id` 生命周期为 24 小时，超时后上下文自动清空；智能体应用不支持跨 `session_id` 追溯历史；
- 工作流应用若含异步节点（如定时触发、人工审核），`/call` 接口默认同步等待至首个阻塞点完成，**不等待最终结果**；如需最终状态，须调用独立的查询接口（见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md)）；
- 所有调用受账户 QPS 与总 [Token](../concepts/token.md) 配额限制，配额可在控制台「用量管理」中查看。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)



