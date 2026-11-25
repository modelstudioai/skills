# security and compliance

阿里云百炼平台提供覆盖身份权限、传输加密、内容安全、模型合规与数据隐私的全栈安全能力，满足企业级AI应用在等保、GDPR及《生成式人工智能服务管理暂行办法》等监管框架下的核心要求。所有安全机制均以最小权限原则设计，支持按业务空间粒度隔离与精细化管控，开发者可通过控制台、OpenAPI 或 SDK 快速集成。

## 支持的模型/功能

- **模型级安全能力**：输入/输出 AI 安全护栏（仅华北2北京地域可用）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)，支持文本与图片模型的实时违规内容检测（涉政、涉黄、广告等）。
- **加密传输**：支持对 `input` 字段进行 AES-RSA 混合加密，防止公网传输中敏感数据被窃听或篡改 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：通过 PrivateLink 建立 VPC 到百炼的内网通道，调用流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **模型备案**：所有接入百炼的模型（含千问、万相、智谱、DeepSeek 等）均完成国家网信办算法备案与大模型备案，备案信息实时公示 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 9 和文档 10 描述的“安全存储业务空间”配置流程（含反向终端节点、MSE网关等）与文档 8 中标准 PrivateLink 流程存在架构差异——前者面向高隔离要求的专有云/私有云客户，后者为通用公有云 VPC 接入方案；二者不互斥但适用场景不同，开发者应根据部署环境选择对应路径。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串，如 `{"input":"cip","output":"cip"}` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | 加密请求体时封装的 RSA 加密后的 AES 密钥（由 SDK 自动注入，无需手动构造） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `enable_encryption=True`（Python） / `.enableEncrypt(true)`（Java） | DashScope SDK 中启用端到端加密的开关参数 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `expire_in_seconds` | 生成临时 API Key 时指定的有效期（1–1800 秒），默认 60 秒 | [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md) |

## 使用方式

- **权限控制**：通过业务空间（Workspace）实现最小化隔离。超级管理员可在全局管理菜单中为各业务空间授权模型调用、调优与部署权限，并设置请求数/Token 限流；业务空间管理员仅能管理本空间内用户与页面权限 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **API Key 安全实践**：
  - 生产环境必须使用**一业务一 Key**，并绑定 IP 白名单（最多 50 个）与模型范围（最多 30 个）；
  - 客户端场景强制使用后端签发的**临时 API Key**（`st-`前缀），有效期按需设为最短必要时长；
  - 敏感环境（如 VPC）优先配置 PrivateLink 私网域名，替换默认公网 base_url。
- **加密调用**：Python/Java SDK 中启用 `enable_encryption=True` 即可自动完成 AES 密钥生成、RSA 公钥获取、`input` 加密与响应解密，无需手动调用 `/api/v1/public-keys/latest` 接口 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **合规材料获取**：算法备案号与主体信息直接引用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)；合作协议需通过自助申请助手提交 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅在北京地域可用；PrivateLink 支持地域以控制台下拉列表为准（含北京、上海、杭州、深圳等），但“安全存储业务空间”专属流程仅支持华北2（北京）[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **Key 生命周期**：2026年3月25日后创建的 API Key **不会因归属 RAM 用户被删除而级联失效**，必须显式重置或删除 Key 本身 [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)。
- **日志追溯**：推理日志（含完整 Prompt/Response）需**提前开启并投递至 SLS**，开启前的历史调用无法追溯；审计日志默认开启但不含输入输出内容 [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)。
- **数据隐私承诺**：百炼**绝不会将您的调用数据用于模型训练**，所有传输数据默认经 AES-256 加密；但调用日志与用量数据会按《服务协议》要求存储，用于计费与安全审计 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


