# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」及时获取最新动态。本文档结构化呈现核心信息，便于快速定位适配要点。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态大模型：`qwen3.8-max`（2.4T MoE）、`deepseek-v4.1-flash`（552B MoE）、`ZHIPU/GLM-5.3-Flash`（320B）、`kimi-k3`（2.8T）；  
  - 视觉与图像生成：`qwen-image-3.0-pro`、`vidu/viduq3-drama_reference2video`、`pixverse/pixverse-motioncontrol`；  
  - 语音全栈：`qwen-audio-3.0-asr-flash-streaming`（实时ASR）、`qwen-audio-3.0-tts-plus`（高质量TTS）、`qwen-audio-3.0-realtime-plus`（双工语音）。  
- **功能模块上线**：  
  - 知识库RAG新增[知识检索服务](raw/model-user-guide/knowledge-base/rag-knowledge-retrieval.md)与[知识问答服务](raw/model-user-guide/knowledge-base/rag-knowledge-qa.md)（2026-06-23）；  
  - 智能体托管运行时API上线（2026-06-29），支持会话与工具执行全托管；  
  - Responses API 新增异步调用模式（`background=true`），适用于长耗时任务（2026-06-01）；  
  - 模型调优新增强化学习训练（邀约制）、视频生成模型类型支持、0代码安全合规强化（2026-05）。

> **注意**：文档2中列出的 `kimi/kimi-k3`（2026-08-17）与 `kimi-k3`（2026-08-19）为同一模型不同发布日期快照，实际能力一致，但后者为最终正式版；开发者应以[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)中最新日期条目为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`glm-5.3`、`kimi-k3`）统一支持 **1M token** 输入；部分Flash轻量模型（如 `qwen3.8-flash`）同样支持1M，但输出延迟更低。  
- **输出长度**：`qwen3.8-max` 支持最大 384K 输出；`ZHIPU/GLM-5.3-Flash` 支持 128K；`kling/kling-v3-turbo-video-generation` 固定音画同出，无显式token限制。  
- **多模态能力**：`qwen3.8-flash`、`GLM-5.3-Flash`、`kimi-k3` 均原生支持图像输入与视觉理解；`pixverse/pixverse-v6-r2v-omni` 支持视频+图片混合输入。  
- **部署单位**：模型部署支持按「模型单元（MU）」计费（2026-01-23上线），性能可调，稳定性高，详见[模型部署入门](../../raw/model-user-guide/model-deployment-1/model-deployment-quick-start.md)。

## 使用方式

- **模型调用**：  
  - 兼容 OpenAI (`/v1/chat/completions`) 与 Anthropic (`/v1/messages`) 协议的模型（如 `qwen3.8-flash`）可直接复用现有 SDK；  
  - 视频/图像类模型需使用专用 API（如 `POST /api/v1/video/generate`），参见各模型[官方API参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)。  
- **功能接入**：  
  - 新增 Skill 能力包（2026-06-10）：通过[Skill 接入文档](../../raw/application-user-guide/skill/introduction-to-skill.md)添加官方或自定义技能；  
  - 数据连接模块（2026-06-10）：支持 MySQL/语雀/OSS 等数据源，配置入口在应用后台「数据连接」；  
  - 多模态翻译 API 已覆盖文本/图片/文档/网页四类场景，详见[通义多模态翻译 API 参考](../../raw/application-user-guide/application-gallery/official-application-tongyi-translate/tongyi-translate-api-reference/api-anytrans-2025-07-07-dir.md)。  
- **模型迁移**：若使用待下线模型，须在通知期完成替代测试与切换。推荐通过[模型监控](https://bailian.console.aliyun.com/model/telemetry)识别存量调用，并优先选用同系列 Flash/Plus 版本（如 `qwen3.7-flash` 替代 `qwen3.6`）。

## 限制和注意事项

- **模型下线机制**：  
  - 快照模型（如 `qwen-max-2025-01-25`）下线前 **30天** 通知；主线模型（如 `qwen3.8-max`）下线前 **3个月** 通知；  
  - 下线后：推理服务立即终止；新调优/部署禁止；已部署模型不受影响；控制台与文档同步移除。详情请严格参照[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。  
- **功能兼容性**：  
  - `企业知识库（旧）` 已于 2026-07-16 下线，必须迁移至新版知识库；  
  - `qwen-turbo` 资源包已于 2026-06-28 启动退市，存量资源包到期后不可续订；  
  - `Managed Agent` 自 2026-07-16 起商业化，免费额度不再适用。  
- **地域与协议**：  
  - 新增美国、德国、日本地域（2026-06-12），但部分模型（如 `vidu` 系列）暂未全地域部署，调用前需确认[地域支持列表](../../raw/model-user-guide/get-started-with-models/regions.md)；  
  - 异步任务推荐使用事件总线 HTTP 回调或 RocketMQ 主动推送（2026-04-23），避免轮询增加客户端复杂度。  

> **注意**：文档3中「2026年7月」条目提及「部分老旧长尾模型下线通知」（2026-07-09）与文档1中「2026年10月10日将下线」存在时间差，实际以文档1公布的[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)中明确的下线日期为准；7月通知为预热提醒，非最终执行日。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


