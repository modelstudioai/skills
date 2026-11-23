# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI 官方 RESTful 接口规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/files` 等），使开发者无需修改业务代码逻辑，仅需替换 `base_url`、`api_key` 和 `model` 参数，即可将现有 OpenAI SDK、LangChain、LlamaIndex 或各类 AI 编程工具（如 Cursor、WorkBuddy、Qwen Code）快速迁入百炼生态。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：支持三类核心协议  
  - **Chat Completions**：标准对话接口，兼容 `messages` 数组输入，支持文本、图像、音频、视频多模态（如 `qwen3-vl-plus`、`qwen3.8-omni-flash`），但 `qwen-audio` 不支持该协议；  
  - **Responses**：面向智能体（Agent）的增强型接口，内置联网搜索、代码解释器、知识库检索等工具链，通过 `previous_response_id` 简化多轮上下文管理，并支持 `x-dashscope-session-cache: enable` 自动会话缓存；  
  - **Embeddings / Rerank / Files / Batch**：向量生成、重排序、文件上传与批量推理等能力均提供 OpenAI 风格路径（如 `/v1/embeddings`、`/v1/files`、`/v1/batch`），实现功能平移与工具链复用。

- **开发工具接入**：主流 CLI（`qwen`、`opencode`）、桌面端（Trae、WorkBuddy）及 IDE 插件（Qwen Code）均原生适配 OpenAI 兼容协议，只需配置对应计费方案的 API Key 与 Base URL（如 Token Plan 使用 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），即可开箱即用。

- **框架集成**：完全兼容 LangChain、LlamaIndex、llama.cpp（via `openai` adapter）、Ollama（via `--host` 指向百炼 endpoint）等生态工具，开发者可复用已有 Prompt 工程、Chain 构建和评估流水线。

- **迁移与演进**：相比 DashScope 原生协议，OpenAI 兼容接口牺牲了极少数底层控制能力（如 `max_frames` 视频帧数、`qwen-audio` 全功能支持），但显著降低接入门槛；平台明确推荐新项目优先采用兼容接口，旧版 `dashscope.aliyuncs.com` 域名虽仍可用，但性能与稳定性低于业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填。服务根地址，**必须使用业务空间专属域名**：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>支持地域：`cn-beijing`、`ap-southeast-1`、`us-east-1`、`eu-central-1`、`ap-northeast-1`、`cn-hongkong` | ❗ 旧域名 `https://dashscope.aliyuncs.com` 已不推荐；Token Plan/Coding Plan 有固定域名（见文档） |
| `api_key` | 必填。密钥类型需与计费方案匹配：<br>- Token Plan：个人版/团队版专属密钥<br>- 按量计费：通用百炼 API Key<br>- Coding Plan：Coding Plan 专属密钥 | 密钥权限隔离，不可混用 |
| `model` | 必填。模型名须严格匹配，不同接口支持范围不同：<br>- Chat：`qwen4-max`、`qwen3-vl-plus`、`deepseek-v4.1-flash` 等<br>- Responses：额外支持 `qwen3.8-omni-flash`（含音视频输入）<br>- Embeddings：仅限向量模型（如 `text-embedding-v4`、`qwen3.7-text-embedding`） | 模型列表以 [官方兼容性文档](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope) 为准，非所有 Qwen 模型均全协议支持 |
| `messages` / `input` / `content` | Chat 与 Anthropic 使用 `messages`；Responses 支持 `string` 或 `array` 格式 `input`；Embeddings/Rerank 使用 `input` 字段 | 多模态输入需按 OpenAI 格式组织（如 `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`） |
| `previous_response_id` | Responses 特有。用于关联上一轮响应，自动注入上下文与工具执行历史 | 替代手动拼接 `messages`，简化 Agent 开发 |
| `x-dashscope-session-cache` | Headers 中设置为 `enable`，启用服务端会话缓存，提升多轮响应一致性 | 仅 Responses 接口支持 |

## 面向开发者，简洁实用

✅ **快速启动（Python 示例）**：
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-xxx",  # 替换为你的 API Key
    base_url="https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

# 调用千问大模型
response = client.chat.completions.create(
    model="qwen4-max",
    messages=[{"role": "user", "content": "你好，请用中文介绍你自己"}]
)
print(response.choices[0].message.content)
```

✅ **关键检查清单**：
- ✅ 确认 `base_url` 使用 `{WorkspaceId}` 专属域名（控制台「模型设置」→「API Key」页可查）  
- ✅ 核对 `model` 是否在当前接口的支持列表中（如 `qwen-audio` 不支持 OpenAI 协议）  
- ✅ 多模态请求注意 `detail`、`min_pixels`、`max_pixels` 等参数取值（`qwen4-max` 图像 `max_pixels=16777216`）  
- ✅ Agent 场景优先选 `Responses` 接口 + `previous_response_id`，避免上下文管理复杂度  
- ✅ 新项目禁用 `dashscope.aliyuncs.com`，旧项目请尽快迁移至 `maas.aliyuncs.com` 域名  

✅ **调试建议**：  
- 使用 `curl -v` 查看完整请求/响应头，确认 `x-dashscope-request-id` 便于问题定位；  
- 错误码统一遵循 OpenAI 标准（`400 Bad Request`、`401 Unauthorized`、`429 Rate Limited` 等），响应体结构一致；  
- 所有兼容接口均支持流式响应（`stream=True`），适用于前端实时渲染。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [vector and sort](../api/vector-and-sort.md)


