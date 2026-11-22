# qwen api reference

阿里云百炼平台提供多种 API 协议兼容的 Qwen 模型调用方式，包括 OpenAI 兼容、Anthropic 兼容和原生 DashScope 协议。开发者可根据现有技术栈选择最适配的接口，所有协议均支持主流 Qwen 系列模型（如 `qwen4-max`、`qwen3.8-plus`、`qwen3-vl-plus` 等）及部分第三方模型。统一采用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障性能与稳定性。

## 支持的模型/功能

Qwen API 支持三类核心调用协议，覆盖不同场景需求：

- **OpenAI 兼容 Chat API**：适用于标准对话场景，路径为 `/compatible-mode/v1/chat/completions`，支持 `messages` 数组输入、系统角色、[多模态](../concepts/multi-modal.md)（图像/视频/音频）及 `reasoning.effort` 思考强度控制。但需注意：**Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议**，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **OpenAI 兼容 Responses API**：面向复杂 Agent 场景，路径为 `/compatible-mode/v1/responses`，内置联网搜索、代码解释器、知识库检索等工具，支持 `previous_response_id` 多轮串联与 `x-dashscope-session-cache: enable` 自动会话缓存。其输入格式更灵活（支持纯字符串或结构化消息），但**最大输入上下文约为模型窗口的 80%（预留缓冲区），超出部分将自动截断**，详见 [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。
- **Anthropic 兼容 Messages API**：路径为 `/apps/anthropic/v1/messages`，支持 `system` 字段、`tool_use`/`tool_result` 结构化工具交互及 `thinking` 深度推理模式。注意 `temperature` 取值范围为 `[0, 2)`，与 Anthropic 官方 `[0.0, 1.0]` 不同，迁移时需校准。
- **DashScope 原生 API**：路径为 `/api/v1/services/aigc/{text-generation|multimodal-generation}/generation`，是底层协议，对[多模态](../concepts/multi-modal.md)（如 `video`、`image`）支持最完整，且明确区分文本模型与[多模态](../concepts/multi-modal.md)模型的 endpoint。例如，`qwen3.7-plus` 在 DashScope 中需根据输入类型选择对应服务路径。

> **注意**：文档 2（OpenAI兼容-Chat）与文档 8（DashScope API 参考）在 `detail` 和 `max_pixels` 参数的嵌套层级上存在不一致描述：前者要求 `detail` 在 `image_url` 对象内，后者要求与 `image` 同级；实际行为以 [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md) 的 `image` 字段说明为准，OpenAI 兼容层存在兼容性映射逻辑。

## 关键参数

所有协议共用的核心参数如下（具体行为因协议而异）：

- **`model`**（必选）：模型 ID。OpenAI 兼容 Chat 支持 `Qwen-VL`、`Qwen-Coder`、`DeepSeek` 等广泛列表；Responses API 仅支持明确列出的 Qwen 商业版模型（如 `qwen4-max`、`qwen3.8-flash`）及部分第三方模型，非列表模型 Agent 能力受限；Anthropic 兼容则聚焦 `qwen4-max`、`qwen3.7-plus` 等 Max/Plus/Flash 系列。
- **`messages` / `input` / `content`**（必选）：输入内容。OpenAI Chat 使用 `messages` 数组（含 `role`/`content`）；Responses API 支持 `string` 或 `array`（含 `EasyInputMessage` 结构）；Anthropic Messages 使用 `messages` 数组（`content` 可为 `text`/`image`/`video`/`document` 等类型）；DashScope 原生需将 `messages` 封装在 `input` 对象中。
- **多模态参数**：
  - 图像：`image_url.url`（OpenAI Chat）、`image`（DashScope）、`source.type=url/data`（Anthropic）；`detail`（精度）、`min_pixels`/`max_pixels`（像素阈值）均受模型版本约束。
  - 视频：`video_url.url` 或 `video` 数组（OpenAI Chat）；`video` 字符串或数组（DashScope）；`type=video` + `source`（Anthropic）；`fps`（抽帧率）和 `max_frames`（帧数上限）为 DashScope 特有参数，OpenAI 兼容层不支持自定义 `max_frames`。
- **推理控制**：
  - `temperature`：取值 `[0, 2)`，所有协议一致。
  - `reasoning.effort`（Responses API）或 `thinking.type`（Anthropic）：控制思考强度，`qwen4-max` 等模型默认开启。
  - `max_tokens`：Anthropic 兼容中，对 `qwen4-max` 表示“回复+思考”总长度；其他协议中通常仅限制回复长度。

## 使用方式

1. **认证与域名**：  
   - 获取 API Key 并配置环境变量（如 `DASHSCOPE_API_KEY`）或 SDK 初始化参数。  
   - **必须使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 等，`{WorkspaceId}` 从控制台获取。旧域名（如 `dashscope.aliyuncs.com`）仍可用但不推荐，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

2. **协议选择与调用示例**：  
   - **OpenAI Chat**（推荐快速迁移）：  
     ```python
     from openai import OpenAI
     client = OpenAI(
         api_key=os.getenv("DASHSCOPE_API_KEY"),
         base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
     )
     response = client.chat.completions.create(
         model="qwen3.8-max",
         messages=[{"role": "user", "content": "你好"}]
     )
     ```
   - **OpenAI Responses**（推荐 Agent 开发）：  
     ```python
     response = client.responses.create(
         model="qwen4-max",
         input="分析这份财报",
         tools=[{"type": "file_search"}],
         store=True  # 启用存储以便后续 retrieve
     )
     # 后续可调用 client.responses.retrieve("resp_xxx")
     ```
   - **DashScope 原生**（推荐精细控制）：  
     ```python
     import dashscope
     client = dashscope.Client(
         api_key=os.getenv("DASHSCOPE_API_KEY"),
         workspace="{WorkspaceId}",
         region="cn-beijing"
     )
     response = client.multimodal_generation.call(
         model="qwen3-vl-plus",
         input={"messages": [{"role": "user", "content": [{"image": "https://x.jpg"}]}]}
     )
     ```

3. **辅助操作**：  
   - **获取响应**：`GET /compatible-mode/v1/responses/{response_id}`（需 `store=true`）。  
   - **获取输入项列表**：`GET /compatible-mode/v1/responses/{response_id}/input_items`，用于审计多轮对话历史。  
   - **删除响应**：`DELETE /compatible-mode/v1/responses/{response_id}`，仅限已存储响应。

## 限制和注意事项

- **地域与模型可用性**：三方直供模型（如 SiliconFlow DeepSeek、月之暗面 Kimi）**仅在中国站的华北2（北京）地域可用**，且需在控制台手动开通服务，详见 [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。
- **协议差异与弃用项**：  
  - Responses API **不支持 OpenAI 的 `background` 异步参数**，仅同步调用。  
  - Anthropic 兼容的 `thinking.budget_tokens` 参数**即将废弃**，新接入应使用 `output_config.effort` 或 `thinking.type`。  
  - OpenAI 兼容 Responses API 的旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已停止维护，**必须迁移至 `/compatible-mode/v1/responses`**。
- **缓存与性能**：  
  - Session 缓存（`x-dashscope-session-cache: enable`）可显著降低多轮延迟，但需确保请求头正确设置。  
  - 显式缓存（`prompt_cache_breakpoint` 或 `cache_control`）仅 `qwen4-max` 全面支持，其他模型效果有限。
- **错误处理**：`response_id` 相关操作（retrieve/list/delete）均要求原请求中 `store=true`，否则返回 `Response not found` 错误。

## 来源文档

- [OpenAI兼容-Responses](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses.md)
- [OpenAI兼容-Chat](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
- [创建响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
- [获取响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/retrieve-a-response.md)
- [获取输入项列表](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/list-input-items.md)
- [删除响应](../../raw/model-api-reference/qwen-api-reference/openai-compatible-responses/delete-a-response.md)
- [Anthropic兼容-Messages](../../raw/model-api-reference/qwen-api-reference/anthropic-api-messages.md)
- [DashScope API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)


