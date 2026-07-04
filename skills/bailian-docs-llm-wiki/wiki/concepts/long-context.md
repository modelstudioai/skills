# 长上下文

长上下文指模型在单次调用中能够接收并处理的输入 token 上限（部分模型还包含输出）。上下文窗口越大，单次请求可携带的对话历史、文档、图像、视频等数据越多，能减少多轮拼接与外部检索的复杂度。

## 在百炼平台中的使用场景

- **文本生成**：Qwen3.7-max / Qwen3.7-plus / Qwen3.6-flash 以及 deepseek-v4 系列均提供 1M token 上下文窗口，可在单轮内喂入长文档、长对话历史或多文件做总结、问答与代码调试。
- **视觉理解**：Qwen3.7-plus 等模型支持 1M 上下文，可接收最长 2 小时视频（2GB）或大段图文混合输入，进行视频内容分析与 OCR。
- **PTU 部署**：预置吞吐部署支持长输入（部分模型最高 200K token），通过阶梯容量系数折算 TPM，超出额度或输入超过模型上限时自动转为按量计费，业务不中断。
- **对话历史管理**：OpenAI 兼容 Responses 接口由平台自动维护对话历史，无需在请求中手动拼接 messages；其他接口需由调用方维护上下文长度与轮次，避免超出模型上下文窗口。

## 关键参数与配置

- **上下文长度**：按模型不同，常见档位为 32K / 64K / 128K / 200K / 1M。选型时确认目标模型在对应兼容接口下的实际上下文上限。
- **PTU 长输入阶梯系数**：超出 32K 的输入按更高系数折算 TPM。以 glm-5.1 为例，`[0, 32K)` 系数 1.0，`[32K, 200K]` 输入系数 1.33 / 输出 1.17。
- **前缀缓存折扣**：命中缓存的输入 token 按模型对应折扣折算容量（如 glm-5.1 为 0.2，deepseek-v4-pro 为 0.08）。
- **自动溢出阈值**：千问 128K、DeepSeek 64K 为模型上限阈值，超过即转按量计费，响应头返回 `x-dashscope-ptu-overflow: true`。
- **图像 token 计算**：视觉模型每张图片 token 数按 `h x w / (32 x 32) + 2` 估算，叠加在上下文总额内。

## 容量与额度评估

长输入场景下建议先用控制台的 PTU 容量计算器评估额度：根据每分钟请求数（RPM）、平均输入/输出长度、预估缓存命中率推算输入 TPM 和输出 TPM，避免意外转为按量计费。PTU 部署的响应包含以下与额度相关的字段：

- `service_tier`：`ptu-standard` 表示使用 PTU 额度；`default` 或不返回表示按量计费。
- `provisioned_tokens`：折算后实际消耗的 PTU 额度（含阶梯系数和缓存折扣）。
- `cached_tokens`：前缀缓存命中的 token 数。OpenAI Chat 兼容为 `usage.prompt_tokens_details.cached_tokens`；OpenAI Responses 为 `usage.input_tokens_details.cached_tokens`；Anthropic 兼容暂不返回。

## 限制与注意事项

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生全部参数；如需最全采样参数与插件能力，建议改用 DashScope 原生接口。
- **上下文窗口 ≠ 输出上限**：1M 上下文主要指输入侧，单次输出长度仍受模型自身限制，长输入场景需评估输出截断风险。
- **历史轮次管理**：迁移到不自动管理历史的接口时，需自行裁剪历史消息，避免累积超出窗口导致请求失败或尾部被截断。
- **跨接口迁移**：从 OpenAI / Anthropic 迁移时应先确认目标 Qwen 模型在对应兼容接口下是否支持所需上下文长度与参数（如 `temperature`、`tools`、`stream` 等），再决定接口选型。
- **地域差异**：各地域（北京、新加坡、弗吉尼亚）的 API Key 不互通，长上下文模型的可用性可能与地域相关，部署类操作仅适用于华北2（北京）地域。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)
- [model deployment 1](../guides/model-deployment-1.md)


