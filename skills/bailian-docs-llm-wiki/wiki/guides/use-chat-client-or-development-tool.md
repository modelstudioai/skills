# use chat client or development tool

百炼平台支持通过多种主流聊天客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成及低代码工作流编排等场景。开发者可直接配置 API Key 和 Endpoint 即可调用，无需部署模型服务。所有工具均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`）通信，兼容性由 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 统一维护。

## 支持的模型与功能

- **模型覆盖**：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio、Qwen2-Audio 及 DeepSeek-V2/V3（需开通对应权限）；部分工具如 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 和 [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 还支持多模态输入（图像/音频）和[函数调用](../concepts/function-calling.md)（function calling）。
- **核心能力**：包括流式响应（`stream: true`）、系统提示（`system` role）、工具调用（`tools` + `tool_choice`）、JSON Schema 输出约束（`response_format: { "type": "json_object" }`），以及上下文长度扩展（最高 32768 tokens，取决于所选模型）。
- > **注意**：[Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档中提及的 `/v1/images/generations` 接口示例已过时，当前图像生成统一走 `/v1/chat/completions` 并启用 `qwen-vl` 模型，详见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的“多模态接入”章节。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`、`qwen-plus`、`qwen2.5-72b-instruct`；必须与所选工具支持的模型列表一致（见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中各工具子页） |
| `temperature` | number | 否 | 默认 `0.8`；取值范围 `[0.0, 2.0]`，影响输出随机性 |
| `top_p` | number | 否 | 默认 `0.8`；建议与 `temperature` 不同时调整 |
| `max_tokens` | integer | 否 | 最大生成 token 数，默认 `1024`，上限 `8192`（部分模型支持更高） |
| `stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应 |

## 使用方式

1. **获取凭证**：在百炼控制台「API 密钥」页创建密钥，记录 `API Key` 和 `Endpoint`（如 `https://dashscope.aliyuncs.com/api/v1`）；
2. **配置工具**：
   - CLI 工具（如 `Kilo CLI`、`Cline`）：通过环境变量 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL` 设置；
   - GUI 工具（如 `Cursor`、`Cherry Studio`、`Dify`）：在设置页粘贴 Endpoint 和 API Key，选择模型后即可发送请求；
   - 自定义代码：按 OpenAI SDK 格式初始化客户端（如 `openai.OpenAI(base_url=..., api_key=...)`）；
3. **发起请求**：构造标准 `messages` 数组（含 `role` 和 `content`），调用 `/v1/chat/completions`。

## 限制和注意事项

- 单次请求 `messages` 总长度（输入+输出）不得超过模型上下文窗口（例如 `qwen-plus` 为 32768 tokens），超长将被截断并返回 `400` 错误；
- 所有工具均不支持自定义模型微调权重上传，仅能调用平台托管的公开或私有部署模型；
- `system` 消息在部分旧版工具（如早期 `Claude Code` 插件）中可能被忽略，建议优先使用 `Qwen Code` 或 `Qoder CN（原 Lingma）` 等明确声明支持 system role 的工具；
- 流式响应需客户端正确处理 `data:` 前缀与 `event: message` 字段，参考 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的“流式调试”小节。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


