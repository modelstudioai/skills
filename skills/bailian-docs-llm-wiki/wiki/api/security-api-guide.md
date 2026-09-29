# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于统一鉴权机制，通过阿里云百炼 API Key 认证，Endpoint 按工作空间与地域拼装。开发者可据此构建安全监控看板、自动化告警响应或合规审计流程。

## 支持的模型/功能

Security API 当前**不涉及大模型推理调用**，而是面向 Agent 安全治理的数据服务接口，覆盖以下功能域：

- **防护概况**：查询最近 24 小时防护总览（`/overview`）与 Agent 资产挂载统计（`/asset_summary`），包括能力开关状态、各模块拦截/扫描量等；
- **策略管理**：获取全量 11 条安全策略的启用状态与分类（`/policies`），策略按 `risk_domain` 分组，如 `model_interaction`、`runtime_tool` 等；
- **告警全生命周期**：支持分页查询（`/agent_logs`）、单条详情（`/agent_logs/{alert_id}`）、异步导出（`/export_agent_logs`）及导出状态轮询（`/export_status`）。

> **注意**：文档 5 中列出的 `policy_code` 值（如 `content_safety`）与文档 2 中 `capabilities` 的 `key`（如 `content_safety`）命名一致，但语义不同：前者表示策略项，后者表示防护能力开关。二者逻辑关联但非一一映射，实际启用需结合 `/policies` 接口判断策略是否生效，详见 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，取自[控制台 API Key 管理页](https://bailian.console.aliyun.com/?tab=model#/api-key) |
| `workspace_id` | Endpoint | string | 是 | 工作空间 ID，见控制台右上角下拉菜单；地域固定为 `cn-beijing` |
| `alert_id` | Path | string | 是（`/agent_logs/{alert_id}`） | 告警唯一标识，纯数字字符串，取自告警列表响应 |
| `export_id` | Query | integer | 是（`/export_status`） | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `params` | Body（JSON） | string | 是（`/export_agent_logs`） | 列表查询参数的 JSON 字符串（非对象），需手动序列化，例如 `"{\"risk_level\":\"high\"}"` |

其他常用查询参数（如 `risk_level`, `status`, `order_by`）仅在 `/agent_logs` 和 `/export_agent_logs` 的 `params` 中生效，详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **发起请求（以查询防护总览为例）**：  
   ```bash
   curl -X GET "https://<workspace_id>.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer <your-api-key>"
   ```

3. **处理响应**：  
   所有接口遵循统一响应结构：`{"success": true/false, "data": {...}}`。失败时返回 `errorCode` 与 `errorMsg`；成功时 `data` 字段结构依接口而异（如 `/overview` 返回嵌套对象，`/policies` 返回数组）。单项数据不可用时字段值为 `null`，不报错。

4. **导出告警流程**：  
   - 先调用 `POST /export_agent_logs` 提交任务，传入 `params`（需 JSON 字符串化）；  
   - 再轮询 `GET /export_status?export_id=<id>`，等待 `export_status` 变为 `"success"` 且 `link` 非空；  
   - 最后下载 Excel 文件。该流程细节请参考 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 和 [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 不可替换为其他值；
- **时间范围硬编码**：`/overview` 固定查询最近 24 小时，不支持自定义时间窗口；
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），非传统 offset 分页；`/policies` 不分页，固定返回 11 条；
- **导出参数格式**：`/export_agent_logs` 的 `params` 字段必须是 JSON **字符串**（如 `"\"risk_level\":\"high\""`），而非 JSON 对象，否则将导致解析失败；
- **字段空值语义**：`/asset_summary` 中未取到的字段返回 `null`（非 `0`），需做空值判断；`/agent_logs` 响应中 `handle_time` 等未处置字段为 `null`；
- **错误重试建议**：遇到错误码 `12000093` 或 `12000094`（HTTP 503）时，应指数退避重试，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 来源文档

- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)


