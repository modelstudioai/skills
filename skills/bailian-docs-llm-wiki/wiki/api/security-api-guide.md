# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的程序化访问能力，支持查询防护总览、资产统计、策略列表、告警详情与批量导出。所有接口均基于统一鉴权机制与响应结构，适用于安全运营自动化与集成场景。当前仅支持 `cn-beijing` 地域。

## 支持的模型/功能

Security API 不涉及模型调用，而是面向 Agent 安全治理提供以下核心功能模块：

- **防护概况**：获取最近 24 小时防护能力开关状态、模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描）；详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **Agent 资产统计**：按业务空间汇总 Agent 数量及其挂载资源（模型、工具、技能、知识库、记忆库等），去重计数；详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **策略管理**：查询全量 11 条安全策略的启用状态、风险域归属与免费标识，策略不可分页、不可增删改；详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警生命周期**：支持告警列表查询（游标分页）、单条告警详情获取、异步导出任务提交与状态轮询；该能力覆盖模型交互、运行环境、知识记忆、身份凭证、配置组件五大风险域。

> **注意**：文档 5 中 `asset_type` 参数允许值为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 6 响应体示例中 `asset_type` 出现了 `"app"`（见 `"asset_type": "app"`），该取值未在参数说明中定义，且与文档 3 中 `risk_domain` 的分类逻辑不一致。实际使用请以文档 5 的参数定义为准，`asset_type` 应严格匹配枚举值。

## 关键参数

- **全局必需**：
  - `Authorization: Bearer <your-api-key>`：通过阿里云百炼控制台申请的 API Key，置于 HTTP Header。
  - Endpoint 拼装：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 须从控制台右上角下拉菜单获取；详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

- **告警相关接口特有**：
  - `/agent_logs` 支持筛选参数：`risk_level`（`high`/`medium`/`low`）、`status_list`（数组）、`asset_type`（枚举）、`order_by`（默认 `check_time`）、`order`（默认 `desc`）、`lang`（`zh`/`en`）。
  - `/export_agent_logs` 请求体需传 `params` 字段，其值为**列表查询参数序列化后的 JSON 字符串**（注意非嵌套对象，且字段名首字母大写，如 `"CurrentPage"`），详见文档 7 示例。
  - `/export_status` 必须携带 `export_id` 查询参数，值来自 `/export_agent_logs` 响应中的 `export_id`。

## 使用方式

1. **初始化请求**：构造 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，确保 `workspace_id` 和 API Key 正确。
2. **调用基础接口**（无参）：
   - `GET /overview`：获取防护总览（固定 24 小时窗口）。
   - `GET /asset_summary`：获取 Agent 及挂载资源统计。
   - `GET /policies`：获取全量策略列表。
3. **调用告警接口**（带参/分步）：
   - 先用 `GET /agent_logs?...` 获取告警列表及 `alert_id`；
   - 再用 `GET /agent_logs/{alert_id}` 查询详情；
   - 如需导出，先 `POST /export_agent_logs` 提交任务，再轮询 `GET /export_status?export_id=...` 直至 `export_status == "success"` 且 `link` 非空。

所有接口均遵循统一响应结构：成功返回 `{"success": true, "data": {...}}`，失败返回 `{"success": false, "errorCode": "...", "errorMsg": "..."}`。单项数据不可用时，对应字段返回 `null` 或 `available: false`，不影响整体响应。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为 `cn-beijing`，其他地域将返回错误。
- **分页机制**：告警列表 `/agent_logs` 使用游标分页（`current_page` + `page_size`），`next_page` 字段指示下一页页码；导出任务 `/export_agent_logs` 不受分页限制，导出的是当前筛选条件下的**全部匹配记录**。
- **导出任务约束**：导出任务生成后，`/export_status` 接口返回的 `link` 为临时有效 URL（有效期通常为 24 小时），需及时下载；任务状态为 `init` 或 `exporting` 时 `link` 为 `null`。
- **错误处理**：常见错误码包括 `12000093`（云安全服务异常）和 `12000094`（告警查询失败），均为 503 状态码，建议实现指数退避重试。
- **字段兼容性**：文档 4 明确说明“取不到的字段返回 `null`，不返回 0”，开发者需对数值型字段（如 `agent_count`）做 `null` 判空处理，避免类型错误。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


