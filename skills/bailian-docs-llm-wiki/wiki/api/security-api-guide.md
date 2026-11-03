# security api guide

Security API 提供 Agent 安全防护数据的查询与告警导出能力，覆盖防护概况、资产统计、策略配置、告警列表及详情等核心场景。所有接口均基于 RESTful 设计，通过标准 HTTP Header 鉴权，并遵循统一的错误响应规范。开发者需先完成工作空间配置与 API Key 获取，再按约定拼装 Endpoint 并发起调用。

## 支持的模型/功能

Security API 不涉及模型推理，而是面向 Agent 安全治理的数据服务接口，当前支持以下 6 类功能：

- **防护概况**：`GET /overview`（固定查询最近 24 小时防护能力开关、模块覆盖状态及拦截统计）  
- **Agent 资产统计**：`GET /asset_summary`（按业务空间聚合 Agent 及其挂载资源数量，如模型、工具、技能、知识库等）  
- **安全策略查询**：`GET /policies`（返回全量 11 条策略，含启用状态、免费标识与风险域分类）  
- **告警管理**：包括 `GET /agent_logs`（游标分页查询）、`GET /agent_logs/{alert_id}`（单条详情）、`POST /export_agent_logs`（提交导出任务）和 `GET /export_status`（轮询导出状态）  
- **策略与告警能力均不支持写操作（如启用/禁用策略、标记告警状态等），仅提供只读查询能力**  

> **注意**：文档 5 中 `policy_code` 列表明确包含 `baseline_check` 和 `vulnerability_scan` 两条免费策略，但文档 4 的 `capabilities` 字段未体现对应能力项；二者定位不同（前者为策略层控制，后者为防护能力层开关），实际使用中应以 `/policies` 接口为准判断策略生效状态。该差异已在[概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)中统一说明。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，详见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角下拉菜单获取 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `current_page` / `page_size` | Query | integer | 否 | 仅 `/agent_logs` 支持分页，默认 `current_page=1`, `page_size=20` |
| `risk_level`, `status`, `asset_type` 等 | Query | string/array | 否 | 告警筛选参数，详见[查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md) |
| `params` | Body (JSON) | string | 是 | `/export_agent_logs` 请求体中必填字段，为告警列表查询参数的 JSON 字符串序列化值（注意非嵌套对象） |

## 使用方式

1. **准备环境**：  
   - 开通百炼服务，创建 API Key（见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
   - 获取 `workspace_id`（控制台右上角）  
   - 拼装 Base URL：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **发起请求示例（curl）**：  
   ```bash
   # 查询防护总览
   curl -X GET "$BASE_URL/overview" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 查询高风险告警（第1页，每页20条）
   curl -X GET "$BASE_URL/agent_logs?risk_level=high&current_page=1&page_size=20" \
     -H "Authorization: Bearer $BAILIAN_API_KEY"

   # 提交告警导出任务（参数需 JSON 字符串化）
   curl -X POST "$BASE_URL/export_agent_logs" \
     -H "Authorization: Bearer $BAILIAN_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"lang":"zh","params":"{\"risk_level\":\"high\"}"}'
   ```

3. **处理响应**：  
   - 成功响应统一含 `"success": true` 和 `data` 字段  
   - 错误响应结构分两类：网关层（扁平 `{"request_id","code","message"}`）与服务层（嵌套 `{"error":{"code","message"}}`），详见[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他 region 将返回 `BadRequest.IllegalEndpoint`（HTTP 400）  
- **分页机制**：告警列表 `/agent_logs` 使用游标分页（`next_page` 字段），不支持 offset 分页；`/policies` 和 `/asset_summary` 无分页，固定返回全量  
- **导出任务约束**：`/export_agent_logs` 的 `params` 字段必须为合法 JSON 字符串（双引号转义），且内容需与 `/agent_logs` 查询参数语义一致；导出结果为 Excel 文件，有效期 24 小时  
- **空值处理**：资产统计接口 `/asset_summary` 中缺失字段返回 `null` 而非 `0`，调用方需做空值判断  
- **鉴权失败响应**：若 API Key 无效或缺失，网关直接返回 `InvalidApiKey`（HTTP 401），不进入业务逻辑层  
- **错误排查**：所有响应头含 `x-request-id`，与响应体 `request_id` 一致，可用于日志追踪；建议在调试阶段优先检查该 ID 对应的完整链路日志

## 来源文档

- [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)
- [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)
- [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


