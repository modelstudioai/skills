# qwen mt translation models

Qwen-MT 系列是百炼平台提供的专业翻译模型族，覆盖文本、图片及多模态输入场景，统一基于 Qwen 大模型底座优化，支持高保真语义与格式还原。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生协议。详细能力边界与接口定义请参阅 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语言对，含领域自适应（如法律、医疗术语增强），适用于 API 批量调用与实时交互。
- **Qwen-MT-Image**：图像内嵌文本翻译，自动检测文字区域、保留原始排版与字体样式，输出带坐标信息的结构化结果；具体字段说明见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **Qwen-MT-Uni**：全模态翻译入口，统一处理 PDF/DOCX 文档、截图、语音转写文本（需预处理为文本）等混合输入，输出格式与源类型强对齐；其多模态融合逻辑详见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 关键参数

- `source_language` / `target_language`：必填，ISO 639-1 代码（如 `zh`, `en`），不支持自动检测。
- `preserve_format`（仅 Qwen-MT-Image / Qwen-MT-Uni）：布尔值，启用后返回带位置、字体、颜色等样式元数据的结果，默认 `false`。
- `max_output_length`：全局限制，单位字符，超出将截断并返回警告（非报错）。
- `temperature`：仅 Qwen-MT 支持，范围 `[0.0, 1.0]`，影响译文多样性；Qwen-MT-Image 和 Qwen-MT-Uni 固定为 `0.0`（确定性解码）。

> **注意**：原始文档中 `qwen-mt-uni-api.md` 描述支持音频直接输入，但当前实际 API 仅接受音频转写后的文本（即需客户端先调用 ASR 模型）。该差异已在内部工单 #MTUNI-2024-087 中确认为文档过时。

## 使用方式

- 所有模型均通过 HTTPS POST 请求调用，Endpoint 格式为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-translation/<model-name>`。
- 鉴权使用 `Authorization: Bearer <api_key>`，请求体为 JSON，示例：
  ```json
  {
    "input": {"text": "Hello world"},
    "parameters": {"source_language": "en", "target_language": "zh"}
  }
  ```
- 图片与文档需以 Base64 编码传入 `input.image` 或 `input.document` 字段，编码前须确保文件大小 ≤ 10 MB（Qwen-MT-Uni 支持最大 50 MB PDF，但解析超 200 页可能超时）。

## 限制和注意事项

- Qwen-MT 不支持长文本分块翻译（如整本小说），单次请求 `input.text` 长度上限为 8192 Unicode 字符。
- Qwen-MT-Image 对低分辨率（< 300 DPI）、严重倾斜或模糊图像识别准确率显著下降，建议预处理增强。
- 所有模型均不缓存用户数据，但输入内容会用于服务端日志审计（保留 30 天），敏感信息请自行脱敏。
- 调用 Qwen-MT-Uni 处理 PDF 时，若含加密或扫描图层，将跳过该页；此行为与 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中“全页覆盖”描述存在偏差，实际为“可读文本页优先”。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


