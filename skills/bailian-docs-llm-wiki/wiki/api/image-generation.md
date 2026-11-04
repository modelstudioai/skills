# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成等）。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu 和 Z-Image 等，支持同步/[异步调用](../concepts/asynchronous-invocation.md)、多地域部署及 OpenAI 兼容协议。所有服务均需严格匹配模型、API Key 与 Endpoint 的地域一致性。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` / `qwen-image-3.0`（支持 T2I + I2I，[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）  
  - `wan2.7-image-pro` / `wan2.7-image`（支持文生图、组图、图像编辑，最高 4K 输出）  
  - `z-image-turbo`（轻量级文生图，快速响应，支持中英文字渲染）  

- **专业图像编辑与重绘**：  
  - `wan2.5-i2i-preview`（单图/多图融合编辑）、`wanx-style-repaint-v1`（人像风格重绘）、`wanx-x-painting`（图像局部重绘）  
  - `qwen-image-2.1-pro`（支持最多 10 张参考图，自动输出带透明通道图像）  

- **垂直场景工具**：  
  - `facechain-finetune`（人物形象训练）、`wanx-virtualmodel`（虚拟模特）、`shoemodel-v1`（鞋靴试穿）、`creative-poster-generation-v1`（创意海报）  
  - `image-erase-completion`（擦除补全）、`image-instance-segmentation`（人物实例分割）  

> **注意**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`wanx-poster-generation-v1` 等模型当前仅提供免费体验，额度用完后不可调用且不支持付费，官方明确建议迁移到 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 或 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 等替代方案。

- **视频关联图像模型**：  
  `kling/kling-v3-omni-image-generation`（支持分镜组图生成）、`vidu/viduq2-pro_reference2image`（工业级稳定性，适合漫剧制作）

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：  
  - 千问系列：支持自由宽高（如 `"1024*1536"`），总像素须在 `512×512` 至 `2048×2048` 之间；默认由模型自动推荐。  
  - 万相 V2（`wan2.6-t2i`）：支持 `[1280×1280, 1440×1440]` 总像素范围，宽高比 `1:4 ~ 4:1`。  
  - 可灵/ Vidu：显式指定 `"1K"` / `"2K"` / `"4K"`，或通过 `width`/`height` 字段设置（部分模型要求固定宽高比如 `16:9`, `1:1`）。  
- **`n`**：生成图像张数（多数模型支持 `1–9`，Z-Image 固定为 `1`）。  
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认 `true`）。  
- **`input.image` / `input.image_url` / `mask_url`**：图像输入方式，支持公网 URL 或 Base64；注意 `mask_url` 仅用于擦除补全等特定模型。  
- **`element_list`**（可灵）：指定需保持一致性的主体列表，与参考图数量之和 ≤ 10。  

## 使用方式

- **接入协议**：  
  - 千问支持 **OpenAI 兼容模式**（复用 `/v1/images/generations` 接口，传 `image` 字段即为 I2I），也支持 DashScope 同步/[异步调用](../concepts/asynchronous-invocation.md)；  
  - 万相 V2、Z-Image、可灵、Vidu 等统一使用 DashScope HTTP API，但调用方式分两类：  
    - **同步调用**：适用于 `wan2.7-image-pro`、`z-image-turbo` 等低延迟模型，一次请求返回结果（Endpoint：`/api/v1/services/aigc/multimodal-generation/generation`）；  
    - **[异步调用](../concepts/asynchronous-invocation.md)**：适用于耗时较长任务（如编辑、海报生成、FaceChain 训练），需两步：① `POST /generation` 创建任务获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 获取结果（有效期 24 小时）。  

- **地域与域名**：  
  所有模型必须保证 **模型、API Key、Endpoint URL 三者地域一致**（华北2/北京、新加坡、弗吉尼亚等）。强烈推荐迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，旧域名（`dashscope.aliyuncs.com`）虽仍可用但非最优。  

- **SDK 支持**：  
  DashScope Python/Java SDK 已覆盖千问、万相 V2、Z-Image 等主流模型；但 `wanx-style-repaint-v1` 等部分工具模型**仅提供 HTTP API，暂无 SDK**（见 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)）。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、弗吉尼亚等地域的 API Key 与 Endpoint **完全独立，不可混用**；跨地域调用将导致鉴权失败或 401/403 错误。  
- **图像输入限制**：  
  - 格式：普遍支持 PNG/JPEG/JPG，部分模型（如可灵）**不支持透明通道**；  
  - 分辨率：单边长度通常限 `300–8000` 像素（可灵）、`512–4096` 像素（擦除补全）；  
  - 大小：多数模型上限 `10MB`，虚拟模特/鞋靴模型建议 `<5MB`。  
- **文本提示词**：  
  - 长度限制：千问/万相一般 ≤2500 字符，Vidu 支持 ≤5000 字符；  
  - 内容要求：避免模糊指令（如“更好看”），应明确描述主体、动作、风格、构图；复杂图文混排需注意千问对“复杂文本渲染”的专项优化优势。  
- **免费额度与计费**：  
  - 免费额度按账号（含 RAM 子账号）共享，过期或用尽后需开通付费；  
  - FaceChain 训练（`facechain-finetune`）计费单元为“次”，单价 2.5 元/次，免费额度 50 次（90 天有效）；  
  - 多数创意工具（如虚拟模特、海报生成）当前**无付费通道，额度用尽即停用**。  
- **模型演进提示**：  
  > **注意**：文档中 `qwen-image-2.0-pro` 系列（如 `qwen-image-2.0-pro-2026-06-22`）被标注为“推荐”，但其能力已由 `qwen-image-3.0-pro` 全面覆盖；同理，`wan2.6-t2i` 已被 `wan2.7-image-pro` 取代。开发者应优先选用新版模型（3.0/2.7），旧版仅作兼容保留。

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
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)


