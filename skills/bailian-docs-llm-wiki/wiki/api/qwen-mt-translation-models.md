# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。开发者可根据输入类型、延迟要求和文件规模选择最适配的模型。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，适用于高精度、低延迟的文本翻译场景。支持 `translation_options` 参数配置源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）及领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持 55 种语言间任意互译；`qwen-mt-image` 仅支持源或目标语言至少有一方为中文或英文。两者均支持术语干预（`terminologies`）、敏感词过滤（`sensitives`）和图像主体分割（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等多种格式输入，并原格式输出。自动识别模态、路由至最优子模型，实现“一接口通吃”。支持 `fileUrl` 或 `source_texts` 任一输入方式，且必须且只能提供其一。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例被截断（末尾为 `"profe"`），实际应为完整英文描述；而文档 2 和文档 3 明确要求领域提示（`domainHint`）**只支持英文**且建议 ≤200 单词。因此 `qwen-mt-plus` 的 `domains` 字段也应遵循相同约束，该截断属于原文档内容不完整，非功能限制。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 备注 |
|--------|------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 源/目标语言，支持全称（如 `"Chinese"`）、ISO 编码（如 `"zh"`）或 `"auto"`（自动检测） | 全部 | `qwen-mt-image` 要求至少一方为 `zh`/`en`；`qwen-mt-uni` 和 `qwen-mt-image-2.0` 无此限制 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表，格式为 `[{"source": "...", "target": "..."}]`（`qwen-mt-plus`）、`[{"src": "...", "tgt": "..."}]`（`qwen-mt-image`）、`[{"src": "...", "tgt": "..."}]`（`qwen-mt-uni`） | 全部 | `qwen-mt-plus` 使用 `terms`；后两者使用 `terminologies`/`glossary`，字段名不同但语义一致 |
| `tm_list` | `array` | 翻译记忆列表，格式为 `[{"source": "...", "target": "..."}]` | `qwen-mt-plus` 专属 | 仅文本模型支持，用于提升术语与句式一致性 |
| `domainHint` | `string` | 英文领域提示，描述场景、风格、受众等 | `qwen-mt-image`, `qwen-mt-uni` | **必须为英文**，≤200 单词；`qwen-mt-plus` 的 `domains` 字段功能等效但命名不同 |
| `sensitives` | `array<string>` | 敏感词列表，完全匹配时跳过翻译并保留原文 | `qwen-mt-image`, `qwen-mt-uni` | 区分大小写；最多 50 项 |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物/商品/Logo）上的文字翻译 | `qwen-mt-image`, `qwen-mt-uni` | 默认 `false`；旧版 `skipImgSegment` 已弃用，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) |

## 使用方式

- **地域与 Endpoint**：所有模型均支持华北2（北京）、新加坡、美国（弗吉尼亚）地域。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。`{WorkspaceId}` 需在百炼控制台「业务空间详情」中获取。
- **认证**：需已 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并通过环境变量 `DASHSCOPE_API_KEY` 或 SDK 显式传入。
- **调用模式**：
  - **同步调用**：适用于文本、小图、短音频等低延迟场景。`qwen-mt-plus` 使用 `/compatible-mode/v1/chat/completions`；`qwen-mt-image` 和 `qwen-mt-uni` 使用 `/api/v1/services/aigc/.../generation`，无需额外请求头。
  - **[异步调用](../concepts/asynchronous-invocation.md)**：适用于大文档、长音频等耗时场景。`qwen-mt-image` **必须**设置请求头 `X-DashScope-Async: enable`；`qwen-mt-uni` 同理；`qwen-mt-plus` **不支持异步**。
- **SDK 示例（OpenAI 兼容）**：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"  # qwen-mt-plus
  )
  completion = client.chat.completions.create(
      model="qwen-mt-plus",
      messages=[{"role": "user", "content": "你好"}],
      extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}}
  )
  ```

## 限制和注意事项

- **语言支持**：`qwen-mt-plus` 和 `qwen-mt-uni` 支持广泛语种，具体列表请参阅各模型文档；`qwen-mt-image` 的旧版本（非 `-2.0`）存在语种互译限制，务必确认模型版本。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；
  - URL 中**禁止包含中文字符**，否则请求将失败。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms`、`qwen-mt-image` 的 `terminologies`、`qwen-mt-uni` 的 `glossary` 功能等效，但字段名和嵌套结构不同，集成时需按模型分别适配。
- **错误处理**：同步调用失败时响应顶层含 `code`/`message`；[异步调用](../concepts/asynchronous-invocation.md)需先查 `task_status`，再根据 `output.Success` 判断业务成败（`SUCCEEDED` 状态下 `Success=false` 表示业务失败）。错误码详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **计费与用量**：`qwen-mt-uni` 返回详细的 `usage` 统计（含 `input_tokens_details`），按 `input_tokens` 计费；`qwen-mt-plus` 和 `qwen-mt-image` 当前未在响应中返回 token 用量，计费以调用次数或图像数为准。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


