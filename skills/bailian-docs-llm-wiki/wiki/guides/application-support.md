# application [support](support.md)

阿里云百炼平台的应用支持体系面向开发者提供覆盖模型调用、Agent构建、RAG应用开发及运维排障的全链路技术保障。支持范围以平台自身服务边界为基准，聚焦API、SDK、控制台、计费系统等官方能力；第三方工具、本地环境及业务代码层问题不在基础支持范围内。所有服务均受《[阿里云百炼服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html?spm=5176.28197581.0.0.16e829a4HTC9FE)》约束，具体权益详见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)。

## 支持的模型/功能

- **Agent 能力**：官方提供六类内置插件（Python代码解释器、计算器、图片生成、夸克搜索、生成二维码、GitHub搜索），部分需申请开通；支持自定义API插件接入，模型可理解插件参数并完成调用编排。
- **RAG 应用**：支持多知识库并行检索、topN结果融合，适用于问答系统、客服、教育、内容创作等场景；知识库文档上限为单业务空间10万份，超限需[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请扩容。
- **输出控制**：支持流式（`stream=True`）与增量式流式（`incremental_output=True`）响应，便于前端实现逐字渲染或分块处理。

## 关键参数

- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)（默认 `False`）。
- `incremental_output`: 布尔值，仅在 `stream=True` 时生效，启用增量式流式（即每次返回新片段而非累积重发）。
- `MD5`: 文件上传接口必填，用于校验文件完整性（见[Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)）。
- 自定义插件调用：**仅支持透传 `Authorization` header**，其他自定义 header 将被忽略（见[Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)第10条）。

> **注意**：文档3中“Agent和Assistant API的最大区别”描述（第4条）存在表述模糊且缺乏技术依据，未明确区分标准Assistant API与百炼Agent SDK的协议层级、调用方式及扩展机制，建议以[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)中定义的服务边界为准，避免将非平台原生能力误判为官方支持特性。

## 使用方式

- **问题反馈**：RAG测试中模型回复不准确时，可通过界面“问题反馈”按钮提交，或复制 `RequestId` 提交工单。
- **调试验证**：
  - 使用 `curl` 等标准工具测试服务地址连通性（方向性建议，见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)）；
  - 检查API调用明细与计费记录（平台侧可核查）；
  - 渲染Markdown格式输出（如 `**text**`）需由前端自行解析，平台不提供自动HTML转换。
- **合规与备案**：接入通义千问模型上架应用市场或小程序，须按[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)流程操作，并[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请合作协议。

## 限制和注意事项

- **不支持范围**（明确排除）：
  - 第三方工具（如Cursor、Windsurf等）的安装、配置、升级及日常运维；
  - 用户本地环境（内网、代理、VPN、防火墙、OS兼容性）导致的问题排查；
  - 业务代码编写、调试与实现；
  - 第三方工具内部Token统计、费用预估与阿里云实际计费数据差异解释；
  - 非阿里云百炼服务相关的其他云厂商、开源框架或社区产品的配置与故障诊断。

- **责任边界**：阿里云仅对百炼平台服务端（API接口、计量计费、控制台、模型推理服务）承担运维责任；第三方工具运行维护由用户及对应提供方负责，阿里云不对其陈述、行为或故障承担责任（见[阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)第5条）。

- **协议约束**：所有使用行为须遵守《阿里云百炼服务协议》及《阿里云百炼体验功能特别说明》，开源模型使用还需符合对应[开源模型协议条款说明](https://help.aliyun.com/zh/model-studio/open-source-model-terms)。

## 来源文档

- [阿里云百炼平台售后服务范围说明](../../raw/application-user-guide/application-support/application-after-sales-service-scope.md)
- [相关协议](../../raw/application-user-guide/application-support/application-related-agreements.md)
- [Agent 应用与知识库常见问题](../../raw/application-user-guide/application-support/application-faq.md)


