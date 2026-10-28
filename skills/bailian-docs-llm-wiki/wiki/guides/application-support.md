# application [support](support.md)

`application support` 指百炼平台为开发者在构建、调试、部署和运维 AI 应用过程中提供的技术支撑能力，涵盖插件集成、RAG 检索增强、[流式输出](../concepts/streaming-output.md)控制、文件与数据管理，以及售后响应机制等核心环节。该支持体系面向生产环境需求设计，强调可配置性、可观测性和边界清晰的服务范围。所有功能均需通过百炼控制台或标准 API 调用启用，不依赖前端渲染逻辑。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG 检索增强**：支持多知识库并行检索（按用户配置策略执行），再基于相关性得分聚合 TopN 结果，适用于问答系统、客户服务、教育等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **结构化数据导入**：支持 Excel/CSV 表格导入，但存在空行截断策略——若首行为空行，整表将被识别为空文件；后续空行亦会导致其后数据丢失 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **[流式输出](../concepts/streaming-output.md)控制**：支持两种模式：`stream=True`（全量流式）与 `incremental_output=True`（增量式流式），后者可避免重复返回历史 token。  

> **注意**：文档 1 中第 4 条称 “Agent 和 Assistant API 的最大区别是用户可自行开发插件模型”，但该描述未定义“插件模型”具体指代（是自定义 LLM 还是[函数调用](../concepts/function-calling.md)协议？），且与当前百炼统一使用 `tools` 协议调用插件的事实不符；实际开发中应以 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中第 3 条所述的 `tools` 参数协议为准，而非独立“插件模型”。

## 关键参数

- `stream`: 布尔值，启用流式响应（逐 token 返回）。  
- `incremental_output`: 布尔值，仅当 `stream=True` 时生效，启用增量式输出（每次仅返回新增 token，非全量重传）。  
- `tools`: JSON 数组，定义插件函数签名（含 `name`, `description`, `parameters`），模型据此生成 `tool_calls`；**不支持透传自定义 Header，仅允许 `Authorization` 字段** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- [文件上传](../concepts/file-upload.md)必填 `MD5`：用于校验文件完整性，防止传输损坏。  

## 使用方式

- 插件调用：通过 `tools` 参数声明函数能力，模型自动选择并填充参数；自定义插件无需额外训练，依赖协议对齐。  
- RAG 应用调试：若检索结果不准确，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- [文件上传](../concepts/file-upload.md)：PDF 文件后缀必须为小写 `pdf`，否则报错 `140010`；单业务空间上限 10 万文档，超限时需提交工单申请扩容。  
- Markdown 渲染：模型输出中的 `**text**` 等语法需由前端解析并渲染，百炼服务端不执行格式转换。  

## 限制和注意事项

- **插件 Header 限制**：自定义插件调用时，仅支持透传 `Authorization` 请求头，其他 header（如 `X-User-ID`）会被丢弃，不可用于身份上下文传递。  
- **第三方工具支持边界**：阿里云售后仅提供方向性建议（如 API 可达性测试、SDK 示例、计费核查），**不支持**第三方工具（如 Cursor、Windsurf）的安装、配置、故障诊断及本地环境（代理/防火墙/OS）问题排查 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **服务责任边界**：阿里云仅保障百炼服务端（API 接口、计量计费、控制台）稳定性；第三方工具运行、用户业务代码、网络策略等引发的问题，不在标准售后覆盖范围内。  
- **协议约束**：所有使用须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型还需符合对应许可证条款 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)


