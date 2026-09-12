# security and compliance

百炼平台提供端到端的安全与合规能力，覆盖模型调用、数据传输、访问控制、内容安全及监管备案等关键环节。所有能力均基于阿里云整体安全体系构建，并符合中国法律法规及行业监管要求。开发者需结合自身业务场景，合理配置参数并履行应用级合规义务。

## 支持的模型/功能

- **AI 安全护栏**：对输入输出内容进行实时检测与拦截，支持敏感词过滤、价值观对齐、违法不良信息识别等策略，适用于所有调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通义系列模型的 API 请求。  
- **私网访问与 VPC 隔离**：支持通过阿里云专有网络（VPC）调用模型服务，避免公网暴露，详见 [私网访问配置](../../raw/model-user-guide/security-and-compliance.md)。  
- **模型与应用双备案支持**：平台提供模型备案状态查询接口，并支持通过控制台提交 AI 应用合规备案材料，对应能力已在 [应用合规备案](../../raw/model-user-guide/security-and-compliance.md) 和 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance.md) 中明确说明。

## 关键参数

- `enable_security_guard`: 布尔值，默认 `true`，启用输入输出 AI 安全护栏；设为 `false` 仅在沙箱调试环境允许，生产环境强制开启。  
- `vpc_endpoint`: 字符串，指定私网调用 endpoint（如 `https://dashscope-vpc.aliyuncs.com`），需配合 RAM 角色和 VPC 授权策略使用。  
- `compliance_mode`: 枚举值（`standard` / `strict`），影响内容审核粒度，`strict` 模式下会增强对模糊表述、隐喻性风险内容的拦截强度，该行为定义见 [输⼊输出 AI 安全护栏](../../raw/model-user-guide/security-and-compliance.md)。

## 使用方式

1. 调用 `/v1/services/aigc/text-generation` 等接口时，在请求 Header 中携带已授权的 `Authorization` 凭据；  
2. 如需启用私网访问，将 `base_url` 替换为 `vpc_endpoint`，并确保调用方 ECS 实例位于同一 VPC 内；  
3. 对于需完成备案的应用，须在百炼控制台「应用管理 → 合规备案」中上传《生成式人工智能服务算法备案表》及安全评估报告，流程说明参见 [应用合规备案](../../raw/model-user-guide/security-and-compliance.md)。

## 限制和注意事项

- 私网访问不支持跨地域调用，`vpc_endpoint` 必须与实例所在 Region 严格匹配；  
- `enable_security_guard=false` 在生产环境会被平台自动重置为 `true`，不可绕过；  
- 模型备案状态以 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance.md) 页面实时公示为准，API 返回的 `model_filing_status` 字段仅作参考，最终以公示信息为准。  
> **注意**：原始文档中「[传输安全](../../raw/model-user-guide/security-and-compliance.md)」链接指向的官方帮助页实际描述的是 HTTPS/TLS 1.2+ 强制启用机制，但当前 API 网关已升级至 TLS 1.3 默认支持，旧文档未同步更新该细节，开发者应以实际抓包或 `curl -v` 验证为准。

## 来源文档

- [安全合规](../../raw/model-user-guide/security-and-compliance.md)


