# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用大模型，涵盖意图理解、法律推理、深度研究、OCR文字识别和GUI界面交互等方向。这些模型在通用大模型基础上进行了领域精调与能力增强，支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，适用于高精度、低延迟、强专业性的生产级任务。

## 支持的模型/功能

当前 `more models` 类别下已开放以下专用模型：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话系统中的路由决策与工具调用编排。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **法律行业模型**：`farui-plus`，专为法律咨询、文书生成、案情分析与合同审查优化，融合RAG与司法小模型能力。
- **深度研究模型**：`qwen-deep-research`，支持两阶段交互式研究（反问确认 + 深度分析），自动执行网络检索、信息整合与结构化报告生成；**仅限华北2（北京）地域使用**，且**仅支持 Python DashScope SDK**，不支持 Java SDK 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **OCR文字识别模型**：包括 `qwen3.5-ocr`、`qwen-vl-ocr-*` 系列，支持多分辨率图像输入与结构化文本提取，适用于票据、文档、合同等场景。
- **GUI界面交互模型**：`gui-plus` 系列（如 `gui-plus-2026-02-26`），专为桌面自动化设计，支持基于截图的鼠标/键盘操作指令生成，需配合 `computer_use` 工具函数使用。

> **注意**：文档 4 与文档 5 均声明 `min_pixels` 默认值为 3136，但文档 4 明确区分了不同模型版本（如 `qwen3.5-ocr` 对应 `3072`），而文档 5 未作版本区分。实际调用时请以具体模型文档为准，优先参考 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中按模型版本划分的像素阈值说明。

## 关键参数

| 参数 | 说明 | 适用模型 | 备注 |
|------|------|----------|------|
| `model` | 模型标识符 | 全部 | 必填，如 `"tongyi-intent-detect-v3"`、`"farui-plus"` |
| `messages` | 对话消息数组 | 全部 | `user` 消息必含 `content`；视觉模型（OCR、GUI-Plus）支持 `image_url` 类型内容；`qwen-deep-research` 要求两步调用（先反问、再深入） |
| `output_format` | 报告格式 | `qwen-deep-research` | 可选 `model_detailed_report`（默认，~6000 [Token](../concepts/token.md)）或 `model_summary_report`（~1500–2000 [Token](../concepts/token.md)） |
| `vl_high_resolution_images` | 启用高分辨率图像处理 | `gui-plus` 系列 | 非 OpenAI 标准参数，需通过 `extra_body` 传入；设为 `true` 时 `max_pixels` 失效，上限固定为 `12845056` |
| `min_pixels` / `max_pixels` | 图像像素阈值 | OCR、GUI-Plus | 控制图像缩放行为；不同模型版本对应不同像素/[Token](../concepts/token.md) 换算关系（如 `32×32` 或 `28×28`） |
| `enable_thinking` | 开启混合思考模式 | `gui-plus-2026-02-26` | 非 OpenAI 标准参数，需通过 `extra_body` 传入；启用后返回 `reasoning_content` 字段 |

## 使用方式

### 基础前提
- 已在百炼控制台开通对应模型服务并获取 API Key；
- 推荐将 `DASHSCOPE_API_KEY` 配置为环境变量；
- 安装对应 SDK：Python 用户安装 `dashscope` 或 `openai`（>=1.0），Java 用户安装 `dashscope-java-sdk`（>=2.12.0）；
- **必须使用业务空间专属域名**：华北2（北京）→ `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；新加坡 → `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。旧域名（`dashscope.aliyuncs.com` 等）虽仍可用，但性能与稳定性较低 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。

### 调用示例（核心差异）
- **意图识别**：需在 `system` message 中显式声明 `Response in INTENT_MODE.` 并注入工具定义（JSON Schema）或意图字典；
- **法律模型（farui-plus）**：支持单轮、多轮及[流式输出](../concepts/streaming-output.md)，无特殊 system [prompt](../guides/prompt.md) 要求；
- **深度研究（qwen-deep-research）**：必须分两步调用——第一步传入初始主题获取澄清问题，第二步将该问题作为 `assistant` message 回传，并附上用户补充指令；
- **OCR 与 GUI-Plus**：`messages[0].content` 为 `array`，包含 `{"type": "image_url", "image_url": {"url": "..."} }` 和可选 `{"type": "text", "text": "..."}` 提示词。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域，其他地域调用将失败；
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅限 Python DashScope SDK；
- **流式响应解析**：`qwen-deep-research` 的流式响应含多阶段状态（`ResearchPlanning`、`WebResearch`、`answer`），需根据 `message.phase` 和 `message.status` 判断当前阶段，不可简单拼接 `content`；
- **OCR 图像预处理**：`min_pixels`/`max_pixels` 设置不当会导致图像失真或 Token 消耗激增；建议对文档类图像优先使用 `qwen3.5-ocr`（`32×32` 换算）并设 `min_pixels=3072`；
- **GUI-Plus 工具调用**：必须严格遵循 `Action` + `<tool_call>...</tool_call>` 两段式响应格式，且 `<tool_call>` 内 JSON 必须是合法对象，否则下游自动化流程将中断；
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度，其余模型暂未说明免费策略。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [通义法睿大语言模型](../../raw/model-api-reference/more-models/tongyi-farui-api.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


