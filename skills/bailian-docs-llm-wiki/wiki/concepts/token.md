# Token

Token 是大语言模型处理文本的基本计量单位，也是百炼平台模型调用[计费](billing.md)的核心度量。模型在推理时将输入文本拆分为 Token 序列进行处理，并以 Token 为单位生成输出；平台据此分别统计输入 Token 和输出 Token 的消耗量，作为[计费](billing.md)依据。

## 基本概念

在大语言模型中，Token 并非严格对应一个汉字或一个英文单词。对于中文文本，一个 Token 通常对应 1-2 个汉字；对于英文文本，一个 Token 大约对应 3-4 个字符。模型的上下文窗口大小（如 32K、128K、256K）同样以 Token 为单位衡量。

百炼平台将 Token 分为两类进行独立计量：

- **输入 Token**：用户发送给模型的 Prompt、系统指令、历史对话等内容所消耗的 Token 数量。
- **输出 Token**：模型生成的回复文本所消耗的 Token 数量。

## Token 与[计费](billing.md)

百炼平台对文本生成类模型按输入和输出 Token 分别计价，不同模型的单价差异较大。以千问系列为例：

| 模型 | 输入单价（每百万 Token） | 输出单价（每百万 Token） |
|------|------------------------|------------------------|
| qwen3.7-max | 12 元 | 36 元 |
| qwen3.7-plus | 2 元 | 8 元 |
| qwen3.6-flash | 更低 | 更低 |

关键计费规则：

- **阶梯计费**：部分模型（如 qwen3-max、qwen-plus）按单次请求的输入 Token 总量所在区间确定单价，同一请求内所有 Token 按对应阶梯统一结算。
- **Batch 调用优惠**：支持 Batch 的模型，输入和输出 Token 单价均为实时推理的 50%。
- **上下文缓存折扣**：命中缓存的输入 Token 可享受折扣（如缓存命中部分按 20% 折算），但与 Batch 调用互斥。
- **免费额度**：新用户开通百炼时自动获得各模型的免费 Token 额度，有效期 30-90 天。

其他模型类型的计量单位有所不同：图像生成按张数计费，视频生成按秒数计费，语音模型视情况按时长、字符数或 Token 数计费。

## Token 消耗监控

百炼平台提供多层次的 Token 消耗监控能力：

- **用量统计**：在模型用量页面按[业务空间](workspace.md)维度汇总各模型的 Token 消耗，数据延迟约 1 小时，支持查看最近 30 天数据。
- **模型监控**：提供 TPM（Tokens Per Minute）等实时性能指标，高级监控可达分钟级精度。监控看板包含平均单次请求 Token 量、Token 总量等指标。
- **应用观测**：对[智能体应用](agent-application.md)、工作流应用等，可追踪每次调用的 Token 消耗（输入/输出），并按分钟级频率同步，支持按 Token 总量筛选调用记录。
- **告警**：支持设置 Token 消耗阈值，异常时触发告警通知。

## Token 与容量规划

在生产环境中，TPM（Tokens Per Minute）是衡量模型推理吞吐能力的关键指标。百炼提供多种容量保障方案：

- **TPM 预留**：为指定模型预留专属 TPM 容量，按 kTPM（千 Token/分钟）预付费，预留容量内独享资源，超出部分自动降级为按量计费。
- **PTU 预置吞吐部署**：通过预留资源保障特定 TPM 吞吐能力，支持长输入阶梯系数和前缀缓存折扣。
- **模型单元部署**：支持 PD 分离模式，将 Prefill 和 Decode 拆分到不同节点以降低首 Token 延迟。

## Token Plan 订阅服务

百炼还提供 Token Plan 团队版订阅服务，采用 Credits 计量体系（本质上基于 Token 消耗换算），面向团队和企业用户。套餐按坐席购买，月度额度从 25,000 到 250,000 Credits 不等，支持文本生成和图像生成模型。Token Plan 使用专属 [API Key](api-key.md)（sk-sp-xxx 格式）和独立 Base URL，与按量计费体系完全隔离。

## 成本优化建议

- 合理选择模型：简单任务使用 flash 级模型可大幅降低 Token 成本。
- 利用上下文缓存：对高频相似请求启用前缀缓存，降低输入 Token 费用。
- 使用 Batch 调用：对时效性要求不高的场景，Batch 调用可节省 50% Token 费用。
- 购买节省计划或资源包：预估用量后通过承诺消费或预购 Token 获取折扣。
- 开启免费额度用完即停：防止免费额度耗尽后产生意外的 Token 计费。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model monitoring](../guides/model-monitoring.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [application monitoring](../guides/application-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [get started with models](../guides/get-started-with-models.md)


