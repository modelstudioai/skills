# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费单元，用于统一管理 API 调用中的输入/输出 token 消耗。它替代了早期按请求次数或固定套餐的计费模式，使资源使用更透明、可预测。开发者需在调用前确认所选模型是否支持 [Token](../concepts/token.md) Plan，并正确配置 `top_p`、`temperature` 等参数以避免意外超限。

## 支持的模型/功能

当前 [Token](../concepts/token.md) Plan 已覆盖全部百炼公有云模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及部分私有化部署模型。不支持旧版 `qwen-1.8b-chat` 和已下线的 `qwen-7b-chat-v1`。多模态模型（如 Qwen-VL）的图像 token 计入总消耗，具体换算规则见 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。Coding Plan 作为子集，仅适用于代码补全类场景，其 token 计费逻辑与主 Plan 独立，详见 [Coding Plan](../../raw/model-user-guide/token-plan-guide/coding-plan-guide.md)。

## 关键参数

- `max_tokens`：硬性上限，超出将直接截断并返回 `400 Bad Request`；  
- `top_p` / `temperature`：影响输出长度与多样性，间接影响实际 token 消耗；  
- `stream`：流式响应不改变总 token 消耗，但可能因分块导致客户端误判剩余配额；  
- `repetition_penalty`：过高值易引发重复生成，显著增加输出 token 数量。  
所有参数行为均以 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md) 中的实测基准为准。

## 使用方式

1. 在控制台「API 密钥」页绑定 Token Plan 套餐（个人版或团队版）；  
2. 调用 `/v1/chat/completions` 时，`Authorization` 头中使用对应 API Key；  
3. 配额实时扣减，可通过 `/v1/usage` 接口查询当日剩余 token；  
4. 团队版支持子账号额度继承与独立监控，配置入口见 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md)。

## 限制和注意事项

- 单次请求 `input + output` token 总和不得超过套餐单日上限的 5%（例如 100 万 token 套餐，单次最多 5 万）；  
- 免费试用额度不可叠加，且不适用于私有化模型；  
- > **注意**：原始文档中 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md) 提到“支持按小时重置”，但该功能已于 2024-06-15 下线，实际为自然日重置，请以控制台实时显示为准；  
- 流式响应中若发生连接中断，已发送的 token 仍会计费；  
- 图像、音频等非文本输入的 token 换算系数随模型版本更新而调整，最新系数表请参考 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md)。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


