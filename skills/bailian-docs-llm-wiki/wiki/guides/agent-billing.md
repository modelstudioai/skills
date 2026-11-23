# agent billing

Agent 计费采用组件化、按量计费模式，费用由运行时资源（如会话、沙箱）、模型调用、知识库、记忆库、解析服务及安全防护等独立计费项构成。各组件遵循自身定价规则，免费额度仅限抵扣其指定计费项，不跨组件通用。实际费用以控制台台账单为准，开发者需结合用量监控与账单明细进行成本管理。

## 支持的模型/功能

- **模型调用**：所有智能体应用、工作流应用、Managed Agents 及知识库中涉及的大模型（如 `qwen-plus`、`text-embedding-v4`、`qwen3-rerank`）均按输入/输出 Token 计费，标准见[选择模型](raw/model-user-guide/get-started-with-models/models.md)；智能模式下 AUTO 路由按统一刊例价计费，与实际路由模型无关 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **知识库**：支持标准版（0.03 元/知识库/小时）与旗舰版（0.2 元/RCU/小时），费用含规格运行时长 + 向量/排序/路由/问答模型调用费用；其中模型调用费用独立于规格费，按实际 Token 消耗计算 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **记忆库**：自 2026 年 8 月 20 日起商业化计费，按写入（Add）、检索（Search）、存储三类计费，Pro/Lite 版本影响 Rerank 是否启用及单价；检索结果注入 Prompt 将额外增加大模型 Token 消耗 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
- **ParseX 解析服务**：图文按页、音视频按秒计量，提供一次性免费额度（如图文解析 3,000 页），超出后按量计费（图文 ¥0.02/页，视频 ¥0.002/秒） [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Sandbox**：按运行时长（基础款 0.156 元/小时）和数据保留（0.0021 元/GiB·小时）分项计费，暂停或 Snapshot 均产生数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Managed Agents**：包含会话运行时费（0.5 元/小时）、模型调用费、工具/MCP 调用费（如 `web_search` ¥0.03/次）及沙箱持久化费（0.003 元/个/小时） [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Agent 安全高级防护**：限时免费中，正式计费后按防御席位（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）组合计费，每个席位每日默认 300 Credits，不结转 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

> **注意**：文档 6 中“知识库路由”明确说明调用 `qwen-plus` 判断查询路由时产生模型费用；而文档 1 中“MCP”部分称“部分 MCP 涉及第三方 API 调用，该部分费用由第三方收取，阿里云百炼不收取费用”，二者逻辑一致（即百炼仅对自身托管模型调用计费），但需注意 `qwen-plus` 在知识库路由场景属百炼自有模型，非第三方 MCP，故应计费 —— 此处无矛盾，属不同组件范畴。

## 关键参数

- **Token 计量**：模型调用费用 = (输入 Token 总数 / 1000) × 单价（元/千 Token）；知识库检索中 Rerank 费用取决于**初步召回总切片数 × 平均切片 Token 数**，而非最终返回数量 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **RCU（Retrieval Compute Unit）**：旗舰版知识库并发能力单位，1 RCU ≈ 支撑 50 QPS；变配按小时分段计费，1 自然日内最多变配 1 次 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **Plan Version（记忆库）**：`Add` 调用版本由 project 的 `plan_version` 决定（默认 Pro），`Search` 调用版本由请求参数 `plan_version` 独立控制（默认 Pro）；更新 project 版本不影响已写入记忆 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
- **Credits（安全防护）**：每个 Agent 席位每日独立享有 300 Credits，有效期 24 小时（自然日），按被检测内容 Token 量换算消耗，不结转 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

> **注意**：文档 2 与文档 3 对“沙箱”计费描述存在术语混淆。文档 2 中“沙箱持久化”指 Managed Agents 的快照存储（0.003 元/个/小时），而文档 3 中“Sandbox”是独立计算环境服务，计费项为“数据保留费”（0.0021 元/GiB·小时）。二者属不同产品模块，不可混用参数 —— 开发者需严格区分 `Managed Agents > Session > 沙箱持久化` 与 `Sandbox > 运行实例` 的上下文。

## 使用方式

- **查看用量**：  
  - Managed Agents：通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面或调用 [Usage API](raw/application-api-reference/managed-agents-api/usage-api.md)（`POST /usage/summary` 或 `/usage/trend`）获取运行时长、Token、工具调用明细 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
  - 知识库：在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)中筛选“大模型服务平台阿里云百炼”→“阿里云百炼大模型推理”，通过实例 ID 后缀（如 `...-embedding-...`）识别向量/排序模型用量 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
  - ParseX：通过[任务记录](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md)核对单次处理能力与用量，或在[用量](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md)页面查看周期汇总 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **成本优化**：  
  - 知识库：关闭 Rerank、降低初步召回 TopK（如设为 10–30）、使用资源包或节省计划（AI 通用型）抵扣模型费用 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
  - 记忆库：高频低精度场景选用 Lite 版本检索（¥0.00002/次），避免 Pro 版本不必要的 Rerank 开销 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。  
  - 工作流/智能体：避免在未执行路径上配置高成本节点（如 Qwen-VL 图片解析），优先选用暂不计费的内置解析节点 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 限制和注意事项

- **免费额度规则**：  
  - 新人模型免费额度仅抵扣模型调用，知识库、记忆库、ParseX 等组件额度互不通用，且均有时效性（如知识库老用户免费额度截至 2026 年 2 月 3 日） [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
  - 记忆库写入/检索免费额度按规格发放（如事实记忆 Pro 共 250 次），存储额度（10,000 条）长期有效；额度用尽后立即按量计费 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。  
- **关键限制**：  
  - 知识库删除将**永久清除数据且无法恢复**，务必谨慎操作 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
  - Managed Agents 会话处于“运行中”状态即产生运行时费，空闲状态不计费；应及时终止不用的会话 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
  - Sandbox 暂停后保存的数据及 Snapshot 按实际 GiB 占用与时长计费，系统盘 15 GiB 不另收费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。  
- **费用归属**：通过为业务空间（Workspace ID）绑定标签，可实现分账管理，费用将归属至对应标签部门或项目 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **分享应用费用承担**：通过分享链接产生的所有费用均由应用创建者的 UID 账号承担，与访问者无关 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)


