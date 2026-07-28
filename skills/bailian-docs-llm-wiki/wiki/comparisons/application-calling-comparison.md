# 应用调用方式对比

本页对比阿里云百炼平台调用智能体应用和工作流应用的两种 API 方式——**OpenAI 兼容的 Responses API** 与 **DashScope API**，帮助开发者根据生态兼容性、异步能力、多模态支持等需求做出技术选型。两种方式均可调用智能体应用和工作流应用，核心凭证一致（APP ID + API Key），但在端点、SDK、多轮对话机制、异步调用等维度存在差异。

## 前提条件

无论选择哪种方式，均需完成以下准备：

- 获取 **API Key**，配置到环境变量 `DASHSCOPE_API_KEY`。
- 获取 **APP ID**（从控制台「应用管理」页面复制）。若应用位于子业务空间，还需提供 **Workspace ID**。
- 已创建并发布百炼应用（智能体或工作流应用）。
- 安装对应 SDK：Responses API 用 OpenAI SDK，DashScope API 用 DashScope SDK（或直接 HTTP 调用）。

> 目前 APP ID 和 Workspace ID 只能通过控制台手动获取，不支持 API 或 CLI 查询。

## 关键维度对比

| 维度 | Responses API（OpenAI 兼容） | DashScope API |
|------|------------------------------|---------------|
| API 端点 | `POST .../api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST .../api/v1/apps/{APP_ID}/completion` |
| SDK | OpenAI Python / Java SDK | DashScope Python / Java SDK |
| HTTP 调用语言 | 任意支持 HTTP 的语言 | Python、Java、PHP、Node.js、C#、Go 等 |
| 多轮对话 | 通过 `input` 数组传递完整消息历史（role + content） | `session_id`（系统托管，有效期 1 小时，最多 50 轮）或自行维护 `messages` 数组 |
| 异步调用 | 支持，设置 `background=true`，返回任务 ID 后轮询 | 暂不支持 |
| 流式输出 | 支持，设置 `stream=true` | 支持（工作流应用需在结束节点启用流式开关并重新发布） |
| 多模态输入 | 支持图像（`input_image`）和文件（`input_file`） | 通过应用编排配置 |
| 自定义参数透传 | 未提供 | 支持，通过 `biz_params.user_defined_params` 传递业务参数 |
| 可用地域 | 仅华北2（北京） | 仅华北2（北京） |
| 响应结构 | OpenAI 标准响应格式 | `{"output": {"text", "session_id", "finish_reason"}, "usage": {...}, "request_id": "..."}` |
| 典型场景 | OpenAI 生态兼容、异步长任务、多模态交互 | 深度集成百炼能力、多语言调用、自定义参数透传 |

## Responses API 适用场景

Responses API 提供 OpenAI 兼容接口，适合以下场景：

- **OpenAI 生态复用**：已有基于 OpenAI SDK 的代码或服务，可平滑迁移到百炼，仅需替换 `base_url` 和 `api_key`。
- **异步长任务**：如生成报告、多步骤工具调用等耗时任务，通过 `background=true` 异步执行，避免请求超时。流程为创建任务 → 轮询状态 → 获取结果。
- **多模态输入**：需同时传入图像或文件的场景，通过 `input_image` / `input_file` 类型在 `content` 数组中混合多种输入。

> 异步任务暂不支持流式输出（`stream=true`）。

## DashScope API 适用场景

DashScope API 提供更全面的功能支持，适合以下场景：

- **多语言集成**：除 Python/Java SDK 外，还支持 PHP、Node.js、C#、Go 等语言的 HTTP 直接调用，适合异构技术栈。
- **自定义参数透传**：通过 `biz_params.user_defined_params` 向自定义插件或自定义节点传递业务参数，实现动态配置。
- **Session 托管**：通过 `session_id` 让系统自动加载历史对话，减少客户端维护成本（有效期 1 小时，最多 50 轮）。如需更灵活的控制，也可自行管理 `messages` 数组。
- **工作流应用深度集成**：工作流应用支持在调用时传递自定义参数、配置提示词变量 `historyList` 等能力。

## 选型建议

| 需求 | 推荐方案 |
|------|----------|
| 已有 OpenAI SDK 代码，希望快速接入 | Responses API |
| 需要异步执行长耗时任务 | Responses API（`background=true`） |
| 需要多模态（图像/文件）输入 | Responses API |
| 需要多语言 HTTP 调用（非 Python/Java） | DashScope API |
| 需要向自定义插件/节点透传业务参数 | DashScope API |
| 希望由系统托管对话上下文 | DashScope API（`session_id`） |
| 需要完全控制对话历史 | 两者皆可（Responses 用 `input` 数组，DashScope 用 `messages` 数组） |

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)


