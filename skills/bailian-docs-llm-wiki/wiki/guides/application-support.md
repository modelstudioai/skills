# application [support](support.md)

本页汇总阿里云百炼平台应用与[知识库](../concepts/knowledge-base.md)使用过程中的常见问题、关键限制以及相关协议入口，帮助开发者在接入应用、调用插件、管理数据与合规备案时快速定位答案。内容主要参考 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 与 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)。

## 应用中心

### 插件能力

百炼应用中心官方提供六款插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索，其中部分插件需申请通过后方可使用。自定义插件服务本身暂不收费，但配置智能体 API 时若涉及 [prompt](prompt.md) 优化、应用调用及测试窗测试，则会产生费用。

- **插件理解机制**：自定义 API 插件遵循协议传给大模型理解；自定义函数则由大模型学习传入的参数信息并返回完整结果。
- **header 透传**：百炼调用自定义插件时**不支持自定义 header**，仅支持 `authorization`。若业务场景需要透传 header，需在服务端侧另行处理。

### Agent 与 Assistant API 的区别

Agent 偏重于调整插件模型与基于上下文的理解，由用户自行开发；Assistant API 则提供各类能力以方便调优。两者面向不同定制粒度，可根据应用复杂度选择。

### 输出控制

- **流式与增量输出**：默认为全量回复，若需增量输出，可设置 `stream=True`（[流式输出](../concepts/streaming-output.md)）与 `incremental_output=True`（增量式[流式输出](../concepts/streaming-output.md)）。
- **Markdown 加粗**：模型输出中的 `**xxxxx**` 是 Markdown 加粗标识，需在前端渲染时解析 md 语法即可正常显示。

## 知识检索（RAG）

RAG（[检索增强生成](../concepts/rag.md)）在问答系统、对话系统、文本摘要、知识图谱构建与推理、教育与培训、客户服务、新闻与内容创作、智能搜索与推荐等多个领域均有应用。

- **检索顺序**：RAG 检索为**并行**方式，依据每个[知识库](../concepts/knowledge-base.md)的用户配置进行检索，再根据得分选取 topN 结果。
- **回复不准确优化**：可点击模型回复下方的问题反馈按钮，勾选问题类型提交；也可复制 RequestId 通过阿里云工单反馈。详见 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

## 数据管理

### 文件上传

- **格式限制**：上传 PDF 文件时后缀必须为小写 `pdf`，否则会触发错误码 `140010`（"上传文件仅支持 pdf/doc/docx 文件"）。
- **MD5 参数**：上传文件接口的必填 MD5 参数用于校验上传文件的完整性。
- **容量上限**：每个[业务空间](../concepts/workspace.md)最多上传 10 万个文档，超出需提交阿里云工单申请扩容。

### 结构化数据导入

结构化数据导入后若出现条数缺失（如 100 条仅导入 20 条），通常是因为表格中存在空行。产品策略规定：遇到空行后续数据不再识别；若第一行为空行，则整表视为空文件。

## 应用与小程序备案

产品接入通义千问大模型后，若需上架应用市场或小程序平台，需完成备案并申请合作协议：

1. 参考[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)进行备案。
2. [提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请通义千问系列模型的合作协议。

## 相关协议

接入百炼前请阅读以下协议条款：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)

协议入口同时收录在 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 中，建议在正式接入前逐项确认。

## 常见限制与注意事项

- 自定义 header 不被支持，仅 `authorization` 可透传。
- PDF 后缀必须为小写，避免触发 `140010` 错误码。
- 结构化数据表格中的空行会导致后续数据被截断识别。
- [业务空间](../concepts/workspace.md)文档数上限为 10 万，超额需工单申请。
- 自定义插件本身免费，但 [prompt](prompt.md) 优化、应用调用与测试窗测试会收费。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
















