# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台级调整等关键更新，面向开发者提供可落地的版本演进信息。所有变更均以实际生效时间为准，建议通过控制台监控、API 响应头或事件总线（EventBridge）主动感知变更。模型生命周期管理（如上线/下线）与功能发布遵循独立节奏，需分别关注。

## 支持的模型/功能

- **新模型上线**：2026年7月起密集发布多模态与垂直场景模型，包括 `qwen3.8-max`（2.4T MoE 旗舰）、`qwen3.8-omni-flash-realtime`（实时音视频交互）、`decision-model-preview`（结构化决策）、`qwen-mt-uni`（全模态翻译）等；图像生成类新增 `qwen-image-3.0-pro` 和 `vidu/viduq3-ad_reference2video`（广告专用）；语音方向上线 `qwen-audio-3.0-realtime-plus` 与 `qwen-audio-3.0-tts-plus` 双版本。完整清单详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块扩展**：
  - 知识库 RAG 新增检索服务与问答服务（2026年6月23日）；
  - 智能体托管运行时 API 上线（2026年6月29日），支持会话与工具执行托管；
  - 模型评测新增排行榜与综合评估器（2025年12月15日），覆盖 BLEU、ROUGE、人工分类等维度；
  - 多模态交互开发套件已支持 Linux C++、Android/iOS Lite、RTOS C 等多端 SDK（2026年2–4月）；
  - 模型调优新增强化学习训练（邀约制）、0代码安全合规强化、视频/图像/视觉理解模型类型支持（2026年5月）。

> **注意**：文档2中“2026年7月16日企业知识库（旧）下线通知”与文档3未提及该模块状态，但文档2明确标注其为“旧版”，且文档3未列出任何替代知识库模型，开发者应确认是否已迁移至新版 RAG 服务（见 [知识库RAG](../../raw/application-user-guide/agent-context/knowledge-base/service/rag-knowledge-retrieval.md)）。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`stepfun/step-5-preview`、`glm-5.3`）统一支持 **1M Token** 输入；`deepseek-v4.1-flash` 支持 384K 输出；`qwen3.7-text-embedding-flash` 支持 128K 长文本处理。
- **推理性能**：`glm-5.3-flash` 达 200 tokens/s；`kimi-k2.7-code-highspeed` 输出速度约 180–260 tokens/s；`qwen-audio-3.0-asr-flash-streaming` 专为低延迟实时流式识别优化。
- **部署计费模式**：模型部署 API 自2026年1月23日起支持按模型单元（MU）时长计费，并新增 `qwen-flash`/`qwen-plus` 等预置模型选项（见 [模型部署快速入门](../../raw/model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-quick-start.md)）。

## 使用方式

- **模型调用**：新模型均通过标准 `/v1/chat/completions`（OpenAI 兼容）或 `/v1/messages`（Anthropic 兼容）接口接入；多模态模型（如 `qwen3.8-omni-flash`）支持 `image_url`、`video_url`、`audio_url` 等 content type 扩展字段。
- **异步任务**：Responses API 自2026年6月1日起支持 `background=true` 异步提交，结果通过轮询或事件总线 HTTP 回调/RocketMQ 主动推送（见 [异步任务API](https://help.aliyun.com/zh/model-studio/async-task-api#f9e4c6c88c6ho)）。
- **临时凭证**：敏感环境推荐使用生成临时 API Key 方案（2026年6月3日上线），避免永久密钥泄露（见 [获取临时认证令牌](../../raw/application-api-reference/more/application-obtain-temporary-authentication-token.md)）。
- **模型切换**：若使用待下线模型，须在通知期（快照模型30天、主线模型3个月）内完成测试与切换，参考 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 中的操作建议。

## 限制和注意事项

- **模型下线影响**：自正式下线日起，模型推理服务完全停止；已部署的调优模型不受影响，但**不可新建调优或部署任务**（部分模型可能保留有限调优能力，以下线通知为准）。控制台功能与文档同步移除。
- **限流策略**：下线通知发布后即开始逐步缩减 QPM/TPM，先恢复至默认限流值再递减（见 [默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)）。
- **地域与协议兼容性**：2026年6月12日新增美国、德国、日本地域；2026年6月11日 Coding Plan 联网搜索 MCP 升级为 Streamable HTTP 协议；WebSocket 协议已用于通义听悟 Agent 工业指令转写（2026年5月21日）及实时语音对话（如 `qwen-audio-3.0-realtime-plus`）。
- **版本一致性风险**：文档2中 `qwen3.7-flash` 发布日期标注为“2026-07-21”，而文档3中同名模型出现两次（`qwen3.7-flash` 与 `qwen3.7-flash-2026-07-15`），后者更符合快照命名惯例；建议优先采用带日期后缀的模型 ID（如 `qwen3.7-flash-2026-07-15`）确保确定性。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


