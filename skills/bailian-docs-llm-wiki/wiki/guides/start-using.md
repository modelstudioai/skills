# start using

阿里云百炼提供了零代码构建 AI 应用的能力，开发者可以通过控制台快速创建智能体应用、配置知识库并发布上线，整个流程约 5 分钟即可完成。本页汇总了快速上手的核心步骤以及平台应用功能的演进历程。

## 快速上手：零代码构建知识问答应用

百炼支持在无需编写代码的情况下，结合私有知识文档构建大模型问答应用。核心流程分三步，详见 [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

### 第一步：创建智能体应用（约 1 分钟）

1. 在 [应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center) 页面点击 **创建应用**，选择 **智能体应用** 并立即创建。
2. 选择大语言模型（推荐 **千问-Max**）。使用模型会产生计费，百炼提供限时免费额度。
3. 配置 System Prompt，定义应用的角色和任务。
4. 设置欢迎语和预设问题，方便用户快速发起对话。
5. 在右侧测试窗口验证应用效果。

> **注意**：未配置知识库时，大模型缺乏领域专有知识，回答可能笼统或产生幻觉。需在第二步引入知识库来增强回答准确性。

### 第二步：构建知识库（约 3 分钟）

1. 在 [数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list) 页面创建文件类型连接器，上传知识文档。
2. 进入 [知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base) 页面，创建标准版知识库。
3. 选择数据类目，使用 **智能切分** 策略（系统预置，适用于多数文档）。
4. 等待解析完成（通常 1-6 分钟）。

### 第三步：关联知识库并发布（约 1 分钟）

1. 回到应用配置页面，在 **技能 > 知识库** 中添加已创建的知识库。
2. 测试验证知识检索增强后的回答效果。
3. 确认无误后点击 **发布**。

## 应用类型与能力

百炼提供多种应用类型，适用于不同场景：

- **智能体应用**：支持 Prompt 定制、知识库关联、插件工具调用、长期记忆和文件问答。2025 年 12 月上线新版 Agent 2.0，将知识库和 MCP 统一为工具，由智能体自主规划调用。
- **工作流应用**：通过可视化画布编排多步骤流程，支持大模型节点、知识库节点、意图分类、批量节点、多模态生成等。支持 Dify 工作流一键导入。
- **高代码应用**：基于 Python 项目结构部署 AI 后端服务，内置运维和可观测性能力（2025 年 9 月上线）。

## 知识库能力演进

知识库是百炼应用的核心能力之一。根据 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)，主要演进节点包括：

| 时间 | 能力 |
|------|------|
| 2024.05 | 统一数据管理 + 知识索引，基于 LlamaIndex 的 Chunk 切分与向量配置 |
| 2024.09 | 图文检索、自定义 metadata、结构化知识库支持 RDS |
| 2024.11 | 非结构化知识库支持 Excel |
| 2025.05 | text-embedding-v3 模型；支持 Qwen VL 解析图片 |
| 2025.07 | text-embedding-v4 模型；数据源支持自建 MySQL |
| 2025.09 | 知识库类型分为文档/数据/图片三类；数据源支持 DMS；新增调试面板 |
| 2025.12 | 音视频知识库上线 |
| 2026.01 | 知识库商业化计费；支持资源包订阅 |

> **注意**：知识库自 2026 年 1 月 4 日起正式开始计费，费用由规格费用和模型调用费用两部分组成。可通过调整初步召回 TopK 参数降低模型调用成本。

## MCP 与外部工具集成

- 2025 年 4 月上线 MCP 市场，支持预置 MCP 服务和自定义 MCP 服务。
- 2025 年 8 月新增外部调用功能，可一键配置到第三方应用或通过 MCP SDK 集成。

## API 调用方式

百炼应用支持多种 API 调用方式：

- **Responses API**（2025 年 11 月）：兼容 OpenAI 接口，支持同步和异步调用。
- **工作流异步模式**（2026 年 1 月）：后台执行，立即返回 Task ID。
- **长期记忆 API 2.0**（2026 年 1 月）：支持多应用共享记忆库，自动提取关键信息和用户画像。

## 应用发布与分享

应用发布后可通过多种渠道分享，包括 Web 端（PC/H5）、钉钉 AI 机器人、微信公众号 AI 机器人。同时支持音视频实时互动，可通过音视频 SDK 发布到 Web/iOS/Android 应用中。

## 后续步骤

- 了解更多应用配置：参考 [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application) 和 [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/) 文档。
- API 集成：参考 [调用智能体应用](https://help.aliyun.com/zh/model-studio/call-single-agent-application/) 和 [调用工作流应用](https://help.aliyun.com/zh/model-studio/invoke-workflow-application/) 文档。
- 应用评测：使用 [新版评测集](https://help.aliyun.com/zh/model-studio/new-version-of-evaluation-set) 构建评测体系（2026 年 2 月上线）。

## 来源文档

- [0代码构建私有知识问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)
- [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)




