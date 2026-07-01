# Token

Token 是大语言模型处理文本的基本计量单位，代表模型将输入文本分词后的最小语义片段。在百炼平台中，Token 既是模型推理的[计费](billing.md)基础，也是吞吐量（TPM）、用量监控和容量规划的核心度量。

## 什么是 Token

Token 是模型对文本进行分词（tokenization）后产生的基本单元。一个 Token 可能是一个汉字、一个英文单词或单词的一部分。不同模型的分词器实现不同，同一段文本在不同模型下产生的 Token 数可能有差异。百炼平台按输入 Token 和输出 Token 分别计量和[计费](billing.md)。

## 在百炼平台的使用场景

### [计费](billing.md)计量

Token 是百炼按量付费的核心计量单位：

- **文本生成模型**：按输入 Token 和输出 Token 分别计费，部分模型实行阶梯计费
- **向量模型**：按输入文本的 Token 数计费
- **模型训练**：训练费用 = Token 总数 x 循环次数 x 训练单价
- **全模态模型**：文本与其他模态均按 Token 数计费

同一模型的账单可能因输入 Token、输出 Token、缓存命中等类型分别出账。

### 吞吐量与容量规划

TPM（Tokens Per Minute）是衡量模型推理吞吐能力的指标，1 kTPM = 1,000 Tokens/分钟。在 TPM 预留和 PTU 部署中，需分别配置输入 TPM 和输出 TPM：

- **容量计算器**：根据 RPM、平均输入/输出长度、缓存命中率推算所需 TPM
- **长输入阶梯系数**：部分模型超过特定长度（如 32K）的输入按更高系数折算 TPM 消耗
- **前缀缓存折扣**：命中缓存的输入 Token 按折扣系数消耗额度（如 0.2 或 0.08）

### 用量监控

百炼模型监控提供多层次的 Token 追踪能力：

- **汇总统计**：按[业务空间](workspace.md)维度查看历史 Token 消耗，支持按 [API Key](api-key.md) 和时间范围筛选
- **单次追踪**：记录每次模型调用的 Token 消耗明细（需开通推理日志）
- **应用观测**：查看应用级 Token 总量（输入/输出），支持分钟/小时/天粒度聚合
- **告警**：设置 Token 消耗阈值，异常时主动通知

### 订阅服务中的 Token

- **Token Plan 团队版**：以 Credits 统一计量 Token 消耗，按坐席订阅
- **资源包**：预购固定 Token 数量抵扣特定模型的推理用量
- **抵扣优先级**：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费

## 关键参数与配置

| 参数 | 说明 |
| --- | --- |
| 输入 Token | 请求中发送给模型的 Token 数量 |
| 输出 Token | 模型生成响应的 Token 数量 |
| cached_tokens | API 响应中返回的缓存命中 Token 数 |
| TPM（input/output） | 每分钟可处理的输入/输出 Token 数，容量规划核心指标 |
| max_tokens | 单次请求允许的最大输出 Token 数 |

## 开发者注意事项

- 模型输入超过最长输入 Token 限制时，PTU/TPM 预留调用将自动切换为按量付费
- 用量数据按[业务空间](workspace.md)维度统计，不支持按阿里云账号维度汇总
- 不同模型分词器不同，建议通过 API 返回的 usage 字段获取实际 Token 数
- 控制台用量数据延迟约 1 小时，以账单为最终计费依据

## 关联主题页

- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [token plan guide](../guides/token-plan-guide.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)


