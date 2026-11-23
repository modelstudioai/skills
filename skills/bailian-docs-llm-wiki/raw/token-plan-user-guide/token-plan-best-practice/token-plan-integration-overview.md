# 接入概览

Agent 工具原生只处理文本生成协议。图像生成、视频生成、语音合成、语音识别、实时语音对话和决策模型需要通过 Slash Command、Skill 或 Agent 调用原生接口。

## 为什么需要扩展

Claude Code、Codex、OpenCode、Qwen Code 等 Agent 工具原生只处理文本生成协议（OpenAI 兼容或 Anthropic 兼容）。Token Plan 中的图像生成、视频生成、语音合成、语音识别、实时语音对话和决策模型不在这套协议内，需要工具通过 Slash Command、Skill 或 Agent 调用各自的接口。

## 接口总览

能力

接口

决策模型

`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`

图像生成

`https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

视频生成（提交）

`https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

视频生成（查询）

`https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

语音合成

`https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer`

语音识别

`https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

实时语音对话

`wss://token-plan.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.0-realtime-plus`

## 快速接入

按要接入的能力选择对应文档，具体配置步骤见各文档。

[

**接入决策模型**

同步，结构化返回

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-decision-model.md)[

**接入图像生成模型**

同步

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-image-generation.md)[

**接入视频生成模型**

异步任务

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-video-generation.md)[

**接入语音合成模型**

同步

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-synthesis.md)[

**接入语音识别模型**

同步

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-speech-recognition.md)[

**接入实时语音对话模型**

WebSocket

](raw/token-plan-user-guide/token-plan-best-practice/token-plan-realtime-voice.md)[

**添加视觉理解能力**

切换视觉模型，或 Skill/Agent 代调

](raw/token-plan-user-guide/token-plan-best-practice/add-vision-skill.md)

### 前提

-   已订阅 Token Plan。个人版在 [我的订阅（个人版）](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal) 获取以 `sk-sp-` 开头的 API Key；团队版在 [成员管理](https://bailian.console.aliyun.com/cn-beijing/subscription/uac-admin/organization/members/list) 分配席位后获取 API Key。
-   使用的工具支持上表中的扩展方式。

### 工具配置路径

下表以图像生成为例。接入其他能力时，将 `text-to-image` 替换为对应能力的命令名，将 `token-plan-image` 替换为对应的 Skill 名。

工具

扩展机制

配置文件路径

Claude Code

Slash Command

`.claude/commands/text-to-image.md`

Codex

Skill

`~/.codex/skills/token-plan-image/SKILL.md`

Qwen Code

Skill

`~/.qwen/skills/text-to-image/SKILL.md`

OpenCode

Agent

`.opencode/agents/text-to-image.md`

OpenClaw

Skill

`~/.openclaw/workspace/skills/token-plan-image/SKILL.md`

Hermes Agent

Skill

`~/.hermes/skills/media/text-to-image/SKILL.md`

Qoder

Skill

`~/.qoder/skills/text-to-image/SKILL.md`

## 计费与安全

-   各能力的计费方式不同，实际 Credits 消耗以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准。
-   API Key 只在工具配置或环境变量中使用，不要写入命令文件、代码仓库或日志。
-   生成结果的 URL 有时效，使用后及时下载。
