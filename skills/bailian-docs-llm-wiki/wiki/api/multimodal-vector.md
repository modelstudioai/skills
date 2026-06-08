# multimodal vector

多模态向量模型（Multimodal Embedding）将文本、图像和视频转换为同一语义空间中的向量表示，支持跨模态检索、内容分类和语义相似度计算。所有模态的向量位于同一语义空间，可通过余弦相似度等方法直接进行跨模态匹配与比较。

## 核心能力

- **跨模态检索**：以文搜图、以图搜视频、以图搜图等跨模态语义搜索
- **语义相似度计算**：在统一向量空间中衡量不同模态内容间的语义相似性
- **内容分类与聚类**：基于语义向量进行智能分组、打标和聚类分析

## 向量类型

根据 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)，多模态向量模型支持两种向量生成方式：

### 独立向量

为 `contents` 中的每个输入（文本、图片、视频、多图）分别生成独立向量。例如输入 1 段文本和 1 张图片，返回 2 个独立向量。适用于以图搜图、以文搜图等逐项对比场景。

### 融合向量

将 `contents` 中所有输入融合为 1 个向量，实现跨模态综合语义表征。适用于将商品图片和描述文本融合为统一表征进行检索等场景。支持以下融合组合：

- 文本 + 图片
- 文本 + 视频
- 多图 + 文本
- 图片 + 视频 + 文本混合融合

不同模型的融合方式不同：

| 模型 | 融合方式 |
|------|---------|
| `qwen3-vl-embedding` | 设置 `enable_fusion=true` |
| `qwen2.5-vl-embedding` | 始终返回融合向量（仅支持融合） |
| `tongyi-embedding-vision-plus-2026-03-06` / `flash-2026-03-06` | 将 text、image、video 放在同一个 content 对象中 |
| `tongyi-embedding-vision-plus` / `flash` | 仅支持独立向量 |

## 支持的模型

根据 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md) 中的模型概览，北京区域可用模型如下：

| 模型名称 | 默认维度 | 可选维度 | 向量类型 | 文本长度 | 图片限制 | 视频限制 |
|---------|---------|---------|---------|---------|---------|---------|
| `qwen3-vl-embedding` | 2560 | 2048/1536/1024/768/512/256 | 独立/融合 | 32K Token | ≤5MB | ≤50MB |
| `qwen2.5-vl-embedding` | 1024 | 2048/768/512 | 仅融合 | 32K Token | ≤5MB | ≤50MB |
| `tongyi-embedding-vision-plus-2026-03-06` | 1152 | 1024/512/256/128/64 | 独立/融合 | 1K Token | ≤5MB(建议),≤10MB(最大),≤64张 | ≤50MB |
| `tongyi-embedding-vision-flash-2026-03-06` | 768 | 512/256/128/64 | 独立/融合 | 1K Token | 同上 | ≤50MB |
| `tongyi-embedding-vision-plus` | 1152(固定) | — | 仅独立 | 1K Token | ≤3MB,≤8张 | ≤10MB |
| `tongyi-embedding-vision-flash` | 768(固定) | — | 仅独立 | 1K Token | ≤3MB,≤8张 | ≤10MB |
| `multimodal-embedding-v1` | 1024(固定) | — | 独立 | 512 Token | ≤3MB | ≤10MB |

新加坡区域仅支持 `tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash`。

## 关键参数

### 请求参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型名称 |
| `input.contents` | array | 是 | 待处理内容列表，支持 `text`/`image`/`video`/`multi_images` 四种模态 |
| `parameters.dimension` | integer | 否 | 输出向量维度，不同模型支持范围不同 |
| `parameters.enable_fusion` | bool | 否 | 是否生成融合向量，仅 `qwen3-vl-embedding` 支持 |
| `parameters.fps` | float | 否 | 视频帧采样比例，范围 [0,1]，默认 1.0 |
| `parameters.instruct` | string | 否 | 自定义任务说明，建议英文，通常可提升 1%–5% 效果 |
| `parameters.res_level` | integer | 否 | 分辨率档位 0/1/2/3，仅 2026-03-06 版本支持 |
| `parameters.max_video_frames` | integer | 否 | 视频最大采样帧数，最大 64，默认 8，仅 2026-03-06 版本支持 |

### 输入格式

- **文本**：`{"text": "字符串"}` 或直接传入字符串
- **图片**：`{"image": "URL或Base64 Data URI"}`
- **视频**：`{"video": "公开可访问URL"}`（仅支持 URL）
- **多图**：`{"multi_images": ["URL1", "URL2", ...]}`（仅部分模型支持）

## 使用方式

API 端点：

```
POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding
```

### 独立向量示例

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "tongyi-embedding-vision-plus",
        "input": {
            "contents": [ 
                {"text": "多模态向量模型"},
                {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"}
            ]
        }
    }'
```

### 融合向量示例（qwen3-vl-embedding）

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "qwen3-vl-embedding",
        "input": {
            "contents": [
                {"text": "商品描述文本"},
                {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"}
            ]
        },
        "parameters": {
            "enable_fusion": true
        }
    }'
```

### 融合向量示例（2026-03-06 版本）

2026-03-06 版本通过将多个模态放在同一个 content 对象中实现融合：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
        "model": "tongyi-embedding-vision-plus-2026-03-06",
        "input": {
            "contents": [
                {
                    "text": "视觉多模态表征模型",
                    "image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
                }
            ]
        },
        "parameters": { "dimension": 1152 }
    }'
```

## 限制和注意事项

- 调用前需获取 API Key 并配置到环境变量；如使用 SDK 调用还需安装 DashScope SDK。
- `multimodal-embedding-v1` 不支持 `dimension` 参数，固定返回 1024 维向量。
- `qwen2.5-vl-embedding` 仅支持融合向量，不支持独立向量和多图输入。
- `multi_images` 类型仅 `tongyi-embedding-vision-plus`/`flash` 及其 2026-03-06 版本支持。
- 视频输入仅支持 URL 方式，不支持 Base64。
- 对于图像分辨率敏感的场景（IPC/自驾/视觉文字等），2026-03-06 版本设置 `res_level=3` 可提升 5%–10% 效果。
- 各模型的单次请求条数限制不同，详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md) 中的输入格式说明。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)




