# model inference

百炼平台提供覆盖文本、视觉、音频、视频及3D的多模态模型推理服务，支持同步流式、异步任务与端到端交互。开发者可根据延迟、成本与精度需求选择旗舰或轻量模型，并通过标准 HTTP REST API 或 WebSocket 协议快速集成。本文档梳理各模态核心能力、关键参数、调用方式及集成限制。

## 支持的模型与功能

| 模态方向 | 推荐模型/系列 | 核心能力 | 交叉链接 |
|:---|:---|:---|:---|
| **文本生成** | `qwen3.7-max`、`qwen3.6-plus`/`flash` | 长上下文（100万 Token）、Function Calling、内置工具、结构化输出、批量推理。详见 [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)。 | [[text-generation]] |
| **视觉理解** | `qwen3.6-plus`、`qwen-vl-ocr` | 图像/视频分析（最长2小时）、OCR提取、结构化 JSON 输出、最高 16M 像素分辨率。 | [[vision-understanding]] |
| **图像/视频生成** | `wan2.7-image-pro`、`happyhorse-1.0-t2v/i2v` | 文生图（4096x4096）、多图参考编辑、首尾帧生视频、参考一致性视频生成，最长 15 秒。 | [[image-video-generation]] |
| **音频处理** | `cosyvoice-v3.5-plus`（TTS）、`fun-asr`（ASR）、`fun-music-v1`（音乐） | 标准合成/声音设计、实时转写、说话人分离、歌词/Prompt 驱动音乐生成。 | [[speech-processing]] |
| **全模态与 S2S** | `qwen3.5-omni` 系列 | 端到端语音对话、音视频内容分析、实时同传（60种语言）、支持工具调用与联网搜索。详见 [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)。 | [[omni-s2s]] |
| **向量与重排序** | `text-embedding-v4`、`qwen3-vl-embedding`、`qwen3-rerank` | 文本/跨模态向量检索、RAG 精度优化（融合向量 vs 独立向量）、多模态 Top-N 重排。 | [[embedding-rerank]] |
| **3D 生成** | `Tripo/Tripo-H3.1`、`Tripo-P1.0` | 文生/单图生/多图生 3D 模型，支持 GLB 导出与 PBR 贴图精度控制。 | [[tripo-3d]] |

## 关键参数

- **异步/流式控制**：
  - 异步任务（如 3D 生成、长音频处理）需添加请求头 `X-DashScope-Async: enable`。
  - 音频/音乐[[streaming-output|流式输出]]需添加 `X-DashScope-SSE: enable`。
- **思考/推理模式**：通过 `enable_thinking`（Chat API）或 `reasoning.effort`（Responses API）开启，适用于数学推导、代码调试等复杂场景。Qwen3 及以上系列普遍支持，但思考模式下**不输出语音**。
- **多模态输入互斥**：Tripo 3D 模型中 `[[prompt|prompt]]`（文本）、`image`（单图）、`images`（多图列表）三字段互斥，单次请求仅可传其一。音乐生成中 `lyrics` 与 `[[prompt|prompt]]` 至少提供一个，同时传入时 `[[prompt|prompt]]` 会被忽略。
- **视觉 Token 计算**：图像输入 Token 消耗公式为 `h x w / (32 x 32) + 2`，高分辨率将显著增加上下文长度与成本。
- **音频/视频规格**：实时 ASR 支持 8kHz/16kHz 二进制流输入；非实时音频上限 12 小时 / 2GB；视频理解上限 1~2 小时（视模型而定）。

## 使用方式

1. **协议选择**：
   - **WebSocket**：适用于实时语音对话、实时字幕、语音助手等低延迟交互场景。模型名通常带 `-realtime` 后缀。
   - **HTTP REST**：适用于文件转写、长视频分析、批量生成、S2S 文件模式等对延迟容忍度较高的场景。
2. **SDK 集成**：官方提供 Python/Java SDK 原生支持文本、视觉及 CosyVoice/Fun-ASR 的 WebSocket 流式接入；Android/iOS SDK 仅支持部分实时语音模型。其余场景需直接对接 HTTP/WebSocket 协议。
3. **[[async-task-processing|异步任务处理]]**：创建任务后返回 `task_id`，需通过 `GET /tasks/{task_id}` 轮询状态（`PENDING` → `RUNNING` → `SUCCEEDED/FAILED`）。建议设置 10~15 秒轮询间隔，或配置 Webhook 回调替代轮询。

## 限制与注意事项

> **注意**：旧版模型迁移提示。`qwen-omni-turbo`、旧版 Qwen-VL、Qwen-TTS（按 Token 计费）及部分 Paraformer 模型已停止更新或计划下线。新项目请优先采用 Qwen3.5 / Qwen3.6 系列，并前往模型广场核对最新计费与规格。

> **注意**：能力互斥限制。在 Qwen3.5-Omni 全模态场景中，**联网搜索与 Function Calling 不可同时开启**；实时 WebSocket 模型（含 Livetranslate）不支持 Function Calling；思考模式下模型将逐步推理，期间不生成语音输出。

> **注意**：地域与有效期约束。Tripo 3D 生成服务仅限中国内地（北京）地域调用，必须使用对应地域的 API Key。异步任务 `task_id` 查询有效期为 24 小时，3D 生成通常需数分钟，请合理配置重试与超时策略。

> **注意**：分辨率与成本权衡。视觉模型单图最高支持 16M 像素，但 Token 消耗随分辨率非线性增长；视频生成模型最高输出 15 秒/1080P，若需长视频需通过首尾帧模型分段拼接实现。

## 来源文档

- [视觉理解](../../raw/model-user-guide/model-inference/vision-model.md)
- [文本生成](../../raw/model-user-guide/model-inference/text-generation-model.md)
- [图片生成与编辑](../../raw/model-user-guide/model-inference/image-model.md)
- [视频生成与编辑](../../raw/model-user-guide/model-inference/video-generate-edit-model.md)
- [Tripo 3D模型生成](../../raw/model-user-guide/model-inference/tripo-3d-generation-guide.md)
- [语音合成](../../raw/model-user-guide/model-inference/tts-model.md)
- [音乐生成](../../raw/model-user-guide/model-inference/fun-music.md)
- [语音识别](../../raw/model-user-guide/model-inference/asr-model.md)
- [语音转语音](../../raw/model-user-guide/model-inference/s2s-model.md)
- [向量与重排序](../../raw/model-user-guide/model-inference/embedding-rerank-model.md)
- [全模态](../../raw/model-user-guide/model-inference/omni.md)

