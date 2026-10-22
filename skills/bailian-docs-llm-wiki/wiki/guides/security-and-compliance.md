# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、网络隔离、内容审核、权限管控、数据隐私及监管备案等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等法规要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了混合加密流程。
- **私网访问**：支持通过 PrivateLink 在 VPC 内直连百炼 API，流量全程走阿里云内网，规避公网暴露风险。该能力覆盖华北2（北京）、华东2（上海）等 6 个主流地域，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供完整配置路径。
- **AI 安全护栏**：默认启用基础内容过滤，同时支持按需接入 AI 安全护栏服务，对输入输出执行细粒度涉黄、涉政、广告等违规内容识别。该服务与模型强绑定，调用时需显式设置 `X-DashScope-DataInspection` 请求头，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高合规要求场景（如金融、政务），提供独立部署的“安全存储业务空间”，支持对接客户自有 VPC 内的 OSS、ADB、ElasticSearch 等资源，实现数据不出域。该能力需商务开通，配置流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 类型 | 作用 | 示例值 | 来源文档 |
|--------|------|------|--------|----------|
| `X-DashScope-DataInspection` | Header (JSON string) | 启用 AI 安全护栏，控制输入/输出检查策略 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption` / `enableEncrypt` | Boolean (SDK) | 启用端到端 AES+RSA 混合加密 | `True` / `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | Header (Base64) | 手动加密模式下传递 RSA 加密后的 AES 密钥 | `AQABAAE...` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `public_key_id` | Response field | 标识当前生效的 RSA 公钥版本，用于密钥轮换 | `"1"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

> **注意**：`X-DashScope-DataInspection` 的值必须是 JSON **字符串**（即双引号需转义），而非嵌套 JSON 对象。错误写法如 `{"input":"cip"}`（未转义）将导致 400 错误，正确写法为 `"{"input":"cip","output":"cip"}"`。

## 使用方式

- **加密调用（推荐）**：使用 DashScope SDK（Python/Java ≥1.14.0 / ≥2.12.0）并设置 `enable_encryption=True` 或 `.enableEncrypt(true)`。SDK 自动完成公钥获取、AES 密钥生成、加解密及请求头封装，无需手动处理 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 接口。
- **私网调用**：在百炼控制台 **管理 > 网络配置** 中添加私网连接，关联目标业务空间后，将 API 请求的 `base_url` 域名替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。注意：私网域名仅在对应 VPC 内可解析。
- **安全护栏启用**：开通服务并完成授权后，在每次请求 Header 中添加 `X-DashScope-DataInspection`。若未设置，护栏不生效；若设置但内容非法（如非字符串 JSON），请求将被拒绝。
- **安全存储空间配置**：需先申请开通，再依次完成反向终端节点创建、可用区 VIP 配置、OSS/ADB/ES 资源授权与 MSE 网关路由配置。全流程依赖 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 及其子文档。

## 限制和注意事项

- **API Key 归属不可迁移**：单个 API Key 严格绑定一个地域、一个业务空间和一个用户，无法转移。自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号，RAM 用户需通过主账号授权才能使用。
- **默认业务空间无细粒度管控**：默认业务空间无法设置模型调用限流、训练/部署授权，所有模型均可自由调用。精细化权限（如按模型限流、按用户页面权限）仅在**自定义业务空间**中生效，详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限需主账号授权**：RAM 用户默认无权调用知识库、Prompt 工程等 OpenAPI，必须由阿里云主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 等系统策略。
- **安全存储空间强耦合地域与网络**：目前仅支持“华北2（北京）”地域，且专有网络必须满足可用区 G/H/L 组合、交换机网段等硬性约束。其他地域暂不支持该模式。
- **合规备案责任主体明确**：阿里云作为“服务技术支持者”已为千问、万相等模型完成算法备案（备案号见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)），但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、标识规范等全部法定义务。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)


