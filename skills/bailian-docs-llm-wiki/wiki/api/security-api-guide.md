# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)并获取工作空间 ID，方可调用。

## 支持的模型/功能

Security API 不涉及模型推理，而是面向 Agent 安全治理的**数据面能力接口**，当前支持以下 6 类功能：

- **防护概况**：固定查询最近 24 小时的防护能力开关、模块覆盖状态及拦截统计（如 `content_safety`、`file_scan`）  
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）数量，去重计数  
- **安全策略查询**：返回全量 11 条策略（如 `prompt_attack`、`rag_poisoning`），含启用状态、风险域与是否免费  
- **告警列表查询**：游标分页，支持按风险等级（`high`/`medium`/`low`）、处置状态、资产类型（`agent`/`tool`/`knowledge_base` 等）多维筛选  
- **告警详情查询**：通过 `alert_id` 获取原始风险上下文、攻击模式分析（`risk_detail` 字段含 Markdown 格式摘要）及拦截话术  
- **告警导出**：异步提交导出任务，支持按相同筛选条件导出 Excel，通过 `/export_status` 轮询进度与下载链接  

> **注意**：文档 5 中 `policy_code` 列表包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 1 的“可用 API”表格未列出 `/policies` 接口的说明性文字，仅以表格形式呈现；实际以[查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)为准。

## 关键参数

| 参数 | 位置 | 必填 | 类型 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | 是 | string | `Bearer <your-api-key>`，详见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | 是 | string | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | 是 | string | 固定为 `cn-beijing`，其他地域暂不支持 |
| `alert_id` | Path | 是（仅 `/agent_logs/{alert_id}`） | string | 告警 ID，取自告警列表响应中的 `alert_id` 字段 |
| `export_id` | Query | 是（仅 `/export_status`） | integer | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `params` | Body（JSON） | 是（仅 `/export_agent_logs`） | string | 列表查询参数的 JSON 字符串（非对象），需手动序列化，例如 `"{\"RiskLevel\":\"high\"}"` |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`（API Key 请勿硬编码或泄露）

3. **发起请求**（以查询防护总览为例）：  
   ```bash
   curl -X GET "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer <your-api-key>"
   ```

4. **处理告警导出流程**：  
   - 先调用 `POST /export_agent_logs` 提交任务（传入 `params` 字符串）  
   - 用返回的 `export_id` 轮询 `GET /export_status?export_id=<id>`  
   - 当 `export_status` 为 `success` 且 `link` 非空时，直接下载 Excel  

完整流程可参考[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)和[查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)两篇文档。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 不可替换为其他值  
- **分页机制**：告警列表使用游标分页（`current_page`/`page_size`），但 `/policies` 和 `/overview` 等接口**无分页**，固定返回全量  
- **参数格式陷阱**：`/export_agent_logs` 的 `params` 字段必须是**字符串化的 JSON**（即双引号需转义），不是 JSON 对象；错误示例：`{"RiskLevel":"high"}`（会报 400）；正确示例：`"{\"RiskLevel\":\"high\"}"`  
- **字段空值处理**：`/asset_summary` 响应中缺失字段返回 `null` 而非 `0`，需做空值判断（见[查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)）  
- **错误响应差异**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id","code","message"}`；业务层错误（如 `12000094`）返回嵌套结构 `{"error":{"code","message"}}`，需统一解析 `request_id` 用于排查  
- **时间范围固化**：`/overview` 固定查询最近 24 小时，不支持自定义时间窗口；告警列表默认按 `check_time` 倒序，但无时间范围参数，依赖后台默认策略

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)


