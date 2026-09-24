# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用链路中的权限控制、数据传输、网络隔离、内容安全及监管备案等关键环节。所有能力均默认启用或按需配置，开发者需结合业务场景主动启用对应策略。本文档汇总核心能力范围、配置方式及使用约束。

## 支持的模型/功能

当前安全与合规能力适用于全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）及通过 API 调用的自定义模型服务。具体包括：基于 RBAC 的细粒度权限管理、TLS 1.2+ 传输加密、VPC 私网访问支持、输入/输出实时内容安全过滤（含敏感词、涉政、暴恐等 12 类策略）、模型备案状态查询接口，以及 AI 应用上线前的合规备案引导流程。详见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)。

## 关键参数

- `security_level`: 可选 `basic` / `strict`，控制内容安全过滤强度（`strict` 启用全量策略并返回拦截原因）  
- `vpc_enabled`: 布尔值，启用后强制请求必须经由 VPC 内网路由（需提前配置私网访问白名单）  
- `compliance_filing_required`: 布尔值，设为 `true` 时 API 调用将校验应用备案号（仅限中国内地部署场景）  
- `audit_log_enabled`: 控制是否记录完整输入/输出至审计日志（默认关闭，开启后影响响应延迟）  

> **注意**：`security_level=strict` 在部分旧版 SDK 中未生效，建议升级至 v3.2.0+ 或直接通过 HTTP Header `X-Security-Level: strict` 显式传递，参见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 使用方式

1. 权限管理：通过 RAM 控制台为角色绑定 `AliyunBailianFullAccess` 或最小权限策略（如 `AliyunBailianContentSecurityReadOnlyAccess`）  
2. 私网访问：在模型部署页勾选「启用私网访问」，并在 VPC 安全组中放行目标端口（默认 443），参考 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)  
3. 内容过滤：无需额外配置，默认启用基础过滤；如需定制策略，需提交工单申请开通策略组管理权限  
4. 备案集成：调用 `/v1/applications/{app_id}/compliance/status` 接口可实时获取备案审核状态  

## 限制和注意事项

- 模型备案信息仅对已通过国家网信办备案的百炼官方模型有效，自定义微调模型需单独完成备案，详情见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)  
- VPC 私网访问不支持跨地域调用，且无法与公网 Endpoint 混用同一 AccessKey  
- 审计日志保留周期为 90 天，超期自动清除；若需长期留存，须自行对接 SLS  
- 传输安全（TLS）为强制启用，不支持降级为 HTTP；但客户端若未校验证书，可能绕过部分校验 —— 建议始终启用证书校验，参见 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


