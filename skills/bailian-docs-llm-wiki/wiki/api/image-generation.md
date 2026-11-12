# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及专业创意工具等场景。核心模型包括千问（Qwen-Image）、万相（WanX）、Z-Image、可灵（Kling）、Vidu 及 FaceChain 等系列，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到工业级设计的全栈需求。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）同时支持 T2I 与 I2I，支持多图输入（最多 10 张参考图），并可自动输出带透明通道图像；  
  - `wan2.7-image-pro` 支持 4K 文生图输出，`wan2.6-t2i` 支持自由宽高比（1:4 至 4:1）与总像素 1280×1280–1440×1440；  
  - `z-image-turbo` 是轻量级模型，专为中英文字渲染与快速响应优化，总像素支持 512×512 至 2048×2048。

- **专业图像编辑与创意工具**：  
  - 图像编辑类：`wan2.5-i2i-preview`（多图融合）、`qwen-image-2.1-turbo`（语义强遵循）、`vidu/viduq2-pro_reference2image`（工业级稳定性）；  
  - 创意工具类：`wanx-style-repaint-v1`（人像风格重绘）、`virtualmodel-v2`（虚拟模特，支持 2048 像素短边与多长宽比）、`shoemodel-v1`（鞋靴AI试穿）、`facechain-finetune`（LoRA微调定制人物形象）；  
  - 辅助能力：`image-instance-segmentation`（像素级人像掩码）、`image-erase-completion`（擦除补全）、`vary-region`（局部重绘）。

> **注意**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等模型当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议迁移到 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md) 或 [图像编辑-万相2.1](../../raw/model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md) 等替代方案。

## 关键参数

- **分辨率控制**：  
  - 多数模型通过 `parameters.size` 指定，格式如 `"1024*1024"` 或预设值 `"1K"`/`"2K"`/`"4K"`；  
  - `qwen-image-3.0` 默认不指定 `size` 时由模型自动推荐；`wan2.5-i2i-preview` 未指定时默认 `1280*1280` 并保持输入图宽高比；  
  - `kling/kling-v3-omni-image-generation` 仅支持固定宽高比（16:9 / 9:16 / 1:1）。

- **输出控制**：  
  - `n`：控制生成张数（如 `qwen-image-2.0-pro` 支持 1–6 张，`kling` 支持 1–9 张）；  
  - `watermark`：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认 `false`）；  
  - `thinking_mode`：启用推理过程可视化（仅 `wan2.7-image-pro` 支持）。

- **输入约束**：  
  - 提示词长度：`kling` 限 2500 字符，`vidu` 限 5000 字符；  
  - 图像输入：`kling` 要求参考图宽高在 [300, 8000] 像素、宽高比 1:2.5–2.5:1；`vidu` 最多支持 14 张参考图；  
  - `facechain-finetune` 要求训练图 1–10 张，单图分辨率 256×256–4096×4096。

## 使用方式

- **接入协议**：  
  - 推荐使用 **DashScope 同步调用**（功能最全，支持 Base64 与公网 URL 输入）或 **OpenAI 兼容模式**（仅需切换 `base_url` 和 `model`，适用于已有 OpenAI 集成）；  
  - 批量/长耗时任务（如图像编辑、虚拟模特）必须使用 **DashScope 异步调用**（创建任务 → 轮询 `task_id`）。

- **域名与地域**：  
  - 华北2（北京）和新加坡地域**必须使用业务空间专属域名**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；  
  - `dashscope.aliyuncs.com` 等旧域名虽仍可用，但文档明确强调新域名“提供卓越性能和更高稳定性”，强烈建议迁移（[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）。

- **认证与配置**：  
  - 必须为**同一地域**获取 API Key、配置环境变量、选择 Endpoint；跨地域混用将导致鉴权失败；  
  - RAM 子账号调用必须传入 `X-DashScope-WorkSpace` Header 指定 Workspace ID；主账号可不填。

## 限制和注意事项

- **地域隔离严格**：华北2（北京）、新加坡、美国（弗吉尼亚）三地 API Key 与请求地址完全独立，不可复用（[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)）；  
- **异步强制要求**：所有图像编辑类模型（如 `wan2.5-i2i-preview`、`kling/kling-v3-image-generation`、`image-erase-completion`）及创意工具（`virtualmodel-v2`、`shoemodel-v1`）均**仅支持异步调用**，HTTP 请求头必须包含 `X-DashScope-Async: enable`，否则报错；  
- **免费模型风险**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等模型无付费通道，额度用尽即不可用，生产环境应避免依赖；  
- **输入兼容性**：`kling` 不支持 PNG 透明通道；`facechain-facedetect` 要求图像 URL 中文字符必须 URL 编码，否则返回 `InternalError.Algo`；  
- **模型演进提示**：`qwen-image-2.0` 系列已标注为“早期模型”，新项目应优先选用 `qwen-image-3.0` 系列（[千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)）。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
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
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


