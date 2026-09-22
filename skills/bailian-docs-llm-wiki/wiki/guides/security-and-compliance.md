# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节，满足企业级AI应用在等保、GDPR、《生成式AI服务管理暂行办法》等框架下的落地要求。所有能力均通过平台原生配置或API参数启用，无需额外部署。开发者需结合自身业务场景选择适配的防护层级和备案路径。

## 支持的模型/功能

- 所有百炼托管模型（包括Qwen系列、Qwen-VL、Qwen-Audio等）均默认启用输入/输出内容安全护栏，支持敏感词过滤、涉政/暴恐/色情等多类风险识别；详情见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)  
- 权限管理功能支持RAM角色策略、模型级细粒度授权及审计日志导出，适用于多租户隔离场景；详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)  
- 私网访问能力仅对VPC内资源开放，需配合专有网络与安全组策略使用；配置说明见 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)  

## 关键参数

- `enable_content_moderation`: 布尔值，控制是否启用输入/输出内容安全检测（默认 `true`）  
- `response_filter_level`: 字符串，取值 `low`/`medium`/`high`，影响过滤严格度（仅当 `enable_content_moderation=true` 时生效）  
- `vpc_endpoint_id`: 字符串，指定私网访问所用的VPC终端节点ID（启用私网访问时必填）  
- `compliance_filing_id`: 字符串，AI应用上线前必须提交并关联已备案的应用ID；参见 [应用合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)  

## 使用方式

1. 在创建模型服务实例时，于「安全配置」页签勾选对应能力（如内容审核、私网访问）  
2. 调用API时，将上述关键参数作为请求体字段传入（如 `POST /v1/services/qwen/chat`）  
3. 模型备案信息可通过控制台「合规中心」查看，亦支持通过OpenAPI获取；具体接口说明见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)  

## 限制和注意事项

- 内容安全护栏不支持自定义规则库，仅可调节预置策略等级；若需定制化策略，须通过独立内容审核服务对接  
- 私网访问配置后，公网Endpoint将自动失效，且不可与公网访问共存；该行为与 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md) 中TLS 1.2+强制加密的要求无冲突，但需注意网络连通性验证  
> **注意**：原始文档中 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 的标题存在歧义——实际该文档描述的是**私网访问（VPC Endpoint）配置**，而非“安全存储”；其文件路径名 `secure-storage.md` 已过时，正确语义应为 `vpc-access-configuration.md`，请以正文描述为准。  
- 应用合规备案为强制前置流程，未完成备案的应用无法通过百炼网关对外提供服务；备案材料需包含算法备案号、安全评估报告及隐私政策链接，详见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


