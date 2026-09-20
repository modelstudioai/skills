# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、数据隐私及监管备案等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等法规要求的前提下，安全、可控地集成和调用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段的 AES-256 对称加密 + RSA 公钥封装密钥的混合加密机制，适用于敏感数据场景。该能力对所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`）通用，[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，避免公网暴露。当前仅华北2（北京）、中国香港地域支持，且需在百炼控制台完成网络配置与业务空间关联，详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出内容安全检测，覆盖涉黄、涉政、广告等高风险内容。该能力与模型自动绑定，目前支持文本和图片类模型，具体策略参见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高合规要求客户，提供独立部署的“安全存储业务空间”，支持通过反向终端节点、MSE 网关、OSS/ADB/ES 等私有资源构建全链路私网闭环，相关配置指南见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 用途 | 是否必需 | 说明 |
|--------|------|----------|------|
| `enable_encryption=True` (Python SDK) / `.enableEncrypt(true)` (Java SDK) | 启用传输加密 | 否（按需启用） | SDK 自动获取 RSA 公钥、生成 AES 密钥并完成加解密，无需手动管理密钥。 |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏 | 否（按需启用） | JSON 字符串格式，值为 `"cip"` 表示启用内容安全检查；可单独设 `"input":"cip"` 或 `"output":"cip"`。 |
| `X-DashScope-EncryptionKey` | 手动加密时传递加密后的 AES 密钥 | 是（HTTP 手动调用时） | 仅当不使用 SDK 自动加密时需手动构造，SDK 调用时由内部处理。 |
| `X-DashScope-IP-Whitelist` | API Key IP 白名单 | 否 | 在 API Key 管理页配置，美国（弗吉尼亚）地域仅支持 IPv4。 |

> **注意**：文档 1 中提到“自 2026年3月25日开始，华北2（北京）地域的所有新创建的 API Key 均归属主账号”，但该日期明显为笔误（未来日期且无上下文支撑），实际应以控制台最新提示或官方公告为准。当前所有地域新 API Key 均可归属 RAM 用户，且受业务空间权限约束。

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   - 安装最新版 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）；  
   - 调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；  
   - SDK 自动完成公钥获取、AES 加密、密钥封装与响应解密，返回明文结果。

2. **私网访问**  
   - 在百炼控制台 **管理 > 网络配置** 开通 PrivateLink 并添加 VPC 连接；  
   - 在 **业务空间管理** 中将目标空间与私网连接关联；  
   - 将 API 请求域名替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

3. **AI 安全护栏**  
   - 先在 **安全管理** 页面开通并授权服务；  
   - 在模型调用请求头中添加 `X-DashScope-DataInspection`；  
   - 若触发拦截，响应状态码为 `400`，`code` 字段为 `data_inspection_failed` 或 `DataInspectionFailed`。

4. **权限控制**  
   - 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 的 RAM 用户）可在全局管理菜单中跨空间管理模型调用/训练/部署权限、API Key 及用户；  
   - 业务空间管理员仅能管理本空间内用户权限与页面可见性，**不能管理 OpenAPI 接口权限**（该权限必须由主账号在 RAM 控制台单独授予）；  
   - 普通用户权限完全由所属空间的模型授权与页面权限决定，API Key 权限与其归属空间一致，不受其账号控制台权限影响。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储业务空间当前仅支持华北2（北京）地域，且专有网络可用区限定为 G/H/L。
- **模型覆盖范围**：AI 安全护栏服务与模型强绑定，不同模型对应不同算法备案号，上架合规备案时须按实际调用模型提供对应备案信息，详见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 和 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据默认经 AES-256 加密，符合 SOC 2 审计标准，详情见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
- **API Key 生命周期**：RAM 用户的 API Key 在其被移出业务空间后立即失效（重新加入可恢复），但在 RAM 控制台删除该 RAM 用户后，API Key 将永久失效且不可恢复。
- **安全存储空间依赖强耦合**：OSS/ADB/ES 任一组件停止服务或被释放，将导致整个安全存储业务空间不可用且无法恢复，需严格保障底层资源稳定性。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


