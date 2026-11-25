# 音频生成与语音定制化能力对比

本文档旨在帮助开发者清晰区分百炼平台中两类常被混淆的音频能力：**音频生成（Audio Generation）** 与 **语音定制化（Voice Customization）**。二者虽均产出音频，但技术目标、输入范式、模型架构及适用场景存在本质差异。音频生成聚焦于“从文本创造声音内容”（如配乐、音效），强调语义驱动的音频创作；语音定制化则聚焦于“复刻或设计人声音色”，服务于个性化语音合成（TTS）的前端音色准备环节，是高质量语音合成的前置能力。正确理解二者边界，可避免选型错误、资源浪费及集成失败。

以下从关键维度进行结构化对比，并提供面向开发者的选型建议。

## 关键维度对比

| 维度 | 音频生成（Audio Generation） | 语音定制化（Voice Customization） |
|------|------------------------------|-----------------------------------|
| **核心目标** | 根据文本提示（Prompt）生成非语音类音频内容，如背景音乐、环境音效、氛围音等 | 创建专属人声音色（Voice ID），用于后续 TTS 合成，支持音色复刻（Cloning）与音色设计（Design）两种模式 |
| **输入格式** | `text` 字符串（必需），描述所需音频风格/情绪/乐器/场景（如 `"80s synthwave track with driving bassline and nostalgic pads"`）；可选 `duration`（秒，1–60）、`seed` 等控制参数 | • **音色复刻**：参考音频（WAV/MP3/M4A/FLAC，≤30 秒，单声道，16kHz+ 采样率）或其公网 URL / Base64 Data URI<br>• **音色设计**：`voice_prompt`（文本描述，如 `"温和的年轻女性，略带笑意，语速适中"`） + `preview_text`（15–200 字合成预览文本） |
| **输出格式** | JSON 响应体含 `output.audio_url`（直链可下载的 MP3 文件，有效期 24 小时）；无流式响应；不返回原始波形数据 | JSON 响应体含 `output.voice_id`（唯一音色标识符，如 `cosyvoice-v3.5-plus-myvoice-abc123`）；创建成功后需**另行调用标准 TTS API**（如 `/api/v1/services/aigc/audio/tts`）并指定该 `voice_id` 才能生成语音音频 |
| **支持模型** | `qwen-audio-generation`（当前唯一官方支持模型） | • 音色复刻：`qwen-audio-3.x-tts-plus/flash`、`qwen-audio-3.x-realtime-plus/flash`、`cosyvoice-v3/v3.5-plus/flash`<br>• 音色设计：仅 `cosyvoice-v3.5-plus` 及以上版本 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/audio/generation` | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/audio/tts/customization`（地域强绑定，需匹配 Workspace） |
| **计费方式** | 按**每次请求**计费（无论生成时长），单位：千次调用（1K Call） | 按**音色实例生命周期**计费：<br>• 创建/更新/删除操作免费<br>• 每个激活态 `voice_id` 按小时计费（按实际占用时长，最小计费粒度 1 小时）<br>• 静态存储不额外收费，但超期未调用将自动释放 |
| **典型场景** | • 游戏/APP 动态生成 BGM 或交互音效<br>• 视频剪辑工具自动匹配场景音乐<br>• 教育课件生成情境化环境音（如雨声、教室嘈杂声） | • 客服系统使用企业代言人音色播报<br>• 有声书平台为签约主播快速构建数字分身<br>• 内部培训系统采用高管音色讲解政策<br>• 无障碍应用为视障用户定制亲人语音导航 |
| **是否依赖 TTS 流程** | 否。独立完成“文本→音频”全流程，输出即最终可用音频文件 | 是。仅为 TTS 提供音色底座；**必须配合标准 TTS API 使用**才能产出语音，二者为“配置+执行”关系 |
| **实时性支持** | 不支持[流式输出](../concepts/streaming-output.md)；单次请求返回完整音频文件（延迟取决于生成耗时，通常 3–10 秒） | 不涉及实时音频流；音色创建为异步任务（通常 <30 秒完成），后续 TTS 调用可支持流式响应（取决于所选 TTS 模型，如 `qwen-audio-3.x-realtime-plus`） |

## 各方案的适用场景建议

### ✅ 选择 **音频生成（Audio Generation）** 当：
- 你需要的是**非人声的创意音频内容**（音乐、音效、氛围声），而非说话声；
- 输入是纯文本描述，**没有且不需要参考人声样本**；
- 场景对音色一致性无要求（例如每次生成不同风格的咖啡馆背景音乐）；
- 你希望“开箱即用”，无需管理音色生命周期或与 TTS 系统耦合；
- 典型用例：短视频自动配乐、AI 游戏动态音效引擎、智能硬件环境音模拟。

### ✅ 选择 **语音定制化（Voice Customization）** 当：
- 你的核心需求是让合成语音**听起来像某个特定真人或符合某种人格化特征**；
- 你已拥有目标人声的干净录音（≥10 秒），或能精准用文字定义期望音色；
- 你已在使用或计划接入百炼 TTS 服务（如 `qwen2-tts-zh` 或 `cosyvoice-v3.5-plus`），需要为其注入定制音色；
- 你需要长期、稳定、可复用的音色资产（如企业品牌音色），并接受按小时付费的资源管理模式；
- 典型用例：品牌语音助手、个性化新闻播报、数字人语音驱动、多语言客服音色本地化。

### ⚠️ 注意：二者不可互换替代
- ❌ 不要用音频生成 API 去“克隆人声”——它不建模声纹，无法保证说话人身份一致性；
- ❌ 不要用语音定制化 API 去“生成背景音乐”——它不理解音乐语义，无 Prompt 生成功能；
- ✅ 正确组合：先用语音定制化创建 `voice_id` → 再用标准 TTS API（指定该 `voice_id`）合成语音 → 如需配乐，**额外调用音频生成 API** 生成 BGM，再由客户端混音。

## 面向开发者的技术选型参考

| 选型考量点 | 推荐动作 |
|------------|----------|
| **首次集成，验证可行性** | • 音频生成：直接调用 `/audio/generation`，传入简单 Prompt（如 `"calm piano melody"`），5 分钟内可获 MP3 链接<br>• 语音定制化：优先使用 **Python SDK**（`dashscope.Client(audio.voices).create(...)`），自动处理地域路由、参数序列化与错误重试，降低 HTTP 构造门槛 |
| **生产环境稳定性要求高** | • 音频生成：关注 `audio_url` 有效期（24 小时），务必在业务侧实现下载缓存或 CDN 回源；监控 `400 Bad Request`（常见于 Prompt 过长或 duration 超限）<br>• 语音定制化：**必须实现 voice_id 生命周期管理**——创建后记录 `voice_id` 与 `target_model`，TTS 调用时严格匹配；定期调用 `list_voice` 清理闲置音色以控成本 |
| **多语言/多地域部署** | • 音频生成：端点全球统一（`dashscope.aliyuncs.com`），无地域约束<br>• 语音定制化：**端点强绑定 Workspace 地域**（北京/新加坡），Key 与地域不互通；跨地域项目需分别申请 Key 并维护两套 endpoint 配置 |
| **调试与排障重点** | • 音频生成：检查 `input.text` 是否含敏感词（可能触发拦截）、`duration` 是否在 1–60 范围内、响应 `output.status` 是否为 `"success"`<br>• 语音定制化：复刻失败时优先验证参考音频——是否单声道？采样率 ≥16kHz？静音段是否过长？设计失败时检查 `voice_prompt` 长度（≤500 字符）与 `preview_text` 长度（15–200 字符） |
| **成本优化建议** | • 音频生成：批量生成时避免高频小请求（如 1 秒音乐生成 60 次），改用单次长时生成（60 秒）再裁剪<br>• 语音定制化：启用 `auto_delete_after_hours` 参数（若 SDK/HTTP 支持），设置闲置 24 小时自动释放；TTS 调用方应复用 `voice_id`，禁止重复创建相同音色 |

> **最后提醒**：语音定制化能力是百炼平台**语音合成（TTS）生态的关键增强项**，而非独立音频生成服务。请始终将其定位为“TTS 的音色插件”，并在架构设计中预留 TTS 调用环节。详细参数规范、错误码说明及 SDK 示例，请查阅对应子文档的最新版本。

## 被对比主题页

- [audio api directory](../api/audio-api-directory.md)
- [voice customization api directory](../api/voice-customization-api-directory.md)


