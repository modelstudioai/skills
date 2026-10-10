# start using

本节介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。开发者可选择零代码方式快速搭建问答应用，或通过 API 集成模型服务。所有操作均需完成实名认证与项目初始化。

## 支持的模型/功能

当前平台支持通义千问系列大语言模型（如 Qwen2.5-7B、Qwen2.5-72B）、多模态模型（Qwen-VL）及语音合成模型（Qwen-Audio）。应用层提供知识库问答、工作流编排、Agent 能力等开箱即用功能。详细模型列表与能力说明见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用模型时需指定 `model`（必填，如 `"qwen2.5-7b-chat"`）、`input`（含 `messages` 或 `prompt` 字段）和 `parameters`（可选，支持 `temperature`、`top_p`、`max_tokens` 等）。API 请求需携带 `Authorization: Bearer <api_key>` 头。参数约束详见 [开始使用](../../raw/application-user-guide/start-using.md) 中的接口规范章节。

## 使用方式

- **零代码方式**：通过控制台「创建应用」→「知识库问答」向导，上传文档并配置检索策略，5 分钟内发布可访问的 Web 应用；该流程完整说明见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。  
- **代码方式**：调用 `/v1/chat/completions` 接口，参考 Python SDK 示例（需安装 `dashscope` >= 1.18.0）。注意 v1.17.x 版本存在 streaming 响应解析兼容性问题，建议升级 —> **注意**：该限制在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的 2024-Q3 更新日志中已明确标注，但部分旧版文档未同步更新。

## 限制和注意事项

- 免费试用额度为每月 100 万 tokens，超出后需绑定支付方式；  
- 知识库上传单文件上限 100 MB，仅支持 PDF/DOCX/TXT/MD 格式；  
- 模型输出长度受 `max_tokens` 和模型自身 context 长度双重限制（例如 Qwen2.5-7B 最大 context 为 32768 tokens）；  
- 所有 API 调用需在项目（Project）上下文中进行，未指定 `project_id` 将默认使用个人默认项目 —> **注意**：该行为与 [开始使用](../../raw/application-user-guide/start-using.md) 中“多项目隔离”章节描述一致，但部分控制台引导页仍显示旧版“全局 token”提示，属界面文案滞后，以 API 行为为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


