# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套与 OpenAI API 规范兼容的调用接口，开发者只需修改 `base_url`、`api_key` 和 `model` 三个参数，即可将基于 OpenAI SDK 构建的应用无缝迁移至百炼平台，调用千问（Qwen）及其他第三方大模型。

## 兼容的接口端点

百炼的 OpenAI 兼容接口覆盖以下能力：

| 接口 | 端点路径 | 用途 |
|------|---------|------|
| Chat Completions | `/v1/chat/completions` | 对话生成（文本、多模态） |
| Responses | `/v1/responses` | Chat Completions 的演进版，内置工具与简化上下文管理 |
| Completions | `/v1/completions` | 文本/代码补全（FIM） |
| Embeddings | `/v1/embeddings` | 文本向量化 |
| Files | `/v1/files` | 文件上传（文档问答、Batch、调优） |
| Batch | `/v1/batches` | 文件批量推理（异步，5 折优惠） |
| Conversations | `/v1/conversations` | 会话管理（跨设备对话延续） |

其中 Chat Completions 是使用最广泛的接口，支持文本对话与视觉理解；Responses API 在此基础上内置了联网搜索、代码解释器和网页内容提取工具，并可自动管理对话历史。

## Base URL 配置

不同地域和计费方案使用不同的 `base_url`：

### 按量计费

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为业务空间 ID，可在百炼控制台查看。各地域的 API Key 互不通用，切换地域时需同步更换。

### 订阅计费

| 方案 | Base URL |
|------|----------|
| Token Plan 团队版 | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| Coding Plan | `https://coding.dashscope.aliyuncs.com/v1` |

## 快速接入

### 1. 获取 API Key

在百炼控制台的 API Key 管理页面创建。建议将其配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露。

### 2. 安装 SDK

| 语言 | 安装命令 |
|------|---------|
| Python (>=3.8) | `pip install -U openai` |
| Node.js | `npm install --save openai` |
| Java | Maven/Gradle 添加 `com.openai:openai-java`（推荐 3.5.0+） |
| Go (>=1.22) | `go get 'github.com/openai/openai-go/v3'` |

### 3. 发送请求

**Python 示例：**

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

**Node.js 示例：**

```javascript
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
});

const completion = await openai.chat.completions.create({
    model: "qwen3.7-plus",
    messages: [{ role: "user", content: "你是谁？" }],
});
console.log(completion.choices[0].message.content);
```

核心迁移要点：只需将 OpenAI SDK 的 `base_url` 指向百炼、`api_key` 替换为百炼 API Key、`model` 改为百炼支持的模型名称。

## 支持的模型

通过 OpenAI 兼容接口可调用的主要模型包括：

- **文本生成**：千问系列（qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等）、DeepSeek、Kimi、GLM、MiniMax 等第三方模型
- **视觉理解**：Qwen-VL、QVQ、Qwen-OCR 系列（通过 Chat Completions 的多模态输入）
- **代码补全**：qwen-coder-turbo（通过 Completions 接口，支持 FIM 模式）
- **文本向量**：text-embedding-v4（支持 64~2048 维）、text-embedding-v3 等
- **文本排序**：qwen3-rerank 等重排序模型

> 三方直供模型仅在中国站的中国内地地域可用，需先在百炼控制台开通。Responses API 当前支持的模型范围较 Chat Completions 更窄，主要覆盖 qwen3 系列。

## 与 DashScope 原生接口的区别

百炼同时提供 DashScope 原生接口，两者的主要差异如下：

| 对比项 | OpenAI 兼容接口 | DashScope 原生接口 |
|--------|----------------|-------------------|
| 迁移成本 | 极低，复用 OpenAI SDK | 需使用 [DashScope SDK](dashscope-sdk.md) |
| 功能覆盖 | 覆盖主流场景 | 功能最全，支持百炼独有特性 |
| 参数兼容性 | 部分 OpenAI 独有参数可能不支持 | 完整参数控制 |
| 适用场景 | 从 OpenAI 迁移、使用第三方工具 | 需要最完整功能集 |

两种接口的计费方式和限流策略相同，均基于百炼统一的 Token 计量体系。

## 第三方工具接入

百炼的 OpenAI 兼容接口可直接对接多种第三方工具，包括：

- **AI 编程工具**：Claude Code、Cursor、Cline、Codex、Qwen Code 等
- **桌面客户端**：Cherry Studio、Chatbox、QwenPaw
- **开发框架**：LangChain、Dify 等
- **Agent 平台**：OpenClaw

配置方式统一：在工具设置中填入百炼的 Base URL 和 API Key，选择对应的模型名称即可。使用 Token Plan 团队版或 Coding Plan 时，需使用对应方案专属的 Base URL 和 API Key。

## 注意事项

- 不同地域的 API Key 不可混用，切换地域时必须同步更换 API Key 和 Base URL。
- OpenAI 兼容接口虽然与 OpenAI SDK 直接兼容，但部分 OpenAI 独有参数可能不被支持，以百炼文档为准。
- Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议。
- Batch Chat 接口使用独立端点 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`。
- 新加坡地域的旧域名 `https://dashscope-intl.aliyuncs.com` 即将停止维护，建议迁移至业务空间专属域名。

## 关联主题页

- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)
- [token plan guide](../guides/token-plan-guide.md)


