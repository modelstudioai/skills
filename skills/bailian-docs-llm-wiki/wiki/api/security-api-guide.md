# security api guide

Security API 提供 Agent 全生命周期的[安全防护](../concepts/security.md)数据查询能力，包括资产统计、策略配置、实时告警与导出功能。所有接口均基于统一 Endpoint 和 Bearer [Token](../concepts/token.md) 鉴权，返回结构一致，适用于安全运营自动化与合规审计场景。开发者需先完成工作空间配置与 API Key 获取，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 支持的模型/功能

Security API 不涉及模型调用，而是面向 Agent 安全治理的数据服务，覆盖以下核心功能模块：

- **防护概况**：获取最近 24 小时防护能力开关状态、模块覆盖范围及拦截统计（`/overview`）  
- **资产统计**：按业务空间汇总 Agent 及其挂载资源（模型、工具、技能、知识库等）数量（`/asset_summary`），详见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)  
- **策略管理**：查询全部 11 条预置安全策略的状态（启用/禁用）、所属风险域及是否免费（`/policies`）  
- **告警中心**：支持游标分页查询、详情查看、条件筛选与批量导出（`/agent_logs`, `/agent_logs/{alert_id}`, `/export_agent_logs`, `/export_status`）

> **注意**：文档 5 中列出 `/overview` 属于“防护概况”，而文档 7 的标题为“查询防护总览”，二者内容完全对应；但文档 5 的表格中将该接口归类为“防护概况”，文档 7 却未在正文中明确其归属模块。以文档 5 的分类为准，即 `/overview` 是防护概况的核心接口。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | `Bearer <your-api-key>`，取自百炼控制台 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `export_id` | Query | integer | 是（仅 `/export_status`） | 导出任务 ID，来自 `/export_agent_logs` 响应 |
| `alert_id` | Path | string | 是（仅 `/agent_logs/{alert_id}`） | 告警列表返回的纯数字 ID |
| `params` | Body（JSON） | string | 是（仅 `/export_agent_logs`） | 列表查询参数的 JSON 字符串（注意是序列化后的字符串，非对象） |
| `current_page` / `page_size` / `risk_level` 等 | Query | 各异 | 否（默认值见文档） | 仅 `/agent_logs` 支持多维筛选，详见 [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |

## 使用方式

1. **构造 Endpoint**：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`  
2. **设置鉴权头**：`Authorization: Bearer $BAILIAN_API_KEY`  
3. **按需调用接口**：
   - 查资产：`GET /asset_summary`
   - 查策略：`GET /policies`
   - 查告警列表：`GET /agent_logs?risk_level=high&status=intercepted`
   - 查告警详情：`GET /agent_logs/{alert_id}`
   - 导出告警：`POST /export_agent_logs`（需传 `params` 字符串）
   - 查导出状态：`GET /export_status?export_id=123456`

所有接口响应均遵循统一格式：成功时 `"success": true, "data": {...}`；失败时 `"success": false, "errorCode": "...", "errorMsg": "..."`。单项字段不可用时返回 `null`，不报错。

## 限制和注意事项

- **分页机制**：告警列表（`/agent_logs`）使用游标分页，依赖 `next_page` 字段而非传统 offset；导出任务无分页，需通过 `/export_status` 轮询进度。
- **参数格式陷阱**：`/export_agent_logs` 的 `params` 字段必须是 JSON **字符串**（如 `"\"RiskLevel\":\"high\""`），不是 JSON 对象，否则返回 400。
- **时间范围固定**：`/overview` 仅返回最近 24 小时数据，不支持自定义时间窗口。
- **字段空值语义**：响应中缺失字段（如 `skill` 在 Managed Agent 环境下）返回 `null`，而非 `0` 或空数组，需做空值判断。
- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 region 不可替换为其他值。
- **免费策略行为**：`baseline_check` 和 `vulnerability_scan` 标记为 `"free": true`，即使未开通高级防护也生效；其余策略 `"free": false` 表示需开通对应服务才可启用。

## 来源文档

- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)


