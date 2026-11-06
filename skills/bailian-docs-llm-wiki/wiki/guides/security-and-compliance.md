# security and compliance

百炼平台提供多层次安全与合规能力，覆盖模型调用全链路，包括传输加密、权限控制、内容[安全过滤](../concepts/security-filter.md)、私网隔离及监管合规备案支持。所有能力均默认启用或按需配置，开发者需结合业务场景选择适配方案。详细机制参见 [安全合规](../../raw/model-user-guide/security-and-compliance.md)。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、开源微调模型）均默认集成输入/输出 AI 安全护栏，支持敏感词识别、违法信息拦截与价值观对齐过滤；  
- 私网访问能力适用于全部按需部署（Dedicated Instance）和专属集群（Private Cluster）模型实例；  
- 模型备案信息公示功能仅对已通过国家网信办备案的商用模型生效，具体清单见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；  
- 应用合规备案指引适用于基于百炼构建并面向公众发布的 AI 应用，详见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 关键参数

- `enable_content_safety`: 布尔值，控制是否启用输入/输出内容[安全过滤](../concepts/security-filter.md)（默认 `true`）；  
- `vpc_id` / `security_group_ids`: 配置私网访问时必需，用于绑定 VPC 和安全组；  
- `compliance_mode`: 枚举值（`standard` / `strict`），影响安全护栏的拦截阈值，默认为 `standard`；  
- `audit_log_enabled`: 布尔值，开启后记录完整请求/响应日志（含脱敏后的 prompt 和 completion），日志保留 90 天。

## 使用方式

1. **启用内容安全**：在调用 API 时显式传入 `enable_content_safety=true`（即使默认启用，也建议显式声明以确保行为可追溯）；  
2. **配置私网访问**：创建模型实例时，在控制台或 OpenAPI 中指定 `vpc_id` 和 `security_group_ids`，参考 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)；  
3. **审计日志**：通过 `audit_log_enabled=true` 开启，日志将投递至用户指定的 SLS Project；  
4. **权限最小化**：使用 RAM 子账号 + 自定义策略（如 `AliyunBailianFullAccess` 细粒度拆分版），避免主账号密钥泄露风险，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 限制和注意事项

- 内容[安全过滤](../concepts/security-filter.md)不支持自定义规则库，仅可调节 `compliance_mode` 参数；  
- 私网访问配置仅在模型实例创建时生效，创建后不可修改，需重建实例；  
- 传输安全（TLS 1.2+）强制启用，不可关闭，但客户端必须校验证书链，否则连接失败；  
> **注意**：原始文档中 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 提到“支持 TLS 1.0”，该描述已过时；当前生产环境仅支持 TLS 1.2 及以上版本，以符合等保三级要求。  
> **注意**：[私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 的文件名含 `secure-storage`，但实际内容描述的是网络层隔离（VPC），与存储加密无关，命名易引发误解，应以正文描述为准。  
- 所有安全能力均不降低模型推理性能 SLA，但 `strict` 合规模式可能增加平均延迟 50–200ms。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


