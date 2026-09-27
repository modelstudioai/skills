# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为模型调用设计的资源配额与计费管理机制，用于控制 API 调用频次、并发量及总 token 消耗。开发者需根据业务场景选择对应 Plan 类型，并在调用时显式指定 `plan` 参数（部分旧版 SDK 默认 fallback 到 `personal`）。Plan 的生效范围覆盖模型推理、Embedding、Rerank 等核心能力，但不适用于控制台内测功能或未公开的 beta 接口。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 适用于所有已正式发布的百炼模型，包括：
- 文本生成类：`qwen-max`、`qwen-plus`、`qwen-turbo`、`qwen2.5-7b-instruct` 等
- Embedding 类：`text-embedding-v3`、`text-embedding-lite`
- Rerank 类：`bge-reranker-v2-m3`

> **注意**：`qwen-vl-plus` 和 `qwen-audio` 等多模态模型暂不支持 [Token](../concepts/token.md) Plan 控制，其调用仍按请求次数计费；该限制与 [Token Plan 概述](../../raw/model-user-guide/token-plan-guide/token-plan-overview.md) 中“全模型覆盖”的早期描述存在不一致，以当前控制台实际行为为准。

## 关键参数

调用 API 时需在请求头或请求体中传入以下关键参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `plan` | string | 是 | Plan 标识符，如 `"personal"`、`"team"`、`"coding"`；大小写敏感 |
| `model` | string | 是 | 模型 ID，必须与所选 Plan 兼容（例如 `coding` Plan 仅允许调用 `qwen-coder` 系列） |
| `max_tokens` | integer | 否 | 单次响应最大 token 数，受 Plan 配额上限约束（详见 [个人版](../../raw/model-user-guide/token-plan-guide/token-plan-personal.md)） |

## 使用方式

1. **初始化客户端时指定 Plan**（推荐）：  
   ```python
   from aliyunsdkcore.client import AcsClient
   client = AcsClient(plan="team")  # 全局默认 Plan
   ```

2. **单次请求覆盖 Plan**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "X-DashScope-Plan: coding" \
     -d '{"model": "qwen-coder-32b", "input": {"messages": [...]}}'
   ```

3. **SDK 调用示例（Python）**：  
   ```python
   from dashscope import Generation
   Generation.call(
       model='qwen-turbo',
       plan='personal',  # 显式声明，优先级高于客户端全局配置
       ...
   )
   ```

详细接入流程与错误码说明见 [进阶接入](../../raw/model-user-guide/token-plan-guide/token-plan-best-practice.md)。

## 限制和注意事项

- 单个 API Key 最多绑定 3 个不同 Plan（如 `personal` + `team` + `coding`），超出后需解绑旧 Plan；
- Plan 配额按自然日重置，不支持跨日累计或借用；
- 若请求中 `plan` 与 `model` 不匹配（如用 `coding` Plan 调用 `qwen-max`），将返回 `400 Bad Request` 错误，而非降级执行；
- 企业版客户可通过 [团队版](../../raw/model-user-guide/token-plan-guide/token-plan-team-edition.md) 文档了解子账号隔离、用量审计等高级能力；
- 所有 Plan 均禁止用于训练数据回传、模型蒸馏等非推理用途，违者将触发配额冻结。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


