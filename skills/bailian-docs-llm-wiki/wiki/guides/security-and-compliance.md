# security and compliance

阿里云百炼平台提供覆盖身份权限、传输加密、数据隐私、内容安全及合规备案的全栈安全与合规能力，面向企业级开发者设计。所有功能均基于最小权限原则和零信任模型构建，关键控制点（如 API Key 权限、业务空间隔离、私网访问）需显式配置，无默认开启的安全策略。开发者需主动启用并验证各项防护措施的有效性。

## 支持的模型/功能

- **[AI 安全护栏](../concepts/security-guardrails.md)**：仅在华北2（北京）地域可用，支持文本与图片类模型的输入/输出内容检测（涉黄、涉政、广告等），需手动开通并配置请求头 `X-DashScope-DataInspection` [原文标题](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **加密传输**：支持 AES-RSA 混合加密，对 `input` 字段进行端到端加密，SDK（Java/Python）提供开箱即用的 `enable_encryption` 参数，HTTP 调用需手动获取 RSA 公钥并管理密钥 [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，支持北京、上海、杭州、深圳等 6 个地域；需在控制台配置终端节点、关联业务空间并替换 API 域名为私网域名 [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：专为高敏感场景设计，支持通过 MSE 网关接入客户自有 VPC 内的 ElasticSearch、ADB、OSS 等资源，实现数据不出私有网络 [原文标题](../../raw/model-user-guide/security-and-compliance/secure-storage.md)。

> **注意**：文档 9 和文档 10 均描述“安全存储业务空间”，但文档 9 明确要求地域为“华北2（北京）”且可用区限定为 G/H/L，而文档 10 的前提条件未限定地域，且步骤中多次引用“华北2（北京）”作为示例。实际部署必须严格遵循文档 9 的地域与可用区约束，文档 10 中的非北京地域示例属于过时或错误信息。

## 关键参数

| 参数 | 说明 | 限制/注意事项 |
|------|------|----------------|
| `X-DashScope-DataInspection` | [AI 安全护栏](../concepts/security-guardrails.md)开关，值为 JSON 字符串（如 `{"input":"cip","output":"cip"}`） | 仅北京地域生效；必须在请求头中显式设置，业务空间维度开关为替代方案 |
| `X-DashScope-EncryptionKey` | 加密请求中封装的 AES 密钥（经 RSA 公钥加密后） | SDK 自动处理，HTTP 调用需手动调用 `/api/v1/public-keys/latest` 获取公钥 [原文标题](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | 取值范围 1–1800 秒，不支持提前删除，继承签发 Key 的全部权限 |
| IP 白名单 | API Key 级别网络访问控制 | 最多 20 个 IPv4 地址或网段；填写百炼实际看到的公网出口 IP（非服务器内网地址） |

## 使用方式

- **权限隔离**：使用**业务空间**作为最小管理单元，超级管理员可跨空间管理模型授权与限流，业务空间管理员仅管理本空间内用户、模型调用/训练/部署权限；API Key 权限严格继承其归属业务空间的模型授权状态 [原文标题](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 管理**：
  - 生产环境禁用长期 Key，客户端场景必须使用后端签发的临时 Key（`st-` 前缀）；
  - 为不同环境（生产/测试/调试）分配独立 Key，并配置 IP 白名单与模型范围；
  - 敏感凭证必须通过环境变量或密钥管理服务（KMS）注入，禁止硬编码、截图、日志打印。
- **加密调用**：
  - SDK 方式：Java 设置 `.enableEncrypt(true)`，Python 设置 `enable_encryption=True`；
  - HTTP 方式：先调用 `GET /api/v1/public-keys/latest` 获取公钥，再用该公钥加密 AES 密钥，最后将加密后的 input 和密钥放入请求头。
- **私网调用**：
  1. 控制台「设置 > 网络配置」添加 PrivateLink 终端节点（指定 VPC/可用区/交换机）；
  2. 在「业务空间管理」中编辑目标空间，于「高级配置」绑定该终端节点；
  3. 将 API 请求的 base_url 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

## 限制和注意事项

- **地域限制**：[AI 安全护栏](../concepts/security-guardrails.md)、部分安全存储配置（如反向终端节点）仅支持华北2（北京）；私网连接支持地域以控制台下拉列表为准（当前含北京、上海、杭州、深圳等 6 地域）。
- **Key 生命周期**：2026 年 3 月 25 日后创建的 API Key **不会因删除归属 RAM 用户而级联删除**，必须单独处置 Key；删除 Key 不取消已提交的异步任务，需另行终止 [原文标题](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **合规责任**：阿里云提供千问、万相等模型的算法备案号（如 `网信算备330110507206401230035号`）及大模型备案号，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、标识规范等全部法定义务 [原文标题](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
- **监控告警延迟**：“达到预算后立即停止”存在生效延迟，延迟期间费用仍会计取；预置吞吐（PTU）溢出与应用调用暂不支持自动停止。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


