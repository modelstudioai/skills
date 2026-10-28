# qwen api reference

阿里云百炼平台提供多种 API 接口协议（OpenAI 兼容、Anthropic 兼容、DashScope 原生）调用 Qwen 系列大模型，支持文本、多模态、工具调用等能力。开发者可根据现有技术栈选择适配路径，所有接口均基于业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`）提供高性能、高稳定性服务。

## 支持的模型/功能

Qwen API 支持全系列千问模型及主流第三方模型，但不同协议接口支持的模型范围存在差异：

- **OpenAI 兼容 Chat API**（[OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.5-flash`、`Qwen-VL`、`Qwen-Omni`、`Qwen-Math`、`DeepSeek`（硅基流动/快手万擎直供）、`Kimi`、`GLM`、`MiniMax` 等；但明确注明 **Qwen-Audio 不支持 OpenAI 兼容协议**，仅支持 DashScope 协议。
- **OpenAI 兼容 Responses API**（[创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）聚焦 Agent 场景，支持 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4.1-flash-1017`、`glm-5.3` 等，并内置联网搜索、网页抓取、代码解释器等工具；非列表中模型仅支持基础文本生成，Agent 能力受限。
- **Anthropic 兼容 Messages API**（[Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3-vl-plus`、`qwen3-coder-flash` 及 `deepseek-v4-pro`、`glm-5.2`、`kimi-k3` 等，提供深度思考（`effort`）、结构化输出（`format`）等扩展能力。
- **DashScope 原生 API**（[DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)）是底层协议，支持最广模型集，包括 `Qwen-Audio`、`Qwen-Coder`、数学模型等，且对视频帧数控制（`max_frames`）等参数支持更完整。

> **注意**：文档 1 和文档 8 对 `min_pixels` 默认值描述存在不一致。文档 1 中 `Qwen3.7` 图像输入默认值为 `65536`，而文档 8 同样列出 `Qwen3.7` 但未明确其默认值；文档 8 明确 `qwen3-vl-plus` 视频输入 `max_frames` 默认值为 2000，而文档 1 的 OpenAI Chat API 完全未提及 `max_frames` 参数——该参数**仅 DashScope 原生 API 支持**。

## 关键参数

核心参数按协议分层，需严格匹配协议规范：

- **通用必选参数**：`model`（字符串，如 `"qwen3.7-plus"`）、`messages`（Chat/DashScope）或 `input`（Responses）或 `system`+`messages`（Anthropic）。
- **多模态控制**：
  - `fps`：控制视频抽帧频率（取值 `[0.1, 10]`），在 OpenAI Chat、Responses、Anthropic、DashScope 四类接口中均支持，但 Anthropic 文档未说明其时间动态语义。
  - `min_pixels` / `max_pixels` / `total_pixels`：图像/视频分辨率控制，**OpenAI Chat API 文档 1 提供最完整取值表**（含各模型系列的默认值与范围），DashScope 文档 8 仅覆盖部分模型。
  - `max_frames`：**仅 DashScope 原生 API 支持**（文档 8），用于硬性限制视频总帧数，OpenAI/Anthropic 接口无此参数。
- **Agent 与推理增强**：
  - `tools`：Responses API 和 Anthropic API 均支持，但内置工具集不同：Responses 内置 `web_search`/`web_extractor`/`code_interpreter`；Anthropic 需显式声明 `web_search_20250305` 类型工具且依赖 `x-anthropic-billing-header` 头。
  - `reasoning.effort`（Responses）与 `output_config.effort`（Anthropic）：均为控制思考强度的参数，但取值枚举和映射规则不同（如 `qwen3.8-max` 在 Responses 中无此字段，在 Anthropic 中支持 `xhigh`/`medium`/`low`）。
- **流式与缓存**：`stream`（布尔值）、`cache_control`（`{"type": "ephemeral"}`）在三类协议中语义一致；`x-dashscope-session-cache: enable` 为 Responses API 特有请求头。

## 使用方式

所有接口均需配置业务空间专属域名与 API Key：

- **域名格式**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 为控制台业务空间 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1` 等。旧域名（如 `dashscope.aliyuncs.com`）仍可用，但**强烈建议迁移至新域名以获得更高性能与稳定性**（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md) 和 [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)）。
- **协议路由**：
  - OpenAI Chat：`/compatible-mode/v1/chat/completions`
  - OpenAI Responses：`/compatible-mode/v1/responses`（新版路径，旧版 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停用）
  - Anthropic Messages：`/apps/anthropic/v1/messages`
  - DashScope：`/api/v1/services/aigc/text-generation/generation`（文本）或 `/multimodal-generation/generation`（多模态）
- **SDK 配置**：
  - OpenAI SDK：设置 `base_url` 为业务空间域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）
  - DashScope SDK：设置 `workspace` 和 `region`（如 `workspace="{WorkspaceId}", region="cn-beijing"`）
  - Anthropic SDK：设置 `base_url` 为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic`

## 限制和注意事项

- **地域可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站华北2（北京）地域可用**，且需在控制台手动开通（见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)）。
- **上下文长度**：Responses API 为预留工具调用空间，**最大输入上下文约为模型窗口大小的 80%**，超出部分自动截断（见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)）；Chat API 无此显式说明，但实际受模型窗口限制。
- **参数兼容性**：[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**忽略未文档化的 OpenAI 参数**（如 `background`），且 Responses API 明确不支持异步执行（`background` 固定为 `false`）；Anthropic 兼容接口 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校验。
- **响应管理**：Responses API 提供完整的生命周期操作——创建（`POST /responses`）、获取（`GET /responses/{id}`）、删除（`DELETE /responses/{id}`）、查询输入项（`GET /responses/{id}/input_items`），所有操作均要求 `store=true`（见 [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md) 和 [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)）。

## 来源文档

- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


