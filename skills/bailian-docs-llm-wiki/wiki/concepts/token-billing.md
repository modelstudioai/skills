# Token 计费

Token 计费是百炼平台的核心计量与计费机制：模型的推理、训练等用量以 Token（文本的最小计量单位）为口径分别统计输入与输出，并按各模型单价结算费用。开发者关心的"调用花多少钱、如何抵扣、如何查账"几乎都围绕 Token 计费展开。

## 在不同场景中的使用

### 模型推理（调用）

- 默认按量付费，**输入 Token 与输出 Token 分别计价**，最小计费单位 1 Token，出账粒度约分钟级（2~10 分钟）。
- **阶梯计费**：部分模型单价取决于单次请求的输入 Token 总量，整个请求的所有 Token 均按落入区间的单价结算（如输入 100K 落入 `32K<Token≤128K` 档则全部按该档计价）。
- **Batch 调用半价**：支持 Batch 的模型输入/输出单价为实时推理的 50%，但不与上下文缓存折扣叠加。
- **上下文缓存**：显式缓存创建按标准输入单价的 125% 计费，命中按 10% 计费。
- **思考模式**：部分模型（如 qwen-plus 系列）思考模式输出单价更高，思维链 Token 计入输出 Token。
- **地域差异**：同一模型在北京、新加坡、弗吉尼亚等地域单价不同，北京地域通常最低且才有免费额度。

### 模型训练（调优）

训练按训练 Token 计费：千问文本/VL 模型为 `（训练数据 Token + 混合训练数据 Token）× 循环次数 × 训练单价`；万相图像/视频模型按公式折算 Token 总量或计费时长，出账为小时级。

### 模型部署

- **按 Token 用量部署**：仅部分 LoRA 调优后模型支持，`费用 = 输入 Token 数 × 输入单价 + 输出 Token 数 × 输出单价`，不使用不计费，一个月不用自动释放。
- **预置吞吐（PTU）**：虽按时长计费，但额度以 TPM（每分钟 Token 数）折算消耗——长输入（超 32K）按更高系数折算，命中前缀缓存的输入按折扣系数（如 0.08~0.2）消耗；「自动溢出」策略下超额请求转按量 Token 计费（响应头 `x-dashscope-ptu-overflow:true`），「仅使用 PTU 容量」则返回 429。

### 订阅类产品

Token Plan / Coding Plan 以 Credits 统一计量而非直接按 Token 计价，其专属 API Key（`sk-sp-` 开头）**不消耗免费额度**；与通用按量付费 Key 混用会导致鉴权失败或意外走按量 Token 计费通道。

## 抵扣与优惠

费用抵扣优先级固定：**免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费**，系统自动按序抵扣。

- **新人免费额度**：通常每模型 100 万 Token，有效期 90 天，仅抵扣实时推理，不抵扣 Batch、调优、部署；不同模型（含快照版本）额度相互独立。可开启"免费额度用完即停"，耗尽时返回 `AllocationQuota.FreeTierOnly`（403）。
- **资源包**：预购特定模型的 Token 量，仅抵扣该模型超出免费额度后的实时推理用量。
- **节省计划**：AI 通用型节省计划按承诺月消费换阶梯折扣（最高 5.3 折），可抵扣模型调用、上下文缓存、批量推理等按量 Token 费用，不抵扣调优/部署。

## 用量查询与监控

- **模型用量页面**：按[业务空间](workspace.md)统计各模型 Token 消耗与费用，数据延迟约 1 小时，仅保留 30 天；文本/思考/视觉理解/向量模型按 Token 统计，图像按张、视频按秒。
- **模型监控**：成本类指标含平均单次请求调用量与 Token 消耗；开通推理日志后可查看单次调用的 Token 用量、请求与响应内容（分钟级延迟，仅记录开通后的调用）。
- **高级监控 / Prometheus**：可通过 `model_usage` 等指标接入 Grafana，按 `workspace_id`、`model`、`apikey_id` 等维度分析 Token 消耗。
- **应用观测**：应用维度可查看 Token 总量、输入/输出 Token、平均单次请求 Token 量、平均首 Token 耗时等指标，并支持按 Token 量筛选 Span。

## 关键参数与注意事项

| 项目 | 说明 |
| --- | --- |
| `model` 参数 | 免费额度按模型（含快照版本）隔离，用完不自动切换，需手动更换 |
| `service_tier` / `provisioned_tokens` / `cached_tokens` | PTU 场景响应字段：是否走 PTU 额度、折算后额度消耗、缓存命中 Token 数 |
| `x-dashscope-ptu-overflow` | 响应头为 `true` 表示该请求已溢出到按量 Token 计费 |
| `AllocationQuota.FreeTierOnly` | 开启"用完即停"后免费额度耗尽的报错码 |

常见误区：模型部署（PTU/模型单元）按时长计费，**部署为"运行中"即持续扣费，与是否有 Token 调用无关**，这是"没调用也产生费用"的最常见原因；不再使用务必删除部署任务。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [model deployment 1](../guides/model-deployment-1.md)


