# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-RSA 混合加密，适用于敏感数据场景；该能力已集成至 DashScope SDK（Java/Python），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：提供两种私网方案：
  - **PrivateLink 接入**：通过终端节点（Endpoint）将 VPC 与百炼网关直连，流量全程走阿里云内网，支持华北2（北京）、华东2（上海）等6个地域 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储业务空间**：专为高安全要求客户设计，需配置反向终端节点、MSE 网关及私有网络资源（OSS/ADB/ES），仅限申请开通的客户使用 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持输入/输出双路内容检测（CIP），可识别涉黄、涉政、广告等违规内容，需显式设置 `X-DashScope-DataInspection` 请求头启用 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有接入的千问、万相、DeepSeek、Moonshot 等主流模型均已取得国家网信办算法备案号及大模型备案号，信息实时公示于控制台与文档 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 12 中提及“万相”对应两个不同备案主体（达摩院与通义云启），但文档 10 的备案表中未明确区分适用场景。实际备案查询应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时结果为准，开发者需根据所用具体模型版本（如图像合成 vs 视频生成）匹配对应备案号。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用传输加密的开关，自动完成公钥获取、AES 密钥生成与加解密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非嵌套对象），必须严格转义 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密模式下，用于传递 RSA 加密后的 AES 密钥的请求头 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| 私网域名格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com` | 通过 PrivateLink 访问时必需替换的 base_url，仅在关联 VPC 内可解析 | [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) |

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   安装最新 DashScope SDK（≥2.0.1 for Python, ≥2.12.0 for Java），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，无需手动管理密钥或调用公钥接口。

2. **AI 安全护栏**  
   - 先在[安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1)页面完成服务开通与授权；  
   - 在 SDK 或 HTTP 请求头中添加 `X-DashScope-DataInspection`，值为 `{"input":"cip","output":"cip"}` 的字符串形式（注意引号转义）。

3. **PrivateLink 私网访问**  
   - 在百炼控制台 **设置 > 网络配置** 中开通私网连接并绑定 VPC；  
   - 编辑业务空间，在 **高级配置 > 私网连接** 中关联该连接；  
   - 获取私网域名（格式见上表），替换 SDK 或 HTTP 请求中的 `base_url`。

4. **安全存储业务空间（高安全场景）**  
   需商务侧申请开通，完整流程包括：创建反向终端节点 → 配置可用区 VIP → 部署 MSE 网关 → 配置 OSS/ADB/ES 资源 → 激活空间，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 及后续文档。

## 限制和注意事项

- **权限粒度**：默认业务空间无法设置模型调用/训练/部署的细粒度限流与授权，仅超级管理员或业务空间管理员可在自定义业务空间中配置 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 绑定**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可跨空间或跨用户转移；自 2026年3月25日起，华北2（北京）地域新创建的 API Key 均归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储依赖强耦合**：OSS Bucket 或 ADB/ES 实例若被释放，将导致安全存储业务空间**永久不可用且无法恢复**，必须重建空间 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **合规责任主体**：阿里云提供模型备案信息与技术支撑，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案（如适用）等全部法定义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据默认经 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


