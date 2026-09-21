# application [use cases](use-cases.md)

本节汇总百炼平台在实际业务场景中的典型应用模式，涵盖轻量级嵌入式助手、企业通讯工具集成、以及基于私有知识的[检索增强生成](../concepts/rag.md)（RAG）等落地路径。所有用例均基于平台提供的标准 API 和 SDK 实现，无需训练模型即可快速部署。详细操作步骤请参考 [实践教程](../../raw/application-user-guide/application-use-cases.md)。

## 支持的模型/功能

- 支持调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全系列 Qwen 模型，适用于不同响应速度与推理精度要求的场景  
- 提供开箱即用的对话管理能力（含历史上下文维护、[流式输出](../concepts/streaming.md)、中断控制）  
- 内置 RAG 基础设施：支持上传 PDF/Word/TXT 等格式文档，自动完成分块、向量化与检索索引构建  
- 企业级通道集成能力：原生适配企业微信、钉钉、微信公众号等平台的消息协议与鉴权机制  
- 更多模型能力细节见 [实践教程](../../raw/application-user-guide/application-use-cases.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 指定模型 ID，如 `qwen-turbo`；不支持自定义模型别名 |
| `input.messages` | array | 是 | 对话消息列表，每条含 `role`（`user`/`assistant`）和 `content` 字段 |
| `retrieval_config` | object | 否 | RAG 场景下启用，需指定 `top_k`（默认3）、`knowledge_id`（知识库ID）等 |
| `enable_stream` | boolean | 否 | 设为 `true` 启用 SSE 流式响应（仅部分模型支持） |

> **注意**：`retrieval_config` 中的 `knowledge_id` 必须通过 `/v1/knowledge_bases/{id}/documents` 接口预先上传并激活文档；该限制在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中未明确强调，但实测未激活知识库将导致检索返回空结果。

## 使用方式

1. **嵌入式助手（网站/APP）**：调用 `/v1/chat/completions` 接口，传入用户输入 + 预设 system prompt（如“你是一名技术支持专家”），前端直接渲染流式响应  
2. **企微/钉钉/公众号集成**：使用对应平台的 Webhook 回调地址接收事件，解析 `MsgType=text` 消息后调用百炼 API，再将响应按平台协议封装回发  
3. **RAG 应用**：先调用 `/v1/knowledge_bases` 创建知识库，上传文件后等待状态变为 `active`，再于请求中传入 `retrieval_config` 启用检索  

全部集成示例代码与配置模板均可在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 的子页面中获取，例如 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（`qwen-max`）或 8192（`qwen-turbo`），超限将返回 400 错误  
- RAG 检索仅支持精确匹配知识库内已激活文档，不支持跨知识库联合检索  
- 企业微信/钉钉等平台的会话上下文需由开发者自行维护（百炼 API 不保存跨请求 session）  
- 流式响应（`enable_stream=true`）在 `qwen-turbo` 上可能因模型优化关闭部分中间 token，建议客户端兼容空 chunk  
- 所有集成方案均依赖百炼平台的公网可访问性；内网部署需额外配置反向代理与证书信任链

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


