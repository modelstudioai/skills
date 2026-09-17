# use chat client or development tool

百炼平台支持通过标准 Chat API 接入各类第三方客户端与开发工具，适用于快速原型验证、本地 IDE 集成及低代码工作流编排。所有工具均基于统一的 `/v1/chat/completions` 接口协议，无需定制适配即可调用百炼托管的[多模态](../concepts/multi-modal.md)与代码大模型。详细配置方式和兼容性说明请参考 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 支持的模型与功能

当前支持的客户端覆盖通用对话、代码生成、办公协同、Agent 编排四类场景，典型工具包括：
- **IDE 增强类**：Cursor、Qwen Code、Claude Code、Qoder、Cherry Studio  
- **轻量 CLI 工具**：Kilo CLI、Cline、OpenClaw  
- **Agent 框架**：Hermes Agent、DeepSeek Harness、Qoder CN（原 Lingma）  
- **低代码平台**：Dify、Postman（仅限图像/视频 API 调用）、Chatbox  

所有工具均可调用百炼平台上的 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen-vl` 等模型，但[多模态](../concepts/multi-modal.md)输入（如图像、视频）需显式启用 `enable_multimodal=true` 参数，并仅在 [Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 和 Cherry Studio 等少数工具中完整支持。具体模型能力边界详见 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 关键参数

调用时必须设置以下请求头与参数：

| 字段 | 必填 | 说明 |
|------|------|------|
| `Authorization: Bearer <api_key>` | 是 | 百炼平台申请的 API Key，非阿里云主账号 AK/SK |
| `Content-Type: application/json` | 是 | 不支持 `application/x-www-form-urlencoded` |
| `model` | 是 | 必须为平台已开通的模型名（如 `"qwen-plus"`），不支持别名或通配符 |
| `stream` | 否 | 默认 `false`；设为 `true` 时需按 SSE 格式解析响应流 |
| `enable_multimodal` | 否 | [多模态](../concepts/multi-modal.md)输入必需，且仅对 `qwen-vl`、`qwen2-vl` 生效；该参数未在 [QwenPaw](../../raw/model-user-guide/use-chat-client-or-development-tool/qwenpaw.md) 文档中声明，实际调用会静默忽略 —— > **注意**：QwenPaw 当前不支持多模态，文档未同步更新 |

## 使用方式

1. 在百炼控制台「API 密钥管理」中创建并复制有效 API Key  
2. 根据目标工具文档配置 Base URL 为 `https://dashscope.aliyuncs.com/api/v1`  
3. 将模型名、消息数组（`messages`）及必要参数写入请求体  
4. 发起 POST 请求，验证响应状态码为 `200` 且含 `choices[0].message.content`  

各工具的具体配置示例见对应子文档，例如 [Hermes Agent](../../raw/model-user-guide/use-chat-client-or-development-tool/hermes-agent.md) 的 YAML 配置片段、[Codex](../../raw/model-user-guide/use-chat-client-or-development-tool/codex.md) 的 VS Code [插件](../concepts/plugin.md)设置项等。完整工具列表与入口链接汇总于 [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)。

## 限制和注意事项

- 单次请求 `messages` 总 token 数上限为 32768（`qwen-max`）或 8192（`qwen-turbo`），超限将返回 `400 Bad Request`  
- 所有工具均**不支持**自定义 system [prompt](prompt.md) 的 `role: "system"` 消息（除 Dify、Hermes Agent 等明确声明支持的框架外）  
- Postman 仅可用于调用图像/视频类 API（如 `/v1/images/generations`），其 Chat API 示例已过时 —— > **注意**：[Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md) 文档标题与内容存在偏差，实际不涵盖 Chat 接口调用流程  
- 免费试用额度仅适用于首次调用的模型实例，切换模型需重新申请配额  
- Qoder CN（原 Lingma）与 Qoder Agent 为同一工具的不同命名，配置方式一致，但后者文档更新更及时

## 来源文档

- [接入客户端/开发工具](../../raw/model-user-guide/use-chat-client-or-development-tool.md)


