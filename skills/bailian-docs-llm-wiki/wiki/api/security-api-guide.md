# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向开发者提供防护状态、策略配置、资产统计及告警全生命周期操作能力。所有接口均基于 RESTful 设计，统一使用 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。调用前需完成工作空间 ID 获取与地域配置，并参考[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)文档完成鉴权准备。

## 支持的模型/功能

Security API 不涉及模型推理，而是聚焦于 Agent 安全治理能力的数据面暴露，覆盖以下四类核心功能：

- **防护概况**：实时获取防护能力开关状态、模块覆盖情况及各维度拦截统计（如内容安全、文件扫描、技能扫描），固定查询最近 24 小时窗口，详见[查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）数量，以 Agent 为中心去重统计，无分页、无参数，详见[查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **策略管理**：查询全量 11 条安全策略的启用状态、风险域归属与免费属性，返回固定列表（不分页），策略类型涵盖模型交互、运行环境、知识记忆、身份凭证与配置组件五大风险域，详见[查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警管理**：支持告警列表查询（游标分页+多维筛选）、单条告警详情获取、批量导出（[异步任务](../concepts/asynchronous-task.md)）及导出状态轮询，是安全运营闭环的关键链路。

> **注意**：文档 7 中 `asset_type` 参数允许值为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 8 响应体示例中 `asset_type` 出现了 `"app"`（见 `"asset_type": "app"`），该值未在文档 7 的枚举中定义，且与文档 5 中策略分组逻辑不一致。实际调用应以文档 7 的枚举为准，`"app"` 属于过时或错误示例。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 需通过[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)文档指引创建并保管 |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取，用于拼装 Endpoint |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，硬编码在 Endpoint 中 |
| `alert_id` | Path | string | 是（告警详情） | 取自 `/agent_logs` 响应中的 `alert_id` 字段，纯数字字符串 |
| `export_id` | Query | integer | 是（导出状态） | 取自 `/export_agent_logs` 响应中的 `export_id` 字段 |
| `current_page`, `page_size`, `risk_level`, `status`, `asset_type` 等 | Query | 各异 | 否（告警列表） | 全部为可选筛选与分页参数，详见[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `params` | Body（JSON） | string | 是（导出） | 告警列表查询参数的 JSON 字符串序列化值（注意：是字符串而非对象），字段名首字母大写（如 `"CurrentPage"`），详见[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |

## 使用方式

1. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
2. **设置请求头**：`Authorization: Bearer <your-api-key>`  
3. **发起请求**：根据所需功能选择对应 HTTP 方法与路径：
   - 查询防护总览：`GET /overview`
   - 查询 Agent 资产：`GET /asset_summary`
   - 查询安全策略：`GET /policies`
   - 查询告警列表：`GET /agent_logs?risk_level=high&page_size=50`
   - 查询告警详情：`GET /agent_logs/{alert_id}`
   - 提交导出任务：`POST /export_agent_logs`，Body 包含 `params` 字段（如 `{"RiskLevel":"high"}` 的 JSON 字符串）
   - 查询导出状态：`GET /export_status?export_id=131231`

所有接口均返回标准响应结构：`{"success": boolean, "data": any, ...}`。错误响应遵循统一格式，含 `request_id` 用于问题定位，详见[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 固定为 `cn-beijing`，不支持其他地域。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），非传统 offset 分页；资产、策略、防护总览接口均无分页。
- **导出参数一致性**：`/export_agent_logs` 的 `params` 字段必须为 JSON 字符串（非对象），且字段命名需与列表接口实际接收的参数名完全一致（如 `CurrentPage` 而非 `current_page`），否则导出结果可能为空或不匹配。
- **空值处理**：响应中未获取到的字段（如 `file_name`）返回 `null`，而非 `0` 或空字符串，客户端需做 `null` 安全判断。
- **权限与路由**：`Endpoint.AccessDenied`（403）表示工作空间不存在或当前 API Key 无访问权限；`BadRequest.IllegalEndpoint`（400）表示 `workspace_id` 格式或路由无效，请核对控制台获取的 ID。
- **服务可用性**：云安全服务异常（错误码 `12000093`）或告警查询失败（`12000094`）时返回 503，建议实现指数退避重试。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


