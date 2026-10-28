# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地构建和部署大模型应用。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，密钥通过平台托管的 RSA 公钥安全分发，适用于敏感数据场景。该能力已集成至 DashScope SDK（Python/Java），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 终端节点**：适用于标准业务空间，通过 VPC 私网连接直连百炼 API 网关，流量全程内网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储业务空间**：专为高安全要求客户设计，需配置反向终端节点、MSE 云原生网关及专属云资源（ES/ADB/OSS），实现数据不出私有网络 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中启用输入/输出内容安全检测（`X-DashScope-DataInspection`），自动拦截涉黄、涉政、广告等违规内容，适用于文本与图片类模型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办算法备案号及大模型备案号，信息实时公示 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`）明确限定适用范围为“已开通百炼安全存储业务空间”的客户；而文档 5（`access-model-studio-through-privatelink.md`）面向通用业务空间，两者定位不同，不可混用。开发者应根据业务安全等级选择对应方案。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `enable_encryption=True`（Python） / `enableEncrypt=true`（Java） | 启用 SDK 自动加解密 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用输入与输出双路内容安全检测 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey`（HTTP Header） | 手动加密时封装加密后的 AES 密钥（Base64 编码） | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `Authorization: Bearer <API_KEY>` | 所有 API 调用必需的身份凭证 | `Bearer sk-xxx` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   安装最新版 DashScope SDK（Python ≥ 1.20.0，Java ≥ 2.12.0），调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）。SDK 自动完成公钥获取、AES 密钥生成、加解密及密钥传输，无需手动调用 `/api/v1/public-keys/latest` 接口。

2. **私网访问（二选一）**  
   - **通用业务空间**：在百炼控制台「设置 > 网络配置」中添加 PrivateLink，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换 API 请求中的 base_url 即可 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
   - **安全存储业务空间**：需按顺序完成四步配置：① 创建反向终端节点；② 配置 MSE 云原生网关及可用区 VIP；③ 将 VIP 加入安全组白名单；④ 授权并配置 ES/ADB/OSS 等后端资源 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

3. **AI 安全护栏**  
   在 API 请求 Header 中添加 `X-DashScope-DataInspection`，值为 JSON 字符串（非对象），例如 `{"input":"cip","output":"cip"}`。若检测失败，返回 HTTP 400 及 `data_inspection_failed` 错误码。

4. **合规备案材料获取**  
   应用上架所需算法备案号、主体信息及截图，可直接查阅 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 文档；完整备案系统查询指引见 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理的最小单元，**默认业务空间无法设置模型调用/训练/部署限制**，仅自建业务空间支持精细化授权 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 归属**：单个 API Key 严格绑定一个地域、一个业务空间和一个用户，不可跨空间或跨用户复用；自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **OpenAPI 权限隔离**：RAM 用户默认无权调用应用、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等 OpenAPI，必须由阿里云主账号在 RAM 控制台为其授予 `AliyunBailianDataFullAccess` 等特定策略 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间地域限制**：目前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据默认使用 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


