# token plan best practice

Token Plan 提供了多种 AIGC 能力的标准化接入方式，涵盖决策模型、多模态生成（图像/视频）、语音处理（合成/识别）及实时语音对话。本文档面向开发者，总结各能力的通用接入模式、关键参数、使用约束与最佳实践，帮助你高效、稳定地集成 Token Plan 服务。

## 支持的模型/功能

Token Plan 当前支持以下核心能力，均通过统一 API 基础设施提供，但调用协议和行为模式各异：

- **决策模型**：`decision-model-preview`，专用于结构化判断（如内容审核、工单分类），同步返回 `choice`、`probabilities` 和 `confidence`，不生成自然语言文本，显著降低 token 开销 [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)。  
- **图像生成**：包括 `qwen-image-3.0-pro`、`wan2.7-image-pro` 等，支持文生图与图生图，同步返回图片 URL [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)。  
- **视频生成**：包括 `happyhorse-1.1-t2v`（文生视频）、`happyhorse-1.1-i2v`（图生视频）等，采用异步任务模式，需轮询 `GET /api/v1/tasks/{task_id}` 获取结果 [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)。  
- **语音识别（ASR）**：`qwen-audio-3.0-asr-flash`，支持非实时音频转写，输入可为公网 URL 或 Base64 Data URI [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)。  
- **语音合成（TTS）**：`qwen-audio-3.0-tts-plus`，将文本转为音频流，返回带过期时间的 `output.audio.url` [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)。  
- **实时语音对话**：`qwen-audio-3.0-realtime-plus`，基于 WebSocket 协议，支持双向音频流与实时转录，需本地运行客户端脚本 [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)。  
- **视觉理解**：原生支持模型（如 `qwen3.8-max`、`qwen3.7-plus`）可直接处理图片；纯文本模型（如 `glm-5.2`）可通过 Skill/Agent 代理调用视觉模型实现扩展能力 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。

> **注意**：文档 2 和文档 3 中关于模型支持范围的描述存在不一致——文档 2 称 `qwen-image-2.0-pro` 和 `qwen-image-2.0` 为“团队版专属”，而文档 3 未明确限定其可用版本；实际以控制台[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)模型列表为准，建议在控制台确认当前订阅版本所含模型。

## 关键参数

所有能力均依赖统一的认证机制和基础参数，但具体字段因能力而异：

- **认证**：全部接口使用 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`（或 `TOKEN_PLAN_API_KEY`），API Key 必须为 `sk-sp-` 开头的 Token Plan 套餐密钥。  
- **模型标识**：`model` 字段为必填，值必须严格匹配文档中列出的模型 ID（如 `decision-model-preview`、`qwen-image-3.0-pro`），拼写错误将导致 `404` 或 `422` 错误。  
- **输入格式**：
  - 决策模型：通过 `state`（结构化上下文）和 `questions`（类型化问题）传入，`questions` 中每个 key 对应一个独立判定项。
  - 多模态生成（图像/视频/ASR/TTS）：统一使用 `input` 字段嵌套内容，如 `input.messages[0].content[0].text`（图像）、`input.messages[0].content[0].input_audio.data`（ASR）、`input.text`（TTS）。
  - 实时语音：通过 WebSocket 发送 JSON event，如 `input_audio_buffer.append` 或 `session.update`。
- **输出控制**：
  - `confidence`（决策模型）：0–1 浮点数，用于分流策略（如 `>= 0.9` 自动执行，`< 0.9` 转人工）。
  - `parameters`（图像/视频）：控制分辨率（`size`/`resolution`）、宽高比（`ratio`）、时长（`duration`）、采样率（`sample_rate`）等，不指定则取默认值。
  - `output.audio.url`（TTS/ASR）和 `output.video_url`（视频）均为临时链接，需及时下载。

## 使用方式

所有能力均通过 Agent 工具的扩展机制（Slash Command / Skill / Agent）调用，通用流程如下：

1. **配置密钥**：将 `sk-sp-xxx` API Key 设置为环境变量 `$ANTHROPIC_AUTH_TOKEN`（或 `$TOKEN_PLAN_API_KEY`），**严禁硬编码到配置文件或日志中**。  
2. **创建扩展**：按工具类型将对应能力的配置内容保存至标准路径（如 Claude Code → `.claude/commands/<name>.md`；OpenCode → `.opencode/agents/<name>.md`）。完整路径映射见 [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)。  
3. **触发执行**：在工具中输入对应指令（如 `/text-to-image 一只猫`、`/review-comments comments.txt`），工具自动解析参数、构造请求并处理响应。  
4. **结果消费**：
   - 同步能力（决策、图像、ASR、TTS）：直接解析 JSON 响应体，提取 `answers.c1.choice`、`output.choices[0].message.content[0].image`、`output.text`、`output.audio.url` 等字段。
   - 异步能力（视频）：提交后获取 `task_id`，轮询 `GET /api/v1/tasks/{task_id}` 直至 `task_status == "SUCCEEDED"`，再提取 `output.video_url`。
   - 实时能力（语音）：运行独立 Python 客户端，由本地 `sounddevice` 采集/播放音频，WebSocket 透传至服务端。

## 限制和注意事项

- **计费与用量**：各能力 Credits 消耗不同（视频 > 图像 > 语音 > 决策），实际用量以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准，不依赖请求次数而取决于输出规模（如图片数量、视频秒数、字符数、音频时长）。  
- **URL 时效性**：所有生成资源（图片、视频、音频）的 `url` 字段均有时效限制，必须在返回后立即下载，不可缓存长期使用。  
- **输入约束**：
  - 视频生成：单次任务时长 3–15 秒，分辨率与模型强绑定（如 `happyhorse-1.1-t2v` 不支持 `4K`）。
  - 语音识别：音频时长 ≤ 5 分钟，格式需符合 [音频规格](https://help.aliyun.com/zh/model-studio/asr-model#asr_audio_spec02)。
  - 实时语音：需本地麦克风/扬声器权限，外放易引发回声打断，**强烈建议使用耳机**。  
- **安全与稳定性**：
  - 请求失败需按状态码处理：`401`（密钥无效）、`422`（参数校验失败，响应体含具体错误字段）、`429`/`529`（限流，需指数退避重试）。
  - 高风险动作（如账号封禁、资金操作）**不得仅依赖模型 `choice` 自动执行**，必须保留人工复核环节。
  - 视觉模型需显式声明 `modalities.input = ["text", "image"]`（如 OpenCode、OpenClaw 配置），否则即使模型支持也无法启用视觉能力 [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)。

## 来源文档

- [接入决策模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)
- [接入视频生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)
- [接入图像生成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)
- [接入概览](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-integration-overview.md)
- [接入语音识别模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)
- [添加视觉理解能力](../../raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)
- [接入语音合成模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)
- [接入实时语音对话模型](../../raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)


