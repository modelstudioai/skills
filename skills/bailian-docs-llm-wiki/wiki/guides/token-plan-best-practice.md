# token plan best practice

[Token](../concepts/token.md) Plan 提供了覆盖文本、图像、视频、语音、实时对话和决策推理的多模态能力，但这些能力不通过标准 LLM 协议（如 OpenAI 或 Anthropic）暴露，需通过专用接口和工具扩展机制接入。本文档汇总各能力的接入方式、关键参数、使用约束及最佳实践，帮助开发者高效集成。

## 支持的模型/功能

[Token](../concepts/token.md) Plan 当前支持以下核心能力，每类对应独立接口与模型：

- **决策模型**：`decision-model-preview`，专用于结构化判定（如评论审核、工单分类），通过 `/compatible-mode/v1/systemone` 接口调用，返回 `choice`、`probabilities` 和 `confidence` 三字段，不生成自然语言文本 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)。
- **图像生成**：支持 `qwen-image-3.0-pro`、`wan2.7-image-pro` 等多款文生图/图生图模型，接口为 `POST /api/v1/services/aigc/multimodal-generation/generation`，同步返回图片 URL [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)。
- **语音合成（TTS）**：`qwen-audio-3.0-tts-plus`，支持多音色、多格式输出，接口为 `POST /api/v1/services/audio/tts/SpeechSynthesizer`，返回带过期时间的音频 URL [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)。
- **语音识别（ASR）**：`qwen-audio-3.0-asr-flash`，非实时识别，接口复用图像生成路径 `POST /api/v1/services/aigc/multimodal-generation/generation`，但 `input` 中需传 `input_audio` 类型内容 [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)。
- **视频生成**：`happyhorse-1.1-t2v` 等模型，采用异步任务模式，需先提交 `POST /api/v1/services/aigc/video-generation/video-synthesis`，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果 [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)。
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`，基于 WebSocket 连接 `wss://token-plan.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=...`，需客户端处理音频流收发 [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)。
- **视觉理解**：`qwen3.8-max`、`qwen3.7-plus` 等原生支持图像输入；纯文本模型（如 `glm-5.2`）可通过 Skill/Agent 代理调用视觉模型实现 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 1 和文档 7 均列出语音识别接口为 `/api/v1/services/aigc/multimodal-generation/generation`，但文档 1 将其归类为“语音识别”，而文档 7 明确指出该接口同时承载图像生成与语音识别——这并非矛盾，而是同一通用多模态接口根据 `input` 内容类型动态路由。实际使用时以文档 7 的请求体结构为准。

## 关键参数

所有能力均需 `Authorization: Bearer <API Key>` 头，API Key 必须为 [Token](../concepts/token.md) Plan 套餐专属（以 `sk-sp-` 开头），且仅限在环境变量（如 `$ANTHROPIC_AUTH_TOKEN` 或 `$TOKEN_PLAN_API_KEY`）中使用，严禁硬编码或日志输出。

| 能力 | 必填参数 | 说明 |
|--------|-----------|------|
| **决策模型** | `state`, `model="decision-model-preview"`, `questions` | `questions` 中每个 key 对应一个判定问题，`type` 可为 `choice`/`score`/`noul`；`criteria` 定义判定边界，比 prompt 更稳定 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)。 |
| **图像生成** | `model`, `input.messages[0].content[0].text` | `parameters.size`（如 `1024*1024`）可选，未指定时由模型自动选择；URL 有时效性，需立即下载。 |
| **语音合成** | `model="qwen-audio-3.0-tts-plus"`, `input.text`, `input.voice` | `input.format` 默认 `mp3`，支持 `pcm`/`wav`/`opus`；`input.sample_rate` 默认 `22050`。 |
| **语音识别** | `model="qwen-audio-3.0-asr-flash"`, `input.messages[0].content[0].input_audio.data` | `data` 字段必须为公网 URL 或 `data:audio/{format};base64,...` 格式；`parameters.format` 必填（如 `wav`）。 |
| **视频生成** | `model`, `input.prompt`, `X-DashScope-Async: enable` | `parameters.resolution`（`480P`/`720P`/`1080P`）、`ratio`（`16:9`/`9:16`）、`duration`（3–15 秒）均为可选，默认值见文档。 |
| **实时语音对话** | WebSocket URL 中 `model` 参数、`session.update` 消息中的 `voice` 和 `instructions` | `input_audio_format` 和 `output_audio_format` 必须为 `pcm`；`turn_detection` 配置服务端 VAD 参数。 |

## 使用方式

接入流程统一为三步：**配置 API Key → 创建工具扩展（Slash Command/Skill/Agent）→ 触发调用**。

- **API Key 配置**：个人版在 [我的订阅（个人版）](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 获取 `sk-sp-xxx`，团队版通过成员管理分配。必须设为环境变量，不可写入配置文件。
- **工具扩展创建**：
  - *Slash Command*（Claude Code）：在 `.claude/commands/` 下新建 `.md` 文件，内含 `curl` 或 Python 脚本逻辑；
  - *Skill*（Codex/Qwen Code/OpenClaw）：在对应 `skills/` 目录下建子目录并放 `SKILL.md`，需包含 YAML front matter；
  - *Agent*（OpenCode）：在 `.opencode/agents/` 下建 `.md` 文件，front matter 中声明 `mode: subagent` 和 `model`。
  各工具路径详见 [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md) 的“工具配置路径”表。
- **触发调用**：
  - 决策/图像/语音等同步能力：直接执行命令（如 `/review-comments comments.txt` 或 `/text-to-image 一只猫`）；
  - 视频生成：命令提交后自动轮询，无需手动查任务；
  - 实时语音：运行生成的 Python 脚本，麦克风输入直连 WebSocket；
  - 视觉理解：对纯文本模型，用 `@image-analyzer` 或 `/skill image-analyzer` 显式调用代理 Skill。

## 限制和注意事项

- **计费与用量**：各能力独立计费，图像按张、语音按字符、视频按生成时长、决策按判定次数、实时语音按连接时长。实际消耗以控制台 [用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 为准，非请求次数。
- **时效性约束**：所有生成结果（图片、音频、视频 URL）均有短期有效期（通常数分钟至数小时），必须及时下载，不可缓存长期使用。
- **模型兼容性**：视觉理解能力依赖工具配置。例如 OpenCode 需在 provider 配置中显式声明 `"input": ["text", "image"]`，否则即使使用 `qwen3.7-plus` 也无法解析图片 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。
- **错误处理**：
  - `401 Unauthorized`：检查 API Key 是否正确、是否过期；
  - `422 Unprocessable Entity`：检查请求体 JSON 结构，响应正文会指明具体字段错误；
  - `429 Too Many Requests` / `529 Backend Error`：实施指数退避重试；
  - 视频任务 `FAILED`：检查 `parameters` 是否超出模型支持范围（如 `duration=20` 超出 15 秒上限）。
- **安全红线**：API Key 绝对禁止出现在代码仓库、命令文件、日志或前端代码中；生成结果 URL 不可公开分享，避免被他人盗用配额。

## 来源文档

- [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)
- [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)
- [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)
- [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)
- [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)
- [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)
- [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)
- [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)


