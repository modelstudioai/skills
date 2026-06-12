# DashScope 接口

DashScope 是阿里云百炼平台的原生 API 接口体系，提供最完整的功能集和参数支持，是百炼所有模型与应用服务的统一调用入口。其服务端点统一托管在 `dashscope.aliyuncs.com`，覆盖文本生成、语音合成、语音识别、应用调用等全部能力。

## 在百炼平台中的定位

百炼平台同时提供多种 API 接口风格（OpenAI 兼容、Anthropic 兼容、DashScope 原生），其中 DashScope 接口具备以下独特优势：

- **功能覆盖最广**：支持百炼平台全部能力，包括文本生成、多模态输入、语音合成与识别、应用调用、深度研究等，其他兼容接口可能仅覆盖部分功能。
- **参数支持最全**：提供最完整的请求参数集，如 `top_p`、`top_k`、`temperature`、`incremental_output`（流式增量输出）等控制参数在 DashScope 接口中均可使用。
- **性能最优**：作为平台原生接口，在延迟和吞吐方面表现最佳。

## 核心服务端点

DashScope 接口根据服务类型使用不同的端点和协议：

| 服务类型 | 协议 | 端点 |
|---------|------|------|
| 文本生成（Qwen 系列） | HTTPS | `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` |
| 应用调用（智能体/工作流） | HTTPS | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` |
| 语音合成（实时） | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |
| 语音合成（非实时） | HTTPS | `POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer` |
| 语音识别（实时） | WebSocket | `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |
| 录音文件识别 | HTTPS | `POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription` |
| 兼容模式入口 | HTTPS | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

多地域部署时，新加坡使用 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，美国使用 `dashscope-us.aliyuncs.com`，德国使用 `{WorkspaceId}.eu-central-1.maas.aliyuncs.com`。

## 鉴权方式

所有 DashScope 接口采用 API Key 鉴权，通过请求头 `Authorization: Bearer <your_api_key>` 传递。建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。

公共请求头：

| 参数 | 说明 |
|------|------|
| `Authorization` | `Bearer <API_KEY>`，必填 |
| `Content-Type` | `application/json`（HTTPS 请求） |
| `X-DashScope-WorkSpace` | [业务空间](workspace.md) ID，子[业务空间](workspace.md)或特定地域时必填 |
| `X-DashScope-Async` | 设为 `enable` 以提交[异步任务](async-task.md)（录音文件识别等） |
| `X-DashScope-DataInspection` | 数据合规检测开关 |

## 典型使用场景

### 文本生成

通过 DashScope SDK 调用 Qwen 系列模型，请求体使用 `input` / `parameters` 结构：

```python
import dashscope

response = dashscope.Generation.call(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    result_format="message",
    stream=True
)
```

### 应用调用

调用已发布的智能体或工作流应用：

```python
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
```

### 语音服务

语音合成和语音识别通过 WebSocket 协议实现实时双向流式通信，客户端通过 `run-task` → 数据流 → `finish-task` 三阶段事件控制流程。

## SDK 支持

DashScope 提供多语言官方 SDK：

| 语言 | 安装方式 | 最低版本建议 |
|------|---------|-------------|
| Python | `pip install -U dashscope` | 最新版 |
| Java | Maven: `com.alibaba:dashscope-sdk-java` | ≥ 2.12.0 |
| Android / iOS | 平台原生 SDK | — |

对于 Node.js、Go、PHP、C# 等语言，可直接通过 HTTP 接口或 OpenAI 兼容 SDK 调用，将 `base_url` 指向 `https://dashscope.aliyuncs.com/compatible-mode/v1` 即可。

## 与兼容接口的对比

| 维度 | DashScope 原生 | OpenAI 兼容 | Anthropic 兼容 |
|------|---------------|-------------|----------------|
| 功能覆盖 | 最全 | 部分功能 | 部分功能 |
| 迁移成本 | 需学习专属 API | 对 OpenAI 用户零成本 | 对 Anthropic 用户零成本 |
| 应用调用支持 | 完整（智能体+工作流） | 通过 Responses API 支持 | 不支持 |
| 语音/音频能力 | 完整 | 不支持 | 不支持 |
| 建议场景 | 需要完整功能集或最优性能 | 迁移现有 OpenAI 项目 | 迁移现有 Anthropic 项目 |

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [audio api references](../api/audio-api-references.md)
- [speech recognition api reference](../api/speech-recognition-api-reference.md)
- [more models](../api/more-models.md)
- [preparations](../api/preparations.md)


