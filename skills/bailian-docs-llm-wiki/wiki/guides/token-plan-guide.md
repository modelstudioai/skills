# token plan guide

Token Plan 是百炼平台为开发者提供的模型调用配额管理机制，用于控制 API 调用量、保障服务稳定性并支持按需弹性伸缩。它适用于不同规模的应用场景，从个人实验到企业级生产部署均可配置对应策略。所有 Token Plan 均基于实际请求的输入/输出 token 数进行计量，计费与用量统计统一由平台后端实时完成。

## 支持的模型/功能

当前 Token Plan 适用于百炼平台全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型（Fine-tuned Model），但**不支持**离线推理 SDK、本地部署模型或通过 `model.export` 导出的模型实例。图像理解（Qwen-VL）、语音转文本（Qwen-Audio）等多模态能力均纳入统一 token 计量体系，其 token 消耗按 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中定义的换算规则计算。

## 关键参数

- `max_tokens`：单次请求允许生成的最大 token 数（默认 2048，上限 8192）  
- `temperature` / `top_p`：不影响 token 计量，但影响实际输出长度和 token 分布  
- `input_token_limit`：部分高并发场景下可配置输入长度硬限制（需联系技术支持开通）  
- `plan_id`：绑定至具体 Token Plan 实例的唯一标识，用于路由和配额校验，详见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)  

> **注意**：文档中曾提及 `max_output_tokens` 参数名，但该字段已于 v2.3.0 版本统一替换为 `max_tokens`；旧参数名已失效，请以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的最新接口定义为准。

## 使用方式

1. 在控制台「模型服务」→「Token Plan」中创建计划，选择版本（个人版/团队版）并设置月度 quota  
2. 调用 API 时在请求 header 中添加 `X-Plan-ID: <your_plan_id>`  
3. 若未显式传入 `X-Plan-ID`，系统将自动 fallback 至账户默认 plan（如无则报错 `403 Forbidden`）  
4. 配额超限后请求立即失败，错误码为 `429 Too Many Requests`，响应体含剩余重试窗口时间（`Retry-After` header），参考 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中的熔断处理示例。

## 限制和注意事项

- 单个 plan 最多绑定 50 个 API Key；超出需新建 plan 或解绑闲置 key  
- 团队版 plan 的 quota 不可跨成员共享，每个成员使用独立子配额（见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)）  
- Coding Plan 为独立子类，仅适用于 `/v1/coding/completions` 等专用 endpoint，不兼容通用 `/v1/chat/completions` 接口  
- 所有 token 计量以平台侧解析结果为准，客户端预估的 token 数（如 tiktoken 计算）可能存在 ±3% 偏差，建议以实际返回的 `usage` 字段为准

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


