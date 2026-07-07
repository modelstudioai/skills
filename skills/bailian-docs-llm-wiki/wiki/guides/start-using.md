# start using

阿里云百炼提供零代码方式快速构建基于私有知识的问答应用，同时持续迭代应用、[知识库](../concepts/knowledge-base.md)、[工作流](../concepts/workflow.md)等核心能力。本页汇总从创建第一个[智能体应用](../concepts/agent-application.md)到跟踪功能动态所需的关键信息，帮助开发者快速上手并了解平台最新能力。

## 快速构建私有知识问答应用

借助百炼的[智能体应用](../concepts/agent-application.md)构建能力，可在约 5 分钟内零代码完成一个能回答私有领域问题的大模型问答应用，完整流程见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。整体分为三步：

1. **构建第一个[智能体应用](../concepts/agent-application.md)（约 1 分钟）**：在应用管理页面创建空白[智能体应用](../concepts/agent-application.md)，选择大语言模型（建议千问-Max），编写 System Prompt 定义角色与任务，并配置欢迎语和预设问题。此阶段由于缺少私有知识，回答较为笼统甚至可能无中生有。
2. **构建[知识库](../concepts/knowledge-base.md)（约 3 分钟）**：在数据连接页面创建文件类型连接器并上传知识文档（如 docx），等待 1~6 分钟解析完成；随后在[知识库](../concepts/knowledge-base.md)页面创建标准版知识库，选择默认类目与智能切分策略，等待 1~2 分钟完成解析。智能切分为系统预置策略，经[评测](../concepts/evaluation.md)对多数文档可获得最佳检索效果。
3. **添加知识库并发布应用（约 1 分钟）**：进入应用配置界面，通过「技能 > 知识库」旁的「+」按钮为应用挂载知识库，验证检索增强效果后点击「发布」。

> **注意**：使用大模型会产生[计费](../concepts/billing.md)，百炼提供限时免费额度，可在模型广场查看；知识库服务自 2026 年 1 月 4 日起正式[计费](../concepts/billing.md)，费用由规格费用和模型调用费用两部分组成。

## 支持的模型与功能

百炼应用支持多种模型系列，详见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)：

- **千问系列**：千问-Max 为构建问答应用的推荐模型；[智能体应用](../concepts/agent-application.md)与[工作流](../concepts/workflow.md)应用均支持 QwQ 系列（具备强推理能力，先输出思考过程再输出回答，数学/代码能力达 DeepSeek-R1 满血版水平，但不包括插件、流程、音视频交互能力）；视觉模型支持 qwen-vl-plus-latest、qwen-vl-plus-0125（Qwen2.5-VL 系列，128k 上下文）以及 qwen-vl-max/plus 用于图片解析。
- **DeepSeek 系列**：[智能体应用](../concepts/agent-application.md)与[工作流](../concepts/workflow.md)应用均可集成 DeepSeek 系列模型，结合知识库、长期记忆和 Prompt 模板构建私有知识问答应用。
- **嵌入模型**：知识库支持 text-embedding-v3、v4 模型，v4 在语种支持、代码片段向量化效果和向量维度选择上较 v3 全面升级。

## 应用类型与关键能力

百炼提供多种应用类型以适配不同场景：

- **智能体应用**：2025 年 12 月 26 日上线新版智能体应用（Agent 2.0），将知识库、MCP 统一为工具，由智能体自主规划调用时机与顺序，并完整展示模型思考与工具调用全过程。文件问答支持全文引用、切片检索和自定义处理三种模式。
- **工作流应用**：支持批量节点、[多模态](../concepts/multimodal.md)生成节点（生成图像/视频/音频）、异步运行模式（文本生成模式下后台执行并返回 Task ID）、Dify 工作流一键导入、[多模态](../concepts/multimodal.md)数据节点（文档/图片/视频/音频解析）等。
- **高代码应用**：2025 年 9 月 24 日上线，支持基于 Python 项目结构部署 AI 后端服务，内置自动化运维、可观测性及日志服务等企业级能力。
- **MCP 服务**：2025 年 4 月 9 日新增 MCP 市场与 MCP 管理功能，可开通预置 MCP 服务或部署自定义 MCP 服务；8 月 13 日新增外部调用功能，支持一键配置到第三方应用或通过 MCP SDK 调用。

## 知识库核心能力

知识库是构建私有知识问答应用的关键，能力持续扩展：

- **类型与数据源**：分为文档、数据、图片三类；结构化知识库数据源支持云数据库 RDS、自建 MySQL、DMS；非结构化知识库支持导入 docx、pdf、Excel、离线 HTML，并支持自定义 metadata 与标签分类。
- **音视频知识库**：2025 年 12 月 25 日上线，支持上传音视频文件实现智能检索问答（直播回放问答、课程助教、客服质检）与二次创作（脚本、字幕、剪辑建议）；2026 年 1 月 30 日支持通过 API 创建音视频知识库。
- **检索与调优**：知识库节点支持必定调用、智能调用和旧版调用三种方式；支持权重设置（多知识库按重要性召回）；支持调整初步向量检索 TopK 和关键词检索 TopK 以降低成本；提供在线调试面板实时验证召回效果；支持图文检索与[多模态](../concepts/multimodal.md)回复增强。
- **监控与管理 API**：2026 年 1 月新增 GetIndexMonitor（监控数据）、UpdateIndex（更新配置）等 API，并支持子账号开通知识库与基于标签的分账管理。

## 应用调用与发布

- **API 调用**：2025 年 11 月 3 日起支持通过 Responses API 调用百炼应用，提供同步调用 API（实时交互，可复用 OpenAI 代码库）与[异步调用](../concepts/async-invocation.md) API（设置 `background=true` 立即返回任务 ID）。调用工作流和[智能体编排](../concepts/agent-orchestration.md)应用时需传入自定义参数。
- **发布渠道**：支持微信、钉钉分享渠道（创建钉钉 AI 机器人或微信公众号 AI 机器人）；支持音视频实时互动（将图文对话应用转为音视频实时互动应用，提供 H5/APP 调试窗口，通过音视频 SDK 发布到 WEB/iOS/Android）。
- **应用观测**：2024 年 10 月 24 日新增应用观测能力，支持端到端查看应用处理流程；2026 年 2 月 6 日上线新版应用[评测](../concepts/evaluation.md)，支持智能体、工作流和自定义三种类型[评测](../concepts/evaluation.md)集。
- **长期记忆**：2026 年 1 月 31 日上线新版长期记忆与用户画像管理 API，支持多应用共享同一记忆库、自动提取关键信息、语义检索优化及完整用户画像管理。

## 限制与注意事项

- 知识库自 2026 年 1 月 4 日起正式[计费](../concepts/billing.md)，提供后付费（按量付费）和资源包两种方式，总费用由规格费用与模型调用费用组成，详情参见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中的[计费](../concepts/billing.md)公告。
- 大模型调用产生[计费](../concepts/billing.md)，平台提供限时免费额度，可在模型广场查看各模型系列详情。
- QwQ 系列模型在智能体应用中不支持插件、流程、音视频交互能力。
- 文档解析耗时与文档大小相关，知识文档导入通常 1~6 分钟，知识库解析通常 1~2 分钟，需耐心等待。
- [智能体编排](../concepts/agent-orchestration.md)应用已于 2025 年 8 月 12 日随工作流应用界面升级而下线，相关需求请使用新版智能体应用或工作流应用。
- Assistant API 处于下线中状态，如需全代码开发高度定制化 RAG 应用请关注官方公告。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)












