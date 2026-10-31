# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘及专业创意工具等场景。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到工业级生产的全栈需求。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0` 等支持文生图与图生图二合一，具备强文本渲染与语义遵循能力；`qwen-image-2.1-pro` 和 `qwen-image-2.1-turbo` 支持最多 10 张参考图输入，并可自动输出带透明通道图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相系列**：覆盖多代能力，`wan2.7-image-pro` 支持文生图 4K 输出；`wan2.6-image` 支持图文混排；`wan2.5-i2i-preview` 支持单图编辑与多图融合；`wanx-sketch-to-image-lite` 专用于涂鸦作画 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。  
- **专业工具类**：`facechain-finetune` 支持基于 1–10 张人脸图像训练专属人物形象；`image-erase-completion` 和 `image-instance-segmentation` 提供擦除补全与像素级实例分割能力；`wanx-style-repaint-v1` 实现人像艺术风格重绘 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。  
- **其他模型**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与工业级稳定性；`z-image-turbo` 为轻量级文生图模型，兼顾速度与中英文字渲染。

> **注意**：`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`、`image-instance-segmentation` 等模型当前仅提供免费体验，额度用完后不可调用且不支持付费，官方明确建议使用[图像编辑-千问](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/qwen-image-edit-guide.md)或[图像编辑-万相2.1](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/wanx-image-edit.md)作为替代方案。

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：  
  - 千问系列支持 `宽*高`（如 `"1024*1024"`）或语义值（如 `"2K"`、`"4K"`），总像素需在 `512×512` 至 `2048×2048` 之间；  
  - 万相 V2 (`wan2.6-t2i`) 要求总像素在 `[1280×1280, 1440×1440]` 区间；  
  - 可灵与 Vidu 支持 `"1K"`/`"2K"`/`"4K"` 字符串值，对应固定分辨率档位。  
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值 1–9）；`series_amount` 用于可灵组图模式（2–9）。  
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认开启）。  
- **`thinking_mode`**：部分万相模型（如 `wan2.7-image-pro`）支持启用推理过程可视化。  
- **`element_list`**（可灵）与 **`auxiliary_parameters`**（创意海报）等为模型特有高级参数，详见各模型文档。

## 使用方式

- **接入协议**：推荐使用 DashScope 同步调用（功能最全），亦支持 OpenAI 兼容模式（仅限千问系列，需切换 `base_url` 与 `model`）；异步调用适用于批量任务或长耗时场景（如图像编辑、虚拟模特）。  
- **请求地址**：必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **认证与配置**：所有模型均需地域匹配的 API Key，并通过环境变量（如 `DASHSCOPE_API_KEY`）或请求头 `Authorization: Bearer <key>` 传入；务必确保模型、Endpoint 与 API Key 属于同一地域，跨地域调用将失败。  
- **输入格式**：  
  - 文生图：`input.messages[0].content` 中传入 `text` 字段（中英文，长度限制依模型而定，如可灵为 2500 字符，Vidu 为 5000 字符）；  
  - 图生图/编辑：同上，额外在 `content` 数组中加入 `image` 字段（支持公网 URL 或 Base64）；  
  - 多图输入：万相 2.5+、可灵 Omni、Vidu 均支持多张 `image` URL，Vidu 最多 14 张，可灵要求 `image` + `element_list` 总数 ≤ 10。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key 与 Endpoint，不可混用；未明确说明支持多地域的模型（如早期 `wanx-v1`、`wanx2.1-imageedit`）仅限北京地域 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)。  
- **调用模式差异**：  
  - 千问、Z-Image、万相 2.7+ 支持 HTTP 同步调用；  
  - 万相 V2（`wan2.5` 及以下）、可灵、Vidu、所有创意工具类（虚拟模特、海报生成、擦除补全等）强制异步，必须包含 `X-DashScope-Async: enable` 请求头，否则报错。  
- **图像约束**：  
  - 输入图格式普遍支持 JPG/PNG（Vidu 不支持透明通道）；  
  - 分辨率下限多为 `512×512`，上限因模型而异（如可灵输入图宽高范围 `[300, 8000]`，Vidu 为 `[512, 4096]`）；  
  - 文件大小通常 ≤ 10MB，URL 不得含中文字符（需 URL 编码）。  
- **免费额度与计费**：多数创意工具类模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`）为限时免费，额度用尽即停用；FaceChain 训练按次计费（2.5 元/次），检测限时免费；详细计费请查阅各模型文档中的“计费单价”表格。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)


