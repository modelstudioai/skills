# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、专业工具链（如虚拟模特、FaceChain）等全场景需求。核心模型包括千问图像系列（qwen-image）、万相（wanx/wan2.x）、可灵（kling）、Vidu、Z-Image 及创意工具套件，均支持通过 DashScope 协议或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用。所有服务需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同地域匹配。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0` 支持 T2I 和 I2I 一体化调用；`wan2.7-image-pro` 支持 4K 文生图及多图参考生成；`z-image-turbo` 为轻量级快速生图模型，适合低延迟场景 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **专业图像编辑**：`wan2.5-i2i-preview` 支持单图编辑与多图融合；`qwen-image-2.0-pro` 在文字渲染与语义遵循上表现突出；`vidu/vidu-image-pro_reference2image` 擅长 UI/图表像素级还原与复杂逻辑处理 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。
- **创意工具链**：涵盖人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`virtualmodel-v2`）、鞋靴试穿（`shoemodel-v1`）、图像擦除补全（`image-erase-completion`）及 FaceChain 人物写真生成（需先训练 `facechain-finetune` 模型）[创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。
- **图像翻译与本地化**：`qwen-mt-image-2.0` 支持中、英、日、韩、西、法等 55 种语言互译，精准保留排版 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

> **注意**：`wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-poster-generation-v1`、`shoemodel-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-virtualmodel` 等模型当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确推荐迁移到千问或万相 2.1+ 系列替代 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。

## 关键参数

- **`model`**：必填，指定模型名称（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`vidu/viduq2-pro_reference2image`），不同模型能力差异显著，需按任务类型选择。
- **`size`**：控制输出分辨率，格式因模型而异：
  - `qwen-image-*`：接受 `宽*高`（如 `1024*1024`）或预设值（如 `"2K"`）；
  - `wan2.6-t2i`：总像素约束在 `[1280*1280, 1440*1440]`；
  - `kling/kling-v3-image-generation`：仅支持 `"1k"`、`"2k"`；
  - `vidu/*`：支持 `"1K"`、`"2K"`、`"4K"`（字符串大小写敏感）。
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling`、`qwen-image`），取值 1–9；`series_amount` 专用于 `kling/kling-v3-omni-image-generation` 的分镜组图模式（2–9 张）。
- **`input.messages.content`**：统一结构，为 `array` 类型，包含 `text`（必填提示词）和 `image`（可选参考图 URL 数组）。`vidu` 和 `kling` 均支持最多 14 张参考图输入。
- **`parameters.watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持设为 `false`。

## 使用方式

- **调用协议**：推荐使用 DashScope 同步调用（`/multimodal-generation/generation` 或 `/image-generation/generation`），功能最完整；OpenAI 兼容模式仅支持同步，适用于已集成 OpenAI SDK 的应用 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **地域与域名**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **认证与配置**：API Key 需与 Workspace ID 同地域，且必须通过环境变量（如 `DASHSCOPE_API_KEY`）或请求头 `Authorization: Bearer <key>` 传入。
- **异步流程**：对耗时较长的任务（如 `wan2.5-i2i-preview`、`kling`、`vidu`、`FaceChain` 训练），采用“创建任务 → 轮询结果”两步式：
  1. `POST /api/v1/services/.../generation`（带 `X-DashScope-Async: enable` 头）获取 `task_id`；
  2. 定期 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回图像 URL（有效期通常为 24 小时）。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、Workspace ID 三者必须严格一致，跨地域调用必然失败。
- **图像输入限制**：
  - URL 必须公网可访问、无中文路径（需 URL 编码）、协议为 HTTP/HTTPS；
  - 格式支持 JPG/JPEG/PNG/BMP/WEBP/TIFF，不支持透明通道（除 `qwen-image-2.1-pro` 明确声明支持）；
  - 分辨率：多数模型要求宽高均在 `[512, 8192]` 像素，总像素上限 `2048*2048`（约 400 万像素）；
  - 文件大小：通常 ≤10 MB，`qwen-mt-image-2.0` 要求 ≤100 MB。
- **文本提示词**：长度限制因模型而异——`kling` 限 2500 字符，`vidu` 限 5000 字符；禁止空提示词或纯符号。
- **免费模型风险**：`wanx-poster-generation-v1`、`shoemodel-v1`、`image-erase-completion` 等模型无付费通道，额度耗尽即不可用，生产环境应避免依赖。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)


