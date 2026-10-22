# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向工作空间级安全运营场景，支持防护状态概览、资产统计、策略配置、实时告警查询与导出等核心能力。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并按工作空间路由访问。开发者应首先完成[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)与 Endpoint 拼装，再调用具体接口。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供**Agent 安全治理能力的数据面接口**，覆盖以下四类功能：

- **防护概况**：`GET /overview`（固定查询最近 24 小时防护开关状态与拦截统计）、`GET /asset_summary`（Agent 及挂载资源资产统计）  
- **策略管理**：`GET /policies`（返回全量 11 条安全策略，含启用状态与免费标识）  
- **告警生命周期**：`GET /agent_logs`（游标分页查询告警列表）、`GET /agent_logs/{alert_id}`（单条告警详情）、`POST /export_agent_logs`（提交导出任务）、`GET /export_status`（轮询导出状态与下载链接）  

> **注意**：文档 7 中 `/agent_logs` 的 `status_list` 参数在响应示例中未体现实际使用效果，且文档 10 的响应体字段 `app_name` 与文档 7 中同名字段语义不一致（前者为 Agent 名称，后者在文档 7 中定义为“应用名称”），建议以实际接口返回字段为准，优先参考 [查询告警列表](raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) 和 [查询告警详情](raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md) 的最新字段说明。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，详见 [认证](raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing` |
| `export_id` | Query | integer | 是（仅 `/export_status`） | 导出任务 ID，取自 `/export_agent_logs` 响应 |
| `alert_id` | Path | string | 是（仅 `/agent_logs/{alert_id}`） | 告警 ID，纯数字字符串，取自 `/agent_logs` 响应 `data[].alert_id` |
| `params` | Body（JSON） | string | 是（仅 `/export_agent_logs`） | 列表查询参数的 JSON 字符串（需手动序列化，非嵌套对象），例如 `{"RiskLevel":"high","OrderBy":"CheckTime"}` |

其他常用查询参数（如 `current_page`, `page_size`, `risk_level`, `lang` 等）仅适用于 `/agent_logs` 接口，详见其文档。

## 使用方式

1. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
2. **设置鉴权头**：`Authorization: Bearer <your-api-key>`  
3. **按需调用接口**：  
   - 快速查看整体防护水位 → 调用 `/overview`  
   - 统计 Agent 及关联资源规模 → 调用 `/asset_summary`  
   - 查看当前生效的安全策略 → 调用 `/policies`  
   - 查询高风险告警 → `GET /agent_logs?risk_level=high&order_by=check_time&order=desc`  
   - 导出告警 Excel → 先 `POST /export_agent_logs` 提交任务，再轮询 `GET /export_status?export_id=xxx` 直至 `export_status == "success"` 且 `link` 非空  

所有请求均需使用 HTTPS，推荐使用 `curl` 或主流 HTTP 客户端（如 Python `requests`）发起。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint` 错误（见 [错误码](raw/application-api-reference/security-api-guide/security-api-errors.md)）  
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；`/policies` 固定返回全量 11 条，无分页参数  
- **导出约束**：`/export_agent_logs` 的 `params` 字段必须为 JSON 字符串（非对象），且需与 `/agent_logs` 查询参数严格一致（包括大小写与命名风格），否则可能导出空结果或报错  
- **API Key 安全**：API Key 具有账号级权限，严禁硬编码、提交至 Git 或暴露在前端，详见 [认证](raw/application-api-reference/security-api-guide/security-api-authentication.md) 中的警告说明  
- **错误处理**：网关层错误（如 `InvalidApiKey`, `Endpoint.AccessDenied`）返回扁平结构 `{"request_id", "code", "message"}`；业务错误（如 `12000093`）返回嵌套结构，务必检查 `response.error.code` 并结合 `request_id` 排查  

> **注意**：文档 4 明确 `/overview` “固定查询最近 24 小时”，但文档 1 未说明该限制，开发者不应自行添加时间范围参数，否则将被忽略或导致 400 错误。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)


