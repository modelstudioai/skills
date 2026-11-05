# security and compliance

百炼平台提供多层次安全与合规能力，覆盖模型调用全链路，包括传输加密、权限控制、内容安全过滤、私网访问支持及监管要求的备案能力。所有能力均默认启用或按需配置，开发者需结合业务场景合理选用。具体实现细节请参考 [安全合规](../../raw/model-user-guide/security-and-compliance.md) 文档。

## 支持的模型/功能

- 所有百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio）均默认集成输入/输出 AI 安全护栏，支持敏感词识别、涉政/暴恐/色情等多类风险内容拦截；  
- 私网访问（VPC 内网直连）支持全部公有云区域下的模型服务调用，需配合 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 完成 VPC 绑定与安全组策略设置；  
- 模型备案信息公示与应用合规备案能力仅适用于中国大陆地域部署的生产环境应用，详情见 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 关键参数

- `enable_content_safety`: 布尔值，默认 `true`，控制是否启用输入输出内容安全过滤（影响响应延迟约 50–200ms）；  
- `vpc_endpoint`: 字符串，用于指定私网调用 endpoint（格式为 `https://<service-id>.<region>.aliyuncs.com`），需与已配置的 VPC 及安全组匹配；  
- `compliance_filing_id`: 字符串，仅在中国大陆地域调用时生效，用于关联已提交的 AI 应用备案编号，该字段不校验合法性，但缺失可能导致监管审计失败。

## 使用方式

1. 启用内容安全：在 `ChatCompletion` 或 `Completions` 请求中显式传入 `"enable_content_safety": true`（即使为默认值，也建议显式声明以明确意图）；  
2. 配置私网访问：先在控制台完成 VPC 授权与 endpoint 创建，再将请求 URL 替换为 `vpc_endpoint` 值，并确保客户端所在 ECS 实例处于同一 VPC；  
3. 关联备案信息：在调用 `CreateApp` 或更新应用元数据时，通过 `compliance_filing_id` 字段填入备案号，该 ID 将透传至审计日志与模型服务调用上下文。

## 限制和注意事项

- 内容安全过滤不支持自定义规则集或白名单豁免，如需绕过（仅限测试环境），须申请临时白名单权限，详见 [输入输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)；  
- 私网 endpoint 不支持跨地域调用，且无法与公网 endpoint 混用同一 AccessKey；  
- > **注意**：[传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 文档中提及“TLS 1.1+ 即可”，但实际平台强制要求 TLS 1.2+，低于该版本的客户端连接将被拒绝，此为平台强制升级策略，非文档过时；  
- > **注意**：[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md) 中列出的 GDPR 适用条款，仅适用于欧盟境内用户直接调用百炼 API 的场景；若通过中国境内企业代理调用，则适用《个人信息保护法》（PIPL），而非 GDPR；  
- 模型备案信息公示页面（`/api/v1/model/filing`）返回的数据为只读快照，每日凌晨同步一次，不支持实时查询最新备案状态。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


