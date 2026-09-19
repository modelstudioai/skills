# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、[多模态](../concepts/multimodal.md)理解、工作流编排等能力的智能体应用。本文档聚焦“开始使用”阶段的核心操作路径，涵盖模型/功能选型、关键参数配置、典型使用方式及重要限制，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型支持**：智能体应用（Agent 1.0）和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等主流模型；其中 QwQ 系列模型需注意其不支持插件、音视频交互等高级能力（详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)）。  
- **知识库类型**：支持文档型（PDF/DOCX/HTML/Excel）、音视频型（MP4/MOV/MP3/WAV）、图片型及结构化（MySQL/RDS/DMS 表）知识库；非结构化知识库已支持自定义 metadata 和标签分类 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **核心能力模块**：包括知识检索增强（RAG）、[长期记忆](../concepts/memory.md)（新版 API 已上线，支持自动提取与语义检索）、MCP 工具集成、[多模态](../concepts/multimodal.md)生成节点、文件问答（全文引用/切片检索/自定义处理三模式）及音视频实时互动。

> **注意**：文档 1 中推荐的“千问-Max”模型在文档 2 的 2025 年 12 月更新中已被更名或归入新版 Agent 2.0 模型体系；实际控制台中应以当前可用模型列表为准，旧版 Agent 1.0 的模型兼容性请参考 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整初步向量/关键词检索 TopK 值，降低 [Token](../concepts/token.md) 消耗与成本（[模型调用费用](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#e58a3fee888x8)）；多知识库场景下支持按权重分配召回优先级 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **[长期记忆](../concepts/memory.md)参数**：新版[长期记忆](../concepts/memory.md) API 支持自动信息提取、去重及用户画像管理，无需手动维护记忆条目，显著提升响应准确性与效率（详见 [长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)）。  
- **[多模态](../concepts/multimodal.md)增强开关**：智能体应用中可启用“多模态回复增强”，使模型能解析知识库内图表与图像内容，生成结合视觉信息的回答（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)）。

## 使用方式

1. **零代码快速启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击“创建应用” → 选择“智能体应用” → 设置 Prompt（如“你是一位阿里云百炼手机导购…”）→ 配置欢迎语与预设问题 → 发布前绑定知识库（参见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)）。  
2. **API 集成调用**：支持 OpenAI 兼容的 Responses API（同步/异步模式），可复用现有 OpenAI SDK；异步调用返回 Task ID，结果通过 [任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center) 查询（详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)）。  
3. **知识库直连配置**：创建知识库时可跳过独立数据连接步骤，直接上传文件或选择 DMS/RDS 数据源；调试阶段可使用内置“调试面板”实时验证检索效果（见 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)）。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用由规格费 + 模型调用费构成；2026 年 2 月起新增资源包计费选项（[知识库计费说明](../../raw/application-user-guide/knowledge-base/billing-for-knowledge-base.md)）。  
- **模型能力边界**：QwQ 系列模型虽推理能力强，但明确不支持插件、流程编排及音视频交互（见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)）；音视频知识库需配合新版 Agent 2.0 或工作流应用使用。  
- **权限与分账**：子账号可开通知识库并启用标签分账，但需主账号授权对应服务关联角色（如 `AliyunServiceRoleForSFMTelemetry`），否则应用观测等功能不可用（详见 [SFM服务关联角色](../../raw/application-api-reference/more/bailian-service-linked-role.md)）。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


