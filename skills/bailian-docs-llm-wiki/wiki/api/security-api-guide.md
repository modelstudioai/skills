# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警检索与批量导出等核心场景。所有接口均基于工作空间路由，通过 API Key 鉴权，基路径为 `/api/v1/agentstudio/security`。开发者需先完成[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)并确认工作空间与地域配置。

## 支持的模型/功能

Security API 不涉及模型调用，而是面向 Agent 安全治理的**数据面接口**，提供以下五类功能：

- **防护概况**：实时获取防护能力开关状态、模块覆盖情况及拦截统计（如内容安全、文件扫描、技能扫描），固定查询最近 24 小时数据。详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库、记忆库等）数量，以 Agent 为中心去重计数。详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **安全策略管理**：查询全部 11 条预置策略的启用状态、所属风险域（如 `model_interaction`、`runtime_tool`）及是否免费。策略不可写，仅读取。
- **告警全生命周期操作**：支持分页查询（含多维筛选）、单条详情查看、异步导出及状态轮询。
- **错误诊断支持**：统一错误响应结构，含 `request_id` 用于问题定位，区分网关层与服务层错误码。

> **注意**：文档 7 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 2 的 `capabilities.key` 列表未涵盖二者；实际策略枚举应以 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，API Key 从[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)获取 |
| `workspace_id` | Host | string | 是 | 工作空间 ID，控制台右上角下拉菜单查看；拼入 Endpoint 主机名 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` / `status` / `asset_type` 等 | Query | string/array | 否 | 告警筛选条件，详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `params` | Body (JSON) | string | 是 | 导出告警时需将筛选参数 JSON 序列化为字符串（注意字段名大小写需与列表接口一致） |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`

3. **发起请求**（以查询防护总览为例）：
   ```bash
   curl -X GET "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer <your-api-key>"
   ```

4. **告警导出流程**（三步）：
   - 调用 `POST /export_agent_logs` 提交任务，传入 `params`（如 `{"risk_level":"high"}` 的 JSON 字符串）；
   - 从响应中提取 `export_id`；
   - 轮询 `GET /export_status?export_id=<id>` 直至 `export_status="success"` 且 `link` 非空。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域返回 `BadRequest.IllegalEndpoint` 错误（HTTP 400）。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务不支持增量导出，每次提交均为全量筛选结果。
- **数据时效性**：防护总览（`/overview`）固定返回最近 24 小时聚合数据，不可指定时间范围。
- **字段空值处理**：资产统计接口（`/asset_summary`）中未统计到的字段返回 `null` 而非 `0`，需做空值判断。
- **错误处理**：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）响应为扁平结构 `{"request_id","code","message"}`；服务层错误（如 `12000093`）嵌套在 `error` 字段内。排查时务必记录 `request_id` 并参考 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 文档。
- **策略一致性**：策略启用状态（`enabled`）反映当前生效配置，但策略本身不可通过 API 修改，需在控制台操作。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


