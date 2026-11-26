# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、存储、内容安全及合规资质的全链路安全与合规能力，面向企业级开发者支持精细化权限控制、端到端加密、私网隔离、AI安全护栏及算法备案信息可追溯。所有能力均基于阿里云统一安全基座构建，并通过 SOC 2 审计认证。

## 支持的模型/功能

- **模型级安全能力**：输入/输出 AI 安全护栏（仅华北2北京地域可用）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)，支持对文本、图片类模型的实时内容风险识别（涉黄、涉政、广告等），需在请求头中设置 `X-DashScope-DataInspection` 或通过业务空间开关启用。
- **加密传输支持**：所有模型推理接口均支持 AES-RSA 混合加密，对 `input` 字段进行端到端加密，防止公网传输中敏感数据泄露 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问能力**：支持通过 PrivateLink 建立 VPC 到百炼服务的内网通道，流量全程不经过公网；同时支持“安全存储业务空间”专属架构，将模型应用与客户私有资源（ElasticSearch、ADB、OSS）完全隔离部署 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **合规资质与备案**：平台已通过 SOC 2 无保留意见审计；所接入的千问、万相等主流大模型均完成国家网信办《生成式人工智能服务管理暂行办法》要求的算法备案与大模型备案，备案号及主体信息持续公示 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)、[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 参数 | 作用 | 说明 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏 | 值为 JSON 字符串，如 `{"input":"cip","output":"cip"}`，表示对输入和输出均启用内容检查；必须显式设置请求头或在业务空间开启全局开关 |
| `X-DashScope-EncryptionKey` | 传输加密密钥标识 | SDK 自动注入，HTTP 调用时由客户端封装 RSA 加密后的 AES 密钥，见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |
| `enable_encryption=True`（Python） / `enableEncrypt=true`（Java） | SDK 加密开关 | DashScope SDK 封装全部加解密逻辑，仅需启用该参数即可，无需手动管理密钥或调用公钥接口 |
| `expire_in_seconds`（临时 API Key） | 有效期控制 | 取值范围 1–1800 秒，建议按最小必要原则设置，避免使用默认 60 秒以外的长周期 |

> **注意**：文档 13 中描述的 `X-DashScope-DataInspection` 参数值格式为 JSON 字符串（如 `"{"input":"cip"}"`），而文档 15 的示例代码中误写为嵌套 JSON 对象（如 `{"input":"cip"}`）。实际调用必须传入字符串类型，否则将返回 `400 Bad Request`。请严格遵循 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 中的格式说明。

## 使用方式

- **权限配置**：通过业务空间（Workspace）实现最小粒度隔离。超级管理员可在全局管理菜单中为各业务空间授权模型调用、训练、部署权限，并设置请求数/[Token](../concepts/token.md) 限流；业务空间管理员仅能管理本空间内用户与页面权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 管理**：生产环境必须启用“自定义权限”，并配置 IP 白名单（最多 50 个）与模型范围（最多 30 个，受业务空间已授权模型约束）；高风险场景（如前端直连）应使用后端签发的临时 API Key（`st-` 前缀），有效期严格控制在任务所需最短时长内。
- **加密调用**：
  - 推荐使用 DashScope SDK（Java/Python），设置 `enable_encryption=True` 即可自动完成公钥获取、AES 密钥生成、加解密全流程；
  - 若需手动实现 HTTP 调用，须先调用 `/api/v1/public-keys/latest` 接口获取最新 RSA 公钥，再执行混合加密 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **私网接入**：
  - 普通模型调用：在百炼控制台创建 PrivateLink 终端节点 → 关联目标业务空间 → 替换 API 请求中的 `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）；
  - 安全存储业务空间：需额外配置 MSE 云原生网关、可用区 VIP、NLB 安全组放行及后端资源（ES/ADB/OSS）授权，流程更复杂但网络与数据完全隔离 [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅在北京地域可用；PrivateLink 私网连接支持北京、上海、杭州、深圳、乌兰察布、张家口六地，但“安全存储业务空间”相关功能（如反向终端节点）目前仅限北京地域 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **API Key 生命周期**：2026 年 3 月 25 日起创建的 API Key 不再随归属 RAM 用户删除而级联失效，必须显式重置或删除 Key 本身；轮换时需同步更新权限与预算配置，新 Key 不继承旧 Key 设置 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **日志与取证**：审计日志默认开启、保留 30 天，含 Request ID、模型、[Token](../concepts/token.md) 用量、状态码，但**不包含 Prompt/Response 内容**；推理日志需主动开启并投递至 SLS，且仅对开启后的新调用生效，历史数据不可追溯 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **数据主权承诺**：阿里云明确声明“绝不会将您的数据用于模型训练”，所有传输数据默认经 AES-256 加密；但客户仍需自行承担应用层合规责任，例如上架含大模型的应用时，开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立完成算法备案、安全评估及内容审核义务 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)、[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


