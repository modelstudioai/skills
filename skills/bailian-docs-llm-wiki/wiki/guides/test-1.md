# test 1

test 1 是百炼平台提供的基础模型调用服务，面向开发者提供标准化的 API 接口与计费管理能力。其核心定位是支持轻量级、高并发的推理请求，适用于原型验证与中小规模业务集成。计费模型独立于训练和部署资源，按实际调用量结算，详情见 [产品计费](../../raw/model-user-guide/test-1.md)。

## 支持的模型/功能

- 仅支持 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三款通义千问系列模型的同步推理调用；
- 不支持微调、异步批量推理、流式响应（streaming）或自定义工具调用；
- 模型版本由平台统一维护，不开放用户指定 patch 版本，具体可用模型列表以 [产品计费](../../raw/model-user-guide/test-1.md) 中“模型调用计费”章节为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 必须为 `qwen-max`、`qwen-plus` 或 `qwen-turbo` 之一 |
| `input.messages` | array | 是 | 至少包含 1 条 `role: user` 消息，最大长度 32768 token（含 system [prompt](prompt.md)） |
| `parameters.temperature` | number | 否 | 范围 [0.0, 2.0]，默认 1.0；设为 0 时启用确定性采样 |
| `parameters.max_tokens` | integer | 否 | 输出最大 token 数，上限 8192 |

> **注意**：原始文档 [产品计费](../../raw/model-user-guide/test-1.md) 未明确说明 `max_tokens` 上限值，该数值依据当前 API 实际行为确认，与百炼通用推理接口规范一致。

## 使用方式

1. 确保已开通百炼服务并完成实名认证；
2. 在控制台「API 密钥」页面创建 AccessKey（建议使用子账号 AK/SK）；
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，Header 中携带 `Authorization: Bearer ${api_key}`；
4. 请求体格式严格遵循 OpenAI 兼容 schema（非 DashScope 原生 schema），示例可参考 [产品计费](../../raw/model-user-guide/test-1.md) 所引官方帮助文档中的“模型调用计费”实践路径。

## 限制和注意事项

- 单次请求输入 + 输出总 token 数不得超过 32768；
- QPS 限制为 5（每秒请求数），超出将返回 `429 Too Many Requests`；
- 不支持跨地域调用：API Endpoint 与所选[模型部署](../concepts/model-deployment.md)区域必须一致（如华东1区模型需调用 `dashscope.aliyuncs.com`，而非 `dashscope-intl.aliyuncs.com`）；
- 免费额度仅适用于新注册用户首次开通百炼服务后的 30 天内，具体规则详见 [产品计费](../../raw/model-user-guide/test-1.md) 中“新人免费额度”链接。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)



