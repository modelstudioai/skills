# application component api reference

应用组件 API 提供了百炼平台中可复用业务能力的标准化调用接口，用于构建对话式 AI 应用（如智能客服、知识助手等）。该接口封装了模型推理、上下文管理、工具调用等核心能力，支持通过 HTTP 请求快速集成。开发者需通过 RAM 授权并使用指定 Endpoint 访问服务。

## 支持的模型/功能

当前应用组件 API 支持以下模型与能力：
- 基础大模型推理：`qwen-max`、`qwen-plus`、`qwen-turbo`（详见 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)）
- 多轮对话状态管理（含 history 透传与 session 生命周期控制）
- 内置工具调用（如搜索、数据库查询、代码执行），需在 `tools` 字段中声明
- 流式响应（`stream=true`）与非流式响应双模式支持

> **注意**：`qwen-vl` 和 `qwen-audio` 等多模态模型暂未开放至应用组件 API，仅限独立多模态 API 调用；此限制在 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中有明确标注，但 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 中未同步更新，以目录为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为白名单内值，如 `qwen-plus` |
| `input.messages` | array | 是 | 对话消息列表，每项含 `role`（`user`/`assistant`/`system`）和 `content` |
| `parameters.temperature` | number | 否 | 默认 0.85，取值范围 [0, 2] |
| `parameters.top_p` | number | 否 | 默认 0.8，取值范围 [0, 1] |
| `stream` | boolean | 否 | true 时返回 SSE 流，false 时返回 JSON 包体 |
| `tools` | array | 否 | 工具定义数组，结构见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 附录 |

## 使用方式

1. **鉴权**：使用阿里云 STS Token 或长期 AccessKey，通过 `Authorization: Bearer <token>` 头传递  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat`（Endpoint 具体值见 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md)）  
3. **示例请求体**：
```json
{
  "model": "qwen-plus",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.5},
  "stream": false
}
```

## 限制和注意事项

- 单次请求 `input.messages` 最多支持 50 轮历史消息（含 system），总 token 数上限为模型 context length 的 90%  
- `app_id` 必须已在百炼控制台创建并启用，且已绑定有效模型配额  
- 流式响应下，`tool_calls` 字段可能分片返回，客户端需按 `delta` 顺序拼接解析  
- RAM 授权策略需包含 `dashscope:ListApps` 和 `dashscope:InvokeApp` 权限（详见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）  
- 超时时间建议设为 120 秒（部分长上下文场景可能接近上限）

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


