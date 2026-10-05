# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、API 调用规范及售后响应机制等核心环节。其目标是保障应用功能可扩展、调用可追溯、问题可定位、服务有边界。所有支持行为均以阿里云百炼平台自身服务范围为限，不延伸至第三方工具或用户侧环境。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置执行），再基于相关性得分选取 topN 结果用于生成；适用于问答系统、客服对话、教育训练等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式与增量输出**：通过 `stream=True` 启用流式响应；进一步设置 `incremental_output=True` 可实现增量式[流式输出](../concepts/streaming-output.md)（即每次返回新片段，而非全量重发）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过标准协议注册自定义 API 插件，大模型可理解其参数结构并完成调用；但**仅支持透传 `Authorization` header，不支持其他自定义 header**（如 `X-User-ID` 等）> **注意**：文档 1 第 10 条明确声明“不支持自定义header，仅支持authorization”，而部分旧版 SDK 示例曾误含 `headers` 字段传递，该用法已失效。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | bool | 启用流式响应（SSE） | 否，默认 `False` |
| `incremental_output` | bool | 在 `stream=True` 下启用增量式输出（避免重复内容） | 否，默认 `False` |
| `md5` | string | 文件上传时必填，用于校验文件完整性 | 是（见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 数据管理章节） |
| `Authorization` | string | 自定义插件调用时唯一允许透传的 header 字段 | 是（若插件要求鉴权） |

> **注意**：`incremental_output=True` 仅在 `stream=True` 为真时生效；单独设置 `incremental_output=True` 无效果。

## 使用方式

- **插件调用**：在智能体（Agent）配置中启用对应插件，或通过 Assistant API 的 `tools` 字段声明函数签名；自定义插件需符合 OpenAI-style function calling 协议。  
- **RAG 集成**：在应用配置中绑定知识库，系统自动并行检索各库并融合结果；优化建议包括调整 chunk size、重排策略及 [prompt](prompt.md) 中的指令清晰度。  
- **错误排查**：RAG 输出不准确时，优先点击回复下方「问题反馈」按钮提交；若需深度分析，请复制 `RequestId` 并[提交阿里云工单](https://smartservice.console.aliyun.com/service/create-ticket) [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **文件上传**：PDF 文件后缀必须为小写 `pdf`；结构化数据导入需避免空行（首行为空将被识别为无效文件）[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **插件透传限制**：自定义插件调用时，仅 `Authorization` header 可被透传至目标服务端；其他 header 将被丢弃（文档 1 第 10 条已明确）。  
- **知识库容量**：单业务空间最多支持 10 万个文档；超限时需[提交工单申请扩容](https://smartservice.console.aliyun.com/service/create-ticket) [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **售后边界**：阿里云百炼售后仅覆盖平台自身服务（API、控制台、计费、SDK），**不包含**：第三方工具部署/配置（如 Cursor、Windsurf）、用户本地网络/代理/防火墙问题、业务代码编写、非阿里云服务对接故障 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **协议约束**：使用前须遵守《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)》及《[阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)》[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


