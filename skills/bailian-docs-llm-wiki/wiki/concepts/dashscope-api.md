# DashScope 接口

DashScope 接口是阿里云百炼平台的原生 API 体系，提供最完整的功能集和参数支持，是百炼各类模型服务与应用调用的统一入口。所有 DashScope 接口均以 `https://dashscope.aliyuncs.com` 为 Base URL，通过 API Key 进行鉴权。

## 接口定位与选型

百炼平台同时提供 DashScope 原生接口和多种兼容接口（OpenAI Chat Completions、OpenAI Responses、Anthropic Messages）。DashScope 接口的核心优势在于功能覆盖最广、性能最优，适合需要使用平台全部能力的场景。如果项目已有 OpenAI 或 Anthropic 代码，可选择对应的兼容接口以降低迁移成本。

| 接口类型 | 适用场景 |
|---------|---------|
| DashScope 原生 | 需要完整功能集、最优性能，或使用百炼专属能力（如长期记忆、[异步任务](async-task.md)管理） |
| OpenAI 兼容 | 迁移已有 OpenAI 应用，或复用 OpenAI 生态工具链 |
| Anthropic 兼容 | 使用 Anthropic 生态的开发者 |

## 主要使用场景

### 文本生成模型调用

通过 DashScope 接口调用通义千问（Qwen）系列模型，支持多轮对话、[流式输出](streaming.md)、Function Calling 等完整能力。HTTP 端点为模型对应的 DashScope 路径，SDK 层面使用 `dashscope` 包直接调用。

### 应用调用（智能体与工作流）

调用已发布的智能体或工作流应用，HTTP 端点为：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

支持单轮/多轮对话、[流式输出](streaming.md)、自定义插件参数透传、多模态输入等。SDK 调用方式为 `Application.call()`（Python）或 `ApplicationParam.builder()`（Java）。

### 长期记忆管理

长期记忆 API 基于 DashScope 服务，Base URL 为 `https://dashscope.aliyuncs.com/api/v2/apps/memory/`，提供记忆片段的增删改查、语义搜索及用户画像管理共 11 个接口。

### 文本向量化

通用文本向量模型（text-embedding 系列）通过 DashScope 同步接口或异步批处理接口调用，可将文本转换为数值向量用于语义搜索、推荐等下游任务。

### [异步任务](async-task.md)管理

文生图、文生视频等长耗时任务采用异步调用模型，通过 `GET /api/v1/tasks/{task_id}` 等接口查询、取消任务，并支持通过 EventBridge 接收任务完成通知以替代轮询。

## 鉴权与凭证

- **API Key**：唯一鉴权凭证，在百炼控制台的密钥管理页面创建。建议配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码。
- **请求头**：HTTP 调用时在 Header 中携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。
- **临时 API Key**：面向浏览器等不可信环境，通过 `POST /api/v1/tokens` 换取有效期 1-1800 秒的临时凭证（以 `st-` 开头）。

## SDK 与调用方式

| 语言 | DashScope SDK | 安装 |
|------|--------------|------|
| Python（≥3.8） | `dashscope` | `pip install -U dashscope` |
| Java | `com.alibaba:dashscope-sdk-java`（建议 ≥2.12.0） | Maven/Gradle 引入依赖 |
| 其他语言 | 无官方 SDK | 直接使用 HTTP 接口（cURL/PHP/Node.js/Go/C# 等） |

### 快速示例（Python）

```python
import os
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你好"
)
print(response.output.text)
```

## 多地域支持

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

各地域的 API Key 互相独立，调用时需使用对应地域的凭证和 Base URL。

## 关键配置参数

高并发场景下建议配置 SDK 连接池以复用 TCP 连接：

- **Java SDK**：通过 `ConnectionConfigurations.builder()` 设置 `connectionPoolSize`（默认 32）、`connectionIdleTimeout`（默认 300 秒）等参数。
- **Python SDK**：异步调用时传入 `aiohttp.TCPConnector(limit=...)` 控制并发连接数。

[异步任务](async-task.md)管理接口的账号级限流为 20 QPS，查询结果保留 24 小时。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [long term memory new](../api/long-term-memory-new.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [preparations](../api/preparations.md)
- [general text embedding](../api/general-text-embedding.md)


