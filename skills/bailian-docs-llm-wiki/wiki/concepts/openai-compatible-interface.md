# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 协议规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/images/generations` 等），使开发者无需修改代码逻辑即可将现有基于 OpenAI SDK 或工具链（如 LangChain、LlamaIndex）的应用快速迁移到百炼平台，底层由 Qwen 系列大模型（如 `qwen-max`、`qwen-plus`、`qwen-vl`）提供服务。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有项目**：若您的应用已使用 `openai` Python SDK、`@langchain/openai` 或 Postman 调用 OpenAI 接口，只需将 `base_url` 替换为百炼的兼容端点（如 `https://dashscope.aliyuncs.com/v1` 或 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并改用百炼 API Key，即可零代码改动运行。
- **集成主流开发工具**：支持 Cursor、Cline、Qwen Code、WorkBuddy、Hermes Agent 等 CLI 与桌面客户端；配置时选择「OpenAI 协议」并填入对应 `base_url` 和 API Key 即可调用 Qwen 模型。
- **构建 RAG 应用**：通过 `/v1/embeddings` 调用 `text-embedding-v1` 生成向量，或通过 `/v1/rerank` 使用 `rerank-v1` 重排序，响应结构与 OpenAI 一致（含 `data` 数组、`object` 类型字段），可直接复用现有向量检索流水线。
- **多模态与批量任务**：支持 `images/generations`（Qwen-VL）、`batches`（Batch Chat）、`files`（文件上传解析）等端点，适用于文生图、异步批量推理、PDF/Excel 内容提取等场景。
- **LangChain 等框架直连**：安装 `langchain-bailian` 后，使用 `BailianChatModel` 或 `BailianEmbeddings` 类，传入 `model_name="qwen-plus"` 即可替代 `ChatOpenAI`，完全兼容 LangChain v0.1.x 的链式调用与提示工程。

> ⚠️ 注意：并非所有 OpenAI 功能均 100% 行为一致。例如：
> - `OpenAI 兼容-Responses` 接口的 `max_tokens` 计算包含系统提示与工具返回内容，非仅限模型输出；
> - `stream=true` 时 `functions` / `tools` 参数被忽略，不支持流式[函数调用](function-calling.md)；
> - `system` 角色在部分视觉接口（如 `qwen-vl`）中不被支持；
> - 所有兼容接口**仅接受百炼平台发放的 API Key**，不兼容 OpenAI 官方 Key。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| `model` | string | 是 | 百炼注册的模型 ID（区分大小写），非 OpenAI 原生名 | `"qwen-plus"`, `"qwen-vl-plus"`, `"text-embedding-v1"` |
| `base_url` | string | 是（客户端侧） | 兼容接口统一入口地址，按套餐类型区分：<br>• Token Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Coding Plan：`https://coding.dashscope.aliyuncs.com/v1`<br>• 按量计费：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1` | `https://dashscope.aliyuncs.com/v1`（通用调试用） |
| `Authorization` | header | 是 | `Bearer <your_bailian_api_key>` | `Bearer sk-xxx` |
| `temperature` / `top_p` / `max_tokens` | number | 否（有默认值） | 语义与 OpenAI 一致，但受模型能力硬性约束（如 `qwen-vl` 最大 `max_tokens=2048`） | `"temperature": 0.5`, `"max_tokens": 1024` |
| `response_format` | object | 否 | 仅 `chat/completions` 支持 `{"type": "json_object"}`，需模型本身启用 JSON 模式 | `{"type": "json_object"}` |
| `enable_code_interpreter` / `enable_web_search` | boolean | 否（仅 `OpenAI 兼容-Responses`） | 开启预置增强能力（联网搜索、代码执行），独立开关 | `"enable_web_search": true` |

> ✅ 提示：  
> - 所有兼容接口均**不支持自定义 function calling 工具**（仅 DashScope 原生与 Anthropic 接口支持）；  
> - `file_id`、`batch_id` 等资源 ID **必须通过百炼平台上传获取**，不可复用 OpenAI 的 ID；  
> - 图像 URL 必须为公网可访问地址（如 S3、OSS 公共链接），本地路径或内网地址将失败。

## 面向开发者：一句话上手

```bash
# 一行 cURL 调用 Qwen-Plus（OpenAI 兼容）
curl -X POST "https://dashscope.aliyuncs.com/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen-plus",
        "messages": [{"role": "user", "content": "用中文写一首关于春天的五言绝句"}],
        "temperature": 0.3
      }'
```

✅ 推荐实践：  
- 新项目优先选用 **DashScope 原生接口**（功能最全、控制最细）；  
- 迁移项目首选 **OpenAI 兼容接口**（省时省力，生态无缝）；  
- 需要深度推理、GUI 自动化或 OCR 等专用能力时，请确认该模型是否支持 OpenAI 协议（如 `qwen-deep-research` **不支持**，必须用 DashScope SDK）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


