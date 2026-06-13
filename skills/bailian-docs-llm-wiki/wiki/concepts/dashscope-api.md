# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 接口体系，提供最完整的功能集和参数支持，是百炼所有模型调用与应用调用的底层通道。开发者通过 DashScope 端点可以调用通义千问系列模型、触发智能体和工作流应用，并管理[异步任务](async-task.md)等平台能力。

## 接口定位

百炼平台同时提供 OpenAI 兼容、Anthropic 兼容和 DashScope 原生三类接口。其中 DashScope 接口的覆盖面最广：

- **模型调用**：支持全部文本生成参数（`top_p`、`top_k`、`temperature`、增量[流式输出](streaming.md)等），以及多模态输入（文本、图片、文件、音视频）。
- **应用调用**：支持智能体（含 Agent 2.0）和工作流应用的完整功能，包括多轮对话、Plugin、RAG、Function Calling 等。
- **[异步任务](async-task.md)管理**：文生图、文生视频等长耗时任务的提交、查询、取消，以及 EventBridge 事件通知。

当项目需要使用百炼平台的全部能力时，应优先选择 DashScope 接口。

## 核心端点

| 场景 | HTTP 端点 | 说明 |
|------|-----------|------|
| 模型调用（文本生成） | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | 直接调用通义千问等模型 |
| 应用调用 | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | 调用已发布的智能体或工作流应用 |
| [异步任务](async-task.md)查询 | `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` | 查询长耗时任务状态与结果 |
| 临时 API Key | `POST https://dashscope.aliyuncs.com/api/v1/tokens` | 为前端等不可信环境生成短期凭证 |

## 鉴权方式

所有 DashScope 请求均需在 HTTP Header 中携带 API Key：

```
Authorization: Bearer $DASHSCOPE_API_KEY
```

API Key 在百炼控制台的密钥管理页面创建，建议通过 `DASHSCOPE_API_KEY` 环境变量注入，避免硬编码。对于前端场景，可通过临时 API Key 接口换取有效期 1-1800 秒的短期凭证（以 `st-` 开头）。

## SDK 支持

DashScope 提供多语言 SDK，覆盖主流开发场景：

| 语言 | SDK / 方式 | 推荐版本 |
|------|-----------|---------|
| Python | `dashscope` 包（`Application.call` / `Generation.call`） | 最新版（自定义参数透传需 >= 1.14.0） |
| Java | `com.alibaba:dashscope-sdk-java`（`ApplicationParam.builder`） | >= 2.12.0 |
| 其他语言 | HTTP 直接调用（PHP、Node.js、Go、C# 等） | -- |

## 关键参数

### 模型调用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型名称，如 `qwen-max`、`qwen-plus` |
| `input.prompt` 或 `input.messages` | string / array | 用户输入或多轮对话历史 |
| `parameters.top_p` | float | 核采样概率 |
| `parameters.top_k` | int | 采样候选数 |
| `parameters.temperature` | float | 生成随机性控制 |
| `parameters.incremental_output` | bool | 流式场景下是否增量输出 |

### 应用调用参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `app_id` | string | 目标应用 ID |
| `input.prompt` | string | 用户当前轮输入 |
| `input.messages` | array | 自行管理的多轮对话历史（优先级高于 `session_id`） |
| `session_id` | string | 云端托管会话 ID（有效期 1 小时，最多 50 轮） |
| `input.biz_params` | object | 自定义插件/节点的业务透传参数 |

## 框架集成

主流框架通过 DashScope 接口与百炼平台对接：

- **LlamaIndex**（Python）：通过 `DashScopeParse`、`DashScopeCloudIndex` 等组件构建云端 RAG 应用，底层调用 DashScope 端点。
- **Spring AI Alibaba**（Java）：通过 `DashScopeDocumentRetriever` 和 `DashScopeAgent` 实现知识库检索与应用调用，配置中使用 `DASHSCOPE_API_KEY` 或 `AI_DASHSCOPE_API_KEY` 鉴权。

## 连接复用

高并发场景下，DashScope SDK 支持连接池复用以降低延迟：

- **Java SDK**：内置 OkHttp 连接池，可配置 `connectionPoolSize`（默认 32）、`connectionIdleTimeout`（默认 300 秒）等参数。
- **Python SDK**：支持 `httpx` 连接复用，适当调整超时与并发参数。

## 与兼容接口的对比

| 维度 | DashScope 原生 | OpenAI 兼容 | Anthropic 兼容 |
|------|---------------|-------------|---------------|
| 功能覆盖 | 最完整 | 部分参数不支持 | 部分参数不支持 |
| 迁移成本 | 需使用 DashScope SDK 或自行构造请求 | 可直接复用 OpenAI 客户端库 | 可复用 Anthropic SDK |
| 适用场景 | 需要全部平台能力 | 迁移 OpenAI 项目 | 迁移 Anthropic 项目 |

当不确定选择哪种接口时，DashScope 原生接口是最稳妥的选择——它覆盖所有功能，且通常能获得最优性能。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [frameworks](../api/frameworks.md)


