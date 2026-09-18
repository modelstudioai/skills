# support

`support` 是百炼平台为模型调用和服务使用提供的综合支持能力，涵盖模型兼容性、功能覆盖、参数配置及服务边界说明。开发者可通过该模块快速确认所用模型是否受支持、了解关键调用约束，并获取售后与合规依据。所有支持范围均以官方文档为准，建议结合具体模型文档交叉验证。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，覆盖通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型（需通过百炼控制台开通）。功能支持包括同步推理、流式响应、Function Calling、多模态输入（图像/音频）等，但具体能力因模型而异——例如 Qwen-VL 支持图像理解，而 Qwen1.5-7B 不支持视觉输入。> **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注“已下线”的模型不可用于新部署，但存量应用仍可调用至生命周期结束。

## 关键参数

调用 `support` 相关接口或配置服务时，以下参数影响支持行为：
- `model`: 必填，必须为 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确列出的模型标识符；
- `enable_stream`: 控制是否启用[流式输出](../concepts/streaming-output.md)，仅对支持流式的模型生效（参见各模型详情页）；
- `max_tokens`、`temperature` 等通用参数受模型自身能力限制，超出范围将返回 400 错误。

## 使用方式

1. 在百炼控制台「模型服务」中选择目标模型，点击「调试」或「部署」；
2. 调用 `/v1/chat/completions` 或 `/v1/embeddings` 等标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)时，`model` 字段需严格匹配支持列表；
3. 售后问题排查请优先查阅 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)，其中包含高频报错码（如 `ModelNotSupported`、`QuotaExceeded`）的根因与解决路径。

## 限制和注意事项

- 单次请求最大上下文长度、输出 token 数、并发数等硬性限制由模型本身决定，不因 `support` 配置改变；
- 非列表内模型（含自定义 Hugging Face 模型）默认不受 `support` 保障，无法享受 SLA、自动扩缩容及官方故障响应；
- [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确界定免费支持范围（如 5×8 小时工单响应），超出部分需按企业服务协议执行；
- > **注意**：[相关协议](../../raw/model-user-guide/support/related-agreements.md) 中关于数据归属与模型输出权责的条款优先级高于本页说明，调用前务必审阅。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


