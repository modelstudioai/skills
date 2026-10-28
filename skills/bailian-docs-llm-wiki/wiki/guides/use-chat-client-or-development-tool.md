# use chat client or development tool

百炼平台支持通过多种主流聊天客户端与开发工具接入大模型服务，适用于快速原型验证、本地 IDE 集成及低代码工作流编排等场景。开发者可直接配置 API Key 和 Endpoint 即可调用，无需部署模型服务。所有工具均基于标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/v1/chat/completions`）通信，兼容性由 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 统一维护。

## 支持的模型与功能

- **模型覆盖**：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio、Qwen2-Audio 及 DeepSeek-V2/V3（需开通对应权限）；部分工具如 [Cherry Studio](../../raw/model-user-guide/use-chat-client-or-development-tool/cherry-studio.md) 和 [Qoder](../../raw/model-user-guide/use-chat-client-or-development-tool/qoder-agent.md) 还支持多模态输入（图像/音频上传）。
- **核心能力**：包括基础对话、[函数调用](../concepts/function-calling.md)（Function Calling）、工具调用（Tool Use）、结构化输出（JSON Mode）、流式响应（`stream: true`）及系统提示词注入（`system` role）。
- > **注意**：[Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档中示例仍指向旧版 `/v1/image/generate` 路径，实际图像/视频类 API 已统一迁移至 `/v1/multimodal/chat/completions`，请以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中的最新路由为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`、`qwen-plus`、`qwen-turbo`；必须与所选工具支持的模型列表一致（见各工具子文档） |
| `temperature` | number | 否 | 默认 `0.7`；取值范围 `[0, 2]`，影响输出随机性 |
| `top_p` | number | 否 | 默认 `1.0`；建议与 `temperature` 不同时调整 |
| `max_tokens` | integer | 否 | 响应最大 token 数，上限依模型而定（如 `qwen-max` 为 8192） |
| `stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应，需客户端支持解析 `data:` 块 |

## 使用方式

1. **获取凭证**：在百炼控制台「API 密钥」页生成 AccessKey ID / Secret，或使用短期 STS [Token](../concepts/token.md)；
2. **配置 Endpoint**：  
   - 标准 Chat 接口：`https://dashscope.aliyuncs.com/api/v1/chat/completions`  
   - 多模态接口：`https://dashscope.aliyuncs.com/api/v1/multimodal/chat/completions`  
   （详见 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md)）
3. **工具适配**：  
   - OpenClaw、Cursor、Cherry Studio 等 GUI 工具：在设置中填入 Endpoint + API Key，选择对应模型；  
   - CLI 工具（如 Kilo CLI、Cline）：通过 `--endpoint` 和 `--api-key` 参数传入；  
   - Dify / Hermes Agent：在「模型配置」中选择「DashScope」提供商并填写凭证。

## 限制和注意事项

- 单次请求最大上下文长度受模型限制（如 `qwen-turbo` 为 4096 tokens），超长文本需预处理截断或分块；
- 所有工具均不支持自定义 LoRA 或微调模型加载，仅限平台已发布的官方模型；
- [函数调用](../concepts/function-calling.md)（Function Calling）需显式声明 `tools` 字段且模型支持该能力（`qwen-max`、`qwen-plus` 支持，`qwen-turbo` 不支持）；
- 图像/音频输入仅支持 Base64 编码或阿里云 OSS URL，不支持本地文件路径直传；
- 部分工具（如 Codex、Claude Code）文档未明确标注是否支持 `response_format: { "type": "json_object" }`，实际可用性请以 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的兼容性矩阵为准。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


