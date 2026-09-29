# use chat client or development tool

百炼平台支持通过标准 Chat API 接入各类第三方客户端与开发工具，开发者可复用现有工作流快速调用百炼模型。所有工具均基于 `v1/chat/completions` 接口协议，兼容 OpenAI SDK 及主流开源客户端。具体能力取决于所选模型与工具自身的功能边界，需结合 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中列出的工具清单按需选用。

## 支持的模型/功能

当前支持接入的客户端/工具覆盖通用对话、代码生成、办公辅助、多模态调用等场景，包括但不限于：OpenClaw（多模型路由）、Hermes Agent（自主任务编排）、Qwen Code（专注代码补全与解释）、Cursor（IDE 内嵌增强）、Dify（低代码应用编排）、Postman（API 快速调试）等。各工具对模型的支持存在差异，例如 QwenPaw 仅支持 `qwen-max` 和 `qwen-plus`，而 Codex 默认绑定 `qwen-turbo`；详细兼容性请参考 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 的子文档链接列表。

## 关键参数

调用时需确保以下参数正确配置：
- `model`: 必填，值必须为百炼平台已开通的模型 ID（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），不支持别名或旧版名称；
- `api_key`: 使用百炼控制台生成的 SK（Secret Key），**不可使用 AK/SK 对中的 Access Key**；
- `base_url`: 固定为 `https://dashscope.aliyuncs.com/compatible-mode/v1`（兼容模式）或 `https://dashscope.aliyuncs.com/api/v1`（原生模式），部分工具（如 Postman）需显式指定；
- `stream`: 布尔值，`true` 时启用流式响应，但部分工具（如早期版本 Cherry Studio）未完全适配流式解析，建议在 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 对应子文档中确认支持状态。

> **注意**：`qwen-coder` 模型已在 2024 年 Q3 下线，但部分子文档（如 `opencode.md`）仍提及该模型，属过时信息，请以控制台可用模型列表为准。

## 使用方式

1. 在百炼控制台开通目标模型并获取 API Key；
2. 根据所选工具文档配置 endpoint、model 和认证信息（多数工具提供“Aliyun DashScope”预设模板）；
3. 发起标准 Chat 请求，示例 payload：
   ```json
   {
     "model": "qwen-plus",
     "messages": [{"role": "user", "content": "你好"}],
     "temperature": 0.8
   }
   ```
4. 工具链集成参考各子文档（如 [原文标题](../../raw/model-user-guide/use-chat-client-or-development-tool.md) 中的 `cursor.md` 或 `dify.md`）。

## 限制和注意事项

- 单次请求 `messages` 长度上限为 32768 token（含 system/user/assistant 所有内容），超限将返回 `400 Bad Request`；
- 不支持 `function calling` 字段（即 OpenAI-style tools schema），所有工具需通过 [prompt](prompt.md) 工程实现工具调用逻辑；
- 部分工具（如早期 Kilo CLI v0.3.x）默认发送 `n=2` 参数，百炼不支持该参数，需手动移除，否则报错；
- 流式响应中 `delta.content` 可能为空字符串（尤其在首 chunk 含 role 或 finish_reason 时），客户端须健壮处理；
- 多模态请求（图像/视频）仅限特定工具（如 Postman）且需额外配置 `files` 字段，详见 `first-call-to-image-and-video-api.md` 子文档。

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


