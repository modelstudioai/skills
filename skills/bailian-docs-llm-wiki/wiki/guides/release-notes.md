# release notes

百炼平台的 Release Notes 汇总了近期模型上架/下线、核心功能迭代、API 兼容性调整及平台能力升级等关键变更。本文面向开发者，聚焦可操作信息，涵盖新模型支持范围、关键参数行为、调用方式变更、已知限制与迁移建议。所有内容均基于最新生产环境状态，不包含预览或灰度特性。

## 支持的模型/功能

- **新增模型**：2026年11月起，华北2（北京）地域正式上线 `qwen4-max`（服务部署范围：中国内地）、`decision-model`（结构化决策模型）、`qwen-audio-3.1-live`（实时语音对话）、`qwen-audio-3.1-captioner`（音频打标）、`pixverse/pixverse-v6-max-t2v` 与 `pixverse/pixverse-v6-max-it2v`（视频生成）、`vidu/viduq3.1-fast_reference2image`（图片生成）等模型。其中 `qwen4-max` 已全面替代下线的 `qwen4-max-preview`，详见 [模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md)。
- **Agent 平台增强**：Managed Agent 新增 `deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`glm-5.3` 等可选模型；支持用户消息多模态输入（图片、视频、文件），并提供沙箱持久化、定时任务、网页搜索（`web_search`）与读取（`web_fetch`）等内置工具。相关能力详见 [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)。
- **模型平台扩展**：支持图像生成模型（如 Wan / Wanx 系列）和视频生成模型的定制训练；新增强化学习（RL）训练（邀约制）、模型压缩模块、异步任务事件总线（HTTP 回调与 RocketMQ）等能力，详见 [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md)。

## 关键参数

- **`max_tokens` 行为统一**：自 `qwen4-max-preview` / `qwen4-max` 起，Qwen 系列新模型的 `max_tokens` 参数等效于 `max_completion_tokens`，严格限制思考内容与最终回答的 [Token](../concepts/token.md) 总量；开启思考模式时，思考过程占用同一输出预算。存量模型（`qwen4-max-preview` 之前）行为保持不变。该调整对齐 OpenAI 最新协议，详见 [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)。
- **上下文窗口**：多数新模型（如 `kimi-k3.1-pro`、`deepseek-v4.1-flash`、`glm-5.3-flash`、`xiaomi/mimo-v2.6-pro-ultraspeed`）支持 1M [Token](../concepts/token.md) 上下文窗口；`qwen-audio-3.1-realtime-flash` 支持 262,144 [Token](../concepts/token.md)；`qwen-audio-3.1-realtime-plus` 同样为 262,144 Token。
- **输出长度**：`deepseek-v4.1-flash` 系列支持最高 384K 输出长度；`glm-5.3-flash` 系列支持 128K 输出；`qwen4-max` 支持结构化输出与工具调用，但未在文档中明确最大输出长度。

> **注意**：文档 1 中 `qwen-audio-3.1-realtime-plus`（2026-09-20）与 `qwen-audio-3.1-realtime-flash`（2026-10-27）均标注上下文长度为 262,144 Token，但后者额外声明支持“工具调用、联网搜索及声音复刻”，而前者仅提及“Function Calling、联网搜索及声音复刻”。二者能力存在重叠但细节不一致，建议以 `qwen-audio-3.1-realtime-flash` 的完整能力描述为准。

## 使用方式

- **模型调用**：通过标准 API（OpenAI Chat Completions 或 DashScope）调用，需在请求中指定 `model` 字段。Token Plan 用户可在个人版/团队版套餐中直接启用 `qwen4-max`、`deepseek-v4.1-flash-1017` 等模型；语音识别模型（如 `qwen-audio-3.1-asr-flash-*`）需按 [接入语音识别模型](../../token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md) 文档配置。
- **Agent 集成**：Managed Agent 创建会话时，可通过 `agent` 对象覆盖模型、工具、MCP Server 等配置；支持 `sandbox` 参数启用沙箱持久化，`environment_variables` 注入环境变量，`mcp_configs` 为 MCP Server 注入自定义请求头。详细接口见 [创建 Session](../../application-api-reference/managed-agents-api/session-api/session-create.md)。
- **知识库增强**：旗舰版文档知识库支持 Wiki 与本体知识图谱，需单独配置抽取模型（如 `qwen3.8-max`）并按实际 Token 计费，不占用知识库规格费用，详见 [Wiki 与本体知识图谱](../../application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)。

## 限制和注意事项

- **模型下线策略**：预览版模型（含 `preview`、`beta` 标识）自启动下线通知起 14 天后停止服务（EoS）；正式版模型为 3 个月。`qwen4-max-preview` 已于 2026-11-25 下线，所有调用自动路由至 `qwen4-max`，且预览期折扣失效。请参考 [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md) 进行迁移。
- **地域与部署限制**：部分模型（如 `qwen4-max`）明确标注“服务部署范围：中国内地”，暂不支持国际地域；而 `qwen-audio-3.1-live`、`pixverse-v6-max` 等未注明地域限制，需以控制台实际可用区域为准。
- **功能兼容性**：`download_file` 内置工具已于 2026-09-09 下线，由 `mark_artifacts` 替代；`qwen-turbo` 资源包已启动退市流程；企业知识库（旧）已于 2026-07-16 下线。所有变更均影响现有集成逻辑，需及时更新配置与代码。

> **注意**：文档 1 将 `kimi-k3.1-pro` 描述为“3T 级开放权重模型”，而文档 4 在 2025-10-21 条目中提及“千问3-VL-8B-Instruct”等模型支持 SFT 调优，但未提及其他厂商模型是否开放权重。此处“开放权重”属厂商特定表述，百炼平台不提供模型权重下载，仅支持 API 调用与托管微调。

## 来源文档

- [模型上架与更新](../../raw/product-updates/release-notes/newly-released-models.md)
- [Token Plan 功能更新](../../raw/product-updates/release-notes/token-plan-product-updates.md)
- [模型下线机制说明](../../raw/product-updates/release-notes/model-depreciation.md)
- [模型平台功能更新](../../raw/product-updates/release-notes/model-release-notes.md)
- [API 兼容性升级](../../raw/product-updates/release-notes/api-compatibility-upgrade-notice.md)
- [Agent 平台功能更新](../../raw/product-updates/release-notes/application-release-notes.md)


