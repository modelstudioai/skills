# DashScope SDK

DashScope SDK 是阿里云百炼平台的官方开发工具包，提供对百炼模型服务的原生接入能力。开发者可通过 DashScope SDK 调用文本生成、图像生成、视频生成、向量化、应用集成等全系列 API，是除 [OpenAI 兼容接口](openai-compatible.md)外的另一种主要接入方式。

## 支持的语言与安装

DashScope SDK 目前支持 Python 和 Java 两种语言：

| 语言 | 安装方式 | 环境要求 |
|------|---------|---------|
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` | Java 8+ |

> 如果项目更倾向于使用 OpenAI 生态工具链，百炼也提供 [OpenAI 兼容接口](openai-compatible.md)，可通过 `openai` 官方 SDK（Python/Node.js/Java/Go）接入，两种方式功能上大部分等价。

## 鉴权与环境配置

DashScope SDK 通过 API Key 进行鉴权。推荐将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄漏风险：

```bash
# Linux / macOS（永久生效）
echo 'export DASHSCOPE_API_KEY="YOUR_KEY"' >> ~/.zshrc
source ~/.zshrc

# Windows CMD（永久生效）
setx DASHSCOPE_API_KEY "YOUR_KEY"
```

SDK 会自动读取该环境变量，也可在调用时通过 `api_key` 参数显式传入。

## 典型使用场景

### 应用调用

通过 `dashscope.Application.call()` 调用百炼平台上的智能体应用和工作流应用：

```python
from dashscope import Application

response = Application.call(
    app_id='YOUR_APP_ID',
    prompt='你的问题')
print(response.output.text)
```

支持通过 `session_id` 实现多轮对话（云端存储，有效期 1 小时，最多 50 轮），也可通过 `messages` 数组自行管理对话历史。

### 文本生成

通过 `dashscope.Generation.call()` 调用文本生成模型（如通义千问、通义法睿等）：

```python
from dashscope import Generation

response = Generation.call(
    model='qwen3.7-plus',
    messages=[{'role': 'user', 'content': '你好'}])
```

### 向量化

通过 DashScope 原生接口调用文本向量模型（text-embedding-v1 至 v4）和多模态向量模型，将文本、图像、视频转换为数值向量，用于语义搜索、RAG、聚类等场景。

### 图像与视频生成

图像生成和视频生成 API 均采用异步调用模式。SDK 封装了"创建任务 + 轮询结果"的流程，请求时需设置异步标志。支持万相、千问图像、Z-Image、HappyHorse 等多个模型系列。

### 深度研究

`qwen-deep-research` 模型目前仅支持通过 DashScope Python SDK 和 curl 调用（暂不支持 Java SDK 和 [OpenAI 兼容接口](openai-compatible.md)），采用两阶段交互流程：先反问确认研究方向，再深入搜索生成报告。

## DashScope SDK 与 OpenAI 兼容接口的选择

| 维度 | DashScope SDK | OpenAI 兼容接口 |
|------|--------------|----------------|
| 语言支持 | Python、Java | Python、Node.js、Java、Go |
| 功能覆盖 | 全部百炼能力（含应用调用、部分专用模型） | 大部分模型推理能力 |
| 生态兼容 | 百炼原生 | 可复用 OpenAI 生态工具和代码 |
| 推荐场景 | 需要调用百炼应用、使用百炼专有功能 | 已有 OpenAI 代码需迁移、多语言统一接入 |

部分模型（如 `qwen-deep-research`）仅支持 DashScope SDK，而结构化输出等新特性在 OpenAI 兼容接口上支持更好，实际选择时应结合具体模型和功能需求。

## 关键配置参数

| 参数 | 说明 |
|------|------|
| `api_key` | API Key，优先从环境变量 `DASHSCOPE_API_KEY` 读取 |
| `model` | 模型名称，如 `qwen3.7-plus`、`farui-plus`、`text-embedding-v4` 等 |
| `base_url` | 服务端点，不同地域使用不同 URL（北京、新加坡、美国弗吉尼亚等） |
| `X-DashScope-Async: enable` | 异步任务标志（图像/视频生成必须设置） |

## 地域与端点

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |

新加坡、日本、德国地域的 URL 中需将 `{WorkspaceId}` 替换为实际的[业务空间](workspace.md) ID。

## 关联主题页

- [preparations](../api/preparations.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more models](../api/more-models.md)
- [vector and sort](../api/vector-and-sort.md)
- [model inference](../guides/model-inference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


