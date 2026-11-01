# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，代表模型处理的最小语义片段（如子词、标点或图像块）。所有模型调用、训练和部署的计费、限流与配额管控均以 Token 为统一计量基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **实时推理（按量调用）**：输入文本/图像/音频经分词器（Tokenizer）转换为输入 Token，模型生成结果为输出 Token；二者分别计费，单位为「百万 Token」。多模态模型（如 Qwen-VL、Qwen-Audio）中，文本 Token 与图像 Token 分开统计，图像 Token 不计入文本 Token 配额。
- **模型训练**：按训练过程中实际消耗的总 Token 数（含上下文、标签、梯度计算相关 token）计费，不同模型类型（文本/图像/视频/语音）采用差异化 Token 定义与折算逻辑。
- **吞吐预留（PTU/DTU）**：TPM（Tokens Per Minute）是核心容量单位，1 kTPM = 1000 Tokens/分钟；长输入（如 >32K）按模型配置的阶梯系数（如 3×）折算，缓存命中 Token 按缓存系数（如 0.2×）额外折减。
- **Token Plan 配额管控**：支持输入 Token 与输出 Token **分离配额**（`input_token_quota` / `output_token_quota`），超出任一维度即触发 `429 Too Many Requests`；流式响应中，完整 Token 统计仅在最后一个 chunk 的 `usage` 字段返回。
- **成本优化与预算**：免费额度（100 万 Token）、Token Plan、节省计划、资源包等均以 Token 为抵扣单位；预算管控可按 Token 消耗量设置阈值，但生产环境不建议启用“用完即停”，以防服务中断。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 |
|--------|----------|------|
| `input_tokens`, `output_tokens` | API 响应体（`usage` 字段） | 实际消耗的输入/输出 Token 数，用于账单核对与用量监控；流式响应中仅最终 chunk 包含完整值。 |
| `max_tokens` | 请求参数（`parameters.max_tokens`） | 控制生成内容的最大输出 Token 数（不含输入），各模型有硬性上限（如 `qwen-max` 为 8192）。 |
| `input_token_quota`, `output_token_quota` | Token Plan 配置 | 每日/每月独立配额，单位为 Token；需在请求 Header 中传入 `X-Plan-ID` 显式指定生效 Plan。 |
| TPM（Tokens Per Minute） | 吞吐预留（PTU/DTU） | 吞吐容量单位，输入按「万TPM」、输出按「千TPM」报价；长输入与缓存命中支持系数折算。 |
| `total_tokens`（已弃用） | — | 旧版文档中提及的合并配额字段，**当前所有 Plan 均不再使用**，请严格按输入/输出分离方式管理。 |

> ⚠️ 注意：  
> - 免费额度**仅覆盖实时推理费用**，不适用于 Batch 调用、模型微调、部署、PAI-DSW 或 OSS 存储；  
> - Batch 调用虽享半价，但仍属“模型调用”范畴，**不可被免费额度抵扣**；  
> - 图像、音频等多模态输入产生的 Token 单独计费，不与文本 Token 混用或共享配额。

## 面向开发者，简洁实用

- ✅ **计费确认**：调用后检查响应 `usage` 字段，验证 `input_tokens + output_tokens` 是否符合预期，避免长 prompt 或高 `max_tokens` 导致意外超支。  
- ✅ **配额监控**：定期调用 `GET /v1/usage/token-plan` 查询周期内用量，结合 `retry-after` 响应头实现客户端指数退避重试。  
- ✅ **性能优化**：对长文本场景，优先选用支持长上下文的模型（如 `qwen3.7-flash`），并利用上下文缓存降低有效 Token 消耗。  
- ❌ **禁止行为**：不要将 `api_key` 或 `X-Plan-ID` 暴露在前端代码或公开仓库中；不要依赖 `total_token_quota` 等过时参数。  
- 🛠️ **调试建议**：使用 `dashscope` SDK 时，开启 `log_level="DEBUG"` 可查看实际 Token 分词过程与用量明细。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)


