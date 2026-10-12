# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足国内监管要求（如《生成式人工智能服务管理暂行办法》）的同时，构建高可信的AI应用。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段的 AES-256 对称加密 + RSA 公钥封装密钥的混合加密机制，适用于所有文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，适用于华北2（北京）、中国香港地域的模型与应用 API 调用，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持输入/输出双路内容安全检测（涉黄、涉政、广告等），默认由模型自动匹配对应护栏服务，需显式设置 `X-DashScope-DataInspection` 请求头启用，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：专为高敏感场景设计，支持将知识库、审计日志等数据落库至客户私有 VPC 内的 OSS、ADB、Elasticsearch 等资源，需单独开通并完成完整配置流程，[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`）实际描述的是**安全存储业务空间**的私网接入方案，与文档 5 中面向通用模型调用的 PrivateLink 私网访问属不同产品形态和适用场景，不可混用。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `enable_encryption` / `enableEncrypt` | SDK 启用传输加密的布尔开关 | `True` (Python), `true` (Java) | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `'{"input":"cip","output":"cip"}'` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时携带 RSA 加密后的 AES 密钥的请求头 | Base64 编码字符串 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-IP-Whitelist` | API Key 级 IP 白名单（仅限 IPv4，美国弗吉尼亚地域） | `"192.168.1.0/24,203.0.113.5"` | [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) |

## 使用方式

### 1. 传输加密（推荐使用 SDK）
- Python：设置 `enable_encryption=True`，SDK 自动获取公钥、生成 AES 密钥、加解密 `input`；
- Java：设置 `.enableEncrypt(true)`；
- HTTP 手动调用：先调用 `/api/v1/public-keys/latest` 获取公钥，再自行实现混合加密逻辑，[获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 2. 私网访问
- 控制台操作：在 **管理 > 网络配置** 添加私网连接 → 在 **业务空间管理** 中关联目标空间 → 获取私网域名 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`；
- SDK 调用：将 `base_url` 或 `dashscope.base_http_api_url` 替换为私网域名（见文档 5 示例）。

### 3. AI 安全护栏
- 开通：在 AI 安全护栏购买页开通，并在百炼控制台 **安全管理 > 全局设置** 授权；
- 调用：在请求 header 中添加 `X-DashScope-DataInspection`，值为 `{"input":"cip","output":"cip"}`（字符串格式，非对象）。

### 4. 安全存储空间（高敏数据专用）
- 仅限已开通“安全存储空间”类型的业务空间；
- 必须按顺序完成：创建反向终端节点 → 配置可用区 VIP → 配置 OSS/ADB/ES → 配置 MSE 网关 → 激活空间，[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储空间仅支持华北2（北京）且需特定可用区（G/H/L）；[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key 绑定**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可转移；自 2026年3月25日起，华北2（北京）新创建的 API Key 均归属主账号，[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用应用、知识库、Prompt 工程等 OpenAPI，必须由阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 等策略，[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **模型备案责任**：阿里云公示所接入模型的算法备案号与大模型备案号，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担备案、安全评估、内容审核等全部法定义务，[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
- **数据隐私承诺**：百炼绝不会将您的输入数据用于模型训练；所有传输数据默认经 AES-256 加密；平台已通过 SOC 2 Type II 审计，[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

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


