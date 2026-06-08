# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 接口体系，提供最完整的功能集和参数支持，是百炼所有模型服务和应用调用的底层通信协议。相比 [OpenAI 兼容接口](openai-compatible-api.md)和 Anthropic 兼容接口，DashScope 接口覆盖面最广，适用于需要使用百炼全部能力的场景。

## 接口定位

百炼平台同时提供多种 API 接口风格，DashScope 接口在其中的定位为：

| 维度 | DashScope 接口 | 兼容接口（OpenAI/Anthropic） |
|------|---------------|---------------------------|
| 功能覆盖 | 最完整，支持全部平台能力 | 部分功能可能不支持 |
| 性能 | 最优 | 与 DashScope 一致 |
| 迁移成本 | 需要适配百炼专有协议 | 可直接复用现有代码 |
| 适用场景 | 新项目、需要完整功能集 | 从其他平台迁移的项目 |

## 使用场景

### 文本生成模型调用

通过 DashScope 接口调用通义千问（Qwen）系列模型，端点为：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

支持完整的参数集，包括 `top_p`、`top_k`、`temperature`、[流式输出](streaming-output.md)（`incremental_output`）等。

### 应用调用（智能体与工作流）

调用百炼平台已发布的智能体和工作流应用，端点为：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

支持多轮对话（`messages` 或 `session_id`）、多模态输入（文本/图片/文件/音视频）、Plugin、RAG、Function Calling 以及[异步任务](async-task.md)等能力。

### 框架集成

主流开发框架通过 DashScope SDK 接入百炼服务：

- **Python**：DashScope SDK（`pip install -U dashscope`），通过 `Application.call()` 或模型专属接口调用
- **Java**：DashScope SDK（Maven artifact `com.alibaba:dashscope-sdk-java`，建议 >= 2.12.0），通过 `ApplicationParam.builder()` 构建请求
- **LlamaIndex**：使用 `DashScopeParse`、`DashScopeCloudIndex` 等组件构建 RAG 应用
- **Spring AI Alibaba**：通过 `DashScopeAgent` 和 `DashScopeDocumentRetriever` 集成

## 关键参数与配置

### 鉴权

所有 DashScope 接口请求必须在 Header 中携带 API Key：

```
Authorization: Bearer $DASHSCOPE_API_KEY
```

建议通过环境变量 `DASHSCOPE_API_KEY` 注入，避免硬编码。

### 多地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

不同地域的 API Key 互相独立，不可跨地域使用。

### 请求体结构

DashScope 接口统一采用以下根字段结构：

- `input`：包含 `prompt`（用户输入）、`messages`（对话历史）等
- `parameters`：模型/流程级参数，如 `top_p`、`temperature`、`incremental_output`
- `debug`：调试信息开关

### 连接复用（高并发场景）

- **Java SDK**：内置 OkHttp 连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）、`connectionIdleTimeout`（默认 300 秒）
- **Python SDK**：根据同步/异步调用方式分别配置

## 注意事项

- 当应用位于子[业务空间](workspace.md)时，请求中必须携带 `Workspace ID`
- DashScope 接口与 [OpenAI 兼容接口](openai-compatible-api.md)支持的参数范围可能存在差异，DashScope 覆盖面最广
- 新版智能体应用（Agent 2.0）与旧版智能体/工作流应用的请求字段并不完全一致，需参考对应文档
- [异步任务](async-task.md)（文生图、文生视频等）采用"提交任务获取 task_id → 轮询或回调获取结果"模式，查询结果仅保留 24 小时

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)
- [preparations](../api/preparations.md)


