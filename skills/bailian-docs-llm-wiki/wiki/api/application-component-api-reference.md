# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、知识检索、工作流编排等能力。该 API 以 RESTful 形式提供，支持同步调用与流式响应，适用于构建对话机器人、智能客服、RAG 应用等场景。所有接口均需通过 RAM 授权并使用指定服务接入点 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型/功能

- **基础模型调用**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等 Qwen 系列模型（详见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）  
- **增强能力组件**：包括知识库检索（`retrieval`）、[函数调用](../concepts/function-calling.md)（`tool_call`）、多步骤工作流（`workflow`）等可插拔模块  
- **输入适配器**：支持结构化消息（`messages` 数组）、文件上传（`file_ids`）、上下文快照（`session_id`）等输入形式  

> **注意**：`qwen-vl` 和 `qwen-audio` 模型暂未在当前版本的应用组件 API 中开放，相关能力请参考 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中标注的“实验性接口”说明，实际调用前需确认服务端白名单配置。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-plus`；必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的可用模型一致 |
| `input.messages` | array | 是 | 对话历史数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`（string 或 object） |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；范围 `[0.0, 2.0]` |
| `parameters.top_p` | number | 否 | 核采样阈值，默认 `0.95`；范围 `[0.0, 1.0]` |
| `parameters.max_tokens` | integer | 否 | 最大生成 token 数，默认 `1024`，上限 `4096` |

## 使用方式

1. **认证**：使用阿里云 RAM 用户 AccessKey（`AccessKeyId` + `AccessKeySecret`），通过 `X-Authorization` 请求头传递 STS [Token](../concepts/token.md) 或签名凭证（参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）  
2. **请求地址**：向服务接入点（如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）发送 `POST` 请求（具体 endpoint 见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）  
3. **响应解析**：成功时返回 `200 OK`，`output.text` 为生成文本；流式响应需监听 `text/event-stream`，按 `data:` 行解析 chunk  

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含角色标记）不得超过 32768 tokens；超长内容需预处理截断或分片  
- 免费调用量受应用配额限制，超出后返回 `429 Too Many Requests`；配额策略详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)  
- `system` 角色消息仅支持首条消息，后续 `system` 消息将被忽略（此行为与部分旧版 SDK 文档描述不一致，请以 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 实际行为为准）  
- 文件类输入（如 PDF、TXT）需先调用 `/v1/files` 接口上传获取 `file_id`，再在 `input` 中引用；直接传 raw content 将导致 `400 Bad Request`

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


