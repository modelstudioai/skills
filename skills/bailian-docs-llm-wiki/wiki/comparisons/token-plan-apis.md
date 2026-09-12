# [Token](../concepts/token.md) 计划相关 API 对比

本文档面向百炼平台企业级开发者与系统集成方，旨在清晰区分三类常被混淆的“[Token](../concepts/token.md) 相关”API：**[Token](../concepts/token.md)Plan API（组织配额治理）**、**Billing API（账单与用量计量）** 和 **File Management API（文件级 Token 消耗载体管理）**。尽管三者均涉及 Token 的生命周期管理环节（如配额分配、费用归因、数据输入），但其设计目标、作用域、技术契约与计费语义存在本质差异。正确理解边界可避免误用（例如：试图用 TokenPlan API 查询模型调用费用，或用 Billing API 分配成员席位），是构建合规、可审计、可扩展的 AI 运营体系的前提。

以下从核心维度进行结构化对比，并给出技术选型建议。

## API 关键维度对比

| 维度 | TokenPlan API | Billing API | File Management API |
|------|----------------|--------------|------------------------|
| **核心定位** | 组织级资源配额治理（Seat/Member/API Key 生命周期管理） | 账单与用量计量服务（费用、Token 消耗、调用次数的聚合与趋势分析） | 文件级数据载体管理（为 fine-tune / file-extract / batch 等场景提供带用途标识的文件托管能力） |
| **是否参与模型推理调用** | ❌ 不参与。纯治理接口，无模型调用行为 | ❌ 不参与。仅读取已发生的计费事件，不触发任何模型执行 | ❌ 不参与。仅上传/管理文件元数据；文件内容本身在后续模型调用（如 `fine_tunes.create`）中才被消费并产生 Token |
| **支持模型** | 无。不关联任何大模型 | 通用。支持按 `model_id`（如 `qwen-max`, `qwen-plus`）等维度分组统计，但本身不调用模型 | 无。文件用途（`purpose`）决定其后续被哪类模型能力消费（如 `fine-tune` → 微调任务；`file-extract` → 文档解析任务），但 API 本身不绑定具体模型 |
| **API 端点示例** | `POST /organizations/{org_id}/seats/assign`<br>`GET /organizations/{org_id}/member-seat-stats` | `POST https://modelstudio.aliyuncs.com/?Action=GetBillingOverview`<br>`POST https://modelstudio.aliyuncs.com/?Action=GetBillingTrend` | `POST https://dashscope.aliyuncs.com/api/v1/files`<br>`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}` |
| **认证方式** | `Authorization: Bearer <TokenPlan_API_Key>`（百炼平台生成的专用长期凭证） | 阿里云 STS Token 或 AccessKey（需 `bss:Describe*` 权限） | `Authorization: Bearer <DashScope_API_Key>`（同模型调用密钥） |
| **输入格式** | JSON（RESTful Body），含 `seat_count`, `invite_code` 等业务字段 | Query String + Signed Request（阿里云 RPC 风格），含 `StartTime`, `EndTime`, `GroupBy` 等参数 | `multipart/form-data`（上传）、Query（分页）、Path（ID 操作） |
| **输出格式** | JSON，结构化返回操作结果（如 `{"success": true, "assigned_seats": 5}`）或统计对象（如成员数、已用席位数） | JSON，标准阿里云 OpenAPI 响应格式（含 `Data`, `RequestId`, `Code`, `Message`），`Data` 内为嵌套账单对象 | JSON，统一返回 `data` 字段，内含文件元数据（`file_id`, `url`, `purpose`, `size`, `created_at` 等） |
| **计费方式** | ✅ **不直接计费**。TokenPlan API 调用本身免费；其管理的“席位”是付费资源单位，席位购买/续订通过控制台或商务流程完成 | ✅ **反映计费结果**。返回的是已结算或待结算的费用与 Token 消耗量（单位：千 Token），用于对账与预算监控 | ✅ **间接影响计费**。文件本身不收费；但文件被用于 `fine-tune`（训练）或 `batch`（批量推理）时，其处理过程将按对应模型的 Token 计费规则消耗额度（如训练 Token、推理输入/输出 Token） |
| **典型场景** | • 企业 SSO 同步后批量开通 200 名员工席位<br>• 为销售部门单独创建邀请链接并分配 10 个席位<br>• 审计组织内 API Key 使用情况并轮转高风险密钥 | • 财务团队每月初拉取上月各项目 `qwen-plus` 调用量与费用报表<br>• 运维告警：过去 7 天 `qwen-max` 日均 Token 消耗超阈值<br>• 分析不同地域（`region_id`）的模型调用成本分布 | • 上传 500 份合同 PDF 用于 `file-extract` 提取关键条款<br>• 准备 `train.jsonl` 和 `val.jsonl` 文件供 `fine-tune` 任务使用<br>• 批量提交 10,000 条文本至 `batch` 接口进行摘要生成 |

## 适用场景建议

### ✅ 选择 TokenPlan API 当：
- 你需要**管理组织架构与人员权限**（添加/移除成员、分配角色、设置席位）；
- 你需要**控制 API 密钥生命周期**（创建、轮转、撤销），且该密钥用于访问百炼平台所有服务（包括模型 API、TokenPlan API 自身）；
- 你需要**查询组织级资源水位**（当前有多少席位、多少成员已激活、剩余可用席位数），用于容量规划；
- 你正在构建企业级 SSO 集成、HR 系统联动或自动化入职流程。

> ⚠️ 注意：TokenPlan API **不能**用于查询某次模型调用花了多少钱，也不能用于上传训练数据。

---

### ✅ 选择 Billing API 当：
- 你需要**财务级精度的费用与用量归因**（按模型、项目、时间、地域等多维下钻）；
- 你需要**构建成本看板或自动化预算预警**（如：当 `qwen-turbo` 月度 Token 消耗 > 10M 时触发钉钉通知）；
- 你需要**与内部财务系统对接**，生成符合会计准则的 AI 成本分摊报表；
- 你需要**验证计费逻辑**（例如：确认某次长文本 `file-extract` 是否按预期计为输入 Token + 输出 Token）。

> ⚠️ 注意：Billing API **不能**用于分配资源、管理用户或上传文件；其数据有约 2 小时延迟，不适用于实时用量控制。

---

### ✅ 选择 File Management API 当：
- 你需要**为非实时、批处理类 AI 任务准备结构化输入数据**（如微调数据集、批量推理文档、知识库抽取源）；
- 你需要**复用已上传文件**（例如：同一份 `faq.jsonl` 可被多个微调任务引用）；
- 你需要**按用途隔离文件资产**（`fine-tune` 类文件不可用于 `batch`，反之亦然），便于权限与审计；
- 你的应用部署在 `cn-beijing` 地域，且需快速集成（注意：新项目请优先选用 [OpenAI 兼容接口](../concepts/openai-compatibility.md) `/compatible-mode/v1/files`）。

> ⚠️ 注意：File Management API **不能**用于流式上传、实时推理输入或[模型部署](../concepts/model-deployment.md)配置；单文件大小与总存储有硬性限制（详见文档）。

## 技术选型参考总结

| 你的需求 | 推荐 API | 关键理由 |
|----------|-----------|-----------|
| “我要给新入职的 50 名工程师开通百炼平台访问权限” | **TokenPlan API** | 唯一支持成员批量邀请、席位分配、角色绑定的治理接口 |
| “我想知道上季度 `qwen-vl-plus` 在华东区域的总调用费用和 Token 消耗” | **Billing API** | 唯一提供按 `model_id` + `region_id` 多维聚合账单数据的接口 |
| “我有一批 200 个 PDF 合同，需要提取甲方名称、签约日期、金额三项字段” | **File Management API** + **file-extract 模型调用** | 必须先上传文件获取 `file_id`，再在 `file-extract` 请求中引用；TokenPlan/Billing 均无法替代此步骤 |
| “我的 SaaS 应用要为每个租户独立计费，需精确到每次 API 调用的 Token 数” | **Billing API（趋势分析）** + **模型 API 的 `usage` 字段（响应头/体）** | Billing 提供宏观账单，模型 API 响应中的 `usage` 提供单次粒度；TokenPlan 无此能力 |
| “如何安全地轮换生产环境使用的 API 密钥？” | **TokenPlan API**（`POST /api-keys/rotate`） | 此为唯一支持密钥轮转的官方接口；Billing/File API 均不提供密钥管理能力 |

> 💡 **最佳实践提示**：  
> - **组合使用是常态**：一个企业级 AI 平台通常同时调用三类 API —— TokenPlan 管人、Billing 管钱、File Management 管数据。  
> - **认证隔离很重要**：TokenPlan API Key（高权限治理密钥）不应与模型调用 Key（`DashScope_API_Key`）混用，更不应与阿里云 AccessKey 共享。  
> - **新项目请拥抱兼容性**：File Management API 的原生路径（`/api/v1/files`）已明确标注为“兼容历史场景”，新开发务必采用 `/compatible-mode/v1/files`，以获得长期维护与跨 Region 支持。  

如需进一步了解各 API 的错误码处理、重试策略或 SDK 集成示例，请参阅对应模块的详细参考文档。

## 被对比主题页

- [token plan api](../api/token-plan-api.md)
- [billing api](../api/billing-api.md)
- [file management api](../api/file-management-api.md)


