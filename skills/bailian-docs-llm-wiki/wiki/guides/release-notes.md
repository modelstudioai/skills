# release notes

阿里云百炼平台的 release notes 由两条互补的时间线组成：一是**平台功能更新**（计费、部署、调优、知识库 RAG、SDK/接入工具、API 等能力的演进），二是**模型上下架与更新**（各模型的上架时间、服务部署范围、模型规格与能力说明）。开发者可据此追踪能力可用性、模型可调用状态与计费/下线变更，避免因模型下线或网关变更导致线上调用中断。

## 两类更新的定位

release notes 覆盖两个正交的维度，查询时应按需求选择对应文档：

- **平台功能动态**：记录平台侧能力的上线与调整，按 `年 → 月 → 日` 组织，每条含"功能模块 / 功能点 / 功能说明"。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型上架清单**：按地域（如华北2（北京））列出每个模型的上架时间、服务部署范围、模型规格（如 `qwen3.7-max`、`kimi/kimi-k2.7-code`）及能力说明。详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

> **注意**：模型**上架**信息在上表中维护，而模型**下线**规则与清单不在此列，需单独参考 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)。功能更新文档中也频繁出现"部分老旧模型下线通知""网关变更通告"等公告，建议在集成前定期核对，防止依赖的模型或域名失效。

## 平台功能更新的关键脉络

从 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 可提炼出几条对开发者影响较大的主线：

- **[模型调优与部署](../concepts/fine-tuning-and-deployment.md)**：陆续新增视觉理解（VL）、视频生成、图像生成模型的定制训练支持；DPO 偏好训练、强化学习（RL，邀约制）训练；以及按模型单元（MU）时长计费的部署方式与预置模型部署（qwen-flash / qwen-plus 等）。
- **API 能力**：文本生成 API 入口聚合 OpenAI Responses、Anthropic Messages 等分类；Responses API 新增 `background=true` 异步调用；异步任务支持事件总线 EventBridge 回调，无需轮询。
- **知识库 RAG**：上线知识检索服务、知识问答服务，检索调用全量投递 SLS 日志，Retrieve 接口新增排序模型与指令干预模式。
- **接入与计费**：新增 Codex、Kilo CLI 等客户端接入；Token Plan 团队版团队管理与共享用量包；Coding Plan 联网搜索 MCP 升级；API Key 加密存储与业务空间专属推理域名升级。
- **地域接入**：新增美国、德国、日本等地域与服务部署范围，跨地域部署时需确认目标模型的服务部署范围。

## 模型上架的读法与关键字段

[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 的每一行都对应一个可调用的模型规格，集成时重点关注：

- **模型规格**：即调用时使用的 `model` 名称，例如推理模型 `qwen3.7-max`、`qwen3.7-plus`、`deepseek-v4-pro`、`kimi/kimi-k2.7-code`、`ZHIPU/GLM-5.1`；文字提取 `qwen3.5-ocr`；语音合成 `qwen-audio-3.0-tts-plus/flash` 等。三方厂商模型通常带 `厂商/` 前缀（如 `vidu/`、`pixverse/`、`stepfun/`、`xiaomi/`）。
- **快照版本**：形如 `qwen3.7-max-2026-05-20`、`wan2.7-t2v-2026-04-25` 的带日期后缀模型为快照版，能力与主版本一致但版本锁定，适合对稳定性敏感的生产环境。
- **服务部署范围**：当前上架清单多为"中国内地"，跨地域调用前务必核对。
- **模态与模式限制**：部分模型有明确约束，例如 `qwen3.6-max-preview` 仅支持纯文本输入、不支持图像与视频输入且默认开启思考模式；`kimi/kimi-k2.7-code` 仅支持思考模式。

## 限制与注意事项

- **计费与优惠会随时间调整**：如 `deepseek-v4-pro` 的 `cached_token` 单价曾调整为 1 元/百万 token（标准 `input_token` 不变），GLM-5.2 Fast mode 降价、上下文缓存降价等均以对应公告为准，release notes 中的价格描述可能滞后。
- **模型可能延期或提前下线**：功能更新中同时存在"部分老旧模型下线通知"与"部分老旧模型延期下线通知"，同一批模型的下线时间可能被修订，务必以最新公告为准。
- **两份文档存在时间粒度差异**：功能更新文档到具体功能点，模型清单文档到具体模型规格；排查某能力是否可用时，建议交叉比对 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 与 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 两处。
- **以控制台/API 实际返回为准**：release notes 是变更记录而非实时状态，最终的可调用模型列表、配额与地域支持应以控制台模型广场和 API 返回为准。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


