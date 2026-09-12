# support

`support` 是百炼平台为开发者提供的服务支持入口，涵盖模型能力覆盖范围、常见问题解答、服务协议及售后保障等核心信息。所有支持资源均通过官方帮助中心统一维护，确保信息权威性与时效性。开发者应优先查阅 [服务支持](../../raw/model-user-guide/support.md) 文档获取最新链接与范围说明。

## 支持的模型/功能

当前支持的模型列表以 [服务支持](../../raw/model-user-guide/support.md) 中引用的 [模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list) 为准，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方接入模型。功能支持范围包括 API 调用、控制台调试、批量推理、微调任务提交与监控。**注意：** 模型列表页面未明确标注各模型在百炼平台的具体可用性状态（如是否支持[流式输出](../concepts/streaming-output.md)、是否开放 Function Calling），实际能力请以控制台模型详情页或 [服务支持](../../raw/model-user-guide/support.md) 所列官方链接为准。

## 关键参数

`support` 本身不涉及请求参数，但其关联的服务（如售后工单、问题反馈）依赖用户身份（阿里云主账号/子账号）、实例 ID、模型 ID 及错误日志等上下文信息。提交售后请求时，需按 [售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 要求提供完整复现步骤与 trace_id；相关协议约束详见 [相关协议](https://help.aliyun.com/zh/model-studio/related-agreements)，该内容亦被 [服务支持](../../raw/model-user-guide/support.md) 引用。

## 使用方式

- 访问百炼控制台 →「帮助与支持」→「常见问题」，直接检索关键词（如“鉴权失败”“429 错误”）；
- 遇到技术问题，优先查阅 [服务支持](../../raw/model-user-guide/support.md) 提供的 [常见问题](https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio) 页面；
- 需人工介入时，在控制台右上角点击「工单」，选择对应服务类型（如“模型服务”），并准确填写问题描述与环境信息。

## 限制和注意事项

- 售后响应时效依服务等级协议（SLA）执行，免费版用户工单响应时间为 5 个工作日，企业版为 2 小时（具体以 [售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 为准）；
- 非百炼平台直接托管的模型（如通过自定义 API 接入的第三方模型）不在标准售后范围内；
- > **注意**：[服务支持](../../raw/model-user-guide/support.md) 中列出的链接均为外部帮助中心页面，其内容更新频率独立于百炼 Wiki，若发现链接失效或信息矛盾（例如某模型在帮助中心显示“已下线”，但在控制台仍可选），请以控制台实时状态为准，并通过工单反馈。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


