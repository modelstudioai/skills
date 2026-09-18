# release notes

百炼平台的 Release Notes 汇总了模型上下架、功能迭代、参数变更及平台策略更新等关键信息，面向开发者提供可操作的版本演进视图。所有变更均以实际生效日期为准，建议通过控制台监控、API 响应头或事件总线主动订阅变更通知。模型生命周期管理（如上下线）与功能发布遵循独立节奏，需分别关注。

## 支持的模型/功能

- **新模型上架**：2026年7–9月密集发布多模态旗舰模型，包括 `qwen3.8-max`（2.4T MoE）、`ZHIPU/GLM-5.3-Flash`（原生多模态，320B总参）、`kimi-k3`（2.8T开源旗舰）、`vidu/viduq3-drama_reference2video`（剧集专用视频生成）等；覆盖文本生成、视觉理解、视频/图片生成、语音识别（ASR）、语音合成（TTS）、实时语音对话、多模态翻译等全模态能力。  
- **功能模块新增**：知识库 RAG 新增[知识检索服务](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)与[知识问答服务](raw/application-user-guide/knowledge-base/rag-knowledge-qa.md)；智能体托管运行时上线，支持会话与工具执行全托管；模型压缩模块支持量化部署降本；多模态交互开发套件覆盖 Android/iOS/Lite/Linux C++/RTOS C 等全端 SDK。  
- **模型能力扩展**：模型调优新增强化学习训练（邀约制）、图像/视频/视觉理解模型类型支持；文本生成 API 入口聚合 OpenAI Responses 与 Anthropic Messages 接口；Responses API 新增异步调用（`background=true`）；API Key 支持加密存储与业务空间专属域名。

> **注意**：文档 3 中 `kimi/kimi-k3` 与 `kimi-k3` 在 2026-07-17 和 2026-08-19 两次出现，但模型 ID 格式不一致（带斜杠 vs 不带），实际调用应以控制台或 API 文档中公布的标准化 model_id 为准；该差异可能反映内部命名规范调整，建议以 [模型平台功能更新](raw/model-user-guide/release-notes/model-release-notes.md) 中的链接说明为权威参考。

## 关键参数

- **上下文窗口**：主流旗舰模型（如 `qwen3.8-max`、`GLM-5.3-Flash`、`kimi-k3`）统一支持 **100 万 token** 上下文；`qwen3.7-text-embedding-flash` 支持 **128K 长文本处理**；`pixverse/pixverse-upscale` 支持 4K 视频超分。  
- **性能指标**：`deepseek-v4-flash-0731` 激活参数 13B，输出延迟低；`kimi-k2.7-code-highspeed` 编程场景输出达 **260 Token/s**；`qwen-audio-3.0-realtime-flash` 专注端到端低时延。  
- **计费模式**：模型部署新增按**模型单元（MU）时长计费**；Token Plan 团队版支持跨坐席共享 Credits 弹性用量包；Coding Plan Pro 新客首月特惠 ¥39.90。  
- **限流策略**：待下线模型自通知发布日起逐步缩减 QPM/TPM，最终恢复至[默认限流](raw/model-user-guide/get-started-with-models/rate-limit.md)后执行；具体阈值见各模型详情页。

## 使用方式

- **模型调用**：通过标准 REST API（兼容 OpenAI/Anthropic 协议）或 DashScope SDK 调用；新模型如 `qwen-mt-uni` 支持同步/异步双模式；视频生成类模型（如 `wan3.0-video-prime`）需按接口要求传入多模态输入。  
- **功能接入**：  
  - 知识库 RAG：调用 `/retrieve` 接口启用排序模型与指令干预；  
  - 智能体托管：使用 [Managed Agent 运行时 API](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 提交任务；  
  - 模型导入：国际站支持从 OSS 导入 LoRA 模型，详见 [模型导入 API](raw/model-api-reference/model-production/fine-tuning-jobs-api/model-fine-tuning-text-generation-api/custom-models-api.md)；  
  - 临时凭证：在不可信环境使用 [生成临时 API Key](raw/application-api-reference/more/application-obtain-temporary-authentication-token.md) 避免泄露。  
- **监控与迁移**：通过 [模型监控](https://bailian.console.aliyun.com/model/telemetry) 检查待下线模型使用情况；切换前需在沙箱环境验证替代模型效果。

## 限制和注意事项

- **模型下线影响**：正式下线后，模型推理服务立即终止，已创建的应用将无法返回结果；**模型调优与部署功能同步禁用**（已训练/部署模型不受影响）；控制台功能与文档同步下线。快照模型（如 `qwen-max-2025-01-25`）提前 30 天通知，主线模型提前 3 个月通知 —— 详见 [模型下线机制说明](raw/model-user-guide/release-notes/model-depreciation.md)。  
- **地域与协议限制**：新增美国、德国、日本地域接入，但部分模型（如 `happyoyster-1.0-adventure`）仅限华北2（北京）可用；多模态翻译 API 的版面还原能力依赖输入文件格式（PDF/Word/PPT 等），不支持加密文档。  
- **兼容性风险**：`qwen3.7-max-2026-05-20` 与 `qwen3.7-max-2026-06-08` 为快照版本，视觉能力增量发布，若依赖特定模态能力，需显式指定带日期后缀的 model_id；`glm-5.2-fast-preview` 与 `GLM-5.2` 能力对齐但 TPS 更高，非完全等价替换。  
- **[安全与合规](../concepts/security-and-compliance.md)**：模型调优新增 0 代码安全合规强化流程，但该能力仅适用于文本生成模型；视觉/视频类模型暂未开放同等强化选项，需自行校验输出内容。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


