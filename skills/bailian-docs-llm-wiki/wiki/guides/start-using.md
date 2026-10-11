# start using

阿里云百炼平台提供零代码与低代码两种路径，帮助开发者快速构建具备私有知识问答、多模态理解、工作流编排等能力的智能体应用。本文档聚焦“开始使用”阶段的核心操作路径，涵盖模型与功能选型、关键参数配置、典型使用方式及当前限制，适用于首次接入的开发者快速上手。

## 支持的模型/功能

- **基础模型支持**：智能体应用（Agent 1.0）和工作流应用均支持 `qwen-max`、`qwq-plus`、`qwq-32b`、`deepseek-v3` 等主流大模型；其中 `qwq` 系列模型具备强推理能力，支持思维链输出，但[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)暂不支持其插件与音视频交互能力。  
- **多模态能力**：`qwen-vl-plus-latest` 和 `qwen-vl-plus-2025-01-25` 已集成至智能体应用，支持图像/视频内容解析；知识库亦支持上传音视频文件并构建音视频知识库，详见[创建和使用知识库](../../raw/application-user-guide/knowledge-base/rag-knowledge-base.md)。  
- **知识库类型**：支持三类知识库——**文档型**（PDF/DOCX/HTML/Excel等）、**数据型**（RDS/DMS/自建MySQL同步）、**图片型**（含图文检索与Qwen-VL解析），创建时可按场景直接选择类型，流程已大幅简化 [9月23日更新](../../raw/application-user-guide/start-using/application-release-notes.md)。  
- **高级功能模块**：长期记忆（2.0版API）、MCP服务市场、Prompt样例库、调试面板、权重设置（多知识库优先级控制）均已上线，覆盖个性化记忆管理、外部工具集成与检索优化等关键需求。

> **注意**：文档 1 中提及的“千问-Max”为推荐默认模型，但根据[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)（2026年2月起），`qwen-max` 已明确列为标准支持型号；而文档 1 中未体现 `qwq`、`deepseek` 及多模态 VL 模型支持，属信息滞后，应以功能动态为准。

## 关键参数

- **知识库检索参数**：可通过“检索配置”调整 `初步向量检索TopK` 与 `初步关键词检索TopK`，降低送入排序模型的 Token 量，从而显著优化成本（见[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 2026年1月6日条目）。  
- **模型调用参数**：智能体应用中 System Prompt 定义角色与任务边界；欢迎语与预设问题影响用户首屏体验；“多模态回复增强”开关需手动开启以启用图表/图像内容解析能力（2026年3月24日新增）。  
- **知识库权重**：当一个智能体关联多个知识库时，可为每个知识库单独设置权重值，系统将优先召回高权重知识库中的片段（2026年4月10日上线）。  
- **长期记忆配置**：新版长期记忆 API 支持自动信息提取、语义检索与用户画像管理，相比旧版在延迟、召回率与自动化程度上有显著提升，详见[长期记忆&用户画像管理 API](../../raw/application-user-guide/memory-library-overview/long-term-memory-2-0.md)。

## 使用方式

1. **零代码快速启动**：访问[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，点击**创建应用 → 智能体应用 → 立即创建**，完成应用命名、模型选择、System Prompt 设置、欢迎语与预设问题配置后即可测试（约1分钟）——该流程详见[0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
2. **知识库集成**：无需预先上传至“数据连接”，可直接在知识库创建流程中导入文件（如 DOCX/HTML/Excel/音视频）或配置数据库源（RDS/DMS/MySQL）；支持“智能切分”策略与在线调试面板实时验证召回效果。  
3. **API 调用**：支持 OpenAI 兼容的 Responses API（同步/异步模式），可复用现有 OpenAI SDK；工作流应用还支持异步运行模式，返回 Task ID 后通过[任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center)查询结果。  
4. **发布与分享**：应用配置完成后点击**发布**，即可生成可分享链接；支持导出为钉钉/微信 AI 机器人，或通过 H5/APP SDK 集成至自有客户端。

## 限制和注意事项

- **知识库商业化计费**：自 2026 年 1 月 4 日起，知识库服务正式计费，费用由规格费 + 模型调用费构成；免费额度仅限部分模型试用，详情参见[知识库计费说明](../../raw/application-user-guide/knowledge-base/reference/billing-for-knowledge-base.md)。  
- **模型兼容性限制**：`qwq` 系列模型虽已在智能体与工作流中支持，但其插件调用、音视频实时互动等高级能力尚未开放给 Agent 1.0，仅适用于纯文本推理场景。  
- **文件处理限制**：非结构化知识库支持 Excel 导入，但若 Excel 包含复杂公式或宏，可能无法完整解析；音视频知识库对单文件时长与分辨率存在后台处理阈值，超限文件需预处理分段。  
- **调试与观测依赖权限**：应用观测功能需授权 `AliyunServiceRoleForSFMTelemetry` 服务关联角色；OSS 自动同步依赖 `AliyunServiceRoleForSFMAccessingMNS`，缺失角色将导致变更无法触发知识库更新。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)


