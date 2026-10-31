# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的查询与导出能力，面向工作空间维度统一暴露接口。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并按工作空间 ID 与地域拼装 Endpoint。开发者可通过该 API 获取实时防护概况、资产分布、策略启用状态及全量告警详情，支撑安全运营与审计场景。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全治理数据面能力**，覆盖以下三类核心功能：

- **防护概况**：查询最近 24 小时防护总览（`/overview`）与 Agent 资产统计（`/asset_summary`），包括能力开关状态、各模块覆盖情况及拦截/扫描统计。详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 和 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)。
- **策略管理**：获取全量 11 条安全策略的启用状态、分组与免费标识（`/policies`），策略按 `risk_domain` 分为模型交互、运行环境、知识记忆、身份凭证、配置组件五大类。
- **告警生命周期**：支持告警列表查询（`/agent_logs`）、单条详情获取（`/agent_logs/{alert_id}`）、异步导出（`/export_agent_logs`）及导出状态轮询（`/export_status`）。告警支持多维筛选与游标分页，导出任务需通过 `export_id` 关联。

> **注意**：文档 7 中 `/agent_logs` 的参数 `status_list`（数组类型）与文档 8、9、10 中实际使用的字符串型 `status` 参数存在不一致；实践中应以文档 7 定义为准，`status_list` 用于多值筛选（如 `["unhandled","intercepted"]`），而单值筛选使用 `status`。其他文档未体现该数组参数，属信息遗漏。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，参见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` | Query | string | 否 | 取值 `high`/`medium`/`low`，用于告警筛选 |
| `params` | Body (POST) | string | 是 | 导出接口中需将列表查询参数 JSON 序列化为字符串（注意字段名大小写与文档 9 示例一致，如 `"CurrentPage"`） |

## 使用方式

1. **准备环境**  
   - 开通百炼服务，创建 API Key（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）；  
   - 获取 `workspace_id`（见 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）；  
   - 拼装 `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。

2. **发起请求**  
   所有接口均需携带 `Authorization` Header。示例（查询防护总览）：
   ```bash
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```

3. **处理响应**  
   - 成功响应统一含 `{"success": true, "data": ...}` 结构；  
   - 错误响应分两类：网关层（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id","code","message"}`；业务层错误（如 `12000093`）返回嵌套 `{"error": {"code", "message"}}`（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）；  
   - 告警导出需两步：先调 `POST /export_agent_logs` 获取 `export_id`，再轮询 `GET /export_status?export_id=...` 直至 `export_status == "success"` 且 `link` 非空。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing`，其他地域请求将返回 `BadRequest.IllegalEndpoint`（400）。
- **分页机制**：告警列表（`/agent_logs`）使用游标分页，响应中 `next_page` 字段指示下一页页码；`/policies` 和 `/overview` 等接口无分页，固定返回全量。
- **导出参数格式**：`/export_agent_logs` 的 `params` 字段必须为 JSON 字符串（非对象），且键名需首字母大写（如 `"CurrentPage"`），与文档 9 示例严格一致，否则解析失败导致 400。
- **空值处理**：`/asset_summary` 响应中未统计到的字段返回 `null` 而非 `0`，调用方需做空值判断。
- **错误排查**：所有错误响应均含 `request_id`，务必在日志中记录并提交技术支持；高频 `503` 错误（如 `12000093`）表明云安全后端临时不可用，建议指数退避重试。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


