# 实时API方案对比：Omni Realtime API 与 Realtime API 用户指南

本对比旨在帮助开发者清晰理解百炼平台当前两大核心实时交互API方案的技术定位、能力边界与适用约束，避免因协议误选、模型不兼容或接入路径偏差导致开发返工、延迟超标或功能缺失。随着多模态实时交互场景日益复杂（如智能座舱语音助手、跨境会议实时翻译、无障碍语音交互终端），选择匹配业务需求、终端环境与工程成熟度的API方案已成为关键技术决策点。本文基于最新文档（2024年Q3）整理，聚焦可落地的技术事实，不包含主观评价或路线图预测。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 用户指南 |
|------|-------------------|------------------------|
| **协议类型** | 仅支持 WebSocket（强制） | 支持三种协议：<br>• AOQ（推荐用于原生移动端）<br>• WebRTC（推荐用于浏览器端）<br>• WebSocket（推荐用于服务端/原型验证） |
| **输入格式** | 严格限定为原始 PCM 音频流：<br>• 16-bit, 16kHz, 单声道<br>• 不支持 MP3/WAV 封装<br>• 必须连续帧推送 | 支持 PCM 音频流（同上），且通过 SDK 可扩展支持：<br>• 自定义音频采集（外部音频源推流）<br>• 自定义视频帧（BGRA/I420/JPEG）<br>• 多模态输入（文本+音频+视频组合） |
| **输出格式** | 结构化事件流（WebSocket message）：<br>• `output.text.delta`（流式文本）<br>• `output.audio.delta`（PCM 音频 delta 帧）<br>• `response.done` 等生命周期事件 | 协议相关：<br>• AOQ/WebRTC：原生媒体流（音频/视频轨道） + 文本事件<br>• WebSocket：类 Omni 的 JSON 事件流（含 `text.delta`, `audio.delta`, `video.frame` 等） |
| **支持模型** | 仅 `qwen-omni-realtime`（v1.0+）<br>• 强制绑定 ASR+LLM+TTS+Voice Cloning 四合一能力<br>• 不兼容 `qwen-audio`、`qwen-omni` 等旧模型 | 多模型分层支持：<br>• 全模态：`qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`（三协议全支持）<br>• 专用模型：<br> ✓ ASR（仅 AOQ/WebSocket）：`Qwen-Audio-3.0-ASR-Flash-Streaming`<br> ✓ TTS（仅 AOQ/WebSocket）：`CosyVoice` 系列<br> ✓ 翻译：`qwen3.5-livetranslate-flash-realtime`<br> ✓ 对话：`qwen-audio-3.0-realtime-plus`（三协议） |
| **API 端点** | 固定 WebSocket 地址：<br>`wss://dashscope.aliyuncs.com/realtime/v1/omni` | 协议差异化：<br>• AOQ：需先调用 `/api/v1/allocate` 获取动态凭证（`token`, `sid`, `relayEndpoints`）<br>• WebRTC：通过信令服务交换 SDP/ICE，无固定 URL<br>• WebSocket：`wss://dashscope.aliyuncs.com/realtime/v1/chat`（通用入口，模型由 `session.update` 指定） |
| **计费方式** | 按会话时长（秒）计费：<br>• 超过 120 秒自动断连，按实际使用秒数计费<br>• 语音克隆（voice_id）生成单独计费，不计入会话时长 | 按模型能力维度计费：<br>• ASR/TTS/LLM/Translation 分项计费<br>• 同一会话中混合调用多能力（如 ASR+TTS+LLM）将叠加计费<br>• AOQ/WebRTC 连接建立本身不额外计费，仅按模型调用消耗计量 |
| **典型场景** | • 端到端低延迟语音交互终端（如硬件音箱、车载语音）<br>• 需要实时音色克隆的个性化客服机器人<br>• 对连接轻量性要求高、无需视频/复杂状态管理的嵌入式场景 | • 跨平台智能应用（iOS/Android/Web 多端统一架构）<br>• 实时会议系统（需音视频同步、翻译、字幕）<br>• 无障碍辅助工具（需自定义音频采集/播放链路）<br>• 多模态对话平台（文本+语音+视频联合理解与生成） |
| **客户端复杂度** | 中等：<br>• 需手动处理 PCM 帧分片、心跳保活、事件解析<br>• SDK 提供 Python/Java 封装，但无跨平台统一 SDK | 分层设计：<br>• AOQ：高封装度原生 SDK（各平台 API 一致），隐藏信令/Relay 细节<br>• WebRTC：需开发者实现 SDP 协商、ICE 管理、媒体轨道控制<br>• WebSocket：最低门槛，接近 Omni，但需适配多模型参数 |

## 各方案的适用场景建议

### ✅ 推荐选用 **Omni Realtime API** 当：
- 业务聚焦于**纯语音端到端闭环交互**（说→听→响应→合成），且对端到端延迟敏感（目标 <800ms）；
- 终端为资源受限设备（如 MCU 嵌入式模块、IoT 语音硬件），无法集成大型 SDK 或处理 WebRTC 信令；
- 明确需要**实时声音复刻**（Voice Cloning）能力，并接受其需预上传参考音频、单 `voice_id` 绑定 `app_key` 的限制；
- 团队具备 WebSocket 底层开发经验，或已采用 Python/Java 技术栈并可直接复用官方 SDK；
- 无需视频输入、无需多协议兼容、无需 ASR/TTS 独立调用。

### ✅ 推荐选用 **Realtime API（用户指南）** 当：
- 需要**跨平台一致性体验**（同一套逻辑覆盖 App、小程序、Web 页面）；
- 场景涉及**多模态协同**（如会议中语音转文字+实时翻译+发言人头像视频流）；
- 要求**灵活的音频管线控制**（例如：从蓝牙耳机直采、混音后推流、自定义降噪模块介入）；
- 需要**独立调用 ASR 或 TTS**（如仅做语音转写存档，或仅用 TTS 播报通知），而非强制捆绑 LLM；
- 已有 WebRTC 基础设施或团队熟悉浏览器实时通信开发；
- 项目处于快速验证阶段，需通过 WebSocket 快速对接，同时保留未来升级至 AOQ/WebRTC 的平滑路径。

## 面向开发者的技术选型参考

请按以下顺序进行决策：

1. **确认核心能力需求**  
   → 若必须使用 **实时音色克隆** → 唯一可选：**Omni Realtime API**  
   → 若需 **独立 ASR/TTS 调用** 或 **视频输入支持** → 唯一可选：**Realtime API**  

2. **评估终端环境与协议约束**  
   → 目标平台仅为 **Web 浏览器**，且需原生媒体流 → 选 **Realtime API + WebRTC**  
   → 目标平台为 **iOS/Android 原生 App**，追求低延迟与稳定性 → 选 **Realtime API + AOQ**  
   → 目标为 **服务端代理、边缘网关或嵌入式设备**，无 GUI/无 WebRTC 栈 → 对比 Omni 与 Realtime WebSocket：  
   &nbsp;&nbsp;✓ 仅需语音闭环 + 极致轻量 → **Omni Realtime API**  
   &nbsp;&nbsp;✓ 需未来扩展视频/多模型切换 → **Realtime API + WebSocket**  

3. **检查工程成熟度与维护成本**  
   → 团队无 WebSocket 心跳/重连/事件解析经验 → 优先 Realtime API 的 AOQ SDK（开箱即用）  
   → 已有成熟 WebSocket 基础设施（如自有信令网关）→ Omni Realtime API 更易集成  
   → 需长期演进（如后续加入虚拟人视频）→ Realtime API 提供明确的多模态扩展路径  

4. **验证计费模型匹配度**  
   → 高频短会话（平均 <30 秒）、强依赖音色克隆 → Omni 的“按秒计费”更透明  
   → 混合调用（例：ASR 10s + LLM 5s + TTS 8s）→ Realtime API 的分项计费更精细可控  

> ⚠️ 重要提醒：两个方案**不互通、不兼容**。`qwen-omni-realtime` 模型无法在 Realtime API 中调用；反之，`qwen3.5-omni-plus-realtime` 也无法接入 Omni Realtime API 的 WebSocket 端点。请勿尝试跨方案复用配置、SDK 或 voice_id。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


