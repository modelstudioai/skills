# token plan guide

Token Plan 是百炼平台为模型调用设计的资源配额与计费单元，用于统一计量 API 调用消耗（含输入/输出 token、图像 token、[函数调用](../concepts/function-calling.md)等）。开发者需根据业务场景选择匹配的 Token Plan 类型，并在调用时显式指定 `plan` 参数以启用对应配额与计费策略。所有 Token Plan 均基于实际消耗按量结算，不支持跨类型混用。

## 支持的模型与功能

Token Plan 适用于百炼平台全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及部分专属模型，但**不支持**推理加速服务（如 vLLM 部署实例）和离线批量处理任务。图像理解、语音转文本、结构化输出（JSON Schema）、工具调用（Function Calling）等功能均纳入 Token Plan 计量范围。具体支持模型列表详见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 关键参数

- `plan`: 必填字符串，取值为 `"personal"`、`"team"` 或 `"coding"`，对应不同配额与计费规则；
- `model`: 必填，指定调用的模型 ID（如 `"qwen-max"`），必须与所选 `plan` 兼容；
- `input_tokens` / `output_tokens`: 只读字段，由平台自动返回，用于调试与用量核对；
- `enable_tracing`: 可选布尔值，启用后可在 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中查看细粒度 token 拆分（如 [prompt](prompt.md) template 占比、tool call 参数 token 数）。

> **注意**：文档 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中提及 `"pro"` plan 已于 2024 年 7 月下线，当前仅保留 `"personal"`、`"team"` 和 `"coding"` 三类；旧文档中引用的 `"pro"` 示例已过时，请以 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 和 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 的最新参数说明为准。

## 使用方式

1. 在 API 请求 Header 中添加 `X-DashScope-Token-Plan: <plan>`（推荐），或  
2. 在请求 Body 中传入 `"plan": "<plan>"`（仅限 `/v1/services/aigc/text-generation/generation` 等标准接口）；  
3. 调用成功后，响应头中将返回 `X-DashScope-Used-Tokens`，响应体中 `usage` 字段包含详细拆分（需 `enable_tracing=true`）；  
4. 配额余量可通过 `/v1/usage/token-plan` 接口实时查询（需对应 plan 的访问权限）。

## 限制和注意事项

- 同一请求**不可混用多个 plan**，且 `plan` 必须与调用方账号所属版本一致（例如个人账号无法使用 `"team"` plan）；
- 图像 token 按 1:175 换算为文本 token（即 1 张 1024×1024 图 ≈ 175k text tokens），该换算系数在 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中有详细示例；
- 超出配额的请求将返回 `429 Too Many Requests`，错误码为 `ResourceExhausted`，不触发自动升配；
- `plan` 参数对流式响应（`stream=true`）同样生效，但 `usage` 仅在最终 `data: [DONE]` 帧中返回。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


