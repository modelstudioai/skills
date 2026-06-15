# vector and sort

百炼平台提供多模态向量模型（Multimodal-Embedding），可将文本、图像和视频转换为同一语义空间中的向量表示。这些向量支持跨模态检索（以文搜图、以图搜视频等）、语义相似度计算和内容分类聚类等场景。所有模态的向量位于统一语义空间，可直接通过余弦相似度进行跨模态匹配。

## 支持的模型

百炼目前提供以下多模态向量模型，各模型在向量维度、输入限制和定价上有所不同。详细参数见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

| 模型 | 默认维度 | 向量类型 | 文本长度 | 图片上限 | 视频上限 | 价格（每千Token） |
|------|---------|---------|---------|---------|---------|-----------------|
| qwen3-vl-embedding | 2560 | 独立/融合 | 32,000 Token | 10 MB | 50 MB | 图片/视频 0.0018元，文本 0.0007元 |
| qwen2.5-vl-embedding | 1024 | 仅融合 | — | 5 MB | — | — |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立/融合 | 1,024 Token | 10 MB（最多64张） | 50 MB | 0.0005元 |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立/融合 | 1,024 Token | 10 MB（最多64张） | 50 MB | 0.00015元 |
| tongyi-embedding-vision-plus | 1152 | 仅独立 | 1,024 Token | 3 MB（最多8张） | 10 MB | 0.0005元 |
| tongyi-embedding-vision-flash | 768 | 仅独立 | 1,024 Token | 3 MB（最多8张） | 10 MB | 0.00015元 |
| multimodal-embedding-v1 | 1024 | 仅独立 | 512 Token | 3 MB | 10 MB | 图片/视频 0.0009元，文本 0.0007元 |

北京和新加坡区域均可用，新加坡仅支持 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash`。

## 向量类型：独立向量与融合向量

多模态向量模型支持两种向量生成方式：

- **独立向量**：为 `contents` 中的每个输入分别生成独立向量。例如输入 1 段文本和 1 张图片，返回 2 个向量。适用于以图搜图、以文搜图等逐项对比场景。
- **融合向量**：将所有输入融合为 1 个向量，实现跨模态综合语义表征。适用于将商品图片和描述文本融合为统一表征进行检索等场景。

不同模型的融合方式有差异：

- `qwen3-vl-embedding`：通过设置 `enable_fusion=true` 参数开启融合模式。
- `tongyi-embedding-vision-plus-2026-03-06` / `flash-2026-03-06`：将 text、image、video 放在同一个 content 对象中即可生成融合向量，不使用 `enable_fusion` 参数。
- `qwen2.5-vl-embedding`：仅支持融合向量，始终返回 1 个融合向量。
- `tongyi-embedding-vision-plus` / `flash` 和 `multimodal-embedding-v1`：仅支持独立向量。

## 关键参数

调用 API 时可通过 `parameters` 对象配置以下参数（完整说明见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)）：

| 参数 | 类型 | 说明 | 适用模型 |
|------|------|------|---------|
| `dimension` | integer | 指定输出向量维度。各模型支持的维度不同 | qwen3-vl-embedding、qwen2.5-vl-embedding、2026-03-06 版本 |
| `enable_fusion` | bool | 是否生成融合向量，默认 false | 仅 qwen3-vl-embedding |
| `fps` | float | 视频帧抽取比例，范围 [0,1]，默认 1.0 | 通用 |
| `instruct` | string | 自定义任务说明，建议英文，可提升 1%-5% 效果 | 通用 |
| `res_level` | integer | 输入分辨率档位（0/1/2/3），默认 1 | 仅 2026-03-06 版本 |
| `max_video_frames` | integer | 视频最大采样帧数，最大 64，默认 8 | 仅 2026-03-06 版本 |

> **注意**：`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash`（非 2026-03-06 版本）不支持 `dimension` 参数，固定返回 1152 / 768 维向量。`multimodal-embedding-v1` 同样不支持，固定返回 1024 维。

## 使用方式

### HTTP 调用

请求端点：

```
POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding
```

请求头需包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。

输入通过 `input.contents` 数组传入，每个元素为包含模态类型键的字典：

- `text`：字符串文本
- `image`：公开 URL 或 Base64 Data URI
- `video`：公开 URL
- `multi_images`：图片 URL 数组（仅部分模型支持）

独立向量示例：

```json
{
  "model": "tongyi-embedding-vision-plus",
  "input": {
    "contents": [
      {"text": "多模态向量模型"},
      {"image": "https://example.com/image.jpg"},
      {"video": "https://example.com/video.mp4"}
    ]
  }
}
```

融合向量示例（qwen3-vl-embedding）：

```json
{
  "model": "qwen3-vl-embedding",
  "input": {
    "contents": [
      {"text": "商品描述文本"},
      {"image": "https://example.com/image.png"}
    ]
  },
  "parameters": {
    "enable_fusion": true
  }
}
```

### SDK 调用

调用前需获取 API Key 并配置环境变量，同时安装 DashScope SDK。SDK 调用时 `parameters` 中的参数可直接作为顶层参数传入。

## 输入格式与限制

各模型对输入格式、支持语种和单次请求条数有不同限制：

- **qwen3-vl-embedding**：支持 33 种语言；图片格式包括 JPEG、PNG、WEBP、BMP 等（URL 或 Base64）；视频支持 MP4、AVI、MOV（仅 URL）；单次请求内容元素总数不超过 20，图片不超过 5，视频不超过 1。
- **qwen2.5-vl-embedding**：支持 11 种语言；图片、文本、视频、融合对象每种类型最多 1 次。
- **2026-03-06 版本**：支持 30+ 种语言；图片格式同 qwen3-vl-embedding；视频格式更丰富（MP4、MPEG、MOV、WEBM、AVI 等）；单次请求最多 20 个元素、64 张图片、8 个视频。
- **tongyi-embedding-vision-plus/flash**（旧版）：仅支持中英文；图片格式 JPG、PNG、BMP；无明确条数限制，受 Token 上限约束。
- **multimodal-embedding-v1**：仅支持中英文；单次请求最多 20 条，图片和视频各最多 1 条。

更多细节和完整的响应格式说明，参见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 模型选型建议

- **追求最高精度和多语言支持**：选择 `qwen3-vl-embedding`，支持 33 种语言、最大 2560 维向量、独立和融合两种模式。
- **需要灵活维度和成本平衡**：`tongyi-embedding-vision-plus-2026-03-06` 支持 6 种维度和多分辨率档位，价格仅 0.0005 元/千Token。
- **追求极致性价比**：`tongyi-embedding-vision-flash-2026-03-06` 价格 0.00015 元/千Token，适合大规模向量化场景。
- **仅需融合向量的简单场景**：`qwen2.5-vl-embedding` 始终返回融合向量，使用最简单。
- **图像分辨率敏感场景**（如 IPC、自动驾驶、视觉文字识别）：使用 2026-03-06 版本并设置 `res_level=3`，可提升 5%-10% 效果。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)






