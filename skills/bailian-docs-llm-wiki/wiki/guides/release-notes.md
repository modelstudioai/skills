# release notes

本页汇总阿里云百炼平台模型与功能的发布动态，涵盖模型上架清单与平台功能更新两个维度。开发者可据此跟踪可用模型规格、能力升级及配套 API/SDK 的演进，便于选型与接入。详细上下架规则与最新功能说明请分别参考[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)与[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 模型上架动态

百炼在华北2（北京）区域持续上架新模型，服务部署范围覆盖中国内地。近期重点上新按模态归类如下：

- 推理模型：`qwen3.7-max-2026-06-08`（新增视觉模态理解，具备多模态交互混合智能体能力）、`qwen3.7-plus` / `qwen3.7-plus-2026-05-26`（视觉-语言能力全面升级，可读取屏幕并操作 GUI）、`deepseek-v4-pro` / `deepseek-v4-flash`（阿里直供）、`kimi/kimi-k2.7-code` 与 `kimi/kimi-k2.7-code-highspeed`（月之暗面直供，后者速度提升 5~6 倍）、`ZHIPU/GLM-5.1` / `ZHIPU/GLM-5`、`xiaomi/mimo-v2.5-pro`、`stepfun/step-3.7-flash`、`vanchin/deepseek-v4-pro`（快手万擎直供）。
- 文生文与视觉理解：`kimi/kimi-k2.6`、`kimi-k2.6`（支持文本、图片与视频输入，思考与非思考模式）。
- 图像生成与编辑：`qwen-image-2.0-pro-2026-06-22`（文字渲染增强，支持最长 1k token 指令）、`wan2.7-image-pro` / `wan2.7-image`（支持 4K 输出与多图参考）。
- 文生/图生/参考生视频：`happyhorse-1.1-t2v` / `i2v` / `r2v`（有声视频，3~15 秒、720P/1080P）、`wan2.7-t2v` / `i2v` / `r2v` / `videoedit`、`pixverse/pixverse-v6` 系列、`vidu/viduq3` 系列、`pixverse/pixverse-c1` 系列。
- 全模态：`qwen3.5-omni-plus` / `qwen3.5-omni-flash` 及 `-realtime` 版本，支持长视频分析、113 种语言识别、36 种语言音频生成、联网搜索与语音打断。
- 文字提取/识别：`qwen3.5-ocr`（128K 上下文，多轮对话）、`fun-asr`（覆盖汉语七大方言与 30 个语种）、`vanchin/deepseek-ocr`。
- 其他模态：3D 生成（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`）、音乐生成（`fun-music-v1`）、音视频翻译（`qwen3.5-livetranslate-flash-realtime`）。

完整上架清单及各模型规格说明见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。模型下线规则与清单详见模型下线机制说明。

## 平台功能更新

平台功能更新按时间倒序排列，以下按功能模块归纳近期关键能力。

### 模型调优与训练

- 强化学习训练（邀约制）：基于奖励信号优化模型策略，5 月 31 日上线。
- 模型压缩：量化算法将全精度微调模型转为低精度版本，降低部署成本，5 月 25 日上线。
- 新增模型类型支持：图像生成模型（Wan / Wanx，5 月 28 日）、视觉理解 VL 模型（1 月 22 日）、视频生成模型（1 月 21 日）。
- 0 代码安全合规强化：文本生成模型调优新增训练流程，5 月 4 日上线。
- 千问3-VL-8B-Instruct / Thinking 支持 SFT（10 月 21 日）；千问2.5、千问3 系列支持 DPO 偏好训练（9 月 12 日）。

### 模型导入与部署

- 模型导入功能国际站上线（6 月 5 日），支持从 OSS 导入 LoRA 微调模型；模型导入 API 同步上线（6 月 3 日）。
- 部署方式新增按模型单元（MU）时长计费，支持预置模型（qwen-flash / qwen-plus 等），1 月 23 日上线；按调用量计费方式支持部署 qwen2.5-7B/14B/32B/72B 调优后模型。

### API 与 SDK

- Responses API 新增[异步调用](../concepts/async-invocation.md)模式（`background=true` 提交长耗时任务并轮询），6 月 1 日上线；文本生成 API 入口聚合 OpenAI Responses 与 Anthropic Messages 分类，5 月 15 日上线。
- 异步任务支持事件总线 EventBridge HTTP 回调与 RocketMQ 主动推送，无需轮询，4 月 23 日上线。
- 新版[智能体应用](../concepts/agent-application.md) DashScope API 首发，支持单轮/多轮、流式、文件问答、视觉理解，5 月 11 日上线。
- API 鉴权新增生成临时 [API Key](../concepts/api-key.md) 文档，避免不可信环境下永久 Key 泄露，6 月 3 日上线。
- 多模态交互开发套件：服务端 Java SDK（4 月 28 日）、移动端 Android SDK（4 月 14 日）、Linux C++ SDK（2 月 28 日）、Android/iOS Lite SDK（2 月 6 日）、RTOS C SDK License 模式（4 月 9 日）相继上线。

### 应用与组件

- UI 设计器上线，集成魔笔低代码能力，可视化拖放构建网页 UI 应用，4 月 1 日上线。
- 记忆库 Memory 2.0：自动提取记忆片段与用户画像，支持多应用共享同一记忆库，3 月 20 日上线。
- [知识库](../concepts/knowledge-base.md) RAG：检索调用全量投递至 SLS 日志服务，支持审计/排查/统计/告警，4 月 24 日上线；Retrieve 接口新增排序模型与指令干预模式（2 月 5 日）。
- 应用组件 Prompt 工程 API 上线，提供 Prompt 模板管理能力，4 月 7 日上线。
- 联网检索 Agent 官方应用上线，3 月 19 日上线；通义听悟 Agent 新增特惠 ASR 资源包与工业生产指令转写 WebSocket 协议。
- 通义多模态翻译 API 参考上线（5 月 26 日），网页翻译 JSSDK 上线（2 月 6 日）。
- 全妙 PPT 生成 API 模块开放完整接口，3 月 19 日上线。

### 模型评测与观测

- 模型评测新增排行榜与综合评测，支持 BLEU_4 等评分方法，6 月 9 日上线；排行榜支持多模型多维度对比（12 月 15 日）；新增多种评估器（12 月 15 日）。
- 模型观测新增推理日志查看（11 月 6 日）、告警与通知（6 月 5 日）、高级监控模式（分钟级低延时刷新，4 月 18 日）。

### 接入客户端与生态

- 接入客户端开发工具新增 Kilo CLI，支持 [Token](../concepts/token.md) Plan / Coding Plan / 按量计费三种接入方式，2 月 22 日上线。
- Spring AI Alibaba 调用百炼应用文档上线，6 月 1 日上线。
- 上线官方 MCP 服务，支持平台内集成与外部第三方接入（如 Amap Maps），2 月 6 日上线；国际站官方插件新增 Image Generation（2 月 6 日）。
- CosyVoice 声音复刻 API 接口详情上线，2 月 6 日上线。

### 计费与免费额度

- [Token](../concepts/token.md) Plan 团队版团队管理上线，支持 SSO/钉钉登录、席位分配、Credits 用量监控，5 月 8 日上线。
- 新增免费额度用完即停功能，避免额外费用，7 月 29 日上线。
- 降价动态：qwen-max 输入价格降低 88%、输出价格降低 84%（2025 年 2 月）；千问 VL 系列降价最高 85%（2024 年 12 月）；deepseek-v4-pro `cached_token` 单价调整为 1 元/百万 token（2026 年 4 月 29 日）。

## 限制和注意事项

- `qwen3.7-max-preview` / `qwen3.7-max-2026-05-17` 仅支持纯文本输入，仅支持思考模式；`qwen3.6-max-preview` 仅支持纯文本输入，不支持图像与视频输入，默认开启思考模式。
- `kimi/kimi-k2.7-code` 仅支持思考模式，专为长程软件工程任务优化。
- 强化学习训练当前为邀约制开放，需联系平台获取权限。
- 模型下线遵循既定机制，使用前应核对模型规格的上下架状态，避免调用已下线模型导致失败。
- 免费额度用完即停功能启用后，额度耗尽将返回错误 code `AllocationQuota.FreeTierOnly`。

> **注意**：[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)以平台能力演进为主线，而[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)以具体模型规格上架为主线，二者时间口径与粒度不同。选型时应以模型上下架清单的规格与时间为准，功能更新仅作能力参考。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


