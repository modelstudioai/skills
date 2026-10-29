# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的程序化访问能力，支持查询防护总览、资产统计、策略开关、告警列表与详情，以及告警批量导出。所有接口均基于工作空间路由，通过 API Key 鉴权，适用于安全运营自动化与集成场景。开发者需首先完成[概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)中描述的前置配置。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的**数据面 API**，覆盖以下核心功能模块：

- **防护概况**：`GET /overview`（最近 24 小时防护能力开关、模块覆盖状态、拦截统计）和 `GET /asset_summary`（Agent 及挂载资源数量汇总）  
- **策略管理**：`GET /policies`（返回全部 11 条固定策略，含启用状态与免费标识）  
- **告警管理**：`GET /agent_logs`（游标分页查询）、`GET /agent_logs/{alert_id}`（单条详情）、`POST /export_agent_logs`（提交导出任务）、`GET /export_status`（轮询导出状态）  

> **注意**：文档 7 明确说明 `/policies` 接口“共 11 条策略，固定返回全量，不分页”，但文档 1 的表格中未列出该限制，易被误读为可分页或可筛选。请以[查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，详见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从控制台右上角获取；地域固定为 `cn-beijing` |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `1` / `20` |
| `risk_level`, `status`, `asset_type` 等 | Query | string/array | 否 | 告警筛选条件，详见[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `params` | Body (JSON) | string | 是 | `POST /export_agent_logs` 中需传入**序列化后的查询参数字符串**（非原始 JSON 对象），格式必须与列表接口一致 |

> **注意**：文档 10 的请求示例中 `params` 字段值为 `"{\"CurrentPage\":1,...}"`（首字母大写、双引号转义），而文档 6 的参数名均为小驼峰（如 `current_page`）。实际调用时应严格按文档 10 示例的**大驼峰 + 转义 JSON 字符串**格式构造，否则导出任务将失败。

## 使用方式

1. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
2. **设置 Header**：`Authorization: Bearer <your-api-key>`  
3. **发起请求**：根据功能选择对应路径与方法（见下表）

| 功能 | 方法 | 路径 | 典型用途 |
|------|------|------|----------|
| 查询防护总览 | GET | `/overview` | 获取各防护模块开关状态与拦截统计 |
| 查询 Agent 资产 | GET | `/asset_summary` | 统计 Agent 数量及挂载的模型、工具、知识库等资源数 |
| 查询安全策略 | GET | `/policies` | 检查策略启用状态（如 `prompt_attack` 是否开启） |
| 查询告警列表 | GET | `/agent_logs` | 按风险等级、资产类型等条件筛选告警 |
| 查询告警详情 | GET | `/agent_logs/{alert_id}` | 获取单条告警的原始 Prompt、攻击分析与处置建议 |
| 导出告警 | POST | `/export_agent_logs` | 提交导出任务，返回 `export_id` |
| 查询导出状态 | GET | `/export_status?export_id=xxx` | 轮询进度，`export_status: "success"` 且 `link` 非空时下载 Excel |

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他地域将返回 `BadRequest.IllegalEndpoint` 错误（见[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）  
- **鉴权失败响应**：API Key 无效时网关直接返回 `{"code": "InvalidApiKey", "message": "...", "request_id": "..."}`（扁平结构），无需解析嵌套 `error` 字段  
- **告警导出约束**：`POST /export_agent_logs` 的 `params` 必须是**合法 JSON 字符串的转义形式**，且字段名需与列表接口实际接收的参数名一致（文档 6 为小驼峰，但文档 10 示例强制要求大驼峰）；导出任务最大支持 10,000 条记录，超限将返回 `400` 错误  
- **空值处理**：`/asset_summary` 响应中未统计到的字段返回 `null`（非 `0`），调用方需做空值判断  
- **错误排查**：所有错误响应均含 `request_id`，务必在日志中记录并用于工单提报；服务级错误（如 `12000093`）表示后端依赖异常，应重试而非修改请求参数

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)


