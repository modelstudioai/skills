# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming.md)控制、API 调用规范及售后响应机制等核心环节。该支持体系面向生产环境，强调可配置性、可观测性和边界清晰性。所有服务均以阿里云百炼平台自身能力为限，第三方工具或用户侧环境问题不在直接支持范围内。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，适用于问答系统、客服对话、教育内容生成等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming.md)（即每次返回新 token，而非全量重传）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册自定义 API 插件，大模型可理解其参数结构并生成调用逻辑；但**不支持透传自定义 Header**，仅允许 `Authorization` 字段 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

> **注意**：文档 1 中第4条称“Assistant API 可提供各种类，方便调优”，但未明确定义“类”的具体含义（如 SDK 类、配置类或抽象接口类），且其他文档未佐证该表述；建议以实际 SDK 文档和 OpenAPI 规范为准，避免依赖模糊术语。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE 格式） | 否（默认 `False`） |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式 token 输出（避免重复回传历史内容） | 否（默认 `False`） |
| `MD5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |

## 使用方式

- 插件调用：在应用编排中配置插件节点，自定义插件需符合 OpenAPI 3.0 协议并完成鉴权注册；调用时由大模型自动解析参数并构造请求。  
- RAG 配置：在知识库设置中指定检索权重、分块策略与重排序规则；测试阶段若结果不准，可通过界面反馈按钮提交问题，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 增量[流式输出](../concepts/streaming.md)：需客户端兼容 SSE 协议，并正确处理 `data:` 字段中的增量 token；前端渲染 Markdown（如 `**text**`）需自行解析，平台不提供富文本转换服务 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- 售后接入：7×24 小时支持渠道包括官网智能在线、电话（95187/400）、标准工单；深度技术支持（如业务代码指导、定制集成）需订购付费支持计划 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 限制和注意事项

- **文件上传**：仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；结构化数据导入时，空行将导致后续行被截断 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **知识库容量**：单业务空间上限为 10 万文档；超限时需提交工单申请扩容 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **第三方工具边界**：阿里云仅对百炼服务端状态、API 可达性、SDK 调用示例及计费明细提供支持；第三方工具（如 Cursor、Windsurf）的部署、配置、故障排查等**完全不在支持范围内** [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须遵守《阿里云百炼服务协议》《体验功能特别说明》及开源模型相关条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


