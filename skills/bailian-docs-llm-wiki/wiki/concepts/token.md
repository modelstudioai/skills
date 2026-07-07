# Token 计量

Token 是百炼平台中衡量文本处理量的基本单位，用于模型推理计费、用量统计、吞吐量管理等核心场景。一个 Token 大致对应一个中文字或一个英文单词片段，实际切分由模型的分词器决定。

## 计费中的 Token

百炼平台的模型推理默认按量付费，核心计费维度就是输入 Token 和输出 Token：

- **输入 Token**：发送给模型的 [prompt](../guides/prompt.md)、上下文、系统指令等文本经分词后的 Token 总量。
- **输出 Token**：模型生成的回复文本对应的 Token 总量。
- **思考 Token**：部分模型（如开启深度思考模式）会产生额外的思考过程 Token，可能按独立单价计费。

不同模型的输入/输出单价差异较大。以千问系列为例，qwen3-max 在 32K 以内输入单价为 2.5 元/百万 Token，输出为 10 元/百万 Token；超过 32K 后阶梯上升。部分模型还支持 Batch 调用（输入输出均半价）和上下文缓存（输入 Token 享折扣），两者不可同时生效。

模型训练同样按 Token 计费，费用等于训练数据 Token 总量乘以循环次数再乘以训练单价。

## Token 与用量统计

百炼按[业务空间](workspace.md)维度统计 Token 消耗，开发者可在控制台的**模型用量**页面查看各模型的 Token 用量汇总，数据延迟约 1 小时。不同模型类型的统计单位有所不同：

| 模型类型 | 统计单位 |
|---------|---------|
| 大语言模型（文本生成/深度思考/视觉理解） | Token |
| 全模态模型 | Token |
| 向量模型 | Token（按输入文本） |
| 语音模型 | 秒、字符或 Token（视模型而定） |
| 图像生成模型 | 张 |
| 视频生成模型 | 秒 |

如需账号级 Token 总量，需在费用与成本页面导出账单查看。

## 应用观测中的 Token 追踪

在应用观测功能中，每次调用的 Token 消耗会被自动采集并展示，包括：

- Token 总量（全部/输入/输出）
- 平均单次请求 Token 量
- 平均首 Token 耗时（流式场景下衡量响应速度的关键指标）

开发者可按 Token 总量、输入 Token、输出 Token 等字段筛选调用记录，快速定位高消耗请求。

## 模型监控中的 Token 管理

模型监控提供分钟级的 Token 追踪能力，在成本类监控指标中可查看平均单次请求调用量。结合 TPM（Tokens Per Minute）指标，开发者能评估模型的吞吐消耗趋势，及时发现异常用量。

## TPM 预留与吞吐管理

TPM（Tokens Per Minute）是衡量模型推理吞吐量的核心指标。百炼支持 TPM 预留功能，开发者可为指定模型锁定专属吞吐量。影响实际 Token 容量消耗的关键参数包括：

- **缓存折扣**：命中缓存的输入 Token 按折扣系数消耗容量，不同模型折扣率不同（如千问系列 20%、DeepSeek-v4-Pro 8%）。
- **长输入阶梯系数**：部分模型在输入超过一定长度后，Token 容量消耗系数会提升。

## Token Plan 订阅套餐

百炼提供 Token Plan 团队版和 Coding Plan 两类订阅套餐，以 Credits 或调用次数统一计量。Token Plan 中，Credits 消耗由模型类型、Token 用量、思考模式及工具调用等因素共同决定。套餐的抵扣顺序为：坐席月度额度 > 共享用量包 > 服务暂停。

## 成本优化建议

- **善用免费额度**：开通百炼时自动发放的免费额度可抵扣模型实时推理的 Token 费用，有效期 30~90 天。
- **选择合适的节省计划**：AI 通用型节省计划通过承诺月消费金额换取 Token 单价折扣，最高 5.3 折。
- **利用上下文缓存**：重复的系统提示或长上下文可通过缓存降低输入 Token 费用。
- **关注阶梯计费**：输入 Token 超过一定阈值后单价上升，合理控制上下文长度有助于降低成本。
- **开启用完即停**：避免免费额度耗尽后产生意外的 Token 扣费。

## 关联主题页

- [test 1](../guides/test-1.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [qwen api reference](../api/qwen-api-reference.md)


