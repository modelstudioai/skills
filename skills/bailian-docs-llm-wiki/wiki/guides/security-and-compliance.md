# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `enable_encryption` 参数的模型（如 `qwen-plus`、`qwen-flash` 等），详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：提供两种私网接入路径：
  - **PrivateLink 终端节点**：适用于标准业务空间，通过接口终端节点直连百炼 API，流量全程走阿里云内网（华北2、新加坡地域支持；美国弗吉尼亚地域暂不支持）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储业务空间**：专为高合规场景设计，需配合反向终端节点、MSE 云原生网关及私有云资源（ElasticSearch/ADB/OSS）构建全链路私网闭环，仅限商务开通的专属空间 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持对输入输出内容进行实时合规检测（涉黄、涉政、广告等），需显式设置请求头 `X-DashScope-DataInspection` 启用，当前覆盖文本与图片类模型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示，开发者可直接用于应用上架合规申报 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

> **注意**：文档 6（`secure-storage.md`）将“私网访问配置”列为独立主文档，但其实际内容仅为子文档索引列表，无实质说明；而文档 7–14 已构成完整、可操作的安全存储空间私网部署流程。因此，**应以文档 7–14 为准**，文档 6 仅作导航参考，不作为技术依据。

## 关键参数

| 参数 | 说明 | 示例值 | 文档依据 |
|------|------|--------|----------|
| `enable_encryption` (SDK) / `X-DashScope-EncryptionKey` (HTTP) | 启用混合加密（AES+RSA），自动处理密钥获取、加解密逻辑 | `True` (Python), `true` (Java) | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏，JSON 字符串格式，指定 input/output 检测策略 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `Authorization: Bearer <API_KEY>` | 所有 API 调用必需的身份凭证，绑定至单一业务空间与用户 | `Bearer d1**2a` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `X-DashScope-DataInspection` 请求头 | 必须为 JSON **字符串**（非嵌套对象），双引号需转义 | `"{"input":"cip","output":"cip"}"` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |

## 使用方式

1. **启用传输加密**  
   - SDK 方式（推荐）：初始化调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥并完成加解密 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。  
   - HTTP 方式：先调用 `GET /api/v1/public-keys/latest` 获取 `public_key_id` 和 `public_key`，再手动实现 AES 加密 `input`、RSA 加密 AES 密钥，并通过 `X-DashScope-EncryptionKey` 传入密钥密文。

2. **配置私网访问**  
   - 标准业务空间：在 VPC 中创建接口终端节点（服务名 `com.aliyuncs.dashscope`），替换 API `base_url` 为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/api/v1`）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
   - 安全存储空间：按顺序执行四步配置——创建反向终端节点 → 配置 MSE 网关与可用区 VIP → 配置私有云资源（OSS/ADB/ES）→ 激活空间，全程需严格遵循地域（仅华北2）、可用区（G/H/L）、VPC 一致性要求 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

3. **启用 AI 安全护栏**  
   - 前置：主账号需在 [安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1) 页面完成服务授权。  
   - 调用：在请求头中添加 `X-DashScope-DataInspection: "{\"input\":\"cip\",\"output\":\"cip\"}"`，触发输入/输出双端内容检测 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 限制和注意事项

- **权限粒度**：业务空间是权限管理最小单元，**默认业务空间无法设置模型调用/训练/部署限制**，仅自建业务空间支持精细化管控 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
- **API Key 绑定**：单个 API Key 严格绑定一个地域、一个业务空间、一个用户，不可迁移；自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
- **地域限制**：  
  - PrivateLink 私网访问：仅支持华北2（北京）、新加坡；美国（弗吉尼亚）不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。  
  - 安全存储业务空间：仅支持华北2（北京），且专有网络必须包含可用区 G/H/L 中至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。  
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据默认经 AES-256 加密；但调用日志等元数据将按《服务协议》要求存储用于审计与计费 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。  
- **备案责任主体**：使用百炼调用已备案模型（如千问、万相）仅解决“算法技术支持”环节；若您的应用面向公众且具舆论属性，**您仍需作为服务提供者独立完成安全评估与算法备案**，阿里云不替代履行该法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)


