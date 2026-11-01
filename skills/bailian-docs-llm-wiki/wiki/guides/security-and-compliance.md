# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向生产环境设计，支持开发者在满足国内监管要求（如《生成式人工智能服务管理暂行办法》）的同时，构建高可信的AI应用。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力对所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`）通用，[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，避免公网暴露；同时支持更严格的**安全存储业务空间**架构，通过 MSE 网关 + 反向终端节点 + 专有网络资源（OSS/ADB/ES）实现数据不出客户私网。后者需单独开通，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中启用 `X-DashScope-DataInspection`，对输入输出内容进行涉黄、涉政、广告等违规信息识别。该能力自动匹配调用模型类型（文本/图片），无需为不同模型单独配置策略。
- **模型备案**：所有上架模型均完成国家网信办算法备案及大模型备案，备案号在控制台及文档中公示，便于开发者用于应用上架合规申报。完整清单见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 13 中提及“万相”有两个备案主体（达摩院与通义云启），但文档 12 的表格未明确区分对应关系。实际使用时，请以 [互联网信息服务算法备案系统](https://beian.cac.gov.cn) 实时查询结果为准，避免因主体混淆导致备案材料不一致。

## 关键参数

| 参数名 | 用途 | 示例值 | 来源文档 |
|--------|------|--------|----------|
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | 启用 SDK 自动加密（含公钥获取、AES 密钥生成、加解密） | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，JSON 字符串格式 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密模式下，携带加密后的 AES 密钥（Base64 编码） | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 从 `/api/v1/public-keys/latest` 接口获取，用于手动加密流程 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

### 1. 传输加密（推荐 SDK 自动模式）
- 安装 DashScope SDK ≥ 2.0.1（Python）或 ≥ 2.12.0（Java）；
- 在 `Generation.call()` 或 `chat.completions.create()` 调用中设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入请求头，响应自动解密。

### 2. 私网访问（两种路径）
- **标准 PrivateLink**：在百炼控制台「网络配置」添加私网连接 → 关联业务空间 → 替换 API `base_url` 为私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。适用于通用模型调用。
- **安全存储业务空间**：需先开通专属业务空间类型，再依次完成：[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) → [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) → [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) → [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)。适用于对数据驻留有强要求的企业级场景。

### 3. AI 安全护栏
- 开通服务并授权（需主账号操作）；
- 在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；
- 响应返回 `400` + `data_inspection_failed` 错误码表示拦截，无额外响应体。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理的最小单元，**默认业务空间无法设置模型调用/训练/部署限制**，仅可对自建业务空间进行精细化管控。超级管理员可跨空间管理，但 RAM 用户的 OpenAPI 权限（如知识库、Prompt 工程）需主账号在 RAM 控制台单独授权，[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 文档明确指出此限制。
- **API Key 绑定**：单个 API Key 严格绑定一个地域、一个业务空间、一个用户，不可迁移。自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号。
- **加密限制**：DashScope SDK 加密仅支持 Java 和 Python；HTTP 手动加密需自行实现密钥管理与加解密逻辑，且不支持自定义 RSA 密钥对。
- **安全存储业务空间依赖**：OSS/ADB/ES 任一组件停止服务或被释放，将导致整个安全存储业务空间不可用且**无法恢复**，必须重建空间。
- **合规责任主体**：阿里云百炼提供模型备案信息与技术支撑，但根据《生成式人工智能服务管理暂行办法》，**应用/小程序开发者自身是法定的服务提供者，须独立承担内容审核、用户保护、标识规范等全部法定义务**。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


