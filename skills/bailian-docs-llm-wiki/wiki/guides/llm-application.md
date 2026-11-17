# llm application

`llm application` 是百炼平台提供的低代码/无代码 LLM 应用构建能力，支持通过可视化编排或配置方式快速创建智能体（Agent）、工作流（Workflow）和文件问答等应用形态，无需编写模型推理逻辑即可完成端到端部署与调用。其核心抽象为“应用即服务”，开发者可聚焦于业务逻辑编排与 [Prompt 工程](../concepts/prompt-engineering.md)，而非底层模型适配。该能力统一承载于 [Flow Agent](../../raw/application-user-guide/llm-application.md) 文档体系下。

## 支持的模型与功能

- **模型支持**：底层自动适配百炼托管的主流开源及自研大模型（如 Qwen 系列、Baichuan 等），不支持用户自定义模型权重上传；模型选择在应用创建时通过 `model_id` 参数指定，详见 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)。
- **核心功能类型**：
  - 单智能体（Single Agent）：基于系统 Prompt + 工具调用（插件）的对话式应用；
  - 工作流应用（Workflow Application）：多节点串联（LLM 节点、条件分支、工具调用、变量赋值等）的确定性流程；
  - 文件问答（File Q&A）：支持上传 PDF/DOCX/TXT 等格式，自动切片向量化后提供[检索增强生成](../concepts/rag.md)（RAG）；
  - 任务中心（Task Center）：批量异步执行结构化任务（如批量摘要、分类），支持结果回调。

> **注意**：[工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md) 中描述的“HTTP 请求节点”在 v3.2+ 版本已移除，改由插件机制统一实现，避免直接暴露内网地址风险。

## 关键参数

调用或配置应用时需关注以下关键参数（以 API 调用和控制台配置共通项为准）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，创建后生成，见 [应用发布与分享](../../raw/application-user-guide/llm-application/application-publishing-and-sharing.md) |
| `model_id` | string | 否 | 指定底层模型（如 `qwen-max`, `qwen-plus`），未填则使用应用默认模型 |
| `inputs` | object | 是 | 用户输入变量，键名需与应用中定义的 Input Schema 严格一致 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅对单次请求生效，不影响工作流节点内部流式行为 |

## 使用方式

1. **创建应用**：在控制台「应用开发」→「新建应用」中选择模板（智能体 / 工作流 / 文件问答），按向导完成 Prompt 编辑、工具绑定、输入输出 Schema 定义；
2. **调试与测试**：使用内置调试器提交样例 `inputs`，实时查看各节点执行日志与中间结果；
3. **调用应用**：
   - 控制台：点击「应用调用」获取 SDK 示例与 cURL 命令；
   - API：POST `/v1/applications/{app_id}/chat`（智能体/工作流）或 `/v1/applications/{app_id}/file_qa`（文件问答），鉴权使用 `Authorization: Bearer <api_key>`；
   - 更多细节参见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。

## 限制和注意事项

- 单次请求最大 `inputs` JSON 大小为 2MB；工作流总节点数上限为 50，单工作流执行超时为 300 秒；
- 文件问答仅支持 UTF-8 编码文本，PDF 需含可提取文本层（扫描版需先 OCR）；
- 所有应用默认开启审计日志，但**不自动持久化用户输入/输出内容**，如需合规存储，须自行集成日志服务；
- 插件调用需显式授权，且插件权限粒度独立于应用权限，详见 [权限管理](../../raw/application-user-guide/application-permission-management.md)。

## 来源文档

- [Flow Agent](../../raw/application-user-guide/llm-application.md)


