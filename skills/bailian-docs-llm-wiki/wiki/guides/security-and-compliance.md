# security and compliance

阿里云百炼平台提供覆盖身份权限、传输加密、内容安全、模型合规与数据隐私的全栈安全能力，满足企业级AI应用在等保、GDPR、生成式AI监管等场景下的核心要求。所有安全机制均深度集成于控制台与API，开发者可通过最小权限配置、自动化密钥管理与声明式策略快速落地。

## 支持的模型/功能

- **AI 安全护栏**：仅在北京地域可用，支持对文本和图片类模型的输入/输出进行实时内容检测（涉黄、涉政、广告等），需通过 `X-DashScope-DataInspection` 请求头启用 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输**：支持 RSA+AES 混合加密，对 `input` 字段端到端加密，防止公网传输中敏感数据泄露；SDK 自动完成公钥获取与加解密流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持 PrivateLink 方式建立 VPC 到百炼服务的内网通道，流量全程不经过公网；同时支持安全存储业务空间专属架构（含 MSE 网关、ADB/OSS/ES 隔离资源） [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **模型备案**：所有上架模型均完成国家网信办算法备案与大模型备案，备案号及主体信息在控制台公示，可用于应用上架合规材料准备 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 文档依据 |
|------|------|--------|----------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，JSON 字符串格式 | `{"input":"cip","output":"cip"}` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption=True` (Python SDK) / `enableEncrypt=true` (Java SDK) | 启用自动 AES 加密的 SDK 参数 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `expire_in_seconds` | 临时 API Key 有效期（秒），取值范围 1–1800 | `300` | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |
| `X-DashScope-EncryptionKey` | HTTP 调用时携带加密后 AES 密钥的请求头 | `base64(encrypted_aes_key)` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |

> **注意**：文档 9 和文档 7 均描述私网连接，但文档 9（`secure-storage/configure-an-endpoint-and-initiate-a-connection.md`）聚焦“安全存储业务空间”这一特定高密场景，强制要求华北2（北京）地域及反向终端节点；而文档 7（`transmission-security/access-model-studio-through-privatelink.md`）面向通用模型/API 调用，支持北京、上海、深圳等多地域及标准 PrivateLink。二者适用范围与配置路径不同，非矛盾，开发者应按业务安全等级选择对应方案。

## 使用方式

- **权限隔离**：通过业务空间（Workspace）实现模型调用、训练、部署的权限与成本隔离；超级管理员可跨空间配置模型限流（QPS/[Token](../concepts/token.md)）、授权状态；业务空间管理员仅能管理本空间用户与页面权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **凭证管理**：
  - 生产环境必须使用长期 API Key + IP 白名单 + 模型范围限制；
  - 前端/客户端场景必须使用后端签发的临时 API Key（`st-` 前缀），有效期严格按需设置（建议 ≤300 秒）；
  - 所有 Key 必须通过环境变量或密钥管理服务（KMS）注入，禁止硬编码、截图、日志打印。
- **加密调用**：
  - SDK 用户：直接设置 `enable_encryption=True`，无需手动处理公钥；
  - HTTP 用户：先调用 `/api/v1/public-keys/latest` 获取最新 RSA 公钥，再用其加密 AES 密钥，最后用 AES 加密 `input` [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)；
- **私网接入**：
  1. 在百炼控制台「网络配置」开通 PrivateLink 并绑定 VPC；
  2. 将目标业务空间关联该私网连接；
  3. 替换 API `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅在北京地域可用；私网连接支持地域以控制台下拉列表为准（当前含北京、上海、深圳等 6 地域）；安全存储业务空间仅支持华北2（北京）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **Key 生命周期**：2026年3月25日后创建的 API Key **不会因归属 RAM 用户被删除而级联失效**，必须显式重置或删除 Key 本身 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **审计日志能力边界**：审计日志默认开启，含 Request ID、模型、[Token](../concepts/token.md) 用量、状态码，但**不包含 Prompt/Response 内容**；完整输入输出需提前开启推理日志并投递至 SLS，且仅对未来调用生效 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **数据主权承诺**：阿里云百炼绝不会将客户调用数据用于模型训练；所有传输数据默认 AES-256 加密；但调用日志（含脱敏后的 input/output）会按法规要求存储，详情见《阿里云百炼服务协议》数据条款 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


