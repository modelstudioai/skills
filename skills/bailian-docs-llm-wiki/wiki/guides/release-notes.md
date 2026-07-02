# release notes

百炼平台持续迭代模型能力与平台功能，涵盖推理模型上新、[多模态](../concepts/multimodal.md)生成、模型调优与部署、API 接口扩展、[计费](../concepts/billing.md)调整等多个维度。本页汇总了[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)和[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)两份原始文档中的关键变更，帮助开发者快速了解平台最新动态。

## 模型上新与迭代

百炼模型广场持续引入新模型，覆盖推理、[多模态](../concepts/multimodal.md)、视频生成、图像生成、语音等类型。模型下线规则及清单请参考[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)。

### 推理模型

近期上架的主要推理模型：

| 模型 | 上架时间 | 说明 |
|------|----------|------|
| qwen3.7-max | 2026-05-21 | Qwen Max 新一代旗舰，默认开启思考模式，支持显式缓存 |
| qwen3.7-plus | 2026-06-01 | 视觉-语言能力全面升级，支持[多模态](../concepts/multimodal.md)交互混合智能体 |
| qwen3.6-plus | 2026-04-02 | 代码开发能力重点升级（Agentic Coding），泛化推理增强 |
| qwen3.6-flash | 2026-04-16 | Flash 系列，智能体编程、数学推理和空间智能显著提升 |
| deepseek-v4-pro / v4-flash | 2026-04-24 | DeepSeek-V4 系列，阿里直供 |
| kimi/kimi-k2.7-code | 2026-06-15 | 月之暗面直供，专为长程软件工程任务优化 |
| kimi-k2.6 | 2026-04-21 | 支持文本/图片/视频输入，思考与非思考模式 |
| glm-5.1 | 2026-04-14 | 智谱模型，200K 上下文，最大输出 128K [Token](../concepts/token.md) |
| xiaomi/mimo-v2.5-pro | 2026-05-19 | 小米直供，通用智能体与长程任务能力提升 |
| stepfun/step-3.7-flash | 2026-05-29 | 阶跃星辰直供，搜索/Agent/编码/多模态全面升级 |

### 多模态与全模态模型

- **qwen3.5-omni-plus / flash**（2026-03-30）：全模态大模型，支持 113 种语言识别、36 种语言音频生成，可处理 3 小时音频及 1 小时视频输入
- **qwen3.5-omni-plus-realtime / flash-realtime**（2026-03-30）：实时多模态模型，原生支持联网搜索、语音打断
- **qwen3.5-livetranslate-flash-realtime**（2026-05-19）：音视频实时翻译，识别 60 种语言，翻译为 29 种语言音频

### 视频生成模型

平台提供多家视频生成模型，按任务类型分为文生视频、图生视频、参考生视频和视频编辑：

- **万相 2.7 系列**（2026-04-03 起）：`wan2.7-t2v`（文生视频）、`wan2.7-i2v`（图生视频，支持首帧/首尾帧/续写）、`wan2.7-r2v`（参考生视频，支持主体参考和音色定制）、`wan2.7-videoedit`（视频编辑）
- **HappyHorse 1.0/1.1 系列**（2026-04-27 / 06-22）：支持有声视频生成，3~15 秒，720P/1080P
- **爱诗 PixVerse v6/C1 系列**（2026-03-29 / 04-13）：支持提示词智能分镜，打斗与特效强化
- **Vidu 系列**（2026-04-29）：参考生视频和首帧生视频

### 图像生成与 3D 模型

- **qwen-image-2.0-pro**：持续迭代快照，文字渲染和写实质感不断增强
- **wan2.7-image-pro / wan2.7-image**（2026-04-01）：支持文生图、图像编辑、多图参考生成，Pro 系列支持 4K 输出
- **Tripo-H3.1 / P1.0**（2026-04-29）：3D 生成模型，支持文生 3D、单图/多图生 3D

### 其他模型

- **qwen3.5-ocr**（2026-06-16）：文字提取模型，128K 上下文，多轮对话，覆盖多种国内外卡证
- **fun-music-v1**（2026-05-06）：音乐生成大模型，支持根据创作要求或歌词生成整首歌曲
- **fun-asr**（2026-04-16）：语音识别升级，覆盖汉语七大方言，支持 30 个语种

## 平台功能更新

### 模型调优

模型调优持续扩展支持的模型类型和训练方式，详见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)：

- **强化学习训练**（2026-05 邀约制）：支持基于奖励信号优化模型策略
- **图像生成模型调优**（2026-05）：支持 Wan/Wanx 系列定制训练
- **0 代码安全合规强化**（2026-05）：无需编码即可强化大模型安全合规能力
- **DPO 偏好训练**（2025-09）：千问 2.5/3 系列支持，通过负反馈降低幻觉
- **视觉理解 / 视频生成模型调优**（2026-01）：支持 VL 和万相系列模型定制训练
- **模型压缩**（2026-05）：使用量化算法将全精度模型转为低精度版本，降低部署成本

### 模型部署

- **模型单元（MU）部署**（2025-10）：按时间[计费](../concepts/billing.md)，灵活调整性能，成本可预测
- **按调用量[计费](../concepts/billing.md)部署**（2024-12）：支持 qwen2.5-7B/14B/32B/72B 等调优后模型
- **API 部署预置模型**（2026-01）：支持 qwen-flash/qwen-plus 等预置模型部署

### API 与接口

- **Responses API 异步调用**（2026-06）：通过 `background=true` 提交长耗时任务
- **临时 [API Key](../concepts/api-key.md)**（2026-06）：避免不可信环境下永久 Key 泄露
- **模型导入 API**（2026-06）：涵盖导入任务与自定义模型对象的完整接口
- **文本生成 API 聚合**（2026-05）：入口新增 OpenAI Responses 与 Anthropic Messages 接口分类
- **异步任务 EventBridge 回调**（2026-04）：支持 HTTP 回调与 RocketMQ，无需轮询
- **Batch 任务通知**（2024-12）：支持 Callback 回调和 EventBridge 消息
- **Context Cache**（2024-12）：推理时减少重复运算，降低使用成本

### 模型观测与评测

- **模型观测**（2025-01 起）：监测模型使用与性能，支持推理日志查看、告警通知、高级监控模式（分钟级刷新）
- **模型评测**（2025-12 起）：排行榜功能、综合评测（BLEU、ROUGE 等）、多种评估器
- **模型用量看板**（2025-12）：集中展示免费额度与调用量统计

### 应用与组件

- **记忆库 Memory 2.0**（2026-03）：自动从对话提取记忆片段与用户画像，支持多应用共享
- **知识库 RAG 日志与监控**（2026-04）：检索调用全量投递至 SLS，支持审计/排查/告警
- **Prompt 工程 API**（2026-04）：提供 Prompt 模板管理能力
- **UI 设计器**（2026-04）：集成魔笔低代码，可视化拖放构建网页 UI
- **MCP 服务**（2026-02）：官方 MCP 服务，支持平台内集成与第三方接入
- **多模态交互开发套件**：已上线 Java / Android / iOS / Linux C++ / RTOS SDK

### 开发者工具

- **Spring AI Alibaba 集成**（2026-06）：使用 Spring AI Alibaba 框架调用百炼智能体和工作流
- **Kilo CLI**（2026-02）：支持 [Token](../concepts/token.md) Plan / Coding Plan / 按量计费三种方式接入
- **[Token](../concepts/token.md) Plan 团队版**（2026-05）：支持 SSO/钉钉登录、席位分配、Credits 用量监控

## 计费变更

百炼平台多次调整模型定价，整体趋势为降价：

- **qwen-max 降价 84%~88%**（2025-02）：输入降至 0.0024 元/千 Token，输出降至 0.0096 元/千 Token
- **千问 VL 系列降价最高 85%**（2024-12）
- **qwen2.5-14b/7b-instruct 降价 50%**（2025-01）
- **部分模型由免费转计费**：qwen2.5-3b-instruct、DeepSeek 系列等陆续转为计费

> **注意**：计费信息可能随时调整，最新价格以[百炼控制台模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)为准。

## 注意事项

- 模型快照版本（如 `qwen3.7-max-2026-06-08`）固定模型能力，适用于需要稳定版本的生产环境
- 不带日期后缀的模型名（如 `qwen3.7-max`）会指向最新版本，行为可能随迭代变化
- 部分模型仅支持纯文本输入（如 qwen3.6-max-preview），使用前请确认模态支持情况
- 新人免费额度有有效期限制，可启用"用完即停"功能避免超额计费（返回错误码 `AllocationQuota.FreeTierOnly`）
- 第三方直供模型（如 Kimi、DeepSeek-快手万擎、智谱 GLM、小米 MiMo）的计费和 SLA 可能与阿里直供模型不同

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


