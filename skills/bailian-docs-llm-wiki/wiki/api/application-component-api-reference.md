# application component api reference

应用组件 API 提供了在百炼平台中集成和调用预置能力（如对话、知识检索、工具调用等）的标准接口，适用于构建企业级 AI 应用。该 API 以 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming-output.md)，并与百炼统一身份认证体系深度集成。开发者需通过 RAM 授权获取访问凭证，方可调用相关接口。

## 支持的模型/功能

当前应用组件 API 支持以下核心能力：  
- 基于大模型的多轮对话（`chat` 类型任务）  
- 结构化知识库检索（`retrieval` 类型任务，依赖已配置的知识空间 ID）  
- 内置工具链调用（如日期计算、网页摘要、代码解释等，详见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）  
- 自定义[插件](../concepts/plugin.md)扩展（需提前在控制台注册并发布）  

> **注意**：部分文档中提及的 `code_generation` 功能模块已在 v2024.03 版本中合并至通用 `chat` 接口，旧版独立 endpoint 已废弃；请以 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中的变更日志为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，由控制台创建应用时生成 |
| `messages` | array | 是 | 对话消息列表，格式同 OpenAI `messages`，支持 `user`/`assistant`/`system` 角色 |
| `model` | string | 否 | 指定后端模型，可选值包括 `qwen-max`、`qwen-plus`、`qwen-turbo`；未指定时使用应用默认模型 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；流式模式下响应为 SSE 格式 |
| `retrieval_config` | object | 否 | 知识检索配置，含 `knowledge_id` 和 `top_k` 字段，详见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 中的请求体示例 |

## 使用方式

1. 获取访问凭证：通过 RAM 角色或 AccessKey 进行签名认证，授权流程参见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)  
2. 构造请求：向 `POST /v1/apps/{app_id}/chat`（或 `/v1/apps/{app_id}/retrieval`）发送 JSON 请求  
3. 处理响应：非流式返回标准 JSON；流式响应需按 `data:` 行解析，每条事件含 `delta` 或 `finish_reason` 字段  

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（按 Qwen 分词器统计）  
- 流式响应超时时间为 60 秒，超时将关闭连接并返回 `504 Gateway Timeout`  
- `app_id` 必须与调用方 RAM 权限绑定的应用完全一致，跨应用调用将返回 `403 Forbidden`  
- 所有请求必须携带 `X-Bailian-Date` 和 `Authorization` 头，签名算法与阿里云通用一致，细节见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


