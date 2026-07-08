# DashScope SDK

DashScope SDK 是阿里云百炼平台的官方客户端开发工具包，为开发者提供对平台各类大模型和应用服务的编程访问能力。SDK 封装了鉴权、请求构造、响应解析等底层细节，是除 HTTP 直接调用和 [OpenAI 兼容接口](openai-compatible-interface.md)之外的主要接入方式。

## 支持的语言与安装

| 语言 | 安装方式 | 版本要求 |
|------|---------|---------|
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`（建议 >= 2.12.0） | - |

> Node.js 目前没有官方 DashScope SDK，可通过 HTTP 直接调用或使用 OpenAI 兼容 SDK 接入。

## 鉴权配置

DashScope SDK 统一使用 [API Key](api-key.md) 进行鉴权。推荐将 [API Key](api-key.md) 配置到环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取该变量，避免在代码中硬编码：

- **Linux/macOS**：在 `~/.bashrc` 或 `~/.zshrc` 中追加 `export DASHSCOPE_API_KEY="your-key"`，然后 `source` 使其生效。
- **Windows**：通过系统属性设置系统变量，或使用 `setx` / PowerShell 命令设置永久变量。

也可在调用时通过参数显式传入 `api_key`。

## 覆盖的能力场景

DashScope SDK 覆盖百炼平台的大部分模型和应用调用场景：

### 文本生成

通过 DashScope 原生接口调用 Qwen 系列文本生成模型，功能集最完整，支持全部采样参数和业务字段。适合需要使用百炼平台特有能力（如插件、扩展参数）的场景。

### 图像生成与编辑

图像模型（千问-图像、万相系列、Z-Image 等）均可通过 DashScope SDK 调用，涵盖文生图、图像编辑、图像翻译、风格迁移等能力。

### 视频生成

视频生成接口采用[异步调用](async-invocation.md)模式（创建任务 + 轮询获取），DashScope SDK 对任务提交和状态查询提供了封装支持。

### 向量与排序

文本向量（Embedding）和文本排序（Rerank）模型同时支持 [OpenAI 兼容接口](openai-compatible-interface.md)和 DashScope SDK。对于大规模向量化场景，可通过 SDK 使用异步批处理接口。

### 应用调用

通过 `Application.call`（Python）或 `ApplicationParam`（Java）调用百炼控制台中已创建的智能体应用和工作流应用。SDK 封装了请求构造和多轮对话的 `session_id` 管理。

### 专用模型

部分专用模型仅通过 DashScope SDK 可用。例如 `qwen-deep-research`（深度研究模型）当前仅支持 Python DashScope SDK，暂不支持 Java SDK 和 [OpenAI 兼容接口](openai-compatible-interface.md)。

## 调用示例

### Python — 调用应用

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)

if response.status_code == HTTPStatus.OK:
    print(response.output.text)
```

### Java — 调用应用

```java
import com.alibaba.dashscope.app.*;

ApplicationParam param = ApplicationParam.builder()
    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
    .appId("YOUR_APP_ID")
    .prompt("你是谁？")
    .build();

Application application = new Application();
ApplicationResult result = application.call(param);
System.out.printf("text: %s%n", result.getOutput().getText());
```

## 与 OpenAI 兼容接口的对比

| 维度 | DashScope SDK | OpenAI 兼容接口 |
|------|--------------|----------------|
| 功能覆盖 | 最完整，支持百炼原生全部参数 | 为保证协议一致性，可能不暴露部分平台特有参数 |
| 迁移成本 | 需学习百炼原生 API | 可直接复用 OpenAI SDK 和现有代码 |
| 语言支持 | Python、Java | Python、Java、Node.js、Go |
| 内置工具 | 无内置工具，需自行定义 | Responses 接口内置联网搜索、代码解释器等 |

选择建议：如需使用百炼平台的全部能力或仅支持 DashScope SDK 的模型，使用 DashScope SDK；如从 OpenAI 生态迁移或需要 Node.js/Go 支持，使用 OpenAI 兼容接口。

## 注意事项

- 设置环境变量后，已打开的 IDE 或终端不会自动加载新变量，需要重启相关程序。
- 使用 `sudo` 运行脚本时，默认不继承用户环境变量，需加 `-E` 参数。
- 调用不同地域的模型时，需保证 [API Key](api-key.md) 与模型属于同一地域。华北2（北京）和新加坡地域推荐使用[业务空间](workspace.md)专属域名以获得更好性能。

## 关联主题页

- [image generation](../api/image-generation.md)
- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [video generation api](../api/video-generation-api.md)
- [vector and sort](../api/vector-and-sort.md)
- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)


