# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意海报生成等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具（如 FaceChain、虚拟模特等），支持同步与异步调用，适配开发者集成需求。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0` 支持 T2I 和 I2I 一体化能力，支持最多 10 张参考图输入，并可自动输出带透明通道的 PNG；`wan2.7-image-pro` 支持 4K 文生图输出，`wan2.6-image` 支持图文混排；`z-image-turbo` 为轻量级模型，适合快速生成中英文渲染图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **专业图像编辑能力**：`wan2.5-i2i-preview` 支持单图编辑与多图融合；`vidu/vidu-image-pro_reference2image` 擅长中英文字精准渲染与 UI/图表像素级还原；`qwen-image-2.1-pro` 明确支持多图参考与透明通道自适应输出 [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)。
- **垂直创意工具**：`facechain-finetune` 支持基于 2–10 张人脸图像训练专属人物形象；`wanx-virtualmodel` 和 `shoemodel-v1` 分别面向虚拟模特与鞋靴试穿；`image-erase-completion` 实现掩码驱动的擦除补全；`wanx-style-repaint-v1` 提供人像艺术风格重绘 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。
- **已归档/不推荐模型**：`wanx-v1`、`wanx2.1-t2i-turbo` 等早期版本已被明确标注为“推荐使用 V2 版本”或仅限免费体验且无付费路径，实际生产环境应避免选用 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v1-api-reference.md)。

> **注意**：文档中 `wanx-sketch-to-image-lite`（涂鸦作画）与 `wanx-x-painting`（局部重绘）均声明“目前仅供免费体验，免费额度用完后不可调用且不支持付费”，而同属万相体系的 `wan2.7-image-pro` 和 `wan2.6-image` 则明确支持商用计费，存在功能定位与生命周期策略差异，需按业务稳定性要求谨慎选型。

## 关键参数

- **`size`**：控制输出分辨率。不同模型约束不同：
  - `qwen-image-*` 系列：总像素需在 `512×512` 至 `2048×2048` 之间，未指定时由模型自动推荐；
  - `wan2.7-image-pro`：文生图支持 `4K`（如 `3840×2160`），编辑与组图限 `2K`；
  - `kling/kling-v3-omni-image-generation`：支持 `1K/2K/4K`，宽高比限定为 `16:9`、`9:16` 或 `1:1`；
  - `vidu/*_reference2image`：统一支持 `1K/2K/4K` 输出。
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值 `1–9`）；`series_amount` 用于分镜组图（如 `kling/kling-v3-omni-image-generation`，取值 `2–9`）。
- **`image` 字段**：所有支持图生图的模型均通过该字段传入参考图 URL 或 Base64。限制包括：
  - 格式：`JPEG/JPG/PNG`（多数模型不支持透明通道，`qwen-image-2.1-pro` 除外）；
  - 尺寸：单边 `300–8000` 像素（Kling）、`512–4096` 像素（Vidu、擦除补全）；
  - 数量：`qwen-image-2.1-pro` 和 `qwen-image-2.1-turbo` 最多支持 10 张；`vidu` 系列最多 14 张；`kling-v3-omni` 中参考图数量 + `element_list` 长度 ≤ 10。
- **`watermark`、`thinking_mode`**：`wan2.7-image-pro` 支持 `watermark=false` 关闭水印，`thinking_mode=true` 启用推理过程可视化（调试用）。

## 使用方式

- **调用协议**：主流模型均支持 DashScope SDK（Python/Java）和 HTTP 接口；`qwen-image-*` 还额外提供 OpenAI 兼容模式（仅同步），便于已有 OpenAI 生态快速迁移 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **同步 vs 异步**：
  - **同步调用**：适用于 `qwen-image-*`、`wan2.7-image-*`、`wan2.6-image`、`z-image-turbo` 等低延迟模型，一次请求即返回结果（HTTP `POST /multimodal-generation/generation`）。
  - **异步调用**：适用于耗时较长任务（如 `kling`、`vidu`、`wan2.5-i2i-preview`、`facechain-finetune`、各类创意工具），流程为：① `POST /.../generation` 创建任务并获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 获取状态与结果 URL（有效期 24 小时）。
- **地域与域名**：**必须保证模型、API Key、Endpoint URL 三者地域一致**（北京/新加坡/弗吉尼亚等）。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其性能与稳定性优于公共域名 `dashscope.aliyuncs.com`；跨地域调用将直接失败。

## 限制和注意事项

- **地域隔离严格**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key 与 Endpoint 完全独立，混用将导致鉴权失败或服务报错。`wan2.5-i2i-preview`、`kling`、`vidu` 等文档均反复强调此点 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- **免费模型风险**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`wanx-poster-generation-v1` 等十余个创意工具模型明确标注“仅免费体验，额度用尽后不可调用且不支持付费”，生产环境应优先选用 `qwen-image-*` 或 `wan2.7-image-*` 等商业化模型。
- **输入校验强依赖**：`facechain-finetune` 要求训练图满足人脸数量=1、尺寸≥128×128、无遮挡等条件；`image-instance-segmentation` 要求输入图分辨率在 `512×512` 至 `4096×4096` 之间；`kling` 对参考图宽高比限定在 `1:2.5 ~ 2.5:1`。不符合约束将直接返回错误而非降级处理。
- **URL 编码要求**：所有接受 `image_url` 或 `mask_url` 的接口（如 `facechain-facedetect`、`image-erase-completion`），若 URL 含中文或特殊字符，**必须进行 percent-encoding**（如 Python `urllib.parse.quote()`），否则触发 `InternalError.Algo` 错误 [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)


