# security and compliance

百炼平台提供多层次安全与合规能力，覆盖模型调用全链路，包括传输加密、权限控制、内容安全过滤、私网访问支持及监管要求的备案机制。所有能力均通过 API 参数、控制台配置或服务端策略生效，开发者需结合自身业务场景选择启用方式。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、第三方接入模型）均默认启用传输层 TLS 1.2+ 加密和输入/输出内容安全过滤（基于关键词、敏感实体、图像鉴黄等多模态策略）  
- 私网访问（VPC 内网直连）仅支持百炼专属版实例，标准版不支持 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)  
- 模型备案信息公示与应用合规备案功能仅对已通过百炼平台完成上线审核的 AI 应用开放，详见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)

## 关键参数

- `enable_content_safety`: 布尔值，控制是否启用输入输出 AI 安全护栏（默认 `true`），关闭后仍受基础协议层过滤约束  
- `vpc_endpoint`: 字符串，用于指定私网访问 endpoint（仅专属版有效），需在创建实例时配置，运行时不可变更  
- `compliance_filing_id`: 字符串，应用备案成功后返回的唯一 ID，需在请求 header 中携带 `X-Compliance-Filing-ID` 才能触发备案校验流程  

## 使用方式

- 权限管理通过 RAM 角色策略实现，最小权限原则推荐使用预置策略 `AliyunBailianFullAccess` 或自定义策略，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)  
- 传输安全无需额外配置，所有公网 API 默认强制 HTTPS；私网访问需在控制台开通 VPC 接入并配置安全组规则  
- 内容安全过滤结果通过响应字段 `safety_result` 返回，包含 `action`（`allow`/`block`/`review`）和 `reason`，开发者应据此处理拦截逻辑  

## 限制和注意事项

- 私网访问不支持跨地域调用，且 `vpc_endpoint` 仅对专属版实例生效；标准版即使传入该参数亦被忽略  
- `enable_content_safety=false` 仅禁用 AI 护栏层过滤，底层协议级敏感词拦截（如涉政、暴恐关键词）仍强制生效  
- > **注意**：[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md) 中关于 GDPR 数据驻留的描述已过时——当前百炼所有中国站实例数据默认存储于阿里云华东1（杭州）地域，不支持用户指定境外区域部署，该限制未在文档中同步更新  
- 模型备案信息公示页面（`/api/v1/model-filing`）仅返回已通过国家网信办备案的模型列表，未备案模型调用将返回 `403 Forbidden`，而非降级至未备案版本

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


