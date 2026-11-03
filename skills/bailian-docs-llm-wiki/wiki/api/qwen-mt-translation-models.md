# qwen mt translation models

Qwen-MT 系列是百炼平台提供的[多模态](../concepts/multi-modal.md)翻译模型族，覆盖文本、图片及混合模态输入的高质量翻译能力。模型统一基于 Qwen 大语言模型底座，针对翻译任务进行专项优化，支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生 API。所有模型均需通过百炼控制台开通对应服务后调用。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译模型，支持中英等 100+ 语种互译，适用于 API 批量翻译、实时对话翻译等场景；详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。  
- **Qwen-MT-Image**：图片翻译模型，可识别图中文字并保持原始排版结构（如表格、多栏、图文混排），输出带坐标信息的翻译结果；该能力在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中有简要说明，完整参数见其关联文档。  
- **Qwen-MT-Uni**：全模态翻译模型，支持文本、PDF/DOCX 文档、JPG/PNG 图片、MP3/WAV 音频等多种输入格式，自动识别内容类型并执行端到端翻译；其设计目标与能力边界在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中首次明确列出。

## 关键参数

- `source_language` / `target_language`：必填，ISO 639-1 代码（如 `"zh"`, `"en"`），不支持自动检测（Qwen-MT-Uni 的 `auto` 检测仅限于输入模态类型，非语种）。  
- `input_type`：对 Qwen-MT-Uni 必填，取值为 `"text"` / `"image"` / `"document"` / `"audio"`；Qwen-MT 和 Qwen-MT-Image 不接受此参数。  
- `preserve_layout`：仅 Qwen-MT-Image 和 Qwen-MT-Uni（当 `input_type="image"`）支持，布尔值，默认 `true`。  
- `response_format`：支持 `"json"`（含原文位置、置信度等元信息）和 `"text"`（纯翻译文本），默认 `"text"`。

## 使用方式

- 所有模型均通过 `/v1/services/aigc/mt` 接口调用（DashScope 协议），或使用 OpenAI 兼容 endpoint `/v1/chat/completions`（仅 Qwen-MT 支持，需设置 `model="qwen-mt"`）。  
- 图片与文档需以 base64 编码或 OSS URL 形式传入 `input` 字段；音频需为 PCM 或标准编码格式，且时长 ≤ 300 秒。  
- 认证方式统一使用 `Authorization: Bearer <api_key>`，API Key 需在百炼控制台「模型服务」中开通对应模型权限后获取。

## 限制和注意事项

- Qwen-MT-Uni 当前不支持视频文件输入（尽管 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中“全模态”描述易引发误解，实际未开放 video 解析能力）。  
- > **注意**：Qwen-MT-Image 的 `preserve_layout=true` 在处理复杂 PDF 表格时可能丢失部分边框线信息，建议结合 OCR 后处理校验；该行为与早期 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中“精准还原排版”的表述存在实践偏差。  
- 单次请求最大 token 数：Qwen-MT 为 8192，Qwen-MT-Image 为 2048（受限于图像编码器），Qwen-MT-Uni 视输入模态动态调整（文档类上限 4096 tokens，音频按 16kHz 采样率折算约 120 秒）。  
- 所有模型暂不支持流式响应（`stream=true` 参数将被忽略）。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


