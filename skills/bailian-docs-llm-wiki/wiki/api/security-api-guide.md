# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的查询与导出能力，面向工作空间维度统一暴露。所有接口均基于 `/api/v1/agentstudio/security` 路径前缀，需通过 API Key 鉴权，并按工作空间 ID 与地域拼装 Endpoint。开发者可据此监控防护覆盖、评估风险分布、响应安全事件。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全治理数据面能力**，覆盖以下三类核心功能：

- **防护概况**：查询整体防护能力开关、模块覆盖状态及各维度拦截统计（如内容安全、文件扫描、技能扫描），固定返回最近 24 小时数据。详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **策略与资产**：查询全量 11 条安全策略的启用状态与分类（如 `prompt_attack`、`rag_poisoning`），以及 Agent 及其挂载资源（模型、工具、知识库等）的去重统计。详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 和 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **告警管理**：支持告警列表查询（游标分页、多维筛选）、单条告警详情获取（含原始风险上下文与拦截话术），以及批量导出（[异步任务](../concepts/asynchronous-task.md) + 状态轮询）。详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。

> **注意**：文档 7 中 `asset_type` 参数支持值包含 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 8 的响应体说明中 `asset_type` 示例值为 `"app"`，且未在枚举中列出；实际应以文档 7 的定义为准，`app` 类型不合法，调用时请避免使用。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，API Key 须通过[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)获取 |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` | Query | string | 否 | 告警筛选值：`high` / `medium` / `low` |
| `status_list` | Query | array | 否 | 支持多值筛选处置状态（如 `["unhandled","intercepted"]`） |
| `params` | Body (POST) | string | 是 | 导出接口中需将筛选参数 JSON 序列化为字符串（注意字段名大小写需与列表接口一致，如 `CurrentPage` 而非 `current_page`） |

## 使用方式

1. **准备环境**：开通百炼服务，创建 API Key，并确认工作空间 ID 与地域（当前仅 `cn-beijing`）；
2. **构造 Endpoint**：格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`；
3. **发起请求**：
   - 查询类（GET）：直接附加查询参数，如 `/agent_logs?risk_level=high&order_by=check_time&order=desc`；
   - 导出类（POST）：`Content-Type: application/json`，`params` 字段传入序列化后的筛选条件 JSON 字符串；
   - 详情类（GET）：路径中嵌入 `alert_id`，如 `/agent_logs/4289016`；
4. **处理响应**：检查 `success` 字段与 HTTP 状态码；错误时参考 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 解析 `error.code` 与 `message`。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将返回 `BadRequest.IllegalEndpoint`（400）；
- **导出任务约束**：导出接口 `/export_agent_logs` 不支持分页参数（如 `current_page`），其 `params` 字符串仅用于指定筛选条件，导出范围为该条件匹配的**全部记录**；
- **告警字段一致性**：告警列表响应中 `asset_type` 字段值严格限定为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`；告警详情响应中同名字段若返回 `"app"`，属文档描述偏差，实际接口不会返回该值；
- **空值处理**：资产统计接口 `/asset_summary` 对未挂载的资源项返回 `null` 而非 `0`，调用方需做空值判断；
- **错误排查**：所有错误响应均携带 `request_id`，可用于工单提报；网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）结构扁平，业务层错误（如 `12000093`）嵌套在 `error` 对象内。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


