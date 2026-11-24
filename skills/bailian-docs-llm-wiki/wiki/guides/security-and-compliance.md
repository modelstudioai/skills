# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、权限控制、合规备案等维度的安全与合规能力，支持企业级精细化治理。核心能力包括基于业务空间的多层级权限管理、API Key 全生命周期防护、端到端传输加密（AES+RSA）、私网访问（PrivateLink）、AI 安全护栏内容检测，以及面向中国监管要求的算法与大模型备案信息支持。所有能力均以开发者可集成、可配置、可审计为设计原则。

## 支持的模型/功能

- **模型级安全能力**：输入/输出内容安全检测（AI 安全护栏）仅在华北2（北京）地域可用，支持文本与图片类模型，需显式设置 `X-DashScope-DataInspection` 请求头或通过业务空间开关启用 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **传输加密**：支持对请求体 `input` 字段进行 AES 对称加密，密钥通过百炼托管的 RSA 公钥加密传输；DashScope SDK（Java/Python）提供开箱即用的自动加密能力，其他语言需手动实现 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **网络隔离**：支持两种私网访问方案：
  - **通用私网连接（PrivateLink）**：适用于标准模型/API 调用，通过终端节点将 VPC 流量直连百炼网关，全程内网不走公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **安全存储业务空间专用私网**：面向高敏感场景（如金融、政务），需开通专属安全存储空间，并配置 MSE 网关、OSS/ADB/ES 等私有资源，形成端到端闭环隔离环境 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)。
- **合规资质与备案**：已通过 SOC 2 无保留意见审计；提供千问、万相等主流模型的《互联网信息服务算法备案》及《生成式人工智能服务备案》编号，覆盖生成合成类、深度合成等算法类型，开发者可直接用于应用上架合规申报 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

> **注意**：文档 15 明确指出 AI 安全护栏“仅华北2（北京）地域可用”，但文档 1 中超级管理员全局管理菜单列表包含新加坡、弗吉尼亚、法兰克福、中国香港等多地链接，且未说明该功能在非北京地域是否受限。实际开发中应以控制台实际可用性为准，北京地域外调用 `X-DashScope-DataInspection` 头将返回 400 错误或被忽略。

## 关键参数

- `X-DashScope-DataInspection`：启用 AI 安全护栏的必需请求头，值为 JSON 字符串（如 `{"input":"cip","output":"cip"}`），不可嵌套为对象。
- `X-DashScope-EncryptionKey`：HTTP 手动加密模式下，用于传递经 RSA 加密的 AES 密钥（Base64 编码）。
- `enable_encryption=True`（Python） / `enableEncrypt(true)`（Java）：DashScope SDK 启用传输加密的布尔开关。
- `expire_in_seconds`：生成临时 API Key 时指定有效期（1–1800 秒），默认 60 秒，到期自动失效。
- `public_key_id` 与 `public_key`：通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据，用于客户端手动加密流程 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

## 使用方式

1. **权限初始化**：由超级管理员（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在全局管理菜单（如 [北京](https://bailian.console.aliyun.com/settings/workspace)）创建业务空间，并为业务空间授权模型调用、训练、部署权限；业务空间管理员可在本空间内管理用户与页面权限。
2. **API Key 配置**：
   - 生产环境必须使用独立业务空间 + 独立 Key，禁用默认业务空间；
   - 创建时选择“自定义”权限，严格限制 IP 白名单（最多 50 个）与可调用模型（最多 30 个）；
   - 客户端场景必须使用后端签发的临时 Key（`st-` 前缀），禁止前端直连长期 Key [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
3. **传输加密接入**：
   - SDK 方式：安装 DashScope ≥2.0.1（Python）或 ≥2.12.0（Java），设置 `enable_encryption=True` 即可，SDK 自动完成公钥获取、AES 密钥生成、加解密全流程；
   - HTTP 方式：先调用 `/api/v1/public-keys/latest` 获取公钥，再用该公钥加密 AES 密钥，最后将加密后的 input 和密钥头一并发送。
4. **私网访问**：
   - 标准 PrivateLink：在百炼控制台「网络配置」添加私网连接 → 关联业务空间 → 替换 API `base_url` 为生成的私网域名（格式 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）；
   - 安全存储空间：需完整执行「配置终端节点 → 配置可用区IP → 配置OSS/ADB/ES → 配置MSE网关 → 激活」链路，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅北京地域可用；PrivateLink 私网连接支持北京、上海、杭州、深圳、乌兰察布、张家口，但不支持新加坡、弗吉尼亚等国际地域；安全存储业务空间当前仅支持华北2（北京）。
- **API Key 生命周期**：2026 年 3 月 25 日后创建的 Key 不会因归属 RAM 用户被删除而级联失效，必须单独重置或删除；删除 Key 不取消已提交的异步任务，需另行终止 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **加密约束**：DashScope SDK 加密仅支持 Java/Python；手动 HTTP 加密不支持自定义密钥；加密仅保护 `input` 字段，`model`、`parameters` 等元数据仍为明文。
- **合规责任边界**：阿里云提供模型备案号与合作协议模板，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、数据安全等全部法定义务；内部使用场景（如企业知识库）虽不强制上架备案，但仍需履行数据保密与访问控制义务。
- **日志追溯**：推理日志（含 Prompt/Response）需提前在「数据投递」中开启并授权 SLS，开启前的历史调用无法追溯；审计日志默认开启，但不含输入输出内容。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


