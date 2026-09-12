# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的按量计费资源包方案，用于调用模型 API 时抵扣 token 消耗。它支持灵活购买、自动续订与多模型共享，适用于测试、开发及中小规模生产场景。相比后付费，[Token](../concepts/token.md) Plan 可降低单位 token 成本，并提供更稳定的预算控制能力。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 当前覆盖百炼平台全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不支持私有化部署模型或自定义微调模型的专属 endpoint**。基础文本生成、多模态推理、Function Calling 均可使用 Token Plan 抵扣；而 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide) 为独立资源包，与 Token Plan 不互通，需单独购买。详见 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中的分类说明。

## 关键参数

- `plan_id`：唯一标识符，购买后由系统分配，用于 API 请求中指定资源包  
- `remaining_tokens`：实时剩余 token 数量（可通过 `/v1/token_plan/balance` 接口查询）  
- `valid_until`：有效期截止时间（UTC+8），精确到秒，过期未用完自动作废  
- `scope`：取值为 `all_models`（默认）或指定 model_id 列表，后者需在购买时显式声明  

> **注意**：原始文档中提及“scope 支持按模型组配置”，但当前 API 实际仅接受 `all_models` 或精确 model_id 字符串数组；模型组（如 `qwen-plus-group`）暂未开放该能力，以 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 的最新接口文档为准。

## 使用方式

1. 购买：通过控制台「费用中心 → 资源包」或 OpenAPI `PurchaseTokenPlan` 下单  
2. 绑定：无需手动绑定，同一阿里云主账号下所有子账号调用支持模型时自动优先抵扣可用 Token Plan  
3. 调用：在 API 请求 Header 中添加 `X-DashScope-Token-Plan-ID: <plan_id>` 即可强制指定使用某资源包（否则按有效期+余额最优匹配）  
4. 查询：调用 `GET /v1/token_plan/balance?plan_id=xxx` 获取实时余额，响应结构与 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 完全一致

## 限制和注意事项

- 单次请求消耗 token 超过单个 Plan 剩余量时，系统**不会跨 Plan 拆分抵扣**，将直接回退至后付费（若已开通）或报错 `InsufficientTokenPlanBalance`  
- Token Plan 不支持退款、转让或跨主账号共享  
- 同一请求中不可混用多个 Token Plan；若需多 Plan 协同管理，请自行实现余额轮询逻辑  
- 有效期与 token 余额均以服务端时间为准，客户端务必校准 NTP 时间，避免因时间偏差导致 `valid_until` 判定异常

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


