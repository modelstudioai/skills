# vector and sort

多模态向量模型（Multimodal Embedding）把文本、图片、视频映射到同一语义空间，支持跨模态检索、语义相似度计算与内容聚类。百炼平台通过统一的 HTTP 端点提供该能力，开发者可按需选择独立向量或融合向量模式。完整接口参数与示例见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 支持的模型

北京区域提供 6 款模型，覆盖从轻量到高分辨率的不同场景：

| 模型 | 默认维度 | 向量类型 | 文本上限 | 图片上限 | 视频上限 |
| --- | --- | --- | --- | --- | --- |
| qwen3-vl-embedding | 2560 | 独立 / 融合（`enable_fusion`） | 32,000 Token | 10 MB | 50 MB |
| qwen2.5-vl-embedding | 1024 | 仅融合 | — | 5 MB | — |
| tongyi-embedding-vision-plus-2026-03-06 | 1152 | 独立 / 融合（同 content 对象） | 1,024 Token | 5 MB（最大 10 MB），最多 64 张 | 50 MB |
| tongyi-embedding-vision-flash-2026-03-06 | 768 | 独立 / 融合（同 content 对象） | 1,024 Token | 同上 | 50 MB |
| tongyi-embedding-vision-plus | 1152 | 仅独立 | — | 3 MB，最多 8 张 | 10 MB |
| tongyi-embedding-vision-flash | 768 | 仅独立 | — | 3 MB | 10 MB |
| multimodal-embedding-v1 | 1024 | 固定 | 512 Token | 3 MB | 10 MB |

新加坡区域仅上线 `tongyi-embedding-vision-plus` / `flash` 两款。语种方面，Qwen3 系列支持 30+ 语言，Qwen2.5 支持 11 种，tongyi 老版本只支持中英文。

## 向量类型：独立 vs 融合

- **独立向量**：`contents` 中每一项各自生成 1 个向量，适合逐项对比（以图搜图、以文搜图）。
- **融合向量**：把所有输入融合为 1 个向量，适合"商品图 + 描述文本"这类需要整体语义表征的检索。开启方式因模型而异：
  - `qwen3-vl-embedding`：设置 `parameters.enable_fusion = true`。
  - `qwen2.5-vl-embedding`：始终返回融合向量，无法关闭。
  - `tongyi-embedding-vision-*-2026-03-06`：把 `text` / `image` / `video` 放在**同一个** content 对象中即触发融合（不使用 `enable_fusion`）。
  - `tongyi-embedding-vision-plus` / `flash`（非 2026-03-06 版本）：不支持融合。

融合组合支持：文本+图片、文本+视频、多图+文本、图片+视频+文本混合。

## 关键参数

调用 `POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding` 时，请求体核心字段如下：

- `model`（必选）：模型名称。
- `input.contents`（必选）：内容数组，每项为 `{"text"|"image"|"video"|"multi_images": value}`。图片支持 URL 或 Base64 Data URI，视频必须是 URL。
- `parameters.dimension`：输出维度，仅部分模型支持（qwen3 支持 256/512/768/1024/1536/2048/2560；qwen2.5 支持 512/768/1024/2048；2026-03-06 系列支持 64/128/256/512/768/1024/1152）。`multimodal-embedding-v1` 与 tongyi 老版本固定维度，传此参数会被忽略。
- `parameters.enable_fusion`：仅 `qwen3-vl-embedding` 识别。
- `parameters.res_level`（0/1/2/3）与 `parameters.max_video_frames`（≤64）：仅 2026-03-06 快照版支持，用于控制图像分辨率档位与视频采样帧数；对 IPC/自驾/文档类图像，`res_level=3` 可带来 5%–10% 效果提升。
- `parameters.fps`：视频抽帧比例，范围 [0, 1]，默认 1.0。
- `parameters.instruct`：自定义任务说明（建议英文），可带来 1%–5% 的效果提升，适合 QUERY 侧加意图提示。

请求头需带 `Authorization: Bearer $DASHSCOPE_API_KEY` 与 `Content-Type: application/json`。SDK 调用时 `parameters` 内的字段可直接平铺到顶层。

## 使用方式

前提条件：已获取并配置 API Key 到环境变量 `DASHSCOPE_API_KEY`，SDK 调用需安装 DashScope SDK。典型调用流程：

1. 构造 `contents` 数组，按模态放入 `text` / `image` / `video` / `multi_images` 条目。
2. 按需设置 `parameters`（维度、融合、分辨率、帧数）。
3. 解析响应中的向量，使用余弦相似度等进行下游检索或聚类。

单次请求的条数限制因模型而异：qwen3 限制总条目 ≤20、图片 ≤5、视频 ≤1；2026-03-06 系列总条目 ≤20、图片 ≤64、视频 ≤8；`multimodal-embedding-v1` 总条目 ≤20 且图片/视频各最多 1 条。视频格式统一要求 H.264 / H.265 编码的 MP4/MOV 等常见容器。

> **注意**：文档中关于 qwen2.5-vl-embedding 的视频/文本限制未给出明确数值，仅标注了图片 5 MB 上限；如需处理长文本或大视频，建议优先选用 qwen3-vl-embedding 或 2026-03-06 系列，参数与限制更清晰。更多接口细节见 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)。

## 限制与注意事项

- 所有模态向量位于同一语义空间，可直接跨模态比较，但不同模型输出的维度与归一化方式不同，**不能**跨模型混用向量做相似度。
- `dimension` 参数并非所有模型都支持，传入不支持的模型不会报错但也不会生效，选型时需核对模型能力表。
- 融合向量与独立向量不要混用：同一业务链路内应保持向量类型一致，否则检索结果不可比。
- 视频仅支持 URL 输入，不支持 Base64；图片大小超限或格式不在 JPEG/PNG/WEBP/BMP/TIFF/ICO/DIB/ICNS/SGI 之内会被拒绝。
- 计费按输入 Token 分模态计价，文本与图片/视频单价不同，批量接入前建议结合 [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md) 中的价格表做成本估算。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/vector-and-sort/multimodal-vector/multimodal-embedding-api-reference.md)


