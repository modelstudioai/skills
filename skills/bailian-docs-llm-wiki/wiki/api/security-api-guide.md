# security api guide

Security API 是百炼平台提供的 Agent [安全防护](../concepts/security.md)数据查询与告警管理接口集合，用于获取防护能力状态、资产分布、策略配置及安全告警详情。所有接口均基于统一 Endpoint 和 Bearer [Token](../concepts/token.md) 鉴权，响应结构标准化，适用于自动化监控与安全运营集成。开发者需先完成工作空间配置与 API Key 获取，方可调用全部能力。

## 支持的模型/功能

Security API 不涉及模型推理，而是提供**防护数据面**的可观测性能力，覆盖以下五大安全域（依据 [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中 `risk_domain` 分类）：

- **模型交互安全**：内容安全、提示词攻击防护、敏感数据外泄检测  
- **运行环境与工具安全**：MCP 工具调用安全、Skills 静态扫描、网络防护  
- **知识与记忆安全**：RAG 数据投毒、记忆窃取防护  
- **身份与凭证安全**：Agent 身份签发、凭证隔离、Session 生命周期治理  
- **配置与组件安全**：基线检查（免费）、漏洞检测（免费）  

对应能力通过 `/overview`、`/policies`、`/agent_logs` 等接口暴露，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例 |
|------|------|------|------|------|
| `Authorization` | Header | string | 必填，Bearer [Token](../concepts/token.md) 格式，值为百炼 API Key | `Bearer ak-xxxxx` |
| `BASE_URL` | — | URL | 必填，拼接规则：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security` | 见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) |
| `alert_id` | Path | string | `/agent_logs/{alert_id}` 路径参数，纯数字字符串 | `4289016` |
| `export_id` | Query | integer | `/export_status?export_id=...` 查询参数，取自导出接口返回值 | `131231` |
| `params` | Request Body | string | `/export_agent_logs` 的 `params` 字段需为**序列化后的 JSON 字符串**（非对象），且字段名首字母大写（如 `CurrentPage`） | `"{"CurrentPage":1,"RiskLevel":"high"}"` |

> **注意**：文档 7 中导出接口的 `params` 字段要求为字符串化 JSON，且字段命名风格（PascalCase）与列表查询接口（camelCase）不一致，实际使用时需按文档 7 格式序列化，否则导出任务将失败。

## 使用方式

### 1. 基础调用流程
```bash
# 设置环境变量（替换为实际值）
export WORKSPACE_ID="your-workspace-id"
export BAILIAN_API_KEY="ak-xxxxx"
export BASE_URL="https://${WORKSPACE_ID}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security"

# 查询防护总览（24 小时统计）
curl -X GET "$BASE_URL/overview" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"

# 查询告警列表（高风险、按时间倒序）
curl -X GET "$BASE_URL/agent_logs?risk_level=high&order_by=check_time&order=desc" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"

# 查询单条告警详情
curl -X GET "$BASE_URL/agent_logs/4289016" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

### 2. 告警导出（两步式）
```bash
# 步骤1：提交导出任务（注意 params 是字符串）
curl -X POST "$BASE_URL/export_agent_logs" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lang": "zh",
    "params": "{\"CurrentPage\":1,\"RiskLevel\":\"high\"}"
  }'

# 步骤2：轮询导出状态（直到 export_status == "success" 且 link 非 null）
curl -X GET "$BASE_URL/export_status?export_id=131231" \
  -H "Authorization: Bearer $BAILIAN_API_KEY"
```

### 3. 其他核心接口
- `/asset_summary`：获取 Agent 及挂载资源总数（模型、工具、技能、知识库等）  
- `/policies`：获取全部 11 条策略的启用状态与分类（含免费策略标识）  
- `/export_status`：检查导出任务进度与下载链接有效性  

## 限制和注意事项

- **地域限制**：Endpoint 仅支持 `cn-beijing` 地域，其他地域请求将失败。  
- **时间窗口固定**：`/overview` 接口固定返回最近 24 小时数据，不支持自定义时间范围。  
- **分页机制**：告警列表 `/agent_logs` 使用游标分页（`current_page` + `page_size`），`next_page` 为 `null` 表示末页；导出任务则无视分页，导出当前筛选条件下的**全部匹配记录**。  
- **字段空值处理**：当某项统计不可用时（如未启用某模块），响应中对应字段返回 `null` 而非 `0` 或空数组（见 [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md) 说明）。  
- **错误码统一**：所有接口共用错误码体系，如 `12000093`（云安全服务异常）需重试，详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。  
- **鉴权强依赖**：缺少或错误的 `Authorization` Header 将导致 `401 Unauthorized`，无降级行为。

## 来源文档

- [查询防护总览](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)
- [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)
- [查询 Agent 资产](../../raw/application-api-reference/security-api-guide/security-api-protection-overview/security-api-assets.md)
- [查询安全策略](../../raw/application-api-reference/security-api-guide/security-api-policies.md)
- [查询告警详情](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alert-detail.md)
- [查询告警列表](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-alerts.md)
- [导出告警](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export.md)
- [查询导出状态](../../raw/application-api-reference/security-api-guide/security-api-policies/security-api-export-status.md)


