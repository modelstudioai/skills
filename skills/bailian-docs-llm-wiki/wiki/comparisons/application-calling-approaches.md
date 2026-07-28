# 应用调用方式对比

百炼平台围绕"应用"提供了多套 API 与接入路径，开发者在技术选型时常面临选择困难：是用 OpenAI 兼容的 Responses API，还是用 DashScope API？是走 SDK 还是裸 HTTP？管理类操作（知识库、数据连接、Prompt 模板）又该用哪套接口？本页从定位、端点、认证、功能覆盖、SDK 支持等维度对三种方式做横向对比，帮助开发者快速决策。

## 对比对象概览

| 对比项 | Responses API（OpenAI 兼容） | DashScope API（应用调用） | 应用组件 OpenAPI（bailian/2023-12-29） |
|--------|------------------------------|--------------------------|---------------------------------------|
| 定位 | 运行时调用智能体/工作流应用 | 运行时调用智能体/工作流应用 | 应用资源管理（数据、知识库、Prompt 模板、记忆等） |
| 协议风格 | OpenAI Responses 兼容 | 百炼自有 REST | 阿里云 ROA 签名风格 |
| 典型用途 | 对话交互、[多模态](../concepts/multimodal.md)输入、异步任务 | 对话交互、多轮会话、自定义参数透传 | 文件上传、知识库构建、Prompt 模板 CRUD、数据连接管理 |
| 是否触发模型推理 | 是 | 是 | 否（管理类操作） |

## 关键维度对比

| 维度 | Responses API | DashScope API | 应用组件 OpenAPI |
|------|--------------|--------------|-----------------|
| Endpoint | `POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` | `POST /api/v1/apps/{APP_ID}/completion` | `https://bailian.<region>.aliyuncs.com` 下多路径 |
| 认证方式 | [API Key](../concepts/api-key.md)（`Authorization: Bearer`） | [API Key](../concepts/api-key.md)（SDK 自动读取 `DASHSCOPE_API_KEY`） | RAM 主账号 / RAM 子账号（需百炼权限 + [业务空间](../concepts/workspace.md)） |
| SDK | OpenAI Python/Java SDK | DashScope Python/Java SDK；同时支持 HTTP（Node.js/PHP/C#/Go/curl） | 阿里云 SDK（多语言 ROA 风格） |
| 多轮对话 | 通过 `input` 数组传完整历史 | `session_id`（云端托管，1 小时有效）或自行管理 `messages` | 不涉及 |
| [流式输出](../concepts/streaming.md) | `stream=true`（工作流需启用开关并重新发布） | 支持 | 不涉及 |
| [异步调用](../concepts/async-invocation.md) | `background=true`（创建→轮询→取结果） | 暂不支持 | 部分 Job 类接口异步执行（如 `SubmitIndexJob`） |
| [多模态](../concepts/multimodal.md)输入 | 支持 `input_image` / `input_file` | 支持（取决于应用配置） | 文件上传走 `ApplyFileUploadLease` → `AddFile` |
| 自定义参数透传 | 不直接支持 | `biz_params.user_defined_params` | 不涉及 |
| 适用地域 | 华北2（北京） | 华北2（北京） | 华北2（北京）、新加坡等 |
| 限流策略 | 按应用/模型维度 | 按应用/模型维度 | 文件类 5–10 次/秒，需退避重试 |

## 各方案适用场景

### Responses API（OpenAI 兼容模式）

**推荐场景：**
- 团队已有 OpenAI SDK 技术栈，希望最低成本迁移到百炼。
- 需要异步执行长耗时任务（生成报告、多步骤工具调用），利用 `background` 模式避免请求超时。
- 需要[多模态](../concepts/multimodal.md)输入（图像、文件），且使用 OpenAI SDK 的 `input_image` / `input_file` 类型。

**局限：**
- 暂不支持 `biz_params` 自定义参数透传。
- 异步任务不支持[流式输出](../concepts/streaming.md)。
- 地域仅华北2（北京）。

### DashScope API（应用调用）

**推荐场景：**
- 需要多语言 SDK 支持（Python/Java 之外还有 Node.js/PHP/C#/Go 的 HTTP 调用）。
- 需要通过 `session_id` 让百炼云端托管多轮对话上下文，简化客户端逻辑。
- 智能体应用使用了自定义插件，需要通过 `biz_params.user_defined_params` 透传业务参数。
- 工作流应用需通过 `messages` 自行管理对话历史，获得更灵活的上下文控制。

**局限：**
- 不支持[异步调用](../concepts/async-invocation.md)模式。
- 多轮对话 `session_id` 有效期 1 小时，最多 50 轮。

### 应用组件 OpenAPI（bailian/2023-12-29）

**推荐场景：**
- 需要通过 API 管理数据连接（文件上传、类目、解析器、连接器）。
- 需要编程式创建和管理知识库（`CreateIndex` → `SubmitIndexJob` → `SubmitIndexAddDocumentsJob`）。
- 需要通过 API 维护 Prompt 模板（`CreatePromptTemplate` / `ListPromptTemplates` 等）。
- 需要管理记忆（Memory）、临时存储与支付流转等应用侧资源。
- RAM 子账号需要操作级权限控制（`AliyunBailianDataFullAccess` / `AliyunBailianDataReadOnlyAccess`）。

**局限：**
- 这是管理类 API，不触发模型推理；运行时调用仍需走 Responses API 或 DashScope API。
- 授权粒度为操作级，不支持资源级授权；细粒度隔离需通过[业务空间](../concepts/workspace.md)实现。
- 文件类接口限流较严（5–10 次/秒），批量操作需注意退避重试。

## 选型决策流程

1. **需要管理应用资源（数据/知识库/Prompt 模板）吗？** → 是 → 使用应用组件 OpenAPI；运行时调用再从下面两选一。
2. **已有 OpenAI SDK 技术栈或需要[异步调用](../concepts/async-invocation.md)吗？** → 是 → 使用 Responses API。
3. **需要 `session_id` 托管多轮对话、多语言 HTTP 调用或自定义参数透传吗？** → 是 → 使用 DashScope API。
4. **两者均可用时** → 优先选择与现有技术栈兼容性更好的一方；若需要异步能力则必须选 Responses API。

## 小结

三种方式并非互斥，而是面向不同层面的互补关系：

- **Responses API 和 DashScope API** 都属于运行时调用层，负责触发应用执行并返回推理结果，开发者按生态兼容性和功能需求二选一即可。
- **应用组件 OpenAPI** 属于管理层，负责应用所依赖的数据、知识库和模板的创建与维护，与运行时调用层配合使用才能完成端到端的应用集成。

实际项目中，典型组合是：先用应用组件 OpenAPI 完成知识库构建和文件上传，再通过 Responses API 或 DashScope API 调用已发布的应用进行对话交互。

## 被对比主题页

- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application component api reference](../api/application-component-api-reference.md)


