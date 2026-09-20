# start using

阿里云百炼平台提供低门槛、高灵活性的智能体与工作流应用构建能力，支持开发者快速启动私有知识问答、多模态交互、自动化业务流程等场景。本文档汇总了“开始使用”阶段的核心要素，涵盖模型与功能支持范围、关键配置参数、典型使用路径，以及当前已知的限制与注意事项。所有内容均基于最新控制台行为与 API 规范整理，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型支持**：智能体应用（Agent 1.0）和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`deepseek-v3` 等主流大模型；视觉理解类任务推荐 `qwen-vl-plus-latest` 或 `qwen-vl-plus-2025-01-25` [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel）、**数据型**（RDS/DMS/自建MySQL）、**图片/音视频型**（含图文检索与音视频内容解析能力）[创建和使用知识库](../../raw/application-user-guide/knowledge-base/data-connection-overview/rag-knowledge-base.md)。  
- **高级能力**：  
  - 多模态回复增强（需在智能体应用中手动开启）；  
  - [长期记忆](../concepts/long-term-memory.md) 2.0（提供语义检索、自动画像提取、多应用共享记忆库）[长期记忆 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)；  
  - MCP（Model Context Protocol）服务集成，支持调用预置或自定义外部工具；  
  - 新版 Agent 2.0 已上线，将知识库与 MCP 统一为可自主规划调用的工具，完整暴露思考链路。

> **注意**：文档 1 中推荐的“千问-Max”模型仍可用，但文档 2 明确指出 Agent 1.0 已支持更优推理模型如 `qwq-plus` 和 `deepseek-v3`，且 Agent 2.0 已正式发布。建议新项目优先采用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)，而非文档 1 所述的旧版配置流程。

## 关键参数

- **知识库检索参数**：可通过调试面板实时调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 Token 量以控制成本 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **权重设置**：当一个智能体应用关联多个知识库时，可为每个知识库单独设置权重，系统按权重优先级召回内容。  
- **[长期记忆](../concepts/long-term-memory.md)配置**：启用[长期记忆](../concepts/long-term-memory.md)需通过 API 显式指定 `memory_id` 和 `user_id`，不支持控制台一键开启；旧版长期记忆 API 已标记为下线中，必须迁移至 [长期记忆 2.0](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。  
- **多模态节点参数**：工作流中的多模态生成节点需显式指定输出类型（图像/视频/音频）及提示词，不支持自动推断。

## 使用方式

1. **零代码快速启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击「创建应用」→ 选择「智能体应用」→ 设置 Prompt、欢迎语与预设问题 → 发布前绑定知识库。该流程详见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 集成调用**：  
   - 同步调用：使用 OpenAI 兼容的 `Responses API`，复用现有 OpenAI SDK；  
   - [异步调用](../concepts/asynchronous-invocation.md)：设置 `background=true`，获取 `task_id` 后轮询结果；  
   - 知识库操作：支持通过 API 创建、更新、监控知识库（如 `createindex`、`updateindex`、`getindexmonitor`）。  
3. **调试与验证**：编辑智能体应用时，可直接在控制台打开「知识库调试面板」，上传测试问题并实时查看召回片段与排序得分，无需反复发布。

## 限制和注意事项

- **知识库商业化**：自 2026 年 1 月 4 日起，知识库服务正式计费，费用包含规格费与模型调用费两部分；免费额度仅覆盖模型调用，不包含知识库存储与检索 [知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **模型兼容性限制**：QwQ 系列模型暂不支持插件、音视频交互及复杂流程编排，仅适用于纯文本推理场景；`qwen-vl-plus` 模型在智能体应用中需配合「多模态回复增强」开关方可解析知识库内图表。  
- **文件处理限制**：非结构化知识库导入 Excel 时，若含公式或宏，将被忽略；音视频知识库仅支持 MP4/MOV/MP3/WAV 格式，单文件上限 2GB。  
- **长期记忆迁移强制要求**：旧版长期记忆 API（`api-bailian-2023-12-29-dir-long-term-memory`）已进入下线流程，所有新开发必须使用 [长期记忆 2.0](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md) 接口。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


