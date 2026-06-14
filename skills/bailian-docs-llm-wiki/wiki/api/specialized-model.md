# specialized model

百炼平台提供多种专用模型（specialized model），面向特定垂直场景进行了深度优化。目前包括用于图像文字提取的 Qwen-OCR 模型和用于 GUI 界面交互自动化的 GUI-Plus 模型。这些模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope API 调用，开发者可以快速集成到自己的应用中。

## 支持的模型

### Qwen-OCR

Qwen-OCR（模型名：`qwen-vl-ocr-latest`）是基于通义千问视觉语言模型的 OCR 专用模型，能够从图像中精准提取文字内容。适用于票据识别、文档数字化、表单提取等场景。详细参数与调用方式参见 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)。

**核心特点：**

- 支持自定义 Prompt，可指定提取格式（如 JSON）和提取字段
- 若不传入 Prompt，使用默认提示词：`Please output only the text content from the image without any additional descriptions or formatting.`
- 支持通过 `min_pixels` 和 `max_pixels` 控制输入图像的分辨率阈值

### GUI-Plus

GUI-Plus（模型名：`gui-plus-2026-02-26`）是界面交互专用模型，能够理解桌面截图并生成对应的鼠标/键盘操作指令。适用于 RPA（机器人流程自动化）、UI 自动化测试、智能助手等场景。详细参数与调用方式参见 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)。

**核心特点：**

- 基于 computer_use 工具函数范式，支持 `left_click`、`type`、`key`、`scroll`、`wait` 等多种操作
- 屏幕分辨率默认为 1000x1000
- 需要通过 system [prompt](../guides/prompt.md) 注入工具定义（function calling 格式）
- 建议开启 `vl_high_resolution_images: true` 以获得更好的识别效果

## 调用方式

两个模型均支持以下调用方式：

| 调用方式 | 说明 |
|---------|------|
| OpenAI Python SDK | 通过 `openai` 库调用，设置 `base_url` 指向百炼端点 |
| OpenAI Node.js SDK | 通过 `openai` npm 包调用 |
| curl / HTTP | 直接 POST 到 `/compatible-mode/v1/chat/completions` |

两个模型都支持**流式**和**非流式**两种输出模式。[流式输出](../concepts/streaming.md)需设置 `stream: true`，可选 `stream_options: {"include_usage": true}` 以获取用量信息。

## 多地域部署

Qwen-OCR 支持多地域部署，不同地域的 `base_url` 和 API Key 不同，具体说明参见 [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)：

| 地域 | base_url |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

> **注意**：GUI-Plus 目前仅在文档中提供了北京地域的 `base_url`，未明确说明多地域支持情况。如需在海外地域使用，请参考 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md) 或咨询官方文档获取最新信息。

## 关键参数

### 通用参数

- **model**（必选）：模型名称，Qwen-OCR 使用 `qwen-vl-ocr-latest`，GUI-Plus 使用 `gui-plus-2026-02-26`
- **messages**（必选）：对话消息数组，包含用户消息和可选的系统消息

### Qwen-OCR 特有参数

- **content.type**：`image_url`（输入图片）或 `text`（输入提示词）
- **image_url.url**：图片 URL 地址
- **min_pixels**：输入图像最小像素阈值，低于此值图像会被放大（默认 `32*32*3 = 3072`）
- **max_pixels**：输入图像最大像素阈值，超过此值图像会被缩小（默认 `32*32*8192 = 8388608`）

### GUI-Plus 特有参数

- **system message**：必须在 system [prompt](../guides/prompt.md) 中定义 `computer_use` 工具的函数签名
- **vl_high_resolution_images**：布尔值，建议设为 `true` 以启用高分辨率图像处理（通过 `extra_body` 传入）

## 使用前提

调用这两个模型前，需要完成以下准备：

1. 获取 API Key
2. 将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`
3. 如使用 SDK 调用，需安装对应的 OpenAI SDK（Python 或 Node.js）

## 来源文档

- [Qwen-OCR API参考](../../raw/model-api-reference/specialized-model/qwen-vl-ocr-api-reference.md)
- [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)




