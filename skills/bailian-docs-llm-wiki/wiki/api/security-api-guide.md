# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向开发者提供防护概况、资产统计、策略配置、告警查询与导出等能力。所有接口均基于工作空间隔离，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。调用前需完成工作空间 ID 获取与 API Key 配置，详见 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 支持的模型/功能

Security API 不涉及模型推理，而是聚焦于 **Agent 全生命周期安全治理**，提供以下核心功能模块：

- **防护概况**：实时获取最近 24 小时防护能力开关状态、各模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描）；
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库、记忆库等）的去重数量；
- **安全策略管理**：查询全部 11 条预置策略的启用状态、风险域分类与免费标识，策略不可写，仅可读；
- **告警全链路操作**：支持告警列表查询（游标分页、多维筛选）、单条告警详情查看、批量导出（异步任务）及导出状态轮询。

> **注意**：文档 6 中 `policy_code` 字段示例值 `"content_safety"` 与文档 4 中 `capabilities.key` 的 `"content_safety"` 命名一致，但文档 7 的 `asset_type` 参数支持值包含 `tool` / `skill` 等，而文档 5 的响应字段 `tool` / `skill` 指代资源数量——二者语义不同，前者是告警归属的资产类型，后者是挂载关系计数，开发时需严格区分上下文。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，参见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 固定为 `cn-beijing`，当前不支持其他地域 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `1` / `20`；导出接口的 `params` 字段需将此类参数 JSON 序列化后传入 |
| `risk_level` / `status` / `asset_type` | Query | string/array | 否 | 告警筛选条件，取值见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `alert_id` | Path | string | 是 | 查询告警详情的路径参数，取自告警列表响应中的 `alert_id` 字段 |
| `export_id` | Query | integer | 是 | 查询导出状态的必需参数，由 `/export_agent_logs` 返回 |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **按需调用接口**：  
   - 查询防护总览：`GET /overview`（无参数）  
   - 查询 Agent 资产：`GET /asset_summary`（无参数）  
   - 查询安全策略：`GET /policies`（无参数）  
   - 查询告警列表：`GET /agent_logs?risk_level=high&status=unhandled`  
   - 查询告警详情：`GET /agent_logs/{alert_id}`  
   - 提交导出任务：`POST /export_agent_logs`，请求体含 `params`（JSON 字符串格式的筛选条件）  
   - 查询导出状态：`GET /export_status?export_id=131231`

4. **错误处理**：  
   所有错误响应均含 `request_id`，用于问题定位；网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"code", "message", "request_id"}`；业务错误（如 `12000093`）返回嵌套结构 `{"error": {"code", "message"}}`，详见 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 不可替换为其他值。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务不支持分页，需在 `params` 中传入完整筛选条件。
- **导出任务约束**：导出接口 `/export_agent_logs` 的 `params` 字段必须为 **JSON 字符串**（非对象），且键名需首字母大写（如 `"CurrentPage"`），与列表查询的 snake_case 参数名不一致，易出错。
- **空值处理**：`/asset_summary` 响应中未统计到的字段返回 `null` 而非 `0`，客户端需做空值判断。
- **策略不可变**：`/policies` 接口仅提供只读能力，策略启用状态由控制台统一配置，API 无法修改。
- **时间范围固定**：`/overview` 固定返回最近 24 小时数据，不支持自定义时间窗口。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


