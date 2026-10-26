# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向开发者提供防护状态、策略配置、资产统计及告警全生命周期操作能力。所有接口均基于 RESTful 设计，统一使用 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。调用前需完成工作空间 ID 获取与 API Key 配置。

## 支持的模型/功能

Security API 不涉及模型推理，而是聚焦于 **Agent 运行时安全治理**，提供以下核心功能模块：

- **防护概况**：实时获取防护能力开关状态、各模块覆盖情况及内容安全/文件扫描/技能扫描等维度的拦截统计（见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)）；
- **资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库、记忆库等）数量（见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)）；
- **策略管理**：查询全部 11 条预置安全策略的启用状态、所属风险域及是否免费（见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)）；
- **告警管理**：支持告警列表分页查询、单条详情查看、条件筛选导出及导出任务状态轮询（含 `/agent_logs`、`/agent_logs/{alert_id}`、`/export_agent_logs`、`/export_status` 四个接口）。

> **注意**：文档 5 中 `asset_type` 参数支持值包含 `channel` 和 `memory`，但文档 7 的响应字段说明中明确 `memory` 仅适用于 Agent 1.0/2.0，而 `channel` 统计排除已删除/过期渠道；实际使用时需结合 Agent 类型判断字段有效性，避免对 Managed Agent 误查 `memory` 字段。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `alert_id` | Path | string | 是（`/agent_logs/{alert_id}`） | 告警唯一标识，取自告警列表响应中的 `alert_id` 字段 |
| `export_id` | Query | integer | 是（`/export_status`） | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `params` | Body（POST） | string | 是（`/export_agent_logs`） | 告警列表查询参数的 JSON 字符串（需序列化），非嵌套对象格式 |

其他常用查询参数（如 `risk_level`、`status_list`、`order_by` 等）详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)，均以 query string 形式传递。

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **发起请求**：  
   - 查询防护总览：`GET /overview`（无参数）  
   - 查询资产汇总：`GET /asset_summary`（无参数）  
   - 查询策略列表：`GET /policies`（无参数）  
   - 查询告警列表：`GET /agent_logs?risk_level=high&page_size=50`  
   - 查询告警详情：`GET /agent_logs/{alert_id}`  
   - 提交导出任务：`POST /export_agent_logs`，Body 含 `params` 字段（如 `{"RiskLevel":"high","OrderBy":"CheckTime"}` 的 JSON 字符串）  
   - 轮询导出状态：`GET /export_status?export_id=12345`

所有请求均返回标准响应结构：`{"success": boolean, "data": any, "request_id": string}`。错误响应结构参见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 不可替换为其他值；
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持 offset 分页；策略与资产接口无分页；
- **导出约束**：`/export_agent_logs` 的 `params` 字段必须为合法 JSON 字符串，且字段名需与告警列表接口的 query 参数名一致（如 `RiskLevel` 而非 `risk_level`），否则导出任务将失败；
- **权限范围**：API Key 具有账号级权限，但仅返回当前工作空间内 Agent 相关数据；
- **错误处理**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id","code","message"}`；业务错误（如 `12000093`）返回嵌套结构，需解析 `error.code`；
- **时间范围**：防护总览接口固定查询最近 24 小时数据，不可自定义时间窗口。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)


