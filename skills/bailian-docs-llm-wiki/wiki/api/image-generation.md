# image generation

百炼平台提供多种图像生成与编辑模型，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景能力。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK 集成。所有模型均需严格遵循地域隔离原则，API Key、Endpoint 与业务空间必须同地域。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/图像编辑双模态任务，其中 `qwen-image-3.0-pro` 支持自动透明通道输出 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
- **万相系列**：涵盖多代文生图（`wan2.6-t2i`、`wan2.5-t2i-preview`）、图像编辑（`wan2.5-i2i-preview`、`wanx-image-edit-api-reference`）、涂鸦作画（`wanx-sketch-to-image-lite`）、局部重绘（`wanx-x-painting`）等，其中 `wan2.7-image-pro` 支持文生图场景下的 4K 输出 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)；  
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/viduq3.1-fast_reference2image` 支持通过分辨率与画幅比例精确指定输出尺寸 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)；  
- **轻量与专用模型**：`z-image-turbo` 为轻量级文生图模型，适合快速响应；`facechain-finetune` 支持基于 2~10 张人脸图像训练专属 LoRA 模型，用于批量写真生成；  
- **创意工具类**：含人像风格重绘、虚拟模特、鞋靴模特、创意海报生成、人物实例分割、图像擦除补全等，多数为免费体验模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`），额度用尽后不可续费，建议迁移到千问或万相主模型 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。

> **注意**：文档中 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等模型明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，与通用付费模型（如 `qwen-image-3.0-pro`）存在显著服务生命周期差异，开发者需在架构设计中预留降级路径。

## 关键参数

| 参数 | 类型 | 说明 | 示例值 |
|------|------|------|--------|
| `model` | string | 必选，模型标识符，严格区分大小写与斜杠格式 | `"qwen-image-3.0-pro"`, `"kling/kling-v3-omni-image-generation"` |
| `size` | string / number | 可选，控制输出分辨率；支持 `"1K"`/`"2K"`/`"4K"` 或 `宽*高` 格式（如 `"1024*1024"`）；部分模型（如 `z-image-turbo`）要求总像素在 `[512*512, 2048*2048]` 区间 | `"2048*2048"`, `"4K"` |
| `n` | integer | 可选，生成图像张数（1–9），仅部分模型支持（如 Kling、万相 V2） | `3` |
| `watermark` | boolean | 可选，是否添加水印（默认 `true`） | `false` |
| `input.messages[].content[].text` | string | 必选（文生图），正向提示词，长度上限依模型而定（千问≤2500字符，Vidu≤5000字符） | `"一只橘猫坐在窗台，阳光洒落"` |
| `input.messages[].content[].image` | string | 可选（图生图），参考图 URL 或 Base64；万相 2.5+ 支持多图输入，但总数与 `element_list` 之和 ≤10 | `"https://xxx.png"` |

> **注意**：`size` 参数行为不一致——`qwen-image-3.0-pro` 默认根据提示词自动推荐分辨率，而 `wan2.5-i2i-preview` 未指定时默认 `1280*1280` 且按输入图宽高比缩放，开发者需按模型文档分别校验 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 使用方式

- **调用协议**：  
  - 同步调用：适用于 `qwen-image-*`（DashScope 同步）、`z-image-turbo`、`wan2.6-image`、`wan2.7-image` 等，单次 HTTP 请求返回结果；  
  - 异步调用：适用于 `wan2.5-t2i-preview`、`kling/*`、`vidu/*`、`wanx-*` 工具类模型等，需先 `POST /generation` 创建任务获取 `task_id`，再轮询 `GET /tasks/{task_id}` 获取结果（URL 有效期 24 小时）；  
  - OpenAI 兼容：`qwen-image-3.0-pro` 支持 `/v1/images/generations` 接口，传 `image` 字段即为图生图，否则为文生图。  

- **请求地址**：  
  - **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；  
  - 各模型 endpoint 路径不同：文生图常用 `/api/v1/services/aigc/text2image/image-synthesis`，图生图/编辑常用 `/api/v1/services/aigc/image2image/image-synthesis`，万相 2.6+/2.7 使用 `/api/v1/services/aigc/multimodal-generation/generation`。  

- **认证与配置**：  
  - 所有请求需携带 `Authorization: Bearer <API-Key>`；  
  - 异步调用**必须**设置请求头 `X-DashScope-Async: enable`，缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”；  
  - 地域隔离：API Key、Workspace ID、Endpoint 必须同属一个地域（北京/新加坡/弗吉尼亚），跨地域调用必然失败。

## 限制和注意事项

- **地域强约束**：华北2（北京）、新加坡、美国（弗吉尼亚）三地 API Key 与 Endpoint 完全独立，不可混用；万相 V2 文档明确指出“三地拥有独立 API Key 与请求地址，不可混用” [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；  
- **输入限制**：  
  - 图像格式：JPEG/JPG/PNG 为主，部分模型（如 Kling）**不支持透明通道**；  
  - 分辨率：多数模型要求单边 ≥512px 且 ≤4096px，Kling 参考图宽高范围为 `[300, 8000]` 像素；  
  - 提示词长度：千问限 2500 字符，Vidu 限 5000 字符，超长将直接报错；  
- **免费模型风险**：`wanx-x-painting`、`shoemodel-v1`、`image-erase-completion` 等工具类模型明确声明“免费额度用完后不可调用且不支持付费”，无替代付费通道，生产环境应避免依赖；  
- **SDK 与协议兼容性**：万相 V1、V2 及多数创意工具仅支持 HTTP 异步调用，**不提供官方 SDK 封装**（如人像风格重绘明确注明“仅提供 HTTP API，暂无 SDK”）；  
- **业务空间 ID 传递**：所有新域名请求 URL 中 `{WorkspaceId}` 必须替换为真实 ID（控制台“业务空间详情”页查看），未替换将导致 404 或鉴权失败。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
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
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)


