# image generation

百炼平台提供多种图像生成与编辑模型，覆盖文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、创意工具等全场景能力。所有模型均通过统一的 DashScope API 协议接入，支持同步/异步调用、OpenAI 兼容模式及多语言 SDK。开发者需注意地域隔离、API Key 与 Endpoint 的严格匹配，以及业务空间专属域名的迁移要求。

## 支持的模型/功能

平台当前提供四大类图像模型：

- **通用文生图与编辑**：千问系列（`qwen-image-*`）和万相系列（`wan2.*-t2i`, `wan2.*-image`, `wan2.*-i2i-preview`）均支持高质量文生图与图像编辑，其中 `qwen-image-3.0-pro` 和 `wan2.7-image-pro` 支持 4K 输出；[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确其 T2I/I2I 双模能力。
- **轻量与专用模型**：`z-image-turbo` 专为快速响应设计，适合低延迟场景；`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/viduq3.1-fast_reference2image` 支持分辨率与画幅比例自由指定。
- **创意工具链**：涵盖人像风格重绘、虚拟模特、鞋靴试穿、创意海报生成、人物实例分割、图像擦除补全等垂直能力，全部基于 HTTP 异步接口实现；[创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md) 指出该模型目前仅限免费体验。
- **定制化人像生成**：FaceChain 提供端到端的人物形象训练（`facechain-finetune`）与写真生成流水线，需先完成人脸检测（`facechain-facedetect`）与文件上传，再调用定制任务接口；[FaceChain人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md) 详细说明了训练文件准备与提交流程。

> **注意**：万相-文生图V1版（`wanx-v1`）已被明确标记为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且 V1 文档注明“仅适用于华北2（北京）地域”，而 V2 版已支持北京、新加坡、弗吉尼亚三地，V1 应视为过时模型，不建议新项目接入。

## 关键参数

所有模型共用核心参数结构，关键字段如下：

- `model`：必填字符串，如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`、`"kling/kling-v3-omni-image-generation"`。各地域支持的模型列表需在控制台确认。
- `input.messages`：必填数组，单轮对话格式，`content` 内含 `text`（提示词）和可选 `image`（参考图 URL 或 Base64）。`text` 长度限制因模型而异：千问/万相通常为 2500 字符，Vidu 支持至 5000 字符。
- `parameters.size`：控制输出分辨率。格式多样：
  - 千问系列：接受 `"2K"`、`"4K"` 或具体宽高比（如 `"1024*1024"`），总像素须在 `512*512` 至 `2048*2048` 之间；
  - 万相 V2.5+：支持自定义 `宽*高`（如 `"768*2700"`），默认 `1280*1280`；
  - Vidu/Kling：限定为 `"1K"`/`"2K"`/`"4K"`，并约束宽高比（如 `16:9`, `1:1`）。
- `parameters.n`：生成图像张数，范围通常为 `1–9`（千问/万相/Kling），Z-Image 固定为 `1`。
- `parameters.watermark`：布尔值，控制是否添加水印（默认 `true`）。
- `X-DashScope-Async`：HTTP 调用必需头，异步请求必须设为 `"enable"`；同步调用（如千问 DashScope 同步、万相 2.7+）则不可设置此头。

## 使用方式

调用流程遵循“准备 → 请求 → 获取结果”三步：

1. **环境准备**：获取对应地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；安装 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python/Java）或直接使用 HTTP 客户端。
2. **Endpoint 选择**：**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 强调此举“能够为推理请求提供卓越的性能和更高的稳定性”。
3. **调用方式选择**：
   - **同步调用**：适用于千问（DashScope 同步）、万相 2.6+/2.7、Z-Image 等，一次 POST 即返回结果（含 PNG 图像 Base64 或 URL）。
   - **异步调用**：适用于万相 V2.5 及以下、Kling、Vidu、所有创意工具及 FaceChain 训练，需两步：① POST 创建任务获 `task_id`；② GET 轮询 `task_id` 直至状态为 `SUCCESS`，再提取 `output.results[0].url`（有效期 24 小时）。
   - **OpenAI 兼容**：千问支持 `/v1/images/generations` 接口，`image` 字段存在即为图生图，无需改造现有 OpenAI SDK。

## 限制和注意事项

- **地域强绑定**：API Key、Endpoint、模型三者必须同属一个地域（北京/新加坡/弗吉尼亚）。跨地域调用将导致鉴权失败或服务报错，文档中多次强调此点（如 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)、[Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)）。
- **免费额度与计费**：多数创意工具（如 `wanx-style-repaint-v1`, `shoemodel-v1`, `image-erase-completion`）及 FaceChain 检测/训练均提供有限免费额度（通常 500 张或 50 次），用尽后不可续订；[创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md) 明确标注“免费额度用完后不可调用且不支持付费”，应提前规划替代方案。
- **输入约束**：
  - 图像格式：主流支持 JPG/PNG/WebP，但 Kling 不支持透明通道，Vidu 要求参考图无中文 URL。
  - 分辨率：单边长度通常限于 `[300, 8000]` 像素（Kling）或 `[512, 4096]`（擦除补全），超限将报错。
  - 提示词：禁止包含违法、色情、暴力内容；千问对复杂文本渲染（如多行书法）有专项优化，但需精确描述排版细节。
- **模型演进**：万相 V1 已废弃，千问早期模型（`qwen-image-2.0` 系列）被 `3.0` 系列取代，开发者应优先选用文档中标注 `推荐` 的最新版本。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)


