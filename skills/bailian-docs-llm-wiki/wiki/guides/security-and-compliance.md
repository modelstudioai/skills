# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、网络隔离、权限控制、内容安全、模型备案及隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足国内监管要求（如《生成式人工智能服务管理暂行办法》）的同时，构建高可信的AI应用。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，密钥通过 RSA 公钥安全分发；适用于所有文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 提供完整流程说明。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内网直连百炼 API，流量全程不经过公网；当前仅限华北2（北京）、中国香港地域，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 为权威配置指南。
- **AI 安全护栏**：默认启用基础内容过滤，可选开通增强型 AI 安全护栏服务，对输入/输出进行涉黄、涉政、广告等多类风险识别；支持文本与图片模型，需显式设置 `X-DashScope-DataInspection` 请求头。
- **模型备案**：所有接入的千问、万相、DeepSeek 等主流模型均已取得国家网信办算法备案号及大模型备案号，[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 页面提供完整列表与查询方式。

> **注意**：文档 7 和文档 5 描述的私网连接机制存在定位差异——文档 5 面向通用模型/API 的 PrivateLink 接入（标准百炼业务空间），而文档 7 描述的是“安全存储业务空间”专用的反向终端节点方案，二者适用场景、控制台入口和配置路径均不同，不可混用。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `enable_encryption=True` (Python SDK) / `enableEncrypt=true` (Java SDK) | 启用自动混合加密（AES+RSA） | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用输入与输出双路内容安全检查 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 调用时携带的 RSA 加密后的 AES 密钥（Base64 编码） | `AQAA...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `Authorization: Bearer <API_KEY>` | 所有 API 调用必需的身份凭证 | `Bearer d1**2a` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

### 1. 传输加密（推荐 SDK 自动模式）
- Python：调用 `Generation.call()` 时传入 `enable_encryption=True`，SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥并完成加解密。
- Java：在 `GenerationParam.builder()` 中设置 `.enableEncrypt(true)`。
- HTTP 手动模式：先调用 `GET /api/v1/public-keys/latest` 获取 `public_key` 和 `public_key_id`，再自行实现 AES 加密 `input`、RSA 加密 AES 密钥，并通过 `X-DashScope-EncryptionKey` 头传递。

### 2. 私网访问
- **标准业务空间**：在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加 PrivateLink 连接，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换 API `base_url` 即可。
- **安全存储业务空间**：需额外配置 MSE 云原生网关、可用区 VIP、OSS/ADB/ES 白名单及授权角色（见文档 7–10），该流程独立于标准 PrivateLink，仅适用于已开通安全存储资质的客户。

### 3. AI 安全护栏
- 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 完成购买。
- 授权：在百炼控制台 **安全管理 > 全局设置** 页面点击“去授权”。
- 调用：在请求 Header 中添加 `X-DashScope-DataInspection`，值为 JSON 字符串 `{"input":"cip","output":"cip"}`（注意外层无嵌套，双引号需转义）。

### 4. 合规备案材料准备
- 应用上架前，需从 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 查询并截图对应模型的备案记录（如千问：`网信算备330110507206401230035号`）。
- 同时需与阿里云签署《大模型服务/合作协议》，协议需体现所用模型名称或备案编号，联系商务经理获取。

## 限制和注意事项

- **API Key 归属约束**：单个 API Key 仅归属一个地域内的一个业务空间和一个用户，不可跨空间/用户转移；自 2026年3月25日起，华北2（北京）地域新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **私网访问地域限制**：PrivateLink 私网接入仅支持华北2（北京）、中国香港地域；其他地域（如新加坡、弗吉尼亚）暂不支持，详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **加密功能语言限制**：DashScope SDK 的自动加密仅支持 Python 和 Java；其他语言必须使用 HTTP 手动模式实现 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 及加解密逻辑。
- **安全存储业务空间特殊性**：文档 6–10 描述的“安全存储”方案是独立于标准百炼的增强安全架构，需单独申请开通，且所有资源配置（OSS/ADB/ES）必须位于同一 VPC 及指定可用区（如北京G/H/L），不适用于普通业务空间。
- **数据隐私承诺**：阿里云百炼不会将您的输入数据用于模型训练；所有传输数据默认经 AES-256 加密，符合 SOC 2 审计要求 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)


