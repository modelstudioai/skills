# specialized model

百炼平台的“专用模型”指针对单一垂直任务深度优化的 Qwen 系列模型，覆盖机器翻译（Qwen-MT）、深度研究（Qwen-Deep-Research）、文字识别（Qwen-OCR）、界面交互（GUI-Plus）四大方向。这些模型大多通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope API 调用，参数与通用对话模型存在差异，使用前需特别关注接口形式、地域支持和专属字段。

## 模型与能力一览

| 方向 | 代表模型 | 主要能力 | 调用方式 |
| --- | --- | --- | --- |
| 机器翻译 | `qwen-mt-plus` | 多语言翻译、术语干预、翻译记忆、领域提示 | OpenAI 兼容 / DashScope |
| 深度研究 | `qwen-deep-research` | 两阶段研究：反问澄清 + 深入分析，返回带引用的报告 | 仅 Python DashScope SDK |
| 文字识别 | `qwen-vl-ocr-latest` | 图像 OCR、票据/结构化字段抽取、[流式输出](../concepts/streaming.md) | OpenAI 兼容 / DashScope |
| 界面交互 | `gui-plus-2026-02-26` | 基于截图执行鼠标/键盘等 GUI 操作，工具调用模式 | OpenAI 兼容 / DashScope |

各模型对应的接口与参数详见 [Qwen-MT API参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)、[Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)、[Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md) 与 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)。

## 接入端点与地域

除 Qwen-Deep-Research 外，其余三类模型均提供 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，`base_url` 因地域而异：

- 华北 2（北京）：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`

HTTP 调用统一为 `POST <base_url>/chat/completions`。GUI-Plus 当前文档仅给出北京地域的端点示例，参考 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)。

> **注意**：不同地域的 API Key 互不通用；切换地域时必须同时更换 `base_url`、HTTP endpoint 和 API Key。详见各文档中“地域”章节，例如 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)。

> **注意**：Qwen-Deep-Research **仅适用于中国大陆版（北京）**，且目前只支持 Python DashScope SDK；Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)均不可用，参见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)。

## Qwen-MT：机器翻译

通过在请求体的 `extra_body.translation_options`（OpenAI 兼容）或 `parameters.translation_options`（DashScope）中传入翻译相关字段调用：

- `source_lang` / `target_lang`：源语言与目标语言，可填 `auto` 让模型自动识别。
- `terms`：术语干预表，`[{source, target}]` 强制将专有名词译为指定术语。
- `tm_list`：翻译记忆，传入历史对照句对让模型保持表达风格一致。
- `domains`：领域提示，使用一段英文描述输入文本所属行业，引导译文风格（例如 IT 领域要保持专业故障排查术语）。

`messages` 内容即为待翻译文本，无需 system [prompt](../guides/prompt.md)。完整字段语义、请求/响应示例可参考 [Qwen-MT API参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)。

## Qwen-Deep-Research：两阶段深度研究

调用流程必须分两步进行：

1. **反问确认**：用户传入一个宽泛的研究主题（如“研究一下人工智能在教育中的应用”），模型流式返回澄清式问题。
2. **深入研究**：把第一步返回的 assistant 内容连同用户的澄清答复（缩小范围的回复）一并放入 `messages`，再次调用同一模型，模型才会进入正式研究。

关键参数：

- `model`：固定为 `qwen-deep-research`。
- `messages`：必须按 `user → assistant → user` 三轮顺序组织上下文。
- `output_format`（可选）：
  - `model_detailed_report`（默认）：完整深度报告，约 6000 tokens。
  - `model_summary_report`：精炼摘要报告，约 1500-2000 tokens。

响应通过 SSE 流式返回，`output.message.phase` 标识当前阶段（`ResearchPlanning` / `WebResearch` / `KeepAlive` / `answer`），并在 `answer` 与 `WebResearch` 阶段通过 `extra.deep_research.references`、`webSites` 返回引用网页列表。详细字段、状态机和示例响应见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)。

## Qwen-OCR：图像文字识别

调用方式遵循多模态 chat completions 规范，`messages[].content` 为数组：

- `{"type": "image_url", "image_url": {"url": "..."}}`：传入图像 URL（也支持 base64）。
- `{"type": "text", "text": "..."}`：可选 Prompt；不传时使用默认 Prompt `Please output only the text content from the image without any additional descriptions or formatting.`，仅做纯文本提取。
- `min_pixels` / `max_pixels`：图像预处理的像素阈值，控制放缩范围（示例值 `32*32*3` 至 `32*32*8192`）。

支持[流式输出](../concepts/streaming.md)，开启方式与通用 chat 接口一致：`stream=True`，`stream_options={"include_usage": True}`。模型名建议使用 `qwen-vl-ocr-latest` 跟随最新版本。结合 Prompt 可让模型按 JSON schema 输出结构化字段（如车票发票号码、票价、座位号），示例见 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)。

## GUI-Plus：界面交互模型

GUI-Plus 用于让模型基于屏幕截图执行鼠标/键盘等 GUI 操作，调用形态本质是“截图 + 工具调用”：

- `model`：当前文档示例使用 `gui-plus-2026-02-26`。
- `messages[0]`：必须传入 system [prompt](../guides/prompt.md)，定义可用的 `computer_use` 工具（包含 `key`、`type`、`mouse_move`、`left_click`、`left_click_drag`、`scroll`、`wait`、`terminate`、`answer`、`interact` 等动作）以及输出格式约束。
- `messages[1]`：用户消息，`content` 中一并传入屏幕截图（`image_url`）和自然语言指令。
- `extra_body.vl_high_resolution_images`：建议设为 `true`，让模型按高分辨率处理截图，便于定位坐标。

模型按照 system [prompt](../guides/prompt.md) 约束的格式返回：第一行 `Action:` 简要描述要做的操作，紧跟一个 `<tool_call>` 块，其中 JSON 给出 `name=computer_use` 与具体 `arguments`（动作类型、坐标、文本等）。客户端解析后执行动作并把新截图回传给模型，循环直到 `action=terminate`。完整 system [prompt](../guides/prompt.md) 与示例代码见 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)。

## 使用前的通用注意事项

- **API Key 与环境变量**：所有调用都需要先获取 API Key 并配置 `DASHSCOPE_API_KEY` 环境变量；不同地域的 Key 不可混用。
- **SDK 兼容性**：Qwen-MT、Qwen-OCR、GUI-Plus 三类模型同时支持 OpenAI 兼容与 [DashScope 接口](../concepts/dashscope-api.md)；Qwen-Deep-Research 仅支持 Python DashScope SDK 与等价的 curl 调用。
- **请求体差异**：[OpenAI 兼容接口](../concepts/openai-compatible-api.md)下，所有专属字段（如 `translation_options`、`vl_high_resolution_images`）应放在 `extra_body` 内；[DashScope 接口](../concepts/dashscope-api.md)则放在 `parameters` 中。
- **响应解析**：Qwen-Deep-Research 与 Qwen-OCR 推荐使用[流式输出](../concepts/streaming.md)，需要按 SSE 逐块拼接 `content`；GUI-Plus 客户端需自行解析 `<tool_call>` JSON 并把执行结果回填到 `messages`。
- **图像与坐标**：GUI-Plus 与 Qwen-OCR 都接受图像输入；GUI-Plus 还需要客户端按模型返回的坐标在真实屏幕上执行动作，确保渲染分辨率与模型理解一致。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/specialized-model/qwen-mt-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/specialized-model/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)






