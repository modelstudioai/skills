# support

`support` 是百炼平台为开发者提供的服务支持入口，涵盖模型能力覆盖范围、常见问题解答、服务协议及售后保障等核心信息。所有支持资源均通过统一文档体系组织，便于快速定位技术细节与合规要求。开发者应优先查阅最新版原始文档以确保信息时效性。

## 支持的模型/功能

当前 `support` 覆盖百炼平台上全部公开可调用的模型，包括通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等多模态与语言模型，以及部分第三方合作模型。具体可用模型列表以 [服务支持](../../raw/model-user-guide/support.md) 中链接的[模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list) 为准。功能层面，支持包括 API 调用、控制台调试、批量推理、微调任务提交及结果监控等全链路能力。

## 关键参数

`support` 本身不暴露独立 API 参数，但其关联的服务行为（如售后响应时效、SLA 承诺、配额调整申请）依赖用户身份类型（个人/企业）、套餐等级及调用场景。例如，企业实名用户可申请更高并发配额，该流程需在 [服务支持](../../raw/model-user-guide/support.md) 所述的[售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 页面中提交工单。关键字段如 `service_type`、`ticket_priority` 在工单系统中影响处理路径，详见 [服务支持](../../raw/model-user-guide/support.md) 提供的协议与范围定义。

## 使用方式

开发者可通过以下三种方式获取支持：  
- **自助查阅**：访问 [服务支持](../../raw/model-user-guide/support.md) 页面中的[常见问题](https://help.aliyun.com/zh/model-studio/faq-about-alibaba-cloud-model-studio)，覆盖鉴权失败、限流触发、返回格式异常等高频问题；  
- **协议确认**：调用前务必阅读 [服务支持](../../raw/model-user-guide/support.md) 指向的[相关协议](https://help.aliyun.com/zh/model-studio/related-agreements)，明确数据隐私、知识产权与责任边界；  
- **人工介入**：当自助无法解决时，在控制台「帮助中心 → 提交工单」发起请求，并准确选择服务类型（如“模型调用异常”“配额扩容”），系统将依据 [售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope) 自动分派。

## 限制和注意事项

- 免费试用额度仅适用于新注册用户，且不可叠加或转让，具体规则以 [服务支持](../../raw/model-user-guide/support.md) 中的协议条款为准；  
- 工单响应时效按服务等级协议（SLA）执行：P1 级故障（服务完全不可用）承诺 1 小时内首次响应，P3 级咨询（功能使用疑问）为 3 个工作日，详情见[售后说明](https://help.aliyun.com/zh/model-studio/after-sales-service-scope)；  
> **注意**：原始文档中[模型列表](https://help.aliyun.com/zh/model-studio/model-studio-model-list) 页面已更新 Qwen3-32B 的商用许可状态，但 [服务支持](../../raw/model-user-guide/support.md) 文末的「相关协议」链接仍指向旧版通用协议（v2.1），实际生效协议应以控制台「账户设置 → 协议中心」中最新签署版本（v3.0）为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


