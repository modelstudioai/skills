# release notes

本页汇总百炼平台近期关键功能更新、模型上架与下线、API 行为变更及平台能力演进。内容面向开发者，聚焦可操作信息，涵盖模型支持范围、核心参数调整、调用方式变更、已知限制与注意事项。所有变更均基于官方发布记录，建议结合控制台实时状态与文档链接验证最新行为。

## 支持的模型/功能

- **新增模型**：2026年11月起，Qwen4-Max（正式版）与 Qwen4-Max-Preview（预览版）均已上线，支持 Token Plan 个人版与团队版；详见 [Token Plan 功能更新](../../raw/product-updates/release-notes/token-plan-product-updates.md)。  
- **多模态扩展**：新增 `pixverse/pixverse-v6-max-t2v`（文生视频）、`Tripo/Tripo-ImageToSplat`（3D高斯泼溅生成）、`qwen-audio-3.1-realtime-flash`（实时双工语音对话）等数十个模型，覆盖视频、3D、语音、翻译、决策等场景；详见 [模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md)。  
- **Agent 平台增强**：Managed Agent 新增沙箱持久化、多智能体协作、`todo_write` 内置工具、网页搜索与读取（`web_search`/`web_fetch`）、记忆库（Memory Store）及定时任务；详见 [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)。  
- **平台级能力**：模型平台新增 Responses API 异步调用（`background=true`）、模型压缩模块、强化学习训练（RL，邀约制）、Context Cache（当前仅限 `qwen-plus`）、以及按模型单元（MU）时长计费部署模式。

> **注意**：文档1中称 `qwen-audio-3.0-asr-flash` 和 `qwen-audio-3.0-realtime-plus` 于2026-10-29/22上线，但文档3显示其3.1版本（如 `qwen-audio-3.1-asr-flash`、`qwen-audio-3.1-realtime-plus`）已于2026-09-20起陆续发布。建议优先采用 3.1 系列，3.0 版本可能已进入下线流程，具体请参考 [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md)。

## 关键参数

- **`max_tokens` 行为统一**：自 `qwen4-max-preview` / `qwen4-max` 起，`max_tokens` 含义等效于 `max_completion_tokens`，即限制思考内容与最终回答的 Token 总量；存量模型（如 `qwen3.8-*`、`qwen-plus`）行为不变。该调整影响 OpenAI Chat Completions 与 DashScope 接口；详见 [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)。  
- **思考深度控制**：`glm-5.3-prime`、`MiniMax-M3.1-Flash` 等模型支持三档或五档深度思考；`qwen4-max` 默认开启思考模式并兼容 OpenAI/Anthropic 协议。  
- **上下文长度**：`kimi-k3.1-pro`、`deepseek-v4.1-flash`、`glm-5.3-flash` 等主流模型均支持 1M Token 上下文；`qwen-audio-3.1-realtime-flash` 达 262,144 Token；`qwen3.8-flash` 支持百万级上下文窗口。

## 使用方式

- **模型接入**：Token Plan 用户可直接在控制台选择模型调用；非 Token Plan 用户需通过模型部署（PTU/专属部署）或按量计费开通。语音识别（ASR）、语音合成（TTS）、实时语音对话等音频类模型需通过对应工具或 Agent 工具创建运行。  
- **API 调用**：文本生成 API 已聚合 OpenAI Responses 与 Anthropic Messages 接口分类；异步任务支持 `background=true` 提交 + 轮询，或通过 EventBridge/RocketMQ 主动回调；WebSocket 支持 `qwen3.8-omni-flash-realtime` 等实时全模态模型。  
- **Agent 配置**：Managed Agent 创建时可通过 `agent` 对象覆盖系统提示词、工具与 MCP Server；会话级支持 `environment_variables` 与 `mcp_configs` 自定义请求头；用户消息 `content` 支持 `image`/`video`/`file` 多模态块。  
- **模型调优与部署**：支持 SFT（全参/LoRA）、DPO、RL 训练；图像、视频、视觉理解（VL）模型均已开放调优；部署支持预置模型、OSS 导入 LoRA、按 MU 时长计费等多种方式。

## 限制和注意事项

- **预览版模型风险**：`qwen4-max-preview`、`kimi-k2.8-preview` 等预览版模型服务周期短（EoS 前仅通知14天），且可能随时下线或变更能力；生产环境应优先选用正式版（如 `qwen4-max`）。  
- **模型下线时效性**：正式版模型下线前至少提前3个月公告，但下线节点（启动下线→停止新购→停止服务）存在明确时间差；自“启动下线”日起，QPM/TPM 将逐步缩减，已扩容模型将先恢复默认限流；详见 [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md)。  
- **地域与部署约束**：部分新模型（如 `pixverse-v6-max`、`vidu` 系列）仅在华北2（北京）地域上线；国际站新增美国、德国、日本地域，但模型覆盖不全，需查阅 [地域与部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。  
- **免费额度策略**：启用“免费额度用完即停”后，额度耗尽将返回 `AllocationQuota.FreeTierOnly` 错误；新人免费额度有效期已延长至180天（部分模型），但需以控制台实际展示为准。

## 来源文档

- [Token Plan 功能更新](../../raw/product-updates/release-notes/token-plan-product-updates.md)
- [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md)
- [模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md)
- [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md)
- [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)
- [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)


