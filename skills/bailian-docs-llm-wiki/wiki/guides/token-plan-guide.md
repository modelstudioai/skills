# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的配额管理机制，用于控制 API 调用的 token 消耗额度与计费粒度。它适用于不同规模的应用场景，支持按模型、调用方式和账户层级灵活配置额度策略。开发者需结合自身业务节奏选择合适 plan 类型，并在调用时显式声明 `plan` 参数以生效配额控制。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 及第三方接入模型），但不适用于异步批量推理（`/v1/batch`）和模型微调训练任务。实时流式响应（`stream=true`）和非流式调用均受 plan 配额约束。具体支持范围详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

- `plan`: 字符串类型，必填。取值包括 `"personal"`、`"team"`、`"coding"`，对应不同额度策略与计费规则；
- `model`: 必填，指定目标模型 ID（如 `qwen-max`），其 token 计算逻辑由该模型的 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 文档定义；
- `input_tokens` / `output_tokens`: 仅限预估调用（`/v1/tokenize`）返回，不可手动设置；实际消耗以服务端统计为准。

> **注意**：原始文档中 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 提到 `plan=free` 为合法值，但该值已于 v2.3.0 版本废弃，当前 API 将返回 `400 Bad Request`；请改用 `plan=personal` 并确认账户已开通个人版权限。

## 使用方式

在标准 `/v1/chat/completions` 或 `/v1/embeddings` 请求的 JSON body 中添加 `plan` 字段：

```json
{
  "model": "qwen-plus",
  "plan": "team",
  "messages": [{"role": "user", "content": "你好"}]
}
```

若未传 `plan`，系统将按账户默认 plan（通常为 `personal`）执行配额检查。多 plan 场景下，建议通过 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中的路由策略示例实现动态切换。

## 限制和注意事项

- 单次请求 `input_tokens + output_tokens` 不得超过所选 plan 的单次上限（`personal` 为 32k，`team` 为 64k，`coding` 为 16k）；
- plan 配额按自然日重置，不支持跨日累积或借用；
- 同一 API Key 下并发请求共享 plan 额度，无 per-request 隔离；
- `plan` 参数不参与缓存键计算，即相同 [prompt](prompt.md)+model+plan 组合的响应可能因 plan 额度耗尽而返回 `429 Too Many Requests`。

> **注意**：[Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md) 文档中描述的“自动降级至 `personal`”行为仅适用于 IDE 插件客户端，在 REST API 中不生效；API 调用必须显式指定有效 plan 值，否则报错。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


