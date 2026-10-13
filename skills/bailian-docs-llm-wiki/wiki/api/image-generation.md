# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成等）。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu 和 Z-Image，均支持通过 DashScope SDK 或 HTTP API 调用。所有模型均需严格匹配地域（如华北2、新加坡）的 API Key 与 Endpoint，跨地域调用将失败。

## 支持的模型/功能

- **通用生成与编辑**：  
  - `qwen-image-3.0-pro` / `qwen-image-3.0`：统一支持文生图与图生图，推荐用于高精度编辑任务；[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确其支持 OpenAI 兼容模式与 DashScope 同步/异步调用。  
  - `wan2.7-image-pro`：支持文生图（4K）、组图生成、图像编辑；`wan2.5-i2i-preview` 专注单/多图编辑与融合。  
  - `kling/kling-v3-omni-image-generation`：支持多图参考生图与分镜组图生成，适用于叙事性内容创作。  

- **轻量与垂直场景模型**：  
  - `z-image-turbo`：轻量级文生图模型，响应快，适合对延迟敏感的场景。  
  - `vidu/vidu-image-pro_reference2image`：强项为中英文字精准渲染与 UI/图表像素级还原，适用于信息图、海报设计。  
  - 创意工具类模型（如 `wanx-style-repaint-v1`、`shoemodel-v1`、`image-erase-completion`）均为华北2（北京）地域专属，且多数仅限免费体验，详见[虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)等文档。

> **注意**：万相 V1 系列（如 `wanx-v1`）和早期千问模型（如 `qwen-image-2.0`）已明确被新版本替代，[万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md) 明确提示“推荐使用全面升级的文生图V2版模型”，实际生产环境应优先选用 `wan2.6-t2i` 或 `wan2.7-image`。

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：  
  - 千问系列支持 `宽*高`（如 `"1024*1024"`）或语义值（如 `"2K"`）；  
  - 万相 V2.5+ 支持 `宽*高`，未指定时默认 `1280*1280`（单图输入）或继承最后一张参考图宽高比；  
  - 可灵与 Vidu 支持 `"1K"`/`"2K"`/`"4K"` 等预设档位。  
- **`n`**：生成图像张数，范围通常为 `1–9`（可灵、万相 V2.7），Z-Image 固定为 `1`。  
- **`watermark`**（布尔值）：控制是否添加水印，默认 `true`，部分模型（如 `wan2.7-image-pro`）支持设为 `false`。  
- **`thinking_mode`**（布尔值）：仅 `wan2.7-image-pro` 支持，启用后返回推理过程描述（非图像）。  
- **`element_list`**（可灵）与 **`auxiliary_parameters`**（创意海报）：用于高级控制（主体一致性、分步高清修复），属模型特有参数。

## 使用方式

- **接入协议**：  
  - 推荐使用 **DashScope SDK**（Python/Java），支持同步/异步调用，代码简洁；  
  - **OpenAI 兼容模式** 仅适用于千问系列，需切换 `base_url` 并设置 `model="qwen-image-3.0-pro"`，但**不支持流式或异步**；  
  - **HTTP 直调**：所有模型均支持，但必须注意——  
    - 千问、Z-Image、万相 V2.6+/V2.7 支持 **同步调用**（单请求返回结果）；  
    - 万相 V2.5 及以下、可灵、Vidu、全部创意工具类模型（如虚拟模特、海报生成）**强制异步**，需两步：① `POST /generation` 获取 `task_id`，② 轮询 `/result?task_id=xxx`。  

- **地域与域名**：  
  - 必须确保 API Key、Endpoint、业务空间 ID（`{WorkspaceId}`）三者同地域；  
  - 强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低；该要求在[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)等多份文档中被反复强调。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与 Endpoint **完全不互通**，混用将导致鉴权失败（见文档 5、7、9、10、11、18、19）。  
- **免费额度与限流**：  
  - 多数创意工具类模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`image-erase-completion`）仅限免费体验，额度用尽即不可调用，且**不支持付费开通**；  
  - 所有模型均对 QPS（每秒请求数）与并发任务数设限，例如 `facechain-finetune` 限流为 QPS=2、并发=1（见文档 32）。  
- **输入约束**：  
  - 图像 URL 必须公网可访问、无中文路径（需 URL 编码）、格式为 JPEG/PNG/JPG（可灵不支持透明通道）；  
  - 提示词长度上限因模型而异：可灵为 2500 字符，Vidu 为 5000 字符；  
  - 参考图数量上限：可灵 ≤10 张（含 `element_list` 主体数），Vidu ≤14 张。  
- **模型弃用风险**：万相 V1（`wanx-v1`）、千问早期模型（`qwen-image-2.0` 系列）已进入维护期，新项目应避免依赖；其计费、限流、功能均落后于 V2.6+/V3.0 系列。

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
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


