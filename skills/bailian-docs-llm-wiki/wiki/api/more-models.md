# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖法律、意图理解、深度研究、OCR识别与GUI自动化等方向。这些模型在通用基座上进行了领域精调或架构增强，支持结构化输入/输出、多阶段推理、图文混合处理等能力，适用于专业级AI应用开发。

## 支持的模型/功能

| 模型名称 | 类型 | 核心能力 | 地域支持 | 文档参考 |
|----------|------|-----------|-----------|-----------|
| `farui-plus` | 法律大模型 | 法律咨询、文书生成、案情分析、合同审查、RAG检索增强 | 华北2（北京）、新加坡、中国香港 | [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md) |
| `tongyi-intent-detect-v3` | 意图理解模型 | 百毫秒级意图识别、工具调用决策、标签分类 | 华北2（北京）、新加坡、中国香港 | [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) |
| `qwen-deep-research` | 深度研究模型 | 两阶段交互式研究（反问确认 + 网络搜索 + 报告生成） | **仅华北2（北京）** | [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) |
| `qwen3.5-ocr`, `qwen-vl-ocr-*` | OCR视觉模型 | 多格式图像文本提取、结构化信息抽取（如车票、合同）、高分辨率适配 | 华北2（北京）、新加坡、美国（弗吉尼亚） | [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) |
| `gui-plus-*` | GUI自动化模型 | 基于截图的桌面操作（点击、输入、滚动、等待）、工具[函数调用](../concepts/function-calling.md)、混合思考模式 | 华北2（北京）、新加坡 | [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) |

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而其他模型（如 `qwen-vl-ocr` 和 `gui-plus`）在文档中均列出多地域支持。若跨地域调用 `qwen-deep-research` 将失败，需严格遵循该限制。

## 关键参数

所有模型均支持以下通用参数（部分为 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)标准参数）：

- `model`: 必填，模型标识符（如 `"farui-plus"`）
- `messages`: 必填，对话消息数组，支持 `system`/`user`/`assistant` 角色及图文混合内容（`image_url` + `text`）
- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)（默认 `false`）
- `max_tokens`: 输出长度上限（各模型取值范围不同，详见下文）
- `temperature` / `top_p`: 控制生成多样性（推荐保持默认值 `0.01`，避免同时设置两者）
- `seed`: 随机种子，用于结果可复现

**模型特有关键参数**：
- `qwen-deep-research`: 支持 `output_format`（`model_detailed_report` 或 `model_summary_report`），影响报告篇幅与粒度。
- `qwen-vl-ocr-*` 和 `gui-plus-*`: 支持 `min_pixels` / `max_pixels` 控制图像分辨率缩放策略；`gui-plus-*` 还支持 `vl_high_resolution_images`（启用后忽略 `max_pixels`，固定上限为 `12845056` 像素）。
- `tongyi-intent-detect-v3`: 要求 `system` 消息中显式包含 `Response in INTENT_MODE.`（工具调用）或 `just reply with the chosen tag.`（纯意图分类）指令，否则行为未定义。

## 使用方式

### 基础调用流程
1. **准备环境**：安装最新版 DashScope SDK 或 OpenAI SDK，[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`。
2. **选择域名**：强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 —— 此要求在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 和 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中被多次强调。
3. **构造请求**：按模型要求组织 `messages`（例如 `farui-plus` 需 `system` + `user`；`qwen-deep-research` 需两轮调用；`gui-plus` 需 `system` 工具定义 + `user` 图文）。
4. **发起调用**：通过 `dashscope.Generation.call()`（DashScope）或 `client.chat.completions.create()`（OpenAI 兼容）发送请求。

### 示例模式
- **单轮对话**（`farui-plus`）：直接传入 `system` + `user` 消息，适合法律咨询、文书生成。
- **多轮对话**（`farui-plus`）：将上一轮 `assistant` 回复追加至 `messages`，再发新 `user` 消息。
- **[流式输出](../concepts/streaming-output.md)**（所有模型）：设置 `stream=True`，逐块读取响应（Python SDK 中 `incremental_output=True` 可优化拼接）。
- **两阶段研究**（`qwen-deep-research`）：第一步获取模型反问，第二步将反问+用户澄清作为上下文再次调用。
- **图文混合**（`qwen-vl-ocr-*`, `gui-plus-*`）：`messages[0].content` 为数组，含 `{"type":"image_url","image_url":{"url":"..."}}` 和 `{"type":"text","text":"..."}` 对象。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，调用前必须确认 `base_http_api_url` 或 `base_url` 配置正确；其他模型虽支持多地域，但需确保所用 `WorkspaceId` 与地域匹配。
- **SDK支持差异**：
  - `qwen-deep-research` **仅支持 Python SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）。
  - `tongyi-intent-detect-v3` 的 `dashscope CLI` 不支持 `understanding` 子命令，需用 Python SDK（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）。
- **输入格式强约束**：
  - `tongyi-intent-detect-v3` 的 `system` 消息必须包含明确的响应模式指令（`INTENT_MODE` 或 `just reply with the chosen tag.`），否则无法触发对应能力。
  - `qwen-vl-ocr-*` 和 `gui-plus-*` 的 `image_url` 输入必须为公网可访问 URL 或 Base64 Data URL；本地文件需先上传（参见相关文档链接）。
- **成本与限流**：各模型有独立计费（如 `farui-plus` 输入 20元/百万 Token），且受全局限流策略约束，请查阅 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档。
- **输出解析**：`tongyi-intent-detect-v3` 的工具调用响应需用正则解析 `<tags>`/<tool_call>/`<content>` 结构；`qwen-deep-research` 的流式响应含 `phase` 字段（如 `ResearchPlanning`, `WebResearch`），需按阶段处理。

## 来源文档

- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


