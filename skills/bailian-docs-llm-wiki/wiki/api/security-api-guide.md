# security api guide

Security API 提供 Agent 全生命周期的安全防护数据查询与告警管理能力，覆盖防护能力状态、资产分布、策略配置、实时告警及批量导出等核心场景。所有接口均基于统一 Endpoint 与 Bearer [Token](../concepts/token.md) 鉴权，响应结构标准化。开发者可通过该 API 实现安全态势监控、策略合规审计与风险事件闭环处置。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**安全治理数据面能力**，当前支持以下 5 类功能：

- **防护概况查询**：获取全局防护能力开关、模块覆盖状态及拦截统计（如内容安全、供应链扫描等），详见 [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)；
- **Agent 资产统计**：按业务空间聚合 Agent 及其挂载资源（模型、工具、技能、知识库等）数量，以 Agent 为中心去重统计；
- **安全策略管理**：查询全部 11 条预置策略的启用状态、风险域分类与免费标识，策略按 `risk_domain` 分组（如 `model_interaction`、`runtime_tool` 等）；
- **告警全链路操作**：支持告警列表分页查询、单条详情查看、导出任务提交与状态轮询，覆盖从发现、分析到归档的完整流程；
- **告警导出与下载**：通过 `/export_agent_logs` 提交导出任务，并用 `/export_status` 查询进度与获取 Excel 下载链接。

> **注意**：文档 4 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 2 的“可用 API”表格未在“策略与告警”栏列出 `/policies` 接口的说明文字（仅列出了路径），易造成遗漏。实际开发中应以 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档为准。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，使用阿里云百炼控制台生成的 API Key |
| `workspace_id` | Endpoint 路径 | string | 是 | 工作空间 ID，从控制台右上角下拉菜单获取 |
| `region` | Endpoint 路径 | string | 是 | 当前仅支持 `cn-beijing`，拼入 BASE_URL |
| `alert_id` | Path（`/agent_logs/{alert_id}`） | string | 是 | 告警唯一 ID，取自告警列表响应中的 `alert_id` 字段 |
| `export_id` | Query（`/export_status?export_id=...`） | integer | 是 | 导出任务 ID，由 `/export_agent_logs` 返回 |
| `params` | Request Body（`/export_agent_logs`） | string | 是 | 列表查询参数的 JSON 字符串（需序列化为字符串，非对象），例如 `"{\"risk_level\":\"high\"}"` |

> **注意**：文档 7 要求 `params` 字段为「序列化成的 JSON 字符串」，而非常见的嵌套 JSON 对象；若传入原始对象（如 `{ "risk_level": "high" }`），将导致解析失败。该约束在 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 中有明确定义。

## 使用方式

1. **构造 BASE_URL**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
2. **设置鉴权头**：`Authorization: Bearer $BAILIAN_API_KEY`  
3. **按需调用接口**：
   - 查防护总览：`GET /overview`
   - 查资产汇总：`GET /asset_summary`
   - 查策略列表：`GET /policies`
   - 查告警列表（带筛选）：`GET /agent_logs?risk_level=high&status=unhandled`
   - 查告警详情：`GET /agent_logs/{alert_id}`
   - 提交导出：`POST /export_agent_logs`（Body 含 `params` 字符串）
   - 轮询导出状态：`GET /export_status?export_id=12345`

所有接口均返回标准响应结构：`{"success": boolean, "data": ...}`。失败时 `success=false` 并含 `errorCode` 与 `errorMsg`；成功时 `data` 字段结构依接口而定，部分字段（如 `asset_summary` 中未挂载的资源）返回 `null` 而非 `0`。

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他 region 将返回 404 或 503；
- **分页机制**：告警列表使用游标分页（`current_page` + `page_size`），`next_page` 为 `null` 表示末页；导出任务不支持分页，需一次性导出全部匹配记录；
- **时间范围**：`/overview` 固定查询最近 24 小时数据，不可指定时间窗口；
- **策略不可变**：`/policies` 接口仅支持查询，**不支持启用/禁用策略**（策略开关需在控制台配置）；
- **导出参数一致性**：`/export_agent_logs` 的 `params` 字符串必须与 `/agent_logs` 查询参数完全一致（包括大小写与字段名），否则导出结果可能不匹配预期筛选条件；
- **错误处理**：遇到 `errorCode: "12000093"`（云安全服务异常）或 `"12000094"`（告警查询失败）时，应实现指数退避重试，而非立即报错中断流程。

## 来源文档

- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


