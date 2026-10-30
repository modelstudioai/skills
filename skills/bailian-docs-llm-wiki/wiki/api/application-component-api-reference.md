# application component api reference

应用组件 API 是百炼平台提供的核心能力接口，用于在自定义应用中集成大模型推理、工具调用、会话管理等能力。该 API 以 RESTful 形式提供，支持同步/异步调用模式，适用于构建对话机器人、智能助手、自动化工作流等场景。所有请求需通过 RAM 授权并使用指定服务接入点 [API概览](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-overview.md)。

## 支持的模型与功能

当前支持以下模型类型及对应能力：
- **基础大模型**：`qwen-max`、`qwen-plus`、`qwen-turbo`（见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)）
- **工具增强模式**：支持 `tools` 字段声明函数列表，自动触发工具调用（需模型支持 function calling，如 `qwen-max`）
- **多轮会话管理**：通过 `conversation_id` 维持上下文，最长支持 100 轮历史（详见 [版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md)）

> **注意**：`qwen-turbo` 在 v2023-12-29 版本中**不支持工具调用**，但 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md) 中未明确标注该限制，实际调用将返回 `400 Bad Request`。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须为白名单内值（参见 [API目录](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir.md)） |
| `input.messages` | array | 是 | 消息数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`（string 或 object） |
| `parameters.temperature` | number | 否 | 取值范围 0.0–2.0，默认 0.85 |
| `parameters.max_tokens` | integer | 否 | 最大生成 token 数，上限 8192 |
| `parameters.top_p` | number | 否 | 核采样阈值，取值范围 0.0–1.0，默认 0.8 |

## 使用方式

1. **认证**：使用阿里云 RAM 凭据生成 STS [Token](../concepts/token.md) 或 AccessKey 签名，授权策略需包含 `bailian:InvokeApplicationComponent` 权限（见 [授权信息](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-ram.md)）  
2. **端点**：调用 `POST https://bailian.aliyuncs.com/api/v1/applications/{app_id}/components/invoke`（具体地址以 [服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 为准）  
3. **示例请求体**：
```json
{
  "model": "qwen-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 100 条；单条 `content` 文本长度上限 100,000 字符  
- 异步调用（`async=true`）返回 `task_id`，需轮询 `/tasks/{task_id}` 获取结果，超时时间为 10 分钟  
- `system` 角色消息仅支持首条消息，后续出现将被忽略（[版本说明](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-changeset.md) 明确此行为）  
- 不支持跨 Region 调用：`app_id` 所属地域必须与请求 endpoint 地域一致（[服务接入点](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-endpoint.md) 中各 endpoint 均绑定固定 Region）

## 来源文档

- [应用组件](../../raw/application-api-reference/application-component-api-reference.md)


