# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、内容安全与合规备案的全链路安全与合规能力，面向开发者提供可配置、可审计、可验证的技术保障。核心能力包括 API Key 全生命周期管理、端到端传输加密、私网隔离访问、AI 安全护栏、模型备案信息公示及 SOC 2 合规认证，所有功能均需结合业务空间权限模型进行精细化控制。

## 支持的模型/功能

- **模型级安全能力**：输入输出 AI 安全护栏（仅华北2北京地域支持）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)，支持对文本和图片类模型的违规内容识别（涉黄、涉政、广告等），需通过 `X-DashScope-DataInspection` 请求头显式启用。
- **传输加密**：支持 AES-RSA 混合加密机制，对请求体中 `input` 字段（含 `messages`）及响应结果全程加密，SDK 提供开箱即用的 `enable_encryption=True` 配置 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **网络隔离**：支持 PrivateLink 私网连接，将 VPC 内流量完全限制在阿里云内网，避免公网暴露 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；另提供“安全存储”专属业务空间类型，支持 OSS/ADB/ES 等资源的私有网络深度集成 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **合规资质与备案**：已通过 SOC 2 Type II 无保留意见审计；所有接入大模型均完成国家网信办算法备案与大模型备案，备案号及主体信息在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中完整公开，适用于应用上架所需的第三方合规材料准备。

> **注意**：AI 安全护栏服务仅在北京地域可用，其他地域控制台不显示“安全管理”入口，且无法通过请求头启用该能力。文档 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 明确指出“AI 安全护栏服务仅华北2（北京）地域可用，其他地域暂不支持接入”。

## 关键参数

- `X-DashScope-DataInspection`: 启用 AI 安全护栏的必需请求头，值为 JSON 字符串（如 `{"input":"cip","output":"cip"}`），非嵌套对象。
- `X-DashScope-EncryptionKey`: HTTP 手动加密模式下用于传递 RSA 加密后的 AES 密钥，SDK 自动处理，无需手动设置。
- `expire_in_seconds`: 生成临时 API Key 时指定有效期（1–1800 秒），默认 60 秒，到期自动失效且不可提前删除。
- `public_key_id` / `public_key`: 通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据，用于客户端手动加密流程 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- `workspace_id`, `vpc_id`, `region_id`: 构成私网域名的关键路径参数，格式为 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`，必须与业务空间、VPC 及地域严格匹配。

## 使用方式

- **API Key 管理**：为不同环境（生产/测试/调试）创建独立 Key，归属至对应业务空间；在 Key 创建/编辑面板中启用“自定义权限”，配置 IP 白名单（最多 20 个）与模型范围（最多 30 个）；高风险场景（如前端直连）必须使用后端签发的临时 Key。
- **传输加密接入**：
  - SDK 方式：Python/Java SDK 设置 `enable_encryption=True`，自动完成公钥获取、AES 密钥生成、加解密全流程；
  - HTTP 方式：先调用 `/api/v1/public-keys/latest` 获取公钥，再用其加密 AES 密钥，最后将加密 input 与密钥头一并发送。
- **私网访问配置**：
  1. 在百炼控制台「网络配置」开通 PrivateLink 并添加 VPC 连接；
  2. 在目标业务空间「高级配置」中关联该私网连接；
  3. 将 API 调用 base_url 中的公网域名替换为生成的私网域名（如 `https://{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com/api/v1`）。
- **AI 安全护栏启用**：仅限北京地域，在请求头中添加 `X-DashScope-DataInspection`，或在业务空间维度统一开关（控制台「业务空间管理」→ 编辑空间 → 「AI 安全护栏」开关）。

## 限制和注意事项

- **临时 API Key 权限继承**：临时 Key 继承签发它的长期 Key 的全部权限，**收窄权限必须先收窄长期 Key**，不能依赖临时 Key 自身权限控制 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **私网连接地域限制**：PrivateLink 仅支持华北2（北京）、华东2（上海）、华东1（杭州）、华南1（深圳）、华北6（乌兰察布）、华北3（张家口）六地；而“安全存储”业务空间当前仅支持华北2（北京）地域，且需商务开通 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **预算告警延迟**：“达到预算后立即停止”存在生效延迟，延迟期间费用仍会计取；预置吞吐（PTU）溢出部分与应用产生的调用暂不支持自动停止，**生产关键业务不建议开启自动停止**，应优先配置预警加人工处置 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **推理日志不可追溯**：推理日志需事先在「数据投递」中开启并授权 SLS，**只对未来调用生效，历史调用无法补录**；审计日志虽默认开启但不包含输入输出内容，敏感内容排查必须提前规划日志策略 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **API Key 删除不终止异步任务**：删除 Key 后，已提交但未执行完的异步任务仍会继续运行并产生费用，需另行调用终止接口 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。

## 来源文档

- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


