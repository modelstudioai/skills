# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖身份权限、传输加密、内容安全、模型备案、数据隐私及泄漏防控等关键环节。所有功能均面向企业级开发者设计，支持精细化策略配置与自动化风险响应，满足国内监管要求（如《生成式人工智能服务管理暂行办法》）及国际标准（如 SOC 2）。开发者需结合自身业务场景，在权限隔离、凭证管理、网络通道和内容审核四个维度主动实施控制。

## 支持的模型/功能

- **AI 安全护栏**：仅在华北2（北京）地域可用，支持文本与图片类模型的输入/输出内容检测（涉黄、涉政、广告等），需显式通过 `X-DashScope-DataInspection` 请求头启用 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输**：支持 AES-RSA 混合加密机制，对请求体中 `input` 字段（含 `messages`）端到端加密，SDK 自动处理密钥获取与加解密流程；也可通过 HTTP 手动调用 `/api/v1/public-keys/latest` 接口获取公钥 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **私网访问**：支持 PrivateLink 私网连接（VPC 内网直连），适用于生产环境高安全要求场景；另提供“安全存储业务空间”专属方案，需配合 MSE 网关、ADB/ES/OSS 等私有网络资源部署 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入百炼的模型均完成国家网信办算法备案及大模型备案，备案号公示于控制台及文档，开发者可直接用于应用上架合规申报 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 14 明确指出 AI 安全护栏“仅华北2（北京）地域可用”，但文档 1 中超级管理员全局管理菜单列出的地域包括新加坡、弗吉尼亚、法兰克福、中国香港等，这些地域**不支持**该功能。开发者在跨地域部署时须注意此限制，不可假设功能全域一致。

## 关键参数

| 参数 | 说明 | 来源/约束 |
|------|------|-----------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串，如 `{"input":"cip","output":"cip"}` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密请求中封装 AES 密钥的请求头（由 SDK 自动注入） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True` (Python) / `enableEncrypt=true` (Java) | DashScope SDK 启用传输加密的开关参数 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `expire_in_seconds` | 临时 API Key 有效期（秒），取值范围 1–1800，需按最小必要原则设置 | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |

## 使用方式

- **权限控制**：基于业务空间（Workspace）实现最小粒度隔离。超级管理员可跨空间管理模型授权、限流（请求数/[Token](../concepts/token.md)）、训练与部署权限；业务空间管理员仅能管理本空间内用户、页面权限及 API Key；普通用户仅能使用被授权的模型与页面 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 管理**：
  - 创建时即绑定单一地域+业务空间+用户，不可迁移；
  - 支持 IP 白名单（最多 20 个）与模型范围限制（最多 30 个，受业务空间已授权模型约束）；
  - 生产环境必须使用临时 Key（`st-` 前缀）或私网连接，禁用长期 Key 直连前端。
- **传输加密接入**：
  - SDK 方式：安装 ≥2.0.1（Python）或 ≥2.12.0（Java）版本 DashScope SDK，设置 `enable_encryption=True` 即可，无需手动处理公钥；
  - HTTP 方式：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再用 RSA 加密 AES 密钥，用 AES 加密 `input` 字段。
- **私网调用**：
  - 普通私网连接：在控制台「网络配置」添加 PrivateLink，关联业务空间后使用 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com` 域名；
  - 安全存储业务空间：需完整走「配置终端节点→配置可用区IP→配置OSS/ADB/ES→配置MSE网关→激活」流程，适用于金融、政务等强合规场景。

## 限制和注意事项

- **地域限制明确**：AI 安全护栏、部分安全存储能力（如文档 9–12 描述的配置流程）仅支持华北2（北京）；其他地域（如新加坡、弗吉尼亚）虽可创建业务空间，但无法启用这些安全功能。
- **API Key 生命周期独立**：2026 年 3 月 25 日起创建的 Key **不会因归属 RAM 用户被删除而级联失效**，必须显式重置或删除 Key 本身 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **推理日志不可追溯历史**：开启前的调用无日志；关闭期间不补录；且需额外开通 SLS 并承担日志服务费用，非默认启用 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **加密不替代凭证保密**：即使启用 AES-RSA 加密，若 API Key 泄漏，攻击者仍可在有效期内从合法出口 IP 发起加密调用；IP 白名单仅缩小攻击面，不能替代 Key 轮换与环境加固。
- **备案责任主体不变**：阿里云提供模型备案号与合作协议模板，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


