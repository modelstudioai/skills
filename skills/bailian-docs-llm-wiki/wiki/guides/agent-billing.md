# agent billing

百炼平台的 Agent 计费体系采用“按需组件化计费”原则：Agent 本身不单独收费，费用来源于其运行过程中实际调用的底层能力（如模型、知识库、MCP、沙箱、安全防护等），各组件独立计费、额度隔离、免费额度仅抵扣对应计费项。开发者需根据应用形态（智能体/工作流/Managed Agents/Sandbox）和启用的功能模块，分别核算成本。所有费用以控制台台账单为准，账单按小时聚合出账。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **模型调用**：包括大语言模型（如 `qwen-plus`、`qwen3.7-plus`）、向量模型（如 `text-embedding-v4`、`qwen3-vl-embedding`）、排序模型（如 `qwen3-rerank`）、路由模型及多模态模型（如 `qwen3-vl-rerank`）。计费单位为输入/输出 [Token](../concepts/token.md)，单价见[选择模型](raw/model-user-guide/get-started-with-models/models.md)；智能模式下 AUTO 档位按统一刊例价计费，与实际路由模型无关 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **知识库（RAG）**：含规格费用（标准版 0.03 元/库/小时，旗舰版按 RCU 计费）与模型调用费用（向量化、排序、路由等），二者完全分离 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **MCP 与工具调用**：官方 MCP（如文生图、语音合成）按模型调用计费；第三方 API 调用由第三方收费，百炼不收取费用；内置工具如 `web_search` 按 0.03 元/次计费，`web_fetch` 限时免费 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Sandbox**：按运行时长（基础/进阶/旗舰款分档）和数据保留量（GiB·小时）计费，暂停或 Snapshot 均产生数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **ParseX 解析服务**：图文按页、音视频按秒计量，支持解析与字段抽取分项计费，新文档直接抽取已含解析费用 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：按防御席位（0.42 元/席位·小时）和超额 Credits（0.0015 元/Credit）计费，当前处于限时免费阶段，正式计费前将提前通知 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 4 和文档 7 内容完全重复，均为同一份 `billing.md` 的重复收录，以最新版本为准（即文档 7），但二者均未体现“正式计费起始时间”，仅说明“截至 2026 年 9 月仍限时免费”，开发需关注控制台公告。

## 关键参数

- **[Token](../concepts/token.md) 计费粒度**：模型类费用（含 LLM、Embedding、Rerank）均按千 [Token](../concepts/token.md) 四舍五入计费，不足 1 千 Token 按 1 千计。
- **RCU（Retrieval Compute Unit）**：知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配按小时分段计费，1 自然日内最多变配 1 次。
- **TopK 参数影响成本**：知识库检索中，“初步向量检索 TopK”和“初步关键词检索 TopK”直接决定送入 Rerank 模型的切片总数，从而显著影响排序费用；关闭重排可消除该费用。
- **沙箱计费精度**：Sandbox 运行费按秒计量，数据保留费按 GiB·小时计量，不足 1 小时按整小时计。
- **Credit 时效性**：安全防护 Credit 按自然日清零，不结转，每个席位每日独立享有 300 Credits。

## 使用方式

- **开通即用型服务**（如知识库、ParseX、安全高级防护）：在控制台完成服务开通后，计费自动生效；删除资源（如知识库、Sandbox）可立即停止对应规格费用。
- **按调用触发型服务**（如模型、MCP、工具）：仅当 Agent 实际发起调用时产生费用，空闲会话、UI 设计器操作、Prompt 自动优化等不计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **免费额度使用逻辑**：遵循“免费额度 > 资源包 > 按量付费”三级扣减顺序；多个同类型资源（如多个知识库）共享免费额度或资源包，按实际用量累计扣除。
- **用量查询**：
  - 统一入口：控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看 Managed Agents 运行时长、Token、工具调用明细；
  - 知识库规格费用：账单详情中筛选商品名称为“阿里云百炼知识库（RAG）- 后付费”；
  - 模型 Token 用量：账单详情中筛选商品名称为“阿里云百炼大模型推理”，通过实例 ID 后缀（如 `;embedding_token;RAG;0`）识别来源；
  - ParseX 用量：通过 [任务记录](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md) 和 [用量](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md) 查看。

## 限制和注意事项

- **免费额度不可跨组件使用**：模型免费额度仅抵扣模型调用，知识库免费额度仅抵扣标准版规格费用，ParseX 免费页数仅用于解析/抽取，三者互不通用。
- **知识库路由与多库检索成本倍增**：应用挂载 N 个知识库且开启路由时，Query 向量化、Rerank 排序等操作将执行 N 次，Token 消耗量线性增长。
- **缓存费用独立计算**：智能体应用暂不支持显式缓存配置，隐式缓存自动生效且按对应模型缓存价格计费；显式缓存规则见[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。
- **沙箱快照生命周期影响费用**：Sandbox 恢复运行生成新快照后，上一快照才被释放；快照保留时长计入数据保留费，与运行时长无关。
- **文件上传本身不计费，但内容处理必计费**：文件问答中上传操作免费，但后续基于文件内容的解析、向量化、问答生成等均产生对应费用。
- **分享链接产生的费用归属创建者**：无论谁通过分享链接使用应用，费用均由应用创建者的 UID 账号承担 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


