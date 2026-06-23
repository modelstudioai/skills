# [more](more.md) models

百炼平台除了通义千问系列主力模型外，还提供多个面向特定场景的专用模型，涵盖法律咨询、意图识别、深度研究、机器翻译、GUI 自动化操作和 OCR 文字提取等能力。这些模型均可通过 DashScope API（[OpenAI 兼容接口](../concepts/openai-compatible.md)或 [DashScope SDK](../concepts/dashscope-sdk.md)）调用，开发者可根据业务需求选择合适的模型快速集成。

## 模型一览

| 模型名称 | 能力方向 | 上下文长度 | 调用方式 |
|---------|---------|-----------|---------|
| farui-plus | 法律行业大模型 | 12k | [DashScope SDK](../concepts/dashscope-sdk.md) (Python/Java) |
| tongyi-intent-detect-v3 | 意图理解 | 8,192 | OpenAI 兼容 / [DashScope SDK](../concepts/dashscope-sdk.md) |
| qwen-deep-research | 深度研究 | - | DashScope Python SDK / curl |
| qwen-mt-plus / qwen-mt-turbo | 机器翻译 | - | OpenAI 兼容 / [DashScope SDK](../concepts/dashscope-sdk.md) |
| gui-plus-2026-02-26 | GUI 界面交互 | - | OpenAI 兼容 / [DashScope SDK](../concepts/dashscope-sdk.md) |
| qwen3.5-ocr | OCR 文字提取 | - | OpenAI 兼容 / [DashScope SDK](../concepts/dashscope-sdk.md) |

## 法律行业模型（通义法睿）

[通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)是以千问为基座、经法律行业数据训练的专用模型，具备法律问答、案情分析、法律文书生成、合同审查等能力。模型名称为 `farui-plus`，上下文长度 12k、最大输出 2k，输入成本 20 元/百万 Token。

调用方式与标准千问模型一致，通过 [DashScope SDK](../concepts/dashscope-sdk.md) 的 `Generation.call` 接口，将 `model` 参数设为 `"farui-plus"` 即可。支持单轮对话、多轮对话和[流式输出](../concepts/streaming.md)。

## 意图理解模型

[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)由 `tongyi-intent-detect-v3` 模型提供，能在百毫秒级时间内解析用户意图并选择合适的工具。输入成本 0.4 元/百万 Token，输出成本 1 元/百万 Token，开通后 90 天内有 100 万 Token 免费额度。

该模型支持三种工作模式：

- **意图 + [函数调用](../concepts/function-calling.md)**：在 System Message 中声明工具列表并加上 `Response in INTENT_MODE.`，模型返回包含 `<tags>`、`<tool_call>`、`<content>` 三段结构化输出，需使用正则解析。
- **仅意图分类**：在 System Message 中提供意图标签列表，模型直接返回匹配的标签。可用大写字母映射意图以将输出控制在 1 个 Token，进一步降低延迟。
- **仅[函数调用](../concepts/function-calling.md)**：仅声明工具信息，不添加 `INTENT_MODE` 指令。

## 深度研究模型（Qwen-Deep-Research）

[Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)描述了该模型的两阶段调用流程：

1. **反问确认阶段**：发送初始研究主题，模型返回澄清式问题，帮助聚焦方向。
2. **深入研究阶段**：将反问内容和用户回答拼入 messages，模型进行网络搜索并生成研究报告。

> **注意**：Qwen-Deep-Research 仅支持华北2（北京）地域，需使用该地域的 API Key。当前仅支持 Python [DashScope SDK](../concepts/dashscope-sdk.md) 和 curl，暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible.md)。

响应中包含多个阶段标识（`ResearchPlanning` → `WebResearch` → `KeepAlive` → `answer`），`answer` 阶段的 `extra.deep_research.references` 提供引用来源。通过 `output_format` 参数可选择详细报告（约 6000 Token）或摘要报告（约 1500-2000 Token）。

## 机器翻译模型（Qwen-MT）

[Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)介绍了专用翻译模型的调用方式。通过 `translation_options` 参数控制翻译行为：

- **基础翻译**：指定 `source_lang` 和 `target_lang`（支持 `"auto"` 自动检测源语言）。
- **术语干预**：通过 `terms` 数组指定术语对照，确保专有名词翻译一致。
- **翻译记忆**：通过 `tm_list` 提供参考译文，引导模型遵循已有翻译风格。
- **领域提示**：通过 `domains` 字段描述文本领域背景，提升翻译专业度。

该模型支持多地域部署（北京、新加坡、美国弗吉尼亚），不同地域使用不同的 `base_url` 和 API Key。

## GUI 界面交互模型（GUI-Plus）

[GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)描述了专用于桌面 GUI 自动化操作的视觉模型。模型接收屏幕截图和用户指令，输出结构化的操作动作（点击、输入、滚动、拖拽等）。

调用时需在 System Message 中声明 `computer_use` 工具的完整 function schema，用户消息中以 `image_url` 传入截图。模型返回 `<tool_call>` 格式的操作指令，包含 `action`（如 `left_click`、`type`、`scroll`）和 `coordinate` 等参数。屏幕分辨率默认为 1000x1000，建议开启 `vl_high_resolution_images` 以提升识别精度。

## OCR 文字提取模型（Qwen-OCR）

[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)介绍了基于视觉语言模型的 OCR 能力。模型名称为 `qwen3.5-ocr`，支持从图片中提取文字并按 Prompt 格式化输出（如结构化 JSON）。

关键参数：

- `min_pixels` / `max_pixels`：控制输入图像的像素阈值，影响识别精度和成本。
- 用户可在 `text` 字段传入自定义 Prompt 指定提取格式，未传入时使用默认 Prompt 直接输出纯文本。

该模型同样支持多地域部署（北京、新加坡、弗吉尼亚），支持流式和非[流式输出](../concepts/streaming.md)。

## 通用调用前提

所有模型均需完成以下准备：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并 [配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
2. 如使用 SDK 调用，需先 [安装对应 SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（OpenAI SDK 或 [DashScope SDK](../concepts/dashscope-sdk.md)）。
3. 注意各模型的地域限制和 SDK 支持情况，选择匹配的 `base_url`。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)




