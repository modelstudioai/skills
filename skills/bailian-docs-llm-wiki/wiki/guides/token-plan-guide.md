# token plan guide

[Token](../concepts/token.md) Plan 是百炼平台为开发者提供的资源配额管理机制，用于控制模型调用的 token 消耗量与频次。它适用于不同规模的应用场景，支持按需配置、实时监控和灵活升降级。开发者需结合自身业务流量特征选择合适的 Plan 类型，并在 API 调用中显式声明 `plan` 参数以生效。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前覆盖百炼平台全部公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及基础推理能力（`chat`、`completion`、`embedding`），但**不支持**以下场景：  
- 自定义微调模型（fine-tuned models）的独立配额管理；  
- 流式响应（streaming）中的分块 token 统计暂未纳入 Plan 实时扣减（详见 [进阶配置](https://help.aliyun.com/zh/model-studio/token-plan-best-practice)）；  
- 语音转文本（ASR）与文本转语音（TTS）等非大模型服务（参见 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide)）。  
> **注意**：原始文档中 [Token Plan 概述](https://help.aliyun.com/zh/model-studio/token-plan-overview) 将 ASR/TTS 列为支持功能，但该信息已过时；实际以控制台最新配额策略为准，建议参考 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中的链接说明并交叉验证控制台界面。

## 关键参数

调用 API 时需在请求体（JSON）中传入以下字段：  
- `plan`: 字符串，必填，取值为 `"personal"`、`"team"` 或 `"advanced"`（对应个人版、团队版、进阶版）；  
- `model`: 字符串，必填，指定具体模型 ID（如 `"qwen-max"`）；  
- `max_tokens`: 整数，可选，用于限制单次响应长度，不影响 Plan 配额计算逻辑；  
- `stream`: 布尔值，可选，若设为 `true`，需注意 token 扣减发生在请求完成时（非逐块扣减）。  
所有参数均区分大小写，且 `plan` 值必须与账户已开通的 Plan 类型严格匹配，否则返回 `403 Forbidden`。

## 使用方式

1. **开通 Plan**：登录百炼控制台 → 进入「配额管理」→ 选择对应版本并完成开通（个人版免费，团队版/进阶版需实名认证）；  
2. **API 调用示例**（使用 `curl`）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "plan": "team",
           "input": {"messages": [{"role": "user", "content": "你好"}]}
         }'
   ```
3. **监控用量**：控制台「配额中心」提供小时级 token 消耗图表，支持导出 CSV；也可通过 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 提供的 OpenAPI 查询实时余量（`/v1/usage/token-plan`）。

## 限制和注意事项

- 单个 API 请求最多消耗当前 Plan 小时配额的 10%，超限将被拒绝（错误码 `429 Too Many Requests`）；  
- Plan 配额按自然小时重置（UTC+8），不支持手动刷新或跨小时累积；  
- 同一账号下多个应用共享同一 Plan 配额，无法按应用粒度隔离；  
- 若同时开通了 [Token](../concepts/token.md) Plan 和 Coding Plan，二者配额**完全独立**，不可互通（详见 [原文标题](../../raw/model-user-guide/token-plan-guide.md) 中的 [Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan-guide) 链接）；  
- 降级 Plan（如从 `team` 降至 `personal`）后，剩余配额不退还，新 Plan 配额立即生效。

## 来源文档

- [Token Plan](../../raw/model-user-guide/token-plan-guide.md)


