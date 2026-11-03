# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于在自定义应用中集成对话、知识检索、工作流编排等核心功能。该 API 采用 RESTful 设计，支持通过 HTTP 请求调用，并依赖 RAM 授权与固定服务接入点。所有接口均需指定 `X-DashScope-Source` 请求头以标识调用来源。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- **对话交互**：基于 `bailian-v1` 等基础大模型提供多轮会话能力（详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）；
- **知识增强检索**：结合向量库与关键词混合策略，支持文档级语义召回；
- **工作流执行**：通过 `workflow_id` 触发预置的可视化编排流程，返回结构化执行结果。

> **注意**：原始文档中 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 列出的 `/v1/components/chat` 接口已废弃，实际应使用 `/v1/applications/{app_id}/chat`（参见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中 2024-03-15 的变更记录）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成 |
| `messages` | array | 是 | 对话消息列表，格式同 DashScope ChatCompletion，每项含 `role` 和 `content` |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；流式下需按 SSE 协议解析 |
| `user_id` | string | 否 | 用户标识，用于会话状态隔离与审计追踪 |

所有请求必须携带有效的 `Authorization: Bearer <token>` 及 `X-DashScope-Source: application-component` 头，否则将被拒绝（参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）。

## 使用方式

1. 获取 `app_id` 与 `API Key`（通过 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 查询当前 Region 的 endpoint）；
2. 构造 POST 请求至 `https://{endpoint}/v1/applications/{app_id}/chat`；
3. 设置请求头与 JSON body，示例：
   ```json
   {
     "messages": [{"role": "user", "content": "你好"}],
     "stream": false
   }
   ```

## 限制和注意事项

- 单次请求 `messages` 长度上限为 32，总 token 数不超过模型上下文窗口（如 `bailian-v1` 为 32768）；
- 流式响应不支持 `function calling` 返回格式，仅返回 `content` 字段增量；
- 调用频率受应用级 QPS 限制（默认 5 QPS），超出将返回 `429 Too Many Requests`；
- `user_id` 若为空字符串或缺失，系统将自动分配匿名 ID，可能导致会话状态无法持久化。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


