# security api guide

Security API 提供对 Agent 安全防护状态、策略配置及安全告警的程序化访问能力，支持查询防护总览、资产分布、策略开关、告警列表与详情，以及告警批量导出。所有接口均基于工作空间路由，通过 API Key 鉴权，适用于安全运营、自动化巡检与 SIEM 集成等场景。完整调用链路需严格遵循[概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)中定义的 Endpoint 拼装规则与前置条件。

## 支持的模型/功能

Security API 不涉及大模型推理，而是面向 Agent 安全治理的服务接口，覆盖以下核心功能域：

- **防护概况**：`GET /overview` 返回最近 24 小时各模块防护开关状态与拦截统计；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、知识库等）的去重计数。
- **策略管理**：`GET /policies` 固定返回 11 条预置策略的启用状态与分类（如 `content_safety`、`prompt_attack`），按 `risk_domain` 分组为模型交互、运行环境、知识记忆等五大安全域。
- **告警生命周期**：`GET /agent_logs` 支持游标分页与多维筛选（风险等级、处置状态、资产类型等）；`GET /agent_logs/{alert_id}` 获取单条告警的原始上下文与处置建议；`POST /export_agent_logs` 提交导出任务；`GET /export_status` 查询进度与下载链接。

> **注意**：文档 5 中 `policy_code` 列表包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 6 的 `capabilities` 字段未体现其开关控制能力，实际策略启停仅能通过控制台或独立策略配置 API（当前未在本文档集公开）完成，开发者应以控制台策略配置为准。

## 关键参数

- **Endpoint 必填变量**：`{workspace_id}`（控制台右上角获取）与固定地域 `cn-beijing`，拼接为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。
- **鉴权头**：必须携带 `Authorization: Bearer <your-api-key>`，API Key 需在[百炼控制台 API Key 页面](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)创建。
- **告警查询参数**：`current_page`（默认 1）、`page_size`（默认 20）、`risk_level`（`high`/`medium`/`low`）、`status`、`asset_type`（如 `tool`/`knowledge_base`）等，详见[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)。
- **导出参数**：`POST /export_agent_logs` 的请求体中 `params` 字段需为 URL 编码前的 JSON 字符串（非对象），且字段名首字母大写（如 `CurrentPage`），与列表接口参数名不一致，需严格对照[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)示例。

## 使用方式

1. **初始化配置**：确认工作空间 ID 与地域，构造 `BASE_URL`；获取并安全存储 API Key。
2. **基础调用示例**（以 `curl` 为例）：
   ```bash
   # 查询资产总数
   curl -X GET "$BASE_URL/asset_summary" -H "Authorization: Bearer $BAILIAN_API_KEY"
   
   # 查询高风险告警（第 1 页，每页 10 条）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&page_size=10" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   
   # 导出高风险告警（注意 params 字符串格式）
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"RiskLevel\":\"high\"}"}'
   ```
3. **错误处理**：检查响应 `success` 字段与 HTTP 状态码；失败时解析 `error.code`（业务码）或 `code`（网关码），结合[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)定位问题；务必记录 `request_id` 用于技术支持。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，其他地域 Endpoint 将返回 `BadRequest.IllegalEndpoint` 错误。
- **分页机制**：告警列表使用游标分页（`next_page` 字段），不支持传统 offset 分页；导出任务无分页，提交即触发全量导出。
- **数据时效性**：`/overview` 固定查询最近 24 小时数据，不可指定时间范围；告警列表默认按 `check_time` 倒序，最新告警优先。
- **字段兼容性**：响应中未取到的字段（如 `file_name` 仅 Skill 告警返回）返回 `null` 而非 `0` 或空字符串，客户端需做 `null` 安全判断。
- **权限边界**：API Key 具有账号级权限，但仅能访问当前工作空间内 Agent 相关安全数据；跨工作空间调用将返回 `Endpoint.AccessDenied`。

## 来源文档

- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


