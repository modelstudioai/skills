# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者通过配置、API 或控制台按需启用，无需修改核心业务逻辑。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，密钥通过平台托管的 RSA 公钥安全分发，适用于敏感数据场景。该能力对所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`）通用，[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：提供两种私网方案：
  - **PrivateLink 方式**：适用于标准业务空间，通过终端节点将 VPC 流量直连百炼网关，支持华北2（北京）、华东2（上海）等 6 个地域，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 是主要接入路径；
  - **安全存储空间方案**：专为高合规要求客户设计，需配置反向终端节点、MSE 网关及私有云资源（OSS/ADB/ES），仅限“华北2（北京）”地域，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持对输入输出内容进行实时合规检测（涉黄、涉政、广告等），需显式在请求头中设置 `X-DashScope-DataInspection`，目前覆盖文本和图片类模型，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 提供完整调用示例。
- **模型备案信息**：所有预置大模型（千问、万相、DeepSeek、Moonshot 等）均已完成国家网信办算法备案及大模型备案，备案号及主体信息在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中公开可查，开发者可直接用于应用上架合规申报。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | boolean | SDK 启用传输加密的开关 | `True`（Python）、`true`（Java） |
| `X-DashScope-EncryptionKey` | string | HTTP 调用时携带的 AES 密钥密文（Base64 编码） | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `X-DashScope-DataInspection` | string (JSON) | AI 安全护栏策略，值为 JSON 字符串而非对象 | `'{"input":"cip","output":"cip"}'` |
| `base_url` | string | 私网调用时需替换为 PrivateLink 域名或安全存储空间专属域名 | `"https://ws-xxx-vpc-yyy.cn-beijing.maas.aliyuncs.com/api/v1"` |
| `public_key_id` | string | 从 `/api/v1/public-keys/latest` 接口获取的公钥标识 | `"1"` |

> **注意**：文档 6（`secure-storage.md`）将私网访问归类为“安全存储”，但其实际内容与文档 2（`transmission-security.md`）中的 PrivateLink 属于不同技术栈：前者是面向安全存储业务空间的反向终端节点方案，后者是面向通用业务空间的 PrivateLink 方案。二者不可混用，开发者应根据业务空间类型（普通 or 安全存储）选择对应文档。

## 使用方式

- **传输加密**：推荐使用 DashScope SDK（Java/Python），仅需设置 `enable_encryption=True`，SDK 自动完成公钥获取、AES 密钥生成、加解密全流程；若需手动管理密钥，须先调用 [`GET /api/v1/public-keys/latest`](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 获取公钥，再自行实现混合加密。
- **私网访问**：
  - 普通业务空间：在控制台 **设置 > 网络配置 > VPC私网访问** 添加 PrivateLink，关联业务空间后获取 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com` 格式域名，替换 SDK 或 OpenAI 兼容模式的 `base_url` 即可。
  - 安全存储空间：需依次完成 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) → [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) → [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) → [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) 四步，最终通过 MSE 网关路由访问 OSS/ADB/ES。
- **AI 安全护栏**：开通服务后，在请求头中添加 `X-DashScope-DataInspection`，值为 JSON 字符串（注意双引号转义）。DashScope SDK 需通过自定义 `http_client` 注入 header；OpenAI SDK 可直接在 `extra_headers` 中传入。

## 限制和注意事项

- **权限粒度**：业务空间是权限最小管理单元，**默认业务空间无法设置模型调用/训练/部署限制**，所有模型均可无限制使用；精细化管控必须在新建的非默认业务空间中配置。
- **API Key 生命周期**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 归属主账号，与 RAM 用户解耦；此前创建的 RAM 用户级 API Key 在删除用户时将被同步清除且不可恢复，[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md) 文档明确提示了该变更风险。
- **地域限制**：
  - PrivateLink 私网访问仅支持 6 个地域（北京、上海、杭州、深圳、乌兰察布、张家口），不支持中国香港、新加坡等国际地域；
  - 安全存储空间方案强制要求“华北2（北京）”地域，且专有网络可用区仅限 G/H/L。
- **合规责任边界**：阿里云百炼提供模型备案信息及基础设施合规资质（如 SOC 2），但根据《生成式人工智能服务管理暂行办法》，**应用开发者作为“服务提供者”需独立承担内容审核、用户权益保障、算法备案（如适用）等全部法定义务**，[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 文档强调了此责任划分。

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
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


