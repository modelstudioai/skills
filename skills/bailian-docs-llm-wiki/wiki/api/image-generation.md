# image generation

百炼平台提供多种图像生成与编辑模型，覆盖文生图（T2I）、图生图（I2I）、图像翻译、局部重绘、风格迁移、创意工具等全场景能力。所有模型均通过统一的 DashScope API 协议接入，支持同步/异步调用、OpenAI 兼容模式及多语言 SDK，适用于从快速原型到生产级集成的各类开发者需求。

## 支持的模型/功能

平台当前提供三大主力图像模型系列及十余种垂直工具模型：

- **千问（Qwen-Image）系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/图像编辑双模态任务，[原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确其核心能力边界与地域约束。
- **万相（WanX）系列**：涵盖 `wan2.7-image-pro`（4K文生图）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx-sketch-to-image-lite`（涂鸦作画）等，支持自由分辨率选型与多任务混合调用；其中 `wan2.6-t2i` 为推荐文生图V2模型，[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 详述其尺寸与宽高比约束。
- **专业工具模型**：包括 `vidu/vidu-image-pro_reference2image`（工业级参考生图）、`z-image-turbo`（轻量快速生图）、`qwen-mt-image-2.0`（图像翻译），以及创意类工具如 `wanx-style-repaint-v1`（人像风格重绘）、`facechain-finetune`（人物形象LoRA训练）等。

> **注意**：部分早期模型（如 `wanx-v1`、`qwen-image-2.0`）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”或“当前与新版能力相同”，实际开发中应优先选用带 `-pro`、`-2.5`、`-2.7` 或 `-turbo` 后缀的现代版本，避免兼容性风险。

## 关键参数

所有图像模型共用以下核心参数结构（具体取值范围依模型而异）：

- `model`：必填字符串，指定模型 ID（如 `"wan2.7-image-pro"`、`"qwen-image-3.0-pro"`）；
- `input.messages`：必填数组，单轮 `user` 角色消息，含 `text`（提示词）和可选 `image`（参考图 URL 列表）；
- `parameters.size`：控制输出分辨率，支持显式值（如 `"1024*1024"`）、预设档位（如 `"1K"`、`"2K"`、`"4K"`）或留空由模型自动推荐；
- `parameters.n`：生成图像张数（多数模型支持 1–9 张，`wan2.7-image-pro` 文生图场景支持 1 张，组图生成限 1 张）；
- `parameters.watermark`：布尔值，控制是否添加百炼水印（默认 `true`）；
- `input.image_url` / `input.images`：用于图像编辑类模型（如 `image-erase-completion`、`wanx-x-painting`），需传入原始图与掩码图 URL。

图像格式统一为 PNG（除 `qwen-mt-image-2.0` 固定输出 JPG）；分辨率总像素严格限制在 `512×512` 至 `2048×2048` 区间（`wan2.6-t2i` 限定 `[1280×1280, 1440×1440]`，`vidu` 系列支持 `4K` 即 `3840×2160`）。

## 使用方式

### 接入协议
- **同步调用**：适用于 `qwen-image-*`（DashScope 同步）、`wan2.7-image-*`、`z-image-turbo` 等低延迟模型，单次 HTTP POST 即返回结果；
- **异步调用**：适用于耗时较长的模型（如 `wan2.5-i2i-preview`、`kling/kling-v3-image-generation`、`facechain-finetune`），需两步操作：① `POST /generation` 创建任务获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 查询状态；
- **OpenAI 兼容模式**：仅 `qwen-image-*` 系列支持，复用 OpenAI Images 接口路径，通过 `base_url` 切换至百炼域名即可无缝迁移。

### 地域与认证
- 所有模型强制要求 **API Key、Endpoint、Workspace ID 三者同地域**（华北2/北京、新加坡、弗吉尼亚等），跨地域调用必然失败；
- 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐；
- 认证头统一为 `Authorization: Bearer <API_KEY>`，请求体 `Content-Type: application/json`。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、弗吉尼亚等地域拥有独立 API Key 与 Endpoint，不可混用；[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 和 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 均强调此约束；
- **免费额度与限流**：多数创意工具模型（如 `wanx-x-painting`、`shoemodel-v1`、`image-erase-completion`）仅提供 500 张免费额度，用尽后不可续费，文档明确建议转向 `qwen-image-edit` 或 `wanx-image-edit` 替代；
- **输入限制**：参考图 URL 必须公网可访问、无中文字符、格式合规（JPG/PNG/WEBP 等）；`qwen-mt-image-2.0` 要求宽高比在 `1:10` 至 `10:1`，单边 ≤8192px；`kling` 模型要求参考图宽高比在 `1:2.5` 至 `2.5:1`；
- **异步超时**：任务轮询需自行实现重试逻辑，结果 URL 有效期统一为 24 小时；
- **模型弃用**：`wanx-v1`、`wanx2.1-t2i-turbo` 等 V1 版本已归档，新项目禁止使用；`viduq2-fast_reference2image` 仅支持 `1K` 分辨率，与其他 `vidu` 子型号能力不一致。

## 来源文档

- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)


