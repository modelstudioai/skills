# image generation

百炼平台提供覆盖文生图、图生图、图像编辑及垂直场景的完整生成能力，支持通过 HTTP 接口或 DashScope SDK 快速集成。平台整合了千问、万相、可灵等多系列模型，满足从基础高清出图、复杂文本渲染到交互式编辑与分镜生成的高阶需求。开发者可根据业务对延迟、画质与成本的要求，灵活选择同步或异步调用模式。

## 支持的模型与核心功能
* **通用文生图**：`qwen-image-2.0` 系列擅长多语言复杂文本渲染与细节刻画；`wan2.6-t2i` / `wan2.7-image` 系列支持高分辨率（最高4K）与图文混排；`z-image-turbo` 为轻量极速模型；`kling/kling-v3` 系列支持角色/场景连续性的分镜组图生成。详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)。
* **图像编辑与处理**：涵盖指令编辑、局部重绘、背景替换、智能扩图与擦除补全。`wan2.7-image` 与 [[qwen-image-edit]] 支持交互式框选编辑与多图融合；`image-out-painting` 专注多比例画面扩展。
* **垂直场景与专项模型**：提供 [[aitryon]]（AI试衣与分割精修）、虚拟模特、[[facechain]]（人物写真训练与生成）、创意海报、创意文字（[[wordart]]）及鞋靴试穿等开箱即用方案。图像翻译可通过 [[qwen-mt-image]] 实现带排版保留的跨语种转换。

> **注意**：平台部分早期模型（如 `wanx-v1`、`wanx-sketch-to-image-lite`、`wanx-x-painting`、`wanx-poster-generation-v1`、`wanx-virtualmodel` 等）目前仅支持免费体验，免费额度耗尽后将停止服务且不支持付费转商用。生产环境请优先迁移至万相 2.5+ 或千问系列。详见 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)。

## 关键参数
不同模型协议存在差异，核心参数映射如下：
* **输入结构**：新协议统一使用 `input.messages` 数组格式（如 `[{"role": "user", "content": [{"text": "[[prompt|prompt]]"}, {"image": "url"}]}]`）；旧版协议使用 `input: { [[prompt|prompt]]: "...", images: [...] }`。
* **尺寸控制 (`size` / `resolution`)**：支持格式通常为 `"宽*高"`（如 `"1280*1280"`）或预设档位（`"1K"`, `"2K"`, `"4K"`）。总像素上限因模型而异（常见为 2048×2048 或 4K），宽高比通常需在 `[1:10, 10:1]` 范围内。未指定时默认保持输入图比例或生成 `1024*1024`/`1280*1280`。
* **生成策略**：`n` 控制输出张数（通常 1~6）；`watermark` 默认 `true`，需显式传 `false` 关闭水印；`negative_[[prompt|prompt]]` 用于屏蔽不期望元素；`prompt_extend` 或 `thinking_mode` 可启用提示词智能优化或深度推理，但会增加首字延迟。
* **参考控制**：`ref_image` 配合 `ref_strength` / `ref_mode` 实现内容或风格迁移；`enable_interleave` 开启后可输出图文混排内容。

## 调用方式
* **同步调用（Sync）**：推荐用于 `qwen-image`、`z-image`、`wan2.6+` 等新一代模型。Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。单次 POST 请求即可直接返回图像 URL 或 Base64，链路最短。
* **异步调用（Async）**：适用于 `wanx` 早期版本、大部分编辑类与翻译类模型。请求 Header 必须携带 `X-DashScope-Async: enable`。流程分为两步：1. POST 创建任务获取 `task_id`；2. GET `/v1/tasks/{task_id}` 轮询状态，直至 `SUCCEEDED`。[[async-polling]] 机制下 `task_id` 有效期为 24 小时。
* **SDK 支持**：Python 与 Java DashScope SDK 已全面适配新版协议。安装后可通过 `Generation` 或 `AsyncCall` 客户端封装鉴权与轮询逻辑。

## 限制与注意事项
* **地域与鉴权隔离**：[[api-key]]、计费额度与服务 Endpoint 严格绑定部署地域（如北京、新加坡、弗吉尼亚）。跨地域混用 Key 或地址将直接导致 `InvalidApiKey` 或 `AccessDenied` 报错。
* **图像输入规范**：公网 URL 必须支持 HTTP/HTTPS 且不可包含中文字符；格式通常为 JPG/PNG/WEBP；文件大小一般限制在 10MB 以内；分辨率单边需在 512~4096 像素之间。下载失败通常由防火墙拦截、防盗链或 URL 编码问题引起。
* **计费与限流**：仅对成功生成的**输出图片**计费（按张）。主账号与 RAM 子账号共享免费额度（默认 500 张，90 天有效）与限流阈值（多数模型 QPS 为 2，并发任务 1~2 个）。超限将触发排队或 `RateLimit` 错误。
* **协议演进**：平台正逐步收敛至多模态统一路由。新业务开发请勿使用已废弃的独立路由（如 `/text2image/image-synthesis`、`/image2image/image-synthesis`），以免影响后续功能迭代。详见 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md) 中的服务开通说明。
* **内容安全**：所有请求均经过前置合规检测。触发安全策略的提示词或参考图将直接拦截，请确保输入内容符合合规要求。

## 来源文档

- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wanx-image-edit-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-scaling-api.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/vary-region-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/wordart-quick-start.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)

