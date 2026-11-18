# security and compliance

阿里云百炼平台提供覆盖传输、存储、访问控制、内容安全与合规备案的全栈安全能力，支持开发者构建符合国内监管要求与企业内控标准的AI应用。所有安全机制均以最小权限原则设计，关键操作（如API Key管理、业务空间配置）默认受多层权限隔离与审计约束。开发者需主动配置并验证各项安全策略，平台不替代用户履行数据主权与合规主体责任。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段内容进行 AES-RSA 混合加密，防止公网传输中敏感数据被窃听或篡改；该能力已集成至 DashScope SDK（Java/Python），启用 `enable_encryption=True` 即可开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 建立 VPC 到百炼服务端的全程内网连接，调用流量不经过公网；适用于高安全等级场景，需在控制台完成终端节点创建、业务空间关联与私网域名配置 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：仅限华北2（北京）地域可用，提供输入/输出双路内容检测（涉黄、涉政、广告等），需显式设置请求头 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` 或在业务空间维度全局开启 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：所有接入百炼的主流大模型（如千问、万相、DeepSeek、Moonshot 等）均已取得《互联网信息服务算法备案》及《生成式人工智能服务备案》，备案号与主体信息在控制台及文档中公示，供上架合规使用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 参数 | 说明 | 取值范围/格式 | 文档依据 |
|------|------|----------------|-----------|
| `X-DashScope-EncryptionKey` | HTTP 请求头，封装 RSA 加密后的 AES 密钥 | Base64 编码字符串 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | HTTP 请求头，启用 AI 安全护栏 | JSON 字符串，如 `{"input":"cip","output":"cip"}` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `expire_in_seconds` | 临时 API Key 有效期（秒） | 1–1800（默认 60） | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |
| IP 白名单 | API Key 级别网络访问控制 | 最多 20 个 IPv4 地址或 CIDR 段 | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |

> **注意**：`X-DashScope-DataInspection` 的值必须为 JSON **字符串**（即双引号需转义），而非嵌套 JSON 对象；错误写法如 `{"input":"cip"}`（未包裹在引号内）将导致请求失败。

## 使用方式

1. **凭证管理**  
   - 创建 API Key 时选择 **自定义权限**，配置 IP 白名单与模型范围（最多 30 个）；  
   - 生产环境禁止硬编码 Key，应通过环境变量（如 `DASHSCOPE_API_KEY`）或密钥管理服务注入；  
   - 客户端直连场景（Web/App）必须使用后端签发的临时 API Key（`st-` 前缀），有效期按需设为最短必要时长。

2. **传输加密启用**  
   - DashScope SDK：Java 设置 `.enableEncrypt(true)`，Python 设置 `enable_encryption=True`；  
   - HTTP 手动调用：先调用 `/api/v1/public-keys/latest` 获取 RSA 公钥，再用其加密 AES 密钥，最后将加密后 input 与密钥头一并发送 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

3. **私网连接配置**  
   - 在百炼控制台「设置 > 网络配置」开通 PrivateLink 并添加终端节点；  
   - 在「业务空间管理」中将目标空间关联该终端节点；  
   - 替换 API 调用 `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

4. **安全护栏接入**  
   - 仅北京地域支持，需先在[购买页面](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn)开通服务并授权；  
   - 调用时在请求头添加 `X-DashScope-DataInspection`，或在业务空间「高级配置」中开启全局开关。

## 限制和注意事项

- **地域隔离性**：API Key、业务空间、私网连接均严格按地域隔离，跨地域 Key 无法复用，北京地域配置的 AI 安全护栏在其他地域不可用 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **日志时效性**：审计日志默认保留 30 天且不可配置延长；推理日志需**提前开启**并投递至 SLS，开启前的历史调用无法追溯，关闭期间日志不补录 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **凭证生命周期**：2026 年 3 月 25 日及之后创建的 API Key **不会因归属 RAM 用户被删除而级联失效**，必须显式重置或删除 Key 本身 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **安全责任边界**：平台提供风险检测（如公开代码库扫描）、预算告警、模型监控告警等辅助能力，但**不在 SLA 保障范围内**；API Key 泄漏、数据泄露等安全事件的首要责任方为用户，平台仅协助取证 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **隐私承诺**：百炼绝不会将您的输入输出数据用于模型训练；所有传输数据默认经 AES-256 加密，符合 SOC 2 审计要求 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)


