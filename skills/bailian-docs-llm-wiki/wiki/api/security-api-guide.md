# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向开发者提供防护概况、资产统计、策略配置、告警检索与导出等能力。所有接口均基于 RESTful 设计，统一使用 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。调用前需完成工作空间 ID 获取、API Key 配置及 Endpoint 拼装。

## 支持的模型/功能

Security API 不涉及大模型推理，而是聚焦于 Agent 全生命周期安全治理的数据面能力，覆盖以下核心功能模块：

- **防护概况**：查询最近 24 小时的防护能力开关状态、模块覆盖情况及各维度拦截统计（如 `content_safety`、`file_scan`、`skill_scan`）；详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库、记忆库等）的去重数量；详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **安全策略管理**：获取全量 11 条策略的启用状态、风险域分类与免费标识，支持策略级可观测性；详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警全链路操作**：支持告警列表分页查询（含多维筛选）、单条详情查看、异步导出任务提交与状态轮询；详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。

> **注意**：文档 1 中将 `/agent_logs` 归类为“策略与告警”子项，而文档 7 单独定义为告警功能，二者逻辑一致；但文档 1 未说明告警支持游标分页与多条件筛选，该关键能力仅在 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) 中明确描述，应以该文档为准。

## 关键参数

| 参数名 | 位置 | 类型 | 必填 | 说明 |
|--------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，参见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 固定为 `cn-beijing`，当前唯一支持地域 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` / `status` / `asset_type` | Query | string/array | 否 | 告警筛选条件，支持 `high`/`medium`/`low`、`unhandled`/`intercepted` 等取值 |
| `params` | Body (POST) | string | 是 | 导出接口中需传入 JSON 字符串化的查询参数（注意是字符串而非对象），格式需与列表接口参数严格一致 |

## 使用方式

1. **准备环境**  
   - 在百炼控制台创建 API Key（[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）；
   - 获取工作空间 ID（形如 `ws-xxxxxx`）；
   - 拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。

2. **发起请求**  
   所有接口均需携带 `Authorization: Bearer <your-api-key>` 头。示例：
   ```bash
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```

3. **处理响应**  
   - 成功响应结构统一为 `{ "success": true, "data": {...} }`；
   - 错误响应遵循标准错误格式（含 `request_id`），常见错误码见 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)；
   - 告警导出需两步：先调用 `POST /export_agent_logs` 获取 `export_id`，再轮询 `GET /export_status?export_id=xxx` 直至 `export_status == "success"` 且 `link` 非空。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他 region 将返回 `BadRequest.IllegalEndpoint`（400）；
- **告警导出参数格式**：`/export_agent_logs` 的 `params` 字段必须为 JSON **字符串**（即双层引号转义），不可直接传 JSON 对象，否则返回 `400 参数校验失败`；
- **资产统计字段语义**：`/asset_summary` 响应中缺失字段返回 `null` 而非 `0`，需做空值判断；
- **策略数量固定**：`/policies` 接口固定返回 11 条策略，不支持分页或过滤；
- **防护时间窗口**：`/overview` 仅支持最近 24 小时数据，无时间范围参数；
- **鉴权失败响应差异**：`InvalidApiKey`（401）与 `Endpoint.AccessDenied`（403）由网关层返回，响应体为扁平结构 `{"request_id", "code", "message"}`，不同于业务错误的嵌套 `error` 结构。

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


