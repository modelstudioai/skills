# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可快速集成大模型能力或零代码搭建业务应用。本文档梳理核心使用路径、参数规范及约束条件，帮助开发者高效上手。所有功能均基于 [开始使用](../../raw/application-user-guide/start-using.md) 文档定义的基础流程展开。

## 支持的模型/功能

- 支持调用通义千问系列（Qwen1、Qwen2、Qwen2.5、Qwen3）及百炼专属微调模型（如 `qwen-max`、`qwen-plus`）
- 提供两类使用模式：  
  - **API 调用**：通过 RESTful 接口直接请求模型（见 [开始使用](../../raw/application-user-guide/start-using.md)）  
  - **零代码应用构建**：基于知识库快速搭建问答助手，无需开发即可发布（详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)）

> **注意**：[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中提及的“实时流式对话增强”功能在 v2.3.0 后已默认启用，但部分旧版 SDK 尚未同步该行为，建议升级至最新版 client SDK 或显式设置 `stream=true`。

## 关键参数

调用 API 时必需或强推荐的参数包括：

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `model` | string | 是 | 模型 ID，必须为平台支持的合法值（如 `qwen-max`），不支持自定义别名 |
| `input.messages` | array | 是 | 至少包含一条 `user` 角色消息；系统提示词需显式传入 `system` 消息，不可省略 |
| `parameters.temperature` | number | 否（默认 0.8） | 控制输出随机性，取值范围 [0.0, 2.0]；生产环境建议 ≤1.0 |
| `parameters.top_p` | number | 否（默认 0.95） | 核采样阈值，与 `temperature` 互斥生效，二者同时设置时以 `top_p` 为准 |

## 使用方式

1. **获取 API Key**：在控制台「API 密钥管理」中创建并复制密钥（权限需包含 `model:Invoke`）  
2. **发起请求**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 发送 POST 请求，Header 中携带 `Authorization: Bearer <api_key>`  
3. **解析响应**：检查 `output.choices[0].message.content` 字段获取结果；流式响应需按 SSE 协议解析 `data:` 行（参考 [开始使用](../../raw/application-user-guide/start-using.md) 的示例代码）  

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 32768 token（含 system + user + assistant 消息），超限将返回 `400 Bad Request`  
- 免费试用额度仅限新用户首次开通后 30 天内使用，过期后需绑定支付方式（具体规则见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 附录）  
- 知识库问答应用不支持上传 `.exe`、`.bin` 等可执行文件，且单文件上限为 100 MB；该限制在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中未更新，仍以当前控制台实际校验逻辑为准

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


