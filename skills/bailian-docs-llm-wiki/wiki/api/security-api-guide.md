# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、实时告警及批量导出等核心场景。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)并确认工作空间权限，方可调用。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，提供以下五类功能：

- **防护概况**：`GET /overview` 返回最近 24 小时各模块防护开关状态与拦截统计（如 `content_safety.hit`）；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、知识库等）的去重计数。
- **策略管理**：`GET /policies` 固定返回 11 条安全策略的启用状态与分类（如 `prompt_attack` 属于 `model_interaction` 分组），含免费策略（如 `baseline_check`）。
- **告警查询**：`GET /agent_logs` 支持游标分页与多维筛选（`risk_level`、`asset_type`、`status_list` 等）；`GET /agent_logs/{alert_id}` 获取单条告警的原始风险详情（`risk_detail`）与处置建议（`risk_handle`）。
- **告警导出**：`POST /export_agent_logs` 提交导出任务（参数需 JSON 字符串化），`GET /export_status` 轮询进度并获取下载链接。
- **错误处理**：统一错误结构含 `request_id`，网关层错误（如 `InvalidApiKey`）与业务层错误（如 `12000094`）响应格式不同，详见[错误码](raw/application-api-reference/security-api-guide/security-api-errors.md)。

> **注意**：文档 7 中 `asset_type` 参数支持值为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 8 的响应示例中 `asset_type` 出现了 `"app"`（见 `"asset_type": "app"`），该值未在文档 7 的枚举中定义，实际调用应以文档 7 列出的六种类型为准。

## 关键参数

- **全局必需**：
  - `Authorization: Bearer <your-api-key>`：通过 Header 传递，获取方式见[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)。
  - Endpoint 拼装：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 必须从百炼控制台右上角下拉菜单获取。
- **告警列表（`/agent_logs`）**：
  - `page_size`（默认 20）、`current_page`（默认 1）：分页控制；
  - `risk_level`（`high`/`medium`/`low`）、`status_list`（数组）、`asset_type`（严格限于六种枚举值）：筛选条件；
  - `order_by`（默认 `check_time`）、`order`（默认 `desc`）：排序控制。
- **导出告警（`/export_agent_logs`）**：
  - `params`：**必需**，为列表查询参数的 JSON 字符串（非对象），例如 `"{\"risk_level\":\"high\",\"asset_type\":\"tool\"}"`；
  - `lang`：可选，`zh` 或 `en`，影响导出文件语言。

## 使用方式

1. **初始化**：确认已开通百炼服务，创建 API Key，并从控制台获取 `workspace_id`。
2. **构造请求**：
   - 设置 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`；
   - 所有请求添加 Header：`Authorization: Bearer $BAILIAN_API_KEY`。
3. **典型流程（告警导出）**：
   - 先调用 `GET /agent_logs?risk_level=high&page_size=50` 获取目标数据概览；
   - 再 `POST /export_agent_logs` 提交相同筛选条件（`params` 字段）；
   - 用返回的 `export_id` 轮询 `GET /export_status?export_id=xxx`，直到 `export_status == "success"` 且 `link` 非空；
   - 下载 Excel 文件。
4. **调试建议**：所有错误响应均含 `request_id`，排查问题时务必提供该字段；首次调用推荐从 `GET /overview` 开始验证连通性。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他地域将返回 `BadRequest.IllegalEndpoint` 错误。
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；`/policies` 无分页，固定返回 11 条。
- **导出约束**：`/export_agent_logs` 的 `params` 字段必须是合法 JSON 字符串，若传入对象（如 `{risk_level: "high"}`）将导致 `400` 参数校验失败。
- **数据时效性**：`/overview` 固定查询最近 24 小时数据，不可指定时间范围；告警数据为实时检测结果，无延迟说明。
- **权限隔离**：API 仅返回当前工作空间内 Agent 相关数据，跨工作空间调用会触发 `Endpoint.AccessDenied`（403）。

> **注意**：文档 4 明确说明 `/overview` “固定查询最近 24 小时”，但文档 1 的“可用 API”表格未注明此限制，开发者应以文档 4 的描述为准。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)


