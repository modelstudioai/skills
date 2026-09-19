# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限控制、模型备案及隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 方式**：通过终端节点（Endpoint）将 VPC 与百炼服务直连，流量全程走阿里云内网，适用于通用模型/API 调用 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **安全存储空间方式**：专为高合规要求客户设计，需配合 MSE 云原生网关、ADB/ElasticSearch/OSS 等资源构建全链路私有网络，适用于金融、政务等强隔离场景 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)。
- **AI 安全护栏**：支持输入/输出双路内容审核（CIP），可识别涉政、涉黄、广告等违规内容，需显式通过 `X-DashScope-DataInspection` 请求头启用。
- **模型备案**：所有预置模型（如千问、万相、DeepSeek 等）均已取得国家网信办算法备案号及大模型备案号，详情见公示列表 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 14 中提到“万相”对应两个不同备案主体（达摩院与通义云启）和两个备案号，而文档 11 仅列出三个万相相关备案号但未明确区分适用场景。实际使用时，请严格按调用的具体模型版本（如 `wanxiang-v1` 或 `wanxiang-video`）匹配文档 14 中的备案主体与编号，避免混用。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `X-DashScope-DataInspection` | Header (JSON string) | 启用 AI 安全护栏，指定 input/output 审核策略 | `{"input":"cip","output":"cip"}` |
| `X-DashScope-EncryptionKey` | Header (base64) | HTTP 手动加密模式下，携带 RSA 加密后的 AES 密钥 | `base64(encrypted_aes_key)` |
| `enable_encryption=True` | SDK 参数 | DashScope Python SDK 启用自动加解密 | — |
| `enableEncrypt=true` | SDK 参数 | DashScope Java SDK 启用自动加解密 | — |
| `public_key_id`, `public_key` | Response body | 从 `/api/v1/public-keys/latest` 接口获取，用于手动加密流程 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` |

## 使用方式

1. **启用传输加密**  
   - SDK 方式（推荐）：安装最新版 DashScope SDK，调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动完成公钥获取、AES 密钥生成、加解密全流程。  
   - HTTP 方式：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再用其加密 AES 密钥，最后将加密后密钥（`X-DashScope-EncryptionKey`）和加密后 `input` 发起请求 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

2. **配置私网访问**  
   - PrivateLink：在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加连接，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换 API `base_url` 即可。  
   - 安全存储空间：需依次完成「创建安全存储业务空间 → 配置反向终端节点 → 配置可用区 VIP → 配置 OSS/ADB/ES → 配置 MSE 网关 → 激活」全流程，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

3. **启用 AI 安全护栏**  
   - 在安全管理页面开通并授权服务；  
   - 调用时在请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`；  
   - 违规请求将返回 `400` 及 `data_inspection_failed` 错误码。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理的最小单元，**默认业务空间无法设置模型调用/训练/部署限流**，仅超级管理员可在全局管理菜单中为非默认空间配置 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 绑定**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可转移；自 2026年3月25日起，华北2（北京）地域新创建的 API Key 均归属主账号。
- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储空间方案当前仅支持华北2（北京）。
- **OSS/ADB/ES 依赖**：安全存储空间激活后，若关联的 OSS Bucket 被释放或 ADB/ES 实例停止计费，将导致整个安全存储空间不可用且**无法恢复**，必须重建空间。
- **合规责任主体**：阿里云百炼作为“服务技术支持者”提供模型备案信息，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案（如适用）等全部法定义务。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)


