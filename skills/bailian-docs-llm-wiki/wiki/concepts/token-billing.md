# Token 与计费

Token 是百炼平台衡量模型处理文本量的基本单位，也是绝大多数计费、限流和用量统计的计量基础；平台的费用则围绕 Token 消耗，通过按量付费、免费额度、节省计划与资源包等机制综合结算。理解 Token 如何被计量与抵扣，是控制大模型使用成本的前提。

## Token 在计费中的角色

对大语言模型、全模态模型和向量模型，用量与费用均按 **Token** 计量；图像生成按「张」、视频生成按「秒」、语音模型按「秒/字符/Token」（视模型而定）。因此谈「计费」时，Token 主要针对文本类调用。

模型调用按**输入 Token** 和**输出 Token** 分别计费，单价以「每百万 Token」为单位。部分模型采用**阶梯计费**：按单次请求的输入 Token 总量分档定价，落入某一区间后该请求全部 Token 按对应档位结算（例如 `qwen3-max` 华北2·北京划分为 `0<Token≤32K`、`32K<Token≤128K`、`128K<Token≤256K` 三档）。

## 不同场景中的 Token 与费用

### 1. 实时推理（模型调用）

默认按量付费。发生调用时系统按固定优先级自动抵扣，无需手动设置：

**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**

- **免费额度**：首次开通时各模型自动发放（通常每模型 100 万 Token），仅抵扣实时推理，不抵扣 Batch、调优、部署；不同模型（含同一模型不同快照版本）额度相互独立。开启「免费额度用完即停」后，额度耗尽会停止响应并返回 `AllocationQuota.FreeTierOnly`（或 403），避免意外扣费。
- **折扣**：Batch 调用输入/输出单价按实时推理价的 50% 计费；支持上下文缓存的模型仅输入 Token 享折扣，两者不能同时生效。
- **地域差异**：同一模型在不同地域单价不同，境外地域通常无免费额度。

### 2. 模型训练（调优）

按训练 Token 计费。文本模型公式为 `(训练数据 Token + 混合数据 Token) × 循环次数 × 训练单价`；图像/视频生成模型的训练 Token 总量由 `max_steps`、`max_pixels`、`n_epochs` 等超参决定。免费额度和节省计划**均不抵扣**训练费用。

### 3. 模型部署

免费额度和节省计划同样**不抵扣**部署费用。三种计费方式围绕 TPM（每分钟 Token 数）：

- **预置吞吐（PTU）**：`费用 = 使用时长 × (输入 TPM 单价 × 输入 TPM + 输出 TPM 单价 × 输出 TPM)`。PTU 下超出购买吞吐或输入超上限时自动转按量付费（响应头 `x-dashscope-ptu-overflow:true`）。长输入按阶梯系数折算 TPM 消耗，命中前缀缓存的 Token 按折扣系数消耗额度。
- **模型单元（MU）**：`费用 = 使用时长 × 模型单元数量 × 模型单元单价`。
- **按 Token 使用量**：仅对 LoRA 微调后的自定义模型开放，用于调优效果验证。

### 4. 订阅套餐（Token Plan / Coding Plan）

- **Token Plan 团队版**：按 Token 消耗抵扣 Credits，面向团队协作。
- **Coding Plan**：按模型调用次数计量，面向个人开发。

两者均使用 `sk-sp-` 前缀的**专属 API Key**，**不消耗新人免费额度**，且 Base URL 与按量付费端点完全隔离，混用会导致意外扣费或 401/403 鉴权失败。

### 5. 监控与用量统计

模型监控将 Token 消耗归入「成本」类指标，并提供首 Token 延时、RPM/TPM 等性能指标。应用观测则可查看每次调用的输入/输出/平均 Token 量与平均首 Token 耗时。开通推理日志后可查看单次调用的 Token 消耗，用于排查与审计。

## 关键参数与配置

- **`max_tokens`**：限制单次生成的最大输出 Token 数，是控制输出成本和防止过度生成的首要手段。
- **TPM / RPM 限流**：部署时可配置 `tpm_limit`、`rpm_limit`；触发限流后等待时间取决于限流值。
- **PTU 计费识别字段**：`service_tier`（`ptu-standard` 走 PTU 额度，`default` 或缺失表示按量）、`provisioned_tokens`（折算后实际消耗额度）、`cached_tokens`（缓存命中数，Anthropic 兼容格式暂不返回）。这些字段在 OpenAI Chat、OpenAI Responses、Anthropic 兼容、DashScope 四种协议下 JSON 路径不同，需按协议读取。

## 成本优化与出账

- **节省 Token**：优化 Prompt 减少输入 Token、简单任务选用轻量级模型、非实时任务走批量推理、合理设置 `max_tokens`。
- **预付费方案**：AI 通用型节省计划（承诺月消费换阶梯折扣，最高 5.3 折，月额度不可跨月累积）、其他模型节省计划、资源包（预购具体 Token/图片数量，仅抵扣单个模型超免费额度后的实时推理）。
- **出账时效**：大模型推理分钟级出账（约 2～10 分钟）；批量推理、模型训练等小时级出账。用量统计数据约 1 小时延迟，且不支持查看 30 天前数据。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [support](../guides/support.md)
- [model deployment 1](../guides/model-deployment-1.md)




