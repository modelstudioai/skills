# DashScope SDK

DashScope SDK 是阿里云百炼平台的官方原生 SDK，提供 Python 和 Java 两种语言版本，用于调用百炼平台上的大模型和智能体应用。相比 [OpenAI 兼容接口](openai-compatible.md)，DashScope SDK 提供最完整的平台功能集和参数支持。

## 安装方式

| 语言 | 安装命令 | 最低要求 |
|------|---------|---------|
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` | — |

安装完成后，需将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码。

## 鉴权配置

DashScope SDK 默认从环境变量 `DASHSCOPE_API_KEY` 读取密钥，也支持在调用时通过 `api_key` 参数显式传入。API Key 在百炼控制台的 API Key 管理页面创建，其权限由归属的[业务空间](workspace.md)决定：

- 默认[业务空间](workspace.md)的 API Key 可调用所有标准模型
- 子[业务空间](workspace.md)的 API Key 仅可调用已授权的模型

## 主要使用场景

### 模型调用

DashScope SDK 支持调用百炼平台上的各类模型，包括通义千问系列和专用模型。以 Python 为例，通过 `Generation.call` 接口完成文本生成：

```python
from dashscope import Generation

response = Generation.call(
    model="qwen-plus",
    prompt="你的问题"
)
```

部分模型仅支持 DashScope SDK 调用，不支持 [OpenAI 兼容接口](openai-compatible.md)，例如：

- **通义法睿**（`farui-plus`）：法律行业专用模型，通过 `Generation.call` 调用
- **Qwen-Deep-Research**：深度研究模型，当前仅支持 Python DashScope SDK 和 curl
- **调优后的模型**：经过微调并部署的模型仅支持 DashScope 方式调用

### 应用调用

通过 `Application.call` 接口调用百炼平台上的智能体应用和工作流应用：

```python
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你的问题"
)
```

支持通过 `session_id` 或 `messages` 数组管理多轮对话上下文，也支持通过 `biz_params` 传递自定义插件参数。

### [流式输出](streaming.md)

DashScope SDK 支持[流式输出](streaming.md)（streaming），适用于需要实时展示生成内容的场景。在调用时启用流式模式即可逐步接收模型输出。

## 与 [OpenAI 兼容接口](openai-compatible.md)的对比

| 维度 | DashScope SDK | OpenAI 兼容接口 |
|------|--------------|----------------|
| 功能覆盖 | 最完整，支持全部平台能力 | 覆盖主流功能，部分高级参数不支持 |
| 迁移成本 | 需学习 DashScope API | 可复用 OpenAI SDK 代码 |
| 语言支持 | Python、Java | Python、Node.js、Java、Go 等 |
| 适用场景 | 需要完整功能集和最大灵活性 | 从 OpenAI 生态迁移 |

## 多地域支持

DashScope SDK 支持多地域部署，不同地域使用不同的 Base URL：

| 地域 | 说明 |
|------|------|
| 华北2（北京） | 默认地域，功能最全 |
| 新加坡 | Base URL 需包含 WorkspaceId |
| 美国（弗吉尼亚） | 独立的 API Key 体系 |

> **注意**：新加坡地域使用子业务空间调用时，`base_url` 需包含 `{WorkspaceId}` 前缀。部分模型（如 Qwen-Deep-Research）仅支持华北2（北京）地域。

## 关联主题页

- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [more about models](../api/more-about-models.md)
- [preparations](../api/preparations.md)


