# security and compliance

阿里云百炼平台提供覆盖传输、存储、访问控制、内容安全及合规备案的全栈安全与合规能力，面向企业级开发者支持私网隔离、端到端加密、精细化权限管理、AI安全护栏及算法/模型备案信息公示。所有能力均基于阿里云统一安全基线设计，并通过 SOC 2 审计认证。

## 支持的模型/功能

- **传输安全**：支持 HTTPS 公网调用、PrivateLink 私网接入（[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)）及 AES-RSA 混合加密（[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)）。
- **内容安全**：AI 安全护栏服务（仅华北2北京地域可用）支持对输入/输出文本、图片进行涉黄、涉政、广告等违规内容识别，需显式配置 `X-DashScope-DataInspection` 请求头或在业务空间维度开启开关（[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)）。
- **模型备案**：所有上架模型均完成国家网信办《生成式人工智能服务管理暂行办法》要求的算法备案与大模型备案，备案号及主体信息在控制台及文档中公开可查（[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)）。
- **安全存储**：针对高敏感场景提供“安全存储业务空间”，通过反向终端节点 + MSE 网关 + VPC 内部资源（OSS/ADB/ES）构建完全隔离的数据平面（[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（如 `configure-an-endpoint-and-initiate-a-connection.md`）实际描述的是**安全存储业务空间**的专有网络架构，与文档 5 中面向通用模型调用的 PrivateLink 私网访问属不同技术路径和适用场景，不可混用。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串，如 `{"input":"cip","output":"cip"}` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption=True` (Python SDK) / `enableEncrypt=true` (Java SDK) | SDK 层启用混合加密的开关，自动获取 RSA 公钥、生成 AES 密钥并加解密 input/output | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | HTTP 调用时携带加密后 AES 密钥的请求头（仅手动加密场景使用） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 通过 `/api/v1/public-keys/latest` 接口获取的当前有效 RSA 公钥 ID 及 PEM 值 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **权限控制**：通过超级管理员（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在全局管理菜单（如 [北京](https://bailian.console.aliyun.com/settings/workspace)）配置业务空间级模型调用/训练/部署授权及限流；业务空间管理员仅能管理本空间内用户与页面权限。
- **加密调用**：
  - SDK 方式：设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动完成公钥获取、AES 加密、密钥封装与响应解密。
  - HTTP 方式：先调用 `/api/v1/public-keys/latest` 获取公钥，再用该公钥加密 AES 密钥，最后将加密后的 input 和密钥头一并发送。
- **私网访问**：
  - 通用模型调用：在百炼控制台「网络配置」→「VPC私网访问」添加 PrivateLink 连接，关联业务空间后，使用 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com` 域名替代公网域名。
  - 安全存储业务空间：需单独开通安全存储空间类型，通过反向终端节点 + MSE 网关 + 配置 OSS/ADB/ES 白名单实现数据面隔离（[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)）。
- **合规备案材料获取**：算法备案号见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；完整备案截图需登录 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index) 查询对应编号；合作协议请联系商务经理获取。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅在华北2（北京）地域可用；PrivateLink 私网访问支持北京、上海、杭州、深圳、乌兰察布、张家口六地；安全存储业务空间目前仅支持华北2（北京）。
- **API Key 绑定规则**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 归属主账号，与 RAM 用户解耦；此前创建的 RAM 用户级 API Key 在删除该 RAM 用户时将被同步删除且不可恢复（[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **加密限制**：DashScope SDK 的自动加密仅支持 Java 和 Python；其他语言需自行实现 HTTP 手动加密流程；不支持自定义 AES 密钥。
- **安全存储依赖强耦合**：OSS Bucket 或 ADB/ES 实例若被释放，将导致已激活的安全存储业务空间**永久不可用且无法恢复**，必须重建（[配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)）。
- **隐私承诺**：阿里云百炼不会将您的输入数据用于模型训练；所有传输数据默认经 AES-256 加密（[合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)


