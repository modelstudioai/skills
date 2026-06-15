# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 接口体系，提供最完整的功能集和参数支持，是百炼所有模型调用与应用调用的核心通道。相比 [OpenAI 兼容接口](openai-compatible-api.md)和 Anthropic 兼容接口，DashScope 接口覆盖面最广、性能最优。

## 接口定位

百炼平台同时提供多种 API 接口类型，DashScope 接口在其中的定位如下：

| 接口类型 | 定位 |
|---------|------|
| DashScope 原生接口 | 功能最全、参数覆盖最广、性能最优 |
| OpenAI 兼容 Chat Completions | 便于迁移现有 OpenAI 应用 |
| OpenAI 兼容 Responses | 内置工具能力，自动管理对话历史 |
| Anthropic 兼容 Messages | 兼容 Anthropic 生态 |

当需要使用百炼平台的全部能力时，应优先选择 DashScope 接口。

## 使用场景

### 模型 API 调用

DashScope 接口支持调用通义千问（Qwen）系列文本生成模型，端点格式为：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

通过 DashScope Python/Java SDK 可简化调用：

```python
from dashscope import Generation

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    prompt="你好"
)
```

### 应用调用

已发布的智能体和工作流应用通过 DashScope 接口调用，端点格式为：

```
POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion
```

SDK 调用示例：

```python
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
```

DashScope 应用接口支持多轮对话、[流式输出](streaming-output.md)、Plugin、RAG、Function Calling 等完整能力。

### [异步任务](async-task.md)管理

文生图、文生视频等长耗时任务采用异步调用模型，通过 DashScope 接口提交任务并查询结果：

- 查询任务：`GET /api/v1/tasks/{task_id}`
- 批量查询：`GET /api/v1/tasks/`
- 取消任务：`POST /api/v1/tasks/{task_id}/cancel`

### 临时 API Key 派发

通过 `POST https://dashscope.aliyuncs.com/api/v1/tokens` 接口可生成临时 API Key（有效期 1-1800 秒），适用于浏览器、移动端等不可信环境。

## 关键参数与配置

### 鉴权凭证

- **API Key**：通过控制台密钥管理创建，建议配置到环境变量 `DASHSCOPE_API_KEY`。
- **Base URL**：各地域不同，华北2（北京）为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- **Workspace ID**：当应用位于子[业务空间](workspace.md)时必须携带。

### 请求体核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `input.prompt` | string | 用户输入（必选） |
| `input.messages` | array | 多轮对话历史 |
| `input.biz_params` | object | 工作流业务变量或自定义参数透传 |
| `parameters` | object | 模型参数，如 `top_p`、`temperature`、`incremental_output` |
| `debug` | object | 调试信息开关 |

### SDK 版本要求

| SDK | 推荐版本 |
|-----|---------|
| DashScope Python SDK | 最新版（`pip install -U dashscope`） |
| DashScope Java SDK | ≥ 2.12.0 |

### 连接复用（高并发场景）

Java SDK 内置 OkHttp 连接池，关键参数包括 `connectionPoolSize`（默认 32）、`maximumAsyncRequests`（默认 32）等，可根据并发量调整。

## 各地域端点

| 地域 | DashScope 端点 |
|------|---------------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [preparations](../api/preparations.md)


