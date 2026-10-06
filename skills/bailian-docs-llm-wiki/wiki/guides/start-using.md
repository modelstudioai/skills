# start using

本节介绍如何快速开始使用百炼平台构建 AI 应用，涵盖模型接入、核心参数配置、调用方式及常见约束。适用于希望快速验证能力或集成到生产环境的开发者。所有操作均基于百炼 API 与控制台双路径支持。

## 支持的模型/功能

当前平台默认提供 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类大语言模型，支持文本生成、知识库问答、[函数调用](../concepts/function-calling.md)（Function Calling）和多轮对话状态管理。图像理解（`qwen-vl`）与语音转文本（`qwen-audio`）需单独开通权限并申请配额。详细模型能力说明见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用 API 时必需指定 `model`（如 `"qwen-turbo"`）与 `input.messages`（非空数组，至少含 `role` 和 `content` 字段）。推荐设置 `temperature=0.7`（平衡确定性与多样性）和 `max_tokens=2048`（避免截断）。流式响应需显式传入 `stream=true`；若启用知识库增强，须在请求中携带 `retrieval_config` 对象。更多参数定义请参考 [开始使用](../../raw/application-user-guide/start-using.md) 中的参数速查表。

## 使用方式

1. **控制台快速体验**：登录百炼控制台 → 创建应用 → 选择模板（如“知识库问答”）→ 上传文档 → 点击“测试”即可交互；
2. **API 集成**：使用 `POST /v1/chat/completions` 接口，携带 `Authorization: Bearer <api_key>` 请求头；
3. **SDK 调用**：Python SDK 示例见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)，支持一键部署知识库应用。

> **注意**：原始文档中 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 提到 v2.3.0 版本已支持异步批量推理，但当前 API 文档未同步更新该接口路径与字段，建议以控制台「任务中心」或 `/v1/batch/jobs`（需白名单）为准。

## 限制和注意事项

- 免费试用期为开通后 30 天，每日调用上限 1000 次（按 `model` 分桶计费）；
- 单次请求 `input.messages` 总长度不得超过 32768 token（`qwen-max`）或 8192 token（`qwen-turbo`），超长将被静默截断；
- 知识库检索结果默认返回 Top5，不可通过 `top_k` 参数覆盖（该参数在 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中被错误标注为可配置，实际无效）；
- 所有请求必须携带 `X-DashScope-SSE: enable` 头才能接收 Server-Sent Events 流式响应。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


