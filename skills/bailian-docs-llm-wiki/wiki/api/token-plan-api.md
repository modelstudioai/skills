# token plan api

[Token](../concepts/token.md)Plan API 是百炼平台用于组织级资源配额与成员席位管理的核心接口集合，主要支撑 [Token](../concepts/token.md) 配额分配、成员邀请、API Key 生命周期管理及组织维度用量统计等能力。该 API 不直接参与模型推理调用，而是服务于企业客户对模型服务访问权限和资源消耗的精细化管控。所有接口均需通过阿里云 RAM 凭据或 [Token](../concepts/token.md)Plan 专属 API Key 进行鉴权，详见 [TokenPlan](../../raw/model-api-reference/token-plan-api.md)。

## 支持的模型/功能

TokenPlan API **不绑定具体大模型**（如 Qwen 系列），其功能完全独立于推理模型，聚焦于组织治理层：
- 席位生命周期管理：分配、回收、移除成员（[TokenPlan](../../raw/model-api-reference/token-plan-api.md)）
- 邀请机制控制：创建/获取/撤销邀请链接，配置邀请策略（[TokenPlan](../../raw/model-api-reference/token-plan-api.md)）
- 凭据管理：生成、重置 TokenPlan API Key（[TokenPlan](../../raw/model-api-reference/token-plan-api.md)）
- 组织状态查询：获取组织信息、成员与席位统计、订阅明细、共享包列表等只读接口

> **注意**：原始文档中 `成员数量和席位数量情况展示` 出现两次（分别指向 `/get-organization-member-seat-stats` 和 `/get-subscription-stats`），但后者实际返回的是订阅层级用量汇总（含 Token 消耗趋势），前者仅返回实时计数；二者语义不同，开发时请按实际需求选择，避免误用。

## 关键参数

所有接口共用以下基础参数（部分接口有额外字段）：
- `org_id`（路径参数）：目标组织唯一标识，必填。可通过 `/get-token-plan-account-detail` 获取当前账号下所有组织。
- `Authorization`（Header）：支持两种格式：  
  - `Bearer <token_plan_api_key>`（推荐，专用密钥）  
  - `Bearer <ram_access_token>`（需具备 `tokenplan:FullAccess` 权限）
- `page_size` / `page_number`（Query）：适用于列表类接口（如 `/list-organization-members`），默认分页大小为 20。

## 使用方式

1. **获取 API Key**：首次使用前，调用 `/create-token-plan-key` 生成专属密钥（响应含 `api_key` 和 `key_id`）；密钥可用于所有 TokenPlan 接口，**不可用于模型推理 API**。  
2. **发起请求**：以 `/list-organization-members` 为例：  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/tokenplan/orgs/{org_id}/members" \
     -H "Authorization: Bearer YOUR_TOKEN_PLAN_API_KEY"
   ```  
3. **处理响应**：成功响应均为 `200 OK`，数据结构统一包裹在 `result` 字段内（如 `{"result": {...}}`），错误码遵循阿里云标准（4xx/5xx + `code`/`message`）。

## 限制和注意事项

- 单组织最大成员数为 5000，单次分页最多返回 100 条记录（`page_size` 上限为 100）。  
- API Key 无自动轮转机制，需主动调用 `/rotate-token-plan-key` 更新；旧密钥立即失效，**不影响已分配席位的有效性**。  
- `/get-subscription-seat-details` 返回的席位状态可能滞后最多 5 分钟，实时性要求高的场景建议结合 `/get-organization-member-seat-stats` 的瞬时快照交叉验证。  
- 所有写操作（如 `/assign-seats`、`/revoke-token-plan-invite-link`）均为同步执行，但席位生效依赖下游服务异步同步，通常在 30 秒内完成。

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


