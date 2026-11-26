# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、安全策略、告警管理三大核心场景。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成工作空间 ID 获取与 API Key 配置，方可调用。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供**安全治理能力的数据面接口**，聚焦以下四类功能：

- **防护概况**：实时获取防护能力开关状态、模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描）。固定查询最近 24 小时数据，详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **安全策略**：查询全部 11 条预置策略的启用状态、风险域归属与免费标识，支持快速识别策略配置缺口。策略列表固定返回，不分页，详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警管理**：包括告警列表（游标分页）、单条告警详情、批量导出及导出状态轮询，支持按风险等级、资产类型、处置状态等多维筛选。
- **Agent 资产统计**：以 Agent 为中心，聚合挂载的模型、工具、技能、知识库等资源数量（去重），用于评估攻击面广度，详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。

> **注意**：文档 6（查询告警列表）中 `asset_type` 参数取值包含 `channel` 和 `memory`，但文档 10（查询 Agent 资产）明确说明 `memory` 仅适用于 Agent 1.0/2.0，而 `channel` 在资产统计中定义为“发布渠道数”，二者语义层级不同。实际使用时请以告警响应体中 `asset_type` 字段的实际返回值为准，避免依赖文档间不一致的枚举映射。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 鉴权凭证，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `alert_id` | Path | string | 是（告警详情） | 取自 `/agent_logs` 响应中的 `alert_id` 字段，纯数字字符串 |
| `export_id` | Query | integer | 是（导出状态） | 取自 `/export_agent_logs` 响应中的 `export_id` 字段 |
| `params` | Body（POST） | string | 是（导出） | 告警列表查询参数的 JSON 字符串（非嵌套对象），需手动序列化，详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |

其他常用查询参数（如 `risk_level`, `asset_type`, `page_size` 等）均位于 URL Query 中，具体见各接口文档。

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **发起请求**：  
   - 查询类（GET）：直接附加参数到路径后，例如 `/overview`、`/policies`、`/agent_logs?risk_level=high`  
   - 导出类（POST）：`Content-Type: application/json`，请求体含 `params` 字段（JSON 字符串格式）

4. **处理响应**：  
   - 所有成功响应均为 `{ "success": true, "data": ... }` 结构  
   - 错误响应统一为 `{ "type": "error", "error": { "code": "...", "message": "..." }, "request_id": "..." }`，需结合 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 解析 `error.code` 并记录 `request_id` 用于排查

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint`（400）。
- **分页机制**：告警列表（`/agent_logs`）使用游标分页，依赖 `next_page` 字段推进；策略（`/policies`）和资产（`/asset_summary`）接口无分页，固定返回全量。
- **导出参数约束**：`/export_agent_logs` 的 `params` 字段必须是合法 JSON 字符串（如 `"{\"risk_level\":\"high\"}"`），若传入对象或未转义将导致 `400` 参数校验失败。
- **时间范围固定**：防护总览（`/overview`）仅支持最近 24 小时，不支持自定义时间窗口。
- **字段空值处理**：资产统计接口（`/asset_summary`）中未统计到的字段返回 `null` 而非 `0`，调用方需做空值判断。
- **API Key 权限**：API Key 具有账号级权限，严禁硬编码、提交至代码仓库或暴露在前端，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) 文档警告。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)


