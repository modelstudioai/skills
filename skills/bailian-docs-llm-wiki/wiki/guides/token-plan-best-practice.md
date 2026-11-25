# token plan best practice

Token Plan 提供了覆盖文本、图像、视频、语音、实时对话和决策等多模态能力的统一计费套餐。为在各类 AI 编程工具（如 Claude Code、Qwen Code、OpenCode 等）中稳定、安全、高效地调用这些能力，需遵循统一的接入范式：使用 `sk-sp-` 开头的专用 API Key，通过 Slash Command / Skill / Agent 等扩展机制封装标准 HTTP/WebSocket 接口，并严格处理鉴权、参数、异步轮询与资源时效性。本文档汇总各能力的最佳实践，聚焦开发者实际集成要点。

## 支持的模型/功能

Token Plan 当前支持以下六大类能力，对应不同接口协议与调用方式：

| 能力类型 | 典型模型示例 | 协议 | 同步性 | 文档引用 |
|----------|--------------|------|--------|-----------|
| **决策模型** | `decision-model-preview` | HTTP POST | 同步 | [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md) |
| **图像生成** | `qwen-image-3.0-pro`, `wan2.7-image-pro` | HTTP POST | 同步 | [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md) |
| **视频生成** | `happyhorse-1.1-t2v`, `wan3.0-video` | HTTP POST + GET 轮询 | 异步 | [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md) |
| **语音合成（TTS）** | `qwen-audio-3.0-tts-plus` | HTTP POST | 同步 | [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md) |
| **语音识别（ASR）** | `qwen-audio-3.0-asr-flash` | HTTP POST | 同步 | [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md) |
| **实时语音对话** | `qwen-audio-3.0-realtime-plus` | WebSocket | 长连接 | [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md) |

> **注意**：语音识别（ASR）与图像生成（Image Generation）共用同一 Endpoint `https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，但请求体结构与 `input` 字段语义完全不同（ASR 使用 `input_audio.data`，图像生成使用 `messages[0].content[0].text`），务必按对应文档构造请求体，不可混用。

## 关键参数

所有能力均需在请求头中携带 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`，其中 `$ANTHROPIC_AUTH_TOKEN` 必须为 Token Plan 专属的 `sk-sp-` 开头 API Key（获取路径见[接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md#tp-ext-prereq)）。核心参数如下：

- **`model`**：必填，模型 ID，严格区分大小写与版本号（如 `qwen-image-3.0-pro` ≠ `qwen-image-2.0-pro`）。
- **`input`**：内容载体，格式因能力而异：
  - 决策模型：`{"state": {...}, "questions": {...}}`
  - 图像生成：`{"messages": [{"role": "user", "content": [{"text": "prompt"}]}]}`
  - 视频生成：`{"prompt": "描述"}` 或 `{"image": "...", "prompt": "描述"}`
  - TTS：`{"text": "文本", "voice": "音色名"}`
  - ASR：`{"messages": [{"role": "user", "content": [{"type": "input_audio", "input_audio": {"data": "URL或base64"}}]}]}`
  - 实时语音：通过 WebSocket `session.update` 消息配置 `voice`、`instructions` 等。
- **`parameters`**：可选，控制输出细节：
  - 图像：`size`（如 `"1024*1024"`）
  - 视频：`resolution`（`"720P"`）、`ratio`（`"16:9"`）、`duration`（秒）
  - TTS：`format`（`"mp3"`）、`sample_rate`（`22050`）
  - ASR：`format`（音频格式）、`language_hints`（`["zh"]`）

## 使用方式

1. **API Key 管理**：将 `sk-sp-xxx` 配置为环境变量 `ANTHROPIC_AUTH_TOKEN`（或 `TOKEN_PLAN_API_KEY`），**禁止硬编码到配置文件、脚本或日志中**。
2. **工具扩展配置**：
   - Slash Command（Claude Code）：创建 `.claude/commands/<name>.md`，内含带 `curl` 或 `python` 的完整执行逻辑。
   - Skill（Codex/Qwen Code/OpenClaw）：在 `~/.<tool>/skills/<name>/SKILL.md` 中定义 YAML front matter 和步骤。
   - Agent（OpenCode/Hermes）：在 `.opencode/agents/<name>.md` 或对应路径中定义 `mode: subagent` 及模型。
   - 具体路径详见[接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md#tp-ext-tools)中的“工具配置路径”表。
3. **异步任务处理（仅视频生成）**：必须实现轮询逻辑（如 `GET /api/v1/tasks/{task_id}`），检查 `task_status`，状态为 `SUCCEEDED` 时提取 `video_url`；`task_id` 有效期为 24 小时。
4. **资源下载与时效**：所有返回的 URL（图片、视频、音频）均有明确过期时间（如 `output.audio.expires_at`），必须在有效期内完成 `curl` 下载，不可缓存长期使用。

## 限制和注意事项

- **模型可用性**：`decision-model-preview` 仅限 Token Plan 个人版使用（见[接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)说明），团队版用户需确认控制台权限。
- **视觉能力启用**：即使模型支持视觉（如 `qwen3.7-plus`），OpenCode 和 OpenClaw 等工具**必须显式在配置文件中声明 `"input": ["text", "image"]`**，否则视觉输入会被忽略（见[添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)中“常见问题”部分）。
- **实时语音外放干扰**：扬声器播放的 AI 语音可能被麦克风二次采集，导致模型误判为用户持续输入并打断。**必须使用耳机**，或在 `session.update` 中调整 `turn_detection.silence_duration_ms`。
- **计费与用量**：所有调用均消耗 Token Plan Credits，具体用量以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准，不依赖本地日志或响应字段估算。
- **错误处理**：关注 HTTP 状态码：`401`（Key 无效）、`422`（请求体校验失败，响应正文含具体字段）、`429`/`529`（限流，需指数退避重试）。

## 来源文档

- [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)
- [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)
- [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)
- [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)
- [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)
- [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)
- [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)
- [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)


