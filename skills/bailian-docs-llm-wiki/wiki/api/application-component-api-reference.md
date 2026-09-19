# application component api reference

应用组件 API 是百炼平台提供的核心能力封装，用于在自定义应用中集成大模型推理、知识检索、工具调用等能力。该接口以标准化 RESTful 形式提供，支持同步响应与[流式输出](../concepts/streaming-output.md)，适用于构建对话机器人、智能助手、自动化工作流等场景。所有调用需通过 RAM 授权并使用指定服务接入点 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型与功能

当前支持以下能力模块：
- **大模型推理**：`qwen-max`、`qwen-plus`、`qwen-turbo`（具体支持列表见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）
- **增强功能**：RAG 检索（需配置知识库 ID）、[函数调用](../concepts/function-calling.md)（Function Calling）、多轮上下文管理（最大 16K tokens 上下文窗口）

> **注意**：文档中提及的 `qwen-vl` 和 `qwen-audio` 模型在最新 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中已明确标记为“暂不开放公测”，实际调用将返回 `400 UnsupportedModel` 错误。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-plus`；必须与 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中列出的值严格一致 |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；`role` 仅支持 `user`/`assistant`/`system` |
| `parameters.temperature` | number | 否 | 取值范围 [0.0, 2.0]，默认 1.0；低于 0.1 时可能触发确定性解码（详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)） |

## 使用方式

1. 获取 RAM 凭据（AccessKey ID/Secret），确保策略包含 `bailian:InvokeApplicationComponent` 权限  
2. 构造 HTTPS POST 请求，Endpoint 请参考 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)  
3. 设置 Header：`Authorization: Bearer <access_token>`（或使用 AK/SK 签名）  
4. Body 示例（JSON）：
```json
{
  "model": "qwen-plus",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.8}
}
```

## 限制和注意事项

- 单次请求 `input.messages` 总长度不得超过 32768 字符（UTF-8 编码）  
- 流式响应（`stream=true`）需设置 `Accept: text/event-stream`，且不支持重试机制  
- 跨区域调用（如杭州 AK 调用上海 Endpoint）将失败，务必匹配 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 的地域标识  
- 所有参数名区分大小写，`model` 不可写作 `Model` 或 `MODEL`，否则返回 `400 InvalidParameter`

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


