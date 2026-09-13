# test 1

test 1 是百炼平台提供的基础模型调用服务，面向开发者提供标准化的 API 接口与计费管理能力。该服务支持按量付费与资源包两种结算模式，适用于低频调试、轻量级推理等场景。详细计费规则和成本控制手段请参考 [产品计费](../../raw/model-user-guide/test-1.md) 文档。

## 支持的模型/功能  
- 当前仅支持调用 `qwen-max` 和 `qwen-plus` 等在线推理模型（不支持自定义训练或微调）；  
- 提供同步 `chat` 接口，支持流式响应（`stream=true`）；  
- 不支持图像、音频等[多模态](../concepts/multi-modal.md)输入，纯文本输入输出。完整能力边界参见 [产品计费](../../raw/model-user-guide/test-1.md) 中关于“模型调用计费”的说明。

## 关键参数  
- `model`: 必填，取值为 `qwen-max` 或 `qwen-plus`；  
- `max_tokens`: 可选，默认 2048，最大支持 8192；  
- `temperature`: 可选，范围 [0.0, 2.0]，默认 1.0；  
- `top_p`: 可选，范围 [0.0, 1.0]，默认 1.0；  
- 其他参数（如 `stop`, `repetition_penalty`）暂不生效，以 [产品计费](../../raw/model-user-guide/test-1.md) 所列为准。

## 使用方式  
1. 在控制台开通 Model Studio 服务并完成实名认证；  
2. 获取 API Key（需在「API 密钥管理」中创建）；  
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，Header 中携带 `Authorization: Bearer <api_key>`；  
4. 请求体为标准 JSON，示例详见 [产品计费](../../raw/model-user-guide/test-1.md) 的附录调用示例节（注：该文档未提供完整代码示例，建议同步查阅官方 SDK 文档）。

## 限制和注意事项  
- 单次请求最大输入 tokens 为 4096，超出将返回 `400 Bad Request`；  
- 每分钟调用次数（QPM）默认上限为 60，可通过工单申请提升；  
- > **注意**：原始文档中“模型调用计费”链接指向帮助中心页面，但其中 `qwen-turbo` 的定价描述已过时——该模型在 test 1 服务中不可用，实际仅支持 `qwen-max` 和 `qwen-plus`；  
- 账单按小时出账，延迟不超过 2 小时，可通过「账单查询与成本管理」模块实时监控用量；  
- 免费额度仅限新用户首月使用，具体规则以 [产品计费](../../raw/model-user-guide/test-1.md) 中「新人免费额度」章节为准。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


