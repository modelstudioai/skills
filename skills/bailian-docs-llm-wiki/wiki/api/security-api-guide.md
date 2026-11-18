# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的程序化访问能力，支持查询防护总览、资产分布、策略开关、告警列表与详情，以及告警批量导出。所有接口均基于工作空间路由，通过 API Key 鉴权，适用于安全运营、自动化巡检与合规审计等场景。调用前需确保已开通百炼服务并获取有效 API Key 与工作空间 ID。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，覆盖以下核心功能模块：

- **防护概况**：`GET /overview`（固定查询最近 24 小时）与 `GET /asset_summary`，分别返回防护能力开关、模块覆盖状态、拦截统计，以及 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数。
- **策略管理**：`GET /policies` 返回全量 11 条安全策略（如 `prompt_attack`、`rag_poisoning`、`baseline_check`），含启用状态、风险域分组与免费标识。
- **告警生命周期**：`GET /agent_logs`（游标分页）、`GET /agent_logs/{alert_id}`（详情）、`POST /export_agent_logs`（提交导出任务）、`GET /export_status`（轮询进度与下载链接），构成完整的告警查询与导出链路。

> **注意**：文档 6 中 `/agent_logs` 的请求参数 `status_list`（array 类型）与文档 7、8、9 中实际使用的字符串型 `status` 参数存在不一致；实际调用应以文档 6 的 `status_list` 为准（支持多值筛选），其余文档未体现该字段，属描述遗漏。建议优先参考 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) 的完整参数定义。

## 关键参数

- **Endpoint 拼装**：必须使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 为控制台右上角获取的实际 ID，`region` 固定为 `cn-beijing`（当前唯一支持地域）。
- **鉴权头**：所有请求必须携带 `Authorization: Bearer <your-api-key>`，API Key 需在 [百炼控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)。
- **告警筛选参数**（`/agent_logs`）：支持 `risk_level`（`high`/`medium`/`low`）、`status_list`（数组，如 `["intercepted","unhandled"]`）、`asset_type`（`agent`/`tool`/`skill` 等）、`order_by`（默认 `check_time`）与 `order`（`desc` 默认）等，用于精准过滤。
- **导出参数**（`/export_agent_logs`）：`params` 字段需传入 JSON 字符串（非对象），内容为 `/agent_logs` 查询参数的序列化结果（如 `{"risk_level":"high","status_list":["intercepted"]}`），格式要求严格，详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)。

## 使用方式

1. **初始化**：确认工作空间 ID 与 `cn-beijing` 地域，配置 `BASE_URL`；创建并保管好 API Key。
2. **基础查询**：直接调用 `GET /overview` 或 `GET /asset_summary` 获取全局快照；调用 `GET /policies` 确认当前策略启用状态。
3. **告警操作**：
   - 先用 `GET /agent_logs?risk_level=high&status_list=["unhandled"]` 获取待处理告警列表；
   - 对关键告警 ID 调用 `GET /agent_logs/{alert_id}` 获取 `risk_detail`（原始 Prompt）与 `risk_handle`（拦截话术）；
   - 如需批量分析，用 `POST /export_agent_logs` 提交导出任务，再轮询 `GET /export_status?export_id=xxx` 直至 `export_status == "success"` 且 `link` 非空后下载 Excel。
4. **错误处理**：检查响应 `success` 字段；若为 `false`，解析 `error.code`（网关层如 `InvalidApiKey`，业务层如 `12000094`）与 `message`，结合 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 进行定位。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将返回 `BadRequest.IllegalEndpoint` 错误。
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），非传统 offset 分页；`/policies` 无分页，固定返回 11 条。
- **导出约束**：`/export_agent_logs` 的 `params` 必须是合法 JSON 字符串，且字段名需与 `/agent_logs` 接口文档完全一致（如 `CurrentPage` 首字母大写，见文档 8 示例），否则触发 `400` 参数校验失败。
- **数据时效性**：`/overview` 固定返回最近 24 小时聚合数据，不支持自定义时间范围；告警数据为实时生成，但导出任务可能因数据量延迟完成。
- **权限边界**：API Key 具有账号级权限，调用失败常见原因为 `Endpoint.AccessDenied`（工作空间不存在或无权限），请确认工作空间 ID 正确且当前账号已加入该工作空间。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)


