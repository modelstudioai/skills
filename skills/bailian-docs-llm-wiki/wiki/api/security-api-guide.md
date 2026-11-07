# security api guide

Security API 提供对百炼平台 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于 `/api/v1/agentstudio/security` 路径前缀，需通过 API Key 鉴权并拼装工作空间专属 Endpoint。开发者应优先参考[概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)确认前提条件与基础结构。

## 支持的模型/功能

Security API 不涉及模型调用，而是面向安全治理的数据服务接口，当前支持以下 6 类功能：

- **防护概况**：`GET /overview`（固定查询最近 24 小时）与 `GET /asset_summary`，分别返回防护能力开关状态、模块覆盖情况及各维度拦截统计，以及 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数。
- **策略管理**：`GET /policies` 返回全量 11 条安全策略（如 `content_safety`、`prompt_attack`、`rag_poisoning` 等），含启用状态、风险域分组与是否免费。
- **告警全生命周期操作**：
  - 查询：`GET /agent_logs`（游标分页 + 多维筛选）
  - 详情：`GET /agent_logs/{alert_id}`（需从列表响应中提取 `alert_id`）
  - 导出：`POST /export_agent_logs`（提交任务，返回 `export_id`）
  - 状态轮询：`GET /export_status?export_id=...`（获取进度与下载链接）

> **注意**：文档 6 中 `asset_type` 参数允许值为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 9 的响应体示例中 `asset_type` 出现了 `app` 值（`"asset_type": "app"`），该值未在参数说明中定义，实际使用请以接口响应字段为准，避免硬编码校验。

## 关键参数

| 接口 | 必填参数 | 说明 |
|------|----------|------|
| 所有请求 | `Authorization: Bearer <API_KEY>` | API Key 需通过 Header 传递，获取方式见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| 所有请求 | Endpoint 拼装 | `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，`workspace_id` 须从控制台右上角下拉菜单获取 |
| `/agent_logs` | `current_page`, `page_size` | 默认 `1` 和 `20`；支持 `risk_level`（`high`/`medium`/`low`）、`status_list`（数组）、`asset_type` 等筛选 |
| `/export_agent_logs` | `params`（JSON 字符串） | 必须为告警列表查询参数的序列化字符串（如 `{"RiskLevel":"high","OrderBy":"CheckTime"}`），注意字段名大小写与文档 6 一致 |
| `/export_status` | `export_id` | 整型，来自 `/export_agent_logs` 响应的 `data.export_id` |

## 使用方式

1. **初始化配置**：确认已开通百炼服务，创建 API Key，并获取 `workspace_id`；
2. **构造请求**：按文档 1 的 Endpoint 规则拼接 Base URL，所有请求添加 `Authorization` Header；
3. **调用链路示例**：
   - 查询高风险告警：`GET /agent_logs?risk_level=high&page_size=50`
   - 提交导出：`POST /export_agent_logs`，Body 包含 `params` 字段（序列化后的筛选条件）
   - 轮询状态：`GET /export_status?export_id=131231`，等待 `export_status: "success"` 且 `link` 非空后下载；
4. **错误处理**：统一检查响应中的 `success` 字段（业务层）或直接解析 `error.code`（网关层），结合 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 文档定位问题，务必记录 `request_id` 用于排查。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域不可用；
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务无分页，`params` 决定导出范围；
- **数据时效性**：`/overview` 固定返回最近 24 小时数据，不支持时间范围自定义；
- **策略不可变性**：`/policies` 接口仅提供查询，不支持启用/禁用操作（策略开关需在控制台配置）；
- **导出任务约束**：单次导出最大记录数未明确说明，若 `total_count` 过大导致超时，建议缩小筛选条件（如限定 `risk_level=high`）；
- **字段兼容性**：响应中未出现的字段（如 `skill` 在无 Managed Agent 时）返回 `null` 而非 `0`，需做空值判断（参见[查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)说明）。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)


