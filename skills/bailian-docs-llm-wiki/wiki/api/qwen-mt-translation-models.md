# qwen mt translation models

Qwen MT 系列是百炼平台提供的多模态翻译模型家族，专为高精度、低延迟的跨语言内容转换设计，覆盖纯文本、图像及混合模态输入场景。模型基于 Qwen 大语言模型底座优化，支持端到端语义对齐与格式保真。所有模型均通过统一 API 网关接入，兼容 OpenAI 格式与 DashScope 原生协议。

## 支持的模型与功能

- **`qwen-mt`**：纯文本翻译模型，支持 100+ 语言对，适用于 API 调用与批量文本处理。详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。
- **`qwen-mt-image`**：图像翻译模型，可识别并翻译图片中的文字，同时保留原始排版结构（如表格、段落缩进、图文位置关系）。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本、PDF/DOCX 文档、JPG/PNG 图片、MP3/WAV 音频等多类型输入；自动执行 OCR、ASR、翻译与格式重建全流程。

> **注意**：`qwen-mt-uni` 当前不支持视频文件直接输入，需先提取帧或音频轨道——该限制未在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中明确说明，但已在 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的“输入格式”章节中更新。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是 | 源语言代码（如 `zh`, `en`, `ja`），`auto` 表示自动检测（仅 `qwen-mt` 和 `qwen-mt-uni` 支持） |
| `target_language` | string | 是 | 目标语言代码（如 `en`, `fr`, `ko`） |
| `input_type` | string | 否 | 输入类型标识：`text` / `image` / `document` / `audio`；`qwen-mt` 仅接受 `text`，其余模型默认根据 payload 自动推断 |
| `preserve_format` | boolean | 否 | 默认 `true`；控制是否保留原文格式（对 `qwen-mt-image` 和 `qwen-mt-uni` 生效） |

详细参数定义请参考 [Qwen-MT API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。

## 使用方式

- **文本翻译（`qwen-mt`）**：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-to-text/text-generation \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen-mt",
          "input": {"text": "你好，世界！"},
          "parameters": {"source_language": "zh", "target_language": "en"}
        }'
  ```

- **图片翻译（`qwen-mt-image`）**：  
  `input` 字段需传入 Base64 编码的图片数据或 OSS URL，并显式指定 `"input_type": "image"`。

- **全模态翻译（`qwen-mt-uni`）**：  
  支持 multipart/form-data 提交文件，或 JSON 中以 `file_url` 指向公网可访问资源。具体调用方式见 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 8192 tokens；图片分辨率 ≤ 4096×4096 像素；文档页数 ≤ 50 页；音频时长 ≤ 30 分钟。
- `qwen-mt` 不支持图像或音频输入，若误传将返回 `400 Bad Request`；此行为与 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中“支持多模态”的笼统描述存在偏差，实际应以各子模型文档为准。
- 所有模型均不支持实时流式响应（`stream: true` 无效），响应为完整 JSON 对象一次性返回。
- 非 UTF-8 编码的文本输入可能导致乱码，建议客户端预处理为 UTF-8。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


