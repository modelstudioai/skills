# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，也是计费、限流、上下文长度控制和性能监控的核心度量标准。一个 Token 通常对应一个子词（subword）或标点符号，在中文场景下约等于 1–2 个汉字，英文场景下约等于 1 个单词或标点；具体切分由模型所用 tokenizer 决定。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（API 请求）**：  
  `max_tokens` 参数限制模型单次响应的最大输出 Token 数（如 `qwen3.7-plus` 默认上限为 8192）；`messages` 中所有内容（含 system prompt、user 和 assistant 消息）共同构成输入 Token，总长度受模型上下文窗口限制（如 `qwen3.8-max` 为 32768 tokens）。超出将触发 `400 Bad Request` 错误。

- **计费与用量统计**：  
  百炼按 **总 Token 数 = 输入 Token + 输出 Token** 计费（部分[多模态](multi-modal.md)模型按图像张数/音频秒数等独立计费单位核算，但文本生成类模型统一以 Token 为准）。在「模型用量」控制台中，可按分钟/小时/天维度查看各模型的 `TotalToken` 消耗，用于成本分析与预算管控。

- **[模型评测](model-evaluation.md)（Evaluation）**：  
  评测任务中，被测模型对每条 `Prompt` 的推理会消耗输入 + 输出 Token，产生推理费用；裁判模型（如 `qwen3.8-max`）对每条 `Output` 打分时也按 Token 计费。Token 消耗量直接影响评测成本，小规模验证建议先用 ≤100 条样本预估开销。

- **模型监控（Monitoring）**：  
  `TotalToken` 是核心监控指标之一，与调用次数、失败率、首 Token 延迟等并列展示。告警规则可基于 `TotalToken` 设置阈值（如“单小时超 100 万 Token”），及时发现异常调用或爬虫行为。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 典型取值范围 | 注意事项 |
|--------|----------|------|--------------|----------|
| `max_tokens` | API 调用（OpenAI/DashScope） | 控制模型输出最大 Token 数 | `1`–`8192`（依模型而异，`qwen3.8-max` 最高支持 `8192`） | 不设或设为 `0` 将使用模型默认值；设过高可能增加延迟与费用，且不保证实际输出长度 |
| `input_tokens` / `output_tokens` | API 响应体（`usage` 字段） | 实际消耗的输入/输出 Token 数 | 非负整数 | [OpenAI 兼容接口](openai-compatible-api.md)返回 `"usage": {"prompt_tokens": N, "completion_tokens": M}`；DashScope 返回 `"usage": {"input_tokens": N, "output_tokens": M}` |
| `TotalToken` | 监控与用量报表 | 单次请求的 `input_tokens + output_tokens` 总和 | 同上 | 控制台用量统计、告警规则、账单明细均以此字段为依据；不包含系统内部处理开销 |

> 💡 提示：可通过 SDK 或响应头 `X-DashScope-Usage`（格式为 `{"input_tokens":N,"output_tokens":M}`）实时获取本次调用的精确 Token 消耗，便于客户端做动态限流或成本预估。

## 面向开发者，简洁实用

- **估算 Token 数**：本地可使用 `tiktoken`（OpenAI 兼容）或 `transformers.AutoTokenizer` 加载对应模型 tokenizer 进行粗略计算（如 `qwen3` 系列推荐使用 `QwenTokenizer`）；生产环境请以 API 响应中的 `usage` 字段为准。
- **优化 Token 开销**：
  - 缩短 system prompt，避免冗余描述；
  - 对长文档做分块摘要或提取关键句再输入；
  - 使用 `qwen3.8-flash` 等高性价比模型处理简单任务；
  - 流式响应（`stream=True`）不减少总 Token 消耗，但可降低首 Token 延迟感知。
- **调试技巧**：若遇到 `context_length_exceeded` 错误，优先检查 `messages` 总长度（非字符数）；使用百炼控制台「API 调试」工具可直观查看分词结果与 Token 统计。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model monitoring](../guides/model-monitoring.md)


