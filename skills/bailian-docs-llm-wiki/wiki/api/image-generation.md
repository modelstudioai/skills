# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，支持同步/异步调用、多地域部署与业务空间专属域名接入。所有模型均需严格匹配地域级 API Key 与 Endpoint。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/图像编辑双模式，其中 `qwen-image-3.0-pro` 是当前主力推荐模型 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；早期模型如 `qwen-image-2.0-pro` 已归入[千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)文档，不建议新项目使用。
- **万相系列**：涵盖多代文生图（`wan2.6-t2i`、`wan2.7-image-pro`）、通用图像编辑（`wan2.5-i2i-preview`）、涂鸦作画（`wanx-sketch-to-image-lite`）、局部重绘（`wanx-x-painting`）等，其中 `wan2.7-image-pro` 支持文生图场景下的 4K 输出 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/vidu-image-pro_reference2image` 强调中英文字精准渲染与 UI/图表像素级还原，适用于专业设计场景。
- **轻量与垂直工具**：`z-image-turbo` 为快速响应型文生图模型；`facechain-finetune` 支持基于 2~10 张人脸图像训练专属写真模型，需配合前置[人物图像检测](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)确保输入质量。
- **创意工具类**：包括人像风格重绘、虚拟模特、鞋靴模特、创意海报生成、图像擦除补全、人物实例分割等，均为华北2（北京）地域专属服务，多数处于免费体验阶段（如 `wanx-style-repaint-v1`、`shoemodel-v1`），额度用尽后需切换至千问或万相主模型替代。

> **注意**：`wanx-x-painting`（图像局部重绘）、`wanx-virtualmodel`（虚拟模特）、`shoemodel-v1`（鞋靴模特）、`wanx-poster-generation-v1`（创意海报）等模型明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，官方推荐迁移到[图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)或[图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)作为生产环境替代方案。

## 关键参数

- **`model`**：必填字符串，值须与实际部署模型严格一致（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`），不同地域支持的模型列表需以[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)为准。
- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问系：支持 `512*512` 至 `2048*2048` 总像素范围，可显式指定（如 `"1024*1024"`）或使用语义值（如 `"2K"`）；
  - 万相 V2+：`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`，宽高比 `[1:4, 4:1]`；`wan2.7-image-pro` 文生图支持 `"4K"`，编辑/组图限 `"2K"`；
  - 可灵/Vidu：固定 `"1K"`/`"2K"`/`"4K"` 枚举值。
- **`n` / `series_amount`**：控制生成张数。`n` 用于单图模式（如 `1~9`），`series_amount` 用于可灵的分镜组图（`2~9`）。
- **`input.messages.content`**：必须为单元素数组，含 `text`（提示词，长度限制依模型而定：千问≤2500字符，Vidu≤5000字符）和可选 `image`（参考图 URL 或 Base64，数量上限：可灵≤10张，Vidu≤14张）。
- **`parameters.watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持设为 `false`。
- **`X-DashScope-Async`**：HTTP 调用必需头，异步模型（如万相 V1/V2 编辑、可灵、Vidu）必须设为 `"enable"`；同步模型（如千问 DashScope 同步调用、Z-Image）不可设置该头。

## 使用方式

- **同步调用（推荐多数场景）**：适用于千问（DashScope 同步接口）、Z-Image、万相 `wan2.7-image-pro` 等。一次 HTTP POST 请求即返回结果，Endpoint 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，需配置 `Content-Type: application/json` 和 `Authorization: Bearer <API_KEY>`。
- **异步调用（长耗时任务必需）**：适用于万相 V1/V2 编辑、可灵、Vidu、创意工具类（虚拟模特、海报生成等）。流程为两步：① `POST /api/v1/services/.../generation` 创建任务并获取 `task_id`；② 定期 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回带 24 小时有效期的图像 URL。
- **OpenAI 兼容模式**：千问支持 OpenAI Images 协议，仅需将 `base_url` 切换为百炼专属域名，`model` 设为对应千问模型名，无需修改请求结构 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **SDK 调用**：推荐使用 DashScope SDK（Python/Java），已封装同步/异步逻辑及错误重试。安装见 [安装DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，调用前务必配置环境变量 `DASHSCOPE_API_KEY`。

## 限制和注意事项

- **地域强绑定**：API Key、Endpoint、模型三者必须同属一个地域（如华北2、新加坡、弗吉尼亚）。跨地域调用必然失败，错误码通常为鉴权失败或 404。万相 V2+ 与可灵/Vidu 明确支持弗吉尼亚地域，但千问与 Z-Image 当前仅支持华北2与新加坡。
- **域名迁移强制要求**：华北2（北京）与新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 虽仍可用，但官方强调新域名“提供卓越性能和更高稳定性”，强烈建议迁移 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **输入图像约束**：
  - 格式：主流 PNG/JPEG/WebP，但可灵明确不支持透明通道；
  - 分辨率：单边 300~8000 像素（可灵）、512~4096 像素（擦除补全/实例分割）；
  - 大小：普遍 ≤10MB，部分工具类（如鞋靴模特）建议 <5MB；
  - URL 编码：若图像 URL 含中文或特殊字符，必须进行 percent-encoding，否则返回 `InternalError.Algo` [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。
- **免费额度与限流**：多数创意工具类模型（如 `wanx-style-repaint-v1`, `image-erase-completion`）有 500 张免费额度，用尽即停；QPS/并发限制按账号（含 RAM 子账号）全局共享，例如 FaceChain 训练限 QPS=2、并发=1，人像检测限 QPS=5。
- **模型能力边界**：千问 `qwen-image-2.1-pro` 与 `qwen-image-2.1-turbo` 支持根据提示词自动决定是否输出透明通道（PNG with alpha），但万相 `wan2.5-i2i-preview` 默认无 alpha；Vidu 系列强调 UI/图表像素级还原，而万相涂鸦作画（`wanx-sketch-to-image-lite`）专精手绘风格生成，选型需匹配业务目标。

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
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
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
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)


