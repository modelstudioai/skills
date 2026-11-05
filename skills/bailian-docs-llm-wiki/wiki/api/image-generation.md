# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、专业工具类（如虚拟模特、海报生成）等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等，均支持通过 DashScope SDK 或 HTTP API 调用，适配开发者集成需求。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` / `qwen-image-3.0`（支持 T2I + I2I，[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）  
  - `wan2.7-image-pro`（支持 4K 文生图、组图生成、多图参考编辑）  
  - `z-image-turbo`（轻量级快速生图，支持中英文字渲染）  

- **专业图像工具**：  
  - `kling/kling-v3-omni-image-generation`（支持多图参考与分镜组图）  
  - `vidu/viduq2-pro_reference2image`（工业级稳定性，适合漫剧、UI 设计）  
  - `facechain-finetune`（需先训练人物专属 LoRA 模型，再生成写真）  

- **创意增强与后处理**：  
  - `wanx-style-repaint-v1`（人像风格重绘）  
  - `image-erase-completion`（擦除补全，需 mask 输入）  
  - `wanx-virtualmodel` / `shoemodel-v1`（虚拟模特、鞋靴试穿）  

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`image-instance-segmentation`）当前仅限免费体验，额度用尽后不可调用且不支持付费，建议优先选用千问或万相系列替代 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必选，指定模型名称 | `"qwen-image-3.0-pro"`, `"wan2.7-image-pro"` |
| `size` | string / string | 分辨率控制（部分模型支持语义值如 `"2K"`，部分需 `"width*height"`） | `"2K"`, `"1280*1280"`, `"2048*2048"` |
| `n` | integer | 生成图像张数（多数模型支持 1–9 张） | `1`, `4` |
| `watermark` | boolean | 是否添加水印（默认 `true`） | `false` |
| `input.messages[].content[].text` | string | 正向提示词，长度限制因模型而异（如 Kling ≤2500 字符，Vidu ≤5000 字符） | `"一只橘猫坐在窗台，阳光洒落"` |
| `input.messages[].content[].image` | string array | 参考图 URL 列表（Vidu 最多支持 14 张；千问 2.1 系列最多 10 张） | `["https://x.png"]` |

> **注意**：`size` 参数行为不一致——`wan2.5-i2i-preview` 默认输出 `1280*1280` 并保持输入图宽高比，而 `qwen-image-3.0-pro` 默认由模型自动推荐分辨率，未显式指定时无固定值 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 使用方式

- **调用协议**：  
  - 同步调用：适用于 `qwen-image-*`、`z-image-turbo`、`wan2.6-image`、`wan2.7-image` 等模型，单次请求返回结果（推荐大多数场景）。  
  - [异步调用](../concepts/asynchronous-invocation.md)：适用于 `kling/*`、`vidu/*`、`wan2.5-i2i-preview`、`wanx-style-repaint-v1` 等耗时较长模型，需两步：① 提交任务获取 `task_id`；② 轮询 `task_id` 获取结果（URL 有效期 24 小时）。  

- **地域与域名**：  
  - **必须保证模型、API Key、Endpoint 三者地域一致**（华北2/北京、新加坡、美国弗吉尼亚等），跨地域调用将失败。  
  - **强烈推荐使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于公共域名 `dashscope.aliyuncs.com`。  

- **SDK 与 HTTP**：  
  - DashScope Python/Java SDK 全面支持同步/[异步调用](../concepts/asynchronous-invocation.md)（除少数模型如 `wanx-x-painting` 仅支持 HTTP）。  
  - HTTP 请求头必须包含 `Authorization: Bearer <API_KEY>` 和 `Content-Type: application/json`；[异步调用](../concepts/asynchronous-invocation.md)还需 `X-DashScope-Async: enable`。  

## 限制和注意事项

- **图像输入限制**：  
  - 格式：PNG/JPG/JPEG/WEBP/BMP（部分模型如 `qwen-mt-image-2.0` 仅支持 JPG）；  
  - 分辨率：宽高均在 `[300, 8192]` 像素间（`kling`）或 `[512, 4096]`（`image-erase-completion`）；  
  - 大小：≤10 MB（多数模型），`qwen-mt-image-2.0` ≤100 MB；  
  - URL：必须公网可访问、无中文字符（需 URL 编码），否则报 `InternalError.Algo` [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。  

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）各自拥有独立 API Key 与 Endpoint，不可混用；RAM 子账号调用必须显式传入 `X-DashScope-WorkSpace`。  

- **免费模型约束**：`wanx-x-painting`、`shoemodel-v1`、`image-erase-completion` 等模型免费额度为 500 张/账号，用尽后服务不可用，文档明确建议迁移到千问或万相系列。  

- **模型弃用提示**：万相 V1 版（`wanx-v1`）已不推荐使用，应升级至 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；千问早期模型（如 `qwen-image-2.0`）已由 3.0 系列全面替代。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)


