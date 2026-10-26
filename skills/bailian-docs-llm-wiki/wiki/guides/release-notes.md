# release notes

百炼平台的 Release Notes 汇总了近期模型上架、功能迭代、平台能力升级及下线机制等关键变更，面向开发者提供可操作的版本演进信息。本文档聚焦于**已发布可用**的模型与功能，不包含预览或邀约制未开放能力；所有模型均默认支持华北2（北京）地域，其他地域支持情况请参考 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 支持的模型/功能

截至 2026 年 10 月下旬，平台新增以下核心模型类别：

- **多模态大语言模型（MLLM）**：`MiniMax/MiniMax-M3.1-Flash`（1M 上下文，五档思考深度，原生支持文本/图片/视频）、`xiaomi/mimo-v2.6-pro-ultraspeed`（10 倍输出加速，1M 上下文，文本/图片/视频/音频全模态）、`deepseek-v4.1-flash-1017`（MoE 552B，Terminal-Bench 4.0 等基准显著提升，支持“许愿式”编程）、`qwen3.8-omni-flash-realtime`（实时音视频交互，支持 WebSocket/WebRTC/AOQ）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s，1M 上下文，128K 输出）。
- **图像生成模型**：`qwen-image-2.1-turbo`（轻量高性价比，生成与编辑一体化）、`qwen-image-3.0-pro`（4.5k token 输入，10px 小字精准渲染，报纸/分镜等复杂版面支持）、`vidu/viduq3-drama_reference2video`（精品剧/AI漫剧专用，强一致性与动效）。
- **视频生成模型**：`kling/kling-v3-turbo-video-generation`（文生/图生视频，多镜头生成）、`wan3.0-video-prime`（30 秒高速生成，四模态全能参考）、`pixverse/pixverse-motioncontrol`（动作迁移）、`vidu/viduq3-ad_reference2video`（广告专用，商品图直出 16 秒视频）。
- **专用模型**：`decision-model-preview`（结构化决策，支持分类/是非判断/评分+概率分布）、`happyoyster-1.0-adventure`（开放式世界模型，文本/图像驱动实时探索）、`qwen-mt-uni`（多模态翻译，支持 PDF/Word/PPT/图片/音频输入，自动版面还原与语音克隆）。

> **注意**：文档 1 中 `kimi/kimi-k3`（2026-07-17）与 `kimi-k3`（2026-08-19）为同一模型，但后者描述中称其为“全球首个开源的 3 万亿级别模型”，而前者未提“开源”属性；实际发布状态以 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新条目为准，开发者应以控制台模型广场显示的标签（如 `open-source`）为依据。

## 关键参数

各模型共性关键参数如下（具体值以模型文档为准）：

- **上下文窗口**：主流 MLLM 普遍支持 **1,000,000 tokens**（如 `qwen3.8-max`、`glm-5.3`、`stepfun/step-5-preview`），部分轻量模型为 262,144（如 `qwen-audio-3.1-realtime-plus`）或 32K–128K（如 `qwen3.7-text-embedding-flash`）。
- **最大输出长度**：范围从 128K（`GLM-5.3-FlashX`）到 384K（`deepseek-v4.1-flash` 系列）。
- **多模态输入支持**：文本为必选；图像/视频/音频支持因模型而异，需查阅具体模型文档；`qwen3.8-omni-flash` 明确支持文本/图片/音频/视频输入，`qwen-mt-uni` 支持文档类文件（PDF/Word 等）输入。
- **推理速度**：`xiaomi/mimo-v2.6-pro-ultraspeed` 声称输出速度提升约 10 倍；`ZHIPU/GLM-5.3-FlashX` 达 200 tokens/s；`MiniMax/MiniMax-M3.1-Flash` 约 170 tokens/s。

## 使用方式

- **API 调用**：所有模型均通过统一推理 API 接入，兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/v1/messages`）协议；多模态输入需按 `multipart/form-data` 或 base64 编码传递；实时语音/视频模型需使用 WebSocket 或 WebRTC 协议（见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)）。
- **模型部署**：支持 PTU 预置吞吐部署（含长输入与前缀缓存能力，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）；图像/视频生成模型支持异步调用（`background=true`）。
- **功能集成**：多模态翻译、重排序、向量嵌入等模型已封装为独立服务（如 `qwen3.7-text-rerank`、`qwen3.7-text-embedding-flash`），可通过对应 API 直接调用；Managed Agent、Skill 能力包、数据连接模块等平台级功能需在应用层配置启用。

## 限制和注意事项

- **模型下线策略**：快照模型（含日期后缀，如 `qwen3.8-max-2026-09-02`）下线前 **30 天**通知；主线模型（如 `qwen3.8-max`）下线前 **3 个月**通知；下线后 API 将不可用，已部署实例不受影响（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **地域与协议限制**：实时语音/视频模型（如 `qwen-audio-3.0-realtime-plus`、`qwen3.8-omni-flash-realtime`）当前仅限华北2（北京）地域，且必须使用指定协议（WebSocket/WebRTC）；部分新模型（如 `decision-model-preview`）可能处于灰度阶段，需申请开通。
- **输入格式约束**：图像/视频生成模型普遍限制参考图数量（如 `vidu` 系列为 0–14 张）；多模态翻译模型对 PDF/Word 文件大小与页数有隐式限制（建议 ≤50MB / ≤100 页）；`qwen-mt-image-2.0` 仅支持 55 种语言互译，不支持方言。
- **成本与性能权衡**：`qwen3.8-flash` 与 `qwen3.8-max` 虽同属 Qwen3.8 系列，但前者侧重高并发低延迟，后者侧重长程任务与极致智能；开发者应基于场景选择，避免在简单对话中误用 `qwen3.8-max` 导致成本上升。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


