# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，用于获取防护能力状态、资产分布、策略配置及安全告警等信息。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并按工作空间拼装 Endpoint。开发者应优先完成认证配置，并结合错误码文档进行健壮性处理。

## 支持的模型/功能

Security API 不涉及模型调用，而是提供**Agent 安全治理数据面能力**，覆盖以下五大功能域：

- **防护概况**：查询整体防护开关状态与拦截统计（`/overview`）、Agent 及其挂载资源资产汇总（`/asset_summary`）  
- **策略管理**：查询 11 条预置安全策略的启用状态与分类（`/policies`），策略按 `risk_domain` 分为 `model_interaction`、`runtime_tool`、`knowledge_memory`、`identity_credential`、`config_component` 五类  
- **告警管理**：支持分页查询告警列表（`/agent_logs`）、获取单条告警详情（`/agent_logs/{alert_id}`）、提交导出任务（`/export_agent_logs`）及轮询导出状态（`/export_status`）  

> **注意**：文档 5 中列出的 `/policies`、`/agent_logs` 等路径在文档 6–10 中均有对应详细说明，但文档 5 的“可用 API”表格未注明 `/export_status` 的请求方法（应为 `GET`），而文档 10 明确其为 `GET` 接口；以 [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md) 为准。

## 关键参数

- **全局必需**：  
  - `Authorization: Bearer <your-api-key>`（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
  - `BASE_URL = https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`（当前仅支持 `cn-beijing` 地域）  

- **告警类接口特有参数**：  
  - `/agent_logs` 支持 `current_page`、`page_size`、`risk_level`、`status_list`、`asset_type` 等筛选与分页参数  
  - `/export_agent_logs` 的 `params` 字段需传入**序列化后的 JSON 字符串**（非对象），且字段名首字母大写（如 `"CurrentPage"`），与列表接口实际参数名不一致（如 `current_page`），详见 [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md) 示例  
  - `/export_status` 必须携带 `export_id` 查询参数  

## 使用方式

1. **准备环境**：  
   - 登录百炼控制台，开通服务并创建 API Key（见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
   - 在控制台右上角获取 `workspace_id`  

2. **构造请求**：  
   ```bash
   curl -X GET "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"
   ```

3. **处理响应**：  
   - 成功响应统一含 `success: true` 和 `data` 字段  
   - 错误响应结构分两类：网关层错误（如 `InvalidApiKey`、`Endpoint.AccessDenied`）返回扁平 `{"request_id", "code", "message"}`；业务错误返回嵌套 `{"error": {"code", "message"}}`（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）  
   - 所有接口均返回 `x-request-id` 响应头，用于问题定位  

## 限制和注意事项

- **鉴权与权限**：API Key 具备账号级权限，禁止硬编码或泄露；工作空间不存在或无访问权限时，网关直接返回 `403 Endpoint.AccessDenied`  
- **分页与导出**：  
  - `/policies` 固定返回全量 11 条，**不支持分页**  
  - `/agent_logs` 使用游标分页（`next_page` 字段），非传统 offset 分页  
  - `/export_agent_logs` 提交后需轮询 `/export_status?export_id=...`，仅当 `export_status == "success"` 且 `link` 非空时方可下载  
- **数据时效性**：`/overview` 固定查询最近 24 小时数据，不支持自定义时间范围  
- **字段兼容性**：响应中缺失字段返回 `null`（如 `/asset_summary` 中未挂载的资源类型），而非 `0` 或空数组  
- **错误重试**：遇到 `503` 类服务级错误（如 `12000093`、`12000094`）应指数退避重试，非客户端错误

## 来源文档

- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


