# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置及告警全生命周期管理（查询、详情、导出）。所有接口均基于统一鉴权机制，通过工作空间专属 Endpoint 访问，适用于安全运营与自动化审计场景。详细设计与行为约束请参考原始文档。

## 支持的模型/功能

Security API 当前支持以下核心功能模块：

- **防护概况**：`GET /overview` 返回最近 24 小时防护能力开关、模块覆盖状态及内容安全/文件扫描/技能扫描三类拦截统计；`GET /asset_summary` 按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）去重数量。
- **策略与告警**：`GET /policies` 固定返回 11 条安全策略（含免费基线检查与漏洞检测），按 `risk_domain` 分组；`GET /agent_logs` 支持游标分页与多维筛选（风险等级、处置状态、资产类型等）；`GET /agent_logs/{alert_id}` 获取单条告警完整上下文；`POST /export_agent_logs` 提交导出任务，`GET /export_status` 查询进度与下载链接。

> **注意**：文档 7 明确说明 `/policies` 接口“共 11 条策略，固定返回全量，不分页”，而文档 1 的“可用 API”表格中未注明该限制，开发者应以 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 为准。

## 关键参数

- **Endpoint 拼装**：必须使用 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`（当前仅支持 `cn-beijing` 地域），详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。
- **鉴权**：所有请求需在 Header 中携带 `Authorization: Bearer <your-api-key>`。
- **告警导出参数**：`POST /export_agent_logs` 的 `params` 字段为 JSON 字符串（非嵌套对象），必须严格匹配 `/agent_logs` 查询时使用的筛选条件序列化结果，例如 `{"RiskLevel":"high","OrderBy":"CheckTime"}` —— 注意字段名大小写与下划线风格需与列表接口响应一致。
- **分页与筛选**：`/agent_logs` 支持 `current_page`/`page_size` 游标分页，以及 `risk_level`、`status_list`（数组）、`asset_type` 等灵活筛选；`/export_agent_logs` 不直接接收这些参数，而是通过 `params` 字符串透传。

## 使用方式

1. **初始化**：在阿里云百炼控制台开通服务并创建 API Key，同时获取工作空间 ID（形如 `ws-xxxxxx`）。
2. **调用防护接口**：
   - 查询总览：`curl -X GET "$BASE_URL/overview" -H "Authorization: Bearer $API_KEY"`
   - 查询资产：`curl -X GET "$BASE_URL/asset_summary" -H "Authorization: Bearer $API_KEY"`
3. **调用告警接口**：
   - 列表查询：`curl -X GET "$BASE_URL/agent_logs?risk_level=high&lang=zh" -H "Authorization: Bearer $API_KEY"`
   - 详情查询：`curl -X GET "$BASE_URL/agent_logs/4289016" -H "Authorization: Bearer $API_KEY"`
4. **导出告警**：
   - 提交任务：`curl -X POST "$BASE_URL/export_agent_logs" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d '{"lang":"zh","params":"{\\"RiskLevel\\":\\"high\\"}"}'`
   - 轮询状态：`curl -X GET "$BASE_URL/export_status?export_id=131231" -H "Authorization: Bearer $API_KEY"`，仅当 `export_status == "success"` 且 `link` 非空时可下载 Excel。

> **注意**：文档 5 中 `params` 示例使用双引号转义（`\"RiskLevel\"`），而文档 8 的请求示例 URL 参数使用下划线（`risk_level`），二者字段命名不一致。实际调用时，`params` 内部 JSON 的键名必须与 `/agent_logs` 接口文档中定义的**请求参数名完全一致**（即 `risk_level`，非 `RiskLevel`），否则导出可能返回空结果或错误。请以 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) 的参数定义为准。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域暂不可用。
- **时间范围固定**：`/overview` 接口固定查询最近 24 小时数据，不支持自定义时间窗口。
- **字段空值处理**：响应中不可用字段返回 `null`（如 `file_name` 在非 Skill 告警中为 `null`），而非 `0` 或空字符串；`data` 字段始终存在，但可能为 `null` 或空对象/数组。
- **错误处理**：通用错误码如 `12000093`（云安全服务异常）、`12000094`（告警查询失败）均为 503，建议实现指数退避重试；单项数据不可用时不触发整体失败，对应字段置为 `null` 或 `available: false`。
- **导出可靠性**：导出任务状态需轮询 `/export_status`，`progress` 字段仅作参考，最终以 `export_status == "success"` 且 `link` 非空为下载依据；链接有效期有限，需及时下载。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)


