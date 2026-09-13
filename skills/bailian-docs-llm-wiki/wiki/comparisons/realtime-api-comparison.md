# 实时 API 方案对比：Omni Realtime API vs Realtime API User Guide

本文旨在帮助开发者清晰区分百炼平台提供的两类核心实时接口——**Omni Realtime API** 与 **Realtime API User Guide（标准 Realtime API）**，明确其定位差异、能力边界与集成成本。随着[多模态](../concepts/multi-modal.md)交互和低延迟场景需求激增，选型不当易导致架构返工、体验降级或计费异常。本对比基于最新 v2024.07+ 文档规范，聚焦可落地的技术指标，不涉及抽象概念或未来规划。

## 关键维度对比

| 维度 | Omni Realtime API | Realtime API User Guide |
|------|------------------|--------------------------|
| **核心定位** | 端到端[多模态](../concepts/multi-modal.md)实时交互协议（语音↔文本↔语音闭环） | 低延迟流式文本生成与语音转写接口（文本/语音单向增强） |
| **输入格式** | 支持 `input.audio`（PCM16/Opus 流式音频帧）、`input.text`；需严格遵循采样率 16kHz、单声道、小端序 | `messages` 数组（类 Chat API 格式）；语音输入需**前置调用 ASR 模型**（如 `paraformer-realtime-v1`）转换为文本后传入 |
| **输出格式** | 多事件类型流式响应：<br>• `output.text`（渐进式文本）<br>• `output.audio`（TTS 合成音频流）<br>• `output.intermediate`（实时 ASR 中间结果）<br>• `session.*` / `error.*` 状态事件 | SSE 或 WebSocket 流式 token 响应：<br>• `event: message` → `delta.content`（逐 token 文本）<br>• `event: done` / `event: error`<br>• 不直接输出音频二进制或原始 ASR 流 |
| **支持模型/功能** | 仅 `qwen-omni-realtime`（统一[多模态](../concepts/multi-modal.md)模型）<br>• 内置 ASR + LLM + TTS + Voice Cloning 四合一能力<br>• 零样本/少样本声纹复刻（需 `voice_id`） | 多模型可选：<br>• 文本模型：`qwen-max`、`qwen-plus`、`qwen-turbo`<br>• 语音模型：`paraformer-realtime-v1`（仅 ASR）<br>• **不支持 TTS、声纹复刻、多模态联合推理** |
| **API 端点** | WebSocket 专用：<br>`wss://dashscope.aliyuncs.com/realtime/v1/omni` | 双协议支持：<br>• SSE：`POST https://dashscope.aliyuncs.com/api/v1/realtime/chat/completions`<br>• WebSocket：同上，但需 `Connection: upgrade` 头 |
| **会话生命周期** | 单次会话 ≤ 5 分钟；超时强制关闭；需客户端主动重连并重建 `session.create` | 单连接 ≤ 15 分钟；支持 `conversation_id` 跨请求保持上下文；中断后可通过 `continue_from` 恢复 |
| **计费方式** | 按**会话时长（秒） + 音频处理量（分钟） + 声纹调用次数**综合计费；<br>• 语音输入/输出按实际传输音频时长计费<br>• 文本交互不单独计费 | 按**模型调用次数 + 输出 token 数**计费；<br>• ASR 模型（如 `paraformer-realtime-v1`）按音频时长单独计费<br>• 文本生成模型按 `output_tokens` 计费（与标准 Chat API 一致） |
| **典型场景** | • 智能语音客服（用户说话→实时转译→AI 思考→合成语音回复）<br>• 虚拟人直播互动（唇形同步+声音克隆+上下文感知）<br>• 实时会议纪要（ASR 字幕+摘要生成+语音播报） | • 实时代码补全 IDE 插件（流式 token 响应）<br>• 客服坐席辅助（ASR 转文本 → LLM 生成回复建议 → 坐席编辑发送）<br>• 低延迟对话机器人（纯文本流式问答，无语音合成需求） |

## 适用场景建议

### ✅ 选择 Omni Realtime API 当：
- 业务要求**语音输入直出语音回复**，且对端到端延迟敏感（≤300ms）；
- 需要**定制化声音形象**（如品牌音色、人物角色音），并支持快速声纹注册与复用；
- 架构中希望**收敛多模态链路**，避免自行编排 ASR→LLM→TTS 三个独立服务；
- 场景强依赖**实时中间结果**（如边说边显示 ASR 字幕，或检测用户停顿触发追问）。

### ✅ 选择 Realtime API User Guide 当：
- 主要处理**文本交互**，语音仅作为可选输入源（需自行完成 ASR 预处理）；
- 已有成熟 ASR/TTS 服务，只需百炼提供**高并发、低延迟的 LLM 流式推理能力**；
- 需要灵活切换不同文本模型（如 `qwen-turbo` 快速响应 vs `qwen-max` 高质量生成）；
- 依赖**结构化输出**（JSON Schema）、多轮会话持久化或中断恢复等高级对话管理能力；
- 团队熟悉 SSE 协议，且倾向使用 RESTful 风格调试（相比 WebSocket 事件驱动更易排查）。

## 技术选型参考（面向开发者）

| 评估项 | Omni Realtime API | Realtime API User Guide | 建议动作 |
|---------|------------------|--------------------------|-----------|
| **客户端复杂度** | ⚠️ 高：需实现 WebSocket 连接管理、二进制音频帧编码/解码、多事件状态机、声纹注册流程 | ✅ 中：SSE 更易调试；WebSocket 仅需处理文本事件；无需处理音频编解码 | 若团队缺乏实时音视频经验，优先评估 Realtime API |
| **调试友好性** | ❌ 低：无法用 `curl` 直接测试；依赖 SDK 或自研 WebSocket 客户端；错误需结合 `error.*` 事件码分析 | ✅ 高：可用 `curl -N` 测试 SSE；响应为明文 JSON 行；`trace_id` 易关联日志 | 快速验证阶段推荐 Realtime API |
| **扩展性** | ⚠️ 中：多模态能力耦合紧密，难以单独替换 ASR 或 TTS 组件 | ✅ 高：各模块解耦，可自由组合 ASR 模型（百炼/第三方）、LLM、TTS | 长期需多供应商策略时选 Realtime API |
| **合规与审计** | ⚠️ 需注意：音频流经百炼传输，涉及声纹数据需符合《个人信息保护法》关于生物特征信息的要求 | ✅ 更可控：若 ASR 在本地完成，仅文本上传，降低敏感数据暴露面 | 涉及金融、政务等强监管场景，建议 Realtime API + 本地 ASR |
| **SDK 支持** | 提供 Python SDK（含音频流封装、重连逻辑）；其他语言需自行实现协议 | 提供 Python/Node.js SDK（含 SSE 自动解析、重连模板）；社区有更多第三方适配 | 查阅 [SDK 文档](../../raw/model-api-reference/) 确认目标语言支持度 |

> **重要提醒**：  
> - 两者**不可混用替代**：Omni Realtime API 不提供 `qwen-max` 的 JSON Schema 输出能力；Realtime API 无法返回 `output.audio` 或处理 `voice_id`。  
> - **计费隔离**：Omni 会话费用与 Realtime API 的 token 费用分别计量，控制台中归属不同服务目录，请按实际调用路径配置预算告警。  
> - **升级路径**：当前 `qwen-omni`（旧名）已完全下线，所有新项目必须使用 `qwen-omni-realtime`；Realtime API 的 `top_p` 参数已废弃，勿在请求中携带。  

如需进一步评估性能压测数据、QPS 限制详情或跨区域部署建议，请查阅对应文档末尾的「性能基准」与「运维指南」章节。

## 被对比主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)


