# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均遵循明确的时间节点与通知机制，建议通过[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)定期核查所用模型状态，并关注控制台公告与邮件通知。模型生命周期管理（含下线）与平台能力更新均以稳定性、兼容性及开发者体验为优先。

## 支持的模型/功能

- **新上线模型**：2026年8月起密集发布多模态与垂类模型，包括 `qwen3.8-flash`（原生百万上下文、OpenAI/Anthropic 协议兼容）、`MiniMax/MiniMax-M3.1-Flash`（Agentic 任务优化）、`Tripo/Tripo-AutoRig`（3D 自动绑骨）、`qwen-mt-uni`（跨模态统一翻译）、`happyoyster-1.0-adventure`（开放式世界模型）等；语音方向新增 `qwen-audio-3.1-tts-plus`（专业级音色）、`qwen-audio-3.1-asr-flash-streaming`（低延迟流式识别）；图像生成新增 `qwen-image-3.0-pro`（高保真细节渲染）与 `vidu/vidu-image-pro_reference2image`（参考图精准还原）。
- **平台功能扩展**：2026年6月起全面支持异步调用（`background=true`）、事件总线 HTTP 回调与 RocketMQ 主动推送；新增智能体托管运行时 API、知识检索与问答服务、数据连接模块（MySQL/语雀/OSS）、Skill 能力包、多模态交互开发套件全栈 SDK（Android/iOS/Linux C++/RTOS C）；模型部署支持 PTU 长输入与前缀缓存、按模型单元（MU）时长计费；模型调优新增 RL 训练（邀约制）、0 代码安全合规强化、视频/图像/视觉理解模型类型支持。
- **模型类型区分**：正式版模型（如 `qwen-max`、`qwen-max-2025-01-25`、`qwen-max-latest`）面向生产环境，预览版模型（ID 含 `preview`/`beta`/`experimental`）用于公测验证，详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-flash`、`deepseek-v4.1-flash`、`glm-5.3-flash`）普遍支持 **1M [Token](../concepts/token.md)** 上下文；部分模型（如 `qwen-audio-3.1-realtime-flash`）为 **262,144 [Token](../concepts/token.md)**；`qwen-image-3.0` 支持最大 **4.5k token 输入**。
- **输出能力**：`deepseek-v4.1-flash-1017` 最大输出 **384K tokens**；`GLM-5.3-FlashX` 支持 **128K 输出**；`qwen3.8-2.4t-a95b` 在 GPQA Diamond 等基准达 **92.6 分**。
- **性能指标**：`qwen-audio-3.1-tts-flash` 侧重低延迟实时合成；`ZHIPU/GLM-5.3-FlashX` 推理速度达 **200 tokens/s**；`xiaomi/mimo-v2.6-pro-ultraspeed` 相比原模型输出速度提升 **约 10 倍**。
- **多模态支持**：`qwen3.8-omni-flash`、`MiniMax-H3`、`kimi-k3` 等支持文本/图片/音频/视频输入；`qwen-mt-uni` 自动识别并处理文本/文档/PDF/图片/音频等多模态输入。

## 使用方式

- **模型调用**：正式版模型推荐使用带日期后缀的稳定快照（如 `qwen3.8-max-2026-09-02`）或 `-latest` 别名；预览版需在控制台或文档中确认标注；API 调用需适配对应协议（如 OpenAI Responses 或 Anthropic Messages），详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中的接口分类说明。
- **功能接入**：新功能（如异步调用、事件总线回调、智能体托管运行时）需查阅对应 API 文档（如 `raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md`）；SDK 接入请参考各平台（Android/iOS/Linux C++/RTOS C）的官方文档。
- **模型迁移**：若依赖模型即将下线，须在启动下线后 3 个月内完成切换；建议先在测试环境验证替代模型效果，再灰度上线。操作指引见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 的“操作建议”章节。

## 限制和注意事项

- > **注意**：文档 2 中列出的 `qwen3.8-max-0902`（别名 `qwen3.8-max-2026-09-02`）与文档 3 中 2026 年 8 月发布的 `qwen3.8-max` 存在命名逻辑冲突——前者为快照版本，后者为持续演进的正式版主干；实际使用应以控制台显示的模型 ID 及其状态为准，避免硬编码日期后缀导致意外降级。
- > **注意**：文档 3 明确列出 `2026年7月16日` 企业知识库（旧）下线通知，但未说明迁移路径；而文档 1 未覆盖此非模型类组件下线规则。开发者需同步查阅 [企业知识库（旧）下线通知](https://www.aliyun.com/notice/118448) 原文，及时迁移到新版知识库服务。
- 预览版模型下线周期极短（EoS 前仅 14 天通知），且不设“停止新购”节点，一旦启动下线即逐步限流并快速终止服务；正式版模型虽有 3 个月缓冲期，但自启动下线日起即停止新用户接入并下调 QPM/TPM，已扩容用户将被恢复至[默认限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)值。
- 模型下线计划可能因特殊情况暂停、延期或中止，公告内容会动态更新并附“变更说明”；开发者应订阅官网公告与邮件通知，不可仅依赖历史发布时间表。详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md) 的“下线计划的调整”章节。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


