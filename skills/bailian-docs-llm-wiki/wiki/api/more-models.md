# [more](more.md) models

百炼平台提供一系列面向特定任务的专用模型，包括深度研究（Qwen-Deep-Research）、意图理解（tongyi-intent-detect-v3）、OCR识别（Qwen-OCR系列）和界面交互（GUI-Plus）。这些模型通过 DashScope 或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持多地域部署与精细化参数控制，适用于研究分析、智能路由、文档解析与自动化操作等场景。所有模型均需配置业务空间专属域名及对应 API Key。

## 支持的模型/功能

- **Qwen-Deep-Research**：两阶段深度研究模型，支持反问确认 → 网络搜索 → 报告生成全流程，输出含参考文献与研究过程元数据。仅限华北2（北京）地域，且**仅支持 DashScope Python SDK**，不支持 Java SDK 与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **tongyi-intent-detect-v3**：毫秒级意图识别模型，支持两种模式：① `INTENT_MODE` 下同时输出意图标签与[函数调用](../concepts/function-calling.md) JSON；② 纯意图分类模式（返回单个 tag）。支持多地域，推荐使用业务空间专属域名 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-OCR 系列**（如 `qwen3.5-ocr`, `qwen-vl-ocr`）：多模态 OCR 模型，支持图像文本提取与结构化信息抽取。支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope API，覆盖华北2（北京）、新加坡、美国（弗吉尼亚）三地 [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus 系列**（如 `gui-plus-2026-02-26`）：专用于 GUI 自动化操作的视觉语言模型，支持截图理解、工具调用与混合思考（`enable_thinking`），需传入屏幕截图与系统指令 [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：文档 2 和文档 3 均提及“建议迁移至业务空间专属域名”，但文档 2 明确列出新加坡、中国香港两地，而文档 3 仅列出华北2（北京）、新加坡两地，**中国香港地域未在 OCR 文档中确认支持**，实际调用前请以控制台业务空间详情页为准。

## 关键参数

| 参数 | 适用模型 | 说明 | 默认值 |
|------|----------|------|--------|
| `output_format` | Qwen-Deep-Research | 控制报告格式：`model_detailed_report`（约6000 [Token](../concepts/token.md)）或 `model_summary_report`（1500–2000 [Token](../concepts/token.md)） | `model_detailed_report` |
| `min_pixels` / `max_pixels` | Qwen-OCR、GUI-Plus | 图像预处理像素阈值，单位为像素；不同模型每 [Token](../concepts/token.md) 对应像素不同（如 `qwen3.5-ocr`: 32×32） | `qwen3.5-ocr`: 3072 / 8388608；GUI-Plus: 3136 / 1003520（`vl_high_resolution_images=false`） |
| `vl_high_resolution_images` | GUI-Plus | 启用高分辨率图像处理（固定上限 12845056 像素），设为 `true` 时忽略 `max_pixels` | `false` |
| `enable_thinking` | GUI-Plus（仅 `gui-plus-2026-02-26`） | 开启思考模式，输出将包含 `reasoning_content` 字段 | `false` |
| `temperature` / `top_p` | Qwen-OCR、GUI-Plus | 控制生成多样性，二者互斥，建议只设其一 | `qwen3.5-ocr`: 0.01 / 0.001；GUI-Plus: 0.01 / 0.01 |

## 使用方式

- **地域与域名**：所有模型均推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其中 `{WorkspaceId}` 需替换为控制台获取的真实 ID。华北2（北京）为 Qwen-Deep-Research 唯一支持地域。
- **SDK 选择**：
  - Qwen-Deep-Research：**必须使用 DashScope Python SDK**，且需显式设置 `dashscope.base_http_api_url`（见 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)）；
  - 其他模型：支持 DashScope SDK 与 OpenAI SDK（兼容 `openai>=1.0`），OpenAI SDK 需配置 `base_url` 为对应地域的 `/compatible-mode/v1` 端点。
- **消息结构**：
  - Qwen-Deep-Research：`messages` 必须按两阶段构造（初始 user → assistant 回复 → 新 user 澄清），且 `role` 严格为 `user`/`assistant`；
  - Qwen-OCR / GUI-Plus：`messages[0].content` 为 `array`，支持 `text` + `image_url` 混合输入；
  - tongyi-intent-detect-v3：**必须设置 system message**，分别指定 `Response in INTENT_MODE.` 或 `just reply with the chosen tag.`。
- **流式响应**：Qwen-Deep-Research、Qwen-OCR、GUI-Plus 均支持 `stream=true`；意图模型暂未明确说明流式支持，建议非流式调用。

## 限制和注意事项

- **地域限制**：Qwen-Deep-Research 仅支持华北2（北京）地域，其他模型虽支持多地域，但部分功能（如 `vl_high_resolution_images`）可能因地域而异。
- **SDK 限制**：Qwen-Deep-Research 不支持 Java SDK 与 OpenAI 兼容接口，此限制在 [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中明确强调。
- **图像参数差异**：Qwen-OCR 与 GUI-Plus 的 `min_pixels`/`max_pixels` 默认值与取值范围不同，且 GUI-Plus 的 `max_pixels` 行为受 `vl_high_resolution_images` 控制，不可直接复用 OCR 参数配置。
- **意图模型输出解析**：tongyi-intent-detect-v3 在 `INTENT_MODE` 下返回 `<tags>...</tags><tool_call>...</tool_call><content>...</content>` 格式，**必须使用正则解析**（见 [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中的 `parse_text` 示例），不可直接 JSON 解析。
- **Token 成本与配额**：tongyi-intent-detect-v3 提供 90 天内 100 万 Token 免费额度；Qwen-Deep-Research 与 GUI-Plus 无明确免费额度说明，需关注控制台计费项。

## 来源文档

- [Qwen-Deep-Research API 参考](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)
- [意图理解能力](../../raw/model-api-reference/more-models/intent-detect-capability.md)
- [Qwen-OCR API参考](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)


