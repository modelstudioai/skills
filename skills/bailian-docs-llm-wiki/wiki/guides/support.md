# support

`support` 是百炼平台为模型调用和服务使用提供的基础支持能力，涵盖服务可用性保障、问题响应机制及售后范围说明。开发者可通过该模块获取技术协助、了解服务边界，并查阅相关协议与常见问题。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 为准。

## 支持的模型/功能

- 当前 `support` 模块本身不绑定特定模型，而是面向所有在百炼平台部署和调用的模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等）提供统一的服务支持入口。  
- 支持范围包括 API 调用异常排查、配额与计费咨询、模型服务不可用告警响应，以及沙箱环境调试协助。  
- 不支持模型训练过程中的算法调优或私有数据标注服务，此类需求需参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确列出的服务边界。

## 关键参数

`support` 无独立调用接口或参数配置项。其行为由平台级策略控制，例如：  
- `service_level`（隐式）：默认按「标准支持」等级执行（工作日 5×8 小时响应），企业版客户可升级至「高级支持」（7×24 小时）。  
- `ticket_priority`（隐式）：根据错误码（如 `503 Service Unavailable` 或 `429 Rate Limited`）自动分级，详情见 [服务支持](../../raw/model-user-guide/support.md) 中的 SLA 定义。  
- 所有支持请求需附带 `request_id`（来自 API 响应头 `X-Request-ID`），否则无法关联日志追踪。

## 使用方式

1. **自助排查**：优先查阅 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md)，覆盖 80% 以上高频报错（如鉴权失败、超时、格式错误）。  
2. **提交工单**：登录阿里云控制台 → 百炼服务页 → 「技术支持」→ 创建工单，务必填写完整上下文（模型 ID、时间戳、完整请求/响应体、`X-Request-ID`）。  
3. **紧急响应**：若遇全链路服务中断（如 `/v1/chat/completions` 持续 5 分钟不可用），可拨打企业支持专线（仅限合同客户），并同步邮件至 support@bailian.aliyun.com，主题注明「P0-服务中断」。

## 限制和注意事项

- 工单响应时效以工作日（周一至周五，不含法定节假日）计算；非工作时间提交的工单，首响时间从下一个工作日开始计时。  
- 自定义模型（BYOM）的推理服务稳定性由用户自行保障，平台仅对托管基础设施（GPU、网络、API 网关）提供 SLA，具体条款参见 [相关协议](../../raw/model-user-guide/support/related-agreements.md)。  
> **注意**：[服务支持](../../raw/model-user-guide/support.md) 中提及的「7×24 技术支持」仅适用于已签署《百炼企业服务协议》的客户，未签约用户实际享受的是标准支持（5×8），此差异已在最新版 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确修订，旧文档未同步更新。  
- 不支持通过 GitHub Issue、社区论坛或即时通讯工具（如钉钉群）发起正式支持请求；非工单渠道的问题反馈不纳入 SLA 保障范围。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


