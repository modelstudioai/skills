# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景需求。核心模型包括千问系列（Qwen-Image）、万相系列（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等，均支持通过 DashScope 协议或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与业务空间必须同地域配对使用。

## 支持的模型/功能

- **千问图像生成与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro`、`qwen-image-2.1-turbo` 等，统一支持文生图与图生图/编辑双模态，其中 `qwen-image-3.0-pro` 支持最高 2048×2048 分辨率，且图生图可传入最多 10 张参考图 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相系列**：涵盖多代模型，如 `wan2.7-image-pro`（支持 4K 文生图）、`wan2.6-t2i`（V2 文生图主力）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx-style-repaint-v1`（人像风格重绘）等；另含专用工具类模型，如 `wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-x-painting`（局部重绘）[万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。  
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/viduq3.1-fast_reference2image` 支持按分辨率与画幅比例精确指定输出尺寸 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。  
- **轻量与垂直模型**：`z-image-turbo` 为轻量级文生图模型，适合快速响应场景；`facechain-finetune` 支持基于 2~10 张人脸图像训练专属写真模型，需前置人脸检测（`facechain-facedetect`）与文件管理流程 [FaceChain人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)。  
- **创意工具套件**：包含虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像擦除补全（`image-erase-completion`）及人物实例分割（`image-instance-segmentation`），全部为华北2（北京）地域专属服务，且多数当前仅限免费体验。

> **注意**：文档中 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`、`image-instance-segmentation` 均明确标注“目前仅供免费体验，免费额度用完后不可调用且不支持付费”，而 `qwen-image-2.0-pro` 在文档4中被列为推荐模型，但其能力已被 `qwen-image-3.0-pro` 全面覆盖，实际生产环境应优先选用新版模型。

## 关键参数

- **`size` / `parameters.size`**：控制输出分辨率。不同模型取值范围不同：  
  - 千问系列：支持自由宽高组合，总像素须在 `512×512` 至 `2048×2048` 之间；未指定时自动推荐 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - 万相 V2 (`wan2.6-t2i`)：限定总像素在 `[1280×1280, 1440×1440]` 区间；  
  - Vidu 与可灵：支持 `1K`/`2K`/`4K` 字符串标识（如 `"2K"`），部分型号还支持显式宽高比（如 `16:9`）。  
- **`n` / `series_amount` / `generate_num`**：控制生成张数。`n` 适用于千问、可灵文生图（1–9 张）；`series_amount` 专用于可灵组图模式（2–9 张）；`generate_num` 用于创意海报（1–4 张）。  
- **`watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型如 `wan2.7-image-pro` 支持设为 `false`。  
- **`thinking_mode`**：仅 `wan2.7-image-pro` 支持，启用后返回推理过程描述（非必需）。  
- **`element_list`**（可灵）与 `auxiliary_parameters`（创意海报）：分别为主体保持列表与高分辨率修复参数，属高级控制字段。

## 使用方式

- **同步调用**：适用于千问（DashScope 同步）、万相 2.6/2.7、Z-Image 等模型，单次 HTTP POST 即返回结果，Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`，需设置 `Content-Type: application/json` 与 `Authorization: Bearer <API_KEY>`。  
- **[异步调用](../concepts/asynchronous-invocation.md)**：适用于万相 V1/V2 编辑类（`wan2.5-i2i-preview`）、可灵、Vidu、创意工具全系及 FaceChain 训练任务。流程为：① `POST /generation` 或 `/fine-tunes` 提交任务获取 `task_id`；② 轮询 `/tasks/{task_id}` 查询状态；③ 成功后获取带 24 小时有效期的图像 URL。所有异步请求必须携带 `X-DashScope-Async: enable` 请求头。  
- **OpenAI 兼容模式**：千问图像模型支持直接复用 OpenAI Images SDK，仅需将 `base_url` 切换为百炼域名，`model` 设为 `qwen-image-3.0-pro`，文生图不传 `image` 字段，图生图则传入 Base64 或公网 URL。  
- **SDK 依赖**：推荐安装 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，Python/Java 均已支持；部分工具类模型（如人像风格重绘）仅提供 HTTP 接口，无官方 SDK。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key、Endpoint 和业务空间 ID，**跨地域混用必然失败**。务必使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。  
- **输入约束**：  
  - 图像格式：JPEG/JPG/PNG 为主，部分模型（如可灵）明确不支持透明通道；  
  - 图像尺寸：单边长度通常限制在 `[300, 8000]`（可灵）或 `[512, 4096]`（擦除补全）像素；  
  - 提示词长度：可灵限 2500 字符，Vidu 限 5000 字符，超长将报错。  
- **免费额度与限流**：多数创意工具模型（虚拟模特、鞋靴模特、海报生成等）为限时免费，额度用尽即停服；QPS 与并发数按账号（含 RAM 子账号）全局限制，例如 `facechain-finetune` QPS=2、并发=1，`wanx-style-repaint-v1` QPS=2、并发=1。  
- **模型弃用提示**：文档中多次出现 `legacy-qwen-image-models`、`wanx2.1-t2i-turbo` 等路径，表明对应模型已归档；新项目应避免使用 `wanx-v1`、`wanx2.1` 等 V1/V2 早期版本，转而采用 `wan2.6-t2i` 或 `wan2.7-image-pro`。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


