# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别和GUI自动化等方向。这些模型在通用大模型基础上进行了领域精调或架构增强，支持更精准的任务执行与更高性能的推理体验。所有模型均通过 DashScope SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，需配合业务空间专属域名以获得最佳稳定性与延迟表现。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 地域支持 | 文档参考 |
|----------|------|-----------|-----------|-----------|
| `farui-plus` | 法律大模型 | 法律咨询、案情分析、文书生成、合同审查、RAG检索增强 | 华北2（北京）、新加坡、中国香港 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策、多标签分类 | 华北2（北京）、新加坡、中国香港 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 + 网络检索 + 报告生成） | **仅华北2（北京）** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr`, `qwen-vl-ocr-*` | 多模态OCR模型 | 图像文本提取、结构化信息抽取（如车票、合同）、高分辨率图像适配 | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-*`（如 `gui-plus-2026-02-26`） | GUI自动化模型 | 基于截图的桌面操作（点击、输入、滚动、等待）、[函数调用](../concepts/function-calling.md)驱动界面交互 | 华北2（北京）、新加坡 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而其他模型（如 `farui-plus`、`tongyi-intent-detect-v3`）在文档中均列出多地域支持，但未明确排除其他地域。若在非北京地域调用 `qwen-deep-research`，将返回错误，此限制不可绕过。

## 关键参数

所有模型共用以下基础参数（部分为 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)标准字段，DashScope SDK 中对应 `GenerationParam` 属性）：

- `model`: 必填字符串，模型标识符（如 `"farui-plus"`）。
- `messages`: 必填数组，按对话顺序组织的 `role`/`content` 对；`content` 支持纯文本或含 `image_url` 的多模态输入（见 OCR 和 GUI-Plus 文档）。
- `result_format` / `response_format`: 推荐设为 `"message"` 以获取结构化输出（`choices[0].message.content`）。
- `stream`: 布尔值，启用流式响应（`True`/`true`），适用于长输出或低延迟场景。
- `max_tokens`: 输出长度上限，各模型默认值不同（如 `qwen3.5-ocr` 默认 32768，`qwen-vl-ocr` 系列旧版默认 4096）。

**模型特有关键参数**：
- `tongyi-intent-detect-v3`：依赖 `system` message 中显式包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯意图分类）指令，否则无法触发对应模式。
- `qwen-deep-research`：**不支持 `output_format` 参数以外的生成控制参数**（如 `temperature`、`top_p`），其行为由两阶段流程严格定义；该模型也**暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**，仅 Python DashScope SDK 可用。
- `qwen3.5-ocr` / `gui-plus-*`：支持 `min_pixels` 和 `max_pixels` 控制图像预处理分辨率，且像素-Token 转换规则因模型版本而异（`32×32` vs `28×28`），详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- `gui-plus-*`：`vl_high_resolution_images` 为布尔开关，启用后忽略 `max_pixels` 并强制使用 12845056 像素上限；`enable_thinking` 仅对特定版本（如 `gui-plus-2026-02-26`）有效，用于返回 `reasoning_content` 字段。

## 使用方式

### 1. 基础准备
- 获取并配置 API Key：参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 安装 SDK：Python 或 Java 版 DashScope SDK（[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)），或 OpenAI SDK（需兼容模式）；
- **必须配置业务空间专属域名**：华北2（北京）地域使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。现有全局域名（如 `dashscope.aliyuncs.com`）虽仍可用，但[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 均强调新域名可提供“卓越性能和更高稳定性”。

### 2. 典型调用模式
- **单轮对话**（如法睿生成起诉书）：构造 `messages = [{'role': 'user', 'content': '...'}]`，直接调用 `Generation.call()`。
- **多轮对话**（如法睿迭代修改文书）：将上一轮 `response.output.choices[0].message` 追加至 `messages` 数组，再发起新请求。
- **[流式输出](../concepts/streaming-output.md)**（如 Deep Research 实时反馈各阶段状态）：设置 `stream=True`，循环读取响应流，解析 `message.phase`（如 `"WebResearch"`、`"answer"`）及 `status` 字段。
- **多模态输入**（如 OCR 提取车票）：`messages[0].content` 为数组，含 `{"type": "image_url", "image_url": {"url": "..."}}` 和 `{"type": "text", "text": "Prompt..."}` 两项。
- **工具调用意图识别**：`system` message 必须包含工具 JSON 描述和 `Response in INTENT_MODE.`，响应需用正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构。

## 限制和注意事项

- **地域硬性限制**：`qwen-deep-research` 仅支持华北2（北京）地域，跨地域调用将失败；其他模型虽支持多地域，但需确保 API Key 与所选地域匹配。
- **SDK 兼容性差异**：
  - `qwen-deep-research` **仅支持 Python DashScope SDK**，Java SDK 和 OpenAI 接口均不支持（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）；
  - `tongyi-intent-detect-v3` 的 `understanding` 子命令在 dashscope CLI 中暂不支持，需用 Python SDK（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **参数冲突与过时说明**：
  > **注意**：文档 4（Qwen-OCR）中 `min_pixels` 默认值描述为“3072（即 `3×32×32`）”，而文档 5（GUI-Plus）中同参数默认值写为“3136”。经核对，`3136 = 4×28×28`，属于旧版 OCR 模型（如 `qwen-vl-ocr`）的默认值；`qwen3.5-ocr` 等新版模型应以文档 4 的 `3072` 为准。开发者需根据实际选用的模型版本选择对应阈值。
- **成本与限流**：`farui-plus` 的计费单位为“每百万 Token”，具体价格见其文档表格；所有模型均受统一限流策略约束，详情请参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。
- **安全实践**：强烈建议将 `DASHSCOPE_API_KEY` 配置为环境变量，避免硬编码或日志泄露（见 [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)）。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


