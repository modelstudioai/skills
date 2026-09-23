# security and compliance

阿里云百炼平台提供端到端的[安全与合规](../concepts/security.md)能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，适用于敏感数据场景。该能力已集成至 DashScope SDK（Python/Java），调用时仅需设置 `enable_encryption=True` 即可启用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：提供两种私网方案：
  - **PrivateLink 方式**：通过终端节点服务（VPC Endpoint）实现 VPC 内资源直连百炼 API，流量全程内网，不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储空间方式**：专为高敏感业务设计，需配置反向终端节点、MSE 网关、可用区 VIP 及私有云资源（OSS/ADB/ES），形成全链路私有网络隔离 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)。
- **AI 安全护栏**：支持在请求头中注入 `X-DashScope-DataInspection` 参数，对输入输出内容进行实时违规识别（如涉政、涉黄、广告等），需提前开通并授权 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示，开发者可直接用于应用上架合规申报 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 5（`secure-storage.md`）标题为“私网访问配置”，但其子文档实际描述的是**安全存储业务空间**这一独立高安全等级产品形态，与文档 13 中通用型 PrivateLink 私网访问属不同架构层级。前者需商务开通、强制多可用区部署、绑定专属云资源；后者为标准 VPC 功能，控制台自助开通。二者不可混用，选型需依据安全等级要求。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption` / `enableEncrypt` | SDK 中启用传输加密的布尔开关 | `True`（Python）、`true`（Java） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密模式下，携带 RSA 加密后的 AES 密钥的请求头 | `Base64(RSA_encrypt(AES_key))` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `Authorization: Bearer <API_KEY>` | 所有 API 调用必需的身份凭证 | `Bearer sk-xxx` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **传输加密（推荐 SDK 自动模式）**  
   安装最新 DashScope SDK（≥1.14.0 Python / ≥2.12.0 Java），调用时传入 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）。SDK 自动完成公钥获取、AES 密钥生成、加解密全流程，响应体为明文。

2. **私网访问（二选一）**  
   - *通用 PrivateLink*：在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加连接，关联业务空间后，将 API 域名替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
   - *安全存储空间*：需商务开通后，按顺序执行：创建反向终端节点 → 配置可用区 VIP → 授权 OSS/ADB/ES → 配置 MSE 网关 → 激活空间 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

3. **AI 安全护栏**  
   在百炼控制台 **安全管理** 页面开通并授权服务，调用时在请求头添加 `X-DashScope-DataInspection` 参数。若检测到违规内容，返回 `400` 状态码及 `data_inspection_failed` 错误码。

4. **权限管控**  
   使用 RAM 用户 + 业务空间模型级授权。超级管理员通过全局管理菜单（如 [北京](https://bailian.console.aliyun.com/settings/workspace)）统一管控；业务空间管理员仅能管理所属空间内的模型调用/训练/部署限流及用户权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储空间当前仅支持华北2（北京），且专有网络必须包含可用区 G/H/L 中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **API Key 绑定约束**：单个 API Key 仅归属一个地域、一个业务空间、一个用户，不可迁移。自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储空间强依赖**：OSS Bucket 或 ADB/ES 实例一旦被释放，将导致整个安全存储空间**不可恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：使用百炼模型的应用/小程序，开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、标识规范等全部法定义务；阿里云仅提供模型备案号及合作协议模板，不替代开发者履行合规义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
- **加密兼容性**：传输加密仅作用于 `input` 字段（如 `messages`），不影响 `model`、`parameters` 等其他参数；不支持自定义 AES 密钥（SDK 模式）或非标准加密算法（HTTP 模式）[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


