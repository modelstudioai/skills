# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套遵循 OpenAI API 协议规范的调用方式，允许开发者使用现有的 OpenAI SDK 和工具链直接访问百炼模型服务，仅需替换 `api_key`、`base_url` 和 `model` 三个参数即可完成迁移。

## 接入三要素

| 参数 | 说明 |
| --- | --- |
| `api_key` | 百炼 API Key，各地域互不通用 |
| `base_url` | 因地域而异，见下方服务地址表 |
| `model` | 百炼模型名称，如 `qwen-plus`、`qwen3-vl-plus`、`text-embedding-v4` |

## 服务地址

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

新加坡和法兰克福地域的 URL 中 `{WorkspaceId}` 需替换为真实的[业务空间](workspace.md) ID。

## 支持的接口类型

百炼的 OpenAI 兼容模式覆盖以下接口：

- **Chat Completions**（`/v1/chat/completions`）：最常用的对话接口，支持千问全系列及第三方模型。
- **Responses**（`/v1/responses`）：面向智能体场景的演进版本，内置联网搜索、代码解释器等工具，通过 `previous_response_id` 自动管理对话历史。
- **Completions**（`/v1/completions`）：文本/代码补全，支持前缀补全和中间填充（FIM）模式，当前仅支持 `qwen-coder-turbo`。
- **Vision**：复用 Chat Completions 端点，`content` 改为数组形式传入图片。
- **Embedding / Files / Batch**：向量化、文件管理、批量推理等辅助能力。

## 典型使用场景

### 迁移现有 OpenAI 应用

已有 OpenAI 代码的项目可直接切换到百炼，改动量最小。Python 示例：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 接入第三方工具和客户端

百炼通过 OpenAI 兼容接口支持大量第三方工具直接接入，包括：

- **终端工具**：Codex、Kilo CLI、Qwen Code 等
- **桌面客户端**：Cursor、Cherry Studio、Chatbox
- **IDE 插件**：Cline、Qoder（原 Lingma）
- **开发平台**：Dify

配置时将 Base URL 和 API Key 填入对应工具的设置项即可。

### 模型调优（Fine-tuning）

Fine-tuning Jobs API 遵循 OpenAI 兼容接口规范，开发者可通过标准的 OpenAI SDK 提交微调任务、查询状态和管理调优模型。

### 专用模型调用

Qwen-MT（机器翻译）、Qwen-OCR（文字识别）、GUI-Plus（界面交互）等专用模型均通过 OpenAI 兼容接口调用，部分模型需在请求体中传入专属扩展字段（如 `extra_body.translation_options`）。

### 框架集成

LangChain、LlamaIndex、Spring AI Alibaba 等主流框架通过 OpenAI 兼容接口接入百炼，可快速构建 RAG 应用和智能体服务。

## 注意事项

- 不同地域的 API Key 互不通用，切换地域时须同时更换 `base_url` 和 API Key。
- OpenAI 兼容接口覆盖了绝大多数常用功能，但部分高级参数仅在 DashScope 原生接口中支持。
- Responses 接口会自动管理对话历史，对话状态管理逻辑与 Chat Completions 不同。
- 新加坡旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版地址。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [specialized model](../api/specialized-model.md)
- [fine tuning jobs api](../api/fine-tuning-jobs-api.md)
- [frameworks](../api/frameworks.md)


