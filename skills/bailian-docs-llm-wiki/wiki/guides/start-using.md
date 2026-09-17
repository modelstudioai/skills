# start using

本页面介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。开发者可基于平台提供的 API 或低代码界面快速集成大模型能力。所有操作均需先完成[身份认证与项目初始化](../../raw/application-user-guide/start-using.md)。

## 支持的模型/功能

当前平台默认提供 `qwen-max`、`qwen-plus` 和 `qwen-turbo` 三类推理模型，覆盖高精度、均衡型与低成本场景；同时支持知识库问答、工作流编排、RAG 增强检索等应用级功能。具体模型能力详见 [开始使用](../../raw/application-user-guide/start-using.md) 中的“可用模型列表”章节。知识库问答助手的零代码构建流程在 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中有完整演示。

## 关键参数

调用模型 API 时，必需参数包括 `model`（字符串，如 `"qwen-turbo"`）、`input.messages`（非空消息数组）；推荐设置 `temperature`（0.1–1.0）、`max_tokens`（默认 2048，上限 8192）。注意：`top_p` 与 `temperature` 不建议同时设为极值（如 `temperature=0` 且 `top_p=0.1`），否则可能触发服务端校验拒绝 —— 此限制在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的 v2024.06 版本说明中已明确。

> **注意**：原始文档 [开始使用](../../raw/application-user-guide/start-using.md) 中提及的 `stream=true` 默认启用流式响应，但实际 API 文档（v2024.07）要求显式传入该字段才生效，旧示例代码存在过时风险。

## 使用方式

- **API 方式**：发送 POST 请求至 `/v1/chat/completions`，携带 `Authorization: Bearer <api_key>` 和 JSON body  
- **低代码方式**：进入控制台 → 创建应用 → 选择“知识库问答”模板 → 上传文档并发布，全程无需编码，流程见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)  
- **SDK 调用**：推荐使用 `dashscope` Python SDK（>=1.15.0），初始化时指定 `api_key` 和 `base_url`（国内用户需设为 `https://dashscope.aliyuncs.com/api/v1`）

## 限制和注意事项

- 单次请求 `input.messages` 最多 10 条，总 token 数不超过模型上下文长度（`qwen-turbo` 为 8192）  
- 知识库上传文件单个 ≤ 100 MB，格式仅支持 PDF/TXT/DOCX/MD/CSV/XLSX  
- 免费额度按自然月重置，超出后按用量计费；详细配额规则参见 [开始使用](../../raw/application-user-guide/start-using.md) 附录  
- 所有请求必须携带有效 `api_key`，未授权访问返回 `401 Unauthorized`，不支持匿名试用

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


