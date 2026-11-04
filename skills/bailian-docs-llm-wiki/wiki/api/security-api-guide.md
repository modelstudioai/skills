# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向开发者提供防护概况、策略配置、资产统计及告警全生命周期操作能力。所有接口均基于 RESTful 设计，需通过 [API Key 鉴权](../concepts/api-key-authentication.md)，并按工作空间与地域拼装 Endpoint。调用前请确保已开通百炼服务并完成[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)配置。

## 支持的模型/功能

Security API 不涉及模型推理，而是聚焦于 **Agent 安全治理数据面**，提供以下核心功能模块：

- **防护概况**：查询最近 24 小时防护能力开关状态、模块覆盖情况及拦截统计（`/overview`）；  
- **资产统计**：按业务空间汇总 Agent 及其挂载资源（模型、工具、技能、知识库等）数量（`/asset_summary`）；  
- **策略管理**：获取全部 11 条安全策略的启用状态、分组与免费标识（`/policies`）；  
- **告警管理**：支持告警列表查询（游标分页）、单条详情获取、批量导出及导出状态轮询（`/agent_logs`, `/agent_logs/{alert_id}`, `/export_agent_logs`, `/export_status`）。

> **注意**：文档 5 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 4 的 `capabilities` 字段未体现基线与漏洞类能力开关。该差异表明能力开关（`capabilities`）与策略启停（`policies`）属于不同控制平面，开发者应以 `/policies` 接口为准进行策略生效判断。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，参见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看 |
| `region` | Host | string | 是 | 固定为 `cn-beijing`（当前唯一支持地域） |
| `alert_id` | Path | string | 是（仅 `/agent_logs/{alert_id}`） | 告警唯一标识，取自 `/agent_logs` 响应中的 `alert_id` 字段 |
| `export_id` | Query | integer | 是（仅 `/export_status`） | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` / `status` / `asset_type` 等 | Query | string/array | 否 | 告警筛选条件，详见[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |

## 使用方式

1. **构造 Endpoint**：  
   ```
   https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security
   ```

2. **发起请求（以查询防护总览为例）**：  
   ```bash
   curl -X GET "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer sk-xxx"
   ```

3. **处理响应**：  
   - 所有成功响应均为 `{ "success": true, "data": {...} }` 结构；  
   - 错误响应遵循统一格式（含 `request_id`），详见[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)；  
   - 告警导出需三步联动：`POST /export_agent_logs` → 轮询 `GET /export_status?export_id=...` → `link` 就绪后下载。

## 限制和注意事项

- **鉴权与权限**：API Key 具备账号级权限，严禁硬编码或提交至公开仓库；Endpoint.AccessDenied（403）表示工作空间不存在或当前账号无访问权限。  
- **地域限制**：所有请求必须使用 `cn-beijing` 地域，其他 region 将返回 `BadRequest.IllegalEndpoint`（400）。  
- **分页机制**：告警列表采用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务不支持并发提交相同筛选条件。  
- **数据时效性**：`/overview` 固定返回最近 24 小时数据，不可指定时间范围；`/asset_summary` 为实时快照，无缓存延迟。  
- **字段空值处理**：`/asset_summary` 响应中缺失字段返回 `null` 而非 `0`，调用方需做空值判断（如 `data.skill ?? 0`）。

## 来源文档

- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)


