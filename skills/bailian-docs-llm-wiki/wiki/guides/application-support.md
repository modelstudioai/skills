# application [support](support.md)

阿里云百炼平台为开发者提供多层次的售后支持体系，涵盖 7×24 基础咨询、标准工单、付费增值服务等渠道，同时明确了平台自身与第三方工具之间的支持边界。本页汇总应用开发中的常见问题解答、相关服务协议及售后服务范围，帮助开发者快速定位支持资源。

## 应用中心常见问题

以下问题摘自 [常见问题](../../raw/application-user-guide/application-support/application-faq.md)，覆盖插件、RAG 检索、API 调用等高频场景。

**官方插件类型**

目前系统提供六款内置插件：Python 代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub 搜索。部分插件需申请审批后方可使用。自定义插件服务暂不收费，但涉及 [prompt](prompt.md) 优化、应用调用及测试窗测试时会产生费用。

**自定义插件与 Assistant API**

- 自定义 API 插件遵循协议传给大模型理解，[函数调用](../concepts/function-calling.md)会返回完整结果。
- 不支持透传自定义 header，仅支持 `authorization`。
- Agent 与 Assistant API 的核心区别：Agent 允许开发者自行调整插件模型和上下文理解逻辑；Assistant API 提供多种类以方便调优。

**RAG 检索增强**

- 多[知识库](../concepts/[knowledge](../api/knowledge.md)-base.md)检索采用**并行**方式，各[知识库](../concepts/[knowledge](../api/knowledge.md)-base.md)按用户配置独立检索，最终按得分取 topN。
- 模型回复不准确时，可点击回复下方的问题反馈按钮提交，或复制 RequestId 后提交阿里云工单。

**流式/增量输出**

若需增量[流式输出](../concepts/streaming.md)，在 SDK 调用时设置：

```python
stream=True            # 开启流式输出
incremental_output=True  # 增量式流式输出
```

**Markdown 渲染**

AI 输出中的 `**text**` 为标准 Markdown 加粗语法，需在前端渲染时解析 Markdown 并做对应展示。

## 数据管理常见问题

**文件上传**

- PDF 文件后缀必须为小写 `pdf`，否则报错码 `140010`。
- 每个[业务空间](../concepts/workspace.md)最多上传 10 万个文档；如需扩容，提交阿里云工单申请。
- 上传接口中的 MD5 参数用于校验文件完整性。

**结构化数据导入**

若结构化数据导入后条数少于预期，请检查表格中是否含空行——空行之后的数据不会被识别；若第一行为空行，文件将被视为空文件。

## 应用/小程序备案

接入通义千问大模型并准备上架应用市场或小程序平台时：

1. 参考[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)完成备案。
2. 提交阿里云工单申请通义千问系列模型的合作协议。

## 售后服务范围

详细说明见 [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

### 基础支持（免费，服务期内）

通过官网、电话（95187、400）及阿里云 APP 提供 7×24 咨询，支持范围：

- 模型服务与产品功能、架构咨询
- 使用与配置最佳实践
- API 及官方 SDK 故障诊断
- 管理控制台相关问题
- 账号、财务、合同及计费咨询

### 付费增值服务

阿里云提供付费版售后增值服务（含支持计划），需在阿里云官网订购后生效。如项目需要更深度的技术支持（业务代码编写指导、定制化集成方案等），建议联系阿里云商务经理沟通定制化方案。

### 第三方工具对接的支持边界

**支持范围（方向性建议）**：
- 确认百炼 API 接口及服务端可用状态
- 官方 API 调用示例及 SDK 使用说明参考
- 协助核查服务端调用明细和计费记录
- 基本连通性测试建议（如 curl 测试）

**不在支持范围内**：
- 第三方工具（Cursor、Windsurf、Cline 等）的安装、配置、升级及使用指导
- 第三方工具内部功能、交互逻辑问题排查
- 用户业务代码的编写、调试与实现
- 用户本地环境（内网、代理、VPN、防火墙等）导致的连通性或兼容性问题
- 第三方工具显示的 [Token](../concepts/token.md) 数/费用预估与阿里云计费数据之间的差异解释

> **注意**：第三方工具不构成阿里云的代理或联合服务主体，阿里云不对外部第三方工具的任何陈述、承诺或行为承担责任。第三方工具的运行维护责任由用户及相应工具提供方承担。

## 相关协议

以下协议文本详见 [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)：

- [阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)
- [阿里云百炼体验功能特别说明](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20260716114753386/20260716114753386.html)
- [开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)

## 来源文档

- [常见问题](../../raw/application-user-guide/application-support/application-faq.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)







