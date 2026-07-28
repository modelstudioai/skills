# DashScope SDK

DashScope SDK 是阿里云百炼平台的原生官方 SDK，提供 Python 和 Java 两种语言实现，用于调用百炼平台的全部模型能力与应用调用接口。它是百炼功能覆盖最完整的接入方式，当 [OpenAI 兼容接口](openai-compatible-interface.md)无法满足需求时（如特定模型仅支持 DashScope 协议），DashScope SDK 是唯一选择。

## 安装

| 语言 | 安装方式 | 版本要求 |
|------|----------|----------|
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` | 建议 >= 2.12.0 |

> **注意**：Node.js 没有官方 DashScope SDK，Node.js 开发者可通过 [OpenAI 兼容接口](openai-compatible-interface.md)或 HTTP 直接调用。

## 认证配置

SDK 通过 [API Key](api-key.md) 鉴权，推荐将 [API Key](api-key.md) 配置到环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取该变量，避免在代码中硬编码：

```bash
# Linux / macOS
export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"
```

也可在调用时通过 `api_key` 参数显式传入。

## 使用场景

### 调用文本生成模型

DashScope 原生接口提供百炼平台最完整的参数集和功能支持。适合需要使用平台全部能力的场景，如特殊参数配置、平台独有功能等。若仅需标准对话能力且已有 OpenAI 生态代码，可优先考虑 [OpenAI 兼容接口](openai-compatible-interface.md)以降低迁移成本。

### 调用百炼应用（智能体 / 工作流）

通过 `Application.call`（Python）或 `ApplicationParam` + `Application`（Java）调用已发布的智能体应用和工作流应用：

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)

if response.status_code != HTTPStatus.OK:
    print(f'code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

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

对应的 HTTP 端点为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。

### 调用仅支持 DashScope 的专用模型

部分模型只能通过 DashScope SDK 调用，不支持 [OpenAI 兼容接口](openai-compatible-interface.md)：

- `farui-plus`（法律大模型）：支持 Python/Java DashScope SDK。
- `qwen-deep-research`（深度研究）：**仅支持 Python DashScope SDK**，不支持 Java SDK 和 [OpenAI 兼容接口](openai-compatible-interface.md)，且仅限华北2（北京）地域。

其他模型如 `tongyi-intent-detect-v3`、`qwen-mt-plus`、`qwen3.5-ocr` 同时支持 OpenAI 兼容和 DashScope 两种调用方式。

## 关键参数

### 模型调用通用参数

- `model`（string，必选）：模型名称。
- `messages`（array，必选）：对话消息列表。
- `stream`（bool，可选）：是否启用[流式输出](streaming.md)。

### 应用调用参数

- `app_id`（string，必选）：应用 ID，从控制台应用卡片获取。
- `prompt`（string）：用户输入。
- `session_id`（string，可选）：多轮对话时传入上一次响应返回的 session_id 以维护上下文。
- `biz_params`（dict，可选）：自定义参数，透传到应用内部。

### 响应结构

应用调用响应统一为 `{"output": {"finish_reason", "session_id", "text"}, "usage": {...}, "request_id": "..."}` 结构，业务侧主要消费 `output.text`。

## 与 [OpenAI 兼容接口](openai-compatible-interface.md)的选择建议

| 场景 | 推荐方式 |
|------|----------|
| 已有 OpenAI 生态代码，追求最低迁移成本 | OpenAI 兼容接口 |
| 需要平台最完整的参数和功能 | DashScope SDK |
| 调用百炼应用（智能体/工作流） | DashScope SDK 或 Responses API |
| 模型仅支持 DashScope 协议（如 qwen-deep-research） | DashScope SDK（唯一选择） |
| Node.js / Go 项目 | OpenAI 兼容接口或 HTTP 调用 |

## 注意事项

- DashScope 域名（`dashscope.aliyuncs.com`）为存量兼容域名，请求超时 600 秒；生产环境建议迁移至[业务空间](workspace.md)专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），超时 3600 秒且提供 99.9% SLA。
- [API Key](api-key.md) 必须与 Base URL 所属地域匹配，不同地域的 Key 和端点不能混用，否则报 401 错误。
- 跨接口迁移时（DashScope 与 OpenAI 兼容之间），需核对参数映射差异，两者参数集合并不完全一致。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [get started with models](../guides/get-started-with-models.md)
- [preparations](../api/preparations.md)
- [application call](../api/application-call.md)



