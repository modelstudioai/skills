# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可落地的操作依据。所有变更均遵循明确的时间节点与通知机制，模型生命周期管理（上架、升级、下线）与平台能力演进（API、SDK、部署、评测）同步推进。开发者应定期查阅本页，并结合[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)评估服务连续性。

## 支持的模型/功能

- **新上线模型（2026年重点）**：  
  - 多模态大模型：`qwen3.8-max`（2.4T MoE）、`kimi-k3`（2.8T）、`MiniMax-M3.1-Flash`（1M上下文+五档思考）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s）；  
  - 实时语音：`qwen-audio-3.1-realtime-flash`（双工+声音复刻）、`qwen-audio-3.0-realtime-plus`（低延迟标准版）；  
  - 3D生成：Tripo 系列共 10 个模型（如 `Tripo/Tripo-AutoRig`、`Tripo/Tripo-Retopology`），覆盖网格分割、重拓扑、绑定、动画重定向等全链路；  
  - 视频生成：`kling/kling-v3-turbo-video-generation`、`wan3.0-video-prime`（30秒高速版）、`vidu/viduq3-drama_reference2video`（剧集专用）；  
  - 图像生成：`qwen-image-3.0-pro`（10px小字渲染）、`vidu/vidu-image-pro_reference2image`（参考生图+UI像素级还原）；  
  - 专用模型：`decision-model-preview`（结构化决策）、`qwen-mt-uni`（跨模态文档翻译）、`happyoyster-1.0-adventure`（开放式世界模型）。  

- **平台功能新增（2026年Q2-Q3）**：  
  - 智能体托管：`Managed Agent` 运行时 API 上线（2026-06-29），支持会话与工具执行托管；  
  - 知识库 RAG：新增联合检索与混合排序（2026-06-23）、日志全量投递至 SLS（2026-04-24）；  
  - 模型部署：PTU 预置吞吐支持长输入与前缀缓存（2026-06-15）；  
  - SDK 扩展：Linux C++、Android/iOS Lite、RTOS C SDK 全面覆盖（2026-02）；  
  - API 增强：Responses API 支持异步调用（`background=true`）、DashScope 新版智能体 API（2026-05-11）、事件总线 HTTP 回调（2026-04-23）。  

> **注意**：文档2中列出的 `qwen3.8-max-0902`（别名 `qwen3.8-max-2026-09-02`）与文档3中 2026年8月上线的 `qwen3.8-max` 存在版本命名歧义——前者为快照版本，后者为正式发布版；实际生产环境请以控制台显示的 `qwen3.8-max`（无日期后缀）为准，其能力与文档2描述一致，但不推荐在代码中硬编码带日期的别名。

## 关键参数

- **上下文窗口**：主流新模型统一支持 **1,000,000 Token**（如 `qwen3.8-max`、`kimi-k3`、`GLM-5.3-FlashX`），部分轻量模型为 262,144（如 `qwen-audio-3.1-realtime-flash`）或 32K–128K（如向量模型 `qwen3.7-text-embedding-flash`）。  
- **输出长度**：最大支持 `384K`（`deepseek-v4.1-flash-1017`）、`128K`（`GLM-5.3-FlashX`）、`256K`（`qwen3.8-flash`）；实时语音模型未公开最大输出长度，以流式响应为准。  
- **多模态能力**：`qwen3.8-omni-flash`、`MiniMax-M3.1-Flash`、`ZHIPU/GLM-5.3-Flash` 等明确支持文本/图片/视频/音频四模态输入；`qwen-mt-uni` 支持 PDF/Word/PPT/Excel/HTML/Markdown/TXT/图片/音频八类输入模态自动识别。  
- **推理性能**：`ZHIPU/GLM-5.3-FlashX` 达 200 tokens/s，`qwen-audio-3.0-tts-flash` 专为低延迟优化，`qwen-audio-3.1-realtime-flash` 端到端响应时延控制在行业领先水平。  
- **模型架构**：MoE 成为主流，参数规模从 `284B`（`deepseek-v4-flash-0731`）到 `2.4T`（`qwen3.8-2.4t-a95b`）不等；稀疏注意力、混合注意力、KV Cache 压缩（如 `deepseek-v4.1-flash` 压缩至 HBM 的 1/4）为性能优化关键。

## 使用方式

- **模型调用**：  
  - 通过标准 REST API（兼容 OpenAI / Anthropic 协议）调用，如 `qwen3.8-flash` 支持 `/v1/chat/completions` 接口；  
  - 实时语音模型需使用 WebSocket 或 WebRTC 协议（如 `qwen3.8-omni-flash-realtime`）；  
  - 多模态翻译 `qwen-mt-uni` 支持同步（HTTP）与异步（回调）两种模式，异步任务结果通过事件总线推送。  
- **平台功能接入**：  
  - 新增功能均配套完整文档路径，例如 Managed Agent 运行时 API 文档位于 [raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)，知识检索服务文档位于 [raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md](../../raw/application-user-guide/knowledge-base/rag-knowledge-retrieval.md)；  
  - SDK 集成参考对应语言文档：Linux C++ SDK（2026-02-28）、Android Lite SDK（2026-02-06）、Java SDK（2026-04-28）。  
- **模型部署与调优**：  
  - PTU 部署支持长输入与前缀缓存（2026-06-15）；  
  - 模型调优已支持文本、视觉理解（VL）、图像生成、视频生成四类模型（2026-01 至 2026-05），强化学习（RL）训练为邀约制（2026-05-31）；  
  - 模型压缩模块（2025-05-25）支持量化降低部署成本。

## 限制和注意事项

- **模型下线强制时间表**：  
  - 正式版模型自启动下线公告起 **3个月后停止服务（EoS）**，期间逐步缩减 QPM/TPM；预览版模型仅 **14天** 宽限期；详情见[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)；  
  - 已明确下线模型包括：2026年10月10日批次（公告号 118177/118434 等）、2026年7月10日“部分老旧模型”（公告 118434）、2026年7月9日“部分老旧长尾模型”（公告 118427）。  
- **功能兼容性风险**：  
  - `qwen-turbo` 资源包已于 2026-06-28 启动退市（[文档3](../../raw/model-user-guide/release-notes/model-release-notes.md)），存量用户需迁移至 `qwen-flash` 或 `qwen-plus`；  
  - 企业知识库（旧）于 2026-07-16 下线（[文档3](../../raw/model-user-guide/release-notes/model-release-notes.md)），必须切换至新版知识库 RAG 服务；  
  - `qwen-audio-3.0-asr-flash-streaming` 等 ASR 模型虽支持方言与古诗词，但对极低信噪比（<5dB）或严重混响场景识别率未作保证，建议预处理降噪。  
- **计费与配额**：  
  - Token Plan 团队版自 2026-05-08 起支持 SSO/钉钉登录与席位用量监控；  
  - 新人免费额度有效期已调整（[文档3](../../raw/model-user-guide/release-notes/model-release-notes.md)），具体以控制台实时展示为准；  
  - 部分模型（如 `qwen-vl` 系列、`qwen` 系列）存在阶段性降价活动，价格变动不影响已购资源包有效期。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


