# Token

Token 是大语言模型处理文本的基本计量单位，也是百炼平台计费、监控和容量规划的核心度量。一个 Token 大致对应一个中文字或一个英文单词的一部分，模型的输入和输出均以 Token 数量衡量。

## 在百炼平台中的作用

Token 贯穿百炼平台的多个核心场景：

- **模型推理计费**：按量付费模式下，费用按输入/输出 Token 数量分别计算。部分模型实行阶梯计费，单价取决于单次请求的输入 Token 总量。
- **模型训练计费**：训练费用按训练 Token 总量乘以循环次数乘以训练单价计算。
- **模型部署容量**：TPM（Tokens Per Minute）是部署场景的核心容量单位，用于衡量模型每分钟可处理的 Token 吞吐量。
- **应用观测指标**：应用观测功能追踪每次调用的 Token 总量、输入 Token、输出 Token，以及平均首 Token 耗时等性能指标。
- **用量统计与监控**：模型监控面板以 Token 为维度统计大语言模型、全模态模型和向量模型的消耗量。
- **订阅套餐抵扣**：Token Plan 团队版以 Credits 统一计量，Credits 消耗由模型类型和 Token 用量共同决定。

## 计费相关参数

### 阶梯计费

部分模型的单价随单次请求输入 Token 总量变化。例如 qwen3-max 在 0\~32K、32K\~128K、128K\~256K 三个区间分别适用不同单价，输入越长单价越高。

### 缓存折扣

命中前缀缓存的输入 Token 按折扣系数消耗额度，不同模型折扣率不同（如千问系列 20%、DeepSeek-v4-Pro 8%）。通过 API 响应中的 `cached_tokens` 字段可确认缓存是否命中。

### 长输入阶梯系数

PTU 部署场景下，部分模型输入超过 32K Token 后按更高系数折算 TPM 消耗，例如 GLM-5.1 在 32K 以上输入时系数提升为输入 1.33 / 输出 1.17。

## 关键配置参数

| 参数 | 说明 |
|------|------|
| `max_tokens` | 限制单次生成的最大输出 Token 数，用于控制成本和响应长度 |
| TPM（输入/输出） | 部署或预留场景下分别设置输入和输出的每分钟 Token 吞吐量 |
| `cached_tokens` | API 响应字段，值大于 0 表示命中前缀缓存 |

## 降低 Token 成本的方式

- **Batch 调用**：输入/输出 Token 单价按实时推理价格的 50% 计费，适合非实时大批量任务。
- **上下文缓存**：重复前缀场景下命中缓存的输入 Token 享有折扣。
- **优化 Prompt**：简洁清晰的提示词可减少不必要的输入 Token 消耗。
- **按任务选模型**：简单任务优先使用轻量级模型，降低单次 Token 成本。
- **免费额度**：首次开通百炼时平台自动发放各模型免费推理额度（通常每个模型 100 万 Token），有效期 90 天。

## 监控与观测

在模型监控面板中，Token 相关的核心指标包括：

- **平均单次请求调用量**：衡量单次请求的平均 Token 消耗
- **Token 总量（输入/输出）**：应用观测中按时间粒度聚合的 Token 消耗趋势
- **首 Token 耗时**：流式场景下从请求发出到收到第一个输出 Token 的延迟
- **TPM 使用率**：部署场景下实际 Token 吞吐与预留容量的比值

## 关联主题页

- [test 1](../guides/test-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application monitoring](../guides/application-monitoring.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [model monitoring](../guides/model-monitoring.md)


