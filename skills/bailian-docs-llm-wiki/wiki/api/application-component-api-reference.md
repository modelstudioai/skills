# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于构建对话式 AI 应用（如智能客服、知识助手等）。该 API 封装了模型推理、上下文管理、工具调用等核心能力，开发者无需直接对接底层模型即可集成高阶功能。所有接口均基于 RESTful 设计，支持 HTTPS 调用与 RAM 授权。

## 支持的模型/功能

当前应用组件 API 支持以下模型与能力：
- 内置模型：`qwen-max`、`qwen-plus`、`qwen-turbo`（默认为 `qwen-turbo`）；
- 功能模块：多轮对话状态维护、RAG 检索增强、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应（`stream=true`）；
- 工具集成：支持通过 `tools` 字段声明并调用预注册的插件（如搜索、数据库查询），具体可用工具列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)。

> **注意**：文档中提及的 `qwen-vl` 和 `qwen-audio` 模型**暂未开放**于应用组件 API，仅限独立多模态 API 使用；此信息与 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md) 中“支持全模态模型”的表述存在冲突，以本节为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，必须为白名单内值（见上节） |
| `messages` | array | 是 | 对话历史，格式为 `[{ "role": "user/system/assistant", "content": "..." }]` |
| `stream` | boolean | 否 | 默认 `false`；设为 `true` 时返回 SSE 流式响应 |
| `tools` | array | 否 | 工具定义数组，结构需严格匹配 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md) 中已授权的工具 Schema |
| `tool_choice` | string / object | 否 | 控制工具调用策略，可选 `"auto"`、`"none"` 或指定工具名称 |

## 使用方式

1. **获取访问凭证**：通过 RAM 角色或 AccessKey 获取 `Authorization` 头（详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）；  
2. **确定接入点**：使用地域化 Endpoint，例如 `https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`（Endpoint 列表见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）；  
3. **发起请求**：POST JSON payload，`Content-Type: application/json`，示例：
   ```json
   {
     "model": "qwen-plus",
     "messages": [{"role": "user", "content": "今天北京天气如何？"}],
     "stream": true
   }
   ```

## 限制和注意事项

- 单次请求 `messages` 总长度上限为 32768 token（含 system prompt）；
- 流式响应中 `delta.content` 可能为空（表示工具调用触发），需检查 `delta.tool_calls` 字段；
- 应用 ID（`app_id`）需在百炼控制台创建，并确保其关联的模型与工具已获 RAM 授权；
- 版本兼容性：v2023-12-29 是当前唯一稳定版本，旧版接口已下线；变更详情参见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)。

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


