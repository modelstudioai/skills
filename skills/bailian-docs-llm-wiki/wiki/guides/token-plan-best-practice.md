# token plan best practice

[Token](../concepts/token.md) Plan 提供了文本生成之外的多模态能力（图像、视频、语音、决策等），但这些能力不兼容标准的 OpenAI/Anthropic 文本协议，需通过 Slash Command、Skill 或 Agent 显式调用原生接口。本文档汇总各能力的接入方式、关键参数、使用约束与最佳实践，帮助开发者快速、安全、高效地集成。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持以下核心多模态能力，均需独立接入：

- **决策模型**：`decision-model-preview`，专用于结构化判定（如评论审核、工单分类），通过 `/compatible-mode/v1/systemone` 接口同步返回 `choice`、`probabilities` 和 `confidence`，[接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md) 详细说明其并行多问题处理与置信度分流机制。
- **图像生成**：支持 `qwen-image-3.0-pro`、`wan2.7-image-pro` 等模型，通过 `/api/v1/services/aigc/multimodal-generation/generation` 同步生成图片，[接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md) 提供了完整的 Slash Command 示例与尺寸参数说明。
- **视频生成**：支持 `happyhorse-1.1-t2v`（文生视频）等模型，采用异步任务模式，需先提交再轮询 `GET /api/v1/tasks/{task_id}` 获取 `video_url`，[接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md) 给出了带重试逻辑的 Python 轮询脚本。
- **语音合成（TTS）**：`qwen-audio-3.0-tts-plus`，同步返回音频 URL；**语音识别（ASR）**：`qwen-audio-3.0-asr-flash`，同样复用 `/multimodal-generation/generation` 接口但输入为 `input_audio`，二者均需注意音色/格式匹配与 Base64 编码规范。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`，基于 WebSocket 连接，需客户端管理音频流与会话状态，[接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md) 提供了完整可运行的 Python 客户端脚本。
- **视觉理解**：非独立模型，而是通过切换 `qwen3.8-max` 等原生支持视觉的模型，或为 `glm-5.2` 等纯文本模型配置 Skill/Agent 代理调用视觉模型实现，详见 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 1 与文档 8 均列出语音识别接口为 `/api/v1/services/aigc/multimodal-generation/generation`，但文档 1 错误地将该接口同时标注为“语音识别”和“图像生成”共用入口；实际中二者虽共享同一 Endpoint，但请求体结构（`input.messages[].content[]` 内容类型）和 `model` 参数完全不同，不可混用。请以文档 8 的 ASR 请求体结构为准。

## 关键参数

所有能力均需 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`（或 `TOKEN_PLAN_API_KEY`）鉴权。核心参数按能力归类如下：

- **通用必填**：`model`（模型 ID，严格区分大小写与版本号，如 `qwen-image-3.0-pro`、`decision-model-preview`）。
- **图像生成**：`input.messages[0].content[0].text`（prompt）、`parameters.size`（如 `1024*1024`）。
- **决策模型**：`state`（待判定数据）、`questions`（结构化问题定义，含 `type`、`instructions`、`criteria`），`criteria` 边界描述比 prompt 工程更可靠。
- **视频生成**：`input.prompt`、`parameters.resolution`（`720P`/`1080P`）、`parameters.ratio`（`16:9`）、`parameters.duration`（3–15 秒）；提交时必须携带 `X-DashScope-Async: enable` 头。
- **语音合成**：`input.text`、`input.voice`（音色名，如 `longanhuan_v3.6`，需与模型匹配）、`input.format`（`mp3`/`wav`）。
- **语音识别**：`input.messages[0].content[0].input_audio.data`（URL 或 `data:audio/{format};base64,...`）、`parameters.format`（必填，如 `wav`）。
- **实时语音对话**：WebSocket URL 中 `?model=qwen-audio-3.0-realtime-plus`，会话初始化 `session.update` 中 `modalities`、`voice`、`turn_detection` 等字段决定交互行为。

## 使用方式

1. **API Key 管理**：始终将 `sk-sp-xxx` Key 配置为环境变量（`ANTHROPIC_AUTH_TOKEN` 或 `TOKEN_PLAN_API_KEY`），**禁止硬编码、写入配置文件或日志**（见 [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)）。
2. **工具扩展配置**：
   - **Slash Command**（Claude Code）：在项目根目录创建 `.claude/commands/<name>.md`，内容为带步骤的 Markdown + 内联代码块（Bash/Python）。
   - **Skill**（Codex/Qwen Code/OpenClaw）：在 `~/.<tool>/skills/<name>/SKILL.md` 中定义 YAML front matter（含 `name`、`description`）和执行逻辑。
   - **Agent**（OpenCode）：在 `.opencode/agents/<name>.md` 中定义 YAML front matter（含 `mode: subagent`、`model`）和指令。
3. **异步任务处理**：视频生成必须轮询 `GET /api/v1/tasks/{task_id}`，建议设置合理间隔（如 10 秒）与超时（`task_id` 有效期 24 小时），并处理 `FAILED`/`CANCELED` 状态。
4. **结果消费**：所有能力返回的媒体 URL（`image`、`video_url`、`audio.url`）均有短时效性，**必须立即下载并持久化**，不可缓存 URL 长期使用。

## 限制和注意事项

- **模型可用性**：`decision-model-preview` 仅限 [Token](../concepts/token.md) Plan 个人版（见 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)）；部分图像/视频模型（如 `qwen-image-2.0-pro`）为团队版专属，需核对 [个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models) 与 [团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models) 模型列表。
- **计费与用量**：各能力计费单位不同（图片张数、视频秒数、TTS 字符数、ASR 音频秒数、决策调用次数），**实际消耗以控制台 [用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 为准**，非凭请求参数估算。
- **安全红线**：API Key 严禁泄露；生成结果 URL 有时效；高风险操作（如账号封禁）必须保留人工复核环节（见 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md) 注意事项）。
- **技术约束**：
  - OpenCode 使用视觉模型需在配置文件中显式声明 `"input": ["text", "image"]`（见 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)）。
  - 实时语音对话外放易导致自激打断，**必须使用耳机**（见 [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)）。
  - ASR 单次音频时长上限为 5 分钟，格式需符合 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。

## 来源文档

- [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)
- [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)
- [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)
- [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)
- [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)
- [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)
- [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)
- [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)


