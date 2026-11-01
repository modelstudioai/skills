# qwen api reference

阿里云百炼平台提供多种兼容主流协议的 API 接口，支持通过 OpenAI 兼容、Anthropic 兼容及原生 DashScope 协议调用 Qwen 系列大模型（含文本、多模态、代码、数学等能力）。所有接口均基于业务空间（Workspace）隔离，需配置专属域名与 API Key，推荐使用新推出的 `workspace.{region}.maas.aliyuncs.com` 域名以获得更高性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用方式，覆盖不同开发习惯与能力需求：

- **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**：提供 `/chat/completions`（基础对话）和 `/responses`（增强 Agent 能力）两套端点。`/responses` 是百炼重点演进方向，内置联网搜索、网页抓取、代码解释器、知识库检索等工具，并支持 `previous_response_id` 多轮上下文管理与 Session 缓存，显著简化复杂 Agent 开发。详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容接口**：通过 `/apps/anthropic/v1/messages` 提供 Messages 协议支持，适配 Claude 生态 SDK。支持 `output_config.effort` 控制思考强度、结构化 JSON 输出（`format`）、以及 `tool_use`/`tool_result` 工具交互范式。注意其 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准。
- **DashScope 原生接口**：提供最底层、最灵活的控制，区分 `text-generation`（纯文本）与 `multimodal-generation`（多模态）服务路径。支持 `max_frames` 等 DashScope 特有参数，但不支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)中的 `store`/`previous_response_id` 等高级会话功能。

> **注意**：文档 1 中声明 “Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议”，而文档 8 的 DashScope API 文档明确列出 `千问Audio` 为支持模型。这表明音频模型能力仅在原生 DashScope 接口可用，开发者若需调用 Qwen-Audio，必须使用 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)，不可尝试通过 `/chat/completions` 或 `/responses` 调用。

## 关键参数

各接口共性参数与关键差异如下：

- **`model`**：必填。OpenAI 兼容 `/chat/completions` 支持广泛模型（含第三方直供），但 `/responses` 仅明确列出 Qwen3.x 系列、DeepSeek-V4、GLM-5、Kimi-K3 等；Anthropic 兼容接口模型列表与 `/responses` 高度重叠；DashScope 接口支持范围最广，明确包含 `千问Audio`。模型命名需严格匹配，如 `qwen3.8-max`、`qwen3-vl-plus`。
- **`messages` / `input` / `system` + `messages`**：输入格式依协议而异。OpenAI `/chat/completions` 和 DashScope 使用标准 `messages` 数组；OpenAI `/responses` 支持更灵活的 `input`（string 或 array）；Anthropic 使用 `system` + `messages` 结构。所有协议均支持 `system` 角色设定全局指令，但需注意 `QwQ` 模型不建议设置，`QVQ` 模型设置无效。
- **多模态参数**：
  - `image_url`/`input_image`/`image`：传入图片，支持 URL 或 Base64 Data URI。
  - `video_url`/`input_video`/`video`：传入视频，支持 URL 或图像列表。`fps`（抽帧率）为通用参数，取值 `[0.1, 10]`，默认 `2.0`；`min_pixels`/`max_pixels`/`total_pixels`（OpenAI）或 `min_pixels`/`max_frames`（DashScope）用于精细控制图像/视频分辨率与 [Token](../concepts/token.md) 消耗。
- **Agent 与推理参数**：
  - `tools`：定义可调用工具。`/responses` 和 Anthropic 接口均支持内置 `web_search`、`code_interpreter` 等；`/chat/completions` 仅支持 `function` 类型自定义工具。
  - `reasoning.effort`（`/responses`）或 `output_config.effort`（Anthropic）：控制模型思考强度，取值如 `xhigh`/`high`/`low`，不同模型默认值与映射规则不同，需查阅对应文档。
  - `stream`：是否流式返回，默认 `false`。

## 使用方式

1. **认证与配置**：所有接口均需 `DASHSCOPE_API_KEY`，通过 `Authorization: Bearer <key>` 请求头或 SDK 配置传入。必须将 `{WorkspaceId}` 替换为真实业务空间 ID，并选择对应地域的 `base_url` 或 `region`。
2. **端点选择**：
   - 追求快速迁移与简单对话：使用 OpenAI `/chat/completions`。
   - 构建复杂 Agent 应用：首选 OpenAI `/responses`，利用其内置工具、`previous_response_id` 和 `store` 机制。
   - 适配 Anthropic 生态：使用 `/apps/anthropic/v1/messages`。
   - 需要最大灵活性或调用 Qwen-Audio：使用 DashScope 原生接口。
3. **SDK 示例**：OpenAI SDK 可用于 `/chat/completions` 和 `/responses`（需配置正确 `base_url`）；DashScope SDK 专用于原生接口；Anthropic SDK 需手动配置 `base_url` 和 `x-api-key` 头。
4. **响应管理**：`/responses` 接口提供配套的 `GET /responses/{id}`（[获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)）、`GET /responses/{id}/input_items`（[获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)）和 `DELETE /responses/{id}`（[删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）等辅助 API，用于调试与状态追踪。

## 限制和注意事项

- **域名迁移**：华北2（北京）、新加坡、中国香港地域已启用业务空间专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com` 等）虽仍可用，但官方强烈建议迁移以获得“卓越的性能和更高的稳定性”。此要求在文档 1、4、6、8 中被多次强调。
- **功能限制**：
  - OpenAI `/chat/completions` 不支持 `Qwen-Audio` 和 `QwQ` 的 `system` 消息。
  - OpenAI `/responses` 不支持 `background` 异步执行（仅同步），且 `max_tokens` 上下文约为模型窗口的 80%（预留 20% 给工具与推理）。
  - Anthropic 接口不提供 `/v1/models` 列表 API，客户端模型发现请求将返回 404。
- **计费与 [Token](../concepts/token.md)**：`/responses` 接口的 `usage` 字段返回详细 [Token](../concepts/token.md) 消耗（`input_tokens`, `output_tokens`, `reasoning_tokens`, `cached_tokens`），并按 `x_details` 分项计费。`/chat/completions` 和 DashScope 接口的计费逻辑类似，但字段名略有差异。
- **错误处理**：所有接口均返回标准 HTTP 状态码与 JSON 错误体。常见错误包括 `InvalidParameter`（如 Response ID 不存在）和 `400 Bad Request`（如传入不支持的参数）。务必检查响应状态码与 `error.type` 字段。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


