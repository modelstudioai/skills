# model management

模型管理是百炼平台为开发者提供的核心能力，用于发现、授权、限流和监控模型使用。通过统一的 REST API，开发者可程序化地查询可用模型、检查权限状态、设置调用配额，并动态调整业务空间内的模型访问策略。所有操作均基于 API Key 认证，适用于多地域、多业务空间的生产环境。

## 支持的模型与功能

百炼平台支持跨供应商、多模态、全场景的模型生态，包括文本生成（`TG`）、视觉理解（`VU`）、图像生成（`IG`）、视频生成（`VG`）、语音识别（`ASR`）等能力。模型来源覆盖 `qwen`、`zhipu-ai`、`wan`、`mini-max`、`kling` 等十余家供应商，推理服务由 `aliyun-bailian`、`siliconflow`、`moonshot` 等提供。可通过 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 接口按 `capabilities`、`providers`、`features`（如 `function-calling`、`structured-outputs`）等维度筛选，并获取上下文长度、定价、输入/输出模态等元信息。

模型权限分为三类：`inference`（调用）、`fine_tune`（微调）、`deploy`（部署）。默认仅开放部分基础模型的推理权限；未授权模型无法调用，即使其在 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md) 中可见。权限状态需通过 [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) 显式确认。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model` | 模型唯一 ID，API 调用必需字段 | `"qwen3.8-max"` | 所有接口通用 |
| `request_limit` / `request_limit_period` | 请求频率限制（QPS/RPM），`period=1` 表示每秒，`period=60` 表示每分钟 | `500` / `1`（QPS）；`2` / `60`（RPM） | [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) |
| `usage_limit` / `usage_limit_period` | 用量限制（TPM），单位为 [Token](../concepts/token.md) 数，周期单位为秒 | `500000` / `6`（6 秒内上限） | [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) |
| `authorization_scope` | 权限查询范围：`AUTHORIZABLE`（可授权）或 `AUTHORIZED`（已授权） | `"AUTHORIZED"` | [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md) |
| `access_all_entities` | 一键授权开关：`OPEN`（授权全部推理模型）、`CLOSE`（清空）、`KEEP`（默认） | `"OPEN"` | [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md) |

> **注意**：文档 4 中 `update-model-rate-limits.md` 的请求示例 Endpoint 使用了 `https://dashscope.aliyuncs.com/api/v1/models/limits`（无 `{WorkspaceId}`），但其他所有文档（包括文档 1、3、4 的请求说明正文）均明确要求替换 `{WorkspaceId}`。实际调用必须使用带 WorkspaceId 的地址，否则返回 404。该不一致属于文档过时，请以 [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md) 中的 Endpoint 格式为准。

## 使用方式

### 1. 发现模型
调用 `GET /api/v1/models`，支持分页与多维筛选：
```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/models?capabilities=TG&providers=qwen&page_no=1&page_size=50" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 2. 检查权限
调用 `GET /api/v1/models/permissions?authorization_scope=AUTHORIZED` 获取当前业务空间已启用的模型及权限明细。

### 3. 查询配额
调用 `GET /api/v1/models/limits?model=qwen3.8-max` 查看账号级与业务空间级限流配置，含 `request_limit`、`usage_limit` 及异步任务限制（`async_user_concurrency_limit` 等）。

### 4. 更新权限
- **逐模型**：`POST /api/v1/models/permissions`，传 `models=[{"model":"qwen-plus","inference":true}]`
- **一键授权**：传 `{"access_all_entities": "OPEN"}`，自动授权所有当前及未来新增的推理模型。

### 5. 更新限流
调用 `POST /api/v1/models/limits`，支持 `OVERLAY`（合并覆盖）与 `DELETE`（删除）：
```json
{
  "models": [{
    "model": "qwen-plus",
    "operation_type": "OVERLAY",
    "request_limit": 60,
    "request_limit_period": 60,
    "usage_limit": 100000,
    "usage_limit_period": 60
  }]
}
```
> **注意**：若需“仅设 QPM、不限 TPM”，必须分两步：先 `DELETE` 清除现有配额，再 `OVERLAY` 设置 QPM。单次请求不可只设 `request_limit` 而留空 `usage_limit`，否则报错 `Cannot set TPM without QPM`（见 [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)）。

## 限制和注意事项

- **配额继承关系**：业务空间级限流（`workspace_limit`）不能超过账号级限流（`model_limit`），且 `workspace_limit` 为 `null` 表示未单独设置，完全继承 `model_limit`。
- **异步任务限制**：部分模型（如 `wan2.6-i2v-flash`）额外限制 `async_user_queue_limit`（排队数）和 `async_user_concurrency_limit`（并发数），需在配额响应中显式检查。
- **PTU 部署模型**：支持 `deployment_methods=ptu` 的模型需额外配置预置吞吐量，其限流逻辑独立于常规 QPM/TPM，详见 [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)。
- **权限生效延迟**：授权变更后，新 token 或新会话立即生效；但已有长连接可能缓存旧权限，建议客户端重试或刷新认证上下文。
- **错误处理**：所有接口共用统一错误码体系，失败时参考 [错误信息](raw/model-api-reference/preparations/error-code.md) 文档排查，而非各接口末尾的孤立链接（该路径在 Wiki 中将被自动解析）。

## 来源文档

- [查询模型限额](../../raw/model-api-reference/model-management/list-quotas.md)
- [查询模型列表](../../raw/model-api-reference/model-management/list-models.md)
- [查询模型授权](../../raw/model-api-reference/model-management/list-model-permissions.md)
- [更新模型限流](../../raw/model-api-reference/model-management/update-model-rate-limits.md)
- [更新模型授权](../../raw/model-api-reference/model-management/update-model-permissions.md)


