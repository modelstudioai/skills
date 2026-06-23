# DashScope SDK

DashScope SDK 是阿里云百炼平台的官方多语言客户端库，用于调用通义千问系列模型、专用模型以及百炼应用。相比 [OpenAI 兼容接口](openai-compatible.md)，它覆盖最完整的平台原生能力，是使用百炼特有参数和高级功能时的推荐接入方式。

## 适用场景

- 需要使用 DashScope 原生接口的全部参数和高级能力（如平台特有的输出格式控制、深度研究两阶段调用等）
- 调用百炼智能体应用或工作流应用，结合 `biz_params` 进行自定义插件参数透传
- 调用仅支持 DashScope SDK 的专用模型，例如 `farui-plus`（通义法睿）、`qwen-deep-research`（深度研究，仅 Python SDK + curl）
- 已使用 Python 或 Java 技术栈，希望以最小集成成本接入百炼

## 支持语言与版本

| 语言 | 安装命令 | 版本要求 |
|------|----------|----------|
| Python | `pip install -U dashscope` | Python ≥ 3.8 |
| Java | 引入 `com.alibaba:dashscope-sdk-java`（Maven/Gradle） | Java ≥ 8，建议 2.12.0 及以上 |

Node.js、Go、C# 等语言可通过 HTTP 直接调用 DashScope API，无需安装 SDK。

## 基础调用

调用前需将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码。

### 文本生成

通过 `Generation.call` 调用通义千问或专用模型，将 `model` 参数设为目标模型名称即可：

```python
import os
from dashscope import Generation

response = Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-max",
    prompt="你的问题")
```

调用 `farui-plus`（通义法睿法律模型）时，仅需将 `model` 改为 `"farui-plus"`，支持单轮、多轮和[流式输出](streaming-output.md)。

### 应用调用

通过 `Application.call` 调用百炼智能体应用或工作流应用，端点为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`：

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你的问题')

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

## 关键参数与配置

### 应用调用上下文管理

| 方式 | 说明 | 特点 |
|------|------|------|
| `session_id` | 传入首次调用返回的 session_id，云端加载历史 | 有效期 1 小时，最多 50 轮，实现简单 |
| `messages` 数组 | 自行维护对话历史并传入 | 完全控制上下文，更灵活（推荐） |

若请求同时包含 `session_id` 和 `messages`，系统优先使用 `messages`。工作流应用使用 `messages` 前，需在大模型节点配置提示词变量 `historyList` 并重新发布。

### 自定义插件参数

智能体应用关联自定义插件后，通过 `biz_params.user_defined_params` 传递插件 ID 和参数。创建插件时输入参数的传参方式须选择「业务透传」：

```python
biz_params = {
    "user_defined_params": {
        "your_plugin_code": {
            "article_index": 2
        }
    }
}

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='查询内容',
    biz_params=biz_params)
```

### 深度研究模型特殊流程

`qwen-deep-research` 仅支持华北2（北京）地域的 API Key，当前仅 Python DashScope SDK 和 curl 可用，暂不支持 Java SDK 与 [OpenAI 兼容接口](openai-compatible.md)。调用分两阶段：反问确认阶段返回澄清问题，深入研究阶段将反问内容与用户回答拼入 messages 后生成研究报告。可通过 `output_format` 选择详细报告（约 6000 Token）或摘要报告（约 1500-2000 Token）。

## 鉴权与权限

所有调用使用百炼 API Key 鉴权。HTTP 调用需在 Header 中传入 `Authorization: Bearer $DASHSCOPE_API_KEY`。API Key 的调用权限由归属[业务空间](workspace.md)决定：默认[业务空间](workspace.md)下的 Key 可调用所有标准模型及该空间内的应用；子[业务空间](workspace.md)下的 Key 仅可调用该子空间已授权的模型与应用。

## 接口选择对比

| 场景 | 推荐接口 |
|------|----------|
| 从 OpenAI 迁移现有应用 | OpenAI 兼容 Chat Completions |
| 需要内置工具（搜索、代码执行等） | OpenAI 兼容 Responses |
| 从 Anthropic 生态迁移 | Anthropic 兼容 Messages |
| 需要完整功能集和最大灵活性 | DashScope 原生接口（SDK） |

第三方兼容接口便于迁移，DashScope SDK 覆盖最全的平台能力。选择时需权衡兼容性与功能完整度。

## 错误处理

调用失败时响应中包含 `status_code` 和 `message` 字段，可参考百炼错误码文档定位问题。常见原因包括 API Key 未配置、使用了 `sudo` 未加 `-E` 导致环境变量丢失、或服务管理器（systemd/supervisord）未显式注入环境变量。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more models](../api/more-models.md)
- [preparations](../api/preparations.md)
- [frameworks](../api/frameworks.md)


