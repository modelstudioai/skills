# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘及专业场景工具（如虚拟模特、海报生成、FaceChain写真等）。所有模型均通过统一的 DashScope API 协议接入，支持同步与[异步调用](../concepts/asynchronous-invocation.md)模式，适配开发者集成需求。

## 支持的模型/功能

- **千问系列（Qwen-Image）**：支持文生图与图生图/图像编辑一体化能力，主流模型包括 `qwen-image-3.0-pro`（推荐）、`qwen-image-2.1-turbo` 和 `qwen-image-2.0-pro` 系列。其中 `qwen-image-3.0-pro` 同时支持 T2I 与 I2I，且默认根据提示词自动推荐分辨率 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **万相系列（WanX）**：提供多代模型，覆盖通用文生图（`wan2.6-t2i`, `wan2.7-image-pro`）、图像编辑（`wan2.5-i2i-preview`, `wanx2.1-imageedit`）、涂鸦作画（`wanx-sketch-to-image-lite`）、局部重绘（`wanx-x-painting`）等。`wan2.7-image-pro` 在文生图场景下支持 4K 输出，而组图生成与图像编辑限于 2K [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
- **可灵（Kling）与 Vidu**：专注高保真生成与工业级稳定性。`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图；`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与像素级 UI 还原 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。
- **创意工具类**：包括人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、FaceChain 写真（需先训练 `facechain-finetune`）等，多数为免费体验模型，额度用尽后不可续用 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。
- **轻量模型**：`z-image-turbo` 适用于快速原型验证，支持中英文字渲染与灵活宽高比，总像素范围为 512×512 至 2048×2048 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。

> **注意**：`wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-instance-segmentation`、`image-erase-completion` 等模型当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议迁移到千问或万相 2.1+ 编辑模型作为替代方案（见 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md) 及 [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）。

## 关键参数

- **`model`**：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"` 或 `"wan2.7-image-pro"`），需与所选地域支持的模型列表一致。
- **`size`**：控制输出分辨率，格式因模型而异：
  - `qwen-image-*`：接受 `width*height`（如 `"1024*1024"`）或语义值（如 `"2K"`），总像素须在 512×512 至 2048×2048 之间；
  - `wan2.*` 系列：支持 `"1K"`/`"2K"`/`"4K"` 或具体尺寸（如 `"1280*1280"`）；
  - `kling`/`vidu`：仅支持预设值 `"1K"`/`"2K"`/`"4K"` 及宽高比约束（如 `"16:9"`）。
- **`n`**：生成图像张数（部分模型支持，如 `kling/kling-v3-image-generation` 支持 1–9 张；`qwen-image-*` 默认 1 张，最大 6 张）。
- **`input.messages[].content`**：包含 `text`（必填提示词，长度限制依模型而定：`kling` ≤2500 字符，`vidu` ≤5000 字符）和可选 `image`（URL 或 base64，数量上限各异：`kling` 总参考图+主体数 ≤10；`vidu` 最多 14 张）。
- **`watermark`**、`thinking_mode`：`wan2.7-image-pro` 等模型支持禁用水印（`false`）或启用推理过程可视化（`true`）。

## 使用方式

- **调用协议**：统一使用 DashScope HTTP API（兼容 OpenAI Images 协议的 `qwen-image-*` 模型除外）。OpenAI 兼容模式仅支持同步调用，且 `/images/generations` 接口通过 `image` 字段区分 T2I/I2I [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **同步 vs 异步**：
  - **同步**：适用于低延迟场景（如 `qwen-image-*`、`wan2.7-image-pro`、`z-image-turbo`），单次请求返回结果，Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
  - **异步**：适用于耗时较长任务（如 `wan2.5-i2i-preview`、`kling`、`vidu`、所有创意工具类模型），需两步：① `POST /image-synthesis` 或 `/generation` 创建任务获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 查询状态，结果 URL 有效期 24 小时。
- **地域与域名**：必须确保 API Key、Endpoint 和业务空间 ID（`{WorkspaceId}`）属同一地域（北京/新加坡/弗吉尼亚）。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，旧域名（`dashscope.aliyuncs.com`）仍可用但非最优 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **认证与 SDK**：通过 `Authorization: Bearer <API_KEY>` 认证；推荐安装 DashScope SDK（Python/Java），并配置 `DASHSCOPE_API_KEY` 环境变量；若使用自定义 Host，需替换 `DASHSCOPE_API_HOST`。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key、Endpoint、业务空间 ID 严格隔离，混用将导致鉴权失败或服务报错（见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 及 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)）。
- **输入限制**：
  - 图像格式：JPEG/JPG/PNG（`kling` 不支持透明通道；`vidu`/`wan2.*` 支持 PNG 透明）；
  - 图像分辨率：单边长度通常为 300–8000 像素（`kling`）、512–4096 像素（创意工具类）；
  - 提示词长度：`kling` ≤2500 字符，`vidu` ≤5000 字符，超限将报错。
- **免费额度与限流**：多数创意工具类模型（如 `wanx-style-repaint-v1`, `shoemodel-v1`）有 500 张/次免费额度，用尽即停；QPS/RPS 限制按账号（含 RAM 子账号）共享，例如 `wanx-style-repaint-v1` QPS=2，`facechain-finetune` QPS=2 并发=1 [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)。
- **模型弃用**：`wanx-v1`（V1 版文生图）已不推荐使用，应升级至 `wan2.6-t2i` 或更高版本；`qwen-image-2.0` 系列虽仍可用，但新项目建议选用 `qwen-image-3.0-pro` 以获完整功能支持。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


