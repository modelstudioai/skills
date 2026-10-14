# application [support](support.md)

阿里云百炼平台的应用支持覆盖模型服务使用、API调用、插件集成、RAG应用开发及配套运维等全链路场景，面向开发者提供基础技术咨询、故障诊断与方向性指导。支持范围以阿里云百炼平台自身服务边界为限，不延伸至第三方工具、用户本地环境或业务代码实现层。具体能力、参数与限制详见下文。

## 支持的模型/功能

- **插件能力**：官方提供六类内置插件：Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索；其中部分需申请开通 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **自定义插件**：支持通过符合协议的 API 接入，大模型可理解参数结构并完成调用；但**不支持透传除 `Authorization` 外的任意自定义 Header** [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **RAG（知识检索增强）**：支持多知识库并行检索、按得分聚合 topN 结果，已应用于问答系统、客户服务、教育、内容创作等场景 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。  
- **流式输出**：支持增量式流式响应，需同时设置 `stream=True` 与 `incremental_output=True`。  

> **注意**：文档2中“Agent和Assistant API的最大区别”条目表述模糊（如“调整插件模型、基于上下文的理解，用户可以自己去开发”），未明确技术差异边界，且与当前平台实际API设计（如 `/v1/agents` 与 `/v1/assistants` 的能力划分）存在不一致。建议以[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)及控制台最新文档为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必需 |
|--------|------|------|----------|
| `stream` | boolean | 启用流式输出（逐 token 返回） | 否（默认 `False`） |
| `incremental_output` | boolean | 启用增量式流式输出（仅返回新增内容） | 否（仅当 `stream=True` 时生效） |
| `MD5` | string | 文件上传时用于校验完整性的哈希值（小写十六进制） | 是（结构化数据/文件导入必填） |

## 使用方式

- **技术支持渠道**：7×24 小时电话（95187 / 400）、智能在线客服、标准工单（推荐含 `RequestId` 的问题反馈）[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **问题定位建议**：  
  - API 调用异常时，优先使用 `curl` 测试服务端可达性；  
  - RAG 回复不准时，可通过控制台“问题反馈”按钮提交或复制 `RequestId` 提交工单；  
  - Markdown 渲染（如 `**text**`）需在前端自行解析，平台仅返回原始文本。  
- **备案与合作**：应用上架前须完成[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)，并提交工单申请通义千问合作协议 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项

- **第三方工具免责**：阿里云不提供 Cursor、Windsurf 等第三方 AI 工具的安装、配置、升级或故障排查支持；也不对第三方工具内部显示的 [Token](../concepts/token.md) 数量、费用预估与阿里云计费数据差异作解释 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **环境责任边界**：用户本地网络（代理/VPN/防火墙）、操作系统兼容性、账号权限配置等问题，属用户侧责任，阿里云仅提供连通性测试等方向性建议 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。  
- **文件与容量限制**：  
  - 上传文件仅支持 `.pdf`（小写后缀）、`.doc`、`.docx`；  
  - 单业务空间最多存储 10 万份文档，超限时需提交工单申请扩容；  
  - 结构化数据导入时，空行将导致后续行被跳过（首行为空则视为无效文件）。  
- **协议约束**：所有服务受《[阿里云百炼服务协议](../../raw/application-user-guide/application-support/application-related-agreements.md)》及《体验功能特别说明》约束，开源模型使用还需遵守对应[开源模型协议条款](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


