# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均默认启用或按需配置，开发者可通过 API 参数、控制台策略或 SDK 集成方式生效。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、开源微调模型）均默认集成输入/输出 AI 安全护栏，支持敏感词过滤、涉政/暴恐/色情等内容识别与拦截  
- 私网访问（VPC 内网直连）、传输加密（TLS 1.2+）、细粒度权限管理（RBAC）为全模型通用能力  
- 模型备案信息公示与应用合规备案功能仅适用于在中国大陆地区部署并面向公众提供服务的 AI 应用，详见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)

## 关键参数

- `enable_content_safety`: 布尔值，控制是否启用输入/输出内容安全检测（默认 `true`）  
- `vpc_endpoint`: 字符串，指定私网访问域名（需提前在控制台配置 VPC 接入点），启用后自动绕过公网流量  
- `request_id_header`: 可选字符串，用于透传审计请求 ID 至后端日志系统，配合 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 中的 TLS 日志审计要求使用  

## 使用方式

- 权限管理通过 RAM 角色策略配置，最小权限原则下建议授予 `AliyunBailianFullAccess` 或自定义策略（参考 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）  
- 私网访问需在百炼控制台「网络设置」中绑定 VPC，并在 API 请求中显式指定 `vpc_endpoint`；未配置时自动降级至公网 TLS 连接  
- 内容安全策略不可关闭，但可通过 `content_safety_level`（`strict` / `balanced` / `relaxed`）调整检测强度（仅对部分模型开放，详见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)）

## 限制和注意事项

- 私网访问不支持跨地域调用：`vpc_endpoint` 必须与模型部署地域一致，否则返回 `403 Forbidden`  
- 启用 `enable_content_safety` 后，响应延迟平均增加 80–200ms，高并发场景需预留缓冲  
> **注意**：原始文档中 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 的文件名存在明显错误——该路径实际描述的是“私网访问”，但文件名误标为 `secure-storage.md`（应为 `vpc-access.md` 或类似），请以页面标题和内容为准，避免按文件名推测功能。  
- 模型备案信息公示为只读接口（`GET /v1/model/filing`），不支持开发者主动提交；备案状态变更需通过阿里云合规门户人工审核，非 API 自动同步。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


