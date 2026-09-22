# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、多模态理解、工作流编排等能力的智能体应用。本文档聚焦“开始使用”核心流程，涵盖模型与功能支持范围、关键配置参数、典型使用方式及当前限制，适用于首次接入的开发者快速上手并规避常见问题。

## 支持的模型/功能

- **基础模型**：智能体应用（Agent 1.0）和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`deepseek-v3` 等主流大模型；其中 QwQ 系列模型支持深度推理与思考链输出，适用于数学、代码等强逻辑场景 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **多模态能力**：`qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 已集成至智能体应用，支持图像/视频内容解析与图文联合检索；知识库节点亦支持图片、音视频文件上传与结构化提取 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS、DMS、自建MySQL）、**图片型**（含图文检索与视觉解析），且自2025年9月起创建流程已按类型分层简化 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **高级功能**：新版智能体应用（Agent 2.0）统一将知识库、MCP 服务作为可自主规划调用的工具；[长期记忆](../concepts/memory.md) 2.0 提供自动信息提取、语义检索与用户画像管理能力 [长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档1中推荐的“千问-Max”模型在文档2的2025年12月更新中已被更名或归入新版模型体系（如 `qwen-max`），实际控制台中不再显示“千问-Max”字样，应以[模型广场](../../raw/model-user-guide/release-notes/newly-released-models.md)最新列表为准。

## 关键参数

- **知识库检索配置**：可在智能体应用中开启“知识检索增强”，并设置“初步向量检索TopK”和“初步关键词检索TopK”以控制召回数量，降低[Token](../concepts/token.md)消耗与成本 [模型调用费用](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#e58a3fee888x8)。  
- **多知识库权重**：当应用关联多个知识库时，支持为每个知识库单独设置权重值（1–10），系统优先召回高权重知识库中的片段 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **检索增强开关**：包括“多模态回复增强”（启用后解析知识库内图表/图像）和“检索配置”（控制回答范围、来源展示等），均需在应用配置页手动开启 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **[长期记忆](../concepts/memory.md)参数**：通过[长期记忆](../concepts/memory.md) 2.0 API 可配置自动提取规则、语义相似度阈值、用户画像字段映射等，不依赖人工输入 [长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 使用方式

1. **零代码快速启动**：访问[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击“创建应用” → 选择“智能体应用” → 设置名称、Prompt（如“你是一位阿里云百炼手机导购…”）、欢迎语与预设问题 → 发布即用。  
2. **知识库集成**：在[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面创建标准版知识库，支持直接上传文件（无需预先导入数据连接器）；创建完成后，在应用配置中点击“技能知识库”旁的“+”按钮添加即可 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
3. **API 调用**：支持 OpenAI 兼容的 Responses API（同步/异步模式），请求体格式与 OpenAI 完全一致，可复用现有 SDK；异步调用返回 Task ID，结果通过 `/v1/tasks/{task_id}` 查询 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。  
4. **调试与验证**：编辑智能体应用时，可使用内置“调试面板”实时调整知识库参数并查看检索召回效果，无需反复发布 [知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 限制和注意事项

- **知识库计费生效**：自2026年1月4日起，知识库服务正式商业化，费用由规格费（按实例规格计费）与模型调用费（Embedding + LLM）两部分构成，免费额度仅覆盖模型调用，不含知识库资源 [知识库商业化计费](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性限制**：QwQ 系列模型在智能体应用（Agent 1.0）中**不支持插件、流程控制、音视频交互能力**，如需完整能力请升级至 Agent 2.0 或使用工作流应用 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **文件处理限制**：非结构化知识库虽支持 Excel、HTML、音视频等格式，但单文件大小上限为 100 MB；图片解析依赖 `qwen-vl-plus` 模型，若未显式指定则默认使用基础文本 Embedding 模型，无法识别视觉内容 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **权限与分账**：子账号可独立开通知识库，但需主账号授权并配置标签（Tag）实现分账；未打标资源产生的费用将归属主账号 [分账管理](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#60dc157f979as)。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


