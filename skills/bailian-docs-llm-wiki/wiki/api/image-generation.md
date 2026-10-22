# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，支持同步/异步调用、多模态输入与灵活分辨率控制。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同地域匹配。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等支持文生图与图生图二合一，[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)明确其支持 OpenAI 兼容协议及 DashScope 同步/异步调用。
- **万相系列**：涵盖 `wan2.7-image-pro`（4K 文生图）、`wan2.6-t2i`（V2 文生图）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx2.1-imageedit`（通用编辑）及 `wanx-sketch-to-image-lite`（涂鸦作画）等，[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)指出 wan2.6 及以上版本支持自由尺寸选型与 HTTP 同步调用。
- **可灵与 Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图；`vidu/vidu-image-pro_reference2image` 强调中英文字精准渲染与 UI/图表像素级还原，适用于专业设计场景。
- **轻量与垂直模型**：`z-image-turbo` 专注快速生图；`facechain-finetune` 提供人物形象定制训练能力；`wanx-style-repaint-v1`、`shoemodel-v1`、`virtualmodel-v2` 等属于创意工具子类，聚焦人像风格重绘、鞋靴试穿、虚拟模特等细分任务。

> **注意**：文档 2、5、6 中提及的 `qwen-image-2.0-pro` 等早期模型在文档 1 的“模型概览”中已被明确标注为 Legacy，当前推荐使用 `qwen-image-3.0-pro` 或 `qwen-image-3.0`；文档 9 明确提示“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，表明 V1 版本已不作为主力迭代方向。

## 关键参数

- **`size`**：控制输出分辨率。不同模型约束不同：
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间（[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）；
  - 万相 V2（`wan2.6-t2i`）：宽高比 `[1:4, 4:1]`，总像素 `[1280×1280, 1440×1440]`；
  - 万相 2.7 Pro：文生图支持 `4K`，编辑/组图限 `2K`；
  - 可灵与 Vidu：支持 `1K`/`2K`/`4K` 显式指定；
  - Z-Image：总像素 `[512×512, 2048×2048]`。
- **`n` / `series_amount`**：控制生成张数。千问、万相基础模型默认 `n=1`；可灵 `kling-v3-omni` 在组图模式下通过 `series_amount` 指定 `2~9` 张。
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 支持）。
- **`thinking_mode`**：部分万相模型（如 `wan2.7-image-pro`）支持开启思考模式以提升语义一致性。
- **`element_list`**：可灵模型用于指定需保持的主体列表，与参考图数量合计 ≤10。

## 使用方式

- **调用协议**：主流模型均支持 DashScope SDK（Python/Java）及 HTTP 接口；千问系列额外提供 OpenAI 兼容模式（仅同步），通过切换 `base_url` 和 `model` 即可复用现有 OpenAI 集成逻辑。
- **同步 vs 异步**：
  - 同步调用（推荐多数场景）：适用于 `qwen-image-*`、`wan2.7-image-*`、`z-image-turbo` 等低延迟模型，单次请求返回结果。
  - 异步调用（必需）：`wan2.5-i2i-preview`、`kling/*`、`vidu/*`、`wanx-style-repaint-v1`、`shoemodel-v1` 等耗时较长模型必须使用“创建任务 → 轮询结果”两步流程，`task_id` 有效期 24 小时。
- **输入格式**：
  - 文本：`text` 字段，长度限制因模型而异（如可灵 ≤2500 字符，Vidu ≤5000 字符）；
  - 图像：支持公网 URL 或 Base64；万相通用编辑、Vidu 最多支持 14 张参考图；千问 2.1 系列支持最多 10 张。
- **Endpoint 与认证**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），并配置对应地域的 API Key 到环境变量 `DASHSCOPE_API_KEY`。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key、Endpoint 和 Workspace ID，跨地域调用必然失败。文档 1、6、7、11、12 均强调此规则。
- **免费额度与限流**：多数创意工具类模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`）当前仅限免费体验，额度用尽即不可调用（见文档 13、22、24、26）。所有模型均对 QPS 和并发任务数设限（如 FaceChain 训练限 QPS=2，并发=1）。
- **图像输入限制**：参考图格式通常限 JPEG/PNG/JPG；分辨率范围常见为 `[300, 8000]` 像素（可灵）或 `[512, 4096]`（擦除补全）；文件大小上限多为 10MB。
- **模型弃用风险**：文档 2、5、6 中列出的 `qwen-image-2.0-*` 及 `wanx-v1` 等模型已被新版本替代，生产环境应避免依赖；文档 9 明确将 V1 版本标记为非推荐。
- **异步接口头字段**：HTTP 异步调用必须携带 `X-DashScope-Async: enable`，缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”（见文档 9、13、15、18、22、23、24、25、26、27）。

## 来源文档

- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


