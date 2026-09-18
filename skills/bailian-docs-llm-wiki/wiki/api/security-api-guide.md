# security api guide

Security API 提供 Agent 全生命周期安全防护数据的查询与告警导出能力，覆盖防护能力状态、资产分布、策略配置、实时告警及批量导出等核心场景。所有接口均基于统一 Endpoint 与 Bearer Token 鉴权，响应结构标准化，适用于自动化监控与安全运营集成。开发者需先完成工作空间配置与 API Key 获取，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全态势感知与治理能力接口**，共涵盖 6 类功能：

- **防护概况**：获取全局防护开关状态与拦截统计（`/overview`）、Agent 及其挂载资源资产汇总（`/asset_summary`）  
- **策略管理**：查询全量 11 条安全策略的启用状态与分类（`/policies`），包括内容安全、提示词攻击、RAG 数据投毒、身份凭证安全等关键领域  
- **告警管理**：支持分页查询（`/agent_logs`）、单条详情获取（`/agent_logs/{alert_id}`）、异步导出（`/export_agent_logs`）及导出状态轮询（`/export_status`）  

> **注意**：文档 4 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两项免费策略，但文档 1 的 `capabilities` 字段未体现其对应能力项；实际策略启停以 `/policies` 接口为准，`/overview` 仅反映运行时生效的防护模块覆盖情况，二者语义不同，不可混用。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `Authorization` | Header | string | 必填，Bearer Token 格式，值为百炼 API Key | `Bearer ak-xxxxxx` |
| `BASE_URL` | — | URL | 必填，拼接规则：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security` | 见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `current_page` / `page_size` | Query | integer | 告警列表分页参数，默认 `current_page=1`, `page_size=20` | `/agent_logs?current_page=2&page_size=50` |
| `risk_level` | Query | string | 告警筛选，支持 `high`/`medium`/`low` | `/agent_logs?risk_level=high` |
| `params` | Request Body (POST) | string | 导出接口必填，为 JSON 字符串化的查询参数（注意：是字符串而非对象） | `{"RiskLevel":"high","OrderBy":"CheckTime"}` → 序列化为 `"\"RiskLevel\":\"high\",\"OrderBy\":\"CheckTime\""` |

## 使用方式

1. **初始化配置**：从阿里云百炼控制台获取 `workspace_id` 与 API Key，构造 `BASE_URL`  
2. **调用示例（curl）**：
   ```bash
   # 查询防护总览
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 查询高风险告警（中文）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&lang=zh" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 提交导出任务（参数需 JSON 字符串化）
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\"}"}'
   ```
3. **解析响应**：所有接口遵循统一结构 `{"success": boolean, "data": ...}`；失败时返回 `errorCode` 与 `errorMsg`（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 错误码表）

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，`region` 字段不可替换为其他值  
- **分页机制**：告警列表使用游标分页（`next_page` 字段），非传统 offset 分页；导出任务不支持分页，提交即导出全量匹配记录  
- **字段空值处理**：当某项统计不可用时（如无 Skill 挂载），响应中对应字段为 `null`，**非 `0`**（见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md) 说明）  
- **导出链路**：必须严格按顺序调用 `/export_agent_logs` → 轮询 `/export_status?export_id=xxx` → 下载 `link`；`link` 仅在 `export_status == "success"` 且 `link != null` 时有效  
- **策略与能力映射**：`/policies` 返回策略启停状态，`/overview` 返回运行时各模块（如 `flow_agent`, `memory`）的实际防护覆盖开关，二者独立配置，需分别查询确认

## 来源文档

- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


