# qwen mt translation models

Qwen-MT 系列是百炼平台提供的多模态翻译模型族，覆盖纯文本、图片及混合模态（文档/音频/图文）的端到端翻译任务。所有模型均通过统一 API 接口调用，支持 OpenAI 兼容格式与 DashScope 原生协议。模型能力基于 Qwen 大语言模型底座优化，专为高保真、低延迟、结构化输出设计。

## 支持的模型与功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语种对，可指定源/目标语言、术语表和风格偏好。详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。
- **Qwen-MT-Image**：图片翻译，自动识别图文区域并保持原始排版（如表格、标题层级、文字方向），输出含坐标信息的结构化 JSON。该能力在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中有基础说明，但详细字段定义请参考 [Qwen-MT-Image API 参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **Qwen-MT-Uni**：全模态翻译，统一处理 PDF/DOCX/PNG/WAV 等输入，自动执行 OCR/ASR/文本理解→翻译→格式重建流水线。其输入约束与输出 schema 在 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是（除 auto-detect 场景） | ISO 639-1 代码，如 `"zh"`、`"en"`；设为 `"auto"` 启用自动检测（仅 Qwen-MT 和 Qwen-MT-Uni 支持） |
| `target_language` | string | 是 | 目标语言 ISO 639-1 代码，如 `"ja"` |
| `preserve_formatting` | boolean | 否 | 默认 `true`；设为 `false` 时禁用排版保留（仅 Qwen-MT-Image 和 Qwen-MT-Uni 生效） |
| `glossary` | object | 否 | 术语表对象，格式为 `{ "terms": [{"source": "...", "target": "..."}] }`；仅 Qwen-MT 支持 |

> **注意**：`preserve_formatting` 在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中被描述为“默认启用”，但实测 Qwen-MT-Uni 的默认行为为 `false`（需显式设为 `true` 才触发排版重建）。请以 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的最新参数说明为准。

## 使用方式

- **OpenAI 兼容模式**（推荐）：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen-mt",
      "messages": [{"role": "user", "content": "Hello, world!"}],
      "source_language": "en",
      "target_language": "zh"
    }'
  ```
- **DashScope 原生模式**：使用 `/api/v1/services/aigc/text-generation/generation` 路径，`model` 字段传 `"qwen-mt"`、`"qwen-mt-image"` 或 `"qwen-mt-uni"`，请求体需符合各模型对应 schema（参见 [Qwen-MT API 参考](../../raw/model-api-reference/more-models/qwen-mt-api.md)）。

## 限制和注意事项

- 输入长度限制：Qwen-MT 单次请求 ≤ 8192 tokens；Qwen-MT-Image 图片分辨率 ≤ 4096×4096 px；Qwen-MT-Uni 文档页数 ≤ 50 页（PDF/DOCX）、音频时长 ≤ 10 分钟。
- [异步任务](../concepts/asynchronous-task.md)：Qwen-MT-Uni 对大文件或长音频默认返回 `task_id`，需轮询 `/api/v1/tasks/{id}` 获取结果；同步模式仅适用于小尺寸输入（详见 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）。
- 计费单位：Qwen-MT 按 token 计费；Qwen-MT-Image 和 Qwen-MT-Uni 按“请求次数 + 输出字符数”组合计费，具体规则见控制台定价页。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


