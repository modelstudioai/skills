# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置与安全告警全链路。所有接口均基于工作空间路由，通过 API Key 鉴权，适用于安全运营、合规审计与自动化巡检等开发者场景。完整调用流程需依次完成[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)、Endpoint 拼装与参数构造。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，提供以下核心功能模块：

- **防护概况**：`/overview`（最近 24 小时能力开关与拦截统计）、`/asset_summary`（Agent 及挂载资源数量统计）  
- **策略管理**：`/policies`（11 条固定策略的启用状态与分类，含免费策略如 `baseline_check`）  
- **告警全生命周期**：`/agent_logs`（分页查询）、`/agent_logs/{alert_id}`（详情）、`/export_agent_logs`（异步导出）、`/export_status`（进度与下载链接）  

> **注意**：文档 10 中 `policy_code` 列表明确包含 `vulnerability_scan`（免费），但文档 3 的 `capabilities` 字段未列出该能力；实际策略启用状态以 `/policies` 接口返回为准，`capabilities` 仅反映运行时防护能力开关，二者语义不同，不可混用。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `Authorization` | Header | string | 必填，API Key 鉴权凭证 | `Bearer <your-api-key>` |
| `workspace_id` | Host | string | 必填，从百炼控制台右上角获取 | `ws-abc123` |
| `region` | Host | string | 固定为 `cn-beijing` | — |
| `current_page` / `page_size` | Query | integer | 告警列表分页参数，默认 `1` / `20` | `?current_page=1&page_size=50` |
| `risk_level` | Query | string | 告警筛选：`high` / `medium` / `low` | `&risk_level=high` |
| `params` | Body (POST) | string | 导出任务中需传入 JSON 字符串化的筛选参数（注意字段名大小写与驼峰） | `{"RiskLevel":"high","OrderBy":"CheckTime"}` |
| `export_id` | Query | integer | 查询导出状态必需 | `?export_id=131231` |

> **注意**：文档 8 要求 `params` 字段为「JSON 字符串」，而非嵌套对象；若直接传对象会导致 400 错误，详见[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)示例。

## 使用方式

1. **准备环境**  
   - 开通百炼服务，创建 API Key（见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
   - 获取工作空间 ID（控制台右上角下拉菜单）  
   - 拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **基础调用示例（curl）**  
   ```bash
   # 查询防护总览
   curl -X GET "https://ws-abc123.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer YOUR_API_KEY"

   # 查询高风险告警（第1页，每页50条）
   curl -X GET "https://ws-abc123.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/agent_logs?risk_level=high&current_page=1&page_size=50" \
     -H "Authorization: Bearer YOUR_API_KEY"

   # 提交导出任务（参数需 JSON 字符串化）
   curl -X POST "https://ws-abc123.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/export_agent_logs" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\"}"}'
   ```

3. **轮询导出状态**  
   使用 `/export_status?export_id={id}` 轮询，当 `export_status == "success"` 且 `link` 非空时，直接下载 Excel 文件。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，其他 region 将返回 `BadRequest.IllegalEndpoint`（400）错误  
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持 offset 分页；导出任务无分页，按筛选条件导出全量  
- **响应一致性**：  
  - 网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id","code","message"}`  
  - 业务错误（如 `12000093`）返回嵌套结构 `{"error":{"code","message"}}`，详见[Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)  
- **字段空值处理**：`/asset_summary` 接口对未统计到的字段返回 `null`（非 `0`），调用方需做空值判断  
- **告警 ID 类型**：`alert_id` 在 `/agent_logs` 中为字符串（如 `"4289016"`），但在 `/export_agent_logs` 的 `params` 中需按原始字符串传递，不可转为整数  
- **免费策略行为**：`baseline_check` 和 `vulnerability_scan` 的 `free: true` 表示无需开通高级防护即可生效，但其 `enabled` 字段仍可被手动关闭

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)


