# Token

Token 是大语言模型处理文本的最小计量单位，模型将输入和输出文本切分为若干 Token 进行计算。在百炼平台中，Token 是模型调用计费、用量统计、容量规划和性能监控的核心度量单位。

## 在百炼平台中的使用场景

### 计费

Token 是模型推理和训练计费的基本单位：

- **按量计费**：模型调用按输入 Token 和输出 Token 分别计价。部分模型实行阶梯计费——单次请求的输入 Token 总量决定整笔请求适用的单价（例如 qwen3-max 分 0–32K、32K–128K、128K–256K 三档）。
- **Batch 调用**：输入和输出 Token 均按实时推理价格的 50% 计费。
- **上下文缓存**：缓存命中的输入 Token 按标准单价的 10% 计费，显式缓存创建按 125% 计费。
- **模型训练**：费用按训练数据 Token 总数 × 循环次数 × 单价计算；万相图像模型的 Token 总量由 max_steps × max_token_length 决定。
- **按 Token 用量部署**：LoRA 微调后的模型可部署为按输入/输出 Token 数计费的推理服务，最小计费单位为 1 Token。

费用抵扣优先级为：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费。

### 免费额度与订阅

- 新人免费额度通常为每模型 100 万 Token，有效期 90 天，仅抵扣华北2（北京）地域的实时推理费用。
- 资源包以预购 Token 数量的方式抵扣单个特定模型的实时推理用量。
- Token Plan 订阅服务以 Credits 为统一计量单位（底层仍按 Token 消耗折算），采用 5 小时 + 7 天双层窗口限额（个人版）或月度总额度制（团队版）。

### 容量与吞吐（TPM）

TPM（Tokens Per Minute）是衡量推理吞吐能力的单位：

- **预置吞吐（PTU）**：按输入/输出 kTPM 预留专属容量，超出最长输入 Token 或 TPM 容量时按溢出策略处理（自动转按量付费或返回 429）。长输入场景下超出 32K 的部分按阶梯系数（如 1.33）折算 TPM 消耗。
- **TPM 预留**：独立的高速推理方案，锁定专属吞吐量以规避公共限流，按每 10,000 TPM 日预付费计价。
- **PD 分离模式**：将首 Token 计算（Prefill）与后续 Token 计算（Decode）拆分到不同节点，降低首 Token 延迟、提高吞吐。

### 监控与观测

- **模型用量统计**：按[业务空间](workspace.md)维度汇总 Token 消耗，支持按 [API Key](api-key.md)、模型、时间范围筛选，数据延迟约 1 小时。
- **模型监控**：提供平均单次请求 Token 量、首 Token 延时、非首 Token 延时等性能指标；支持设置 Token 消耗阈值告警。
- **应用观测**：端到端追踪应用调用链路中的 Token 总量（全部/输入/输出），支持按 Span 筛选 Token 相关字段。
- **推理日志**：记录每次调用的 Token 用量明细，需开通后方可查看。

## 关键参数与字段

| 参数/字段 | 说明 |
| --- | --- |
| `usage.input_tokens` / `usage.output_tokens` | API 响应中返回的本次调用输入/输出 Token 数 |
| `cached_tokens` | 前缀缓存命中的 Token 数，可用于确认缓存是否生效 |
| `provisioned_tokens` | PTU 部署下折算后实际消耗的额度 Token 数（含阶梯系数和缓存折扣） |
| `service_tier` | 值为 `ptu-standard` 表示使用 PTU 额度，`default` 表示按量计费 |
| `max_tokens` | 请求参数，限制模型单次生成的最大输出 Token 数 |

## 成本优化建议

- 利用上下文缓存降低重复前缀的输入 Token 费用（命中后仅需 10% 单价）。
- 对延迟不敏感的任务使用 Batch 调用享受半价。
- 通过模型监控设置 Token 消耗告警，及时发现异常用量。
- 使用预置吞吐额度计算器，根据 RPM、平均输入/输出长度和缓存命中率估算所需 TPM，避免容量不足导致请求溢出为按量计费。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [fine tuning](../guides/fine-tuning.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)



