# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的程序化访问能力，支持防护概况查询、资产统计、策略管理、告警检索与导出等核心场景。所有接口均基于统一鉴权机制，通过工作空间专属 Endpoint 访问，适用于安全运营自动化与集成开发。详细接口定义与行为约束请参考各功能模块文档。

## 支持的模型/功能

Security API 当前覆盖以下五类安全能力：

- **防护概况**：提供全局防护开关状态与各模块拦截统计，固定查询最近 24 小时数据。包括 `/overview`（防护总览）和 `/asset_summary`（Agent 资产统计）两个接口。
- **策略管理**：返回全量 11 条安全策略的启用状态与分类信息，无分页，策略列表固定不变。详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警管理**：支持告警列表查询（游标分页）、单条告警详情获取、批量导出及导出状态轮询，覆盖风险等级、处置状态、资产类型等多维筛选条件。
- **导出能力**：通过 `/export_agent_logs` 提交导出任务，再调用 `/export_status` 查询进度与下载链接，导出格式为 Excel。
- **通用能力**：所有接口共享统一响应结构（`{"success": boolean, "data": ...}`）与错误码体系，失败时返回 `errorCode` 与 `errorMsg`。

> **注意**：文档 5 中 `asset_type` 参数支持值包含 `channel`，但文档 3 的 `asset_summary` 响应字段中 `channel` 明确说明“发布渠道数（排除已删除、已过期）”，而文档 5 未说明该过滤逻辑是否同步应用于告警筛选——实际使用中建议以告警列表返回的实际 `asset_type` 值为准，避免依赖未明确定义的语义一致性。

## 关键参数

- **Endpoint 拼装**：必须按 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security` 格式构造，其中 `workspace_id` 从控制台右上角获取，地域仅支持 `cn-beijing`。
- **鉴权头**：所有请求必须携带 `Authorization: Bearer <your-api-key>`，API Key 需通过 [控制台](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建。
- **告警筛选参数**（`/agent_logs`）：常用组合包括 `risk_level`（`high`/`medium`/`low`）、`status` 或 `status_list`、`asset_type`（如 `agent`/`tool`/`knowledge_base`）、`order_by=check_time` 与 `order=desc`。
- **导出参数**（`/export_agent_logs`）：`params` 字段需为 JSON 字符串（非对象），内容须与 `/agent_logs` 查询参数严格一致（字段名大小写敏感，如 `"CurrentPage"` 而非 `"current_page"`），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)。
- **导出状态查询**（`/export_status`）：必须传入 `export_id` 查询参数，该 ID 来自 `/export_agent_logs` 响应。

## 使用方式

1. **初始化配置**：确认工作空间 ID 与 API Key 已就绪，拼装 BASE_URL。
2. **调用防护接口**：
   - 获取防护快照：`GET /overview` 和 `GET /asset_summary` 无需参数，直接请求。
   - 获取策略清单：`GET /policies` 固定返回全量策略。
3. **处理告警**：
   - 列表查询：`GET /agent_logs?risk_level=high&order_by=check_time&order=desc`
   - 查看详情：`GET /agent_logs/{alert_id}`，`alert_id` 来自列表响应。
   - 导出任务：`POST /export_agent_logs` 提交含 `params` 的 JSON Body。
   - 轮询状态：`GET /export_status?export_id=131231`，待 `export_status="success"` 且 `link` 非空后下载。
4. **错误处理**：捕获 HTTP 503 及 `errorCode`（如 `12000093`、`12000094`），按文档建议重试；单项字段缺失时响应仍为 `success: true`，对应字段为 `null` 或 `available: false`。

> **注意**：文档 2 与文档 3 均声明其请求示例中的 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，但文档 1 的 Endpoint 定义明确要求 `{region}` 占位符（当前仅 `cn-beijing`），二者实质一致；然而文档 1 的原始路径描述为 `/api/v1/agentstudio/security`，而文档 2/3 示例中 URL 后缀与之完全匹配，可确认路径无歧义。此一致性已在 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中明确定义。

## 限制和注意事项

- **地域限制**：所有接口仅支持 `cn-beijing` 地域，其他 region 域名将返回 404 或 503。
- **时间窗口固定**：`/overview` 接口仅返回最近 24 小时数据，不支持自定义时间范围。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），非传统 offset 分页；导出任务则基于筛选条件全量导出，不受当前页限制。
- **字段空值语义**：当某项统计不可用时（如未启用某模块），响应中对应字段为 `null`，而非 `0` 或 `false`（例如文档 3 明确说明：“取不到的字段返回 `null`，不返回 0”）。
- **策略数量固定**：`/policies` 接口始终返回 11 条策略，新增策略需等待文档更新，客户端不应假设策略数量可变。
- **导出参数格式严格**：`/export_agent_logs` 的 `params` 必须是合法 JSON 字符串，且字段名需与后端内部映射一致（如 PascalCase），与 `/agent_logs` 的 query 参数命名不完全对应，务必按 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 示例构造。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)


