# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建基于大模型的私有知识问答、智能体和工作流应用。核心能力围绕模型调用、知识库集成、[长期记忆](../concepts/long-term-memory.md)、MCP 工具编排及多模态处理展开，支持同步/异步 API 调用与全链路可观测性。本文档聚焦“开始使用”阶段的关键路径与技术要点，适用于首次接入的开发者。

## 支持的模型/功能

- **基础模型**：支持 Qwen 系列（如 `qwen-max`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25`）、QwQ 系列（`qwq-plus`、`qwq-32b`）及 DeepSeek 系列模型，覆盖文本生成、多模态理解与深度推理场景 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **智能体应用（Agent 2.0）**：统一将知识库、MCP 服务作为可自主规划调用的工具，完整暴露模型思考链与工具执行过程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **工作流应用**：支持多模态生成节点（图像/视频/音频）、批量节点、条件判断节点，以及 Dify 工作流一键导入；知识库节点提供“必定调用”“智能调用”“旧版调用”三种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **知识库类型**：分为**文档**、**数据**（结构化，支持 RDS/MySQL/DMS）、**图片**三类；支持音视频知识库（含直播回放问答、字幕生成等场景）及图文混合检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md) & 用户画像管理 API 支持多应用共享、自动信息提取、语义检索与用户画像构建，显著优于旧版 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 2 中提及的“智能体应用（Agent 1.0）”已由 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 明确标注为被新版 Agent 2.0 取代；实际开发应优先采用 Agent 2.0 架构，其能力覆盖并增强旧版全部功能。

## 关键参数

- **知识库检索参数**：可通过降低 `initial_vector_topk` 和 `initial_keyword_topk` 减少送入排序模型的 Token 量，直接降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **权重设置**：当智能体应用关联多个知识库时，可为每个知识库配置权重，系统按权重优先级召回内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **多模态识别开关**：在智能体应用检索配置中启用“多模态回复增强”，可激活对知识库中图表/图像的解析能力，提升视觉信息融合精度 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- **异步任务标识**：调用工作流或应用 API 时，设置 `background=true` 即可触发异步模式，立即返回 Task ID，后续通过 `/tasks/{task_id}` 查询结果 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码入门（推荐）**：  
   - 创建智能体应用 → 选择模型（如 `qwen-max`）→ 配置 System Prompt 与预设问题 → 添加知识库（支持文档/Excel/音视频/数据库直连）→ 发布应用。全程无需编码，详见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **API 集成**：  
   - 同步调用：复用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/v1/chat/completions`），适用于实时交互场景；  
   - 异步调用：请求中携带 `background=true`，获取 Task ID 后轮询 `/v1/tasks/{id}`；  
   - 知识库管理：使用 `POST /v1/knowledge_bases` 创建、`PATCH /v1/knowledge_bases/{id}` 更新、`GET /v1/knowledge_bases/{id}/monitor` 查询监控数据 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
3. **高代码扩展**：  
   - 基于 Python 项目结构部署后端服务，内置自动化运维与可观测性能力，适用于企业级定制需求 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费生效时间**：知识库服务自 2026 年 1 月 4 日起正式计费，费用包含规格费与模型调用费两部分，需提前评估成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用（Agent 1.0）中**不支持插件、流程、音视频交互能力**，仅限纯文本推理；若需完整能力，必须使用 Agent 2.0 或工作流应用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试依赖**：知识库调试面板仅在编辑智能体应用时可用，用于实时调整参数并验证召回效果；工作流应用暂无等效在线调试界面 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件解析限制**：非结构化知识库支持离线 HTML、Excel、PDF、DOC 等格式，但音视频文件需经 ASR/Vision 模型解析为文本/特征向量，原始二进制不可直接检索 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)
- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)


