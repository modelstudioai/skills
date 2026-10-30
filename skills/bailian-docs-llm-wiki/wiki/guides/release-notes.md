# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、服务策略变更等关键更新，面向开发者提供可落地的版本演进信息。所有变更均以生产环境生效时间为准，建议通过控制台「通知中心」及[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)主动跟踪自身依赖项状态。本文档不包含营销性描述，仅提炼技术影响面与操作指引。

## 支持的模型/功能

- **新上线模型（2026年9–10月重点）**：  
  - 多模态推理：`qwen3.8-omni-flash-realtime`（实时全模态）、`xiaomi/mimo-v2.6-pro-ultraspeed`（1T参数+1M上下文+10倍提速）、`MiniMax/MiniMax-M3.1-Flash`（Agentic任务优化）；  
  - 3D生成：Tripo全系 10 个模型（`Tripo/Tripo-ImageToSplat` 至 `Tripo/Tripo-AnimationRetarget`），覆盖生成、分割、补全、重拓扑、绑定、动画重定向等完整工作流；  
  - 决策与排序：`decision-model-preview`（结构化决策）、`qwen3.7-text-rerank`（Web/代码检索提升35%）；  
  - 音视频：`qwen-audio-3.1-realtime-flash`（双工语音）、`qwen-audio-3.1-tts-plus`（专业级音色）、`qwen-audio-3.1-asr-flash-filetrans`（长音频离线转写）。  
  详细清单见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

- **平台功能新增**：  
  - 2026年6月起，知识库RAG服务正式上线「知识检索」与「知识问答」双服务接口；  
  - 2026年5月起，模型调优支持图像生成、视频生成、视觉理解三类模型定制训练；  
  - 2026年4月起，多模态交互开发套件提供 Android/iOS Lite SDK、Linux C++ SDK 及 RTOS C SDK；  
  - 2026年3月起，记忆库升级至 Memory 2.0，支持自动提取记忆片段与跨应用共享。

> **注意**：文档2中 `qwen-audio-3.1-tts-next` 描述为“不再局限于传统 TTS”，但文档3中同期功能动态未提及该模型上线，且其能力边界（如是否支持端到端声景生成）在 API 文档中尚未明确。建议以 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中实际发布的接口说明为准。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`deepseek-v4.1-flash-1017`、`ZHIPU/GLM-5.3-FlashX`）统一支持 **1M [Token](../concepts/token.md)** 上下文；部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 **128K**；语音识别模型（如 `qwen-audio-3.1-asr-flash-streaming`）上下文为流式处理，无固定长度限制。  
- **输出长度**：`qwen3.8-max` 等旗舰模型最大输出 **384K [Token](../concepts/token.md)**；`GLM-5.3-FlashX` 为 **128K**；TTS/ASR 类模型按音频时长计费，不以 [Token](../concepts/token.md) 为单位。  
- **推理速度**：`qwen3.8-omni-flash` 达 200 tokens/s；`xiaomi/mimo-v2.6-pro-ultraspeed` 相比原版提速约 10 倍；`qwen3.8-flash` 兼顾高吞吐与低延迟。  
- **多模态输入支持**：`qwen3.8-omni-flash`、`MiniMax-M3.1-Flash`、`ZHIPU/GLM-5.3-FlashX` 等明确支持文本+图片+视频+音频混合输入；`qwen-audio-3.1-realtime-flash` 支持文本+音频双向输入输出。

## 使用方式

- **模型调用**：  
  - 所有正式版模型（含 `qwen-max`、`qwen-plus`、带日期后缀版本及 `-latest` 别名）均通过标准 `/v1/chat/completions` 或 `/v1/messages` 接口调用；  
  - 预览版模型（ID 含 `preview`/`beta`/`experimental`）需在请求头显式声明 `X-Bailian-Preview: true`；  
  - 新增模型（如 Tripo 系列、`qwen-mt-uni`）使用专属 endpoint，详见各模型文档页的「API 参考」链接。  
- **功能接入**：  
  - RAG 知识库服务通过 `/v1/knowledge/retrieve` 和 `/v1/knowledge/qa` 接口调用；  
  - Managed Agent 运行时通过 `/v1/agents/{agent_id}/invoke` 调用，需启用 [智能体托管运行时](../../raw/model-user-guide/release-notes/model-release-notes.md)；  
  - [异步任务](../concepts/asynchronous-task.md)（如长视频生成）支持 `background=true` 参数或事件总线 HTTP 回调，避免轮询。  
- **部署与调优**：  
  - PTU 部署支持长输入与前缀缓存（见 [PTU 长输入与缓存](../../raw/_short/ptu-long-input-and-cache-f0b1f22118ea9791.md)）；  
  - 模型导入支持从 OSS 导入 LoRA 微调模型（国际站已上线）；  
  - 强化学习（RL）训练当前为邀约制，需提交申请。

## 限制和注意事项

- **模型下线机制**：  
  - 正式版模型下线提前 **3 个月**公告，预览版仅提前 **14 天**；  
  - 下线分三阶段：启动下线（限流开始）→ 停止新购（EoM，仅正式版）→ 停止服务（EoS）；  
  - 已下线模型（如 `qwen-turbo` 资源包、2026年7月10日公告的“部分老旧模型”）将无法调用，控制台功能同步移除。详情请参阅 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。  

- **兼容性与弃用**：  
  - `qwen-turbo` 资源包已于 2026年6月28日启动退市，新用户不可购，存量用户服务至 EoS；  
  - 企业知识库（旧）于 2026年7月16日下线，须迁移至新版知识库服务；  
  - `qwen3.7-flash-2026-07-15` 为快照版本，不享受 `-latest` 自动更新，需手动切换至新快照。  

- **其他约束**：  
  - 预览版模型不承诺 SLA，不适用于生产环境；  
  - `decision-model-preview` 当前仅支持结构化 JSON 输出，不支持流式响应；  
  - Tripo 系列 3D 模型暂不支持自定义材质库或物理引擎导出，仅输出 `.splat`/`.glb` 等标准格式。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


