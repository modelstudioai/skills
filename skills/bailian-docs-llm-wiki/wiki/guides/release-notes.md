# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级调整等关键更新，面向开发者提供可操作的版本演进信息。内容覆盖模型生命周期管理（上架/下线）、核心能力扩展（如多模态、Agent、RAG）、API 与部署机制升级，以及计费与权限相关变更。所有变更均以实际生效日期为准，建议开发者定期查阅并及时适配。

## 支持的模型/功能

- **新模型上架**：2026年7–9月密集发布多模态旗舰模型，包括 `qwen3.8-omni-flash`（全模态输入/输出）、`stepfun/step-5-preview`（1M上下文+MoE架构）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s推理速度）、`kling/kling-v3-turbo-video-generation`（极速视频生成）等；语音方向新增 `qwen-audio-3.0-realtime-plus`（双工实时对话）与 `qwen-audio-3.0-tts-plus`（高表现力TTS）；向量与排序模型同步更新，如 `qwen3.7-text-rerank`（Web检索相对提升35%）和 `qwen3.7-text-embedding-flash`（支持128K长文本与Sparse Embedding）。
- **功能模块扩展**：
  - 知识库RAG：6月上线知识检索服务与知识问答服务，支持多知识库联合检索与混合排序 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)；
  - 智能体托管：6月29日上线智能体托管运行时 API，支持平台托管会话与工具执行 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)；
  - 模型调优：5月新增强化学习训练（邀约制）、图像/视频生成模型类型支持，以及0代码安全合规强化流程 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)；
  - 多模态交互：4月起陆续上线 Android/iOS Lite SDK、Linux C++ SDK、RTOS C SDK 及 JSSDK，覆盖端侧全场景接入。

> **注意**：文档3中多次出现同一模型不同命名（如 `kimi/kimi-k3` 与 `kimi-k3`、`glm-5.2` 与 `ZHIPU/GLM-5.2`），实际调用时应以控制台或API返回的 `model_id` 字段为准，避免依赖别名。

## 关键参数

- **上下文窗口**：主流新模型普遍支持 `1M Token` 上下文（如 `qwen3.8-max`、`GLM-5.3`、`step-5-preview`），部分轻量模型如 `qwen3.8-flash` 亦原生支持百万级窗口。
- **输出长度**：`GLM-5.3-FlashX` 支持 `128K` 输出，`deepseek-v4.1-flash` 支持 `384K` 输出，`qwen3.8-max-0902` 延续 `100万上下文 + 思考模式` 组合。
- **性能指标**：`GLM-5.3-FlashX` 推理速度达 `200 tokens/s`；`kimi-k2.7-code-highspeed` 输出速度约 `180–260 tokens/s`；`qwen-audio-3.0-asr-flash-streaming` 支持实时流式识别，端到端延迟优化至低水平。
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 等均原生支持图像/视频/文件输入；`qwen-mt-uni` 支持 PDF/Word/PPT/HTML/Markdown/TXT/图片/音频等多模态输入自动识别与版面还原。

## 使用方式

- **模型调用**：通过标准 `/v1/chat/completions`（OpenAI兼容）或 `/v1/messages`（Anthropic兼容）接口调用，新模型如 `qwen3.8-omni-flash` 同时支持 Function Calling、联网搜索与上下文缓存。
- **异步任务**：Responses API 自6月1日起支持 `background=true` 异步提交，配合事件总线（EventBridge）HTTP回调或 RocketMQ 主动推送完成事件，避免轮询 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型部署**：1月起支持按模型单元（MU）时长计费，API 部署新增 `qwen-flash`/`qwen-plus` 等预置模型选项；6月15日 PTU 部署新增长输入与前缀缓存能力。
- **临时凭证**：6月3日上线生成临时 API Key 文档，适用于不可信环境，规避永久密钥泄露风险 [原文标题](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 限制和注意事项

- **模型下线机制**：快照模型（如 `qwen-max-2025-01-25`）下线前30天通知，主线模型下线前3个月通知；自通知发布日起逐步缩减 QPM/TPM，正式下线后推理服务终止，调优与部署功能同步停用（已部署模型不受影响）[原文标题](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与接入**：6月12日新增美国、德国、日本地域部署，但部分新功能（如 `qwen-mt-uni` 异步翻译）可能暂未在全部地域开放，需以控制台可用性为准。
- **兼容性风险**：`qwen3.8-omni-flash-realtime` 等实时模型依赖 WebSocket/WebRTC/AOQ 协议，旧版 HTTP 轮询客户端无法直接兼容；`qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-realtime-flash` 功能重叠但侧重不同（质量 vs 速度），需按场景选型。
- **计费变更**：`qwen-turbo` 资源包已于6月28日启动退市；`qwen3.7-text-embedding-flash` 等轻量模型虽成本更低，但效果在部分评测任务（如 AIRBench-zh）仅提升约3%，需结合业务精度要求评估性价比。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


