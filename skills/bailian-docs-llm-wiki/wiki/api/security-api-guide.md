# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心安全运营场景。所有接口均基于工作空间隔离，通过 API Key 鉴权，基地址为 `/api/v1/agentstudio/security`。开发者需先完成工作空间 ID 获取与 API Key 配置，方可调用 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中定义的全部接口。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供**安全态势感知与治理能力**，共包含 5 类功能模块：

- **防护概况**：实时获取防护能力开关状态、各模块覆盖情况及拦截统计（如 `content_safety.hit`），固定查询最近 24 小时数据，详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）数量，以 Agent 为中心去重计数，详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **安全策略管理**：查询全量 11 条预置策略（如 `prompt_attack`、`rag_poisoning`），返回启用状态、风险域分类及是否免费，**不支持写操作**，详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。
- **告警生命周期**：支持告警列表（游标分页）、单条详情、批量导出及导出状态轮询，覆盖筛选、查看、下载全流程。
- **错误诊断**：统一错误响应结构，含 `request_id` 便于问题定位，区分网关层与服务层错误码，详见 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

> **注意**：文档 7（告警列表）与文档 9（告警详情）中对 `app_name` 字段的说明存在不一致：前者称其为“应用名称”，后者在响应体说明中称其为“Agent 名称”。实际使用中应以告警列表响应中的 `app_name` 值为准，该字段在控制台中对应 Agent 实例名称。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从百炼控制台获取，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看，用于拼装基地址 |
| `region` | Endpoint | string | 是 | 固定为 `cn-beijing`，当前仅支持该地域 |
| `alert_id` | Path | string | 是（告警详情接口） | 取自 `/agent_logs` 响应中的 `alert_id` 字段，纯数字字符串 |
| `export_id` | Query | integer | 是（导出状态接口） | 取自 `/export_agent_logs` 响应中的 `export_id` 字段 |
| `params` | Body（POST） | string | 是（导出接口） | 告警列表查询参数的 JSON 字符串（需双引号转义），非嵌套对象格式 |

## 使用方式

1. **准备环境**  
   - 获取 `workspace_id`（控制台右上角）和 `BAILIAN_API_KEY`（[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)）；
   - 拼装 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。

2. **调用示例（curl）**  
   ```bash
   # 查询防护总览
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 查询高风险告警（第1页，每页20条）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&page_size=20" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 导出上述筛选条件的全部告警
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"params": "{\"risk_level\":\"high\"}"}'

   # 轮询导出状态（假设 export_id=131231）
   curl -X GET "$BASE_URL/export_status?export_id=131231" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```

3. **处理响应**  
   - 所有成功响应均为 `{ "success": true, "data": ... }` 结构；
   - 失败响应统一为 `{ "type": "error", "error": { "code": "...", "message": "..." }, "request_id": "..." }`，需结合 `request_id` 排查；
   - 导出任务需轮询 `/export_status`，仅当 `export_status == "success"` 且 `link` 非空时才可下载 Excel 文件。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint`（400）错误。
- **分页机制**：告警列表（`/agent_logs`）采用游标分页（`next_page` 字段），**不支持传统 offset 分页**；导出接口（`/export_agent_logs`）则基于当前筛选条件导出全量，无分页概念。
- **策略不可变**：`/policies` 接口仅提供只读策略列表，**不支持启用/禁用策略**；策略开关需在百炼控制台安全中心配置。
- **导出参数格式严格**：`/export_agent_logs` 的 `params` 字段必须是合法 JSON 字符串（如 `"{\"risk_level\":\"high\"}"`），若传入对象或未转义双引号，将导致 `400 Bad Request`。
- **鉴权失败处理**：若 API Key 无效或缺失，网关直接返回 `InvalidApiKey`（401）错误，响应体为扁平结构 `{"request_id":"...","code":"InvalidApiKey","message":"..."}`，**不含 `error` 嵌套对象**，与服务层错误结构不同。
- **字段空值约定**：资产统计接口（`/asset_summary`）中未统计到的字段返回 `null`，而非 `0`，调用方需做空值判断。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


