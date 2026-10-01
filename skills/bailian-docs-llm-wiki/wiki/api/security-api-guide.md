# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于统一鉴权机制，通过阿里云百炼 API Key 认证，Endpoint 按工作空间与地域拼装。该 API 专为安全运营与自动化集成设计，适用于安全态势监控、合规审计与告警闭环处理。

## 支持的模型/功能

Security API 当前支持以下五大类安全能力的数据访问：

- **防护概况**：提供最近 24 小时的实时防护总览（`/overview`）和 Agent 资产聚合统计（`/asset_summary`），涵盖能力开关状态、模块覆盖情况及内容安全/文件/技能扫描拦截统计。
- **策略管理**：固定返回全部 11 条安全策略（`/policies`），包括 `content_safety`、`prompt_attack`、`rag_poisoning` 等，按 `risk_domain` 分组（如 `model_interaction`、`runtime_tool`），并标识启用状态与是否免费。
- **告警生命周期**：支持告警列表查询（`/agent_logs`）、单条告警详情获取（`/agent_logs/{alert_id}`）、批量导出（`/export_agent_logs`）及导出状态轮询（`/export_status`）。告警来源包括 `Agent-Runtime-Guard`、`aiguard` 等组件，覆盖 `agent`、`tool`、`skill` 等六类资产类型。
- **多维筛选与导出**：告警列表支持按 `risk_level`（`high`/`medium`/`low`）、`status`、`asset_type` 等 10 余个参数组合筛选；导出任务通过 `params` 字段透传相同筛选条件，确保数据一致性。
- **语言与本地化支持**：告警接口（如 `/agent_logs` 和 `/export_agent_logs`）支持 `lang=zh` 或 `lang=en`，响应中的 `risk_name`、`risk_desc` 等字段将返回对应语言版本。

> **注意**：文档 5 中 `asset_type` 参数说明为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 6 的响应示例中 `asset_type` 出现了 `app`（如 `"asset_type": "app"`），且文档 4 的策略分组未定义 `app` 类型。实际调用应以文档 5 的枚举为准，`app` 属于非标准值，可能为历史兼容字段，建议忽略或映射为 `agent`。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，需通过[控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，见控制台右上角下拉菜单 |
| `region` | Host | string | 是 | 固定为 `cn-beijing`，当前仅支持该地域 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` | Query | string | 否 | 取值 `high`/`medium`/`low`，用于告警筛选 |
| `params` | Body (POST) | string | 是 | 导出接口必需，为 JSON 字符串格式的筛选参数（如 `{"RiskLevel":"high"}`），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |
| `export_id` | Query | integer | 是 | 查询导出状态必需，取自 `/export_agent_logs` 响应的 `export_id` 字段 |

## 使用方式

1. **初始化配置**：确认已开通百炼服务并创建 API Key；从控制台获取 `workspace_id`；拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。
2. **调用示例（curl）**：
   - 查询防护总览：  
     ```bash
     curl -X GET "$BASE_URL/overview" -H "Authorization: Bearer $BAILIAN_API_KEY"
     ```
   - 查询高风险告警（中文）：  
     ```bash
     curl -X GET "$BASE_URL/agent_logs?risk_level=high&lang=zh" -H "Authorization: Bearer $BAILIAN_API_KEY"
     ```
   - 提交导出任务（复用列表筛选条件）：  
     ```bash
     curl -X POST "$BASE_URL/export_agent_logs" \
       -H "Authorization: Bearer $BAILIAN_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\"}"}'
     ```
3. **轮询导出状态**：使用返回的 `export_id` 调用 `/export_status?export_id=xxx`，待 `export_status` 为 `success` 且 `link` 非空时下载 Excel 文件。

## 限制和注意事项

- **地域限制**：API 仅支持 `cn-beijing` 地域，其他地域 Endpoint 将返回 404 或 503 错误 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。
- **时间窗口固定**：`/overview` 接口固定查询最近 24 小时数据，不支持自定义时间范围；告警列表默认按 `check_time` 倒序排列，无显式时间筛选参数。
- **分页与游标**：告警列表采用游标分页（`next_page` 字段），非传统 offset 分页；`next_page` 为 `null` 表示末页。
- **空值处理**：当某项数据不可用时，接口不报错，而是返回 `null`（如 `/asset_summary` 中未挂载的资源字段）或在数组中置 `available: false`（文档 1 明确说明）。
- **错误码统一**：失败响应结构固定为 `{"success": false, "errorCode": "...", "errorMsg": "..."}`，常见错误码 `12000093`（云安全服务异常）和 `12000094`（告警查询失败）均建议重试 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。
- **导出参数格式**：`/export_agent_logs` 的 `params` 字段必须为 JSON **字符串**（即双层转义），而非 JSON 对象，否则将导致解析失败 —— 此要求在 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 中明确强调，开发者需特别注意序列化处理。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


