# Token

Token 是百炼平台中用于计量模型调用资源消耗的最小计费与配额单位，代表模型处理的文本、图像、音频等输入或生成内容的基本语义单元。在百炼体系中，Token 不仅是计费依据，更是额度控制、吞吐保障与成本优化的核心度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用（API 层）**：每次请求的 `input tokens`（提示词、上下文、多模态内容编码后长度）与 `output tokens`（模型实际生成内容长度）按 1:1 累加，构成总消耗 token 数，实时扣减所绑定 Token Plan 的剩余额度；超限返回 `402 Payment Required`。
- **计费与成本管理（Billing 层）**：所有按量付费模型（文本、多模态、语音、Embedding、Rerank）均以 token 为最小计费粒度；输入/输出 token 分开结算，缓存命中 token 按折扣单价计费（如 10%），显式缓存创建则按 125% 计费。
- **吞吐预留（TPM 预留）**：以 `kTPM`（千 tokens/分钟）为容量单位，长输入 token 按阶梯系数折算（如 32K–256K 区间 ×3），缓存命中部分再乘缓存折算系数（如 ×0.2），最终从预留额度中扣减。
- **训练与数据处理（Data 层）**：训练集/评测集导入时，系统自动统计 JSONL 或 Excel 中每条样本的 token 长度（基于模型 tokenizer），用于校验数据质量、预估训练成本及设置最大序列长度约束；日志回流生成的数据集也按 token 统计进行规模评估。
- **Token Plan 管理（配额层）**：Token Plan 是跨模型统一的 token 额度容器，支持同步/异步/批量/流式调用；同一 `token_plan_id` 下所有模型共享总额度，不支持按模型隔离——需隔离请创建多个 Plan。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 注意事项 |
|--------|----------|------|-----------|
| `input_tokens` / `output_tokens` | API 响应体 | 每次请求返回的实际消耗 token 数（含 system/user/assistant message 及 content 编码） | 可通过响应头 `X-DashScope-Usage` 获取，格式为 `{"input_tokens":123,"output_tokens":45}` |
| `max_tokens` | API 请求体 | 单次请求允许生成的最大 output token 数 | 受模型能力上限与 Token Plan 剩余额度双重限制；设为 0 表示不限（不推荐） |
| `token_plan_id` | API 请求 Header | 必填，指定本次调用归属的 Token Plan | 需与 API endpoint 所在地域严格匹配（如北京集群 Plan 不可用于杭州 endpoint） |
| `X-Token-Plan-ID` | HTTP Header | 用于传递 `token_plan_id`，启用 Token Plan 配额控制 | 与 `Authorization: Bearer <api_key>` 同时携带，缺一不可 |
| `cache_enabled`（布尔） | API 请求体（高级） | 启用语义缓存时，命中缓存的 input token 按折扣计费 | 缓存创建本身消耗额外 token（+25%），需权衡成本与延迟 |

> ⚠️ 注意：  
> - Token 计算基于百炼平台统一 tokenizer（非开源 HuggingFace tokenizer），相同文本在不同模型下 token 数可能略有差异；  
> - 多模态内容（如 image_url、audio_url）经平台预处理后转换为等效文本 token，其长度计入 `input_tokens`；  
> - 使用 Token Plan 专属 API Key 调用时，**自动跳过新人免费额度**，直接按量扣费。

## 面向开发者，简洁实用

- ✅ **快速验证 token 消耗**：用 DashScope SDK Expert 运行 `dashscope api chat --model qwen-plus --messages "你好" --stream --verbose`，输出中将显示精确的 `input_tokens` 和 `output_tokens`。  
- ✅ **实时查剩余额度**：调用 `GET /v1/token-plan/usage`（Header 带 `X-Token-Plan-ID`），响应含 `remaining_tokens` 和 `used_tokens_today`。  
- ✅ **避免超限失败**：在高并发场景下，建议预估单次请求最大 token（`len(prompt)+max_tokens`），确保 ≤ 当前 `remaining_tokens`；或启用 `402` 重试 + 降级逻辑。  
- ✅ **成本优化优先级**：长期稳定调用 → 开通「AI 通用型节省计划」；短期爆发流量 → 购买「吞吐预留（TPM）」；固定小流量 → 选用「模型专属资源包」。  
- ❌ **禁止行为**：不要硬编码 `token_plan_id` 到前端；不要复用跨地域的 Plan ID；不要假设 `max_tokens=1000` 就能生成 1000 个 token——实际受模型最大上下文与剩余额度双重截断。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [test 1](../guides/test-1.md)
- [model data overview](../guides/model-data-overview.md)


