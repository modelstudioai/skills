# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置及告警全生命周期管理（查询、详情、导出）。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成工作空间 ID 获取与 API Key 配置，方可调用。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供安全治理能力的数据面接口，共涵盖四类核心功能：

- **防护概况**：`GET /overview` 返回最近 24 小时防护能力开关、模块覆盖状态及拦截统计（如 `content_safety.hit`）；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **策略管理**：`GET /policies` 固定返回 11 条安全策略的启用状态与分类（如 `model_interaction`、`runtime_tool`），含免费策略（如 `baseline_check`）与付费策略（如 `prompt_attack`）[查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警管理**：支持完整告警链路——`GET /agent_logs`（列表，游标分页）、`GET /agent_logs/{alert_id}`（详情）、`POST /export_agent_logs`（提交导出任务）、`GET /export_status`（轮询进度与下载链接）[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。
- **错误处理**：统一错误响应结构，区分网关层（如 `InvalidApiKey`）与服务层错误（如 `12000094`），均携带 `request_id` 用于问题定位 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

> **注意**：  
> 文档 4（查询防护总览）声明 `/overview` “固定查询最近 24 小时”，但文档 1（概览）未明确时间范围；实际行为以文档 4 为准，该接口不支持时间参数。  
> 文档 9（查询安全策略）中 `policy_code` 列表含 `network_protection`，而文档 4 的 `protection.key` 列表含 `mcp`；二者语义不同（前者为策略标识，后者为防护模块），无直接映射关系，不可混用。

## 关键参数

- **全局必需**：`Authorization: Bearer <your-api-key>`（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)），`workspace_id` 与 `region`（当前仅 `cn-beijing`）用于拼装 Endpoint。
- **告警列表（`/agent_logs`）**：`current_page`（默认 1）、`page_size`（默认 20）、`risk_level`（`high`/`medium`/`low`）、`asset_type`（`agent`/`tool`/`skill` 等）、`order_by` 与 `order`（默认 `check_time desc`）。
- **导出告警（`/export_agent_logs`）**：`params` 字段必须为 JSON 字符串（非对象），内容需与 `/agent_logs` 查询参数严格一致（字段名大小写敏感，如 `RiskLevel` 而非 `risk_level`）。
- **导出状态（`/export_status`）**：`export_id`（整型，取自导出接口响应）为唯一必填参数。

## 使用方式

1. **准备环境**：在百炼控制台获取 `workspace_id`（右上角下拉菜单）和 API Key（[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)）。
2. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。
3. **调用示例（curl）**：
   ```bash
   # 查询防护总览
   curl -X GET "https://my-ws.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer sk-xxx"
   
   # 查询高风险告警（第1页，20条）
   curl -X GET "https://my-ws.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/agent_logs?risk_level=high&current_page=1&page_size=20" \
     -H "Authorization: Bearer sk-xxx"
   
   # 提交导出任务（参数需 JSON 字符串化）
   curl -X POST "https://my-ws.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/export_agent_logs" \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\",\"CurrentPage\":1,\"PageSize\":20}"}'
   ```
4. **轮询导出状态**：使用返回的 `export_id` 调用 `/export_status?export_id=12345`，直至 `export_status` 为 `"success"` 且 `link` 非空。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 当前仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint`（400）。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务无分页，`params` 决定导出全量匹配记录。
- **参数格式**：导出接口的 `params` 必须是 JSON 字符串（如 `"\"RiskLevel\":\"high\""`），而非 JSON 对象，否则返回 `400` 参数校验失败。
- **字段兼容性**：告警详情响应中 `asset_type` 取值可能为 `app`（见文档 6 示例），但告警列表筛选参数 `asset_type` 仅接受 `agent`/`tool`/`skill` 等（见文档 5 表格），二者不完全对齐，筛选时请以列表接口定义为准。
- **空值处理**：资产统计接口（`/asset_summary`）对未挂载的资源返回 `null` 而非 `0`，需做空值判断。
- **权限边界**：`Endpoint.AccessDenied`（403）表示工作空间不存在或当前 API Key 无访问权限，需检查工作空间 ID 正确性及 API Key 所属账号是否开通百炼并绑定该工作空间。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)


