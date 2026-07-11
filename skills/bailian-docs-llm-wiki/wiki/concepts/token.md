# Token 计量

Token 是百炼平台中衡量模型输入与输出文本量的基本计量单位，是计费、监控、容量规划的核心度量。百炼平台的大语言模型按输入 Token 和输出 Token 分别计价，不同模型、不同场景下的 Token 单价和换算规则各有差异。

## 什么是 Token

Token 是大语言模型处理文本的最小片段。一个 Token 通常对应一个汉字、一个英文单词或子词。模型在推理时先将输入文本拆分为 Token 序列，逐 Token 生成输出。Token 数量直接决定了调用费用和上下文窗口的使用量。

对于非文本模态，Token 也作为统一计量单位：

- **图像理解**：Token 数按 `h x w / (32 x 32) + 2` 公式换算，与图像分辨率成正比。
- **向量模型**：Embedding 操作按向量化的 Token 数计费。
- **语音模型**：部分语音模型也以 Token 作为计量单位（另有按秒、按字符计量的模型）。

## 计费中的 Token

百炼平台模型推理采用按量付费模式，输入 Token 和输出 Token 分别计价。以千问系列为例：

| 模型 | 输入单价（每百万 Token） | 输出单价（每百万 Token） |
|------|--------------------------|--------------------------|
| qwen3.7-max | 12 元（限时 5 折） | 36 元（限时 5 折） |
| qwen3-max（0-32K） | 2.5 元 | 10 元 |
| qwen-plus（0-128K） | 0.8 元 | 非思考 2 元 / 思考 8 元 |

关键计费规则：

- **阶梯计费**：部分模型的单价由单次请求的输入 Token 总量决定，所有 Token 按落入的阶梯统一结算。
- **Batch 推理折扣**：支持 Batch 调用的模型，输入和输出单价均为实时推理的 50%。
- **上下文缓存折扣**：支持上下文缓存的模型，命中缓存的输入 Token 按折扣系数计费（如 DeepSeek-v4-Pro 缓存折扣 8%，千问系列 20%）。Batch 折扣与缓存折扣不能同时生效。
- **思考模式**：开启 `enable_thinking` 后，模型的思考过程也会产生输出 Token，计入费用。

## 免费额度

首次开通百炼时，平台自动发放新人免费额度（通常每个模型 100 万 Token），有效期 90 天。免费额度仅限华北2（北京）地域，仅抵扣实时推理费用。主账号与 RAM 子账号共享同一模型的免费额度，不同模型的额度相互独立。

## 模型训练中的 Token

模型训练按训练 Token 计费，公式因模型类型而异：

- **文本生成模型**：费用 =（训练数据 Token + 混合训练数据 Token）x 循环次数 x 训练单价。
- **图像/视频生成模型**：训练 Token 总量由 max_steps、max_token_length、视频时长等参数决定。

## 模型部署中的 Token

模型部署提供三种与 Token 相关的计费方式：

- **预置吞吐（PTU）**：按 TPM（Tokens Per Minute）预留专属推理容量，超出部分自动转为按量付费。命中缓存的输入 Token 按折扣系数消耗额度。
- **模型单元（MU）**：按算力时长计费，支持 PD 分离模式降低首 Token 延迟。
- **Token 用量**：直接按输入/输出 Token 计费，仅支持部分 LoRA 调优后的模型。

## 监控与用量统计

百炼平台提供多维度的 Token 用量监控：

- **模型监控**：追踪平均单次请求 Token 消耗、TPM（Tokens Per Minute）、首 Token 延时等性能指标，支持按 API-KEY 和推理类型筛选。
- **应用观测**：查看应用调用链路中每个节点的 Token 消耗（输入/输出），包括 Token 总量趋势和平均单次请求 Token 量图表。
- **用量统计**：按[业务空间](workspace.md)维度统计 Token 用量，支持在控制台查看并管理免费额度。
- **告警**：可配置基于 Token 消耗的告警规则，异常时通过短信、邮件、钉钉等渠道通知。

## 成本优化实践

- **控制输出长度**：通过 `max_tokens` 参数限制单次生成的最大 Token 数，避免不必要的开销。
- **优化 Prompt**：简洁清晰的 Prompt 可减少输入 Token 消耗。
- **按任务选模型**：简单任务优先使用轻量级模型（如 flash 系列），Token 单价更低。
- **使用 Batch 推理**：非实时场景使用批量推理接口，Token 单价降至 50%。
- **利用上下文缓存**：多轮对话和重复前缀场景下，缓存命中可大幅降低输入 Token 费用。
- **购买节省计划或资源包**：通过 AI 通用型节省计划（最高 5.3 折）或预购 Token 资源包进一步降低成本。

## 关键参数速查

| 参数 | 说明 |
|------|------|
| `max_tokens` | 限制模型单次生成的最大输出 Token 数 |
| `input_tokens` | API 响应中返回的本次请求输入 Token 数 |
| `output_tokens` | API 响应中返回的本次请求输出 Token 数 |
| `cached_tokens` | 命中上下文缓存的输入 Token 数（大于 0 表示缓存生效） |
| `enable_thinking` | 开启思考模式，思考过程产生额外输出 Token |

## 关联主题页

- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model experience](../guides/model-experience.md)


