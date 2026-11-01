# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、创意工具等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到工业级生产的各类开发者场景。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/图像编辑双模态，其中 `qwen-image-3.0-pro` 支持最多10张参考图输入，并能根据提示词自动输出带透明通道的 PNG 图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **万相系列**：涵盖多代模型，如 `wan2.7-image-pro`（支持4K文生图）、`wan2.6-t2i`（V2版文生图）、`wan2.5-i2i-preview`（通用图像编辑）、`wanx-sketch-to-image-lite`（涂鸦作画）及 `wanx-style-repaint-v1`（人像风格重绘）等；部分模型（如 `wanx-x-painting`）当前仅限免费体验 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/viduq2-pro_reference2image` 专精复杂逻辑与工业级稳定性，均支持1K/2K/4K分辨率输出 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。
- **轻量与专用模型**：`z-image-turbo` 为轻量级文生图模型，强调速度与中英文字渲染；`facechain-finetune` 支持基于2张照片训练专属人物形象，需配合 `facechain-facedetect` 进行前置质量校验 [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)。
- **创意工具类**：包括虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像擦除补全（`image-erase-completion`）及人物实例分割（`image-instance-segmentation`），全部为华北2（北京）地域专属服务，且多数当前仅限免费体验。

> **注意**：文档中 `wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`、`image-instance-segmentation` 等模型均明确标注“目前仅供免费体验，免费额度用完后不可调用且不支持付费”，与通用付费模型（如 `qwen-image-3.0-pro` 或 `wan2.7-image-pro`）在计费模式和长期可用性上存在本质差异，开发者应避免将其用于生产环境依赖路径。

## 关键参数

- **`model`**：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`），不同模型支持的参数范围不同。
- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问系列：接受 `"1024*1024"`、`"2048*2048"` 等像素值，或 `"2K"`、`"4K"`（`wan2.7-image-pro` 文生图支持 `"4K"`）；
  - 万相V2（`wan2.6-t2i`）：限定总像素在 `[1280*1280, 1440*1440]` 区间；
  - 可灵/Vidu：接受 `"1K"`、`"2K"`、`"4K"` 字符串。
- **`n`**：指定生成图像张数（如 `qwen-image-3.0-pro`、`kling/kling-v3-image-generation` 支持 `1–9` 张）；部分模型（如 `z-image-turbo`）固定为1张。
- **`input.messages[].content`**：必填数组，包含 `text`（提示词，长度限制依模型而定：千问≤2500字符，Vidu≤5000字符）和可选 `image`（参考图URL或Base64，万相2.5支持最多14张，千问2.1 Pro支持最多10张）。
- **`parameters.watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认 `false`）。
- **`parameters.thinking_mode`**：布尔值，启用推理过程可视化（仅 `wan2.7-image-pro` 支持）。

## 使用方式

- **接入协议**：推荐使用 DashScope 同步调用（功能最完整）或 OpenAI 兼容模式（零改造迁移）。OpenAI 兼容模式下，`/images/generations` 接口通过是否传入 `image` 字段区分文生图与图生图 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **调用方式**：
  - **同步调用**：适用于 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo` 等模型，一次 HTTP 请求返回结果，Endpoint 为 `/api/v1/services/aigc/multimodal-generation/generation`。
  - **异步调用**：适用于耗时较长任务（如万相2.5编辑、可灵、Vidu、创意工具类），需两步：① `POST /image-synthesis` 或 `/generation` 创建任务获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 获取结果，`task_id` 有效期24小时。
- **地域与域名**：所有模型均要求 **API Key、Endpoint、业务空间 ID 三者地域一致**（华北2/北京、新加坡、美国弗吉尼亚等）。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性，旧域名（`dashscope.aliyuncs.com`）虽仍可用但非最优 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **SDK 与环境**：推荐安装 DashScope SDK（Python/Java），并配置 `DASHSCOPE_API_KEY` 环境变量；HTTP 调用需设置 `Authorization: Bearer <key>` 和 `Content-Type: application/json`。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、业务空间 ID **完全独立，不可混用**。跨地域调用将导致鉴权失败或 401/404 错误，此限制在千问、万相、可灵、Vidu 等所有文档中反复强调。
- **输入约束**：
  - 图像格式：JPG/JPEG/PNG 为主，部分模型（如 `kling/kling-v3-image-generation`）**不支持透明通道**；万相2.5编辑支持 PNG，但涂鸦作画（`wanx-sketch-to-image-lite`）未明确限制。
  - 图像尺寸：千问/万相/可灵等主流模型要求单边像素在 `[512, 8000]` 区间，总像素上限 `2048*2048`；Vidu 支持 `4K`（约 `3840*2160`）。
  - 提示词长度：千问 ≤2500 字符，Vidu ≤5000 字符，超长将直接报错。
- **免费额度与限流**：创意工具类模型（虚拟模特、鞋靴模特、海报生成等）普遍标注“仅限免费体验”，额度用尽即不可用；主模型（如 `qwen-image-3.0-pro`）按实际调用计费。所有模型对 QPS 和并发任务数均有严格限制（如 FaceChain 训练 QPS=2，并发=1），详情需查阅各模型计费文档。
- **模型演进**：早期模型（如 `qwen-image-2.0-pro`、`wanx-v1`）已明确被新版本（`qwen-image-3.0-pro`、`wan2.6-t2i`）取代，文档中多次提示“推荐使用全面升级的[新版模型]”，开发者应优先选用 `3.x` 或 `2.6+` 版本以获得最佳能力与支持。

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
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


