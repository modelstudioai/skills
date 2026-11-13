# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警检索与批量导出等核心场景。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成工作空间 ID 获取与 API Key 配置，方可调用 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中定义的全部接口。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，提供以下五类功能：

- **防护概况**：查询最近 24 小时的防护能力开关状态、模块覆盖情况及拦截统计（如 `content_safety`、`file_scan` 等）；
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）数量，去重计数；
- **安全策略管理**：获取全量 11 条策略的启用状态、风险域分类与免费标识（如 `prompt_attack`、`baseline_check`）；
- **告警生命周期操作**：支持分页查询（`/agent_logs`）、详情查看（`/agent_logs/{alert_id}`）、异步导出（`/export_agent_logs`）及状态轮询（`/export_status`）；
- **错误诊断支持**：统一错误响应结构，含 `request_id` 与标准化错误码，便于问题定位。

> **注意**：文档 7（查询告警列表）中 `asset_type` 参数说明为 `agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel`，但文档 8（查询告警详情）响应体中 `asset_type` 示例值为 `app`，且文档 6 明确将 MCP 工具统一归为 `tool`。实际调用应以文档 7 的枚举为准；`app` 属于过时表述，已在最新服务端逻辑中被 `agent` 替代。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 固定为 `cn-beijing`，当前仅支持该地域 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` | Query | string | 否 | 值为 `high`/`medium`/`low`，用于筛选告警 |
| `params` | Body (POST) | string | 是 | 导出接口中需传入 JSON 字符串化的查询参数（注意是字符串而非对象），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **发起请求**（以查询防护总览为例）：
   ```bash
   curl -X GET "https://your-workspace-id.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer your-api-key"
   ```

4. **处理响应**：  
   所有成功响应均为 `{ "success": true, "data": {...} }` 结构；失败响应含 `request_id`，可用于问题排查，参考 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 仅支持 `cn-beijing`，其他地域返回 `BadRequest.IllegalEndpoint`（400）；
- **导出参数格式**：`/export_agent_logs` 的 `params` 字段必须是**JSON 字符串**（即双引号需转义），不可直接传 JSON 对象，否则返回 `400 参数校验失败`；
- **告警分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；
- **策略固定返回**：`/policies` 接口始终返回全部 11 条策略，无分页、无过滤参数；
- **资产统计字段空值**：`/asset_summary` 中未统计到的字段返回 `null` 而非 `0`，需做空值判断；
- **API Key 安全**：API Key 具备账号级权限，严禁硬编码、提交至 Git 或暴露在前端代码中；
- **错误码优先级**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）由网关直接返回扁平结构 `{"request_id","code","message"}`；业务错误（如 `12000093`）则嵌套在 `error.code` 中。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


