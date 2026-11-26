# agent billing

Agent 计费采用“按需组件化”模式，费用来源于实际调用的模型、工具及基础设施资源（如会话运行时、沙箱、知识库规格等），而非 Agent 编排能力本身。各组件独立计费，免费额度仅限抵扣其指定计费项，且不跨组件通用。实际费用以控制台账单为准，开发者需结合用量监控与配置优化进行成本管理。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力组件：

- **模型调用**：包括大语言模型（如 `qwen-plus`、`qwen3.7-plus`）、向量模型（如 `text-embedding-v4`、`qwen3-vl-embedding`）、排序模型（如 `qwen3-rerank`）、路由模型及语音/多模态生成模型（文生图、文生视频等）。费用按输入/输出 [Token](../concepts/token.md) 精确计量，标准见[选择模型](../../model-user-guide/get-started-with-models/models.md)。  
- **知识库（RAG）**：含规格费用（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时）和模型调用费用（向量化、Rerank、路由、问答生成等），详见[知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **记忆库（Memory Library）**：商业化后按写入（Add）、检索（Search）次数及存储（¥0.002/万条/小时）计费，Pro/Lite 版本影响 Rerank 调用与单价，[计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)明确区分策略版本规则。  
- **ParseX 文档解析**：图文按页、音视频按秒计量，支持在线/离线双价目，免费额度一次性发放，[计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)提供详细分项单价。  
- **Managed Agents**：包含会话运行时费（0.5 元/小时）、模型调用费、工具/MCP 调用费（如 `web_search` 0.03 元/次）及沙箱持久化费（0.003 元/个/小时），[计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)强调空闲状态不计运行时费。  
- **Sandbox**：按秒计费，分会话运行费（基础/进阶/旗舰款 0.156–0.624 元/小时）与数据保留费（0.0021 元/GiB·小时），暂停或 Snapshot 均产生保留费用。  
- **安全高级防护**：限时免费中，正式计费后含防御席位费（0.42 元/席位·小时）与超额 Credits（0.0015 元/Credit），每个席位每日默认 300 Credits，过期不结转。

> **注意**：文档 1 明确指出“Flow Agent 的编排能力本身不单独收费”，而文档 2、3、7 中 Managed Agents、Sandbox、安全防护均按运行时长计费——这反映百炼平台对“运行态资源”与“编排逻辑”的严格分离：前者是基础设施消耗，后者是无感能力。开发者需据此区分应用设计（轻编排+重复用）与资源部署（按需启停）。

## 关键参数

| 参数 | 所属组件 | 说明 | 参考文档 |
|------|----------|------|----------|
| `plan_version` | 记忆库 | 控制 Add/Search 是否启用 Rerank，Pro/Lite 影响单价与质量，请求级独立控制 Search 版本 | [billing-f23f20af1adb6c6b.md](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md) |
| `RCU`（Retrieval Compute Unit） | 知识库（旗舰版） | 1 RCU ≈ 支撑 50 QPS，并发需求 = ⌈峰值 QPS ÷ 50⌉，变配分段计费 | [billing-for-knowledge-base.md](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md) |
| `TopK`（初步向量/关键词召回） | 知识库检索 | 直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗量（费用 = 初步召回总切片数 × 平均切片 [Token](../concepts/token.md) 数 × 单价），可调范围 10–100 | [billing-for-knowledge-base.md](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md) |
| `session state`（运行中/空闲） | Managed Agents | 仅“运行中”状态产生会话运行时费；空闲状态不计费，需主动终止释放资源 | [managed-agents-billing.md](../../raw/application-user-guide/agent-billing/managed-agents-billing.md) |
| `snapshot retention time` | Sandbox | 快照保留时长（小时）直接计入数据保留费，恢复新快照后旧快照立即释放 | [sandbox-billing.md](../../raw/application-user-guide/agent-billing/sandbox-billing.md) |

## 使用方式

- **费用触发条件**：所有计费项均在服务实际被调用或资源处于活跃状态时实时产生。例如：知识库创建即开始计规格费；Managed Agent 会话启用即计运行时费；模型 API 被调用即计 Token 费；上传文件不计费，但后续解析/向量化/问答均触发对应计费。  
- **用量查询**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看各组件明细（运行时长、Token、Credits、页数/秒数等）；也可调用 [Usage API](../../application-api-reference/managed-agents-api/usage-api.md) 获取结构化数据（`POST /usage/summary` 或 `/usage/trend`）。  
- **账单管理**：费用按小时出账，最终以[账单与成本管理](../../model-user-guide/test-1/bill-query-and-cost-management.md)页面显示的控制台账单为准。知识库、Managed Agents 等支持资源包预购，抵扣顺序为：**免费额度 > 资源包 > 按量付费**。  
- **免费额度使用**：新人模型免费额度、知识库 720 小时、记忆库赠送次数等均自动生效，但存在有效期与适用范围限制（如知识库免费额度仅抵扣标准版规格费，不覆盖模型调用费），需在控制台及时核对剩余量。

## 限制和注意事项

- **免费额度不可跨组件抵扣**：模型免费额度不能用于抵扣知识库规格费或 Managed Agents 运行时费；记忆库赠送额度仅限 Add/Search/存储，不覆盖其注入 Prompt 后引发的大模型 Token 消耗。  
- **Rerank 费用易被低估**：知识库检索费用中，Rerank 模型费用取决于**初步召回总切片数**，而非最终返回数量。若 `TopK` 设置过高（如默认 50+50=100），即使只返回 5 条结果，仍按 100 个切片的 Token 总量计费。关闭 Rerank 或调低 `TopK` 是最有效的成本优化手段。  
- **多知识库场景费用倍增**：当智能体/工作流挂载 N 个知识库时，同一 Query 的向量化、路由、Rerank 调用均执行 N 次，模型费用呈线性增长。应避免冗余挂载，优先通过知识库内部分片策略提升单库覆盖度。  
- **沙箱与 Managed Agents 的“隐性”存储成本**：Sandbox 暂停或保存 Snapshot 会产生数据保留费；Managed Agents 开启沙箱持久化后，快照保留时长独立计费（0.003 元/个/小时）。二者均需显式清理快照或终止会话才能停止计费。  
- **安全防护 Credit 时效性**：高级防护的每日 300 Credits 按自然日清零，不结转。高频调用场景需预估日均消耗，避免因 Credit 耗尽导致防护降级。  
- **MCP 第三方费用**：部分 MCP（如调用外部支付网关、地图 API）产生的费用由第三方收取，阿里云百炼不参与计费，开发者需自行与第三方结算。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)


