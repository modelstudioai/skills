# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、多模态理解、工作流编排等能力的智能体应用。本文档聚焦“开始使用”阶段的核心操作路径，涵盖模型与功能选型、关键参数配置、典型使用方式及重要限制，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型支持**：智能体应用（Agent 1.0）和工作流应用均支持 Qwen 系列（如 `qwen-max`、`qwen-vl-plus-latest`）、QwQ 系列（如 `qwq-plus`、`qwq-32b`）及 DeepSeek 系列模型；其中 QwQ 模型需注意其不支持插件、音视频交互等高级能力，详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel 等非结构化文本）、**数据型**（RDS、DMS、自建 MySQL 等结构化数据源）和**图片型**（含图文检索与图表解析能力），创建时可按场景直接选择，无需预导入数据 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。
- **增强能力**：新版智能体应用（Agent 2.0）已统一将知识库与 MCP 作为可自主规划调用的工具；[长期记忆](../concepts/long-term-memory.md)（2.0 版）提供语义检索、自动信息提取与用户画像管理能力，显著优于旧版 [长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 1 中推荐的“千问-Max”模型在文档 2 的 2025 年 12 月更新中已被更名或归入 Qwen 系列新命名体系（如 `qwen-max`），实际控制台中请以当前模型广场显示为准，避免依赖过时型号名称。

## 关键参数

- **知识库检索配置**：在智能体应用的“检索配置”中可调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低该值可减少排序模型 Token 消耗，从而优化成本 [知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#e58a3fee888x8)。
- **多知识库权重**：当应用关联多个知识库时，可通过权重设置控制召回优先级，权重越高，相关片段越可能被优先检索并送入大模型上下文。
- **多模态增强开关**：在 Agent 1.0 的检索配置中启用“多模态回复增强”，可激活对知识库中图表、图像内容的解析能力，提升视觉信息融合回答的准确性。

## 使用方式

1. **零代码快速启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击“创建应用” → 选择“智能体应用” → 设置 Prompt（如“你是一位阿里云百炼手机导购…”）→ 配置欢迎语与预设问题 → 发布前绑定知识库（支持直接上传文件创建，无需预先走数据连接流程）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
2. **API 集成调用**：支持 OpenAI 兼容的 Responses API，提供同步调用（即时响应）与异步调用（返回 Task ID 后轮询）两种模式，适用于 Web/iOS/Android 等多端集成 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
3. **音视频与多模态扩展**：知识库支持上传音视频文件并启用智能切分；智能体应用可结合 `qwen-vl-plus` 等多模态模型实现图文/音视频混合问答；工作流应用新增多模态生成节点，支持根据提示词生成图像、视频或音频。

## 限制和注意事项

- **知识库商业化计费**：自 2026 年 1 月 4 日起，知识库服务正式计费，费用由规格费（按版本：标准版/旗舰版）与模型调用费（含 embedding 与 rerank）两部分构成，免费额度已取消 [知识库商业化公告](https://www.aliyun.com/notice/117726)。
- **模型能力边界**：QwQ 系列模型虽推理能力强，但明确不支持插件调用、音视频实时互动等交互能力；DeepSeek 系列模型在工作流与智能体中可用，但需确认具体版本是否支持 RAG 增强链路。
- **调试与验证**：知识库编辑界面内置调试面板，可在配置智能体应用时实时调整参数并验证检索召回效果，避免发布后才发现语义偏差或切片失效问题。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


