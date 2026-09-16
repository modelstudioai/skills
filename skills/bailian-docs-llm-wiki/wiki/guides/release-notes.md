# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代及关键机制变更，面向开发者提供可操作的版本演进信息。内容涵盖新模型发布、历史模型下线、API/SDK 功能增强、计费与部署模式更新等核心变化，所有变更均以实际生效日期为准，建议开发者定期查阅并及时适配。

## 支持的模型/功能

- **新增模型**：2026年8月起密集上线多模态与垂直场景模型，包括 `qwen3.8-flash`（百万上下文、OpenAI/Anthropic 协议兼容）、`deepseek-v4.1-flash`（552B MoE、原生多模态）、`ZHIPU/GLM-5.3-Flash`（320B、1M上下文）、`kling/kling-v3-turbo-video-generation`（文生/图生视频）、`qwen-audio-3.0-asr-flash-streaming`（方言+古诗词优化实时ASR）等。完整列表详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。
- **功能扩展**：新增知识检索服务与知识问答服务（支持多知识库联合检索与混合排序）、智能体托管运行时 API（平台托管会话与工具执行）、Responses API 异步调用（`background=true`）、多模态翻译 API（覆盖文本/图片/文档/网页翻译）、Prompt 工程 API（模板管理能力）等。
- **SDK/客户端支持**：新增 Codex 客户端接入、Kilo CLI 工具、Linux C++ / Android / iOS Lite / RTOS C 多模态 SDK、服务端 Java SDK 及网页翻译 JSSDK。

> **注意**：文档2中 `kimi/kimi-k3` 与 `kimi-k3` 出现两次（分别在2026-09-19和2026-07-17），但模型ID写法不一致（带斜杠 vs 不带），实际应为同一模型；建议以控制台显示的标准化 ID `kimi/kimi-k3` 为准，避免硬编码非规范ID。

## 关键参数

- **模型标识**：快照模型（如 `qwen3.8-max-2026-09-02`）含日期后缀，主线模型（如 `glm-5.3`）无日期；快照模型下线通知期为**30天**，主线模型为**3个月**（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。
- **上下文与输出**：主流旗舰模型（`qwen3.8-max`、`glm-5.3`、`kimi-k3` 等）统一支持 **1M token 上下文**；部分视频模型（如 `wan3.0-video-prime`）支持最长 **30秒视频生成**；`qwen3.7-text-embedding` 支持 **256~2560维用户自定义向量维度**。
- **性能指标**：`deepseek-v4-pro-0813` 激活参数 49B，`qwen3.8-2.4t-a95b` 激活约 950B；`kimi-k2.7-code-highspeed` 输出速度达 **260 Token/s**（短上下文）；`qwen-audio-3.0-realtime-flash` 专注低延迟，`realtime-plus` 侧重高质量回复。

## 使用方式

- **模型调用**：通过标准 REST API（支持 OpenAI Responses / Anthropic Messages 分类入口）、DashScope SDK 或客户端工具（如 Codex、Kilo CLI）调用；异步任务可通过事件总线 HTTP 回调或 RocketMQ 主动推送完成事件，避免轮询。
- **部署与调优**：支持预置吞吐部署（PTU）长输入与前缀缓存、按模型单元（MU）时长计费；模型调优已覆盖文本、视觉理解（VL）、图像生成、视频生成四类模型，并新增强化学习（RL）训练（邀约制）与 0 代码安全合规强化流程。
- **平台集成**：Spring AI Alibaba 框架可直接调用百炼智能体与工作流应用；UI 设计器支持可视化拖放构建网页应用；数据连接模块支持 MySQL/语雀/OSS 等数据源接入。

## 限制和注意事项

- **模型下线影响**：自下线通知发布日起，QPM/TPM 将逐步缩减至默认限流值；正式下线后，**模型推理服务完全停止**，已创建的应用将无法返回结果；调优与部署功能同步禁用（已训练/部署模型不受影响）。详情请严格遵循 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)。
- **地域与服务范围**：2026年6月起新增美国、德国、日本地域部署，但部分模型（如 `vidu/viduq3-*` 系列）当前仅限华北2（北京）可用，调用前需确认地域支持。
- **兼容性风险**：`qwen-turbo` 资源包已于2026年6月28日启动退市；企业知识库（旧）于2026年7月16日下线，需迁移至新版知识库；`fun-asr-flash-2026-06-15` 等快照ASR模型虽支持30语种，但古诗词识别优化仅针对中文，其他语种无此增强。
- **API变更**：2026年5月11日发布新版 DashScope 智能体应用 API，全面支持单轮/多轮、流式、文件问答与视觉理解；旧版 API 仍可用，但新功能仅在新版中提供。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


