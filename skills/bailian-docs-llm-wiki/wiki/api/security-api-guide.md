# security api guide

Security API 提供 Agent 全生命周期的安全防护数据查询与告警管理能力，覆盖防护能力状态、资产分布、策略配置、实时告警及批量导出等核心场景。所有接口均基于统一鉴权与响应结构设计，适用于安全运营、合规审计与自动化监控等开发者场景。详细前提与错误处理请参考 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全防护能力的数据面接口**，支持以下 5 类功能：

- **防护概况**：获取整体防护开关状态与拦截统计（`/overview`）、Agent 及其挂载资源资产汇总（`/asset_summary`）  
- **策略管理**：查询全量 11 条安全策略的启用状态与分类（`/policies`），策略按 `risk_domain` 分为 `model_interaction`、`runtime_tool`、`knowledge_memory`、`identity_credential`、`config_component` 五类  
- **告警查询**：分页检索告警列表（`/agent_logs`）、获取单条告警详情（`/agent_logs/{alert_id}`）  
- **告警导出**：异步提交导出任务（`/export_agent_logs`）并轮询下载链接（`/export_status`）  
- **数据范围**：所有接口默认返回最近 24 小时数据（如 `/overview` 明确说明“固定查询最近 24 小时”），告警类接口支持按 `risk_level`、`status`、`asset_type` 等多维筛选  

> **注意**：文档 5 中 `/agent_logs` 的请求参数 `current_page` 和 `page_size` 用于游标分页，但文档 8 的导出接口要求将筛选参数序列化为 JSON 字符串传入 `params` 字段——二者参数格式不一致，需严格按各自文档实现，不可复用相同参数结构。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `Authorization` | Header | string | 鉴权凭证，格式为 `Bearer <your-api-key>` | `Bearer sk-xxx` |
| `BASE_URL` | URL 基础路径 | string | 拼接规则：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`，其中 `workspace_id` 需从控制台获取 | 见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `alert_id` | Path（`/agent_logs/{alert_id}`） | string | 告警唯一标识，取自 `/agent_logs` 响应中的 `alert_id` 字段 | `4289016` |
| `export_id` | Query（`/export_status?export_id=...`） | integer | 导出任务 ID，由 `/export_agent_logs` 返回 | `131231` |
| `params` | Body（`/export_agent_logs`） | string | 列表查询参数的 JSON 字符串（非对象），必须与 `/agent_logs` 的实际查询条件一致 | `"{"RiskLevel":"high","OrderBy":"CheckTime"}"` |

## 使用方式

1. **初始化配置**：确保已开通百炼服务、创建 API Key，并确认工作空间 ID 与地域（当前仅 `cn-beijing`）；完整配置说明见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)  
2. **调用防护概况接口**：  
   - 查询总览：`GET /overview` → 获取 `capabilities`（能力开关）与 `protection`（模块覆盖）状态  
   - 查询资产：`GET /asset_summary` → 获取 `agent_count`、`tool`、`skill` 等去重计数  
3. **检查策略配置**：`GET /policies` → 解析 `enabled` 字段判断各策略是否生效，注意 `free: true` 的策略（如 `baseline_check`）无需高级防护即可启用  
4. **处理告警**：  
   - 分页查询：`GET /agent_logs?risk_level=high&order_by=check_time&order=desc`  
   - 查看详情：`GET /agent_logs/{alert_id}` → 重点关注 `risk_detail`（攻击模式分析）与 `risk_handle`（拦截话术）  
   - 批量导出：先 `POST /export_agent_logs` 提交任务，再轮询 `GET /export_status?export_id=...` 直至 `export_status == "success"` 且 `link` 非空  

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他 region 将返回 503 错误（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）  
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出接口不支持分页，需通过 `params` 传递完整筛选条件  
- **字段空值语义**：当某项数据不可用时，响应中对应字段返回 `null`（如 `/asset_summary` 中未挂载 `memory` 则 `memory: null`），而非 `0` 或空数组  
- **策略数量固定**：`/policies` 固定返回 11 条策略，无分页，新增策略将扩展此列表但保持全量返回  
- **导出任务时效性**：导出任务生成的 Excel 文件链接有效期为 24 小时，超时需重新提交任务  
- **错误处理**：所有接口遵循统一响应结构 `{"success": false, "errorCode": "...", "errorMsg": "..."}`，常见错误码 `12000093`（云安全服务异常）和 `12000094`（告警查询失败）建议指数退避重试

## 来源文档

- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


