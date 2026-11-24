# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置及告警全生命周期管理（查询、详情、导出）。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成工作空间 ID 获取与 API Key 配置，方可调用。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，提供以下核心功能模块：

- **防护概况**：实时获取最近 24 小时防护能力开关状态、模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描）；详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库、记忆库等）数量，支持去重计数；详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **策略管理**：查询全部 11 条预置安全策略的启用状态、所属风险域（如 `model_interaction`、`runtime_tool`）及是否免费；策略不可写，仅读取；详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警管理**：支持告警列表分页查询（含多维筛选）、单条告警详情获取、批量导出（异步任务）及导出状态轮询；详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。

> **注意**：文档 7 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 3 的 `capabilities.key` 列表未涵盖二者；实际以文档 7 的策略清单为准，`capabilities` 仅反映运行时防护能力开关，二者语义不同，不构成矛盾。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 鉴权凭证；详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，用于拼装 Endpoint，形如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` |
| `alert_id` | Path (for `/agent_logs/{alert_id}`) | string | 是 | 告警唯一标识，取自告警列表响应中的 `alert_id` 字段 |
| `export_id` | Query (for `/export_status`) | integer | 是 | 导出任务 ID，由 `/export_agent_logs` 接口返回 |
| `params` | Body (for `/export_agent_logs`) | string | 是 | JSON 字符串格式的筛选参数（非嵌套对象），需与 `/agent_logs` 查询参数保持一致 |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
   （当前仅支持 `cn-beijing` 地域）

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **发起请求**（以 `curl` 为例）：
   - 查询防护总览：  
     ```bash
     curl -X GET "$BASE_URL/overview" -H "Authorization: Bearer $BAILIAN_API_KEY"
     ```
   - 查询高风险告警（第1页，每页20条）：  
     ```bash
     curl -X GET "$BASE_URL/agent_logs?risk_level=high&page_size=20" -H "Authorization: Bearer $BAILIAN_API_KEY"
     ```
   - 导出告警（复用上述筛选条件）：  
     ```bash
     curl -X POST "$BASE_URL/export_agent_logs" \
       -H "Authorization: Bearer $BAILIAN_API_KEY" \
       -H "Content-Type: application/json" \
       -d '{"lang":"zh","params":"{\"risk_level\":\"high\",\"page_size\":20}"}'
     ```
   - 轮询导出状态：  
     ```bash
     curl -X GET "$BASE_URL/export_status?export_id=131231" -H "Authorization: Bearer $BAILIAN_API_KEY"
     ```

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint`（400 错误码）。
- **分页机制**：告警列表使用游标分页（`current_page`/`page_size`），导出任务则需通过 `export_id` 轮询 `/export_status` 获取下载链接；导出链接有效期为 24 小时。
- **字段空值处理**：资产统计接口（`/asset_summary`）中未统计到的字段返回 `null`，而非 `0`，需在客户端做空值判断。
- **错误处理**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id", "code", "message"}`；业务错误（如 `12000093`）返回嵌套结构 `{"error": {"code": "...", "message": "..."}}`；务必通过 `request_id` 追踪问题。
- **时间范围固定**：防护总览（`/overview`）仅返回最近 24 小时数据，不支持自定义时间窗口。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


