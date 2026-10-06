# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用频次、并发量及总 token 消耗量。开发者需根据业务场景选择对应 Plan（如个人版、团队版或 Coding Plan），并在调用时显式声明 `plan` 参数以启用配额校验。该机制与模型能力解耦，适用于所有支持按 token 计费的模型 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 支持的模型/功能

- 所有百炼平台托管的 **文本生成类模型**（如 Qwen-Max、Qwen-Plus、Qwen-Turbo）均支持 [Token](../concepts/token.md) Plan 配额控制；
- **不支持**图像生成、语音合成、向量检索等非文本生成类模型；
- Coding Plan 专用于代码补全与解释类任务，仅对 `qwen-coder` 系列模型生效，且需配合 `/v1/coding/completions` 接口使用 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)；
- 多模态模型（如 Qwen-VL）暂不支持 [Token](../concepts/token.md) Plan，其调用仍按请求次数计费。

## 关键参数

调用 API 时需在请求头或 query 参数中指定以下字段：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `plan` | string | 是 | Plan 名称，如 `"personal"`, `"team"`, `"coding"`；必须与所选模型兼容 |
| `max_tokens` | integer | 否 | 单次响应最大 token 数，受当前 Plan 的 `max_output_tokens` 限制 |
| `temperature` | float | 否 | 不影响配额计算，但过高值可能导致实际 token 消耗超出预期 |

> **注意**：部分旧版文档（如 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 中示例）仍将 `plan` 放在 request body 内，**实际仅支持 header（`X-Plan`）或 URL query（`?plan=xxx`）两种方式**，body 方式已被废弃。

## 使用方式

1. **初始化配置**：在控制台「API 密钥」页绑定 Token Plan，或通过 `POST /v1/plans/bind` 接口动态绑定；
2. **发起调用**：在请求中携带 `plan` 参数，例如：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation?plan=team" \
     -H "Authorization: Bearer $API_KEY" \
     -d '{"model": "qwen-plus", "input": {"messages": [...]}}'
   ```
3. **监控用量**：通过 `/v1/plans/usage` 查询实时 token 消耗与剩余配额 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 单个 API Key 最多绑定 **3 个不同 Plan**（如 personal + team + coding），跨 Plan 调用不共享配额；
- Plan 配额按自然日重置，不支持自定义周期；
- 若未传 `plan` 参数，请求将走默认无配额限制通道（可能触发风控拦截或按后付费计费）；
- 当前不支持在流式响应（`stream=true`）中动态切换 Plan，整个 stream 生命周期绑定初始 `plan` 值；
- 团队版 Plan 的成员邀请与权限继承逻辑详见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)，但请注意：该文档中关于“子账号自动继承主账号 Plan”的描述已过时，现需显式调用 `/v1/plans/assign` 接口授权。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


