# start using

阿里云百炼平台提供零代码与低代码方式快速构建 AI 应用的能力，支持智能体、工作流、高代码等多种应用类型。开发者可基于私有知识文档快速搭建问答助手，或通过 API 集成至自有系统。本文档聚焦“开始使用”路径，梳理核心能力、关键配置项及实践约束，帮助开发者高效启动首个应用。

## 支持的模型/功能

- **智能体应用（Agent）**：支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 等模型；新版 Agent 2.0（2025年12月上线）统一将知识库、MCP 作为可自主规划调用的工具，并完整展示思考链与工具执行过程 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **工作流应用**：支持多模态生成节点（图像/视频/音频）、批量节点、条件判断节点；大模型节点兼容 DeepSeek 系列、QwQ 系列及 `text-embedding-v4` 模型；知识库节点支持必定调用、智能调用和旧版调用三种模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库**：支持三类知识库——**文档**（含 PDF/DOCX/HTML/Excel/音视频）、**数据**（RDS、DMS、自建 MySQL）、**图片**；非结构化知识库支持自定义 metadata 与图文混合检索；结构化知识库支持图片索引，提问时可上传图片触发视觉内容召回 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **[长期记忆](../concepts/long-term-memory.md)**：新版[长期记忆](../concepts/long-term-memory.md) & 用户画像管理 API（2026年1月上线）支持多应用共享记忆库、自动信息提取、语义检索及用户画像管理，显著优于旧版 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中提及“智能体编排应用”已于 2024 年 12 月 12 日下线（见“2024年12月16日”条目），当前统一为“智能体应用（Agent 1.0/2.0）”和“工作流应用”，请勿再参考已下线的编排应用文档。

## 关键参数

- **知识库检索参数**：可通过降低 `初步向量检索TopK` 和 `初步关键词检索TopK` 减少送入排序模型的 [Token](../concepts/token.md) 量，从而降低模型调用费用 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权重设置**：当智能体应用关联多个知识库时，可为每个知识库单独设置权重，系统优先召回高权重知识库中的内容 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **多模态回复增强**：智能体应用中开启该开关后，可解析知识库中的图表与图像内容，实现结合视觉信息的精准回答（需关联支持多模态的 VL 模型） [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **异步运行模式**：工作流应用支持异步执行，请求立即返回 Task ID，后续通过 `/tasks/{task_id}` 查询结果；适用于耗时较长的任务 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 使用方式

1. **零代码入门（推荐）**：  
   - 访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) → 创建「智能体应用」→ 选择模型（如 `qwen-max`）→ 编写 System Prompt → 配置欢迎语与预设问题；  
   - 在 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面创建知识库，上传文档（支持 DOCX/PDF/HTML/Excel/音视频）→ 选择「智能切分」→ 完成解析；  
   - 返回应用配置页，在「技能知识库」中添加已创建的知识库 → 发布应用。详细步骤见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  

2. **API 调用**：  
   - 同步调用：复用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/v1/responses`），适用于实时交互场景；  
   - 异步调用：在请求中设置 `background=true`，获取 Task ID 后轮询 `/v1/tasks/{id}`；  
   - 知识库管理：支持 `POST /v1/knowledge_bases` 创建、`PATCH /v1/knowledge_bases/{id}` 更新、`GET /v1/knowledge_bases/{id}/monitor` 查询监控数据等 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费生效时间**：知识库服务自 2026 年 1 月 4 日起正式计费，费用由规格费 + 模型调用费构成；资源包支持 RAG 标准版与旗舰版两种购买方式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型（如 `qwq-plus`）仅支持工作流应用与智能体应用（Agent 1.0），不支持插件、流程编排及音视频交互能力 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **文件限制**：音视频知识库支持 MP4/MOV/AVI/WAV/MP3 等格式，单文件大小上限为 2GB；非结构化知识库导入 HTML 文件需为离线本地文件，不支持远程 URL [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **调试与观测**：编辑智能体应用时可使用内置「调试面板」实时调整知识库参数并验证召回效果；端到端应用处理流程可通过 [应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe) 查看 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 来源文档

- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)
- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)


