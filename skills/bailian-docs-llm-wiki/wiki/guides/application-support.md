# application [support](support.md)

阿里云百炼平台的 `application support` 指面向开发者在构建、调试和运维基于百炼的应用（含智能体、RAG 应用、插件集成等）过程中提供的技术支撑体系，涵盖功能能力边界、关键配置参数、调用方式及服务保障范围。该支持体系以 API 可控性、知识增强可调性和售后响应机制为核心，适用于生产环境集成与问题排查场景。具体能力与限制需结合协议约束与技术文档综合理解。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索，按配置策略打分后取 topN 结果融合生成，已应用于问答系统、客户服务、教育培训等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过 OpenAPI 注册 HTTP 类函数插件，大模型可理解其参数结构并参与调用决策；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)**：支持增量式流式响应，需同时设置 `stream=True` 和 `incremental_output=True`。  

> **注意**：文档2中“Agent和Assistant API的最大区别”描述模糊且缺乏技术细节（如无明确接口差异、版本兼容性说明），实际开发应以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中定义的 API 支持范围为准，避免依赖该主观对比。

## 关键参数

- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)（默认 `False`）。  
- `incremental_output`: 布尔值，启用增量式[流式输出](../concepts/streaming-output.md)（仅当 `stream=True` 时生效）。  
- `MD5`: 文件上传接口必填参数，用于校验文件完整性。  
- 知识库检索配置：支持 per-knowledge-base 的相似度阈值、topK、分块策略等参数，影响 RAG 准确性。  

## 使用方式

- **插件调用**：通过 Assistant API 或 Agent SDK 注册插件 schema 后，由模型自主触发；自定义插件需符合 OpenAPI 3.0 协议规范。  
- **RAG 测试优化**：若检索结果不准确，可通过控制台问题反馈按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：仅支持小写后缀的 `pdf`/`doc`/`docx`；空行会导致结构化数据截断（首行为空则识别为空文件）。  
- **备案与合作**：接入通义千问模型上架应用市场前，须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请合作协议。  

## 限制和注意事项

- **第三方工具支持边界**：阿里云百炼仅保障自身服务端可用性、API 接口行为及计费一致性；对 Cursor、Windsurf 等第三方 AI 工具的安装、配置、本地代理、防火墙穿透等问题**不提供技术支持**，详见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件容量限制**：单业务空间最多上传 10 万个文档；超限时需提交工单申请扩容。  
- **协议约束**：所有应用必须遵守[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)及[开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)，相关法律义务请参阅 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。  
- **自定义插件收费提示**：插件注册本身免费，但使用智能体 API 进行 prompt 优化、应用调用测试等操作将产生计费。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


