# Token

Token 是大模型处理文本的最小计量单位，可以是一个词、一个汉字或若干字符；在阿里云百炼平台中，Token 既是模型推理的计费依据，也是用量统计、容量规划与监控告警的核心度量。

## 在百炼平台的角色

Token 贯穿百炼的推理、训练、部署与监控全链路，不同子系统对它的处理方式各异：

- **模型调用计费**：大语言模型、视觉理解、全模态与向量模型均按输入和输出 Token 数计费。部分模型实行阶梯计费——单价取决于单次请求的输入 Token 总量，落在哪个区间，全部 Token 就按该区间单价结算。例如某模型设 `0 < Token ≤ 32K` 与 `32K < Token ≤ 128K` 两档，输入 100K Token 时全部按第二档计价。
- **附加场景计费**：Batch 调用的输入输出 Token 均按实时推理价格 50% 计费；上下文缓存仅对输入 Token 给予折扣，且与 Batch 半价互斥；模型训练按 `(训练数据 Token 总数 + 混合训练数据 Token 总数) × 循环次数 × 训练单价` 计算，最小计费单位 1 token。
- **用量统计**：模型用量页按[业务空间](workspace.md)维度汇总 Token 消耗，数据延迟约 1 小时，不支持按账号维度统计；如需账号级 Token 总量，需主账号在费用与成本页面导出账单。
- **模型监控**：模型监控提供 Token 消耗的三层管理——汇总（按[业务空间](workspace.md)汇总历史 Token）、追踪（记录每次调用的 Token 消耗，需开通推理日志）、告警（设置 Token 消耗阈值，异常时立即告警）。应用观测则追踪应用内每个节点的 Token 量，如 LLM 节点 Token = 输入 + 输出，EMBEDDING 节点 Token 为本次向量化 Token 数。
- **容量规划**：TPM 预留与 PTU 部署均以 Token 吞吐量（kTPM = 1,000 Tokens/分钟）为容量单位。容量计算器依据每分钟请求数、平均输入/输出长度（token）及预估缓存命中率，自动推荐输入/输出 TPM。
- **套餐抵扣**：Token Plan（团队版）按 Token 消耗抵扣 Credits，单次消耗由模型类型、Token 用量、思考模式及工具调用动态决定；Coding Plan 则按调用次数计费，不直接以 Token 计量。

## 不同模型的统计口径

Token 并非所有模型的唯一计量单位，需按模型类型区分：

| 模型类型 | 统计单位 | 计费说明 |
| --- | --- | --- |
| 大语言模型（文本生成/深度思考/视觉理解） | Token | 按输入和输出 Token 数计费 |
| 视觉模型·图像生成 | 张 | 按成功生成图像张数 |
| 视觉模型·视频生成 | 秒 | 按成功生成视频秒数 |
| 语音模型 | 秒/字符/Token | 视模型而定 |
| 全模态模型 | Token | 文本与其他模态均按 Token |
| 向量模型 | Token | 按输入文本 Token 数 |

## 关键参数与配置

- **阶梯系数**：长输入场景下，超过 32K 的输入按更高阶梯系数折算 TPM 消耗。如 `glm-5.1`（上限 200K）在 [32K, 200K] 区间输入系数 1.33、输出系数 1.17；`deepseek-v4-pro`、`qwen3.7-plus` 则无阶梯（1.0）。
- **缓存折扣**：命中前缀缓存的输入 Token 按折扣系数消耗额度。`glm-5.1` 缓存命中部分按 20% 折算，`deepseek-v4-pro` 按 8%，Qwen 系列按 20%。
- **API 响应字段**：PTU 部署下，`service_tier` 标识计费方式（`ptu-standard` 用 PTU 额度，`default` 按量计费），`provisioned_tokens` 为折算后实际消耗的 PTU 额度 Token 数，`cached_tokens` 为前缀缓存命中的 Token 数。
- **免费额度**：仅抵扣模型实时推理的 Token 消耗，不支持 Batch、调优、部署；可开启"免费额度用完即停"避免超额扣费。
- **抵扣顺序**：免费额度 > 资源包 > 其他模型节省计划 > AI 通用型节省计划 > 按量付费；同类多优惠优先抵扣先到期的。
- **额度耗尽行为**：未认证用户耗尽后返回 `AllocationQuota.FreeTierOnly`，需认证充值；Token Plan 坐席月度额度与共享用量包用尽则暂停至下一计费周期。

## 开发者要点

- 用量数据按[业务空间](workspace.md)统计，跨空间汇总需主账号导出账单。
- Token 计费采用"预占+月结"，系统先冻结额度，次月初生成最终账单，并非实时扣款。
- 长输入场景下 PTU 利用率可能超过 100%（阶梯系数使折算消耗高于原始 Token 数），属正常现象，超出部分自动转按量计费，响应头含 `x-dashscope-ptu-overflow:true`。
- 接入 TPM 预留或 PTU 部署时，只需将 API 请求中的 `model` 参数替换为专属 model code，无需改动其他代码。
- 应用观测中可按 Token 总量、输入 Token、输出 Token 等字段筛选 Span，并将真实线上调用加入评测集作为样本。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [model deployment 1](../guides/model-deployment-1.md)


