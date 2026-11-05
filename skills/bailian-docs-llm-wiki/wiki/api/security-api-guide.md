# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向工作空间提供防护概况、资产统计、策略配置、告警列表及导出等能力。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并按工作空间 ID 和地域拼装 Endpoint。开发者应首先完成认证配置，再按需调用具体接口。

## 支持的模型/功能

Security API 不涉及模型推理，而是聚焦于 **Agent 安全治理数据面**，提供以下核心功能模块：

- **防护概况**：查询最近 24 小时防护能力开关状态、各模块覆盖情况及拦截统计（`/overview`）  
- **Agent 资产统计**：按业务空间汇总 Agent 数量及其挂载资源（模型、工具、技能、知识库等）去重计数（`/asset_summary`）  
- **安全策略管理**：获取全量 11 条策略的启用状态、风险域分类与免费标识（`/policies`）  
- **告警全生命周期操作**：支持分页查询（`/agent_logs`）、详情查看（`/agent_logs/{alert_id}`）、异步导出（`/export_agent_logs`）及导出状态轮询（`/export_status`）

> **注意**：文档 2 中将 `/agent_logs` 归类为“策略与告警”下的能力，而文档 7 单独命名为“查询告警列表”，二者内容一致；但文档 2 未说明该接口支持筛选参数，实际完整参数定义以 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) 为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，参与 Endpoint 拼装 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` / `status` / `asset_type` 等 | Query | string/array | 否 | 告警筛选条件，详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `export_id` | Query | integer | 是 | 查询导出状态时必需，由 `/export_agent_logs` 返回 |
| `params` | Body (JSON) | string | 是 | 导出告警时需传入 JSON 字符串化的筛选参数（注意是字符串而非对象），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) |

## 使用方式

1. **准备环境**  
   - 开通百炼服务，创建并保管好 API Key（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
   - 获取 `workspace_id`，确认地域为 `cn-beijing`  
   - 拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **发起请求**  
   所有接口均需携带 `Authorization` Header。示例（查询资产）：
   ```bash
   curl -X GET "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/asset_summary" \
     -H "Authorization: Bearer sk-xxx"
   ```

3. **处理响应**  
   - 成功响应统一含 `success: true` 和 `data` 字段  
   - 错误响应结构分两类：网关层错误（如 `InvalidApiKey`）返回扁平 `{code, message, request_id}`；业务错误返回嵌套 `{"error": {"code", "message"}}`（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）  
   - 告警导出为异步流程：先调用 `POST /export_agent_logs` 获取 `export_id` → 轮询 `GET /export_status?export_id=xxx` → `export_status == "success"` 且 `link` 非空时下载

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将返回 `BadRequest.IllegalEndpoint`（400）  
- **鉴权强依赖**：未携带或无效 API Key 将直接被网关拒绝，返回 `InvalidApiKey`（401），不进入业务逻辑  
- **告警导出参数格式特殊**：`/export_agent_logs` 的 `params` 字段必须是 **JSON 字符串**（如 `"\"CurrentPage\":1"`），而非 JSON 对象，否则报 `400 参数类型错误`  
- **字段空值语义**：资产统计接口（`/asset_summary`）中未启用的功能项返回 `null`，而非 `0`，需在代码中显式判空  
- **策略数量固定**：`/policies` 接口始终返回 11 条策略，不分页且不可增删，`free: true` 表示基线类能力默认生效  
- **时间范围不可定制**：`/overview` 固定查询最近 24 小时数据，无时间范围参数  

> **注意**：文档 5 描述 `/overview` “固定查询最近 24 小时”，但文档 2 的接口列表未强调该约束；实际行为以 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 为准，开发者不应尝试添加时间参数。

## 来源文档

- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)


