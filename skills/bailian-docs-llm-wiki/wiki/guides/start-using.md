# start using

百炼平台提供零代码与低代码两种方式快速启动 AI 应用开发，支持从知识库问答构建到模型 API 调用的完整链路。开发者可基于预置模板快速部署应用，或通过 SDK/API 集成自定义逻辑。所有能力均统一接入百炼控制台进行管理与监控。

## 支持的模型/功能

- 内置支持 Qwen 系列大模型（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等[多模态](../concepts/multi-modal.md)模型  
- 提供开箱即用的「知识库问答助手」、「智能客服对话流」、「文档摘要提取」等应用模板  
- 支持动态功能更新，新模型与插件能力随 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 实时同步  

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-max`, `qwen-plus`, `qwen-turbo`），需与当前账号开通权限匹配  
- `input`: 结构化输入，文本类任务为 `{"messages": [...]}`，[多模态](../concepts/multi-modal.md)任务需包含 `image_url` 或 `audio_url` 字段  
- `parameters.temperature`: 取值范围 0.0–2.0，默认 0.8；生成确定性高时建议设为 0.0–0.3  
- `stream`: 布尔值，启用流式响应需显式设为 `true`，否则默认返回完整 JSON 响应  

## 使用方式

1. **零代码方式**：登录百炼控制台 →「应用构建」→ 选择「知识库问答助手」模板 → 上传文档并发布，全程无需编码，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)  
2. **API 方式**：调用 `/v1/chat/completions` 接口，使用 `Authorization: Bearer <api_key>` 认证，请求体需符合 OpenAI 兼容格式  
3. **SDK 方式**：安装 `dashscope` Python SDK（≥1.20.0），初始化 `DashScopeClient(api_key=...)` 后调用 `chat.completions.create()`  

> **注意**：原始文档中提及的 `qwen-7b-chat` 模型已下线，当前控制台与 API 均不再支持该 ID；请以 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中最新支持列表为准。

## 限制和注意事项

- 免费试用额度仅限新注册用户首 30 天，调用次数与 [Token](../concepts/token.md) 总量受配额限制（可在控制台「配额管理」查看）  
- 知识库问答应用单次上传文档上限为 100MB，总容量上限 10GB（企业版可扩展）  
- 流式响应不支持 `function calling`，若需工具调用请关闭 `stream` 参数  
- 所有请求必须携带有效 `api_key`，且 `model` 必须在当前项目已授权模型列表中，否则返回 `403 Forbidden`；授权状态请以 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中的权限说明为依据

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


