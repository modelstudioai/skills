# DashScope SDK

DashScope SDK 是阿里云百炼平台的官方原生 SDK，提供对百炼全部模型能力和应用服务的编程访问接口。相比 [OpenAI 兼容接口](openai-compatible-interface.md)，DashScope SDK 的功能集最完整、参数支持最丰富，是需要使用百炼平台全部能力时的首选接入方式。

## 支持的语言与安装

| 语言 | 安装方式 | 版本要求 |
| --- | --- | --- |
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`（建议 >= 2.12.0） | - |

Node.js 目前没有官方 DashScope SDK，需通过 `axios` 等 HTTP 库直接调用 REST API，或使用 OpenAI 兼容 SDK 接入。

## 鉴权与环境配置

DashScope SDK 使用 API Key 进行鉴权。推荐将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取该变量，避免在代码中硬编码：

- **Linux/macOS**：在 `~/.bashrc` 或 `~/.zshrc` 中添加 `export DASHSCOPE_API_KEY="your-key"`，然后 `source` 生效。
- **Windows**：通过系统属性设置系统变量，或使用 `setx` / PowerShell 命令。

也可在调用时通过 `api_key` 参数显式传入。注意不同地域（北京、新加坡等）的 API Key 不通用，切换地域时需同步更换。

## 使用场景

### 应用调用

通过 `Application.call` 方法调用百炼上创建的智能体应用和工作流应用。Python 示例：

```python
from dashscope import Application

response = Application.call(
    app_id='YOUR_APP_ID',
    prompt='你好'
)
print(response.output.text)
```

Java 通过 `ApplicationParam.builder()` 构建参数，调用 `Application.call(param)` 完成请求。两种应用类型的调用接口完全一致，支持多轮对话（通过 `session_id` 或手动拼接历史消息）。

### 文本生成（Qwen 系列）

DashScope 原生接口是百炼为 Qwen 系列模型提供的四种调用方式之一（另有 OpenAI 兼容、Anthropic 兼容、OpenAI Responses）。当需要使用最全的采样参数、插件或业务字段时，建议优先选择 DashScope 原生接口。

### 专用模型

多个专用模型支持通过 DashScope SDK 调用：

- **farui-plus**：法律行业大模型，支持法律咨询、文书生成、案情分析。
- **tongyi-intent-detect-v3**：意图理解模型。
- **qwen-deep-research**：深度研究模型（仅支持 Python DashScope SDK，不支持 Java SDK 和 [OpenAI 兼容接口](openai-compatible-interface.md)，且仅限华北2北京地域）。
- **qwen-mt-plus**：翻译模型，支持术语干预和翻译记忆。
- **qwen3.5-ocr**：图像文字提取与结构化抽取。

### 文本向量与排序

DashScope SDK 支持调用文本向量模型（如 text-embedding-v4）将文本转换为数值向量，也支持通过排序模型（如 qwen3-rerank）对候选文档进行相关性排序，广泛应用于语义搜索和 RAG 场景。

## 与 [OpenAI 兼容接口](openai-compatible-interface.md)的对比

| 维度 | DashScope SDK | OpenAI 兼容接口 |
| --- | --- | --- |
| 功能完整度 | 最全，支持百炼全部参数和插件 | 保证协议一致性，可能不暴露全部百炼参数 |
| 迁移成本 | 需学习百炼原生 API | 可直接复用现有 OpenAI 代码和生态工具 |
| 语言支持 | Python、Java | Python、Java、Node.js、Go |
| 内置工具 | 按各接口自行定义 | Responses 接口内置联网搜索、代码解释器等 |

如果项目已有 OpenAI SDK 集成且无需百炼专属参数，使用 OpenAI 兼容接口迁移成本更低；如果需要使用百炼平台的全部能力或调用仅 DashScope 支持的模型，建议使用 DashScope SDK。

## 常见问题

- **环境变量不生效**：设置环境变量后需重启 IDE 或终端；使用 `sudo` 运行脚本时需加 `-E` 参数以继承用户环境变量。
- **模型不可用**：确认模型名称拼写正确，注意大小写，不要混用开源社区名与百炼模型 ID。
- **地域限制**：部分模型（如 qwen-deep-research）仅在特定地域可用，需使用对应地域的 API Key。

## 关联主题页

- [bailian application calling](../guides/bailian-application-calling.md)
- [more models](../api/more-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [preparations](../api/preparations.md)
- [vector and sort](../api/vector-and-sort.md)


