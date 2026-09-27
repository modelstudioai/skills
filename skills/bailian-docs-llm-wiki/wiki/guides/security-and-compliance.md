# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、网络隔离、内容风控、模型备案、权限管控及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段（含 `messages` 等核心请求体）进行 AES-RSA 混合加密，全程密文流转，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过阿里云 PrivateLink 建立 VPC 内网直连，流量全程不经过公网，适用于金融、政务等强网络隔离需求场景 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持输入输出双路内容安全检测（涉黄、涉政、广告等），需显式设置 `X-DashScope-DataInspection` 请求头启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高敏感业务提供独立部署的“安全存储业务空间”，支持对接客户私有 VPC 内的 OSS、ADB、ElasticSearch 等资源，实现数据不出域 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入的千问、万相、DeepSeek 等主流模型均已完成国家网信办算法备案及大模型备案，并公示备案号与主体信息 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 5（安全存储空间）与文档 3（PrivateLink 私网访问）虽同属网络隔离方案，但适用范围不同：前者为专属安全空间（需商务开通），后者为通用业务空间的可选网络模式。二者不可混用，且安全存储空间的私网接入流程（反向终端节点 + MSE 网关）与通用 PrivateLink（正向终端节点）在控制台路径、组件依赖和配置步骤上存在本质差异，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 与 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 关键参数

| 参数名 | 类型 | 说明 | 文档依据 |
|--------|------|------|----------|
| `enable_encryption` / `enableEncrypt` | boolean | SDK 启用传输加密的开关，设为 `true` 后自动完成 AES 密钥生成、RSA 公钥获取、加解密全流程 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | string | HTTP 调用时携带加密后 AES 密钥的请求头（仅手动加密场景使用） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | JSON string | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}` 格式的字符串（非对象） | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `public_key_id` & `public_key` | string | 通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据，用于手动加密场景 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **传输加密（推荐 SDK 方式）**：安装最新版 DashScope SDK（Java ≥2.12.0 / Python ≥1.14.0），调用 `Generation.call()` 时传入 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动处理公钥拉取、AES 加密、密钥封装与响应解密。
- **传输加密（HTTP 手动方式）**：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再用该公钥加密 AES 密钥，最后将加密后的 `input` 和密钥放入 `X-DashScope-EncryptionKey` 头中发送请求。
- **私网访问**：在百炼控制台「网络配置」中添加 PrivateLink 私网连接，关联目标业务空间，获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），并在 SDK 或 OpenAI 兼容客户端中替换 `base_url`。
- **AI 安全护栏**：开通服务并完成授权后，在请求头中添加 `X-DashScope-DataInspection: "{\"input\":\"cip\",\"output\":\"cip\"}"`；若检测失败，返回 `400` 及 `data_inspection_failed` 错误码。
- **安全存储空间**：需商务开通后，在控制台创建「安全存储空间」→ 配置反向终端节点 → 创建 MSE 网关 → 配置可用区 VIP → 授权 OSS/ADB/ES → 激活空间，全过程需严格遵循 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 等系列文档。

## 限制和注意事项

- **加密能力限制**：DashScope SDK 的自动加密仅支持 Java 和 Python；其他语言必须使用 HTTP 手动加密流程。SDK 不支持自定义 AES 密钥，如需完全自主密钥管理，请参考 [HTTP调用（手动密钥管理）](https://help.aliyun.com/zh/model-studio/encrypted-access-to-model-inference#f9489ce581691)。
- **私网地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储空间当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个。
- **API Key 权限边界**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，其模型调用权限、限流策略完全继承自所属业务空间的配置，与用户账号的控制台页面权限无关 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **数据隐私承诺**：阿里云百炼明确承诺**绝不会将您的输入数据用于模型训练**，所有传输数据默认经 AES-256 加密；但根据协议，调用日志等运营数据仍会按需存储，详情见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
- **备案责任主体**：使用百炼接入的模型（如千问）虽已由阿里云完成算法备案，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，仍须独立承担内容审核、用户保护、标识规范等全部法定义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)


