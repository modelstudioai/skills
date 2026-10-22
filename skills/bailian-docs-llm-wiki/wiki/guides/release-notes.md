# release notes

百炼平台的 Release Notes 汇总了近期模型上架、功能迭代、平台能力升级及关键机制变更，面向开发者提供可落地的技术更新概览。内容覆盖新模型能力边界、核心参数规格、调用方式演进、已知限制与迁移注意事项，所有信息均基于平台当前生产环境状态。建议开发者定期查阅本页，并结合具体模型文档进行集成验证。

## 支持的模型/功能

截至 2026 年 10 月下旬，平台新增支持以下重点模型类别：

- **多模态大模型**：`MiniMax/MiniMax-M3.1-Flash`（文本/图/视频输入，1M 上下文，五档思考深度）、`xiaomi/mimo-v2.6-pro-ultraspeed`（1T 参数基座，10 倍加速，原生音频理解）、`deepseek-v4.1-flash-1017`（552B MoE，Terminal-Bench 4.0 显著提升，支持“许愿式”编程）；  
- **图像生成模型**：`qwen-image-2.1-turbo`（轻量高质，编辑一体化）、`vidu/vidu-image-pro_reference2image`（参考生图+像素级 UI 还原）、`qwen-image-3.0-pro`（4.5k token 指令，10px 小字渲染，报纸/分镜级排版）；  
- **视频生成模型**：`kling/kling-v3-turbo-video-generation`（文生/图生视频，固定音画同出）、`wan3.0-video-prime`（30 秒生成，四模态参考）、`vidu/viduq3-drama_reference2video`（剧集专用，角色一致性强化）；  
- **决策与排序模型**：`decision-model-preview`（并行分类/是非判断/评分，返回概率分布与置信度）、`qwen3.7-text-rerank`（Web 检索相对提升 35%，Agentic 场景优化）；  
- **语音与音频模型**：`qwen-audio-3.1-realtime-plus`（双工语音，262K 上下文，Function Calling + 声音复刻）、`qwen-audio-3.0-asr-flash-streaming`（七大方言 + 30 语种，古诗词识别专项优化）。

> **注意**：文档 1 中多次出现 `kimi/kimi-k3`（2026-07-17）与 `kimi-k3`（2026-08-19）两个条目，模型 ID 格式不一致（前者含斜杠，后者无），且发布时间不同。实际调用应以控制台或 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 中最新发布的 `kimi-k3` 为准，旧条目可能为冗余记录。

## 关键参数

各模型共性关键参数如下（具体以单模型文档为准）：

- **上下文窗口**：主流多模态模型（如 `qwen3.8-flash`、`glm-5.3-flashx`、`stepfun/step-5-preview`）统一支持 **1,000,000 Token**；部分轻量模型（如 `qwen-audio-3.1-realtime-plus`）为 262,144 Token；图像/视频模型通常不适用 Token 计量，以分辨率/时长/参考图数量界定。  
- **输出长度**：`deepseek-v4.1-flash` 系列、`glm-5.3-flashx` 支持 **384K 最大输出**；`qwen3.8-max` 等旗舰模型未明确上限，但实测支持长程交付任务。  
- **多模态能力**：文本/图像/视频/音频输入支持需显式声明（如 `qwen3.8-omni-flash` 支持全模态输入，`qwen-mt-uni` 自动识别输入模态）；视觉理解能力已成标配，但 `qwen3.7-flash` 等早期 Flash 版本仅强化基础识别，`qwen3.8-max` 则贯穿规划-执行-验证全流程。  
- **推理性能**：`ZHIPU/GLM-5.3-FlashX` 达 200 tokens/s，`xiaomi/mimo-v2.6-pro-ultraspeed` 相比原版提速约 10 倍，`MiniMax/MiniMax-M3.1-Flash` 约 170 tokens/s —— 实际吞吐受输入长度、思考深度档位及部署模式（PTU/Serverless）影响显著。

## 使用方式

- **API 调用**：主流文本/多模态模型兼容 OpenAI (`/v1/chat/completions`) 与 Anthropic (`/v1/messages`) 协议（见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 2026 年 5 月 15 日更新）；图像/视频模型使用专属 `/v1/async/tasks` 异步接口（如 `qwen-mt-uni` 同步/异步双模式）。  
- **SDK 与工具链**：支持 Spring AI Alibaba（[文档上线](../../raw/model-user-guide/release-notes/model-release-notes.md)）、Codex CLI（[6 月 24 日接入](../../raw/model-user-guide/release-notes/model-release-notes.md)）、Kilo CLI（[2 月 22 日新增](../../raw/model-user-guide/release-notes/model-release-notes.md)）；多模态交互开发套件提供 Android/iOS/Lite/RTOS/C++ 全端 SDK。  
- **部署与调优**：预置模型支持 API 直接部署（[1 月 23 日上线](../../raw/model-user-guide/release-notes/model-release-notes.md)）；调优支持文本生成、VL、图像生成、视频生成四类模型（[1 月、5 月多次更新](../../raw/model-user-guide/release-notes/model-release-notes.md)），强化学习（RL）训练为邀约制（[5 月 31 日](../../raw/model-user-guide/release-notes/model-release-notes.md)）。  
- **知识库与 Agent**：RAG 新增知识检索与问答服务（[6 月 23 日](../../raw/model-user-guide/release-notes/model-release-notes.md)）；Managed Agent 已商业化（[7 月 16 日通知](../../raw/model-user-guide/release-notes/model-release-notes.md)）；记忆库 Memory 2.0 支持跨应用共享（[3 月 20 日](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 限制和注意事项

- **模型下线策略**：快照模型（含日期后缀，如 `qwen3.8-max-0902`）下线前 **30 天**通知；主线模型（如 `qwen3.8-max`）下线前 **3 个月**通知。自通知日起逐步限流，正式下线后 API 完全不可用，且不再支持新调优/部署（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。  
- **地域与协议限制**：实时语音对话模型（如 `qwen-audio-3.0-realtime-plus`）需通过 WebSocket/WebRTC/AOQ 接入，不支持 HTTP 同步调用；部分新模型（如 `qwen3.8-omni-flash-realtime`）仅在华北2（北京）等指定地域可用。  
- **功能兼容性**：`qwen3.8-flash` 声称“兼容 OpenAI 与 Anthropic 主流接口协议”，但 `qwen3.8-omni-flash` 的 Function Calling 和联网搜索需配合特定参数（如 `tool_choice: "auto"`）；`qwen-mt-uni` 的版面还原与语音克隆能力仅在异步模式下生效。  
- **成本与资源**：`qwen-turbo` 资源包已于 2026 年 6 月 28 日启动退市（[文档 3](../../raw/model-user-guide/release-notes/model-release-notes.md)）；上下文缓存、PTU 长输入等高级能力需单独开通或计费（[6 月 15 日、7 月 14 日更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）。

## 来源文档

- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


