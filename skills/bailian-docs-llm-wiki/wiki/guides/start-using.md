# start using

本页面介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。适用于希望快速集成大模型能力的开发者，无需从零搭建基础设施。所有操作均基于百炼控制台或 API 接口完成。

## 支持的模型/功能

百炼平台当前支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL 多模态模型，以及部分开源模型的托管推理服务。应用层提供知识库问答、工作流编排、Agent 能力封装等开箱即用功能。详细模型列表与能力说明见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用模型时需指定 `model`（如 `qwen-max`、`qwen-plus`）、`input`（结构化输入，含 `messages` 或 `prompt` 字段）及可选参数 `temperature`、`top_p`、`max_tokens`。对于知识库问答类应用，还需传入 `knowledge_id` 和 `retrieval_config`。参数规范以 [开始使用](../../raw/application-user-guide/start-using.md) 中定义为准；注意 `stream` 参数在 v2.3+ API 中默认为 `false`，旧文档中未明确该默认值，> **注意**：请以 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的最新示例代码为准，避免因版本差异导致流式响应行为不一致。

## 使用方式

1. 登录百炼控制台 → 创建应用 → 选择模板（如“知识库问答”）或自定义工作流  
2. 配置模型与插件（如向量库、HTTP 工具）  
3. 通过 SDK（Python/Java/Go）或 REST API 调用 `/v1/chat/completions` 等标准接口  
4. 应用发布后获取 `app_id`，用于生产环境调用。完整流程参见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- 免费额度仅限新用户首月，调用量超限后需绑定支付方式  
- 知识库上传文件单次不超过 100MB，总容量上限取决于所选套餐  
- 模型输出长度受 `max_tokens` 和模型自身 context 长度双重限制（例如 Qwen3 最大 context 为 32768 tokens）  
- 应用配置变更（如模型切换）需重新发布才生效，未发布的草稿不对外提供服务  
- 历史文档中提及的“实时调试沙箱”功能已在 v2.4 版本移除，当前调试需依赖日志与 Trace 分析，详见 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


