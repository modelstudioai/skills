# token plan guide

Token Plan 是百炼平台为模型调用提供的资源配额管理机制，用于控制 API 调用的 token 消耗总量与速率。开发者可通过 Token Plan 实现细粒度的用量隔离、成本管控和稳定性保障，适用于个人开发、团队协作及生产级接入场景。其核心能力基于 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中定义的配额模型。

## 支持的模型与功能

- **支持模型**：所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及通过 `model` 参数指定的第三方模型（需已接入百炼网关）  
- **支持功能**：同步推理（`/v1/chat/completions`）、流式响应（`stream=true`）、批量请求（`/v1/batch`）、[函数调用](../concepts/function-calling.md)（`tools`）、以及多模态输入（图像/音频 base64 或 URL）  
- 不支持直接用于模型微调（fine-tuning）或向量检索（RAG）服务的 token 计费——此类场景需单独配置 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `x-ak` | string | 是 | 百炼 AccessKey ID（用于身份鉴权与配额归属） |
| `x-token-plan-id` | string | 否 | 显式指定 Token Plan ID；若不传，则使用该 AK 默认绑定的 Plan |
| `x-rate-limit-policy` | string | 否 | 可选 `burst`（突发模式）或 `smooth`（平滑模式），默认 `burst`；详见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) |

> **注意**：`x-token-plan-id` 在 v3.2+ API 中已替代旧版 `x-plan-id`，后者自 2024-Q3 起废弃，调用将返回 `400 Bad Request` —— 请务必参考 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 更新客户端逻辑。

## 使用方式

1. **创建 Plan**：在控制台「配额管理」→「Token Plan」中新建，设置总配额（如 `1000000` tokens/month）与速率限制（如 `1000 tokens/sec`）  
2. **绑定 AK**：为 AccessKey 分配指定 Plan（支持一对多绑定）  
3. **发起请求**：在 HTTP Header 中携带 `x-ak` 和可选的 `x-token-plan-id`，例如：  
   ```http
   POST /v1/chat/completions HTTP/1.1
   x-ak: ak-xxxxxxxxxxxxxx
   x-token-plan-id: plan-abc123
   Content-Type: application/json
   ```

## 限制和注意事项

- 单次请求最大 token 数受模型上下文窗口限制（如 Qwen2-72B 最大 32768），不受 Token Plan 配额约束  
- 配额按自然月重置（UTC+8），不可跨月累积；超额请求将返回 `429 Too Many Requests`  
- 流式响应中，token 统计以服务端实际生成并返回的 token 为准（含 `content`、`tool_calls`、`stop_reason` 等全部输出 token）  
- 若同时启用 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 与 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)，且 AK 同时归属多个 Plan，系统优先采用显式传入的 `x-token-plan-id`；未显式指定时，以 AK 所属组织层级最高（即团队级）的 Plan 为准

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


