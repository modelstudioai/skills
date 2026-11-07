# [more](more.md) models

百炼平台提供一系列面向特定任务优化的专用模型，覆盖意图理解、OCR图文识别、GUI界面交互、深度研究等场景。这些模型在对应领域具备更强的精度、速度或结构化输出能力，开发者可根据业务需求直接调用，无需自行微调基础大模型。

## 支持的模型/功能

当前支持的专用模型包括：

- **意图理解模型**：`tongyi-intent-detect-v3`，支持毫秒级意图识别与[函数调用](../concepts/function-calling.md)生成，适用于对话路由、智能助手等场景。详见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **OCR模型**：`qwen3.5-ocr`、`qwen-vl-ocr-2025-11-20` 等，专为高精度文本提取与结构化信息抽取设计，支持图像像素自适应缩放与多格式 Prompt 控制。详见 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI交互模型**：`gui-plus-2026-02-26`，支持基于截图的桌面自动化操作（如点击、输入、等待），需配合 `computer_use` 工具调用。详见 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。
- **深度研究模型**：`qwen-deep-research`，支持两阶段研究流程（反问确认 → 深度分析），自动执行网络搜索、信息整合与报告生成，仅限华北2（北京）地域使用。详见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。

> **注意**：`qwen-deep-research` 明确声明“仅支持华北2（北京）地域”，而文档1和文档2中提及的 OCR 模型在新加坡、美国（弗吉尼亚）等地域均有明确 endpoint 支持，但文档3（GUI-Plus）未说明地域限制，仅给出北京地域示例。实际部署时请以控制台可用地域为准，避免跨地域调用失败。

## 关键参数

各模型共性参数（如 `model`, `messages`, `stream`, `max_tokens`, `temperature`, `top_p`）遵循 [OpenAI 兼容接口](../concepts/openai-compatibility.md)规范，但部分参数为百炼特有或行为存在差异：

- `min_pixels` / `max_pixels`：OCR 与 GUI-Plus 模型均支持，用于控制图像输入分辨率。但默认值不同：
  - `qwen3.5-ocr`：`min_pixels=3072`（`3×32×32`），`max_pixels=8388608`（`8192×32×32`）；
  - `gui-plus`：`min_pixels=3136`（`4×28×28`），`max_pixels` 默认 `1003520`，且受 `vl_high_resolution_images` 开关影响。
- `vl_high_resolution_images`：GUI-Plus 特有布尔参数，启用后忽略 `max_pixels`，固定上限 `12845056` 像素。
- `output_format`：`qwen-deep-research` 特有参数，取值 `model_detailed_report`（默认，约6000 Token）或 `model_summary_report`（约1500–2000 Token）。
- `enable_thinking`：GUI-Plus 混合思考模型（如 `gui-plus-2026-02-26`）特有，启用后返回 `reasoning_content` 字段。
- `extra_body`：非标准参数（如 `top_k`, `enable_thinking`, `vl_high_resolution_images`）必须通过 Python SDK 的 `extra_body` 字典传入，HTTP/curl 调用则作为顶层字段。

## 使用方式

### 基础前提
所有模型均要求：
- 已获取并配置有效的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- 业务空间 ID（`{WorkspaceId}`）已知，并用于构造专属域名；
- 推荐迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更优性能与稳定性 —— 此建议在 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)、[Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 和 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中三处一致强调。

### 调用方式差异
- **OpenAI 兼容 SDK**：适用于 `tongyi-intent-detect-v3`、`qwen3.5-ocr`、`gui-plus-2026-02-26`，需设置 `base_url` 为对应地域的专属域名。
- **DashScope SDK**：`qwen-deep-research` **仅支持 DashScope SDK**（文档4明确说明“暂不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatibility.md)”），且需手动设置 `dashscope.base_http_api_url`。
- **HTTP/curl**：所有模型均支持，但需注意：
  - `qwen-deep-research` 使用 `/api/v1/services/aigc/text-generation/generation` 路径；
  - 其他模型使用 `/compatible-mode/v1/chat/completions` 路径。

### 输入格式要点
- **意图模型**：System Message 必须显式包含 `Response in INTENT_MODE.`（[函数调用](../concepts/function-calling.md)模式）或 `just reply with the chosen tag.`（纯意图分类模式）。
- **OCR / GUI-Plus**：`messages[0].content` 必须为 `array`，内含 `type: "image_url"` + `image_url.url` 和可选 `type: "text"` 的 Prompt。
- **深度研究模型**：采用两阶段调用：第一阶段传入宽泛主题（user only），第二阶段需拼接 `user → assistant（模型反问）→ user（用户澄清）` 的完整 messages。

## 限制和注意事项

- **地域限制**：`qwen-deep-research` 仅支持华北2（北京）地域；OCR 模型支持北京、新加坡、美国（弗吉尼亚）；意图模型与 GUI-Plus 文档仅列出北京与新加坡，实际可用性需以控制台为准。
- **SDK 限制**：
  - `qwen-deep-research` 不支持 OpenAI SDK；
  - `dashscope CLI` 明确不支持 `understanding` 子命令（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)）；
  - `top_k`, `enable_thinking`, `vl_high_resolution_images` 等非标准参数在 Python SDK 中必须置于 `extra_body`。
- **图像处理**：OCR 与 GUI-Plus 模型对图像尺寸敏感。若 `min_pixels` 或 `max_pixels` 设置不当，可能导致识别失败或精度下降；`qwen3.5-ocr` 与旧版 `qwen-vl-ocr` 的像素/Token 换算比例不同（`32×32` vs `28×28`），需按模型版本校准。
- **流式响应解析**：意图模型返回的 `<tags>...</tags>`、<tool_call>...<tool_call>、`<content>...</content>` 结构需用正则解析（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中 `parse_text` 示例）；`qwen-deep-research` 流式响应含 `phase`、`status` 等阶段字段，需按 `phase`（如 `WebResearch`, `answer`）区分处理逻辑。
- **免费额度**：`tongyi-intent-detect-v3` 提供开通后90天内100万 Token 免费额度（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)），其他模型未在原始文档中提及免费额度。

## 来源文档

- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)
- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)


