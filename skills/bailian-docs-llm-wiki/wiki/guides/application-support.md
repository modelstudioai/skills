# application [support](support.md)

阿里云百炼平台为开发者提供应用构建、数据管理和合规备案等多方面的支持。本页面汇总了平台使用过程中的常见问题解答、服务协议说明以及合规备案指引，帮助开发者快速定位和解决问题。

## 平台插件与自定义能力

百炼平台目前提供六款官方插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码和 GitHub 搜索。部分插件需要申请通过后方可使用。自定义插件服务暂不收费，但配置智能体 API 涉及 [prompt](prompt.md) 优化、应用调用及测试时会产生费用。

自定义 API 插件遵循协议传递给大模型进行理解。对于自定义函数，大模型会学习传入的参数信息并返回完整结果。需注意，调用自定义插件时**不支持自定义 header**，仅支持 `authorization`。

更多插件相关问题请参阅[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## Agent 与 Assistant API

Agent 和 Assistant API 的核心区别在于：Agent 侧重插件模型调整和上下文理解，开发者可自行扩展；Assistant API 则提供多种封装类，便于调优。

## RAG 检索增强

知识检索增强（RAG）在问答系统、对话系统、文本摘要、知识图谱构建、教育培训、客户服务等多个领域有广泛应用。使用时需关注以下要点：

- **检索模式**：RAG 检索为并行执行，根据每个知识库的用户配置进行检索，再按得分选取 TopN 结果。
- **回复准确性优化**：当模型回复不准确时，可点击回复内容下方的问题反馈按钮提交反馈，也可复制 RequestId 通过阿里云工单反馈。
- **流式与增量输出**：设置 `stream=True` 启用[流式输出](../concepts/streaming.md)，配合 `incremental_output=True` 实现增量式[流式输出](../concepts/streaming.md)，避免全量重复回复。
- **Markdown 渲染**：大模型输出中的 `**xxx**` 为 Markdown 加粗标识，前端需解析 Markdown 语法做对应渲染。

详细 FAQ 列表参见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)原始文档。

## 数据管理

在使用数据管理功能时，需注意以下限制和要求：

| 事项 | 说明 |
|------|------|
| 文件格式 | 支持 PDF/DOC/DOCX，PDF 文件后缀必须为小写 `pdf` |
| 文档数量上限 | 每个[业务空间](../concepts/workspace.md)最多 10 万个文档，超出需提交工单申请扩容 |
| 上传 MD5 参数 | 用于验证上传文件的完整性，为必填项 |
| 结构化数据 | 表格中不能有空行，空行后的数据将不被识别；首行为空则视为空文件 |

## 应用合规备案

接入通义千问大模型的产品如需上架至应用市场或小程序平台，需完成以下步骤：

1. 参考百炼平台的应用合规备案指南进行备案。
2. 通过阿里云工单系统申请通义千问系列模型的合作协议。

## 服务协议

百炼平台的使用受以下协议约束，开发者在使用前应仔细阅读：

- **阿里云百炼服务协议** — 平台核心服务条款
- **阿里云百炼服务特别说明** — 补充使用说明
- **开源模型协议条款说明** — 开源模型的许可与使用限制

完整协议链接请参阅[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 来源文档

- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)




