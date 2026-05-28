# application [[support|support]]

本文档汇总阿里云百炼应用开发、插件集成与数据管理过程中的核心配置指引与常见问题。旨在帮助开发者快速定位接口调用、[[streaming-output|流式输出]]及知识库检索中的技术细节，并规范完成合规上架流程。平台持续迭代，接入前建议核对最新服务条款。

## 支持的模型与功能
- **官方内置插件**：默认提供 Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分高阶插件需通过工单申请开通，详见 [常见问题](../../raw/application-user-guide/application-[[support|support]]/application-faq.md)。
- **自定义插件/函数**：支持通过标准协议注册外部 API。大模型将自动学习传入的参数定义，完成意图解析与结果透传，可与 [[agent-config]] 协同使用。
- **RAG 检索增强**：多知识库采用并行检索架构，按用户配置计算相关性得分后选取 TopN 结果。适用于复杂问答、文本摘要及 [[rag-retrieval]] 场景。
- **协议支持**：服务遵循标准化授权与数据合规要求，完整法律文本参见 [相关协议](../../raw/application-user-guide/application-[[support|support]]/application-related-agreements.md)。

## 关键参数
| 参数/标识 | 说明 |
|---|---|
| `stream=True` | 启用 HTTP 流式响应，适用于长文本实时渲染场景。 |
| `incremental_output=True` | 配合流式使用，实现增量输出（避免重复返回历史累积内容）。 |
| `MD5` | 数据管理上传接口必填项，用于校验文件传输完整性与防篡改。 |
| `Authorization` | 唯一允许透传至自定义插件后端的请求头，其他自定义 Header 将被拦截。 |

## 使用方式
- **[[streaming-output|流式输出]]配置**：在 API 请求中同时声明 `stream=True` 与 `incremental_output=True` 可获取逐段生成的 Token。前端需通过 SSE 或 WebSocket 协议接收并拼接渲染。
- **Markdown 解析**：模型默认输出标准 Markdown 语法（如 `**加粗**`）。业务侧需集成解析库（如 `marked.js`、`markdown-it`）进行 DOM 转换，不可直接渲染纯文本。
- **检索效果调优**：测试 [[rag-retrieval]] 时若发现回复偏差，可在控制台点击反馈按钮勾选类型，或提取 `RequestId` 通过工单提交底层日志分析。
- **合规备案流程**：接入通义系列模型上架应用市场或小程序前，需先完成 [[compliance-filing]]，并独立申请合作协议。详细指引参考 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 限制和注意事项
- **计费边界**：自定义插件功能本身暂不收费，但涉及 [[assistant-api]] 的 Prompt 优化、实际应用调用及测试窗调试均按标准 Token 计量计费。
- **存储配额**：单业务空间文档上限为 10 万篇。结构化数据导入时，系统遇空行即终止解析（首行为空则判定为空文件），需提前清洗数据。
- **文件规范**：PDF 后缀必须为全小写 `.pdf`，大写后缀将触发 `140010` 格式错误。
- **架构差异**：Agent 侧重开发者自主编排插件模型与上下文逻辑；[[assistant-api]] 提供封装类接口便于快速调优与状态管理。

> **注意**：自定义插件 Header 透传策略已明确限定仅支持 `Authorization`，业务侧若依赖其他自定义鉴权头（如 `X-Custom-Token`），需在插件网关层自行映射或通过参数体传递。平台计费与容量配额策略可能随产品迭代调整，请以控制台实时账单及最新公告为准。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)

