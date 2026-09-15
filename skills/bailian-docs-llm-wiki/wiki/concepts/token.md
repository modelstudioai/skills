# Token

Token 是百炼平台中用于计量模型输入、输出及上下文处理的最小语义单位，是计费、配额控制、限流与资源调度的核心度量基准。一个 Token 通常对应一个子词（subword）或标点符号，在文本场景下近似于英文单词的 3/4 或中文字符的 1–2 个；实际数量由模型专用分词器（Tokenizer）精确计算，不可人工估算。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有模型调用费用均以实际消耗的 Token 总数为唯一依据，包括输入 Prompt、输出 Response 及系统提示词（system message）。训练费用按训练 Token 总数计费，部署费用（PTU）则按每分钟处理的 Token 数（TPM）与时长组合计费。
- **免费额度管理**：华北2（北京）地域为指定模型（如 `qwen3.8-max`）提供 100 万 Token 免费额度，按模型 ID 独立发放、独立消耗，不跨快照版本共享。
- **Token Plan 配额控制**：开发者可创建 Token Plan，设定以千 Token（k-token）为单位的总配额（`quota`）与重置周期（`daily`/`weekly`/`monthly`），绑定至 API Key 后，所有通过该 Key 发起的 `/v1/chat/completions` 或 `/v1/embeddings` 请求自动计入配额。
- **用量监控与观测**：应用监控（Application Monitoring）在「Token 消耗统计」看板中聚合展示各 `app_id` 的实时与历史 Token 使用量，支持按 `trace_id` 下钻分析单次请求的输入/输出 Token 分布。
- **模型能力描述**：模型元数据（如 `/api/v1/models` 返回结果）中包含 `context_length`（最大上下文 Token 数）、`pricing`（按输入 Token 区间分档定价）等字段，直接影响调用设计与成本预估。

## 关键参数和配置

- **计费粒度**：最小计费单位为 **1 token**，无四舍五入或向上取整。
- **Token Plan 配额单位**：`quota` 参数单位为 **千 Token（k-token）**，例如 `quota: 500` 表示 50 万 Token 配额。
- **宽限期**：Token Plan 支持 `grace_period_seconds`（默认 300 秒），超限后允许缓冲期内继续调用，避免瞬时抖动触发限流。
- **精度说明**：配额统计存在 ±50 token 误差，源于分词器实现差异与网关层聚合延迟，不适用于需严格精确到单 token 的审计场景。
- **地域约束**：Token 计费与免费额度严格绑定地域——仅华北2（北京）生效；其他地域调用不参与免费额度抵扣，亦不享受阶梯定价。

## 面向开发者，简洁实用

- ✅ 调用前查模型 `context_length`，避免 `context_length_exceeded` 错误；  
- ✅ 用 `/api/v1/models` 接口动态获取模型 `pricing` 和 `features`，勿硬编码单价；  
- ✅ 生产环境务必为 Token Plan 设置 `sampling_rate < 1.0`（推荐 0.1–0.3），降低监控开销；  
- ✅ 免费额度用完即停开关（`FreeTierOnly`）建议开启，防止意外扣费；  
- ❌ 不要假设 Token 数 = 字符数或字数——始终以 API 响应头 `x-dashscope-token-count-input` / `x-dashscope-token-count-output` 为准；  
- ❌ 不要复用同一 API Key 绑定多个 Token Plan——单 Key 最多绑定 1 个 Plan。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [more about models](../api/more-about-models.md)
- [application monitoring](../guides/application-monitoring.md)


