# application [support](support.md)

本页汇总阿里云百炼平台在应用开发和数据管理过程中的常见问题及相关服务协议。开发者可在此快速查阅插件使用、RAG 检索、数据上传、应用备案等高频问题的解答，同时了解平台的服务条款与开源模型协议。

## 应用中心常见问题

### 插件能力

百炼平台目前提供六款官方插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码和 GitHub 搜索。部分插件需要申请通过后才能使用。关于插件能力的详细说明，参见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)。

- **自定义插件收费**：自定义插件服务本身不收费，但配置智能体 API 时涉及的 [prompt](prompt.md) 优化、应用调用及测试窗测试会产生费用。
- **参数理解机制**：自定义 API 插件会遵循协议将参数传给大模型进行理解；[函数调用](../concepts/function-calling.md)时，大模型会学习传入的参数信息并返回完整结果。
- **Header 透传**：调用自定义插件时不支持自定义 header，仅支持 `authorization`。

### Agent 与 Assistant API

Agent 侧重于插件模型调整和基于上下文的理解，开发者可自行开发；Assistant API 则提供多种工具类，方便进行调优。

### RAG 检索增强

- RAG 广泛应用于问答系统、对话系统、文本摘要、知识图谱构建、客户服务、智能搜索与推荐等领域。
- RAG 检索为**并行**执行：根据每个知识库的用户配置并行检索，再按得分选取 Top N 结果。
- 测试时遇到模型回复不准确，可点击回复下方的问题反馈按钮提交，或复制 RequestId 通过阿里云工单反馈。

### [流式输出](../concepts/streaming.md)配置

如需将应用回复设为增量输出，设置以下参数：

```python
stream=True               # 流式输出
incremental_output=True    # 增量式流式输出
```

### Markdown 渲染

大模型输出中的 `**xxxxx**` 是 Markdown 加粗标识，前端渲染时需解析 Markdown 语法并做对应渲染。

## 数据管理常见问题

在使用百炼平台进行数据管理时，需注意以下事项（详见[常见问题](../../raw/application-user-guide/application-support/application-faq.md)中的数据管理章节）：

| 问题 | 说明 |
|------|------|
| 上传 PDF 报错 140010 | 确保文件后缀为小写 `pdf` |
| 业务空间文档数上限 | 每个空间最多 10 万个文档，超出需提交工单申请扩容 |
| 上传接口的 MD5 参数 | 用于验证上传文件的完整性 |
| 结构化数据导入缺失 | 检查表格中是否存在空行，空行后的数据不会被识别 |

## 应用备案

接入通义千问大模型的产品如需上架应用市场或小程序平台，需完成以下步骤：

1. 参考[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)完成备案流程。
2. 通过[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请通义千问系列模型的合作协议。

## 服务协议与条款

百炼平台涉及多项服务协议，开发者在使用前应仔细阅读（详见[相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)）：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html) — 平台基础服务条款
- [阿里云百炼服务特别说明](https://help.aliyun.com/zh/model-studio/bailian-service-notes) — 服务使用的补充说明
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms) — 使用开源模型时需遵守的协议条款

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)


