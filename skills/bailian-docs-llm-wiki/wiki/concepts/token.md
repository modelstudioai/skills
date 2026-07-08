# Token

Token 是大语言模型处理文本的最小单位，模型将输入和输出的自然语言文本拆分为 Token 序列进行理解与生成。在百炼平台中，Token 既是模型能力的度量基础，也是计费、监控和容量规划的核心计量单元。

## 基本概念

大语言模型不直接处理原始文本，而是先通过分词器（Tokenizer）将文本切分为 Token。一个 Token 可能对应一个汉字、一个英文单词、一个子词片段或一个标点符号，具体粒度取决于模型所使用的分词算法。因此，同一段文本在不同模型下的 Token 数量可能不同。

在百炼平台中，Token 分为以下几类：

- **输入 Token**：用户发送给模型的 Prompt 及上下文所消耗的 Token 数量。
- **输出 Token**：模型生成的回复文本所消耗的 Token 数量。
- **缓存 Token**：命中上下文缓存的输入 Token，通常享有费用折扣。
- **训练 Token**：模型调优（微调）过程中消耗的 Token 总量。

## 计费场景

Token 是百炼平台按量付费的核心计量维度。不同场景的计费方式如下：

| 场景 | 计费方式 |
|------|---------|
| 模型推理（文本生成） | 按输入/输出 Token 数量分别计费，部分模型支持阶梯计费 |
| 模型训练 | 费用 = Token 总量 x 循环次数 x 训练单价 |
| 向量模型 | 按输入文本的 Token 数计费 |
| 全模态模型 | 文本与其他模态均按 Token 数计费 |

部分模型实行阶梯计费，单价取决于单次请求的输入 Token 总量。例如 qwen3-max 在输入 0\~32K Token 时为基础价，32K\~128K 时单价提升，128K\~256K 时进一步提升。

降低 Token 成本的常用手段包括：Batch 调用（输入/输出单价按实时推理的 50% 计费）、上下文缓存（输入 Token 享有折扣）、节省计划与资源包。

## 监控与观测

百炼平台在模型监控和应用观测两个层面提供 Token 相关指标：

- **模型监控**：按[业务空间](workspace.md)维度统计各模型的 Token 用量，支持按输入/输出分别查看。监控详情页提供 TPM（Tokens Per Minute）、平均单次请求 Token 量等性能指标。
- **应用观测**：追踪应用内部每个节点的 Token 消耗，包括 Token 总量、输入/输出 Token、平均单次请求 Token 量，以及平均首 Token 耗时（流式场景下的关键性能指标）。

用量数据按[业务空间](workspace.md)维度统计，数据延迟约 1 小时（普通监控）或分钟级（高级监控）。

## 容量规划：TPM 预留

TPM（Tokens Per Minute）是衡量模型推理吞吐能力的关键指标。百炼提供 TPM 预留功能，允许开发者为指定模型锁定专属推理容量。创建 TPM 预留时需要评估以下参数：

- **每分钟请求数（RPM）**
- **平均输入/输出 Token 长度**
- **预估缓存命中率**

预留容量内的调用不额外收费，超出部分自动降级为按量计费，服务不中断。

## 订阅套餐中的 Token

百炼提供 Token Plan 团队版和 Coding Plan 两类订阅套餐。Token Plan 以 Credits 统一计量，Credits 消耗由模型类型、Token 用量、思考模式等因素决定。两类套餐均使用专属 [API Key](api-key.md)（`sk-sp-xxx`）和专属 Base URL，与按量计费的通用 [API Key](api-key.md) 互不相通。

## 数据集规模参考

在模型调优场景中，训练数据的 Token 规模直接影响调优效果：

| 调优方式 | 最低数据规模 |
|---------|------------|
| CPT（继续预训练） | 一千万 Token 优质预训练数据 |
| SFT（监督微调） | 上千条优质微调数据 |
| DPO（偏好对齐） | 上百条人类偏好数据 |

## 关联主题页

- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [model data overview](../guides/model-data-overview.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


