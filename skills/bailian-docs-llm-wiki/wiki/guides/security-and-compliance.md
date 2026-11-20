# security and compliance

百炼平台提供多层次安全与合规能力，覆盖模型调用全链路，包括传输加密、权限控制、[内容安全过滤](../concepts/security-filtering.md)、私网访问支持及监管要求的备案机制。所有能力均通过 API 参数、控制台配置或服务端策略生效，开发者需结合自身业务场景选择启用方式。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、第三方接入模型）均默认启用传输层 TLS 1.2+ 加密和输入/输出[内容安全过滤](../concepts/security-filtering.md)（基于关键词、敏感实体、图像鉴黄等多模态策略）  
- 私网访问（VPC 内网直连）仅支持百炼专属版实例，标准版不支持 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)  
- 模型备案信息公示与应用合规备案功能仅对已通过阿里云 AI 应用备案流程的客户开放，需在百炼控制台「合规中心」完成关联操作，详见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)

## 关键参数

- `enable_content_safety`: 布尔值，控制是否启用输入/输出[内容安全过滤](../concepts/security-filtering.md)（默认 `true`），关闭后仍受平台级基础策略约束  
- `vpc_endpoint`: 字符串，用于指定私网访问 endpoint（仅专属版有效），格式为 `https://<instance-id>.<region>.aliyuncs.com`  
- `audit_log_enabled`: 布尔值，开启后记录完整请求/响应日志（含脱敏后的 prompt 和 completion），日志保留 90 天，需配合 RAM 权限 `bailian:ListAuditLogs` 使用  

## 使用方式

- 权限管理通过 RAM 角色策略实现，最小权限原则推荐使用预置策略 `AliyunBaiLianFullAccess` 或自定义策略，参考 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)  
- 传输安全无需额外配置，所有公网 API 调用强制 HTTPS；私网访问需在创建专属版实例时勾选「启用 VPC 访问」并绑定目标 VPC  
- 内容安全过滤支持按模型维度开关（通过 `enable_content_safety`），但不可绕过平台级涉政、暴恐、违禁类实时拦截策略  

## 限制和注意事项

- 私网访问不支持跨地域调用，`vpc_endpoint` 必须与实例所在 Region 严格一致；若文档中提及“支持跨 Region 私网互通”，属过时描述  
> **注意**：[传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 文档中关于“可选降级至 TLS 1.0”的说明已失效，当前全量强制 TLS 1.2+，该段落未同步更新  
- `audit_log_enabled=true` 时，日志中 system prompt 和 function call 参数默认不脱敏，需自行在应用层处理敏感字段  
- 模型备案信息公示页面（`/api/v1/model/filing`）仅返回当前账号下已备案模型列表，未备案模型调用将返回 `403 Forbidden`，而非静默降级

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


