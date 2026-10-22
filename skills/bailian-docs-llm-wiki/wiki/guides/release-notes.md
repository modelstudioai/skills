# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的技术更新概览。所有变更均以实际生效时间为准，建议通过控制台「模型监控」和「通知中心」及时获取动态。模型生命周期管理（含下线与上架）与平台能力演进遵循统一治理规范，具体细节请严格参照各原始文档。

## 支持的模型/功能

- **新增模型**：2026年7–10月密集上线多模态与垂直场景模型，包括 `qwen3.8-omni-flash-realtime`（实时全模态）、`decision-model-preview`（结构化决策）、`qwen-mt-uni`（跨模态翻译）、`happyoyster-1.0-adventure`（世界模型）等；图像生成类新增 `qwen-image-3.0-pro` 与 `viduq3-drama_reference2video`；视频生成类覆盖 `wan3.0-video-prime`、`pixverse/pixverse-motioncontrol` 等细分能力模型。完整清单见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能模块升级**：2026年6月起全面支持知识库 RAG 的「联合检索+混合排序」、智能体托管运行时 API、Skill 能力包、数据连接（MySQL/语雀/OSS）、模型评测 Leaderboard 及综合评估器；7月上线记忆库 Memory 2.0（支持多应用共享[长期记忆](../concepts/long-term-memory.md)）；8月新增模型升级通知机制。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型调优扩展**：自2026年1月起支持视觉理解（VL）、视频生成（Wan系列）、图像生成（Wanx）三类模型调优；5月新增强化学习（RL）训练（邀约制）与0代码安全合规强化流程。相关能力说明参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`deepseek-v4.1-flash`、`glm-5.3`）统一支持 **1M [Token](../concepts/token.md)** 上下文；部分轻量模型（如 `qwen3.7-text-embedding-flash`）支持 **128K** 长文本处理。
- **输出长度**：`deepseek-v4.1-flash` 系列最大输出 **384K tokens**；`glm-5.3-FlashX` 支持 **128K** 输出；`qwen-audio-3.0-realtime-plus` 上下文为 **262,144 tokens**。
- **推理性能**：`MiniMax/MiniMax-M3.1-Flash` 达 **~170 tokens/s**；`ZHIPU/GLM-5.3-FlashX` 达 **200 tokens/s**；`qwen-audio-3.0-tts-flash` 专为低延迟优化；`kimi-k3` 采用 KDA 混合注意力机制，兼顾长程推理与响应节奏。
- **多模态输入支持**：`qwen3.8-omni-flash`、`stepfun/step-5-preview`、`ZHIPU/GLM-5.3-Flash` 等均原生支持文本、图片、视频、音频四模态输入；`qwen-mt-uni` 自动识别并处理 PDF/Word/PPT/HTML/Markdown/TXT/图片/音频等输入模态。

## 使用方式

- **模型调用**：通过标准 REST API（兼容 OpenAI Anthropic 协议）或 DashScope SDK 调用；实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket/WebRTC 接入；[异步任务](../concepts/asynchronous-task.md)（如长视频生成）推荐启用 `background=true` 参数并轮询结果，或配置 EventBridge HTTP 回调避免轮询。参考 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中 6月1日与4月23日条目。
- **模型部署**：支持 PTU 预置吞吐部署（含长输入与前缀缓存）、按模型单元（MU）时长计费；国际站已开放 LoRA 模型从 OSS 导入。详情见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 6月5日与1月23日条目。
- **模型迁移**：当模型进入下线流程时，需主动切换至替代模型。建议先在[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)中确认调用情况，并完成业务效果验证后再切换。操作指引见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 限制和注意事项

- > **注意**：文档2中 `kimi/kimi-k3`（2026-07-17）与文档2中同名条目 `kimi-k3`（2026-08-19）存在发布时间矛盾（后者标注为“迄今能力最强”，但早于前者发布），且参数描述（2.8万亿 vs 全球首个3万亿级别）不一致。请以控制台模型广场实时信息及官方公告为准，勿依赖文档中孤立的时间戳。
- > **注意**：文档3中 7月16日「企业知识库（旧）下线通知」与文档1中「模型下线」机制适用范围不同——前者属平台功能模块下线，后者仅约束模型服务本身；二者限流策略、通知周期、影响范围均无关联，不可混用其规则。
- 模型下线前将逐步缩减 QPM/TPM，自通知发布日起即开始限流；正式下线后，**已创建的调用该模型的应用将无法返回结果**，且**不再支持基于下线模型的新调优与新部署**（已训练/部署的实例不受影响）。详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- 部分模型（如 `qwen-turbo` 资源包、`析言GBI` 商品）属于商品/资源包下线，非模型本身下架，不影响同名模型 API 调用；此类变更归属平台功能更新范畴，不触发模型级限流。参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 6月28日与7月9日条目。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


