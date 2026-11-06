# Token

Token 是百炼平台中用于衡量模型输入与输出文本（或多媒体内容）处理粒度的基本计量单位，也是计费、限流与性能监控的核心依据。一个 Token 通常对应一个子词（subword）、标点、空格或特殊控制符；对中文而言，平均约 1–2 个汉字构成 1 个 Token，具体数值由底层分词器（如 Qwen 的 tokenizer）动态确定。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与请求限制**：  
  每次 API 请求的 `input.messages`（含 system/user/assistant 消息）和生成的 `output.text` 均按 Token 统计总长度。不同模型有明确的 **单次请求最大 Token 数限制**（例如 `qwen-turbo` 为 8K，`qwen-max` 为 32K），超出将返回 `400 Bad Request` 错误。该限制包含 prompt + completion 的全部 Token。

- **计费与用量统计**：  
  平台按 **实际消耗的 TotalToken 数** 计费（输入 Token + 输出 Token），精确到个位。用量数据在「模型用量」页面按日/小时展示，并同步至账单；注意：监控页面中的 `模型消耗 TotalToken 数` 仅用于告警与趋势分析，**不作为计费依据**，最终费用以账单为准。

- **性能监控与告警**：  
  在「模型监控」中，`TotalToken 数` 是核心可观测指标，支持配置环比突增、阈值超限等告警规则，帮助识别异常 Prompt、低效提示工程或成本失控风险。同时，`首 Token 延时` 和 `非首 Token 延时` 直接反映 Token 级别的响应效率。

- **多模态模型扩展**：  
  图像、视频、音频等非文本输入经编码后也会转化为等效 Token（如一张 1024×1024 图像在 Qwen-VL 中约等价于 1,500–3,000 Tokens），计入总 Token 配额与用量。上传文件前需确认目标模型的多模态 Token 上限（见各模态文档）。

## 关键参数和配置

- `max_tokens`（请求参数）：  
  控制模型最多生成的 Token 数（不含输入部分）。设为 `1024` 表示最多输出 1024 个 Token；若设为 `0` 或省略，平台将根据模型上下文窗口自动截断。**不保证恰好输出该数量**，实际受 stop words、EOS token 等影响。

- `input.messages` 内容长度：  
  开发者需自行预估或通过 SDK 提供的 `count_tokens()` 工具（如 Python SDK 的 `dashscope.Tokenizer.count_tokens()`）计算消息数组的 Token 数，避免超限。

- Token 计数一致性：  
  百炼所有服务（API、监控、计费）均使用与模型一致的 tokenizer（如 Qwen 系列使用 `QwenTokenizer`），确保输入/输出 Token 数可复现、可验证。不建议依赖第三方 tokenizer 进行配额预估。

- [异步任务](asynchronous-task.md)与批量调用：  
  批量推理（Batch Chat / Batch File）同样按实际消耗 Token 计费，但其 Token 用量**不在「模型监控」图表中展示**，仅可在「模型用量」页面查询。

## 面向开发者，简洁实用

- ✅ **必做**：调用前用官方 tokenizer 预估 Token 数，尤其对长文档、多图、代码块等高密度内容；  
- ✅ **推荐**：在监控中为 `TotalToken 数` 配置「24 小时环比增长 > 200%」类告警，及时发现 Prompt 泄漏或循环生成；  
- ⚠️ **注意**：`max_tokens` 仅限制输出，不限制输入；总 Token = 输入 Token + 输出 Token，两者共同受模型上下文窗口约束；  
- 🔍 **调试技巧**：开启「推理日志」后，响应体中 `usage.input_tokens` 和 `usage.output_tokens` 字段可精确查看本次调用的实际 Token 消耗。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model monitoring](../guides/model-monitoring.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)


