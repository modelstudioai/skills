# security api guide

Security API 提供对 Agent 安全防护状态、策略配置与安全告警的程序化访问能力，支持防护概况查询、资产统计、策略管理、告警检索与批量导出。所有接口均基于统一鉴权机制，返回结构化 JSON 响应。开发者需先开通百炼服务并获取 API Key 与工作空间 ID，方可调用。

## 支持的模型/功能

Security API 不涉及模型推理，而是面向 Agent 安全治理的**数据面接口**，覆盖以下核心功能模块：

- **防护概况**：`GET /overview` 返回最近 24 小时各防护能力（如 `content_safety`、`supply_chain_scan`）与模块（如 `flow_agent`、`knowledge_base`）的启用状态及拦截统计；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数。  
- **策略管理**：`GET /policies` 固定返回全部 11 条安全策略（含免费策略 `baseline_check` 和 `vulnerability_scan`），包含 `policy_code`、`risk_domain`、`enabled` 等字段，详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。  
- **告警全生命周期**：`GET /agent_logs` 支持游标分页与多维筛选；`GET /agent_logs/{alert_id}` 获取单条告警详情（含 `risk_detail` Markdown 分析）；`POST /export_agent_logs` 提交导出任务；`GET /export_status` 查询进度与下载链接。

> **注意**：文档 2 明确说明 `/overview` “固定查询最近 24 小时”，但文档 1 的“可用 API”表格未注明时间范围限制，实际使用中应以文档 2 为准。该行为在 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中有明确定义。

## 关键参数

- **Endpoint 拼装**：必须按 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security` 格式构造，其中 `workspace_id` 为控制台获取的实际 ID，`region` 当前仅支持 `cn-beijing`（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）。  
- **鉴权**：所有请求必须在 Header 中携带 `Authorization: Bearer <your-api-key>`。  
- **告警筛选参数**：`/agent_logs` 支持 `risk_level`（`high`/`medium`/`low`）、`status`、`asset_type`（如 `tool`、`knowledge_base`）等过滤；`/export_agent_logs` 的 `params` 字段需传入**序列化后的 JSON 字符串**（非原始对象），且键名需首字母大写（如 `"CurrentPage"`），与列表接口参数名不一致（见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 示例）。

## 使用方式

1. **初始化**：从百炼控制台获取 API Key 与工作空间 ID；确认地域为 `cn-beijing`。  
2. **构造请求**：以 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security` 为基础路径。  
3. **调用示例**：  
   - 查询总览：`curl -X GET "$BASE_URL/overview" -H "Authorization: Bearer $API_KEY"`  
   - 查询高风险告警：`curl -X GET "$BASE_URL/agent_logs?risk_level=high&page_size=50" -H "Authorization: Bearer $API_KEY"`  
   - 导出告警：`curl -X POST "$BASE_URL/export_agent_logs" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\"}"}'`  
4. **轮询导出状态**：用上一步返回的 `export_id` 调用 `GET /export_status?export_id=xxx`，待 `export_status` 为 `success` 且 `link` 非空后下载 Excel。

## 限制和注意事项

- **地域限制**：所有接口仅支持 `cn-beijing` 地域，其他地域 Endpoint 将返回 404 或 503（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）。  
- **分页机制**：告警列表 `/agent_logs` 使用游标分页（`current_page`/`page_size`），而策略 `/policies` 为全量返回、不分页。  
- **空值处理**：当某项数据不可用时，接口不报错，对应字段返回 `null`（如 `/asset_summary` 中未挂载的知识库返回 `"knowledge_base": null`），而非 `0`。  
- **导出参数兼容性**：`/export_agent_logs` 的 `params` 字段要求 JSON 字符串内键名首字母大写（如 `CurrentPage`），与 `/agent_logs` 接口实际接受的小写参数名（`current_page`）不一致，需手动转换，否则筛选条件可能失效。  
- **错误处理**：通用错误码如 `12000093`（云安全服务异常）和 `12000094`（告警查询失败）均返回 HTTP 503，建议实现指数退避重试。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


