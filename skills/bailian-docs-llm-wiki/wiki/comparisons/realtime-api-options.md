# 实时 API 方案对比：Omni Realtime 与 Realtime 用户指南

本文旨在帮助开发者清晰理解百炼平台两类核心实时 API 方案的定位差异、能力边界与技术约束，从而在智能语音助手、会议辅助、客服机器人等低延迟交互场景中做出合理选型。Omni Realtime 是面向**端到端多模态流式协同**的专用协议；Realtime API 则是覆盖更广、协议更灵活的**统一实时能力接入层**。二者并非替代关系，而是分层协作：Omni Realtime 可视为 Realtime API 生态中针对“全链路语音-文本-语音闭环”高度优化的子集，而 Realtime API 提供了模型、协议、部署形态的全局可扩展性。

---

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API 用户指南 |
|------|-------------------|------------------------|
| **核心定位** | 专为**语音优先、端到端流式多模态协同**设计的轻量级 WebSocket 接口（ASR → LLM → TTS 全链路流式串联） | 百炼平台统一的**实时 AI 能力接入层**，支持 AOQ / WebRTC / WebSocket 三协议，覆盖 ASR、TTS、多模态对话、实时翻译等全栈能力 |
| **输入格式** | 仅支持连续 PCM 音频流（16kHz, 16-bit, mono），通过 `input.audio` 帧逐帧推送；不支持文本/图像等其他模态直接输入 | 支持多模态混合输入：<br>• 音频：PCM / Opus（AOQ/WebSocket）、WebRTC 原生音频轨道<br>• 文本：`input.text` 帧（WebSocket/AOQ）<br>• 图像/视频：需配合 `multimodal-dialog` 等模型启用（AOQ/WebSocket） |
| **输出格式** | 流式事件驱动：<br>• `output.text.delta`（LLM 增量文本）<br>• `output.audio.delta`（TTS 音频片段）<br>• `output.text.final` / `output.audio.done` 等状态事件 | 协议相关：<br>• AOQ/WebSocket：结构化 JSON 事件（如 `text.delta`, `audio.chunk`, `session.updated`）<br>• WebRTC：原生 MediaStream 轨道输出（音频/视频）+ 可选文本信令通道 |
| **支持模型** | 仅 `qwen-omni-realtime-v1`（v2 尚未 GA）；强制绑定 ASR+LLM+TTS 三阶段协同 | 多模型矩阵：<br>• 全模态：`qwen3.8-omni-flash-realtime`, `multimodal-dialog`（三协议均支持）<br>• ASR 专用：`Qwen-Audio-3.0-ASR-Flash-Streaming`（AOQ/WebSocket，**不支持 WebRTC**）<br>• TTS 专用：`CosyVoice`, `qwen-audio-3.0-tts-flash`（AOQ/WebSocket，**不支持 WebRTC**）<br>• 对话增强：`qwen-audio-3.1-realtime-plus`（三协议均支持） |
| **API 端点与协议** | 固定 WebSocket 端点：<br>`wss://dashscope.aliyuncs.com/realtime/v1/omni`<br>（需 `Authorization` + `X-DashScope-Date`） | 协议可选：<br>• AOQ：`wss://dashscope.aliyuncs.com/realtime/v1/aoq`（需服务端签发 `aoqTokenForClient`）<br>• WebRTC：通过 `/api/v1/webrtc/realtime` 获取信令配置后建立 P2P 连接<br>• WebSocket：`wss://dashscope.aliyuncs.com/realtime/v1/ws`（通用接入） |
| **计费方式** | 按**连接时长 + 音频处理时长**计费（单位：秒），区分 ASR/TTS/LLM 各阶段用量；支持按量付费与资源包 | 按**调用模型的实际资源消耗**计费：<br>• ASR/TTS：按音频时长（秒）<br>• LLM：按 token 数量（输入+输出）<br>• 多模态：按综合计算单元（CU）<br>• *所有协议共享同一计费体系，无协议溢价* |
| **典型场景** | • 语音唤醒即响应的智能硬件（如带屏音箱）<br>• 需严格控制端到端延迟（<800ms）的实时会议字幕+摘要<br>• 语音助手类 App 中“说-听-说”无缝闭环体验 | • 跨端统一 SDK 的企业级音视频应用（App/Web/桌面端）<br>• 已有 WebRTC 基建的在线教育/远程医疗平台<br>• 需要灵活组合 ASR+LLM+TTS 或叠加图像理解的复杂工作流<br>• 对客户端安全性要求高（如禁止 API Key 暴露）的金融/政务场景 |
| **客户端安全要求** | `API Key` 需直接嵌入客户端（因 WebSocket 直连鉴权），**存在密钥泄露风险**；适用于可信环境（如预装固件设备） | `API Key` **严格保留在服务端**；客户端仅持有短期、作用域受限的 `aoqTokenForClient` 或信令凭证；符合最小权限原则，推荐用于公网暴露场景 |

---

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 你的产品形态是**纯语音交互终端**（如车载系统、IoT 设备），且对端到端延迟极度敏感（目标 < 500ms）；
- 业务逻辑高度聚焦于“语音输入 → 实时思考 → 语音反馈”这一单一流程，无需额外文本输入、图像理解或协议切换；
- 开发团队希望快速集成，接受单一 WebSocket 协议和固定模型，避免多协议适配成本；
- 客户端运行环境可控（如自有硬件固件），能保障 `API Key` 安全存储。

### ✅ 选择 Realtime API 当：
- 你需要**跨平台一致性体验**（iOS/Android/Web/Windows/macOS），并希望复用同一套业务逻辑；
- 场景涉及**混合模态**（例如：会议中同时处理语音、共享屏幕、PPT 图片）或需要**动态切换模型**（如先 ASR 再调用多模态模型分析图表）；
- 项目对**安全合规有强要求**（如金融 APP），必须杜绝客户端持有长期有效 API Key；
- 你已有 WebRTC 基础设施，或希望利用浏览器原生能力降低 SDK 包体积；
- 需要细粒度控制媒体流（如自定义音频采集/播放、注入 TTS 输出到外部混音器、截获 ASR 结果做 NLU 增强）。

> ⚠️ 注意：若需声音复刻（Voice Cloning），当前仅 Omni Realtime 支持；Realtime API 尚未开放该能力。

---

## 技术选型参考（面向开发者）

| 评估项 | 推荐方案 | 理由 |
|---------|-----------|------|
| **首次原型验证（MVP）** | Omni Realtime | WebSocket 接口简洁，Python/Java SDK 封装完善，5 分钟可跑通语音闭环；适合快速验证核心交互逻辑。 |
| **生产级跨端 App（含 iOS/Android/Web）** | Realtime API（AOQ + WebSocket 回退） | AOQ SDK 提供全平台原生支持，服务端鉴权保障安全；WebSocket 可作为 Web 端兜底方案，统一事件模型降低维护成本。 |
| **浏览器内嵌语音助手** | Realtime API（WebRTC） | 充分利用浏览器原生能力，零 SDK 依赖，自动适配麦克风/扬声器策略，隐私提示友好；但不可用于纯 ASR/TTS 场景。 |
| **低功耗边缘设备（如 ARM SoC）** | Omni Realtime | 轻量级 WebSocket 连接 + PCM 直传，无 WebRTC 协议栈开销，内存/CPU 占用更低。 |
| **需对接企业 SSO 或自定义鉴权流程** | Realtime API | 服务端 allocate 接口完全可控，可将 `aoqTokenForClient` 与内部用户会话绑定，实现精细化权限管控。 |
| **未来需扩展图像/文档理解能力** | Realtime API | `multimodal-dialog` 等模型已支持多模态输入，协议层兼容，无需重构通信架构。 |

> 💡 **最佳实践提示**：  
> - 不要将 Omni Realtime 视为 Realtime API 的“简化版”——它是深度垂直优化的专用通道；  
> - Realtime API 的 AOQ 协议在移动端性能与稳定性上显著优于 WebSocket，**生产环境首选 AOQ**；  
> - 所有方案均需严格遵循 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md) 和 [Realtime API 状态机规范](../../raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)，错误重连与会话恢复逻辑不可省略。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


