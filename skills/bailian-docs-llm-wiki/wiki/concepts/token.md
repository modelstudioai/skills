# Token

Token 是百炼平台中用于计量模型输入与输出文本（或多媒体内容）处理规模的最小语义单位，也是计费、限流和资源配额的核心度量基准。一个 token 通常对应一个子词（subword）、标点、空格或图像/音频编码后的基础单元；具体切分方式由底层模型的 tokenizer 决定，不直接等价于字符或字。

## 在百炼平台的不同场景中，这个概念如何使用

- **API 调用计费**：所有模型服务（如 `test 1`、Realtime API、模型体验）均按实际消耗的 tokens 计费——包括输入 [prompt](../guides/prompt.md) 的 tokens 和模型生成的 output tokens。例如，一次请求若输入 320 tokens、输出 180 tokens，则总计费 500 tokens。
- **资源包抵扣**：Token Plan 购买的资源以「token 数量」为单位，调用时自动按实际消耗抵扣；支持跨模型共享（如 `qwen-max` 和 `qwen-vl` 共用同一份 token 余额），但不适用于私有化或微调模型。
- **能力边界控制**：
  - 单请求总 tokens（input + output）受硬性限制（如 `test 1` 最高 4096，`qwen2.5-vl` 最高 128K）；
  - `max_tokens` 参数仅限制输出长度，不包含输入 tokens；
  - 超出限制将直接返回 `400 Bad Request`，不会截断后继续执行。
- **流式响应监控**：启用 `stream_options.include_usage=true` 后，流式响应末尾会返回 `usage` 字段，精确给出本次请求的 `prompt_tokens`、`completion_tokens` 和 `total_tokens`。
- **模型体验调试**：控制台「模型体验」页面实时显示每次运行的 token 消耗（含多模态输入的图像编码开销），便于快速评估成本与性能。

## 关键参数和配置

- `max_tokens`（整型，可选）：指定模型最多生成的 tokens 数。默认值因模型而异（如 `test 1` 默认 1024，`qwen2.5-vl` 默认 8192），超出上下文窗口上限将报错。
- `stream_options.include_usage`（布尔，仅流式请求）：设为 `true` 时，在流式响应结束事件（如 `data: {"type":"message_stop",...}`）后追加一条含 `usage` 字段的数据帧。
- `X-DashScope-Token-Plan-ID`（HTTP Header）：显式指定用于抵扣的 Token Plan ID；未提供或无效时自动回退至后付费。
- 无全局 token 配置项：token 切分逻辑完全由模型绑定的 tokenizer 决定，开发者不可自定义分词规则或修改 token 定义。

## 面向开发者，简洁实用

- ✅ 始终检查 `usage` 字段（尤其在流式或批量调用中）来验证 token 消耗是否符合预期；
- ✅ 使用 `/v1/models` 接口查询目标模型的 `context_length` 和 `max_output_length`，避免因超限导致 400 错误；
- ✅ 图像/音频等多模态输入会产生额外 tokens（如一张 1024×1024 图像经 Qwen-VL tokenizer 编码后约消耗 1200 tokens），需在 `max_tokens` 预留余量；
- ❌ 不要假设 token ≈ 字符数（中文平均 ~1.5 字/ token，英文平均 ~0.75 词/ token）；
- ❌ 不要依赖 `top_p` 或 `temperature` 改变 token 总数——它们只影响生成内容，不影响计费 token 量；
- ⚠️ 免费额度、Token Plan、后付费三者互斥：同一请求只能归属一种计费模式，无法拆分抵扣。

## 关联主题页

- [test 1](../guides/test-1.md)
- [token plan guide](../guides/token-plan-guide.md)
- [model experience](../guides/model-experience.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [release notes](../guides/release-notes.md)


