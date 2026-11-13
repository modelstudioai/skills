# security and compliance

阿里云百炼平台提供覆盖身份权限、传输加密、内容安全、模型合规与数据隐私的全栈安全能力，满足企业级AI应用在等保、GDPR、生成式AI监管等场景下的核心要求。所有安全机制均深度集成于控制台与API，开发者可通过精细化配置实现最小权限原则与纵深防御。

## 支持的模型/功能

- **模型级安全能力**：输入/输出AI安全护栏（仅华北2北京地域支持）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)，支持文本与图片类模型的实时违规内容识别（涉政、涉黄、广告等）。
- **模型备案信息**：所有接入百炼的官方及第三方大模型（如千问、万相、DeepSeek、Moonshot等）均完成国家网信办《生成式人工智能服务管理暂行办法》要求的算法备案与大模型备案，备案号可公开查询 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **传输加密支持**：所有模型调用均默认启用TLS 1.2+；敏感数据场景支持端到端AES-RSA混合加密（`input`字段加密），SDK开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：通过PrivateLink建立VPC内网直连通道，流量全程不经过公网，适用于金融、政务等高安全要求场景 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

> **注意**：AI安全护栏服务仅在北京地域可用，其他地域（如新加坡、弗吉尼亚）暂不支持该功能，且其开关需由超级管理员在全局管理菜单中开启 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 关键参数

| 参数 | 说明 | 使用方式 |
|------|------|----------|
| `X-DashScope-DataInspection` | 启用AI安全护栏的请求头，值为JSON字符串 `{"input":"cip","output":"cip"}` | 在HTTP请求头中显式设置，或通过业务空间维度全局开关启用 |
| `X-DashScope-EncryptionKey` | AES密钥经RSA公钥加密后的Base64编码值，用于端到端加密 | SDK自动处理；手动调用时需先调用 `/api/v1/public-keys/latest` 获取RSA公钥 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `expire_in_seconds` | 临时API Key有效期（秒），取值范围1–1800 | 调用生成临时API Key OpenAPI时传入，不可超过1800秒 |
| `Authorization: Bearer <API_KEY>` | 所有API调用必需的身份凭证 | 必须通过环境变量或密钥管理服务注入，禁止硬编码 |

## 使用方式

1. **权限配置**：  
   - 超级管理员通过全局管理菜单（[北京](https://bailian.console.aliyun.com/settings/workspace)等）统一管控多业务空间的模型调用/训练/部署权限与限流策略；  
   - 业务空间管理员在对应空间内配置RAM用户页面权限、模型授权状态及API Key管理；  
   - 普通用户仅能使用被明确授权的模型与功能 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

2. **API Key安全管理**：  
   - 生产环境必须使用**一业务一Key**原则，为不同应用/环境分配独立API Key，并绑定至专属业务空间；  
   - 敏感场景强制启用IP白名单（最多20个）与模型范围限制（最多30个）；  
   - 客户端直连必须使用后端签发的**临时API Key**（`st-`前缀），有效期按需设为最短必要时长。

3. **加密与私网接入**：  
   - 端到端加密：Python/Java SDK中设置 `enable_encryption=True` 或 `.enableEncrypt(true)` 即可自动完成RSA公钥获取、AES密钥生成与加解密；  
   - 私网访问：在百炼控制台「网络配置」中添加PrivateLink终端节点，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换原公网base_url即可调用。

## 限制和注意事项

- **地域限制**：AI安全护栏、部分私网连接功能（如安全存储业务空间）仅在北京地域提供；非北京地域创建的API Key无法启用护栏功能。
- **API Key生命周期**：2026年3月25日及之后创建的API Key**不会因归属RAM用户被删除而级联失效**，必须显式重置或删除Key本身 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **推理日志追溯性**：推理日志（含完整Prompt/Response）需**提前开启并投递至SLS**，开启前的历史调用无法补录；审计日志虽默认开启但不包含输入输出内容。
- **安全存储业务空间依赖强耦合**：OSS Bucket若被释放，将导致整个安全存储业务空间**不可恢复**；ADB/ES配置错误或中断将直接导致知识库、审计日志等功能不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **临时API Key权限继承**：其权限完全继承自签发它的长期Key，若需更小权限，必须先收窄长期Key的权限范围，而非在临时Key上做限制。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)


