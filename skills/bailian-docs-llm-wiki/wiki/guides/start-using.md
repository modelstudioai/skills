# start using

本节介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。开发者可选择零代码方式快速搭建问答应用，或通过 API 集成模型服务。所有操作均需完成账号认证与项目初始化。

## 支持的模型/功能

当前平台支持通义千问系列大模型（Qwen1、Qwen2、Qwen2.5、Qwen3）、多模态模型（Qwen-VL、Qwen-Audio）及专属微调模型。应用层提供知识库问答、工作流编排、Agent 能力扩展等模块。详细模型列表与能力说明见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用模型时需指定 `model`（如 `qwen-max`）、`input`（含 `messages` 或 `prompt` 字段）、`parameters`（如 `temperature`、`top_p`、`max_tokens`）。知识库问答类应用还需传入 `knowledge_id` 和 `retrieval_config`。参数默认值与取值范围请参考 [开始使用](../../raw/application-user-guide/start-using.md) 中的接口规范章节。

## 使用方式

- **零代码方式**：通过控制台「创建应用」→「知识库问答」向导，上传文档并配置检索策略，5 分钟内即可发布 Web 应用。该流程详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **API 方式**：使用 `POST /v1/chat/completions` 接口，携带 `Authorization: Bearer <api_key>` 请求头。注意 `api_key` 须在「API 密钥管理」中生成，且仅对已授权项目生效。  
- **SDK 集成**：推荐使用官方 Python SDK（`dashscope` >= 1.20.0），初始化时需显式传入 `api_key` 和 `base_url`（国内环境建议设为 `https://dashscope.aliyuncs.com/api/v1`）。> **注意**：部分旧版文档仍引用已废弃的 `https://api-dashscope.aliyuncs.com` 域名，实际调用请以 [开始使用](../../raw/application-user-guide/start-using.md) 中最新 endpoint 列表为准。

## 限制和注意事项

- 免费额度按自然月重置，超出后需绑定支付方式；单次请求 `max_tokens` 上限为 8192（Qwen3 系列为 32768）。  
- 知识库上传文件单个不超过 100MB，格式支持 PDF/DOCX/TXT/MD/CSV；图片类文件需经 OCR 后方可参与检索。  
- 所有 API 请求必须携带 `x-dashscope-source` 标头（值为 `console` 或 `sdk`），否则返回 400 错误。该要求在 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的调试日志说明中有明确体现，但未在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中同步更新，开发者需以实际接口响应为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


