# application [support](support.md)

阿里云百炼平台为开发者提供应用构建过程中的常见问题解答、数据管理指引、合规备案说明以及相关服务协议。本页面汇总了应用中心、数据管理、插件使用等方面的关键信息，帮助开发者快速定位和解决问题。

## 应用中心常见问题

以下内容整理自 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的应用中心部分。

### 插件能力

- **系统内置插件**：目前提供六款官方插件——Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请后方可使用。
- **自定义插件**：自定义插件服务本身暂不收费，但配置智能体 API 时涉及的 [prompt](prompt.md) 优化、应用调用及测试窗测试会产生费用。
- **自定义 Header**：调用自定义插件时不支持自定义 header，仅支持 `authorization`。

### Agent 与 Assistant API

- **核心区别**：Agent 侧重于调整插件模型、基于上下文的理解，开发者自行开发；Assistant API 提供各类封装，方便调优。
- **参数理解**：自定义 API 插件遵循协议传给大模型理解；[函数调用](../concepts/function-calling.md)时，大模型会学习传入的参数信息并返回完整结果。

### RAG 检索增强

- **应用领域**：问答系统、对话系统、文本摘要、知识图谱构建与推理、教育与培训、客户服务、新闻与内容创作、智能搜索与推荐等。
- **检索方式**：多知识库并行检索，根据每个知识库的用户配置进行检索，然后按得分选取 TopN。
- **回复不准确时**：可点击模型回复内容下方的问题反馈按钮提交，或复制 `RequestId` 通过阿里云工单反馈。

### 输出控制

- 若需增量[流式输出](../concepts/streaming.md)（而非每次全量回复），设置以下参数：

```python
stream=True               # 流式输出
incremental_output=True   # 增量式流式输出
```

- 模型输出的 `**xxx**` 为 Markdown 加粗标识，前端渲染时需解析 Markdown 语法做对应展示。

## 数据管理

根据 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中的数据管理部分，以下为关键注意事项：

| 问题 | 说明 |
|------|------|
| PDF 上传报错 `140010` | 确保文件后缀为小写 `pdf` |
| 文档数量上限 | 每个[业务空间](../concepts/workspace.md)最多 10 万个文档，超出需提交工单申请扩容 |
| 上传接口 MD5 参数 | 用于验证上传文件的完整性 |
| 结构化数据导入缺失 | 检查表格中是否存在空行，空行后的数据不会被识别；首行为空行则视为空文件 |

## 应用合规备案

产品接入通义千问大模型后，如需上架至应用市场或小程序平台：

1. 参考 [应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model) 完成备案流程。
2. [提交工单](https://smartservice.console.aliyun.com/service/create-ticket) 申请通义千问系列模型的合作协议。

## 相关协议

以下协议与服务条款汇总自 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)

> **注意**：两篇原始文档均提及了"阿里云百炼服务协议"链接，内容一致，无矛盾。但 [常见问题](../../raw/application-user-guide/application-support/application-faq.md) 中仅列出了服务协议，而 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md) 额外包含了"服务特别说明"和"开源模型协议条款说明"，建议以后者为完整参考。

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)







