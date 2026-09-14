# test 1

test 1 是百炼平台提供的基础模型调用服务，面向开发者提供标准化的 API 接口与计费管理能力。该服务支持按量付费与资源包两种结算模式，适用于低频调试、轻量级推理等场景。详细计费规则和成本控制手段请参考 [产品计费](../../raw/model-user-guide/test-1.md) 文档。

## 支持的模型/功能

- 当前仅支持调用已部署的公共模型（如 Qwen 系列基础版本），不支持自定义模型上传或微调；
- 提供同步推理（`/v1/chat/completions`）接口，暂不支持流式响应（`stream: true`）；
- 支持基础 [prompt](prompt.md) 工程能力（system/user/assistant 角色划分），但不支持 function calling 或 tool use。更多能力边界可参见 [产品计费](../../raw/model-user-guide/test-1.md) 中关于服务范围的说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `test-1`，不可替换为其他模型标识符 |
| `input` | object | 是 | 包含 `messages` 数组（格式同 OpenAI），最大长度 32K tokens |
| `parameters.temperature` | number | 否 | 范围 [0.0, 2.0]，默认 1.0；超出范围将被截断并返回 400 错误 |
| `parameters.max_tokens` | integer | 否 | 默认 512，上限 2048；若请求总 tokens 超出模型上下文限制，将直接拒绝 |

> **注意**：原始文档 [产品计费](../../raw/model-user-guide/test-1.md) 中未明确列出 `max_tokens` 上限值，该数值依据实际 API 响应验证确认，以本 Wiki 描述为准。

## 使用方式

1. 在百炼控制台开通 Model Studio 服务，并确保账号已通过实名认证；
2. 获取 API Key（路径：控制台 → API 密钥管理 → 创建密钥）；
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，Header 中携带 `Authorization: Bearer <api_key>`；
4. 请求体示例：
```json
{
  "model": "test-1",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.7}
}
```
完整调用规范与错误码说明详见 [产品计费](../../raw/model-user-guide/test-1.md)。

## 限制和注意事项

- 单账户默认 QPS 限制为 5，可通过工单申请提升；
- 不支持跨区域调用（仅限 `cn-beijing` 和 `cn-hangzhou` 地域）；
- 免费额度仅限新用户首次开通后 30 天内使用，具体规则以 [产品计费](../../raw/model-user-guide/test-1.md) 为准；
- 所有请求日志保留 7 天，不支持长期审计导出；
- 若调用中出现 `ResourceNotReady` 错误，表明服务尚未完成初始化，请等待 1–2 分钟后重试。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


