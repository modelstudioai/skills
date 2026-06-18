# Token（令牌）

Token 是大语言模型处理文本的基本计量单位，模型将输入文本拆分为 Token 序列进行理解和生成。在百炼平台中，Token 既是模型推理的计算单元，也是计费、监控和容量规划的核心度量。

## 基本概念

Token 并非直接等同于字符或词语。对于中文，一个汉字通常对应 1-2 个 Token；对于英文，一个常见单词通常为 1 个 Token。百炼平台的 100 万 Token 上下文约相当于 70 万汉字或 10 本小说。模型的输入和输出都以 Token 计量，分别称为输入 Token 和输出 Token。

## 计费中的 Token

百炼平台的模型推理按量付费以 Token 为核心计费单位，不同模型和场景的 Token 单价差异显著：

- **文本生成模型**：按输入/输出 Token 数量分别计价。例如 qwen3.7-max 输入 12 元/百万 Token、输出 36 元/百万 Token；qwen3.6-flash 等轻量模型单价更低。
- **阶梯计费**：部分模型根据单次请求的输入 Token 总量实行阶梯定价，输入越长单价越高。例如 qwen3-max 在 0-32K 范围为 2.5 元/百万 Token，128K-256K 范围升至 7 元/百万 Token。
- **模型训练**：训练费用按训练 Token 计算，公式为（训练数据 Token + 混合训练数据 Token）x 循环次数 x 训练单价。
- **Batch 调用**：支持 Batch 的模型，批量推理价格为实时推理的 50%。
- **上下文缓存**：缓存命中的输入 Token 可享受折扣（如 Qwen 系列按 20% 折算，deepseek-v4-pro 按 8% 折算），与 Batch 调用不可同时生效。

## 用量监控中的 Token

百炼的模型监控体系围绕 Token 提供多维度的可观测能力：

- **用量统计**：按[业务空间](workspace.md)维度统计各模型的 Token 消耗，支持按模型类型和时间范围筛选，数据延迟约 1 小时。
- **性能指标**：包括首 Token 延时（TTFT）、每 Token 生成耗时、每分钟 Token 吞吐量（TPM）等关键指标。
- **告警机制**：可对 Token 消耗突增等异常设置主动告警，通过短信、邮件、钉钉等渠道通知。
- **Prometheus 集成**：高级监控数据支持通过标准 Prometheus API 接入 Grafana 等外部系统，核心指标包括 `model_usage`（Token 用量总和）等。

不同模态的模型使用不同计量单位：文本生成、视觉理解、向量模型按 Token 计量；图像按张、视频按秒、语音按秒/字符/Token 计量。视觉模型的图像 Token 消耗公式为 `h x w / (32 x 32) + 2`。

## 容量规划中的 Token

TPM（Tokens Per Minute）是百炼容量规划的关键参数：

- **TPM 预留**：为指定模型锁定专属 TPM 吞吐量，按 kTPM 预付费，确保业务高峰不受公共资源限流。超出预留容量的请求自动降级为按量计费。
- **容量计算**：控制台提供容量计算器，根据 RPM、平均输入/输出 Token 长度和缓存命中率估算所需 TPM。
- **RPM/TPM 限流**：按量付费模式下共享公共资源池，存在 RPM 和 TPM 上限，高峰期可能被限流。

## Token Plan 套餐

百炼提供基于 Token 的订阅制套餐：

- **Token Plan 团队版**：以 Credits 统一计量 Token 消耗，支持多模型灵活切换，提供标准/高级/尊享三档坐席（25,000-250,000 Credits/月）。
- **Coding Plan**：面向个人开发者，按调用次数计费，有频次上限（每 5 小时 6,000 次）。

## 开发者实践建议

- **控制输出长度**：合理设置 `max_tokens` 参数限制单次生成的 Token 数量，控制成本。
- **优化 Prompt**：简洁清晰的提示词可减少不必要的输入 Token 消耗。
- **选择合适模型**：简单任务优先使用轻量模型（如 Flash/Turbo 系列），避免过度使用高价模型。
- **利用缓存**：对重复前缀的请求启用上下文缓存，降低输入 Token 的有效计费量。
- **批量处理**：非实时场景使用 Batch 调用，Token 单价降低 50%。
- **监控用量**：配置 Token 消耗告警，及时发现异常消耗并优化。

## 关联主题页

- [test 1](../guides/test-1.md)
- [model inference](../guides/model-inference.md)
- [model monitoring](../guides/model-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [token plan guide](../guides/token-plan-guide.md)
- [more about models](../api/more-about-models.md)


