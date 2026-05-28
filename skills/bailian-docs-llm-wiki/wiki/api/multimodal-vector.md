# multimodal vector

多模态向量模型用于将文本、图像和视频映射至统一的语义向量空间，支持跨模态检索、相似度计算与内容聚类分析。开发者可通过百炼 DashScope 接口快速接入，根据业务场景灵活选择独立向量或融合向量生成模式。接口规范与完整参数定义详见 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)。

## 支持的模型与核心能力
### 核心特性
- **跨模态检索**：统一向量空间支持以文搜图、以图搜视频、多图混合查询等场景。
- **语义相似度计算**：输出为 Dense 向量，可直接通过余弦相似度衡量不同模态内容的语义相关性。
- **内容分类与聚类**：基于高维语义表征实现智能打标、分组与聚合分析。

### 模型矩阵
平台提供多款多模态向量化模型，能力定位如下：
- `qwen3-vl-embedding`：默认 2560 维，支持独立/融合向量，支持多 `image` 条目输入，通过参数控制融合行为。
- `qwen2.5-vl-embedding`：默认 1024 维，**仅支持融合向量**（固定返回单向量），不支持独立模式与多图序列。
- `tongyi-embedding-vision-plus` / `flash`（含 2026-03-06 快照版）：快照版基于 Qwen3 底座，支持多分辨率档位、30+ 语种及融合/独立双模式。
- `multimodal-embedding-v1`：固定 1024 维，提供基础跨模态表征能力。
详细维度、语种、配额与成本对照请参阅 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)。构建 [[embedding-models]] 应用时，建议全链路保持模型版本一致以确保向量空间对齐。

## 关键参数说明
HTTP 与 SDK 调用均需遵循以下参数规范：
- `model`（必选）：指定调用的模型名称，需与官方列表严格匹配。
- `input.contents`（必选）：内容数组。支持四种键值对结构：
  - `text`：字符串。
  - `image`：公网 URL 或 Base64 Data URI。
  - `video`：仅支持公网 URL。
  - `multi_images`：图片 URL/Base64 数组（部分模型支持）。
- `parameters.dimension`：自定义输出维度。各模型可选档位不同（如 `qwen3-vl-embedding` 支持 2560~256），部分老模型固定维度，传参将被忽略。
- `parameters.enable_fusion`（bool）：仅 `qwen3-vl-embedding` 适用。设为 `true` 时合并 `contents` 为单向量。
- `parameters.res_level` / `max_video_frames`：仅 `2026-03-06` 快照版支持。分别控制图像分辨率档位（0-3）与视频最大采样帧数（上限 64）。
- `parameters.instruct`：任务提示词（建议英文），可微调下游检索精度。

## 使用方式
### 环境准备
1. 完成 [[api-key]] 获取并注入环境变量。
2. 若使用编程接口，需按指引安装 [[dashscope-sdk]]。

### 调用模式
- **端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding`
- **独立向量**：`contents` 数组每项仅含单一模态，返回向量数量与元素数量一致。
- **融合向量（qwen3）**：附加 `"parameters": {"enable_fusion": true}`，返回长度为 1 的向量数组。
- **融合向量（2026-03-06版）**：在 `contents` 的单对象内同时写入 `text`、`image`、`video` 等键，无需额外开关参数，模型自动融合编码。
完整鉴权头、JSON 报文结构与错误码定义，请参考 [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)。

## 限制与注意事项
- **输入规格**：单次请求 `contents` 元素总数通常上限为 20。视频仅支持公网可访问 URL，单文件大小建议控制在 3~50 MB（依模型而定），编码格式需为 H.264/H.265。
- **模型行为差异**：
  > **注意**：不同模型生成融合向量的触发逻辑存在硬性隔离。`qwen2.5-vl-embedding` 强制融合且拒收 `multi_images`；`qwen3-vl-embedding` 严格依赖 `enable_fusion` 开关；2026-03-06 快照系列则依赖同对象多字段聚合。错误混用参数将导致 `400` 错误或非预期截断，接入前请严格核对目标模型的能力矩阵。
- **计费与配额**：按千输入 Token 计费，文本与视音频单价独立核算。新用户通常享有开通后 90 天内 100 万 Token 的免费额度，超额按量计费。
- **向量检索对接**：生成后的向量可直接导入 [[vector-database]] 或检索引擎进行近似最近邻搜索。跨模型、跨批次或跨语言生成的向量严禁混合计算相似度，必须保证查询向量与索引向量同源同参。

## 来源文档

- [Multimodal-Embedding API详情](../../raw/model-api-reference/multimodal-vector/multimodal-embedding-api-reference.md)

