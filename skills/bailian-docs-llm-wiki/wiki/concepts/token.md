# Token

Token 是百炼平台中用于计量模型输入与输出文本长度的基本单位，也是计费、配额控制、资源调度和性能评估的核心度量基准。一个 Token 通常对应一个子词（subword）或标点符号，在中文场景下平均约等于 1.5–2 个汉字，具体取决于分词器（如 Qwen 的 tokenizer）的切分策略。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费与成本管理**：所有文本生成类模型（如 `qwen-plus`、`qwen3.8-max`）均按实际消耗的 `input_tokens + output_tokens` 计费；多模态（如 `qwen-vl`）、语音（如 `qwen-tts`）、图像（如 `wanx2.1-t2i`）等模型也基于等效 Token 或像素/时长换算为 Token 进行计费。
- **Token Plan 配额控制**：通过 `plan` 参数启用配额校验后，每次调用的总 token 消耗（含 prompt 和 completion）将实时扣减所属 Plan 的日额度（如 `team` 版每日 1000 万 tokens）；Coding Plan 仅对 `/v1/coding/completions` 接口及 `qwen-coder` 系列模型生效。
- **模型部署计费模式选择**：
  - *Token 按量*：仅适用于 LoRA 微调模型，按实际调用 token 数实时计费；
  - *PTU（预置吞吐）*：以 TPM（Tokens Per Minute）为容量单位，`ptu_capacity` 中的 `input_tpm`/`output_tpm` 直接对应每分钟可处理的 token 量；
  - *DTU/MU（独占算力）*：虽按模型单元或 TPM 计费，但实际吞吐能力仍以 token 处理速率（TPM）为底层指标。
- **模型评测**：当使用「评测数据集」触发被测模型推理时，会产生 `input_tokens + output_tokens` 的推理费用；若启用「大模型评估」维度，裁判模型（如 `qwen-max`）对每条样本的评分过程同样消耗 token。
- **异步与文件调用**：多模态模型（如 `qwen-vl-plus`）在解析 `oss://` 图片 URL 时，视觉编码器会将图像转换为等效 token 序列参与计算，该部分 token 会计入总消耗。

> ⚠️ 注意：非文本生成类任务（如向量检索、Function Calling 调用本身、联网搜索插件）不产生 token 消耗，但其触发的后续模型推理（如 LLM 决策或结果生成）仍计入 token。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 开发者须知 |
|------|----------|------|-------------|
| `input_tokens` / `output_tokens` | 计费、监控、调试 | 响应头中返回的实际消耗值（如 `X-DashScope-Usage-Input-Tokens: 1247`），是账单与用量统计的唯一依据 | 不可设置，仅读取；可用于客户端 token 预估与 budget 控制 |
| `max_tokens` | 所有文本生成调用 | 限制模型生成的最大输出 token 数；受当前 Token Plan 的 `max_output_tokens` 限制（如 `personal` 版上限为 2048） | 设置过大会导致超配额失败（403）；建议设为业务所需最小值 |
| `plan` | Token Plan | 请求头 `X-Plan` 或 query 参数 `?plan=xxx`，启用配额校验 | 必填且必须与模型兼容（如 `coding` plan 不能用于 `qwen-plus`）；body 方式已废弃 |
| `temperature`, `top_p`, `repetition_penalty` | 生成质量控制 | 影响输出多样性与稳定性，**不改变 token 消耗量**，但可能间接导致实际输出长度波动 | 高 `temperature` 可能引发更长/更短响应，建议压测时固定该类参数以稳定 token 预估 |

## 面向开发者，简洁实用

- ✅ **必做**：所有生产环境文本生成调用，务必显式传 `plan` 参数并监控 `X-DashScope-Usage-*` 响应头，避免意外超限或后付费。
- ✅ **推荐**：用 `max_tokens` 主动约束输出长度，既控成本又防超时；结合 `stream=true` 实时流式消费时，token 消耗仍按完整响应累计。
- ✅ **避坑**：
  - 不要依赖字符数估算 token —— 使用 [DashScope Tokenizer 工具](https://help.aliyun.com/zh/dashscope/developer-reference/token-calculator) 或 SDK 的 `count_tokens()` 方法精确计算；
  - Token Plan 绑定的是 API Key，不是模型或业务空间；单 Key 最多绑 3 个 Plan，跨 Plan 不共享额度；
  - 免费额度、资源包、节省计划、Token Plan 的抵扣顺序为：**免费额度 > 资源包 > 节省计划 > Token Plan > 按量付费**，需按优先级规划采购。
- ✅ **调试技巧**：本地开发时，用 `curl -v` 查看响应头中的 `X-DashScope-Usage-*` 字段，快速验证 token 消耗是否符合预期。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [test 1](../guides/test-1.md)
- [model deployment index](../guides/model-deployment-index.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [more about models](../api/more-about-models.md)


