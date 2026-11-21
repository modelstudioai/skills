# 语音合成、语音识别与声音定制对比

本对比旨在帮助开发者清晰区分百炼平台中三类核心语音能力的技术定位、能力边界与集成路径，避免因功能混淆导致选型偏差。随着AIGC音频应用向精细化、个性化演进，语音识别（ASR）、语音合成（TTS）与声音定制（Voice Customization）虽同属音频处理范畴，但在输入输出范式、模型架构、调用流程及业务价值上存在本质差异。本文基于当前（v2024.10）非实时音频API体系，聚焦**离线/长时文件处理场景**，为技术方案设计与API集成提供客观、可落地的决策依据。

## 核心能力对比表

| 维度 | 语音识别（ASR） | 语音合成（TTS） | 声音定制（Voice Customization） |
|------|----------------|----------------|------------------------------|
| **核心目标** | 将语音信号转换为结构化文本 | 将文本（或SSML/LaTeX）转换为自然语音波形 | 创建可复用的专属音色资产（ID），供TTS调用 |
| **输入格式** | 音频文件（WAV/MP3/OPUS等，≤100MB；推荐OPUS提升Paraformer效率）<br>• 同步：短音频（≤60s）<br>• 异步：长音频（支持视频抽音后文件） | 文本内容（纯文本 / SSML / LaTeX）<br>• 必填 `text` 字段<br>• 必填 `voice`（系统音色ID 或 定制音色ID） | • **音色复刻**：30–60秒单人语音URL（WAV/MP3，单声道/16kHz，≤10MB）<br>• **音色设计**：20–200字自然语言描述（中文优先） |
| **输出格式** | JSON结构化结果：<br>• 同步：直接返回 `text`、`segments`、`words` 等字段<br>• 异步：返回 `task_id`，轮询获取含 `result_url`（有效期24h）的JSON | 音频二进制流（默认MP3）或直传OSS的 `result_url`（异步模式）<br>• 支持 `format`（mp3/wav/flac）、`sample_rate`（8k–48k）配置 | JSON响应，含唯一 `voice_id`（如 `vc_abc123xyz`）及 `status`；无音频输出 |
| **支持模型** | • Qwen-Audio-ASR（短音频流式）<br>• Qwen-Audio-ASR-Filetrans / Fun-ASR / Paraformer（长音频异步）<br>• Fun-ASR-Flash / Qwen-ASR（支持上下文增强 & OpenAI兼容） | • Qwen-Audio-TTS<br>• CosyVoice（v3.5+）<br>• *均支持三类音色源：系统音色、复刻音色、设计音色* | • `sound-reengraving-v1`（音色复刻）<br>• `voice-design-v1`（音色设计）<br>• *不独立生成语音，仅为TTS提供音色ID* |
| **API端点（HTTP）** | • 同步：`POST /api/v1/audio/asr`（Qwen-Audio-ASR）<br>• 异步：`POST /api/v1/audio/asr/jobs`（需 `X-DashScope-Async: enable` 头） | • 同步：`POST /api/v1/audio/tts`（Qwen-Audio-TTS/CosyVoice）<br>• 异步：`POST /api/v1/audio/tts/jobs`（同ASR异步头） | `POST /api/v1/services/aigc/voice-customization`<br>• **独立域名**：`https://dashscope.aliyuncs.com`（不走Workspace专属域名） |
| **计费方式** | 按**音频时长（秒）** 计费<br>• 同步/异步统一计价<br>• Paraformer等模型无额外热词费用（热词需单独开通且北京地域专用） | 按**合成字符数（UTF-8编码）** 计费<br>• SSML标签内文本计入，标签本身不计费<br>• 音频时长不影响费用 | 按**音色创建次数**计费<br>• 复刻与设计均为单次调用计费<br>• 成功生成即扣费，无论后续是否用于TTS |
| **典型场景** | • 会议录音转文字纪要<br>• 教育视频字幕自动生成<br>• 客服通话质检分析<br>• 法律文书语音归档 | • 有声书/播客自动配音<br>• 智能硬件TTS播报（导航、IoT）<br>• 多语言网站无障碍朗读<br>• 游戏NPC语音生成 | • 企业品牌语音形象统一（CEO语音播报）<br>• 影视IP角色音色复刻（动画配音）<br>• 无障碍服务个性化音色（视障用户专属）<br>• 虚拟主播音色资产库建设 |

## 各方案适用场景建议

- **选择语音识别（ASR）当且仅当**：  
  你的输入是**已有音频/视频文件**，目标是提取其中的**语义文本信息**。若需高精度长音频转写（如2小时讲座），优先选用 `Qwen-Audio-ASR-Filetrans` 或 `Paraformer`（注意强制异步头）；若需低延迟短句识别（如语音指令），选用 `Qwen-Audio-ASR` 同步接口。

- **选择语音合成（TTS）当且仅当**：  
  你的输入是**结构化文本内容**，目标是生成**可播放的语音音频**。若追求高表现力与情感控制，选用 `CosyVoice`；若需强稳定性与多语言兼容，选用 `Qwen-Audio-TTS`。**关键前提**：必须已拥有合法音色ID——可直接使用系统音色，或通过声音定制API预先生成。

- **选择声音定制（Voice Customization）当且仅当**：  
  你需要**构建专属音色资产**，且该音色将被**多次、跨项目复用于TTS合成**。若你有高质量真人语音样本（30s+），选 `sound-reengraving-v1`；若仅有角色设定描述（无样本），选 `voice-design-v1`。**重要提醒**：声音定制本身不产生音频，它只是TTS的“前置生产环节”，不可替代TTS调用。

## 技术选型参考（面向开发者）

| 决策问题 | 推荐动作 | 注意事项 |
|----------|----------|----------|
| **我的需求是“把一段客服录音变成文字报告”** | ✅ 直接调用 ASR 异步接口（如 `Fun-ASR`）<br>• 提交音频 → 轮询 `task_id` → 下载 `result_url` 解析JSON | • 务必添加 `X-DashScope-Async: enable` 头<br>• 音频预处理为 OPUS 可显著提升 Paraformer 效率与准确率 |
| **我的需求是“给网页文章生成朗读音频”** | ✅ 调用 TTS 同步接口（如 `Qwen-Audio-TTS`）<br>• 构造含 `text` + `voice`（系统音色ID）的请求 | • `voice` 参数必须是有效ID（系统音色列表见文档）<br>• 如需定制音色，**必须先完成声音定制API调用**获取 `voice_id` |
| **我的需求是“让APP用CEO的声音播报通知”** | ✅ 分两步：<br>1️⃣ 调用 `sound-reengraving-v1` 上传CEO语音 → 获取 `voice_id`<br>2️⃣ 在TTS请求中将 `voice` 设为该 `voice_id` | • CEO语音需严格满足：30–60s、单人、无背景音、16kHz单声道<br>• 复刻音色生成后，即可像系统音色一样在任意TTS请求中复用 |
| **我需要“生成一个温柔知性的女性AI助手音色”但没有真人样本** | ✅ 调用 `voice-design-v1`，提交描述如 `"30岁女性，声音温柔清晰，语速适中，略带知性书卷气，适合教育类APP"` → 获取 `voice_id` → 在TTS中使用 | • 描述需20–200字，中文效果最优<br>• `style` 等历史参数已废弃，勿传入 |
| **我同时需要ASR转写 + TTS配音（如视频自动配音）** | ✅ 组合调用：<br>ASR异步 → 解析文本 → 清洗/编辑文本 → TTS同步/异步合成<br>• 全流程需自行编排任务状态（如ASR完成才触发TTS） | • ASR输出的 `segments` 可用于分段TTS，实现精准时间对齐<br>• 两个API使用**不同域名**：ASR/TTS走 Workspace 域名，声音定制走 `dashscope.aliyuncs.com` |

> **最后提示**：所有能力均需 API Key 认证，高安全场景请务必使用临时API Key（有效期60秒）；Java/Python SDK 的 CosyVoice/Qwen-Audio-TTS 当前仅支持华北2（北京）地域；新加坡地域不支持热词定制与部分SDK音色能力——跨地域部署前请严格核验地域限制。

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


