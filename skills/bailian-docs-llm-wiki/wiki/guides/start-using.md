# start using

本文档介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。开发者可通过控制台或 API 快速接入，无需从零搭建基础设施。所有操作均基于百炼统一的模型服务与应用框架 [开始使用](../../raw/application-user-guide/start-using.md)。

## 支持的模型/功能

- 当前支持 Qwen 系列大语言模型（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL 多模态模型及 Qwen-Audio；部分模型需申请开通权限。
- 应用层提供开箱即用的能力：知识库问答、Agent 工作流、RAG 增强检索、多轮对话管理。具体功能演进详见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)。
- 0 代码构建能力仅限控制台「应用构建」模块，支持拖拽式编排知识库+LLM+提示词链路，详细流程见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 关键参数

- `model`: 必填，取值如 `qwen-max`、`qwen-plus`、`qwen-turbo`，区分推理性能与成本；不支持传入未在控制台已授权列表中的模型 ID。
- `input.messages`: 至少包含一个 `role: user` 的消息对象；系统提示词（system [prompt](prompt.md)）需显式传入，不可依赖模型内置默认行为。
- `parameters.temperature`: 范围 0.0–1.0，默认 0.8；设为 0 时启用确定性解码（top_k=1），但部分模型（如 qwen-max）在 temperature=0 下可能返回空响应 —> **注意**：该行为与 [开始使用](../../raw/application-user-guide/start-using.md) 中“默认参数稳定可靠”的描述存在偏差，建议生产环境显式设置 `temperature=0.1` 并配合 `top_p=0.95` 使用。

## 使用方式

1. **API 调用**：通过 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 发起请求，需携带 `Authorization: Bearer <api_key>` 及正确 `Content-Type: application/json`。
2. **SDK 调用**：推荐使用 `dashscope==1.20.0+` 版本，初始化时指定 `api_key` 和 `model`，调用 `Generation.call()` 即可。
3. **控制台快速验证**：登录百炼控制台 → 进入「模型服务」→ 选择模型 → 在「调试」页填写输入并执行，结果实时返回；该流程与 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中的调试入口一致。

## 限制和注意事项

- 单次请求 `input.messages` 总长度上限为 32768 token（含 system + user + assistant 消息），超长将触发 `400 Bad Request`。
- 免费额度仅覆盖 `qwen-turbo` 和 `qwen-plus` 的基础调用量，`qwen-max` 及多模态模型需单独开通配额；配额策略以控制台「用量管理」页实时显示为准。
- 所有请求必须携带 `X-DashScope-Source: aliyun` 标头（SDK 自动注入，手动调用需显式添加），否则返回 `403 Forbidden` —> **注意**：该要求未在 [开始使用](../../raw/application-user-guide/start-using.md) 中明确说明，属近期安全策略更新，务必检查请求头完整性。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


