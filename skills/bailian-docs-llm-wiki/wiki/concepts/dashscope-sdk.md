# DashScope SDK

DashScope SDK 是阿里云百炼平台提供的原生客户端开发工具包，支持 Python 和 Java 两种语言，用于通过 DashScope 原生接口调用百炼平台上的各类模型和应用服务。相比 [OpenAI 兼容接口](openai-compatible-interface.md)和 Anthropic 兼容接口，DashScope SDK 提供最完整的功能集和参数支持，是使用百炼独有高级功能的推荐选择。

## 安装与配置

### API Key 配置

使用 DashScope SDK 前，需在百炼控制台的密钥管理页面获取 API Key，并配置到环境变量中：

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

### Python SDK 安装

```bash
pip install dashscope
```

### Java SDK 安装

建议使用 dashscope SDK 2.12.0 及以上版本。通过 Maven 或 Gradle 引入依赖即可。

## 使用场景

### 文本生成模型调用

DashScope SDK 可直接调用 Qwen 系列文本生成模型，使用 `dashscope.Generation.call()` 方法：

```python
import dashscope

response = dashscope.Generation.call(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你好"}
    ],
    result_format="message",
)
```

DashScope 原生接口是百炼平台功能最全的接口类型。如需使用百炼独有的高级功能或最新特性（如 Deep Research 两阶段调用），推荐使用此接口。

### 应用调用

通过 DashScope SDK 调用已创建的智能体或工作流应用，使用 `Application.call()` 方法：

**Python 示例：**

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你的问题'
)

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

**Java 示例：**

```java
ApplicationParam param = ApplicationParam.builder()
    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
    .appId("YOUR_APP_ID")
    .prompt("你的问题")
    .build();

Application application = new Application();
ApplicationResult result = application.call(param);
System.out.println(result.getOutput().getText());
```

应用调用支持通过 `session_id` 或 `messages` 数组实现多轮对话，其中 `session_id` 由系统自动管理对话历史，`messages` 则由开发者自行维护上下文。

### 向量化与排序模型

DashScope SDK 支持调用文本向量化（Embedding）和文本排序（Rerank）模型。批处理接口适用于大规模文本向量化场景，单次最多处理 10 万行文本，调用时需设置请求头 `X-DashScope-Async: enable`。

### 视频生成

所有视频生成 API 均采用异步调用模式，通过 DashScope 端点访问。基本流程为：

1. 创建任务：`POST` 请求提交生成参数，必须设置 `X-DashScope-Async: enable` 请求头
2. 轮询结果：使用返回的 `task_id` 查询任务状态，直到完成

### 图像生成

DashScope SDK 可调用千问图像、万相、可灵等多系列图像生成模型，支持文生图、图像编辑、涂鸦作画等能力。部分模型采用同步调用，部分采用异步调用。

### 专用领域模型

通过 DashScope SDK 还可调用通义法睿（法律大模型）、意图理解、Deep Research 等专用领域模型。其中 Deep Research 仅支持 Python DashScope SDK，且采用独特的两阶段调用流程。

## DashScope SDK 与其他接口的对比

| 特性 | DashScope SDK | [OpenAI 兼容接口](openai-compatible-interface.md) | Anthropic 兼容接口 |
|------|--------------|----------------|-------------------|
| 功能完整度 | 最全 | 部分参数不支持 | 支持 thinking 和 tool use |
| 适用场景 | 百炼原生功能、最新特性 | 从 OpenAI 迁移 | 从 Anthropic 迁移 |
| 支持语言 | Python、Java | 所有 OpenAI SDK 语言 | 所有 Anthropic SDK 语言 |
| 应用调用端点 | `/api/v1/apps/{APP_ID}/completion` | `/api/v2/.../compatible-mode/v1/responses` | - |

## 关键注意事项

- DashScope SDK 的应用调用接口仅适用于中国大陆版（北京地域）。
- 环境变量 `DASHSCOPE_API_KEY` 是所有调用的认证凭据，建议避免硬编码到代码中。
- 异步调用场景（视频生成、批量向量化等）需设置 `X-DashScope-Async: enable` 请求头。
- 子业务空间下的应用调用还需额外提供 Workspace ID。
- 各接口的计费方式和限流策略相同，均基于百炼平台统一的 Token 计量体系。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [vector and sort](../api/vector-and-sort.md)
- [video generation api](../api/video-generation-api.md)
- [more models](../api/more-models.md)
- [image generation](../api/image-generation.md)


