# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一组遵循 OpenAI API 协议规范的调用端点，允许开发者使用现有的 OpenAI SDK 和生态工具直接访问百炼上的大模型服务，无需修改业务代码逻辑。

## 核心价值

OpenAI 兼容接口的设计目标是将迁移成本降到最低。开发者只需替换三个参数即可从 OpenAI 切换到百炼：

- **api_key**：替换为百炼 [API Key](api-key.md)（建议通过环境变量 `DASHSCOPE_API_KEY` 注入）
- **base_url**：替换为百炼[业务空间](workspace.md)专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`
- **model**：替换为百炼支持的模型名称（如 `qwen3.7-plus`、`qwen3.7-max` 等）

## 支持的接口类型

百炼的 OpenAI 兼容接口覆盖多种能力：

| 接口 | HTTP 路径 | 典型场景 |
| --- | --- | --- |
| Chat Completions | `POST /chat/completions` | 多轮对话、function call、流式输出 |
| Responses | `POST /responses` | 智能体原生能力、内置工具（联网搜索、代码解释器、网页抓取）、自动管理对话历史 |
| Completions | `POST /completions` | 代码补全、文本续写（FIM） |
| Embeddings | `POST /embeddings` | 文本向量化 |
| File | `POST /files` | 文件上传/查询/删除 |
| Batch | `POST /batches` | 异步批量推理（费用减半） |

## 地域与接入域名

不同地域使用不同的 base_url，且 [API Key](api-key.md) 必须与地域匹配：

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中 `{WorkspaceId}` 为[业务空间](workspace.md) ID，可在百炼控制台查看。弗吉尼亚地域使用固定域名，不带 WorkspaceId。

## 支持的模型

Chat Completions 接口支持的模型范围最广，包括：

- **Qwen 系列**：qwen3.7-max、qwen3.7-plus、qwen3.6-flash 等全系列
- **第三方模型**：DeepSeek、Kimi、GLM、MiniMax（需在控制台开通，仅限中国内地地域）

部分专用模型（如 qwen-mt-plus 翻译、qwen3.5-ocr、gui-plus 界面交互、tongyi-intent-detect-v3 意图理解）也支持通过 OpenAI 兼容接口调用。但 qwen-deep-research 等少数模型暂不支持该协议。

## [计费](billing.md)方案

OpenAI 兼容接口支持三种[计费](billing.md)方案，每种方案有独立的 [API Key](api-key.md) 和 Base URL，不可混用：

- **按量[计费](billing.md)**：按实际调用量后付费，适用于所有工具
- **Coding Plan**：固定月费，专属域名 `https://coding.dashscope.aliyuncs.com/v1`
- **[Token](token.md) Plan 团队版**：按坐席订阅，专属域名 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

## 与 DashScope 原生接口的区别

- **功能完整度**：兼容接口为保证协议一致性，可能不暴露百炼原生的全部参数；如需最全的采样参数或业务字段，建议使用 DashScope 原生接口
- **工具能力**：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力，Chat Completions 接口不内置这些工具
- **对话历史**：仅 Responses 接口自动维护历史，其他接口需自行管理上下文

## 典型使用示例

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3.7-plus",
    messages=[{"role": "user", "content": "你好"}]
)
print(completion.choices[0].message.content)
```

## 注意事项

- API Key、Base URL、地域三者必须匹配，否则会返回 401 错误
- 从 OpenAI/Anthropic 迁移时，应先确认目标模型在兼容接口下是否支持所需参数（如 `temperature`、`tools`、`stream` 等）
- Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议
- 流式输出时可通过 `stream_options={"include_usage": True}` 在最后一行获取 token 用量

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [more models](../api/more-models.md)
- [get started with models](../guides/get-started-with-models.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [preparations](../api/preparations.md)
- [managed agents api](../api/managed-agents-api.md)


