# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的查询与导出能力，面向开发者提供结构化数据接口。所有接口均基于统一鉴权机制和响应格式，适用于安全运营、合规审计与自动化监控场景。API 基地址需按工作空间 ID 与地域动态拼装，当前仅支持 `cn-beijing` 地域。

## 支持的模型/功能

Security API 不涉及大模型推理，而是聚焦于**Agent 安全治理数据面**，覆盖以下三类核心能力：

- **防护概况**：实时获取防护能力开关状态、模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描）。详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **资产与策略**：  
  - 查询 Agent 及其挂载资源（模型、工具、知识库等）的去重数量，以 Agent 为中心聚合；  
  - 查询全量 11 条安全策略的启用状态、所属风险域及是否免费，策略列表固定返回、不分页。该能力在 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中明确定义。
- **告警管理**：支持告警列表查询（游标分页、多维筛选）、单条告警详情获取、批量导出（异步任务）及导出状态轮询，覆盖从发现、分析到归档的完整流程。

> **注意**：文档 4（[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)）中 `asset_type` 参数说明为 `agent` / `tool` / `skill` 等，但文档 6（[查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)）示例中 `asset_type` 值为 `"app"`，且说明字段为“风险节点类型，MCP 统一归为 `tool`”。实际调用应以接口响应体中 `asset_type` 字段真实取值为准，建议以列表接口返回的 `asset_type` 枚举值为依据进行筛选。

## 关键参数

- **全局必需**：  
  - `Authorization: Bearer <your-api-key>`（HTTP Header），通过阿里云百炼控制台获取；  
  - 工作空间 ID（`workspace_id`）与地域（`region`，当前仅 `cn-beijing`）用于构造 Endpoint。
- **防护概况类接口（`/overview`, `/asset_summary`）**：无请求参数。
- **告警类接口**：  
  - 列表查询（`/agent_logs`）支持 `current_page`、`page_size`、`risk_level`、`status_list`、`asset_type` 等筛选与排序参数；  
  - 导出任务（`/export_agent_logs`）需在请求体中传入 `params` 字段，其值为**列表查询参数的 JSON 字符串序列化结果**（注意字段名大小写与驼峰格式，如 `"CurrentPage"`），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 文档；  
  - 导出状态查询（`/export_status`）必须携带 `export_id` 查询参数。

## 使用方式

1. **准备环境**：开通百炼服务，创建 API Key，并在控制台右上角获取 `workspace_id`；  
2. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`；  
3. **发起请求**：使用 `curl` 或 SDK 发起 HTTP 请求，务必携带 `Authorization` Header；  
4. **解析响应**：所有接口遵循统一响应结构：成功时 `"success": true` 且 `data` 字段包含业务数据；失败时 `"success": false` 并返回 `errorCode` 与 `errorMsg`；单项数据不可用时，对应字段返回 `null` 或 `available: false`，不影响整体响应。

示例（查询防护总览）：
```bash
curl -X GET "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
  -H "Authorization: Bearer <your-api-key>"
```

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 当前仅支持 `cn-beijing`，其他地域将返回 404 或 503 错误；  
- **时间范围固定**：`/overview` 接口固定查询最近 24 小时数据，不支持自定义时间窗口；  
- **导出任务约束**：  
  - `/export_agent_logs` 提交后需轮询 `/export_status?export_id=xxx` 获取结果；  
  - `link` 字段仅在 `export_status` 为 `"success"` 且非空时有效，下载链接有效期有限，需及时使用；  
- **错误处理**：常见错误码如 `12000093`（云安全服务异常）、`12000094`（告警查询失败）均为服务端临时不可用，建议实现指数退避重试；  
- **字段兼容性**：文档 3（[查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)）明确说明“取不到的字段返回 `null`，不返回 0”，开发者需对 `null` 做健壮性处理，不可假设默认值为 0。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


