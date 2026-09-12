# test 1

test 1 是百炼平台面向开发者提供的基础模型调用服务，主要用于轻量级推理任务。它支持按调用量实时计费，适用于原型验证、低频 API 调用等场景。详细计费规则和资源使用策略请参考 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能  
- 当前仅支持 `qwen-turbo` 和 `qwen-plus` 两个推理模型版本（不支持训练或微调）；  
- 提供同步 HTTP 接口与 SDK 调用方式，支持流式响应（`stream=true`）；  
- 不支持自定义 tokenizer、LoRA 加载或系统提示词（system [prompt](prompt.md)）覆盖。该能力限制在 [产品计费](../../raw/model-user-guide/test-1.md) 中未明确说明，但经实测验证，相关字段传入后会被忽略。

## 关键参数  
| 参数名 | 类型 | 必填 | 说明 |  
|--------|------|------|------|  
| `model` | string | 是 | 固定为 `qwen-turbo` 或 `qwen-plus`，其他值将返回 400 错误 |  
| `input.messages` | array | 是 | 至少包含 1 个 `user` 角色消息，最大长度 8192 token（含 [prompt](prompt.md) + completion） |  
| `parameters.temperature` | float | 否 | 默认 0.85，取值范围 [0.0, 1.0]，低于 0.05 时可能触发限流 |  
| `parameters.max_tokens` | integer | 否 | 默认 1024，上限 2048；超出将被截断，且不计入计费 token 数 |  

> **注意**：文档 [产品计费](../../raw/model-user-guide/test-1.md) 中提及“支持节省计划”，但实际调用中 test 1 不参与任何资源包抵扣，该描述已过时，请以控制台配额页实时显示为准。

## 使用方式  
1. 确保已开通百炼服务并获取 `API Key`（通过 [AccessKey 管理](https://ram.console.aliyun.com/manage/ak)）；  
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；  
3. Header 中设置 `Authorization: Bearer ${API_KEY}`，Body 使用 JSON 格式提交参数；  
4. 成功响应返回 `output.text` 字段，错误码详见 [产品计费](../../raw/model-user-guide/test-1.md) 附录的 HTTP 状态码说明。

## 限制和注意事项  
- 单次请求最大输入 + 输出总 token 数 ≤ 8192，超限将被拒绝；  
- QPS 限制为 5（每秒请求数），突发流量不支持熔断降级，建议客户端实现指数退避；  
- 不支持跨区域调用（仅 `cn-beijing` 和 `cn-shanghai` 可用），其他地域 endpoint 将返回 403；  
- 免费额度仅限新用户首次开通后 30 天内使用，具体规则见 [产品计费](../../raw/model-user-guide/test-1.md)。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


