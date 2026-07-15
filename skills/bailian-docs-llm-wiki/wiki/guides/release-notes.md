# release notes

本页汇总百炼平台的功能更新与模型上下架动态，帮助开发者快速跟踪平台能力演进、新模型可用性以及影响调用的变更（下线、降价、网关调整等）。内容分为两条主线：平台功能迭代（[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)）与模型规格的上架/更新记录（[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)）。建议在集成前先核对相关模型的最新状态与下线机制。

## 两类更新说明

- **平台功能更新**：记录计费方案、API 能力、模型调优/部署、知识库 RAG、多模态套件、接入工具（如 Codex、Kilo CLI）等模块的迭代，按年份和月份倒序排列。详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。
- **模型上下架与更新**：记录各地域（如华北2/北京）新上架模型的类型、时间、服务部署范围（如「中国内地」）与模型规格。详见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 平台功能动态（要点）

功能更新按「日期 / 功能模块 / 功能点 / 功能说明」组织，覆盖的主要方向包括：

- **计费与套餐**：团队版共享用量包（跨坐席共享 Credits）、Coding Plan Pro 首月特惠、上下文缓存降价等。
- **API 能力**：Responses API 异步调用（`background=true` 提交长耗时任务并轮询）、文本生成 API 聚合 OpenAI Responses 与 Anthropic Messages 接口、异步任务支持 EventBridge 回调与 RocketMQ、临时 API Key 生成、API Key 加密存储。
- **模型调优与部署**：新增强化学习（RL）训练（邀约制）、图像/视频/视觉理解（VL）模型定制训练、DPO 偏好训练、模型压缩（量化降精度）、模型导入（从 OSS 导入 LoRA）、按模型单元（MU）时长计费、PTU 长输入与前缀缓存。
- **知识库 RAG**：知识检索服务、知识问答服务、知识库日志与监控（投递至 SLS）。
- **接入工具与生态**：新增 Codex、Kilo CLI 客户端接入，官方 MCP 服务，多模态交互开发套件（Java/Android/iOS/Linux C++/RTOS C SDK）。

上述条目的完整时间线请查阅 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中的「功能动态」章节。

## 模型上架动态（要点）

模型上架记录覆盖多种模型类型，示例包括：

- **推理/文本模型**：qwen3.7-max 系列、qwen3.6 系列（flash/plus/max-preview/27b）、DeepSeek-V4 系列（pro/flash）、Kimi K2.6/K2.7-code、GLM-5/5.1、MiMo-V2.5-Pro、Step 3.7 Flash 等第三方直供模型。
- **多模态与生成**：Qwen-Image-2.0（文生图/图像编辑融合）、万相 2.7（文生/图生/参考生视频、视频编辑、图像生成与编辑）、HappyHorse（有声视频，3~15 秒、720P/1080P）、Vidu / 爱诗（Pixverse）视频系列、Tripo 3D 生成、Fun-Music 音乐生成。
- **语音与翻译**：Qwen-Audio-3.0（realtime/tts，Flash 版首包延时 <200ms）、Fun-ASR（覆盖 30 语种、七大方言）、qwen3.5-livetranslate（识别 60 种语言、翻译为 29 种语言音频）。
- **文字提取**：qwen3.5-ocr（128K 上下文、多轮对话、卡证信息抽取）。

## 关键字段与使用方式

- **服务部署范围**：模型上架条目会标注部署范围（如「中国内地」）与地域（如华北2/北京）。集成前需确认目标模型在所需地域可用。平台已新增美国、德国、日本等地域与部署范围。
- **模型规格命名**：带日期后缀的规格（如 `qwen3.7-max-2026-05-20`、`wan2.7-t2v-2026-06-12`）为快照版本，能力通常与主版本一致，用于锁定行为、便于灰度与回滚。
- **第三方直供模型**：使用 `厂商/模型` 形式的 ID（如 `kimi/kimi-k2.7-code`、`ZHIPU/GLM-5.1`、`vidu/viduq3-fast_reference2image`），调用文档参见各模型对应指南。

## 限制与注意事项

- **模型下线**：平台持续发布老旧/长尾模型下线与延期下线通知。下线规则与完整清单请以 [模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation) 为准，及时迁移以避免调用中断。
- **网关变更**：存在网关变更通告与业务空间专属推理 API 域名升级，可能影响既有调用地址，需关注公告并同步更新配置。
- **免费额度**：启用「免费额度用完即停」后，新人免费额度耗尽将无法继续调用（返回错误 `code: AllocationQuota.FreeTierOnly`），避免产生额外费用。
- **能力约束**：部分推理模型（如 qwen3.6-max-preview、qwen3.7-max 系列）仅支持纯文本输入、默认或仅支持思考模式，不支持图像与视频输入，接入前需核对模态支持。

> **注意**：两篇文档的日期跨度较大且更新频繁，部分记录已进入 2026 年。计费、模型可用性与下线时间以官方最新公告和控制台实际状态为准；本页为聚合快照，可能滞后于 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 与 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 的原始内容。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


