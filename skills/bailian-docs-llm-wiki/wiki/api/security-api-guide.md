# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心安全运营场景。所有接口均基于工作空间路由，需通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者应首先完成[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)并确认工作空间 ID 与地域配置。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全运营数据服务**，当前支持以下 6 类功能：

- **防护概况**：`GET /overview` 返回最近 24 小时各模块防护开关状态与拦截统计（如 `content_safety.hit`）；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、知识库等）的去重计数。
- **策略管理**：`GET /policies` 固定返回 11 条安全策略全量信息，含启用状态、风险域（如 `model_interaction`）与是否免费（如 `baseline_check`）。
- **告警生命周期**：`GET /agent_logs`（游标分页）、`GET /agent_logs/{alert_id}`（单条详情）、`POST /export_agent_logs`（导出任务提交）与 `GET /export_status`（进度与下载链接查询）构成完整告警处理链路。

> **注意**：文档 5 中 `policy_code` 列表明确包含 `vulnerability_scan`（免费），但文档 1 的“可用 API”表格未列出该策略接口；实际策略查询能力以 [查询安全策略](raw/application-api-reference/security-api-guide/security-api-policies.md) 文档为准，该接口已支持全部 11 条策略。

## 关键参数

- **全局必需**：`Authorization: Bearer <API_KEY>`（见 [认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)），`workspace_id` 与 `region=cn-beijing` 构成 Endpoint（如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`）。
- **告警列表筛选**：`risk_level`（`high`/`medium`/`low`）、`status_list`（多值数组）、`asset_type`（`agent`/`tool`/`knowledge_base` 等）、`order_by`（默认 `check_time`）与 `order`（默认 `desc`）。
- **导出任务**：`POST /export_agent_logs` 的请求体中 `params` 字段必须为**字符串化 JSON**（非原始对象），且字段名需首字母大写（如 `"CurrentPage"`），与 [导出告警](raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 示例严格一致。

## 使用方式

1. **初始化**：获取 API Key 并确认工作空间 ID（控制台右上角下拉菜单）；拼装 BASE_URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。
2. **快速验证**：  
   ```bash
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```
3. **告警导出流程**：  
   - 调用 `POST /export_agent_logs` 提交参数（如 `{"RiskLevel":"high"}` 字符串化）→ 获取 `export_id`；  
   - 轮询 `GET /export_status?export_id=xxx` → 待 `export_status == "success"` 且 `link` 非空后下载 Excel。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，其他 region 将返回 `BadRequest.IllegalEndpoint` 错误（见 [Security API 错误码](raw/application-api-reference/security-api-guide/security-api-errors.md)）。
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；`/policies` 不分页，固定返回 11 条。
- **数据时效性**：`/overview` 仅返回最近 24 小时数据，无时间范围参数；告警列表默认按 `check_time` 倒序，最新告警优先。
- **字段兼容性**：`/asset_summary` 响应中缺失字段返回 `null`（非 `0` 或省略），需做空值判断；`/agent_logs` 响应中 `stats` 对象的 `total` 与 `data` 数组长度可能不一致（因分页）。
- **错误处理**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"code","message","request_id"}`；业务错误（如 `12000094`）嵌套在 `error.code` 中，务必检查 `request_id` 排查问题。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)


