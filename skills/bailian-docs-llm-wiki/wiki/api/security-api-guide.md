# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置及告警全生命周期管理。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)并拼装正确 Endpoint 后方可调用。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据服务型 API**，提供以下核心功能模块：

- **防护概况**：`GET /overview`（固定查询最近 24 小时）返回能力开关、模块覆盖状态及内容安全/文件扫描/技能扫描三类拦截统计；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数。
- **策略管理**：`GET /policies` 固定返回 11 条安全策略全量清单，含 `policy_code`、`risk_domain`、启用状态及是否免费，如 `prompt_attack`（提示词攻击）、`rag_poisoning`（RAG 数据投毒）等。
- **告警管理**：支持完整告警链路——`GET /agent_logs`（游标分页+多维筛选）、`GET /agent_logs/{alert_id}`（详情）、`POST /export_agent_logs`（导出任务提交）、`GET /export_status`（进度与下载链接查询）。

> **注意**：文档 2 中将 `/agent_logs` 归类为“策略与告警”子项，而文档 7 单独命名为“查询告警列表”，二者实际为同一能力层级；此处统一按功能语义归类为“告警管理”，以避免混淆。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，详见[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing` |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level`, `status`, `asset_type` 等 | Query | string/array | 否 | 告警筛选条件，详见[查询告警列表](raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `params` | Body (JSON) | string | 是 | 导出接口中需传入 URL 查询参数的 JSON 字符串化形式（注意非对象嵌套），例如 `"{\"RiskLevel\":\"high\"}"` |

## 使用方式

1. **准备环境**：  
   - 创建 API Key（见[认证](raw/application-api-reference/security-api-guide/security-api-authentication.md)）；  
   - 获取 `workspace_id`（见[概览](raw/application-api-reference/security-api-guide/security-api-overview.md)）；  
   - 拼装 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。

2. **发起请求示例（curl）**：  
   ```bash
   # 查询防护总览
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 查询高风险告警（第1页，每页20条）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&page_size=20" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 提交导出任务（筛选高风险告警）
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"params": "{\"RiskLevel\":\"high\"}"}'
   ```

3. **处理响应**：  
   - 所有成功响应均为 `{ "success": true, "data": ... }` 结构；  
   - 错误响应结构分两类：网关层（扁平 `{"request_id","code","message"}`）与业务层（嵌套 `"error": {"code", "message"}`），详见[错误码](raw/application-api-reference/security-api-guide/security-api-errors.md)；  
   - 导出任务需轮询 `/export_status?export_id=...` 直至 `export_status == "success"` 且 `link` 非空。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他 region 将返回 `BadRequest.IllegalEndpoint`（HTTP 400）。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出接口的 `params` 必须是字符串化 JSON，若传入原始对象会导致 `400 Bad Request`。
- **数据时效性**：`/overview` 固定返回最近 24 小时数据，不支持时间范围自定义；`/asset_summary` 为实时聚合，无时间窗口。
- **字段空值处理**：`/asset_summary` 响应中未统计到的字段返回 `null` 而非 `0`，调用方需做空值判断。
- **鉴权失败场景**：`InvalidApiKey`（401）表示密钥无效或未携带；`Endpoint.AccessDenied`（403）表示工作空间不存在或当前账号无访问权限。

> **注意**：文档 4 和文档 5 的请求示例中 `BASE_URL` 均明确写为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/...`，但文档 2 的 Endpoint 描述为 `https://{workspace_id}.{region}.maas.aliyuncs.com/...`。实际生产环境必须使用 `cn-beijing` 字面量，不可动态替换 `{region}` —— 此处文档 2 的模板存在误导，应以具体示例为准。

## 来源文档

- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


