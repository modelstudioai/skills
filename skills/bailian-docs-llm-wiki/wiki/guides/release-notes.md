# release notes

百炼平台的 Release Notes 汇总了模型上下架、平台功能迭代、计费策略调整等关键变更，面向开发者提供可操作的版本演进信息。所有变更均以实际生效日期为准，模型生命周期管理（如上架/下线）与平台能力升级（如 API、SDK、部署方式）同步推进。建议开发者定期查阅本页，并结合控制台通知与[模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)做好兼容性迁移。

## 支持的模型/功能

- **新增模型（2026年7–9月重点）**：  
  - 多模态大模型：`qwen3.8-omni-flash`（全模态输入/输出）、`stepfun/step-5-preview`（1M上下文+视觉输入）、`ZHIPU/GLM-5.3-FlashX`（200 tokens/s推理速度）；  
  - 实时交互模型：`qwen-audio-3.1-realtime-plus`（双工语音+Function Calling）、`qwen3.8-omni-flash-realtime`（音视频聚合+远程MCP调用）；  
  - 垂直场景模型：`qwen-mt-uni`（跨模态文档/图片/音频翻译）、`happyoyster-1.0-adventure`（开放式世界模型）、`vidu/viduq3-ad_reference2video`（广告专用视频生成）。  
- **功能模块上线**：  
  - 知识库RAG服务（2026年6月23日）：含联合检索与混合排序、知识问答生成；  
  - 智能体托管运行时（2026年6月29日）：平台托管会话与工具执行；  
  - 模型压缩模块（2026年5月25日）：支持量化降低部署成本；  
  - 强化学习训练（2026年5月31日，邀约制）：基于奖励信号优化策略。  
- **SDK与接入工具扩展**：  
  - 新增 Linux C++ SDK（2026年2月28日）、Android/iOS Lite SDK（2026年2月6日）、RTOS C SDK License模式（2026年4月9日）；  
  - Codex 客户端接入（2026年6月24日）、Kilo CLI 工具（2026年2月22日）。

> **注意**：文档2中 `kimi/kimi-k3` 与 `kimi-k3` 出现两次（发布日期分别为2026-08-19和2026-07-17），但模型ID不一致（前者含路径前缀），实际应为同一模型不同命名规范；建议以控制台显示的 `model_id` 为准，避免硬编码别名。

## 关键参数

- **上下文窗口**：主流新模型（如 `qwen3.8-max`、`GLM-5.3`、`stepfun/step-5-preview`）统一支持 **1M Token** 上下文；  
- **输出长度**：`deepseek-v4.1-flash` 支持最大 384K 输出，`ZHIPU/GLM-5.3-FlashX` 支持 128K 输出；  
- **多模态能力**：`qwen3.8-omni-flash`、`GLM-5.3-Flash`、`deepseek-v4.1-flash` 均原生支持图像/视频/文件输入；  
- **推理性能**：`GLM-5.2-Fast-Preview` 输出 TPS 较标准版提升 1.5–2 倍；`qwen-audio-3.0-tts-flash` 专为低延迟实时合成优化；  
- **部署粒度**：模型部署支持按模型单元（MU）时长计费（2026年1月23日上线），适用于 `qwen-flash`/`qwen-plus` 等预置模型。

## 使用方式

- **模型调用**：  
  - 兼容 OpenAI（`/v1/chat/completions`）与 Anthropic（`/v1/messages`）协议的模型（如 `qwen3.8-flash`）可直接复用现有 SDK；  
  - 实时语音类模型（如 `qwen-audio-3.0-realtime-plus`）需使用 WebSocket 或 WebRTC 协议接入；  
  - 多模态翻译 `qwen-mt-uni` 支持同步/异步两种调用方式，异步任务通过 `background=true` 提交并轮询结果（见 [Responses API 文档](../../raw/model-api-reference/qwen-api-reference.md)）。  
- **平台功能启用**：  
  - 新增功能（如记忆库 Memory 2.0、Managed Agent）需在控制台对应模块开启或配置；  
  - 技能（Skill）能力包需通过应用编辑器添加官方或自定义技能（2026年6月10日上线）；  
  - 数据连接模块支持 MySQL/语雀/OSS 等数据源配置（2026年6月10日上线）。  
- **模型调优与部署**：  
  - 视觉理解（VL）、视频生成（如 Wan 系列）、图像生成模型均支持调优（2026年1–5月陆续上线）；  
  - 预置吞吐（PTU）部署支持长输入与前缀缓存（2026年6月15日）；  
  - 模型导入 API 支持从 OSS 导入 LoRA 微调模型（2026年6月5日国际站上线）。

## 限制和注意事项

- **模型下线影响**：  
  - 自下线通知发布日起，QPM/TPM 将逐步缩减；正式下线后，API 推理、新调优/部署均停止，但已部署模型不受影响；  
  - 快照模型（如 `qwen-max-2025-01-25`）提前30天下线通知，主线模型提前3个月通知（详见 [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)）。  
- **地域与服务范围**：  
  - 新增美国、德国、日本地域（2026年6月12日），但部分模型（如 `qwen3.8-omni-flash-realtime`）可能暂未全地域可用，需以控制台地域列表为准。  
- **兼容性风险**：  
  - `qwen-turbo` 资源包已启动退市（2026年6月28日），存量用户需迁移至 `qwen-flash` 或其他替代模型；  
  - 企业知识库（旧）已于2026年7月16日下线，需迁移到新版知识库服务；  
  - `qwen-audio-3.0-asr-flash` 系列模型虽标注“非实时”，但 `qwen-audio-3.0-asr-flash-streaming` 明确为实时流式，调用时需严格区分 endpoint 与参数（见 [语音识别文档](../../raw/model-user-guide/release-notes/newly-released-models.md)）。  
- **计费变更**：  
  - GLM-5.2 Fast mode 模式于2026年7月14日降价（[公告链接](https://www.aliyun.com/notice/118443)）；  
  - Token Plan 团队版自2026年5月8日起支持 SSO/钉钉登录与席位分配，旧版团队管理接口已废弃。

## 来源文档

- [模型下线机制说明](../../raw/model-user-guide/release-notes/model-depreciation.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)


