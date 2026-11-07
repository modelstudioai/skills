# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`、`messages` 数组、`tool_choice` 等），使开发者能**零代码改造复用现有 OpenAI SDK、LangChain、LlamaIndex 等生态工具**，仅需替换 `base_url` 和 `model` 即可快速接入千问及第三方模型。

## 在百炼平台的不同场景中如何使用

- **基础对话与多模态推理**：通过 `chat.completions.create()` 调用 `qwen3.8-max`、`qwen3-vl-plus`、`qwen3.8-omni-flash` 等模型，支持文本、图像、音视频混合输入（`messages` 中含 `image_url` 或 `video_url`），适用于客服、内容生成、多模态分析等场景。  
- **智能体（Agent）开发**：使用 `responses.create()`（OpenAI Responses 兼容接口），原生支持 `web_search`、`code_interpreter`、`file_search` 等内置工具，并允许传入自定义 function schema，无需手动解析 tool calls。  
- **向量嵌入**：调用 `embeddings.create()`，支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，可指定 `dimensions`、`encoding_format`，适用于 RAG、语义搜索等场景。  
- **文件处理与批量任务**：通过 `files.create(purpose="file-extract")` 上传 PDF/Word 等文档，再结合 `chat.completions.create()` 的 `file_ids` 参数实现文档问答；或使用 `purpose="batch"` 提交 JSONL 文件执行异步批量推理。  
- **会话状态管理**：配合 `conversations.create()` 与 `conversations.items.create()`，结合 `responses.create(previous_response_id=...)` 实现跨设备、无状态的多轮上下文延续，替代手动拼接 `messages`。  

> ⚠️ 注意：`Qwen-Audio` 模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口；`QwQ`/`QVQ` 模型的 `system` message 不生效，建议避免设置。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 是否必填 |
|------|------|--------|----------|
| `base_url` | 地域专属兼容模式入口，格式为 `https://{WorkspaceId}.{Region}.maas.aliyuncs.com/compatible-mode/v1` | `https://wk-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 是 |
| `model` | 模型 ID，大小写敏感，须从[支持列表](#)中选择 | `"qwen3.8-max"`, `"text-embedding-v4"`, `"qwen3-vl-plus"` | 是 |
| `messages` | 标准 OpenAI 消息数组，支持 `role`（`system`/`user`/`assistant`/`tool`）、`content`（字符串或含 `image_url` 的对象） | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"data:image/png;base64,..."}}]}]` | 是（Chat/Responses） |
| `stream` | 启用流式响应，返回 `text/event-stream` | `true` | 否（默认 `false`） |
| `previous_response_id` | Responses 接口特有，用于轻量级多轮对话（自动继承上下文与工具结果） | `"resp_abc123..."` | 否（替代 `messages`） |
| `dimensions` | 向量模型专用，指定输出维度（仅部分 embedding 模型支持） | `1024` | 否 |
| `purpose` | Files 接口必需，标识文件用途：`file-extract`（文档解析）、`batch`（批量任务）、`fine-tune`（微调） | `"file-extract"` | 是（Files） |

- **认证方式**：使用环境变量 `DASHSCOPE_API_KEY`（非 `OPENAI_API_KEY`），SDK 自动注入 `Authorization: Bearer <key>`。
- **地域要求**：`base_url` 中的 `{Region}` 必须与工作空间所在地域一致（如 `cn-beijing`），不支持跨 Region 调用。

## 面向开发者：快速上手提示

1. **安装 SDK**：`pip install -U openai langchain_openai`（推荐 LangChain v0.3+）  
2. **初始化客户端**：
   ```python
   from openai import OpenAI
   client = OpenAI(
       api_key=os.getenv("DASHSCOPE_API_KEY"),
       base_url="https://wk-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
   )
   ```
3. **一句话切换模型**：将 `model="gpt-4o"` 改为 `model="qwen3.8-omni-flash"`，其余代码完全不变。  
4. **调试技巧**：启用 `stream=True` 查看 token 流；检查响应中的 `x-dashscope-status` header 判断是否命中缓存或工具调用。  
5. **避坑指南**：  
   - 不要对 `Qwen-Audio` 使用 OpenAI 接口；  
   - 多模态输入时，确保 `image_url.url` 为公网可访问链接或 `data:` base64；  
   - 批量任务优先用 `purpose="batch"` + JSONL，而非高频单请求。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [vector and sort](../api/vector-and-sort.md)


