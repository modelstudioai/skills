# DashScope SDK

DashScope SDK 是阿里云百炼平台提供的官方客户端开发工具包，开发者通过它可以在 Python 和 Java 应用中直接调用百炼平台上的模型服务和应用能力，无需手动拼装 HTTP 请求。

## 支持语言与安装

| 语言 | 安装方式 | 最低建议版本 |
|------|---------|-------------|
| Python | `pip install -U dashscope` | 最新版 |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java` | >= 2.12.0 |

Node.js 场景目前无官方 SDK 封装，推荐使用 `axios` 直接调用 HTTP API 或通过 [OpenAI 兼容接口](openai-compatible-interface.md)接入。

## 认证配置

SDK 统一通过 API Key 进行身份认证，推荐将密钥写入环境变量：

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

SDK 会自动读取 `DASHSCOPE_API_KEY` 环境变量，无需在代码中硬编码。也可在调用时通过 `api_key` 参数显式传入。

## 使用场景

### 模型调用

DashScope SDK 可调用百炼平台上的各类模型，包括：

- **文本生成**：Qwen 系列对话模型，通过 DashScope 原生接口获得最完整的参数支持
- **图像生成与编辑**：千问图像、万相系列等模型的文生图、图像编辑、图像翻译能力
- **专用模型**：法律大模型（farui-plus）、意图理解（tongyi-intent-detect-v3）、深度研究（qwen-deep-research）、翻译（qwen-mt-plus）、OCR（qwen3.5-ocr）等

> 注意：部分模型仅支持通过 DashScope SDK 调用（如 `qwen-deep-research` 当前仅支持 Python SDK），使用前需确认模型的接口兼容性。

### 应用调用

通过 `Application.call` 方法可调用百炼平台上已创建的智能体应用和工作流应用：

```python
from dashscope import Application

response = Application.call(
    app_id='YOUR_APP_ID',
    prompt='你的问题'
)
print(response.output.text)
```

Java 中使用 `ApplicationParam.builder()` 构建参数后调用。智能体应用与工作流应用的调用接口完全一致。

### 多轮对话

应用调用支持多轮对话，通过 `session_id` 参数让平台自动管理对话历史，无需手动维护上下文。

## 与其他接口的关系

百炼平台提供多种调用方式，DashScope SDK 属于百炼原生接口：

| 接口 | 适用场景 |
|------|---------|
| DashScope SDK/API | 功能最完整，参数支持最丰富，百炼专属能力首选 |
| [OpenAI 兼容接口](openai-compatible-interface.md) | 从 OpenAI 迁移成本最低，兼容现有工具链 |
| HTTP API | 语言无关，适合无官方 SDK 的运行环境 |

当需要使用百炼平台全部参数和插件能力时，建议优先选择 DashScope SDK。

## 关键注意事项

- 不同模型可能仅在特定地域可用，调用前需确认地域限制
- Java SDK 建议使用 2.12.0 及以上版本以获得完整功能支持
- [流式输出](streaming.md)通过 `stream=True`（Python）或对应参数开启
- SDK 调用与 HTTP API 的请求/响应结构一致，可按需切换

## 关联主题页

- [image generation](../api/image-generation.md)
- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [qwen api reference](../api/qwen-api-reference.md)


