# security and compliance

百炼平台提供多层次安全与合规能力，覆盖模型调用链路中的权限控制、数据传输、网络隔离、内容安全及监管备案等关键环节。所有能力均基于阿里云整体安全体系设计，满足国内主流合规要求（如《生成式AI服务管理暂行办法》《个人信息保护法》）。开发者需结合自身业务场景，按需启用对应功能并配置相应参数。

## 支持的模型/功能

当前安全与合规能力适用于全部百炼托管模型（含 Qwen 系列、Qwen-VL、Qwen-Audio 等）及自定义微调模型，但部分能力对模型版本有依赖：  
- 输入输出 AI 安全护栏（内容过滤）支持所有 v2.0+ 模型；v1.x 模型需升级后方可启用 [输入输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)；  
- 私网访问配置仅对部署在专有网络（VPC）内的模型实例生效，不适用于公网直连模式；  
- 模型备案信息公示和应用合规备案为独立流程，与模型运行时能力解耦，需通过百炼控制台单独提交 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [应用合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 关键参数

调用 API 时可通过以下请求头或参数启用对应安全能力：  
- `X-Bailian-Security-Mode: strict`：启用严格内容安全策略（默认为 `basic`），触发更细粒度的敏感词与图像内容检测；  
- `X-Bailian-Private-Access: true`：强制走私网通道（需模型已配置 VPC 接入）；  
- `X-Bailian-Permission-Context: <role_arn>`：传递临时权限上下文，用于细粒度权限校验，依赖 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 中定义的角色策略。

## 使用方式

1. **传输安全**：所有 HTTPS 接口默认启用 TLS 1.2+ 加密，无需额外配置；若需双向证书认证，须在模型部署阶段开启 mTLS 并上传 CA 证书 —— 具体操作见 [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)；  
2. **内容安全**：在 `messages` 或 `input` 字段中传入用户原始内容后，系统自动执行过滤；返回结果中 `security_violation` 字段为 `true` 时，表示内容被拦截，响应体将不含 `output`；  
3. **私网访问**：需先在控制台为模型绑定 VPC 及安全组，再通过私网 Endpoint 调用，不可混用公网域名。

## 限制和注意事项

- 内容安全护栏不支持自定义规则集，仅可开关全局策略（`strict`/`basic`），如需定制化策略，请联系技术支持；  
- 私网访问下，模型实例无法主动访问公网（包括 OSS、RDS 等云产品），若需访问，须配置 NAT 网关或 PrivateLink；  
- > **注意**：[私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md) 文档标题存在误导——该文档实际描述的是 VPC 网络接入配置，而非“安全存储”；正确的能力归属应为网络层隔离，与对象存储加密无关；  
- > **注意**：[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md) 中引用的《百炼平台隐私政策》已于 2024 年 7 月更新，旧版 PDF 链接已失效，开发者应以控制台内嵌最新版为准；  
- 所有安全能力均不改变模型推理逻辑本身，仅作用于请求/响应边界，不影响 token 计费与延迟 SLA。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


