# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，代表模型处理的最小语义片段（如子词、标点或符号）。在计费、限流、性能监控与资源配额等核心环节，Token 是统一的度量基准。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与用量统计**：所有模型调用按实际消耗的 `input_tokens`（提示词/上下文）和 `output_tokens`（生成结果）计费；费用明细、账单汇总及用量报表均以 Token 为单位呈现。  
- **限流控制**：业务空间可配置 `token_per_second_limit`（每秒 Token 消耗上限），用于防止突发流量冲击；该限制作用于整个空间内所有模型调用的 Token 总和。  
- **模型监控**：监控系统自动采集并展示每分钟输入/输出 Token 总量（`input_token_count`, `output_token_count`），支持趋势分析与异常检测；自定义模型需返回标准 `x-bailian-token-count` Header 才能被准确统计。  
- **推理参数约束**：`max_tokens` 参数直接限制单次响应的最大输出 Token 数，取值范围为 `[1, 模型最大输出 Token]`（如 `qwen-max` 当前上限为 8192）；超出将触发 `InvalidParameter` 错误。  
- **吞吐预留（DTU/PTU）**：专属部署容量以 TPM（Tokens Per Minute）为单位购买和分配，`input_tpm` 与 `output_tpm` 分别对应输入/输出 Token 的每分钟保障额度。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `max_tokens` | 单次请求允许生成的最大输出 Token 数 | 必须 ≤ 模型能力上限；设为 `0` 或负数将报错；不设则使用模型默认值（通常为 2048） |
| `token_per_second_limit` | 业务空间级每秒 Token 消耗硬上限 | 仅对非默认业务空间生效；设为 `0` 表示不限流；超限请求立即返回 `429 Too Many Requests` |
| `input_tpm` / `output_tpm` | DTU/PTU 部署的输入/输出 Token 每分钟保障额度 | 创建时需为模型基准 TPM 的整数倍；实际使用中超出部分可能被限速或拒绝 |
| `x-bailian-token-count`（响应 Header） | 自定义模型必须返回的 Token 统计 Header | 格式为 `{"input":123,"output":456}`；缺失则监控中 Token 字段恒为 `0` |

> ⚠️ 提示：Token 计数由百炼服务端统一计算（基于模型 tokenizer），开发者无需自行分词；但若使用 `response_format={"type":"json_object"}`，需注意其对 `max_tokens` 的实际占用（JSON 结构本身也计入 Token）。

## 面向开发者，简洁实用

- ✅ **快速验证 Token 消耗**：发起一次最简请求后，检查响应中的 `usage` 字段（[OpenAI 兼容接口](openai-compatible-interface.md)）或 `output.usage`（DashScope 原生接口），获取 `prompt_tokens` 和 `completion_tokens`。  
- ✅ **调试限流问题**：若遇到 `429` 错误，优先检查 `token_per_second_limit` 配置，并用监控页查看实时 Token 消耗曲线。  
- ✅ **优化成本**：长上下文场景下，`input_tokens` 占比高，可考虑摘要预处理或启用前缀缓存（DTU/PTU 支持）降低重复计算开销。  
- ❌ **避免误区**：Token ≠ 字符数 ≠ 词数；不同模型 tokenizer 差异大（如 `qwen3` 与 `glm-5` 的分词结果不一致），切勿跨模型估算。  
- 📌 **工具推荐**：使用百炼控制台「模型体验」页的 Token 计数器，或调用 `/v1/tokenize` 接口（需开通权限）进行离线预估。

## 关联主题页

- [preparations](../api/preparations.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application permission management](../guides/application-permission-management.md)
- [model monitoring](../guides/model-monitoring.md)


