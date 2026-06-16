# release notes

百炼平台持续迭代，功能更新和模型上下架是开发者最需要关注的两大动态。本页汇总了平台的功能发布记录与模型变更信息，帮助开发者快速了解最新能力、计费调整及下线计划，以便及时适配业务。

## 功能更新概览

百炼平台的功能更新覆盖模型推理、模型调优与部署、应用开发、API 接口、计费策略等多个模块。完整的功能更新时间线请参见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

### 模型推理与部署

- **[模型部署](../concepts/model-deployment.md)**：支持按模型单元（MU）时长计费和按调用量计费两种方式，可灵活调整性能并获得可预测的固定成本。预置模型（如 qwen-flash、qwen-plus）也支持通过 API 部署。
- **模型导入**：支持从 OSS 导入 LoRA 微调模型，已上线国际站，并提供完整的 API 接口（导入任务与自定义模型对象）。
- **模型压缩**：使用量化算法将全精度微调模型转为低精度版本，降低部署成本。
- **Context Cache**：上下文缓存功能可减少重复运算量，提升响应速度并降低使用成本。

### 模型调优

- 支持 SFT（全参微调 + LoRA 高效微调）、DPO 偏好训练、强化学习训练（邀约制）。
- 支持的模型类型涵盖文本生成、视觉理解（VL）、视频生成、图像生成。
- 新增 0 代码安全合规强化训练流程。

### API 与接口

- **Responses API**：新增异步调用模式，通过 `background=true` 提交长耗时任务并轮询结果。
- **[异步任务](../concepts/async-task.md)**：支持通过事件总线 EventBridge 主动推送任务完成事件（HTTP 回调与 RocketMQ），无需轮询。
- **临时 API Key**：在不可信环境下避免永久 API Key 泄露。
- **文本生成 API**：入口聚合 OpenAI Chat Completions、OpenAI Responses、Anthropic Messages 等多类接口。
- **Batch**：支持任务完成通知（Callback 回调和 EventBridge 消息）。

### 应用开发

- **知识库 RAG**：检索调用全量投递至 SLS 日志服务，Retrieve 接口新增排序模型与指令干预模式。
- **记忆库 Memory 2.0**：自动从对话提取记忆片段与用户画像，支持多应用共享。
- **MCP 服务**：上线官方 MCP 服务，支持平台内集成与外部第三方接入。
- **多模态交互开发套件**：覆盖 Java SDK、Android SDK、Linux C++ SDK、iOS Lite SDK、RTOS C SDK 等多端。
- **UI 设计器**：集成魔笔低代码能力，可视化拖放构建网页 UI 应用。
- **[Prompt 工程](../concepts/prompt-engineering.md)**：应用组件新增 Prompt 模板管理 API。

### 模型观测与评测

- **模型观测**：支持查看推理日志、告警与通知、高级监控模式（分钟级刷新）。
- **模型评测**：新增排行榜功能和多种评估器（字符串匹配、文本相似度、模型打分等）。
- **模型用量**：集中展示各模型免费额度及调用量统计。

### 计费调整

平台多次对千问系列和 DeepSeek 系列模型进行降价调整，部分模型降幅最高达 88%。免费额度方面，新增"用完即停"功能，启用后免费额度耗尽将返回错误码 `AllocationQuota.FreeTierOnly`，避免产生额外费用。详细的价格变动可在 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 的计费章节中查阅。

## 模型上下架

模型上下架信息记录了百炼平台新增模型的时间、规格与能力说明。模型下线规则及清单请参考模型下线机制说明文档。完整的模型上架列表请参见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

### 推理模型

| 时间 | 模型 | 说明 |
|------|------|------|
| 2026-06-10 | qwen3.7-max-2026-06-08 | Qwen3.7 Max 旗舰，新增视觉模态理解，支持多模态交互混合智能体 |
| 2026-06-01 | qwen3.7-plus | 全面升级视觉-语言能力，支持 GUI 操作、视觉代码生成 |
| 2026-05-21 | qwen3.7-max | 新一代旗舰，编程与办公能力突出，支持显式缓存 |
| 2026-04-24 | deepseek-v4-pro / flash | DeepSeek-V4 系列，阿里直供 |
| 2026-04-20 | qwen3.6-max-preview | Qwen3.6 最大闭源模型，Coding 与 Agent 能力提升 |
| 2026-04-16 | qwen3.6-flash | 相较 Qwen3.5-Flash 显著提升，空间智能增强 |

### 全模态与语音模型

| 时间 | 模型 | 说明 |
|------|------|------|
| 2026-03-30 | qwen3.5-omni-plus / flash | 支持长视频分析、113 种语言识别、36 种语言音频生成 |
| 2026-03-30 | qwen3.5-omni-plus-realtime | 实时多模态，原生联网搜索，支持语音打断 |
| 2026-05-19 | qwen3.5-livetranslate-flash-realtime | 多语言音视频实时翻译，识别 60 种语言 |
| 2026-05-06 | fun-music-v1 | 百聆音乐生成大模型，支持中英文歌曲创作 |

### 视频生成模型

平台集成了多家视频生成模型，覆盖文生视频、图生视频、首尾帧生视频、参考生视频、视频编辑等任务类型：

- **万相系列**：wan2.7-t2v / i2v / r2v / videoedit，支持多模态输入与多种分辨率。
- **爱诗 PixVerse**：v6 / C1 系列，支持智能分镜、打斗特效强化，真人与动漫风格。
- **Vidu**：viduq3-pro / turbo / viduq2 系列，涵盖文生视频到参考生视频全链路。
- **HappyHorse**：支持有声视频生成，720P/1080P，3-15 秒。
- **可灵 Kling**：V3 系列，支持文生视频、图生视频、参考生视频和视频编辑。

### 图像生成与 3D 模型

- **万相 2.7 图像**：wan2.7-image-pro / image，支持文生图、图生组图、图像编辑、多图参考生成，Pro 支持 4K 输出。
- **千问图像**：qwen-image-2.0-pro，融合图片生成与编辑，多语言图内文字生成。
- **可灵 V3 图像**：支持文生图与参考图生图。
- **Tripo 3D**：H3.1 高精度（最高 200 万面）和 P1.0 专业版（最高 2 万面），支持文生 3D、单图/多图生 3D。

### 第三方直供模型

百炼平台接入了多家第三方模型提供商的直供服务：

- **DeepSeek**（快手万擎直供）：deepseek-v4-pro、v3.2-think、v3.1-terminus、r1 等
- **Kimi**（月之暗面直供）：kimi-k2.6，支持文本/图片/视频输入与思考模式
- **GLM**（智谱直供）：glm-5.1 / glm-5，200K 上下文，128K 最大输出
- **MiMo**（小米直供）：mimo-v2.5-pro，通用智能体与长程任务能力提升
- **Step**（阶跃星辰直供）：step-3.7-flash，搜索/Agent/编码/多模态全面升级

## 注意事项

- **模型下线机制**：百炼平台有明确的模型下线规则，请关注官方下线通知，及时迁移到推荐的替代模型。
- **快照版本**：部分模型提供日期快照版本（如 `qwen3.7-max-2026-05-20`），功能与同名最新版一致，适合需要固定版本的生产环境。
- **计费变动**：模型价格可能随版本更新调整，建议定期查看控制台最新计费信息。

> **注意**：功能更新记录（[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）侧重平台能力变更，模型上架记录（[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)）侧重具体模型规格。两者时间线独立维护，如发现模型上架时间与功能上线时间不完全一致属正常现象。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)




