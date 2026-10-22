# security api guide

Security API 是百炼平台提供的 Agent 安全防护数据查询与告警管理接口集合，面向工作空间维度提供防护概况、资产统计、策略配置、告警检索与导出等能力。所有接口均基于 RESTful 设计，需通过 API Key 鉴权，并严格遵循工作空间路由规则。开发者应首先完成[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)与 Endpoint 拼装，再按需调用具体接口。

## 支持的模型/功能

Security API 不涉及大模型推理，而是聚焦于 Agent 全生命周期安全治理，当前支持以下核心功能模块：

- **防护概况**：`GET /overview` 返回最近 24 小时防护能力开关状态、模块覆盖情况及拦截统计（如 `content_safety`, `file_scan`, `skill_scan`）；`GET /asset_summary` 返回 Agent 及其挂载资源（模型、工具、技能、知识库等）的去重计数。
- **策略管理**：`GET /policies` 固定返回 11 条预置安全策略的启用状态与分类（如 `prompt_attack`, `rag_poisoning`, `baseline_check`），按 `risk_domain` 分组，含免费策略标识。
- **告警全链路**：`GET /agent_logs` 支持游标分页与多维筛选（风险等级、资产类型、处置状态等）；`GET /agent_logs/{alert_id}` 提供单条告警的原始上下文与攻击分析；`POST /export_agent_logs` 与 `GET /export_status` 构成异步导出流程，支持按筛选条件导出 Excel 报表。

> **注意**：文档 7 中 `/agent_logs` 的参数 `status_list`（数组类型）与文档 8、9、10 中实际使用的字符串型 `status` 参数存在不一致；生产环境以文档 7 定义为准，`status_list` 为合法参数，`status` 仅用于单值匹配，二者不可混用。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `Authorization` | Header | string | 是 | 格式为 `Bearer <your-api-key>`，详见[认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `workspace_id` | Host | string | 是 | 工作空间 ID，从百炼控制台右上角获取，拼入 Endpoint 主机名 |
| `region` | Host | string | 是 | 当前仅支持 `cn-beijing`，拼入 Endpoint 主机名 |
| `current_page` / `page_size` | Query | integer | 否 | 告警列表分页参数，默认 `current_page=1`, `page_size=20` |
| `risk_level` | Query | string | 否 | 值为 `high`/`medium`/`low`，用于告警筛选 |
| `params` | Body (JSON) | string | 是 | 导出接口中需传入 URL 查询参数的 JSON 字符串化结果（注意非嵌套对象），格式须与 `/agent_logs` 请求参数完全一致 |

## 使用方式

1. **构造 Endpoint**：  
   `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`

2. **设置鉴权头**：  
   `Authorization: Bearer <your-api-key>`（API Key 在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)创建）

3. **发起请求示例（防护总览）**：  
   ```bash
   curl -X GET "https://my-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/overview" \
     -H "Authorization: Bearer sk-xxx"
   ```

4. **告警导出流程**：  
   - 步骤一：`POST /export_agent_logs` 提交导出任务，`params` 字段需序列化 `/agent_logs` 的完整查询参数（如 `{"risk_level":"high","lang":"zh"}` → `"{"risk_level":"high","lang":"zh"}"`）；  
   - 步骤二：轮询 `GET /export_status?export_id={id}`，等待 `export_status="success"` 且 `link` 非空；  
   - 步骤三：下载 Excel 文件（链接有效期 24 小时）。该流程细节可参考[导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)文档。

## 限制和注意事项

- **地域限制**：Endpoint 中 `region` 仅支持 `cn-beijing`，其他地域将返回 `BadRequest.IllegalEndpoint` 错误码（见[错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）。
- **分页机制**：`/agent_logs` 使用游标分页（`next_page` 字段），不支持传统 offset 分页；`/policies` 无分页，固定返回全量 11 条。
- **字段空值处理**：`/asset_summary` 响应中未统计到的字段返回 `null` 而非 `0`，调用方需做空值判断。
- **错误响应结构**：网关层错误（如 `InvalidApiKey`, `Endpoint.AccessDenied`）返回扁平结构 `{"request_id","code","message"}`；业务层错误（如 `12000093`）返回嵌套结构 `{"error":{"code","message"}}`，需统一解析 `request_id` 用于问题定位。
- **导出参数一致性**：`/export_agent_logs` 的 `params` 字符串必须与 `/agent_logs` 实际请求的 query string **完全一致**（包括大小写与编码），否则导出结果可能为空或报错。

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


