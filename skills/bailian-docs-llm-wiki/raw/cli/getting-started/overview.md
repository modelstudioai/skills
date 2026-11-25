# 阿里云百炼 CLI

为 AI Agent 打造的命令行工具，一行指令在终端调度阿里云百炼全模态 AI 能力。

**阿里云百炼 CLI** 是为 AI Agent 打造的命令行工具，把阿里云百炼的全模态能力封装为结构化工具调用。安装并配置后，只需向 Agent 下发一句自然语言需求，即可调度文本对话、图像与视频生成、语音合成识别、知识库检索、长期记忆等 10+ 项原子能力，兼容 Claude Code、Qwen Code、OpenCode、Cursor、Codex 等主流 Agent 框架。

> **重要**
>
> CLI 工具本身免费开源，按各模型及应用服务的实际调用计费，新用户享免费额度。源码与完整文档见 [GitHub 仓库](https://github.com/modelstudioai/cli)。

<a id="能力参考"></a>

## 能力参考

CLI 命令按产品线组织：模型调用、模型训练与部署、Agent 基础设施，以及平台管理与工具。

**模型调用：**

-   [文本对话与全模态](../capabilities/model-invocation/text-chat.md) — 文本生成与 Omni 全模态交互
-   [图像生成与编辑](../capabilities/model-invocation/image.md) — 图像生成、多图合成编辑
-   [视频生成与编辑](../capabilities/model-invocation/video.md) — 文生视频、图生视频、参考生视频、视频编辑
-   [语音合成与识别](../capabilities/model-invocation/speech.md) — TTS 与 ASR
-   [视觉理解](../capabilities/model-invocation/vision.md) — 图像、文档、视频解析
-   [ParseX 文档解析](../capabilities/agent-infrastructure/parsex.md) — 文档与音视频解析、结构化字段抽取
-   [批量推理](../capabilities/model-invocation/batch.md) — CSV 转 JSONL、异步批量任务与结果下载
-   [决策模型](../capabilities/model-invocation/decision.md) — 类型化决策推理与概率输出

**模型训练与部署：**

-   [数据集管理](../capabilities/training-deployment/dataset.md) — 上传、校验与管理数据集
-   [模型微调](../capabilities/training-deployment/finetune.md) — 按文本、音频、图像、视频模态创建微调任务
-   [模型部署](../capabilities/training-deployment/deploy.md) — 按文本、音频、图像模态创建部署与吞吐预留容量
-   [模型导入](../capabilities/training-deployment/cmodel.md) — 从 OSS 导入自定义模型并管理导入任务

**Agent 基础设施：**

-   [Managed Agent](../capabilities/agent-infrastructure/managed-agent.md) — Agent 生命周期、会话与状态管理
-   [Flow Agent](../capabilities/agent-infrastructure/flow-agent.md) — 智能体应用与工作流调用
-   [RAG](../capabilities/agent-infrastructure/rag.md) — 知识库语义检索与 RAG 问答
-   [Memory](../capabilities/agent-infrastructure/memory.md) — 长期记忆与用户画像
-   [联网搜索](../capabilities/agent-infrastructure/web-search.md) — 实时联网检索
-   [MCP & Skill](../capabilities/agent-infrastructure/mcp-skill.md) — MCP 服务编排与技能管理
-   [Sandbox](../capabilities/agent-infrastructure/sandbox.md) — 沙箱实例与模版生命周期管理

**平台管理与工具：**

-   [用量与配额](../capabilities/platform-management/usage-quota.md) — 用量统计、限流与权限管理
-   [监控、日志与告警](../capabilities/platform-management/monitor-log-alert.md) — 调用监控、日志与告警规则管理
-   [配置与工具](../capabilities/platform-management/config.md) — 鉴权、配置、Profile 与通用工具

<a id="从这里开始"></a>

## 从这里开始

-   [安装与鉴权](installation.md) — 安装 CLI 与 Skills，完成鉴权配置并校验
-   [快速开始](quickstart.md) — 3 步接入，向 Agent 下发第一个需求
-   [更新日志](../changelog-group/changelog.md) — 版本变更与新增能力记录

<a id="相关资源"></a>

## 相关资源

-   [在线体验](https://bailian.console.aliyun.com/playground)：无需安装，在控制台 Playground 试用能力
-   [GitHub 仓库](https://github.com/modelstudioai/cli)：源码、Issue 与完整文档
