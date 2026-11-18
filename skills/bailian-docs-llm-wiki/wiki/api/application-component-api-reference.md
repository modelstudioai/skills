# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置业务能力（如对话管理、知识检索、工作流编排等）的标准接口。该 API 以 RESTful 形式提供，支持通过 HTTP 请求完成模型调用、状态查询与结果解析。所有请求需携带有效的身份凭证，并遵循统一的请求结构与响应规范。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- **对话式交互**：基于 `chat` 类型组件实现多轮上下文感知的问答（详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）；
- **知识增强检索**：通过 `retrieval` 组件对接向量库与结构化知识源，支持语义召回与结果精排；
- **工作流编排**：使用 `workflow` 组件串联多个子任务（如意图识别 → 参数提取 → API 调用），支持条件分支与异步回调。

> **注意**：原始文档中 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 列出的 `agent` 类型组件已在 v2.1.0 版本中废弃，实际可用类型请以 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的“已移除功能”章节为准。

## 关键参数

所有请求必须包含以下通用参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `component_id` | string | 是 | 应用内唯一注册的组件 ID，由控制台分配或通过 `/components/register` 接口创建获得 |
| `input` | object | 是 | 用户输入数据，结构依组件类型而异（如 `chat` 要求 `messages: []`，`retrieval` 要求 `query: string`）|
| `parameters` | object | 否 | 运行时覆盖配置项，例如 `temperature`, `top_k`, `enable_history` 等 |

部分高级参数（如 `stream: true`）仅对 `chat` 和 `workflow` 组件生效，具体支持范围请参考 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 文档中的接口级说明。

## 使用方式

1. **鉴权准备**：使用 RAM 角色密钥（AccessKey）或 STS 临时凭证，按 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 要求构造 `Authorization` 头；
2. **构造请求**：向服务端点（如 `https://dashscope.aliyuncs.com/api/v1/components/{component_id}/invoke`）发送 `POST` 请求；
3. **处理响应**：成功响应为 JSON 格式，含 `output` 字段（结构化结果）与 `trace_id`（用于问题排查）；流式响应需按 SSE 协议解析事件流。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 2 MB，`parameters` 键值对总数不得超过 50；
- `chat` 组件默认保留最近 10 轮历史消息，超出部分需显式传入 `history` 数组控制；
- 所有组件均不支持跨区域调用，请求 endpoint 必须与组件部署地域一致（参见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；
- 若同时调用多个 `workflow` 实例，请确保 `callback_url` 具备幂等性，避免重复触发下游系统。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


