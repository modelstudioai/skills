# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI API 规范的调用端点，开发者可以直接使用 OpenAI 官方 SDK 或任何兼容 OpenAI 协议的客户端工具接入百炼的模型服务，无需额外适配。

## 接口类型

百炼提供多种 OpenAI 兼容接口，覆盖不同使用场景：

| 接口 | 端点路径 | 适用场景 |
|------|---------|---------|
| Chat Completions | `/compatible-mode/v1/chat/completions` | 文本对话、function call、多模态理解 |
| Responses API | `/compatible-mode/v1/responses` | 智能体场景，内置联网搜索、代码解释器等工具，自动管理对话历史 |
| Completions | `/compatible-mode/v1/completions` | 代码补全、文本续写（FIM） |
| Embedding | `/compatible-mode/v1/embeddings` | 文本向量化 |
| Files | `/compatible-mode/v1/files` | 文件上传与管理 |
| Batch | `/compatible-mode/v1/batch` | 批量推理，降低成本 |

其中 Chat Completions 是最常用的接口，适合从现有 OpenAI 应用迁移；Responses API 是其演进版本，提供更简洁的智能体原生能力。

## 通用配置

所有 OpenAI 兼容接口共享三个核心配置参数：

- **API Key**：在百炼控制台创建，通过环境变量 `DASHSCOPE_API_KEY` 传入。不同地域和计费方案的 Key 不通用。
- **Base URL**：根据地域和计费方案选择对应端点。
- **模型名称（model）**：替换为百炼支持的模型 ID，如 `qwen3.7-plus`、`deepseek-v4-pro` 等。

### 各地域 Base URL

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

华北2（北京）和新加坡地域还推出了新版域名 `{WorkspaceId}.{region}.maas.aliyuncs.com`，旧版域名即将下线。

### 套餐专属端点

- **Token Plan 团队版**：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`
- **Coding Plan**：`https://coding.dashscope.aliyuncs.com/v1`

## 基本调用示例

使用 OpenAI Python SDK 调用百炼模型：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

同样支持 Node.js（OpenAI SDK）、curl 等方式调用。

## 支持的模型范围

通过 OpenAI 兼容接口可调用的模型涵盖：

- **千问系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等文本生成模型，以及视觉理解模型
- **第三方模型**：deepseek-v4-pro、kimi-k2.7-code、glm-5.1、MiniMax-M2.5 等，API 格式与千问一致
- **专用模型**：Qwen-MT（翻译）、Qwen-OCR（文字提取）、GUI-Plus（界面交互）、tongyi-intent-detect（意图识别）等
- **音视频翻译**：qwen3-livetranslate-flash 通过 OpenAI 兼容接口进行离线翻译
- **向量模型**：text-embedding-v1/v2/v3/v4

## 第三方工具接入

由于兼容 OpenAI 协议，百炼可直接接入大量第三方 AI 工具，包括：

- **终端编程工具**：Codex、Qwen Code、Kilo CLI 等
- **桌面客户端**：Cherry Studio、Chatbox、QwenPaw
- **IDE 插件**：Cursor、Cline、Qoder
- **低代码平台**：Dify

这些工具只需配置百炼的 API Key 和 Base URL 即可使用，无需额外开发。

## 与 [DashScope 接口](dashscope-api.md)的区别

OpenAI 兼容接口与百炼原生 [DashScope 接口](dashscope-api.md)的主要差异：

| 维度 | OpenAI 兼容接口 | [DashScope 接口](dashscope-api.md) |
|------|----------------|---------------|
| 迁移成本 | 低，直接复用 OpenAI SDK | 需使用 DashScope SDK 或适配请求格式 |
| 功能覆盖 | 覆盖主流场景 | 最完整的功能集和参数支持 |
| 生态兼容 | 兼容所有 OpenAI 生态工具 | 百炼专属生态 |

对于已有 OpenAI 代码的项目，优先选择 OpenAI 兼容接口以降低迁移成本；需要百炼平台全部能力时，选择 [DashScope 接口](dashscope-api.md)。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [specialized model](../api/specialized-model.md)
- [token plan guide](../guides/token-plan-guide.md)
- [speech translation api reference](../api/speech-translation-api-reference.md)
- [model inference](../guides/model-inference.md)



