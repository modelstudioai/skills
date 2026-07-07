# release notes

百炼平台持续迭代模型能力与平台功能，本页汇总平台功能更新与模型上下架动态。功能更新涵盖模型调优、部署、评测、观测、API 扩展及 SDK 支持等模块；模型动态则记录各类模型（推理、视觉、视频生成、语音、3D 等）的上架时间与能力说明。完整时间线请参阅 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 和 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 推理与文本生成模型

百炼持续引入和升级推理模型，覆盖自研千问系列与第三方直供模型：

- **Qwen3.7 Max** — 2026 年 5 月上线，千问 Max 系列新一代旗舰，默认开启思考模式，支持显式缓存和 Function Calling，在编程、办公与长周期自主执行方面表现突出。6 月快照新增视觉模态理解能力。
- **Qwen3.6 系列** — 包含 qwen3.6-max-preview、qwen3.6-plus、qwen3.6-flash 等，重点强化智能体编程（Agentic Coding）和数学推理能力，Flash 版本还增强了空间智能与物体定位。
- **Qwen3.5 系列** — qwen3.5-plus 为原生视觉语言模型，qwen3.5-omni 系列支持全模态（音视频交互、113 种语言识别、36 种语言音频生成）。
- **DeepSeek-V4** — 含 deepseek-v4-pro（旗舰）和 deepseek-v4-flash（轻量高速），另有快手万擎直供版本。
- **第三方直供** — Kimi K2.6/K2.7（月之暗面）、GLM-5/5.1（智谱）、MiMo-V2.5-Pro（小米）、Step 3.7 Flash（阶跃星辰）等均已上架。

详细模型列表及上架时间见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 视频与图像生成模型

多媒体生成是百炼近期重点扩展方向，主要模型家族包括：

- **万相 2.7** — 覆盖文生视频（wan2.7-t2v）、图生视频（wan2.7-i2v）、参考生视频（wan2.7-r2v）、视频编辑（wan2.7-videoedit）及图像生成与编辑（wan2.7-image-pro/image），支持 4K 输出与多图参考。
- **HappyHorse 1.0/1.1** — 支持有声视频生成（3-15 秒，720P/1080P），涵盖文生视频、图生视频、参考生视频及视频编辑。
- **爱诗 PixVerse** — C1 和 V6 两代产品线，支持文生视频、首帧/首尾帧生视频、参考生视频，C1 版本新增提示词智能分镜。
- **Vidu** — 参考生视频与首帧生视频系列（Q3/Q2 Pro 等）。
- **千问文生图** — qwen-image-2.0-pro 持续迭代，增强文字渲染、真实质感和语义遵循能力。
- **Tripo 3D** — 支持文生 3D、单图/多图生 3D，H3.1 版本最高 200 万面。

## 语音、OCR 与其他模态

- **全模态 Qwen-Omni** — qwen3.5-omni-plus/flash 支持长视频分析、会议纪要、字幕输出，实时版本支持语音打断与联网搜索。
- **实时语音翻译** — qwen3.5-livetranslate-flash-realtime 可识别 60 种语言并实时翻译为 29 种语言音频。
- **Fun-ASR** — 实时语音识别，覆盖汉语七大方言及 30 个语种，增强古诗词和标点预测。
- **文字提取** — qwen3.5-ocr 基于 Qwen3.5 架构，128K 上下文，覆盖多种国内外卡证信息抽取。
- **CosyVoice 声音复刻** — 支持音色复刻任务创建与查询。
- **Fun 音乐大模型** — fun-music-v1 支持中英文歌曲生成。

## 平台功能更新

### 模型调优与部署

- **调优能力扩展** — 先后新增视觉理解（VL）、视频生成、图像生成模型类型支持，并增加 DPO 偏好训练和强化学习训练（邀约制）。0 代码安全合规强化功能可直接提升模型安全能力。
- **模型部署** — 支持按模型单元（MU）时长计费和按调用量计费两种模式，可部署预置模型（qwen-flash/qwen-plus 等）及调优后模型。
- **模型导入** — 支持从 OSS 导入 LoRA 微调模型，已在国际站上线，并开放完整 API。
- **模型压缩** — 使用量化算法将全精度模型转为低精度版本，降低部署成本。

### 模型观测与评测

- **模型观测** — 支持推理日志查看、分钟级高级监控模式、告警与通知、用量统计看板。
- **模型评测** — 新增排行榜（Leaderboard）和综合评测功能，覆盖 BLEU、ROUGE 等多种评估器。

### API 与开发工具

- **Responses API** — 新增[异步调用](../concepts/async-invocation.md)模式（background=true 提交长耗时任务并轮询）。
- **异步任务回调** — 支持 EventBridge HTTP 回调与 RocketMQ，无需轮询。
- **Context Cache** — 减少重复运算、提升响应速度、降低使用成本。
- **临时 API Key** — 在不可信环境下避免永久 API Key 泄露。
- **Batch API** — 支持任务通知功能。
- **兼容接口** — 文本生成 API 入口聚合 OpenAI Responses 与 Anthropic Messages 分类。
- **MCP 服务** — 上线官方 MCP 服务，支持平台内集成与第三方接入。
- **Spring AI Alibaba** — 支持调用百炼智能体与工作流应用。
- **Kilo CLI** — 支持 Token Plan/Coding Plan/按量计费三种方式接入。

### 应用与组件

- **记忆库 Memory 2.0** — 自动从对话提取记忆片段与用户画像，支持多应用共享。
- **知识库 RAG** — 检索调用支持 SLS 日志审计，Retrieve 接口新增排序模型与指令干预模式。
- **Prompt 工程** — 应用组件新增 Prompt 模板管理 API。
- **UI 设计器** — 集成魔笔低代码能力，可视化拖放构建应用 UI。
- **[多模态](../concepts/multimodal.md)交互 SDK** — 覆盖 Web（JS SDK）、Android、iOS、Linux C++、RTOS C 等平台。
- **通义听悟 Agent** — 新增特惠 ASR 资源包与工业生产指令转写 WebSocket 协议。

## 计费变动要点

百炼持续推进模型降价，主要变动包括：

- qwen-max 输入降价 88%、输出降价 84%（2025 年 2 月）
- 千问 VL 系列降幅最高 85%（2024 年 12 月）
- qwen2.5-14b/7b-instruct 降价 50%（2025 年 1 月）
- 部分模型（qwen2.5-3b-instruct、DeepSeek 系列等）由免费体验转为计费
- deepseek-v4-pro cached_token 单价调整为 1 元/百万 token
- 新增推理资源包优惠活动与上下文缓存降价

> **注意**：模型价格随时间调整，上述价格仅反映公告时点。最新计费以百炼控制台模型广场页面为准。

## 模型下线机制

模型下线遵循统一的退市流程，详见 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 中引用的模型下线机制说明。下线前会提前公告通知，建议开发者关注公告并及时迁移到推荐替代模型。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


