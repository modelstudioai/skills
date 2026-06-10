# image generation

阿里云百炼平台聚合了多个图像生成与编辑模型，覆盖文生图、图像编辑、图像翻译、局部重绘、扩图、背景生成、虚拟模特、人物写真、创意海报等场景。开发者可通过统一的 DashScope API（HTTP 同步/异步接口或 Python/Java SDK）调用这些能力，按任务类型选择不同端点与模型版本。

## 模型体系概览

### 千问 Qwen-Image 系列

主打**文字渲染**与**图文混排**，支持从 512×512 到 2048×2048 的自由分辨率，单次可生成 1–6 张图像。

| 模型 | 定位 | 说明 |
| --- | --- | --- |
| qwen-image-2.0-pro | 文生图 Pro 系列，文字渲染/真实质感/语义遵循能力最强 | 当前等同 `qwen-image-2.0-pro-2026-04-22`，也可选 `-2026-03-03` 快照 |
| qwen-image-2.0 | 加速版，兼顾效果与速度 | 当前等同 `qwen-image-2.0-2026-03-03` |
| qwen-image-max | 真实感最强，AI 痕迹最低 | 当前等同 `qwen-image-max-2025-12-30`，仅单张输出 |
| qwen-image-plus / qwen-image | 多样化艺术风格 + 文字渲染 | `qwen-image-plus` 等同 `qwen-image-plus-2026-01-09` |

**端点（同步）**：
- 北京：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- 新加坡：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

图像编辑使用同名模型但输入带参考图，详见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)。编辑模型包含 `qwen-image-edit-max`（工业设计/几何推理更强）、`qwen-image-edit-plus`、`qwen-image-edit`，输出 1–6 张 PNG。

### Z-Image 系列

轻量快速文生图模型，支持中英文字渲染，分辨率总像素在 [512×512, 2048×2048] 之间，单次固定 1 张。

| 模型 | 说明 |
| --- | --- |
| z-image-turbo | 快速生图，支持 `prompt_extend=true` 开启智能思考（返回优化提示词与推理过程） |

端点与千问系列同步接口相同，详见 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)。

### 万相 Wan 系列

万相是最早的图像生成家族，包含多代模型，覆盖文生图、图像编辑、涂鸦作画、局部重绘等。

| 模型 | 能力 | 备注 |
| --- | --- | --- |
| wanx-v1 | 文生图 V1，支持中英文 [prompt](../guides/prompt.md)、多种风格、参考图迁移 | 仅北京；推荐升级到 V2 |
| wanx2.6-image / wanx-v2 | 文生图 V2，全面升级，支持多分辨率与风格 | 北京/新加坡/弗吉尼亚 |
| wan2.7-image-pro / wan2.7-image | 2.7 代：文生图、文生组图、图生组图、图像编辑、多图参考；Pro 支持 4K 输出 | 最新一代 |
| wan2.6-image | 2.6 代：图像编辑 + 图文混排输出 | — |
| wan2.5-image-edit | 通用图像编辑 2.5：文本指令编辑单图/多图融合 | — |
| wanx-image-edit | 通用图像编辑（扩图、去水印、风格迁移、修复、美化、上色） | 仅北京 |
| wanx-sketch-to-image-lite | 涂鸦作画：输入线稿+文本生成图像 | 仅北京 |
| wanx-x-painting | 图像局部重绘 | 仅北京；当前仅免费体验，额度用尽即停服，建议迁移至千问图像编辑或万相 2.1 |

万相 V1/V2/局部重绘/涂鸦作画/通用图像编辑的 HTTP 调用详见 [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)、[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)、[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

### 专项能力模型

| 模型 | 场景 | 端点 |
| --- | --- | --- |
| qwen-mt-image | 图像文字翻译，保留排版；支持中/英/日/韩/西/法互译（不可非中英语种直接互译） | `/api/v1/services/aigc/image2image/image-synthesis`（异步） |
| wanx-vary-region | 图像局部重绘 | `/api/v1/services/aigc/image2image/image-synthesis` |
| wanx-image-scaling | 画面扩展（扩图）：按宽高比、按比例或四向扩图，可叠加旋转 | `/api/v1/services/aigc/image2image/out-painting` |
| wanx-virtualmodel / virtualmodel-v2 | 虚拟模特：替换真人/人台图中的模特和背景 | `/api/v1/services/aigc/virtualmodel/generation/` |
| shoemodel-v1 | 鞋靴模特：多视角鞋靴图 + 模特模板 → AI 试穿 | 异步 `/image2image/image-synthesis` |
| wanx-poster-generation-v1 | 创意海报生成（背景+文字排版，多风格） | 异步 |
| image-instance-segmentation | 人物实例分割（像素级 mask） | 异步 |
| wanx-background-generation | 图像背景生成 | `/api/v1/services/aigc/background-generation/generation/` |
| outfitanyone | AI 试衣：试衣模型 + 辅助模型组合 | 异步 |
| image-erase-completion | 图像擦除补全（按 mask 删除人体/物品/文字等） | 异步 |
| facechain | 人物写真：2 张照片训练专属形象，批量生成多风格写真 | 异步 |
| wordart | WordArt 锦书：创意文字变形、艺术纹理、特效艺术字 | 异步 |
| kling/kling-v3-image-generation | 可灵文生图 + 单图参考生图；1k/2k，16:9/9:16/1:1，1–9 张 | `/api/v1/services/aigc/image-generation/generation`（异步） |
| kling/kling-v3-omni-image-generation | 可灵 Omni：多图参考、分镜组图，支持 4K；单图 1–9 / 组图 2–9 | 同上 |

## 通用调用流程

### 1. 准备 API Key

调用任何图像模型前，需先 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并 [配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables) `DASHSCOPE_API_KEY`。通过 SDK 调用需先 [安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Java）。

> **注意**：北京和新加坡地域拥有独立的 API Key 与请求地址，**不可混用**，否则鉴权失败。新加坡地域的旧域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

### 2. 同步 vs 异步

- **同步接口**：千问 Qwen-Image / Z-Image 等新一代模型支持，单次 HTTP 直接返回图像（URL 或 base64）。推荐用于大多数场景。
- **异步接口**：万相 V1/V2、可灵、海报、虚拟模特、鞋靴、局部重绘等耗时较长的模型必须走异步。流程：
  1. 提交任务：请求头 `X-DashScope-Async: enable`，返回 `task_id`（有效期 24 小时）。
  2. 轮询结果：用 `task_id` 反复查询直到 `SUCCEEDED`，取图像 URL。

> **注意**：缺少 `X-DashScope-Async: enable` 请求头会报错 "current user api does not [support](../guides/support.md) synchronous calls"。

### 3. 关键参数模式

| 参数 | 说明 |
| --- | --- |
| `model` | 模型名，如 `qwen-image-2.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-image-generation` |
| `input.prompt` / `input.messages[].content[].text` | 文本提示词（千问/Z-Image 用 messages 多模态结构，可带图像 URL 做编辑） |
| `input.image_url` / `ref_img` | 参考图 URL（公网可达；部分模型支持 base64 或本地上传后的临时 URL） |
| `parameters.size` | 输出尺寸，格式如 `"1024*1024"` 或 `"1:1"`；不同模型取值范围不同 |
| `parameters.n` | 输出张数（1–6 居多，可灵 1–9，组图模式用 `series_amount` 2–9） |
| `parameters.style` | 风格（万相 V1 支持 `<auto>`、摄影、卡通等） |
| `parameters.negative_prompt` | 反向提示词（万相 V1/V2 支持） |
| `parameters.prompt_extend` | Z-Image 智能思考开关 |
| `parameters.seed` | 随机种子 |
| `parameters.mask` / `box` | 局部重绘/擦除用 mask 或边界框 |

### 4. 响应与取图

- 同步接口直接返回图像 URL 或 base64。
- 异步接口返回 `task_id`，需要轮询 `/api/v1/tasks/{task_id}` 直到 `task_status = "SUCCEEDED"`，取 `output.results[].url`（有效期 24 小时）。
- 本地调试建议先用 `curl` + 环境变量，再迁移到 SDK；详见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 限流、计费与额度

- 所有模型按张数或次数计费，具体单价见各文档；部分专项模型（如 `wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-instance-segmentation`、`image-erase-completion`、`wanx-virtualmodel`）**当前仅提供免费体验**，额度用完后停服且不支持付费开通，建议迁移到千问图像编辑或万相 2.7。
- QPS 与并发任务数因模型而异：如 `wanx-v1` 默认 QPS=2、同时处理任务数=1，可申请提额。
- 新用户有 [免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)，各模型独立计算。
- 图像 URL 有效期 24 小时，请及时转存到自己的 OSS 或本地。

## 选型建议

- **通用文生图、文字渲染、图文混排**：首选 `qwen-image-2.0-pro`；追求速度选 `qwen-image-2.0`；追求真实感选 `qwen-image-max`；需要轻量快速选 `z-image-turbo`。
- **图像编辑（增删物体、改动作、风格迁移、多图融合）**：`qwen-image-2.0-pro`（编辑模式）或 `qwen-image-edit-max`（工业设计/几何推理）。
- **4K 高清输出、组图/分镜**：`wan2.7-image-pro` 或 `kling/kling-v3-omni-image-generation`。
- **图像文字翻译**：`qwen-mt-image`（仅中国内地）。
- **电商场景（虚拟模特、鞋靴试穿、AI 试衣、背景生成）**：对应专项模型；注意部分仅免费体验。
- **人物写真、创意海报、艺术字**：FaceChain / `wanx-poster-generation-v1` / WordArt。
- **图像预处理（分割、擦除、扩图、局部重绘）**：`image-instance-segmentation` / `image-erase-completion` / `wanx-image-scaling` / `wanx-x-painting`。
- **第三方模型**：可灵系列（`kling/kling-v3-*`）通过 DashScope 异步接口调用，需单独在控制台开通"可灵AI"模型卡片。

> **注意**：万相 V1 文档明确推荐使用 V2；千问系列迭代较快，文档中"当前等同于"的快照版本会随时间更新，调用时建议确认最新快照名或使用不带日期的别名（如 `qwen-image-2.0-pro`）。可灵模型名带 `kling/` 前缀，与其他 DashScope 模型命名风格不同。

## 来源文档

- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wanx-image-edit-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/portrait-style-redraw-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/vary-region-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/wordart-quick-start.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)


