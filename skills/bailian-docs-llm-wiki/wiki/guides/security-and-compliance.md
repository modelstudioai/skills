# security and compliance

阿里云百炼平台提供覆盖身份权限、传输加密、内容安全、数据隐私、合规备案等维度的安全与合规能力，面向企业级开发者设计。所有功能均基于最小权限原则和零信任架构，关键控制点（如 API Key 权限、业务空间隔离、私网访问）需显式配置，不默认启用。开发者需主动管理凭证生命周期、收窄调用范围，并根据业务场景选择对应安全机制。

## 支持的模型/功能

- **AI 安全护栏**：仅在华北2（北京）地域可用，支持文本与图片类模型的输入/输出内容检测，需手动启用请求头 `X-DashScope-DataInspection` 或通过业务空间开关全局开启 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **传输加密**：支持两种方式：
  - **端到端 AES-RSA 混合加密**：对 `input` 字段加密，适用于敏感数据公网传输，SDK（Java/Python）开箱即用，HTTP 调用需手动管理密钥 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
  - **PrivateLink 私网连接**：VPC 内流量全程走阿里云内网，不经过公网，需在控制台配置终端节点并关联业务空间 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **安全存储业务空间**：专为高合规要求客户设计，支持通过反向终端节点 + MSE 网关 + 私有云资源（OSS/ADB/ES）构建完全隔离的数据平面，仅限开通该空间类型的客户使用 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **算法与大模型备案信息**：公示所接入模型的《互联网信息服务算法备案》及《生成式人工智能服务备案》编号，供开发者上架应用时直接引用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 8 和文档 15 均提及“安全存储业务空间”，但文档 8 明确要求“已申请开通”，而文档 15 未说明开通路径；实际使用前必须联系商务确认资质与开通状态，否则后续步骤无法执行。

## 关键参数

| 参数 | 说明 | 取值/约束 | 来源 |
|------|------|-----------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `{"input":"cip","output":"cip"}`，不可为嵌套对象 | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption` / `enableEncrypt` | SDK 加密开关 | Python 设为 `True`，Java 设为 `true` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `expire_in_seconds` | 临时 API Key 有效期 | 1–1800 秒，按需设最短值 | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时的 AES 密钥封装头 | Base64 编码的 RSA 加密后 AES 密钥 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |

## 使用方式

1. **权限初始化**：  
   - 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在[全局管理菜单](https://bailian.console.aliyun.com/settings/workspace)创建业务空间，并授权模型调用、训练、部署权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。  
   - 为不同环境（生产/测试/调试）分配独立业务空间和 API Key，实现权限与成本隔离。

2. **凭证安全配置**：  
   - 生产环境禁用长期 Key，客户端场景必须使用后端签发的临时 Key（`st-` 前缀），有效期 ≤ 1800 秒。  
   - 所有 Key 必须配置 IP 白名单（最多 20 个）和模型范围（最多 30 个），并通过预算告警+达预算即停双控风险 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。

3. **传输层加固**：  
   - 敏感数据公网传输：启用 SDK `enable_encryption=True`，或调用 `/api/v1/public-keys/latest` 获取 RSA 公钥后手动加密 `input` [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。  
   - 高安全要求内网调用：在百炼控制台「网络配置」添加 PrivateLink 终端节点，关联目标业务空间，将 API `base_url` 替换为生成的私网域名 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

4. **内容与合规落地**：  
   - 开通 AI 安全护栏服务（仅北京地域），并在请求头中设置 `X-DashScope-DataInspection` [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。  
   - 应用上架前，从[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)页面复制对应模型的算法备案号与大模型备案号，提交至监管平台。

## 限制和注意事项

- **地域限制**：AI 安全护栏、安全存储业务空间、部分私网连接功能仅支持华北2（北京）地域，其他地域暂不可用 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **API Key 生命周期**：2026 年 3 月 25 日起创建的 Key **不会因归属 RAM 用户被删除而级联失效**，必须单独重置或删除 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **日志追溯能力**：推理日志（含完整 Prompt/Response）需**提前开启**并投递至 SLS，开启前的历史调用无法追溯；审计日志默认开启但不含输入输出内容 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **私网连接依赖项**：PrivateLink 配置需先授权服务关联角色 `AliyunServiceRoleForBackrouterAccessNet` 并开通 PrivateLink 服务，且仅支持特定地域（北京、上海、杭州等）的 VPC [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **合规责任主体**：阿里云提供模型备案信息与基础设施合规资质（如 SOC 2），但应用开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、标识规范等全部法定义务 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)


