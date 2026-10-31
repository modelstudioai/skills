# token plan guide

Token Plan 是百炼平台为模型调用提供的配额管理机制，用于控制 API 调用的 token 消耗量与频次。开发者可通过配置不同 Plan 类型实现资源隔离、成本可控和灰度发布。该机制与模型授权、API Key 权限体系深度集成，适用于个人开发、团队协作及企业级生产接入场景。

## 支持的模型/功能

Token Plan 当前支持全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分第三方模型代理接口（需开通白名单）。不支持直接应用于自定义训练任务或 Model Studio 中的 fine-tuning 作业。具体兼容性请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。Coding Plan 作为子类型，额外支持代码补全、诊断等 IDE 插件链路，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `plan_id`：必填，Plan 唯一标识符（如 `personal-2024-q3`, `team-prod-v2`），由平台分配或通过控制台创建  
- `max_tokens_per_minute`：每分钟最大 token 消耗上限（含 input + output），默认值因 Plan 类型而异  
- `burst_ratio`：突发系数（1.0–3.0），允许短时超额消耗，超出后触发 429 响应  
- `model_whitelist`：可选字符串数组，显式指定允许调用的模型 ID（如 `["qwen-max", "qwen-plus"]`），未设置则继承 Plan 绑定范围  

> **注意**：`burst_ratio` 在 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 文档中标注为“仅企业版支持”，但实测 v2.3+ 版本已向团队版开放，建议以控制台实际配置项为准。

## 使用方式

1. 在 API 请求 Header 中添加 `X-BC-Plan-ID: <plan_id>`  
2. 或在请求 Body 的 `parameters` 字段中嵌入 `"plan_id": "<plan_id>"`（仅限 `/v1/chat/completions` 等标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）  
3. 若使用 SDK，调用时传入 `plan_id` 参数（Python SDK 示例见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)）  
4. 多 Plan 场景下，优先匹配 Header 中的 `X-BC-Plan-ID`，Header 缺失时回退至 Body 参数  

## 限制和注意事项

- 单个 API Key 最多绑定 5 个活跃 Plan；超出需先停用旧 Plan  
- Plan 配置变更（如调整 `max_tokens_per_minute`）通常在 30 秒内生效，但 burst 缓存可能延迟 1–2 分钟  
- 不同 Plan 间 token 消耗不共享、不透支；若请求未携带有效 `plan_id`，将按 API Key 默认 Plan 执行配额检查  
- 请勿在客户端（如浏览器 JS）硬编码 `X-BC-Plan-ID`，存在泄露风险；服务端代理是推荐实践 —— 参考 [玩法攻略](../../raw/model-user-guide/token-plan-guide/token-plan-playbooks.md) 中的网关层封装示例

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


