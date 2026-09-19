# security api guide

Security API 提供 Agent 全生命周期的安全防护数据查询与告警管理能力，包括防护能力总览、资产统计、策略配置、实时告警及批量导出等功能。所有接口均基于统一的鉴权机制和 Endpoint 拼装规则，面向开发者提供结构化、可集成的安全可观测性能力。详细前提条件与通用规范请参见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 支持的模型/功能

Security API 当前覆盖以下核心安全能力维度：

- **防护概况**：提供全局防护开关状态与拦截统计，包括 `agent_identity`（Agent 身份签发）、`content_safety`（内容安全）、`supply_chain_scan`（供应链静态扫描）等 5 类能力开关，以及 `flow_agent`、`managed_agent`、`knowledge_base` 等 6 类模块覆盖开关；同时返回 `content_safety`、`file_scan`、`skill_scan` 三类扫描统计卡片。详情见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **资产统计**：以 Agent 为中心聚合挂载资源数量，包括 `model`、`tool`、`skill`、`knowledge_base`、`memory` 等 9 类资产指标，支持业务空间级安全资产盘点。
- **策略管理**：固定返回 11 条安全策略全量列表，按 `risk_domain` 分组（如 `model_interaction`、`runtime_tool`、`knowledge_memory`），每条策略含 `policy_code`、`enabled` 和 `free` 字段，可用于策略启用状态同步与合规审计。
- **告警全链路**：支持告警列表查询（游标分页、多维筛选）、单条告警详情获取、异步导出任务提交与状态轮询，覆盖从检测、分析到处置的完整闭环。

> **注意**：文档 4 中 `policy_code` 列表包含 `network_protection`，但文档 1 的 `protection.key` 取值未列出该值；实际使用应以 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 返回的 `policy_code` 为准，`protection` 数组仅表示模块覆盖范围，二者语义不同，不可混用。

## 关键参数

- **Endpoint**：必须按格式拼装 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 为控制台获取的实际工作空间 ID，地域目前仅支持 `cn-beijing`。
- **鉴权**：所有请求必须携带 `Authorization: Bearer <your-api-key>` Header，API Key 需通过 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 获取。
- **分页与筛选**：
  - `/agent_logs` 支持 `current_page`、`page_size`、`risk_level`、`status`、`asset_type` 等参数组合筛选；
  - `/export_agent_logs` 的 `params` 字段需传入 JSON 字符串（非对象），且字段名首字母大写（如 `"CurrentPage"`），与列表接口参数名不一致，需严格遵循示例格式。
- **告警导出依赖参数一致性**：导出任务的 `params` 必须与 `/agent_logs` 查询时使用的参数完全一致（包括大小写与序列化方式），否则可能导致导出结果不匹配。

## 使用方式

1. **初始化配置**：确认已开通百炼服务并创建有效 API Key，获取 `workspace_id`，构造 `BASE_URL`。
2. **查询防护状态**：调用 `GET /overview` 获取能力开关与拦截统计，快速验证防护是否生效。
3. **盘点资产规模**：调用 `GET /asset_summary` 获取当前工作空间内 Agent 及其关联资源数量，辅助容量与风险评估。
4. **检查策略启用情况**：调用 `GET /policies` 获取全量策略状态，重点关注 `enabled: false` 的高风险策略（如 `content_safety`、`network_protection`）。
5. **监控与响应**：
   - 调用 `GET /agent_logs` 按需筛选告警（例如 `risk_level=high&status=intercepted`）；
   - 对关键告警调用 `GET /agent_logs/{alert_id}` 获取 `risk_detail` 和 `risk_handle` 用于根因分析；
   - 如需批量处理，先 `POST /export_agent_logs` 提交任务，再轮询 `GET /export_status?export_id=xxx` 直至 `export_status == "success"` 且 `link` 非空后下载 Excel。

## 限制和注意事项

- 所有接口均为只读查询，不支持写操作（如启用/禁用策略、修改告警状态）。
- `/overview` 固定返回最近 24 小时数据，不可指定时间范围；`/agent_logs` 默认按 `check_time` 倒序排列，历史告警保留周期以平台策略为准。
- `/policies` 接口固定返回 11 条策略，无分页，但策略列表可能随版本更新扩展，建议通过 `policy_code` 字段做健壮性判断，而非硬编码索引。
- 告警导出任务最大支持单次导出 10,000 条记录；若 `total_count` 超过该值，需拆分筛选条件（如按 `risk_level` 或 `asset_type` 分批导出）。
- 响应中字段为 `null` 表示“不可用”而非“值为 0”，例如 `file_name` 在非 Skill 类告警中为 `null`，不应默认赋值为空字符串。
- 错误码 `12000093`（云安全服务异常）和 `12000094`（告警查询失败）均为临时性错误，建议实现指数退避重试逻辑。

## 来源文档

- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


