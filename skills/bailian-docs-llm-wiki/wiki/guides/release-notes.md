# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的时效性信息。所有变更均以实际生效日期为准，建议通过控制台「模型监控」和「通知中心」主动订阅更新。模型生命周期管理（含下线与上架）与平台能力演进（如 API、部署、评测）遵循独立但协同的发布节奏，需结合多源文档交叉验证。

## 支持的模型/功能

- **新增模型（2026年7–10月重点）**：  
  - 多模态大模型：`qwen3.8-omni-flash-realtime`（实时全模态）、`stepfun/step-5-preview`（Agentic 旗舰）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s 高速版）；  
  - 图像生成：`qwen-image-2.1-turbo`（轻量高性价比）、`vidu/vidu-image-pro_reference2image`（像素级 UI 还原）；  
  - 视频生成：`kling/kling-v3-turbo-video-generation`（极速文生视频）、`wan3.0-video-prime`（30秒高速版）；  
  - 专用模型：`decision-model-preview`（结构化决策）、`qwen-mt-uni`（跨模态统一翻译）。  
- **平台功能扩展**：  
  - 新增 **Responses API 异步调用模式**（`background=true`），适用于长耗时任务；  
  - **智能体托管运行时 API** 上线，支持平台托管会话与工具执行；  
  - **知识检索服务**与**知识问答服务**同步发布，支持多知识库联合检索与混合排序；  
  - **模型评测**新增排行榜（Leaderboard）与综合评测能力，支持 BLEU_4 等评分方法。  
- **模型调优能力升级**：  
  - 支持图像生成（Wan / Wanx）、视频生成（万相系列）、视觉理解（VL）模型类型；  
  - 新增强化学习（RL）训练（邀约制）与 0 代码安全合规强化流程。  

> **注意**：文档 2 中 `kimi/kimi-k3`（2026-07-17）与 `kimi-k3`（2026-08-19）为同一模型不同命名，但参数描述一致（2.8 万亿参数、100 万上下文），属重复条目；实际以控制台模型 ID 为准。文档 3 中“模型调优新增视觉理解模型类型支持”发布于 2026-01-22，而文档 2 中 `qwen3.7-flash`（2026-07-21）已明确标注“相较3.6-Flash全面提升多模态理解与Agent执行能力”，说明视觉理解调优能力早于文档 3 记录时间点已落地，文档 3 的时间戳可能滞后。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3-Flash`、`deepseek-v4.1-flash`）统一支持 **1M Token**；部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 **128K**。  
- **输出长度**：`deepseek-v4.1-flash` 系列支持 **384K 最大输出**；`GLM-5.3-FlashX` 支持 **128K 输出**。  
- **推理速度**：`MiniMax/MiniMax-M3.1-Flash` 达 **~170 tokens/s**；`ZHIPU/GLM-5.3-FlashX` 达 **200 tokens/s**；`qwen-audio-3.0-realtime-flash` 专注低延迟，端到端响应时延经工程优化控制在极低水平。  
- **多模态输入支持**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持文本、图片、视频、文件输入；`qwen-audio-3.0-realtime-plus` 支持实时音视频交互及文本/音频输出。  
- **向量模型维度**：`qwen3.7-text-embedding` 支持 **256~2560 维用户自定义向量维度**，`qwen3.7-text-embedding-flash` 为轻量级版本，侧重吞吐与成本。

## 使用方式

- **模型调用**：  
  - 通过标准 API（OpenAI Responses / Anthropic Messages 兼容协议）调用，详见 [模型 API 参考](raw/model-api-reference/qwen-api-reference.md)；  
  - 实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 或 WebRTC 协议接入；  
  - 多模态翻译（`qwen-mt-uni`）支持同步与异步两种调用方式。  
- **平台功能接入**：  
  - 智能体托管运行时 API 文档见 [managed-agents-api-overview.md](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)；  
  - 数据连接模块支持 MySQL/语雀/OSS 等数据源，配置入口位于应用控制台「数据连接」；  
  - Prompt 工程模块提供模板管理 API，路径为 [api-bailian-2023-12-29-dir-prompt-engineering.md](raw/_short/api-bailian-2023-12-29-dir-prompt-engineering-11ee962a5f5d5d1e.md)。  
- **模型部署与调优**：  
  - 预置模型（如 `qwen-flash`）可通过 API 直接部署，支持按模型单元（MU）时长计费；  
  - 图像/视频生成模型调优指南分别见 [wan-image-generation-finetune-guide.md](raw/model-user-guide/fine-tuning/wan-image-generation-finetune-guide.md) 和 [wan-video-generation-finetune-guide.md](raw/model-user-guide/fine-tuning/wan-video-generation-finetune-guide.md)。  

## 限制和注意事项

- **模型下线机制**：  
  - **快照模型**（如 `qwen-max-2025-01-25`）下线前 **30 天**通知；**主线模型**下线前 **3 个月**通知；  
  - 自通知发布日起逐步缩减 QPM/TPM，正式下线后停止推理服务，且**不再支持新调优与新部署**（已训练/部署模型不受影响）；  
  - 详细下线清单与时间表请严格参照 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。  
- **功能兼容性**：  
  - `qwen-turbo` 资源包已于 2026-06-28 启动退市，[相关通知](https://www.aliyun.com/notice/118392) 明确其不可续订；  
  - 企业知识库（旧）已于 2026-07-16 下线，迁移至新版知识库 RAG 服务，[迁移指引](raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md) 已发布。  
- **地域与接入限制**：  
  - 新增美国、德国、日本地域支持，但部分模型（如 `qwen-audio-3.0-realtime-plus`）当前仅限华北2（北京）可用；  
  - 国际站模型导入功能已上线，但 LoRA 微调模型导入仅支持 OSS 源，不支持本地上传。  
- **计费与额度**：  
  - Token Plan 团队版自 2026-05-08 起支持 SSO/钉钉登录与席位分配；  
  - 部分模型（如 `qwen3.7-text-embedding`）降价通知见 [千问系列模型降价通知](https://help.aliyun.com/zh/model-studio/qwen-model-billing-notice)，但具体价格需以控制台实时报价为准。  

> **注意**：文档 3 中“部分老旧模型延期下线通知”（2026-07-06）与文档 1 中“2026年10月10日将下线”模型列表存在潜在冲突——若某模型原定 2026-07-30 下线但被延期，则其实际下线日应晚于 10月10日。开发者须以最新官网公告（如 [https://www.aliyun.com/notice/118420](https://www.aliyun.com/notice/118420)）及控制台通知为准，不可仅依赖静态列表。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


