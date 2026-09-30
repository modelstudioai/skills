# security api guide

Security API 提供 Agent 全生命周期[安全防护](../concepts/security.md)数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警检索与批量导出等核心场景。所有接口均基于统一鉴权机制和标准化响应结构，适用于安全运营、合规审计与自动化监控集成。开发者需先完成工作空间配置与 API Key 获取，方可调用。

## 支持的模型/功能

Security API 当前提供以下 6 类功能接口，全部位于 `/api/v1/agentstudio/security` 路径下：

- **防护概况**：`/overview`（查询最近 24 小时防护能力开关、模块覆盖状态及拦截统计）  
- **资产统计**：`/asset_summary`（按业务空间汇总 Agent 及其挂载资源数量，含模型、工具、技能、知识库等维度）  
- **策略管理**：`/policies`（查询全量 11 条安全策略启用状态与分类，如 `prompt_attack`、`rag_poisoning` 等）  
- **告警检索**：`/agent_logs`（游标分页查询告警列表，支持按风险等级、资产类型、处置状态等多维筛选）  
- **告警详情**：`/agent_logs/{alert_id}`（根据告警 ID 获取原始 Prompt、风险分析、拦截话术等完整上下文）  
- **告警导出**：`/export_agent_logs`（提交导出任务） + `/export_status`（轮询导出进度与下载链接）

> **注意**：文档 7 中明确说明 `/policies` 接口“共 11 条策略，固定返回全量，不分页”，但文档 3 的“可用 API”表格未列出该接口的分页或参数说明，实际调用无需分页参数——此为设计一致，非矛盾。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，取自[API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `export_id` | Query | integer | 是（仅 `/export_status`） | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `alert_id` | Path | string | 是（仅 `/agent_logs/{alert_id}`） | 告警唯一标识，取自 `/agent_logs` 响应中的 `alert_id` 字段 |
| `params` | Body（JSON） | string | 是（仅 `/export_agent_logs`） | 列表查询参数的 JSON 字符串序列化值（非嵌套对象），详见[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |
| `lang` | Query/Body | string | 否 | 语言偏好（`zh`/`en`），影响告警描述与导出内容本地化 |

## 使用方式

1. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 从百炼控制台右上角获取；  
2. **设置鉴权头**：所有请求必须携带 `Authorization: Bearer $BAILIAN_API_KEY`；  
3. **发起请求**：按需调用对应接口，例如查询防护总览：
   ```bash
   curl -X GET "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer sk-xxx"
   ```
4. **处理响应**：统一遵循 `{ "success": boolean, "data": ... }` 结构；失败时返回 `errorCode` 与 `errorMsg`，成功时字段缺失返回 `null`（非 `0` 或空字符串），详见[API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，其他 region 不可用；  
- **时间窗口**：`/overview` 接口固定查询最近 24 小时数据，不支持自定义时间范围；  
- **导出依赖列表参数**：`/export_agent_logs` 的 `params` 字段必须严格匹配 `/agent_logs` 的查询参数格式（如 `{"CurrentPage":1,"PageSize":20}`），且需 JSON 序列化为字符串，否则导出任务将失败；  
- **告警字段兼容性**：`/agent_logs` 响应中 `agent_name` 字段在部分告警类型中可能为空，应优先使用 `app_name`；而 `/agent_logs/{alert_id}` 响应中 `asset_type` 对 MCP 工具统一返回 `tool`，与列表接口中 `asset_type: "tool"` 语义一致；  
- **免费策略行为**：`baseline_check` 和 `vulnerability_scan` 标记为 `"free": true`，即使未开通高级防护也默认生效，此逻辑在[查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)中有明确定义。

## 来源文档

- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)


