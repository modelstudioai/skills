# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、知识库检索、工作流编排等能力。该 API 采用 RESTful 设计，支持标准 HTTP 请求与 JSON 数据格式，适用于服务端调用场景。所有接口均需通过 RAM 授权及 API Key 鉴权，具体接入方式和参数规范详见下文。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：
- 同步/异步大模型推理（含 Qwen 系列、Qwen2 系列及部分第三方模型）
- 基于向量库的知识检索（需提前配置知识库 ID）
- 多步骤工作流执行（通过 `workflow_id` 触发预设流程）
- 模型输出结构化解析（启用 `response_format` 参数可返回 JSON Schema 校验结果）

> **注意**：文档 [API概览](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中列出的 `qwen-vl-plus` 模型已下线，实际可用模型请以 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中最新 `model_id` 列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 是 | 模型唯一标识，如 `qwen-max`、`qwen-plus`；取值必须来自 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) |
| `input` | object | 是 | 输入内容，结构为 `{ "messages": [...] }` 或 `{ "query": "...", "retrieval": { "knowledge_id": "..." } }` |
| `parameters` | object | 否 | 推理参数，如 `temperature`（0.0–2.0）、`max_tokens`（1–8192）等；详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) |
| `response_format` | object | 否 | 指定结构化输出格式，需提供 `type: "json_schema"` 及 `schema` 定义 |

## 使用方式

1. **获取接入点**：调用前需从 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 获取对应 Region 的 endpoint URL（如 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`）  
2. **构造请求**：使用 `POST` 方法，Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. **发送调用**：Body 示例：
   ```json
   {
     "model_id": "qwen-max",
     "input": {
       "messages": [{"role": "user", "content": "你好"}]
     },
     "parameters": {"temperature": 0.5}
   }
   ```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 10 条消息，总 token 数上限为 32768（含 system [prompt](../guides/prompt.md)）  
- 异步任务（`/v1/apps/{app_id}/chat/async`）最长保留结果 24 小时，超时后无法查询  
- 知识库检索仅支持已发布状态的知识库，草稿或已删除知识库将返回 `404` 错误  
- > **注意**：[授权信息](raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 文档中描述的旧版 STS [Token](../concepts/token.md) 方式已废弃，现仅支持 API Key 或 RAM Role Assume 方式鉴权，请以 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中 v2024-03-01 起的变更为准。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


