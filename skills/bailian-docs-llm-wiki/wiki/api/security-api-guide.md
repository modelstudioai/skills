# security api guide

Security API 是阿里云百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向工作空间维度提供防护概况、资产统计、策略配置、告警查询与导出等能力。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并按工作空间 ID 和地域拼装 Endpoint。开发者应首先完成认证配置与工作空间准备，再按需调用对应接口。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供**Agent 安全治理数据面能力**，覆盖以下核心功能模块：

- **防护概况**：查询最近 24 小时防护总览（`/overview`）与 Agent 资产汇总（`/asset_summary`），包括能力开关状态、各模块覆盖情况及拦截统计。
- **策略管理**：查询全量安全策略列表（`/policies`），共 11 条固定策略，按 `risk_domain` 分组（如 `model_interaction`、`runtime_tool` 等），含启用状态与免费标识。
- **告警全生命周期操作**：
  - 查询告警列表（`/agent_logs`），支持游标分页与多维筛选（风险等级、资产类型、处置状态等）；
  - 查询单条告警详情（`/agent_logs/{alert_id}`），返回原始风险上下文与处置建议；
  - 提交导出任务（`/export_agent_logs`），支持按当前筛选条件导出全部告警；
  - 查询导出状态与下载链接（`/export_status`）。

> **注意**：文档 2 中将 `/agent_logs` 归类为“策略与告警”下的能力，而文档 7 单独命名为“查询告警列表”，二者内容一致；但文档 2 的表格中路径写为 `/agent_logs`，文档 9 的路径为 `/agent_logs/{alert_id}`，命名逻辑统一，无实质矛盾。另需注意，[查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md) 接口实际属于防护概况范畴，而非策略管理，文档 2 的分类层级略显模糊，建议以接口路径语义为准。

## 关键参数

- **全局必需**：
  - `Authorization: Bearer <your-api-key>`：通过 HTTP Header 传递，API Key 获取方式详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)。
  - `workspace_id` 与 `region`：用于拼装 Base URL，当前仅支持 `cn-beijing` 地域，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`。
- **告警相关接口特有参数**：
  - `/agent_logs`：支持 `current_page`、`page_size`、`risk_level`、`status_list`、`asset_type`、`order_by`、`lang` 等查询参数；
  - `/export_agent_logs`：请求体需包含 `params` 字段，其值为告警列表查询参数的 JSON 字符串（注意需手动序列化，非嵌套对象），例如 `"{\"risk_level\":\"high\"}"`；
  - `/export_status`：必须传 `export_id` 查询参数，值来自 `/export_agent_logs` 响应。

## 使用方式

1. **准备环境**：  
   登录百炼控制台，开通服务并创建 API Key（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）；在控制台右上角获取 `workspace_id`。

2. **构造请求**：  
   拼接 Base URL，例如：  
   `https://ws-abc123.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

3. **调用示例（curl）**：  
   ```bash
   # 查询防护总览
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 查询高风险告警（第1页，每页20条）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&current_page=1&page_size=20" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 导出上述筛选结果
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"risk_level\":\"high\"}"}'

   # 查询导出状态（假设 export_id=131231）
   curl -X GET "$BASE_URL/export_status?export_id=131231" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```

4. **错误处理**：  
   所有错误响应均含 `request_id`，可用于问题定位；网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平结构 `{"request_id", "code", "message"}`；业务错误返回嵌套结构 `{"error": {"code", "message"}}`。详细错误码参考 [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- **地域限制**：当前仅支持 `cn-beijing` 地域，Endpoint 中 `region` 固定为此值，其他地域将返回 `BadRequest.IllegalEndpoint`（400）。
- **分页机制**：告警列表（`/agent_logs`）使用游标分页，响应中 `next_page` 字段指示下一页页码；导出任务（`/export_agent_logs`）不支持分页，始终导出全量匹配记录。
- **策略与资产接口无参数**：`/policies` 和 `/asset_summary` 为无参 GET 接口，不支持筛选或分页。
- **导出参数格式严格**：`/export_agent_logs` 的 `params` 字段必须是合法 JSON 字符串（双引号需转义），且字段名需与 `/agent_logs` 查询参数完全一致（如 `risk_level`，非 `RiskLevel`），否则返回 `400` 参数校验失败。
- **敏感信息保护**：API Key 具有账号级权限，严禁硬编码、提交至 Git 或暴露于前端，应使用环境变量或密钥管理服务存储。
- **响应字段空值处理**：`/asset_summary` 接口对未统计到的资源类型返回 `null` 而非 `0`，调用方需做空值判断（见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)）。

## 来源文档

- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [Security API 错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


