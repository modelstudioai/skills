# token plan best practice

Token Plan 提供了覆盖文本、图像、视频、语音及结构化决策的多模态模型能力。为高效、稳定、安全地集成这些能力，开发者需根据模型类型选择对应接入方式（如同步调用、异步轮询或 WebSocket），并正确配置参数、处理返回结构与资源生命周期。本文档汇总各能力的最佳实践，聚焦可落地的技术要点。

## 支持的模型/功能

Token Plan 当前支持以下核心能力类别，每类对应专用模型与接口协议：

- **决策模型**：`decision-model-preview`，专用于结构化判断（如内容审核、工单分类），通过 `/compatible-mode/v1/systemone` 接口提供 `choice`、`probabilities` 和 `confidence` 三字段输出，不生成自然语言文本 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)。  
- **图像生成**：`qwen-image-3.0-pro`、`wan2.7-image-pro` 等，支持文生图与图生图，使用同步 `POST /api/v1/services/aigc/multimodal-generation/generation` 接口。  
- **视频生成**：`happyhorse-1.1-t2v`、`wan3.0-video` 等，采用异步任务模式，需先提交 `POST /api/v1/services/aigc/video-generation/video-synthesis`，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果。  
- **语音合成（TTS）**：`qwen-audio-3.0-tts-plus`，同步返回音频 URL；**语音识别（ASR）**：`qwen-audio-3.0-asr-flash`，同样复用 `/api/v1/services/aigc/multimodal-generation/generation` 接口，但输入为 `input_audio` 数据。  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`，基于 WebSocket 连接 `wss://token-plan.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`，需客户端管理音频流与事件解析。  
- **视觉理解**：`qwen3.8-max`、`qwen3.7-plus` 等原生支持多模态输入；对纯文本模型（如 `glm-5.2`），可通过 Skill/Agent 封装视觉模型代调实现能力扩展 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 7 中 OpenCode 配置示例要求显式声明 `"modalities": {"input": ["text", "image"]}`，而文档 8 的接口总览未体现该配置项。实际部署时，若视觉模型无响应，应优先检查工具配置中 `modalities` 字段是否已启用，而非仅依赖模型切换 [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)。

## 关键参数

所有能力均需 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`（以 `sk-sp-` 开头的 Token Plan API Key）。关键参数按能力归类如下：

| 能力 | 必选参数 | 说明 |
|--------|-----------|------|
| **决策模型** | `state`, `model`, `questions` | `state` 传入待判定数据（如评论列表）；`questions` 定义问题结构（`type`: `choice`/`score`/`noul`）与判定标准 `criteria`；`model` 固定为 `decision-model-preview` |
| **图像/语音识别** | `model`, `input.messages[0].content[0]` | 图像生成：`content` 含 `{"text": "prompt"}`；ASR：含 `{"type": "input_audio", "input_audio": {"data": "..."}}`；`parameters.size`（图像）、`parameters.format`（ASR）为常用可选参数 |
| **语音合成** | `model`, `input.text`, `input.voice` | `input.voice` 音色必须与模型版本匹配，具体列表见 [Qwen-Audio-TTS 音色列表](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/qwen-audio-tts-voice-list.md) |
| **视频生成** | `model`, `input.prompt`, `parameters.resolution`/`ratio`/`duration` | `resolution`（`480P`/`720P`/`1080P`）、`ratio`（`16:9`/`9:16`）、`duration`（3–15 秒）均需显式指定或接受默认值 |
| **实时语音** | WebSocket URL query 参数 `model`，`session.update` 中 `modalities`, `voice`, `turn_detection` | `turn_detection.type` 推荐设为 `"server_vad"` 并调优 `silence_duration_ms`（如 600ms）以平衡响应延迟与打断率 |

## 使用方式

统一采用“环境变量 + 工具扩展”模式，避免硬编码密钥：

- **API Key 管理**：将 `sk-sp-xxx` 配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`（或 `$TOKEN_PLAN_API_KEY`），所有示例脚本均优先读取后者，其次读取前者。  
- **扩展机制适配**：  
  - *Slash Command*（Claude Code）：在 `.claude/commands/<name>.md` 中定义步骤与 curl/Python 脚本；  
  - *Skill*（Codex/Qwen Code/OpenClaw）：在对应路径创建 `SKILL.md`，需包含 YAML front matter（`name`, `description`）；  
  - *Agent*（OpenCode）：在 `.opencode/agents/<name>.md` 中定义 `mode: subagent` 与 `model` 字段，注意模型 ID 格式为 `bailian-token-plan/<model-id>`。  
- **异步任务处理**：视频生成必须实现轮询逻辑（建议 10s 间隔），`task_id` 有效期 24 小时；所有生成类 URL（图像、语音、视频）均有明确过期时间，需立即下载。  
- **错误处理**：关注 HTTP 状态码——`401` 检查 Key，`422` 查看响应体中的校验失败字段，`429`/`529` 实施指数退避重试。

## 限制和注意事项

- **模型可用性限制**：决策模型当前**仅支持 Token Plan 个人版**，团队版暂未开放 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)；图像/视频/语音模型在个人版与团队版的支持列表存在差异，务必以控制台最新文档为准。  
- **资源与安全约束**：  
  - ASR 单次音频时长 ≤ 5 分钟，格式需符合 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)；  
  - 实时语音需本地麦克风权限，外放易引发自激打断，**必须使用耳机**；  
  - API Key 绝不可写入命令文件、代码仓库或日志，所有脚本均应通过环境变量注入。  
- **业务逻辑设计**：  
  - 决策模型的 `confidence` 是分流核心依据（如 `>= 0.9` 自动执行，`< 0.9` 转人工），阈值需按误判成本调整，而非固定使用示例值；  
  - 复杂判断应拆解为多个独立 `questions`，在客户端组合结果，而非堆砌复杂 prompt；  
  - 高风险动作（如账号封禁）必须保留人工复核环节，模型输出仅为辅助依据。

## 来源文档

- [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)
- [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)
- [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)
- [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)
- [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)
- [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)
- [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)
- [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)


