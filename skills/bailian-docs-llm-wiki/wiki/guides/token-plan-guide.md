# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的按量计费资源包方案，用于调用模型 API 时抵扣 token 消耗。它支持灵活购买、自动续订与多模型共享，适用于测试、开发及中小规模生产场景。相比后付费，[Token](../concepts/token.md) Plan 可降低单位 token 成本，并提供更稳定的预算控制能力。

## 支持的模型与功能

[Token](../concepts/token.md) Plan 当前覆盖百炼平台全部公开模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不支持私有化部署模型或自定义微调模型的专属 endpoint**。基础文本生成、多模态推理、[函数调用](../concepts/function-calling.md)（Function Calling）等核心能力均可用 Token Plan 抵扣；而 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide) 作为独立资源包，专用于代码补全类任务，与 Token Plan 不互通——详见 [原文标题](../../raw/model-user-guide/token-plan-guide.md)。

## 关键参数

- `plan_id`：唯一标识符，购买后由系统分配，用于 API 请求中指定资源包  
- `token_balance`：实时剩余 token 数量，可通过 `/v1/plan/balance` 接口查询  
- `valid_until`：有效期截止时间（UTC），精确到秒，过期未用完自动清零  
- `scope`：取值为 `all_models`（默认）或指定模型 ID 列表（如 `["qwen-max", "qwen-plus"]`），后者需在购买时显式声明  

> **注意**：文档 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中提及“scope 支持 runtime 动态切换”，但该功能已于 v2.3.0 版本下线；当前 scope 仅在购买时锁定，不可修改，请以控制台实际配置为准。

## 使用方式

1. 在控制台「费用中心 → 资源包管理」完成购买（支持按月/季度/年）  
2. 发起 API 请求时，在请求头中添加 `X-DashScope-Token-Plan-ID: <plan_id>`  
3. 若未指定 header 或 plan_id 无效/过期，请求将自动回退至后付费模式  

SDK 调用示例（Python）：
```python
from dashscope import Generation
response = Generation.call(
    model='qwen-max',
    input={'messages': [{'role': 'user', 'content': '你好'}]},
    api_key='your_api_key',
    token_plan_id='tp-xxxxxx'  # 显式传入 plan_id
)
```
更多细节请参考 [原文标题](../../raw/model-user-guide/token-plan-guide.md)。

## 限制和注意事项

- 单个请求最多消耗 100 万 tokens（含输入+输出），超出部分将被截断并返回 `400 Bad Request`  
- Token Plan 不支持跨账号共享；团队版 Token Plan 仅限同一企业主体下的子账号共用  
- 退款政策：未使用 token 可申请全额退款（有效期剩余 ≥7 天），已过期或已消耗部分不可退  
- 同一请求**不可混用多个 Token Plan**；若需分摊成本，须通过不同 API Key 或不同 plan_id 分批调用

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


