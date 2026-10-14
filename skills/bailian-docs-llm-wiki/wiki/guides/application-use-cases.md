# application [use cases](use-cases.md)

本页面汇总百炼平台在实际业务场景中的典型应用模式，涵盖轻量级嵌入式助手、企业通讯工具集成、以及基于私有知识的检索增强生成（RAG）等高频用例。所有用例均基于标准 API 或低代码配置实现，无需训练模型。开发者可直接复用对应模板或参考 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中的分步指南快速落地。

## 支持的模型/功能

- 支持调用百炼平台全部公开模型（如 Qwen 系列、Qwen2-VL、Qwen2-Audio）及用户自部署模型，用于文本生成、多模态理解、语音转写等任务  
- 提供开箱即用的「AI助手」组件，支持对话状态管理、流式响应、历史上下文自动截断  
- RAG 场景下，支持对接向量数据库（如 Milvus、PGVector）与非结构化文档解析（PDF/Word/Excel），相关能力详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)  

## 关键参数

- `model_id`：必需，指定模型标识符（如 `qwen-max`, `qwen2-72b`）  
- `enable_search`：布尔值，启用后自动触发知识库检索（仅 RAG 应用有效）  
- `max_tokens` / `temperature`：通用生成参数，行为与 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中描述一致  
- `system_prompt`：支持动态注入，但长度上限为 4096 字符；超出部分将被静默截断（参见 [在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 的兼容性说明）

## 使用方式

- **嵌入式助手**：通过 SDK（Python/JS）或 iframe 方式集成，适用于官网、后台系统等 Web 场景  
- **IM 工具集成**：使用平台提供的企业微信/钉钉/微信公众号适配器，需配置 Webhook 回调地址与消息加解密密钥  
- **RAG 应用**：先上传文档并完成向量化索引，再通过 `/v1/chat/completions` 接口传入 `enable_search=true` 触发检索，完整流程见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)  

## 限制和注意事项

- 单次请求最大输入 tokens 为 32768（Qwen2 系列模型），超出将返回 `400 Bad Request`；该限制与 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中旧版文档描述的 8192 不符  
> **注意**：`max_input_tokens` 参数在 v2.3+ 版本已废弃，实际限制由所选模型决定，请以 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中最新链接为准  
- 所有 IM 集成场景均不支持上传文件作为输入（如用户发送 PDF），仅支持文本消息触发；若需文件处理，须额外调用 `/v1/files/upload` 接口预处理  
- RAG 检索结果默认最多返回 5 个 chunk，不可配置；如需调整，需改用底层 `retrieval` API 而非助手封装接口

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


