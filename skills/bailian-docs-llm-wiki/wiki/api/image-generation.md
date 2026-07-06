# image generation

百炼平台图像生成类 API 汇总了通义千问、万相、Z-Image、可灵等自研模型，以及一批面向电商、营销、人像场景的创意图像工具。所有接口均通过百炼模型推理网关以 OpenAI 兼容或 DashScope 原生协议调用，统一使用 `Authorization: Bearer <API_KEY>` 鉴权，输入输出以 JSON 承载，部分能力支持流式与异步轮询。

## 能力全景

按模型族与用途可分为四组：

| 分组 | 代表接口 | 主要能力 |
| --- | --- | --- |
| 通义千问图像 | 千问-文生图、千问-图像编辑、千问-图像翻译 | 文生图、图像编辑、图文翻译 |
| 万相图像 | 万相-文生图 V1/V2、万相-图像生成与编辑 2.6/2.7、万相-通用图像编辑 2.5、万相-通用图像编辑、万相-涂鸦作画、万相-图像局部重绘 | 通用文生图、[多模态](../concepts/multimodal.md)编辑、局部重绘、涂鸦生图 |
| 第三方/自研大模型 | Z-Image、可灵-图像生成 | 高质量文生图、艺术风格 |
| 创意工具 | 人像风格重绘、虚拟模特、鞋靴模特、图像画面扩展、创意海报、人物实例分割、AI 试衣 OutfitAnyone、图像背景生成、图像擦除补全、人物写真 FaceChain、创意文字 WordArt 锦书 | 垂类业务化图像处理 |

## 通义千问图像

通义千问图像能力由 Qwen-Image 系列模型提供，统一在 `qwen-image` 模型族下，按任务区分模型名：

- **千问-文生图**：输入中文/英文 [prompt](../guides/prompt.md) + 可选参考图，输出 1024×1024 等多尺寸图像，支持中文原生理解、双语 [prompt](../guides/prompt.md)、长宽比与风格控制。
- **千问-图像编辑**：在保留原图主体与构图的前提下，按自然语言指令做局部修改（换背景、改服饰、增减物体等），支持蒙版与参考图。
- **千问-图像翻译**：面向漫画/图文场景，识别图中文字并翻译为目标语言，同时重绘文字区域以保持视觉一致性。

调用入口通常为 `https://dashscope.aliyuncs.com/compatible-mode/v1/images/generations`（OpenAI 兼容）或 DashScope 原生 `services/aigc/text2image/image-synthesis` 路径，`model` 字段填具体模型名（如 `qwen-image-edit`）。

## 万相图像

万相（Wan）是百炼自研的图像与视频生成模型族，迭代到 2.7 版本，是接口数量最多的一组：

### 文生图

- **万相-文生图 V1**：经典版，支持中文 [prompt](../guides/prompt.md)、尺寸、风格、负面词。
- **万相-文生图 V2**：升级版，画质与中文语义理解提升，支持更多长宽比与参考图引导。

### 生成与编辑一体

- **万相-图像生成与编辑 2.6 / 2.7**：同一接口兼顾文生图与图像编辑，2.7 在编辑自然度、文字渲染、多图融合上进一步优化，是当前推荐的通用版本。
- **万相-通用图像编辑 2.5 / 通用图像编辑**：聚焦"按指令改图"的编辑专用版本，2.5 为较新迭代。

### 局部与创意编辑

- **万相-图像局部重绘（Vary Region）**：指定区域 + [prompt](../guides/prompt.md) 做局部重绘，常用于换物、修复。
- **万相-涂鸦作画**：以用户涂鸦/草图 + [prompt](../guides/prompt.md) 引导生成结构化图像。
- **万相-通用图像编辑（旧）**：早期版本，建议迁移到 2.5+。

万相接口大多走 DashScope 原生异步协议：`POST /services/aigc/text2image/image-synthesis` 返回 `task_id`，再轮询 `GET /tasks/{task_id}` 取结果；文生图 V2 等也提供兼容模式同步调用。

## Z-Image 与可灵

- **Z-Image**：自研高质量文生图大模型，擅长艺术风格、复杂构图与中文语义，适合营销与设计场景。
- **可灵-图像生成**：由可灵团队提供的高美感文生图能力，接入百炼网关统一调用。

二者均以文生图为主，参数聚焦于 [prompt](../guides/prompt.md)、负面词、尺寸与采样控制。

## 创意图像工具

这一组把图像模型封装成业务化接口，输入通常是商品图/人像图 + 简单参数，输出业务可用成图：

| 接口 | 典型用法 |
| --- | --- |
| 人像风格重绘 | 把人像转为指定风格（油画、动漫、3D 等） |
| 虚拟模特 | 商品图 + 模特参数生成虚拟模特穿着图 |
| 鞋靴模特 | 鞋类商品上脚/上模特展示图 |
| 图像画面扩展（Image Scaling） | 扩展画幅、补全边缘 |
| 创意海报生成 | 文案 + 主体图生成营销海报 |
| 人物实例分割 | 抠取人物前景，供后续合成 |
| AI 试衣 OutfitAnyone | 人像 + 服装图生成试穿图 |
| 图像背景生成 | 商品/主体 + 描述生成新背景 |
| 图像擦除补全 | 擦除指定区域并智能补全 |
| 人物写真 FaceChain | 多张人像生成个性化写真集 |
| 创意文字 WordArt 锦书 | 艺术字、文字排版生成 |

这些接口多走 DashScope 原生协议，部分需要先开通对应模型，再以 `model` 字段区分。

## 调用约定

1. **鉴权**：所有接口在请求头携带 `Authorization: Bearer ${API_KEY}`，API_KEY 在百炼控制台"API-KEY 管理"获取。
2. **协议选择**：
   - OpenAI 兼容模式：`https://dashscope.aliyuncs.com/compatible-mode/v1/...`，适合千问文生图等。
   - DashScope 原生模式：`https://dashscope.aliyuncs.com/api/v1/services/aigc/...`，适合万相异步任务、创意工具。
3. **同步 vs 异步**：创意工具与万相多数为异步——提交任务得 `task_id`，按建议间隔轮询 `GET /api/v1/tasks/{task_id}`，状态为 `SUCCEEDED` 后取 `output.results`。
4. **图片传输**：输入图支持公网 URL 或 Base64（需 `data:image/...;base64,` 前缀），输出图一般为临时 URL，需及时下载或转存到 OSS。
5. **尺寸与长宽比**：各模型支持的尺寸集合不同，超范围会报错；万相 V2、千问等支持按 `size` 或 `parameters.size` 指定。
6. **内容安全**：所有接口内置内容安全审核，违规 [prompt](../guides/prompt.md) 或图片会被拒绝并在响应中返回对应错误码。

## 通用错误码

| HTTP / 错误码 | 含义 | 处理建议 |
| --- | --- | --- |
| 400 InvalidParameter | 参数缺失或非法 | 校验 `model`、`input`、`parameters` 结构 |
| 401 AccessDenied | API_KEY 无效或无权限 | 重新获取 KEY 并确认已开通对应模型 |
| 429 Throttling | QPS/并发超限 | 退避重试或申请提配额 |
| 409 DataInspectionFailed | 内容安全拦截 | 修改 [prompt](../guides/prompt.md)/图片后重试 |
| 任务状态 `FAILED` | 异步任务失败 | 查看 `output.message` 定位原因 |

## 选型建议

- **纯中文文生图、追求语义准确**：优先千问-文生图或万相-文生图 V2。
- **按指令改图（编辑）**：万相-图像生成与编辑 2.7 > 通用图像编辑 2.5；细粒度局部改图用图像局部重绘。
- **高美感/艺术风格**：Z-Image、可灵-图像生成。
- **电商/营销垂类**：虚拟模特、鞋靴模特、AI 试衣、创意海报、图像背景生成。
- **人像玩法**：人像风格重绘、人物写真 FaceChain。
- **图像后处理**：画面扩展、擦除补全、人物实例分割。
- **艺术文字**：创意文字 WordArt 锦书。

新接入建议直接使用最新版本（万相 2.7、通用图像编辑 2.5 等），旧版接口保留兼容但不再增强。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)









