# 音频生成、语音合成与语音识别对比

本页旨在帮助开发者清晰区分百炼平台中三类核心音频AI能力：**音频生成（Audio Generation）**、**语音合成（Text-to-Speech, TTS）** 和 **语音识别（Automatic Speech Recognition, ASR）**。尽管三者均处理音频信号，但在技术目标、输入输出范式、模型架构、调用流程及业务价值上存在本质差异。本文基于百炼平台当前（2024年Q3）正式发布的非实时音频API能力进行横向对比，聚焦实际工程落地中的关键决策点，避免概念混淆，助力技术选型高效、准确。

---

## 关键维度对比表

| 维度 | 音频生成（Audio Generation） | 语音合成（TTS） | 语音识别（ASR） |
|------|------------------------------|------------------|------------------|
| **核心目标** | 从零生成具有语义/音乐/环境特征的全新音频（如配音片段、音效、背景音乐、多说话人对话） | 将结构化文本（含SSML/LaTeX）转换为自然、可懂、富有表现力的语音波形 | 将原始语音信号（单/多通道）转换为对应的文字转录结果（含标点、分段、说话人分离等） |
| **输入格式** | • 文本提示（prompt），描述内容、风格、情绪、时长等<br>• 可选参考音频（用于音色/风格对齐）<br>• 不支持纯音频输入（如“以该人声续说下一句”） | • 纯文本（UTF-8，最大长度依模型而定，通常≤5000字符）<br>• 支持SSML标签（控制停顿、语速、重音等）<br>• 支持LaTeX数学公式渲染（需`enable_ssml=true`） | • 同步模式：Base64编码音频数据或`input_audio`字段嵌入消息体<br>• 异步模式：公网可访问的音频URL数组（`input.file_urls`）<br>• 支持WAV/MP3/OPUS/FLAC等常见格式（采样率8k–48k Hz） |
| **输出格式** | • 音频文件（MP3/WAV/OPUS，由`format`参数指定）<br>• 可含元数据（如生成时长、置信度、说话人ID）<br>• *注：当前百炼平台暂未开放通用音频生成API（如音乐生成、SFX生成），此能力主要通过音色定制+TTS组合实现* | • 音频流或文件（MP3/WAV/OPUS，由`format`参数指定）<br>• 支持自定义采样率（8000–48000 Hz）和声道数<br>• 可返回SSML解析后的语音事件（如`viseme`、`word-timing`） | • JSON结构化文本：<br> - `text`: 主要转录结果<br> - `segments`: 时间戳分段（起止时间、说话人ID、置信度）<br> - `words`: 词级时间对齐（部分模型支持）<br>• 异步任务返回`task_id`，需轮询获取最终结果 |
| **平台支持模型** | • **暂无独立“音频生成”模型**；<br>• 实际能力由以下组合覆盖：<br> - `Qwen-Audio-TTS` + 定制音色 → 生成特定人声配音<br> - `CosyVoice`（v3.5）→ 高表现力拟真语音<br> - `voice-customization-sr/vd` → 克隆/设计音色后合成 → 实现“个性化音频生成” | • `Qwen-Audio-TTS`：高兼容性，支持SSML/LaTeX，系统音色丰富<br>• `CosyVoice-v2/v3/v3.5`：自然度优先，v3.5显著提升韵律与情感表达<br>• `Qwen-Audio-TTS`支持接入用户定制音色（通过`voice_id`） | • `Qwen-Audio-ASR`：通用高精度，支持上下文增强与流式返回<br>• `Qwen-Audio-ASR-Filetrans`：长音频批量异步转写（小时级）<br>• `Fun-ASR` / `Fun-ASR-Flash`：平衡速度与准确率，Flash版支持SSE流式中间结果<br>• `Qwen-ASR`：OpenAI兼容接口，便于迁移<br>• `Paraformer`：轻量低延迟，适合边缘/移动端预处理场景 |
| **API端点（HTTP）** | • 无独立`/audio/generation`端点<br>• 使用 `/v1/audio/speech`（TTS）或 `/v1/voices/create` + `/v1/audio/speech`（音色定制）实现生成目标 | • 同步：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/audio/speech`<br>• 异步（部分TTS模型支持）：需设置`X-DashScope-Async: enable` | • 同步：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/audio/asr`<br>• 异步：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/audio/asr/filetrans`<br>• 所有请求必须携带`service_mode="1"`且`device_id`必填 |
| **计费方式** | • 按**合成字符数**（TTS）或**音色创建次数+合成字符数**（音色定制）计费<br>• 音色复刻：按样本上传+合成调用分别计费<br>• 音色设计：按`voice_description`解析+合成调用计费 | • 主流计费粒度：**每千字符（CJK）或每千单词（EN）**<br>• 高保真模型（如CosyVoice v3.5）单价略高于基础TTS<br>• SSML解析、LaTeX渲染不额外计费 | • 按**音频时长（秒）** 计费（主流模型）<br>• `Qwen-Audio-ASR-Filetrans`：按提交文件总时长计费<br>• `Fun-ASR-Flash`：按实际识别耗时（秒）计费，支持流式按有效语音段结算<br>• `Paraformer`：按音频时长计费，单价最低 |
| **典型场景** | • 为短视频自动生成带情绪配音的旁白<br>• 为游戏角色/虚拟主播克隆专属音色并批量生成台词<br>• 基于文案描述快速生成多个风格备选配音（如“新闻播报风”vs“亲切客服风”） | • 有声书/电子课件自动配音<br>• 智能硬件语音反馈（如音箱播报天气）<br>• 客服IVR系统语音导航<br>• 多语言网站无障碍阅读 | • 会议录音转文字纪要<br>• 教育课堂录音自动笔记生成<br>• 客服通话质检与关键词分析<br>• 法律/医疗口述记录数字化<br>• 视频字幕自动生成 |

> ⚠️ **重要说明**：  
> - 百炼平台当前**未提供独立的“通用音频生成”服务**（如文本生成BGM、环境音、非语音音频）。所有“生成”类需求均需通过 **TTS + 音色定制** 的组合路径实现。  
> - “音频生成”在本对比中特指**面向语音内容的端到端生成能力**（即“从文本/描述到可播放语音”），而非广义的音频信号生成。  
> - 音色定制（`voice-customization`）是TTS能力的增强层，不属于独立音频生成模型，但显著扩展了TTS的生成边界。

---

## 各方案适用场景建议

| 场景需求 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| **需要将已有长录音（如2小时会议）转成带时间戳的会议纪要** | `Qwen-Audio-ASR-Filetrans`（异步） | 专为长文件优化，支持批量提交、自动分段、说话人分离，错误率低于流式模型，适合离线批处理。 |
| **开发智能音箱，需低延迟响应用户语音指令并即时播报结果** | `Qwen-Audio-ASR`（同步流式） + `Qwen-Audio-TTS`（同步） | 两者均支持流式交互，端到端延迟可控；`Qwen-Audio-ASR`上下文增强可提升唤醒后连续指令识别准确率。 |
| **为电商APP生成上千条商品卖点语音广告，要求音色统一、节奏一致、支持促销语气强调** | `CosyVoice-v3.5` + SSML `<prosody>` 标签 | CosyVoice v3.5在情感表达与节奏控制上最优；SSML可精确标注重音、停顿、语速变化，保障品牌语音一致性。 |
| **为虚拟偶像打造唯一音色，并为其剧本自动生成全季台词语音** | `voice-customization-sr`（复刻） → 获取`voice_id` → 调用`Qwen-Audio-TTS`合成 | 复刻保证音色高保真；TTS提供稳定、可扩展的批量合成能力；二者解耦设计利于音色迭代与内容生产分离。 |
| **资源受限的IoT设备（如低端录音笔），需本地化部署轻量语音识别模块** | `Paraformer`（SDK集成） | 模型体积小、推理快、内存占用低；支持离线运行；文档明确推荐用于“对时延敏感或资源受限场景”。 |
| **快速验证多种音色风格（如“知性女声”“活力男声”“童声”）哪个更匹配新App定位** | `voice-customization-vd`（音色设计） | 无需采集真人录音，仅用自然语言描述即可生成候选音色，大幅降低试错成本；适合A/B测试与创意探索阶段。 |

---

## 面向开发者的选型参考指南

### ✅ 选型第一步：明确问题本质
- 若输入是**语音**，输出是**文字** → 必选 **ASR**  
- 若输入是**文本**，输出是**语音** → 必选 **TTS**（是否需定制音色？是 → 加入音色定制流程）  
- 若需求是“**生成一段从未存在过的语音内容**”，且无法用现有音色+文本覆盖 → 当前应转向 **TTS + 音色定制组合方案**，而非寻找不存在的“音频生成API”。

### ✅ 选型第二步：关注性能与成本权衡
| 需求侧重点 | 优先模型 | 理由 |
|------------|-----------|------|
| **极致准确率（如法律文书转录）** | `Qwen-Audio-ASR` 或 `Qwen-Audio-ASR-Filetrans` | 在通用领域SOTA，上下文建模强，错误率最低 |
| **超低延迟（<500ms端到端）** | `Fun-ASR-Flash`（ASR） + `Qwen-Audio-TTS`（TTS） | Flash版支持SSE流式返回；Qwen-TTS同步响应快，SDK优化充分 |
| **大规模降本（日均百万字符合成）** | `Qwen-Audio-TTS`（基础音色） | 单价最低，稳定性高，适合标准化内容 |
| **高表现力不可妥协（如广播剧配音）** | `CosyVoice-v3.5` | 当前自然度、情感连贯性、韵律真实感最佳，但单价较高 |

### ✅ 选型第三步：规避常见陷阱
- ❌ **误用ASR模型处理TTS任务**：不要尝试用`Qwen-Audio-ASR`的`input.messages`传文本——它只接受音频输入，会报错`invalid input_audio format`。  
- ❌ **忽略音色定制有效期**：复刻/设计生成的`voice_id`默认90天过期，生产环境务必建立音色生命周期管理（自动续期或灰度切换）。  
- ❌ **在异步ASR中遗漏轮询逻辑**：`Qwen-Audio-ASR-Filetrans`返回`task_id`后，必须主动调用`GET /api/v1/tasks/{task_id}`获取结果，平台不推送回调。  
- ❌ **混用域名与鉴权方式**：所有请求必须使用`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`域名；**强烈禁用长期API Key**，务必通过STS临时凭证或百炼控制台生成60秒有效期Key。

> 💡 **开发者提示**：  
> - 所有音频API均支持Python/Java/Node.js SDK，推荐优先使用SDK（自动处理鉴权、重试、流式解析）；  
> - 调试阶段善用`X-DashScope-Logging-Enable: true`头开启详细日志，便于排查格式/权限问题；  
> - 长文本TTS或长音频ASR，务必启用`X-DashScope-Async: enable`并实现健壮的异步状态机，避免HTTP超时。

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


