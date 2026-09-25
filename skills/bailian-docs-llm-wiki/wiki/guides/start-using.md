# start using

阿里云百炼平台提供低门槛、高灵活性的智能体与工作流应用构建能力，支持开发者快速启动私有知识问答、多模态交互、自动化业务流程等场景。本文档面向开发者，聚焦“首次使用”路径，涵盖模型/功能选型、关键参数配置、操作方式及重要限制，所有内容均基于当前控制台与API的最新行为整理。

## 支持的模型/功能

- **核心应用类型**：智能体应用（Agent 1.0 和 Agent 2.0）、工作流应用、高代码应用（Python后端服务）以及音视频实时互动应用 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **模型支持**：  
  - 智能体应用支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-01-25` 及 DeepSeek 系列模型；  
  - 工作流应用支持 `qwq-plus`、`qwq-32b`、DeepSeek 系列及多模态生成节点；  
  - 知识库向量化默认使用 `text-embedding-v4`（推荐），也兼容 `v3`；图片解析可选 `qwen-vl-max` 或 `qwen-vl-plus` [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **知识库类型**：文档类（PDF/DOCX/HTML/Excel）、音视频类（MP4/MKV/MP3/WAV）、结构化类（MySQL/RDS/DMS 表），并支持图文混合检索与离线 HTML 导入 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

> **注意**：文档 1 中建议新手选用“千问-Max”模型，但文档 2 明确指出智能体应用已全面支持 `qwq-plus`、`qwen-vl-plus-2025-01-25` 等更先进模型，且 Agent 2.0 已将知识库与 MCP 统一为工具调用。因此，“千问-Max”仅为历史默认选项，非当前最优实践。

## 关键参数

- **知识库检索参数**：可通过调试面板或 API 调整 `初步向量检索TopK` 和 `初步关键词检索TopK`，降低送入排序模型的 [Token](../concepts/token.md) 量以优化成本 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **权重配置**：当智能体关联多个知识库时，支持按信息源重要性设置权重，系统优先召回高权重知识库内容。  
- **长期[记忆](../concepts/memory.md)参数**：新版长期[记忆](../concepts/memory.md) API 支持自动提取关键信息、语义检索增强及用户画像管理，替代旧版手动输入模式 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **多模态增强开关**：智能体应用中可启用“多模态回复增强”，使模型能解析知识库中的图表与图像内容，提升视觉相关问答准确性。

## 使用方式

1. **零代码启动**：访问 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，创建智能体应用 → 选择模型 → 配置 System Prompt（如“你是一位阿里云百炼手机导购…”）→ 设置欢迎语与预设问题 → 发布前绑定知识库 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **知识库构建**：支持两种路径：  
   - 控制台快捷路径：创建应用时直接上传文件（如 `.docx`），系统自动完成数据连接、切分与索引；  
   - API 路径：调用 `createindex` 接口创建音视频或结构化知识库，支持 MySQL/DMS 数据源同步。  
3. **API 调用**：  
   - 同步调用：使用 OpenAI 兼容的 Responses API，适用于实时交互；  
   - 异步调用：设置 `background=true`，返回 Task ID 后通过任务中心查询结果；  
   - 应用评测、监控、长期[记忆](../concepts/memory.md)等能力均提供独立 API 接口 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。

## 限制和注意事项

- **计费变更**：知识库服务自 2026 年 1 月 4 日起正式商业化，费用由规格费 + 模型调用费构成；2026 年 2 月起新增资源包计费模式，支持 RAG 标准版/旗舰版 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **模型兼容性**：QwQ 系列模型在智能体应用中**不支持插件、流程编排与音视频交互能力**，仅适用于纯文本推理场景；其在工作流应用中则无此限制。  
- **知识库调试依赖权限**：子账号开通知识库需主账号授权分账标签，且部分高级功能（如音视频解析、图文检索）需对应模型配额与权限开通。  
- **Agent 1.0 与 2.0 共存**：Agent 2.0 已上线，但 Agent 1.0 仍维护；二者在知识库调用逻辑、工具抽象层级上存在差异，迁移前需评估业务适配性。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


