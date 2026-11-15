# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，包括深度研究、意图理解、OCR 文字识别和 GUI 自动化等。这些模型通过 DashScope 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，具备明确的输入约束、阶段化响应机制和精细化参数控制能力，适用于需要高精度、强可控性或领域专精能力的生产场景。

## 支持的模型/功能

当前支持以下四类专用模型：

- **Qwen-Deep-Research**：两阶段深度研究模型，支持自动反问澄清、网络搜索、研究报告生成（详版/摘要版），仅限华北2（北京）地域调用，且**仅支持 DashScope Python SDK**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **tongyi-intent-detect-v3**：毫秒级意图识别模型，支持两种模式：① 同时输出意图标签与[函数调用](../concepts/function-calling.md) JSON（需在 system prompt 中声明 `Response in INTENT_MODE.`）；② 仅输出预定义意图标签（需在 system prompt 中指定 tag list 并要求“just reply with the chosen tag”）[意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-OCR 系列（如 `qwen3.5-ocr`, `qwen-vl-ocr`）**：多分辨率图像文字提取模型，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)与 DashScope API，可传入图像 URL 或 Base64 Data URL，并支持 `min_pixels`/`max_pixels` 控制图像缩放行为 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus（如 `gui-plus-2026-02-26`）**：界面交互专用模型，支持结合截图与工具调用（如 `computer_use`）完成 GUI 自动化操作，需显式传入系统指令（含 `<tools>` 定义）及截图内容 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 和文档 3 均提及“建议迁移至业务空间专属域名”，但文档 2 明确列出新加坡、中国香港地域，而文档 3 仅列出华北2（北京）、新加坡地域，未提中国香港。实际部署时请以控制台中业务空间详情页显示的可用地域为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|--------|-----------|------|---------|
| `output_format` | `qwen-deep-research` | 指定报告格式：`model_detailed_report`（约6000 Token）或 `model_summary_report`（约1500–2000 Token） | `model_detailed_report` |
| `vl_high_resolution_images` | `gui-plus-*` | 是否启用高分辨率图像处理（固定上限 12845056 像素），设为 `true` 时忽略 `max_pixels` | `false` |
| `min_pixels` / `max_pixels` | `qwen3.5-ocr`, `gui-plus-*` | 图像像素阈值控制缩放行为；不同模型每 Token 对应像素不同（如 `qwen3.5-ocr`: 32×32） | `qwen3.5-ocr`: 3072 / 8388608；`gui-plus-*`: 3136 / 1003520（当 `vl_high_resolution_images=false`） |
| `enable_thinking` | `gui-plus-2026-02-26`（仅混合思考模型） | 开启后返回 `reasoning_content` 字段 | `false` |
| `temperature` / `top_p` | 所有模型（除 `qwen-deep-research` 外） | 控制生成多样性；二者互斥，建议只设其一 | `qwen3.5-ocr`: 0.01 / 0.001；`gui-plus-*`: 0.01 / 0.01；`tongyi-intent-detect-v3`: 未显式声明，默认由服务端控制 |

## 使用方式

1. **地域与域名配置**：所有模型均需使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），不可使用旧版 `dashscope.aliyuncs.com` 域名；`{WorkspaceId}` 需从控制台业务空间详情页获取。
2. **认证与 SDK**：
   - 必须已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置；
   - `qwen-deep-research` **仅支持 DashScope Python SDK**，其他模型支持 OpenAI SDK（兼容模式）或 DashScope SDK。
3. **请求构造**：
   - `qwen-deep-research`：必须分两步调用（反问确认 → 深入研究），第二步需将第一步的 `assistant` 消息作为历史传入；
   - `tongyi-intent-detect-v3`：system message 决定输出模式（`INTENT_MODE` 或纯 tag）；
   - `qwen3.5-ocr` / `gui-plus-*`：`messages.content` 为数组，支持 `text` + `image_url` 混合输入；`image_url` 必须含 `url` 字段，可选配 `min_pixels`/`max_pixels`。
4. **流式响应处理**：`qwen-deep-research` 的响应含 `phase`（如 `answer`, `WebResearch`）和 `status`（如 `typing`, `streamingQueries`）字段，需按阶段解析；OCR 与 GUI-Plus 的流式响应遵循 OpenAI 标准 chunk 格式。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 严格限定于华北2（北京）地域，其他地域调用将失败；`tongyi-intent-detect-v3`、`qwen3.5-ocr`、`gui-plus-*` 支持华北2（北京）、新加坡、美国（弗吉尼亚）等多地，但需匹配对应 `base_url`。
- **SDK 限制**：`qwen-deep-research` 不支持 Java SDK 与 OpenAI 兼容接口，此限制在 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中明确强调。
- **图像参数差异**：`qwen3.5-ocr` 与 `gui-plus-*` 的 `min_pixels`/`max_pixels` 默认值不同，且 `gui-plus-*` 的 `max_pixels` 行为受 `vl_high_resolution_images` 控制，而 `qwen3.5-ocr` 无此开关 —— 开发者需严格按模型文档配置，不可复用参数值。
- **输出解析复杂度**：`qwen-deep-research` 响应结构嵌套深（含 `deep_research.references`, `webSites`, `research` 等），`tongyi-intent-detect-v3` 的 `INTENT_MODE` 输出需正则解析 `<tags>`/<tool_call>/`<content>` 三段式结构，均需客户端实现健壮解析逻辑。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度，其他模型未在原始文档中声明免费额度政策。

## 来源文档

- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


