# more models

百炼平台提供一系列面向特定任务的专用模型（more models），覆盖意图理解、机器翻译、深度研究、OCR文字识别及GUI界面交互等场景。这些模型通过统一的 API 接口调用，支持 OpenAI 兼容模式与 DashScope 原生 SDK，适用于需要高精度、低延迟或结构化输出的生产级应用。所有模型均需配合业务空间专属域名使用以获得最佳性能。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由与工具编排场景。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **机器翻译**：`qwen-mt-plus`，支持多语言互译、术语干预与翻译记忆，适用于技术文档、本地化内容等高质量翻译需求。
- **深度研究**：`qwen-deep-research`，仅限华北2（北京）地域调用，支持两阶段交互式研究（反问确认 + 深度分析），可自动联网检索并生成结构化研究报告。
- **OCR文字识别**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等，支持图像中文字提取、结构化信息抽取（如车票、合同字段），兼容 URL 与 Base64 图像输入。
- **GUI界面交互**：`gui-plus`，专为桌面自动化设计，支持结合截图与指令执行鼠标/键盘操作，可调用 `computer_use` 工具链完成真实 GUI 任务。

> **注意**：文档 4 与文档 5 中对 `min_pixels` 默认值的描述存在不一致——文档 4 明确指出 `qwen3.5-ocr` 的 `min_pixels` 默认值为 `3072`（`3×32×32`），而文档 5 对 `gui-plus` 的 `min_pixels` 默认值标注为 `3136`（`4×28×28`），但未说明是否适配 `qwen3.5-ocr`。实际调用时请严格按目标模型文档配置，避免因像素阈值误设导致图像预处理异常。

## 关键参数

各模型共性关键参数如下（具体取值范围与默认值依模型而异）：

| 参数 | 类型 | 说明 | 备注 |
|------|------|------|------|
| `model` | string | 必填，模型名称（如 `tongyi-intent-detect-v3`, `qwen-mt-plus`） | 不同模型地域支持不同，例如 `qwen-deep-research` 仅支持华北2（北京） |
| `messages` | array | 必填，对话消息数组；支持 `text` 和 `image_url` 类型内容（OCR/GUI类模型必需） | `image_url.url` 可为公网 URL 或 Base64 Data URL；`min_pixels`/`max_pixels` 控制图像缩放行为，详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `translation_options` | object | `qwen-mt-plus` 专用，含 `source_lang`, `target_lang`, `terms`, `tm_list` 等子字段 | 非 OpenAI 标准字段，需通过 `extra_body` 传入（Python SDK）或顶层传入（HTTP/curl） |
| `output_format` | string | `qwen-deep-research` 专用，取值 `model_detailed_report`（默认）或 `model_summary_report` | 影响输出长度与详略程度 |
| `enable_thinking` | boolean | `gui-plus` 专用（仅 `gui-plus-2026-02-26` 支持），开启后返回 `reasoning_content` 字段 | 非 OpenAI 标准参数，须放入 `extra_body` |

> **注意**：`temperature` 与 `top_p` 功能重叠，官方明确建议「只设置其中一个值」；`presence_penalty` 在文档 4 中默认值为 `0.0`，在文档 5 中默认值为 `1.5`，调用 GUI-Plus 时应以文档 5 为准，调用 OCR 模型时以文档 4 为准。

## 使用方式

### 1. 域名与认证
所有 `more models` 均**必须使用业务空间专属域名**，不可继续使用旧版 `dashscope.aliyuncs.com` 域名：
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com`

其中 `{WorkspaceId}` 为控制台「业务空间详情」页获取的实际 ID。API Key 需已配置至环境变量 `DASHSCOPE_API_KEY`，并安装对应 SDK（[DashScope SDK](../preparations/install-sdk.md) 或 [OpenAI SDK](../preparations/install-sdk.md)）。

### 2. 调用示例（核心差异）
- **意图理解模型**：需在 `system` message 中声明 `Response in INTENT_MODE.` 并注入工具定义 JSON，响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **机器翻译模型**：`translation_options` 必须作为 `extra_body`（Python）或顶层字段（Node.js/curl）传入，不可置于 `messages` 内。
- **深度研究模型**：**仅支持 DashScope Python SDK**，且必须分两步调用（先反问确认，再传入 `assistant` 消息与用户澄清后发起深入研究），不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
- **OCR 与 GUI 模型**：`messages.content` 必须为数组，内含 `{"type": "image_url", "image_url": {"url": "..."} }` 及可选文本 [prompt](../guides/prompt.md)；`max_tokens` 截断阈值需按模型规格设定（如 `qwen3.5-ocr` 最大支持 32768）。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他模型虽多地可用，但业务空间专属域名需与 API Key 所属地域严格匹配。
- **SDK 限制**：`qwen-deep-research` 明确不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)；`dashscope CLI` 当前不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **图像参数一致性**：`qwen3.5-ocr` 与 `qwen-vl-ocr-2025-11-20` 使用 `32×32` 像素/[Token](../concepts/token.md) 换算规则，而 `qwen-vl-ocr` 及更早版本使用 `28×28`；`min_pixels`/`max_pixels` 默认值与取值范围必须严格匹配所用模型版本，否则将触发图像预处理失败。
- **流式响应**：`stream=true` 时，OCR/GUI 模型需逐块读取响应，并注意 `include_usage=true` 仅在**最后一个数据块**中返回 token 统计。
- **免费额度**：`tongyi-intent-detect-v3` 提供 100 万 [Token](../concepts/token.md) 免费额度（开通后 90 天内有效），其他模型暂未在原始文档中声明免费策略。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


