# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意文字生成等多类任务。核心能力由千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列创意工具模型共同支撑，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到生产级集成的各类开发者场景。

## 支持的模型/功能

平台当前提供三类图像能力模型：

- **通用生成与编辑模型**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（支持 T2I + I2I，[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）；  
  - `wan2.7-image-pro`（支持文生图、组图、图像编辑，最高4K输出）；  
  - `wan2.6-t2i`（文生图V2主力模型，支持自由尺寸与多宽高比）；  
  - `kling/kling-v3-omni-image-generation`（支持单图/多图参考生图及分镜组图）；  
  - `vidu/vidu-image-pro_reference2image`（强文本渲染与UI/图表像素级还原）；  
  - `z-image-turbo`（轻量级文生图，兼顾速度与中英文字渲染）。

- **垂直创意工具模型**：  
  包括人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、AI试衣（`aitryon-plus`）、人物写真（`facechain-generation`）、文字变形（`wordart-semantic`）和图像背景生成（`wanx-background-generation-v2`）等，均面向特定业务场景深度优化。

- **辅助与后处理模型**：  
  如图像擦除补全（`image-erase-completion`）、图像画面扩展（`image-out-painting`）、AI试衣精修（`aitryon-refiner`）等，需配合主模型使用。

> **注意**：部分早期模型（如 `wanx-v1`、`qwen-image-2.0` 系列）已明确标注为“推荐使用升级版”，且其文档中提及的分辨率约束（如 `wanx-v1` 要求总像素在 `[512×512, 1440×1440]`）与新版 `wan2.6-t2i` 的 `[1280×1280, 1440×1440]` 存在重叠但不完全一致；实际调用应以最新版 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 为准。

## 关键参数

所有图像模型共用以下核心参数结构，具体取值因模型而异：

- `model`（必选）：模型标识符，如 `"wan2.7-image-pro"`、`"qwen-image-3.0-pro"`。
- `input`（必选）：包含提示词与可选图像输入：
  - `messages` 数组（仅限部分模型，如 Kling/Vidu），含 `role: "user"` 与 `content`（含 `text` 和 `image` URL/Base64 列表）；
  - `prompt` 字符串（传统文生图模型，如 WanX V1/V2）。
- `parameters`（可选）：
  - `size`：输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。`qwen-image-3.0-pro` 要求总像素在 `512×512` 至 `2048×2048` 之间；`wan2.6-t2i` 限定在 `[1280×1280, 1440×1440]`；`kling` 支持 `1k/2k/4k` 预设档位。
  - `n`：生成张数，范围通常为 `1–9`（`z-image-turbo` 固定为 `1`）。
  - `style` / `font_name` / `generate_mode`：模型特有参数，如 WordArt 的字体选择或海报生成的 `sr`（超分）模式。
- `X-DashScope-Async`（HTTP 异步调用必需）：必须设为 `"enable"`，否则报错 `"current user api does not support synchronous calls"`。

## 使用方式

### 接入协议
- **同步调用**：适用于 `qwen-image-3.0-pro`（DashScope 同步）、`wan2.7-image-pro`、`z-image-turbo` 等低延迟模型，一次请求返回结果。
- **异步调用**：适用于耗时较长的任务（如多数编辑、扩图、试衣模型），流程为：  
  1. `POST /api/v1/services/.../generation` 创建任务 → 获取 `task_id`；  
  2. `GET /api/v1/tasks/{task_id}` 轮询状态 → 返回 `result.url`（有效期 24 小时）。  
  示例见 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

### 地域与域名
- **严格地域隔离**：API Key、Endpoint URL、模型部署地域必须一致（如华北2北京、新加坡、弗吉尼亚），跨地域调用将鉴权失败。
- **推荐使用业务空间专属域名**：  
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`；  
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。  
  `{WorkspaceId}` 在控制台「业务空间详情」中获取，旧域名（`dashscope.aliyuncs.com`）仍可用但性能与稳定性较低。

### 开发准备
- 获取并配置 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；
- 安装 DashScope SDK（Python/Java）或直接使用 HTTP（需设置 `Content-Type: application/json`、`Authorization: Bearer <key>`）；
- 图像输入支持公网 URL 或 Base64 编码（URL 需 HTTPS 且无中文路径，建议先做 URL 编码）。

## 限制和注意事项

- **免费额度与计费**：  
  多数模型提供 500 张/90 天免费额度（如 `wanx-style-repaint-v1`、`facechain-generation`），用尽后按量付费（如 `aitryon-plus` 0.50 元/张，`wordart-semantic` 0.24 元/张）。详细规则见 [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)。

- **调用限制**：  
  - QPS（每秒请求数）与并发任务数按账号（主账号+RAM子账号）共享，例如 `aitryon` 为 RPS=10 / 并发=5，`facechain-finetune` 为 QPS=2 / 并发=1；  
  - 部分模型（如 `wanx-x-painting`、`shoemodel-v1`）为“限时免费”，额度用尽即不可用，无付费通道。

- **输入约束**：  
  - 图像尺寸：`image-instance-segmentation` 要求 `512×512` 至 `4096×4096`；`virtualmodel-v2` 短边为 `1024` 或 `2048`；  
  - 文字渲染：`qwen-image-3.0-pro` 和 `vidu` 系列对中英文文本布局与像素级还原能力突出，适合海报/UI 生成；  
  - FaceChain 训练需正脸单人照（≥1 张，256×256～4096×4096），禁止多人脸或遮挡。

- **关键避坑点**：  
  > **注意**：`X-DashScope-Async: enable` 是所有 HTTP 异步调用的强制头，缺失将直接报错；  
  > **注意**：`wan2.5-i2i-preview` 默认输出 `1280×1280`，但若未指定 `size` 且输入图为 `4:3`，输出宽高比会近似保持，而非强制正方——此行为与 `qwen-image-3.0-pro` 的“默认自动推荐分辨率”逻辑不同，需显式传参确保一致性；  
  > **注意**：`facechain-generation` 必须先通过 [申请体验](https://bailian.console.aliyun.com/model/market/detail/facechain-generation) 审批，否则返回错误状态码，非单纯 API Key 权限问题。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)


