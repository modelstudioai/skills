# release notes

百炼平台持续迭代模型能力与平台功能，发布节奏覆盖模型上新、功能模块升级、计费调整及模型下线等方面。开发者可通过 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md) 跟踪平台级变更，通过 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md) 查看具体模型的上架时间与规格信息。

## 平台公告与计费变更

百炼平台定期发布计费调整与政策公告，开发者在接入前应关注以下要点：

- **模型降价**：千问系列、通义千问VL系列多次降价；qwen-max 输入价格降低 88%、输出降低 84%。
- **上下文缓存降价**：部分模型上下文缓存 `cached_token` 单价已调整（如 deepseek-v4-pro 调至 1 元/百万 token）。
- **资源包变更**：qwen-turbo 资源包已启动退市流程；团队版新增跨坐席共享 Credits 弹性用量包。
- **免费额度**：新人免费额度有效期调整；支持"用完即停"功能，避免超额产生费用。
- **模型下线机制**：老旧模型按既定规则下线，部分已延期，详见模型下线机制说明。

## 模型上新动态

平台持续引入多类型模型，按模型类型分类如下：

### 推理与文生文模型

| 模型 | 上架时间 | 说明 |
|------|----------|------|
| qwen3.7-max | 2026-05 | Qwen Max 新一代旗舰，默认思考模式，擅长编程与办公 |
| qwen3.7-plus | 2026-06 | 视觉-语言全面升级，[多模态](../concepts/multimodal.md)交互混合智能体 |
| qwen3.6-flash | 2026-04 | 视觉语言 Flash 系列，智能体编程能力显著提升 |
| qwen3.6-plus | 2026-04 | 代码开发能力重点升级，[多模态](../concepts/multimodal.md)识别增强 |
| qwen3.5-plus | 2026-04 | Agentic coding 大幅提升，推理速度显著提升 |
| deepseek-v4-pro / flash | 2026-04 | DeepSeek-V4 系列，阿里直供 |
| kimi/kimi-k2.7-code | 2026-06 | 月之暗面直供，编码为中心的智能体模型 |
| glm-5.1 | 2026-04 | 智谱 200K 上下文，最大输出 128K [Token](../concepts/token.md) |
| xiaomi/mimo-v2.5-pro | 2026-05 | 小米直供，通用智能体与复杂工程增强 |

### 视觉与[多模态](../concepts/multimodal.md)模型

| 模型 | 上架时间 | 说明 |
|------|----------|------|
| qwen3.5-omni-plus/flash | 2026-03 | 全模态，支持长视频分析、113 语种识别 |
| qwen3.5-omni-*-realtime | 2026-03 | 实时[多模态](../concepts/multimodal.md)，原生联网搜索与语音打断 |
| qwen3.5-ocr | 2026-06 | 128K 上下文，多轮对话，多卡证信息抽取 |
| qwen-image-2.0-pro | 多快照 | 图片生成与编辑融合，支持多语言图内文字 |

### 视频生成模型

| 模型系列 | 上架时间 | 能力 |
|----------|----------|------|
| 万相 2.7 (wan2.7-*) | 2026-04 起 | 文生视频、图生视频、参考生视频、视频编辑 |
| HappyHorse 1.0/1.1 | 2026-04/06 | 有声视频生成，3-15 秒，720P/1080P |
| 爱诗 PixVerse v6/C1 | 2026-03/04 | 文/图/首尾帧/参考生视频，支持智能分镜 |
| Vidu Q3 系列 | 2026-03/04 | 文/图/参考生视频 |

### 其他模型

- **3D 生成**：Tripo H3.1（最高 200 万面）、Tripo P1.0（2 万面，快速生成）
- **音乐生成**：fun-music-v1，支持输入创作要求或歌词生成演唱歌曲
- **音视频翻译**：qwen3.5-livetranslate-flash-realtime，60 语种识别、29 语种实时翻译
- **语音识别**：fun-asr，覆盖汉语七大方言与 30 个语种
- **图像生成与编辑**：wan2.7-image-pro/image，支持 4K 输出、文生图/组图/交互式编辑

详细模型规格与服务部署范围参见 [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)。

## 平台功能更新

### 模型调优与部署

- **模型调优**：已支持文本生成、视觉理解 (VL)、视频生成、图像生成模型的 SFT 微调；新增 DPO 偏好训练和强化学习训练（邀约制）；新增 0 代码安全合规强化流程。
- **模型部署**：新增按模型单元 (MU) 时长计费的 PTU 部署方式，支持灵活调整性能与固定成本；预置吞吐部署新增长输入与前缀缓存能力。
- **模型压缩**：使用量化算法将全精度微调模型转为低精度版本以降低部署成本。
- **模型导入**：支持从 OSS 导入 LoRA 微调模型，并提供完整的 API 接口。

### 知识库与 RAG

- **知识检索服务**：支持多知识库联合检索与混合排序。
- **知识问答服务**：基于大模型结合检索生成回答。
- **检索增强**：Retrieve 接口新增排序模型选项与指令干预模式。
- **日志与监控**：知识库检索调用全量投递至 SLS 日志服务，支持审计与告警。

### 智能体与应用

- **智能体托管运行时**：平台托管会话与工具执行，通过 API 管理。
- **Skill 能力包**：智能体可添加官方或自定义技能。
- **MCP 服务**：上线官方 MCP 服务，支持平台内集成与第三方接入。
- **记忆库 Memory 2.0**：自动从对话提取记忆片段与用户画像，支持多应用共享。
- **UI 设计器**：集成魔笔低代码能力，可视化拖放构建网页 UI 应用。

### API 与接入工具

- **Responses API**：新增[异步调用](../concepts/async-invocation.md)模式（`background=true`）。
- **Anthropic Messages 接口**：文本生成 API 入口新增 OpenAI Responses 与 Anthropic Messages 分类。
- **异步任务回调**：支持通过 EventBridge 推送完成事件，无需轮询。
- **临时 [API Key](../concepts/api-key.md)**：在不可信环境下避免永久 [API Key](../concepts/api-key.md) 泄露。
- **接入工具**：新增 Codex 终端编程助手接入、Kilo CLI、Spring AI Alibaba 框架等。

### 其他功能

- **Coding Plan**：Pro 套餐首月特惠 ¥39.90；联网搜索 MCP 升级 Streamable HTTP 协议。
- **数据连接**：支持 MySQL / 语雀 / OSS 等数据源接入。
- **模型评测**：新增排行榜、综合评测与多种评估器（BLEU、ROUGE 等）。
- **模型观测**：支持推理日志查看、告警通知、高级监控模式（分钟级刷新）。
- **地域扩展**：新增美国、德国、日本地域与服务部署范围。

## 注意事项

- 模型版本快照（如 `qwen3.7-max-2026-05-20`）与别名（如 `qwen3.7-max`）的能力一致，但别名会自动指向最新快照。
- 部分模型存在阿里直供与第三方直供（月之暗面、快手万擎、智谱、小米等）两种接入方式，计费与 SLA 可能不同。
- 功能更新的完整时间线与详细说明请参考 [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)。

## 来源文档

- [模型平台功能更新](../../raw/model-user-guide/release-notes/model-release-notes.md)
- [模型上下架与更新](../../raw/model-user-guide/release-notes/newly-released-models.md)





