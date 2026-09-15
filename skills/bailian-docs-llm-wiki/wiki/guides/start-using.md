# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、多模态理解、工作流编排等能力的智能体应用。本文档面向开发者，聚焦“开始使用”的核心操作路径、关键能力边界与必要约束，不包含营销性描述。所有功能均需通过控制台或 API 调用，无需本地部署。

## 支持的模型/功能

- **基础模型支持**：智能体应用（Agent 1.0）和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`deepseek-*` 系列模型；多模态场景推荐 `qwen-vl-plus-latest` 或 `qwen-vl-plus-2025-01-25`（详见 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)）。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建MySQL）、**图片/音视频型**（支持上传并解析视觉内容）；非结构化知识库已支持图文混合检索与自定义 metadata [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **高级能力**：新版智能体应用（Agent 2.0）将知识库与 MCP 统一为可自主规划调用的工具；[长期记忆](../concepts/long-term-memory.md) 2.0 提供语义检索、自动画像提取与多应用共享能力 [长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

> **注意**：文档 1 中推荐的“千问-Max”模型在文档 2 的 2025 年 12 月更新中已被更名/归入 `qwen-max` 系列，且其能力边界已扩展至支持 Agent 2.0 工具调用范式。实际选型请以控制台实时模型列表为准，旧版命名（如“千问-Max”）可能已下线或重定向。

## 关键参数

- **知识库检索配置**：可在智能体应用中开启“检索配置”，调整 `初步向量检索TopK` 和 `初步关键词检索TopK` 以平衡效果与成本；多知识库场景支持按权重分配召回优先级 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **多模态增强开关**：智能体应用的“检索配置”中可启用“多模态回复增强”，使模型能结合知识库中的图表/图像内容生成回答（需关联含图片索引的知识库）。  
- **[长期记忆](../concepts/long-term-memory.md)参数**：[长期记忆](../concepts/long-term-memory.md) 2.0 API 支持 `auto_extract`（自动信息抽取）、`semantic_retrieval`（语义检索）等布尔开关，显著影响召回精度与延迟。

## 使用方式

1. **零代码启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击**创建应用 → 智能体应用 → 立即创建**，完成 Prompt 设计、欢迎语与预设问题配置；随后在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建并关联知识库，最后发布应用（全程约 5 分钟）[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 集成**：  
   - 同步调用：使用 OpenAI 兼容的 `Responses API`，复用现有 OpenAI SDK；  
   - 异步调用：设置 `background=true` 获取 Task ID，后续轮询结果；  
   - 知识库管理：通过 `createindex`、`updateindex`、`getindexmonitor` 等 API 实现全生命周期控制 [创建知识库](../../raw/application-api-reference/application-component-api-reference/api-bailian-2023-12-29-dir/api-bailian-2023-12-29-dir-knowledge-base/api-bailian-2023-12-29-createindex.md)。  
3. **调试验证**：编辑智能体应用时，可直接使用内置**调试面板**在线调整知识库参数，并实时查看检索召回片段，无需反复发布 [创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。

## 限制和注意事项

- **知识库商业化**：自 2026 年 1 月 4 日起，知识库服务正式计费，费用 = 规格费 + 模型调用费；免费额度仅限部分模型调用，不覆盖知识库解析与检索 [知识库商业化计费](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用（Agent 1.0）中**不支持插件、流程编排与音视频交互能力**，仅适用于纯文本推理任务；若需完整能力，请升级至 Agent 2.0 或使用工作流应用 [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **文件处理限制**：音视频知识库仅支持常见格式（MP4/MOV/AVI/WAV/MP3），单文件上限 2GB；OCR 与语音转文字依赖 `qwen-vl-*` 或 `asr-*` 模型，需确保对应模型已开通权限。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


