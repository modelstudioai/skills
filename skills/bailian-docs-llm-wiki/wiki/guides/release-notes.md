# release notes

阿里云百炼平台持续迭代模型广场与控制台能力，本页汇总近期新上架 / 下架的模型规格、平台功能动态以及计费调整。开发者可据此判断当前可用模型清单、API 兼容形态以及调优 / 部署 / 监控能力的演进，避免在代码中引用已下线规格或错过更优的替代方案。详细的模型下线规则见[模型下线机制说明](https://help.aliyun.com/zh/model-studio/model-depreciation)，平台侧的功能动态时间线见[模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)，模型上下架清单见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 最新模型上下架（中国内地，2026 年）

模型规格按「上架日期」倒序，仅列出代表性快照版本，完整快照命名请以百炼控制台模型广场为准。

| 类型 | 上架日期 | 模型规格 | 关键能力 |
| --- | --- | --- | --- |
| 推理（文本 + 视觉） | 2026-06-10 | `qwen3.7-max-2026-06-08` | Qwen3.7 系列规模最大，新增视觉模态理解与多模态交互混合智能体能力 |
| 参考生视频 | 2026-06-08 | `pixverse/pixverse-v6-r2v` | 多参考图生视频，支持多宫格分镜拼接图一键转视频 |
| 推理 | 2026-06-01 | `qwen3.7-plus` / `qwen3.7-plus-2026-05-26` | 视觉-语言全面升级，保留编码 / 工具调用 / GUI 操作等智能体能力 |
| 推理 | 2026-05-29 | `vanchin/deepseek-v4-pro` | 快手万擎直供的 DeepSeek 推理服务 |
| 推理 | 2026-05-29 | `stepfun/step-3.7-flash` | 阶跃星辰直供，搜索 / Agent / 编码 / 多模态全面升级 |
| 推理 | 2026-05-25 | `qwen3.7-max-preview` / `qwen3.7-max-2026-05-17` | 仅纯文本，仅思考模式 |
| 推理 | 2026-05-21 | `qwen3.7-max` / `qwen3.7-max-2026-05-20` | 默认开启思考模式，支持显式缓存 |
| 音视频翻译 | 2026-05-19 | `qwen3.5-livetranslate-flash-realtime` | 识别 60 种语言，实时翻译为 29 种语言音频 |
| 推理 | 2026-05-19 | `xiaomi/mimo-v2.5-pro` | 小米直供 MiMo-V2.5-Pro，强化通用智能体与长程任务 |
| 推理 | 2026-05-19 | `ZHIPU/GLM-5.1` / `ZHIPU/GLM-5` | 智谱直供，适配智能交互 / 企业应用 / 开发辅助 |
| 音乐生成 | 2026-05-06 | `fun-music-v1` | 百聆音乐大模型，输入创作要求或歌词生成整首中英文歌曲 |

更早期（2026-03 ~ 2026-04）上架的万相 2.7 系列（`wan2.7-t2v` / `wan2.7-i2v` / `wan2.7-r2v` / `wan2.7-videoedit` / `wan2.7-image-pro`）、Qwen3.6 系列（`qwen3.6-max-preview` / `qwen3.6-flash` / `qwen3.6-plus` / `qwen3.6-27b`）、Qwen3.5-Omni 全模态系列、爱诗 PixVerse V6 / C1、Vidu Q2 / Q3、可灵 V3、Kimi K2.6、DeepSeek-V4（`deepseek-v4-pro` / `deepseek-v4-flash`）等也已陆续上线。完整清单见[模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

> **注意**：`qwen3.7-max-preview` 与 `qwen3.7-max-2026-05-17` 仅支持纯文本输入且**仅支持思考模式**；而 2026-06-08 快照的 `qwen3.7-max-2026-06-08` 已补充视觉模态。若需多模态输入请使用后者或 `qwen3.7-plus` 系列。

## 模型调优与部署能力演进

调优侧的重点变化集中在「支持的模型范围扩大」与「训练范式拓展」两条主线。

- **2026-01-22**：qwen3 系列、qwen3-vl 系列、万相系列的更多参数量模型纳入[模型调优](https://help.aliyun.com/zh/model-studio/model-training-overview)支持范围。
- **2025-10-21**：`qwen3-vl-8b-instruct`、`qwen3-vl-8b-thinking` 支持 SFT（全参 + LoRA）调优与部署。
- **2025-09-12**：qwen3-32B/14B/8B 与 qwen2.5-72B/32B/14B/8B 新增 DPO 偏好训练，通过负反馈降低幻觉、使输出更符合人类偏好。
- **2025-08-14**：`qwen2.5-vl-72b` / `32b` / `7b` 支持调优与部署。
- **2024-12-27**：`qwen2.5-7b-instruct` 支持 SFT 全参与高效调优；同日模型部署新增按调用量计费方式，支持部署 qwen2.5-7B/14B/32B/72B 与 qwen2-7B 调优后的模型。

部署侧在 **2025-10-24** 新增「按模型单元」的部署方式（按时间计费），具备可灵活调整性能、高稳定性、可预测固定成本三项优势，详见[模型单元](https://help.aliyun.com/zh/model-studio/model-deployment-introduction)。

## 平台功能动态

按能力域归类近期控制台与 API 侧的功能演进：

**模型观测 / 监控**
- 2025-11-06 支持查看模型推理日志，用于提示词优化与故障排查。
- 2025-06-05 新增告警与通知，监控指标异常时推送给运维团队。
- 2025-04-18 新增高级监控模式：分钟级刷新、详细失败信息（4xx / 5xx 分别计数）。
- 2025-01-21 模型观测能力首次上线。

**模型评测**
- 2025-12-15 新增排行榜（多模型 × 多指标 BLEU / ROUGE 等横向对比）与多种评估器（字符串匹配、文本相似度、模型分类、模型打分、人工分类）。
- 2024-08-08 自动化评测首次上线。

**模型用量**
- 2025-12-22 新增免费额度与用量统计看板，集中展示各模型已用 / 剩余免费额度与调用量。
- 2025-07-29 新增「免费额度用完即停」功能，启用后免费额度耗尽将返回 `AllocationQuota.FreeTierOnly` 错误码，避免产生额外费用。

**OpenAI 接口兼容**
- 2024-12-20 Batch 支持任务完成通知（Callback 回调 / EventBridge 消息），新增 `qwen-vl-max` / `qwen-vl-plus` / `qwq-32b-preview`。
- 2024-08-27 新增 Vision 调用模式，可直接在原框架替换 `API-KEY` / `BASE_URL` / `model` 使用千问视觉模型。
- 2024-08-23 新增 Batch 调用模式，异步 24 小时内返回结果，费用为实时调用的一半，适合大批量离线推理、数据清洗、抽取任务。

**模型广场 / 数据处理**
- 2024-12-24 新增 Context Cache（上下文缓存），推理时减少重复计算以降低成本，初期支持 `qwen-plus`。
- 2024-12-20 新增 `search_options` 参数，可配置联网搜索来源 / 数量等，适用于 `qwen-max` / `qwen-plus` / `qwen-turbo`。
- 2024-11-07 数据处理支持画布编排，灵活组合清洗与增强节点。
- 2024-08-16 新增可信[业务空间](../concepts/workspace.md)。

## 计费调整要点

历史上几次影响面较大的价格变动，供评估成本基线时参考：

- **2025-02-07**：`qwen-max` 大幅降价 —— 实时调用输入 −88%、输出 −84%；Batch 调用输入 −88%、输出 −84%。
- **2025-01-22**：`qwen2.5-14b-instruct` / `qwen2.5-7b-instruct` 降价 50%；`qwen2.5-3b-instruct` / `qwen-vl-72b-instruct` 由免费体验转为计费。
- **2025-02-08**：部分 DeepSeek 系列模型由免费体验转为计费。
- **2024-12-31**：千问视觉理解模型降价，降幅最高 85%。
- **2024-09-19 / 2024-09-20**：部分千问免费额度由 30 天延长至 180 天；千问系列模型降价；新增节省计划（预付费）用于抵扣推理费用。
- **2024-05-21**：千问部分模型改为输入 / 输出分别计费并全线降价。

> **注意**：免费额度策略经历过多次调整（有效期 30 天 → 180 天、新人额度活动下线等），请以[模型用量](https://help.aliyun.com/zh/model-studio/model-usage-statistics)看板的实时展示为准，不要把历史公告中的额度数值作为当前预算依据。

## 已下线 / 建议替换的模型

- `qwen-max-longcontext`：2024-10-17 下线，建议改用 `qwen-max`。
- `qwen-max-1201`：2024-04-22 下线升级，建议改用 `qwen-max`。

遇到上述旧规格请在调用代码中替换为目标模型，并结合上文「最新模型上下架」选择最新快照版本。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)


