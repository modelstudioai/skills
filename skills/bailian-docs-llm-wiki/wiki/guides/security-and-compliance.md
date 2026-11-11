# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全防护、权限精细化管控、模型备案公示及数据隐私保障等关键维度。所有能力均面向企业级开发者设计，支持在生产环境中按需组合使用，满足金融、政务、医疗等强监管行业的合规要求。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段内容进行 AES-RSA 混合加密，适用于敏感数据通过公网传输场景；该能力对所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`）通用，无需模型侧特殊适配 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **AI 安全护栏**：仅在华北2（北京）地域可用，支持对输入/输出内容进行涉黄、涉政、广告等高风险内容识别；当前覆盖文本类与图片类模型，具体映射关系请参考官方服务文档 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **私网访问**：提供两种私网方案：
  - **PrivateLink 方式**：适用于标准业务空间，通过 VPC 终端节点直连百炼网关，流量全程内网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储空间方式**：专为高安全要求客户设计，需额外配置 MSE 网关、OSS/ADB/ES 等后端资源，仅限“安全存储空间”类型业务空间启用 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **模型备案信息**：所有接入百炼的第三方大模型（如 DeepSeek、Moonshot、MiniMax）及通义系列模型（千问、万相、可灵等）均已依法完成算法备案与大模型备案，并在平台公示 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（文档 7–11）实际描述的是**安全存储空间**这一独立产品形态，与文档 5 中的通用 PrivateLink 私网访问属不同技术路径和适用场景。开发者应根据业务安全等级选择：普通私网隔离用文档 5；金融级数据不出域、存储计算全私有化部署需求则必须使用安全存储空间（文档 7–11）。

## 关键参数

| 参数名 | 说明 | 示例值 | 来源 |
|--------|------|--------|------|
| `X-DashScope-EncryptionKey` | HTTP 请求头，用于传递经 RSA 加密的 AES 密钥 | `"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB\n-----END PUBLIC KEY-----"` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `'{"input":"cip","output":"cip"}'` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `public_key_id` / `public_key` | 从 `/api/v1/public-keys/latest` 接口返回，用于 SDK 或手动加密流程 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **传输加密（SDK 自动模式）**：  
  Python：设置 `enable_encryption=True`；Java：设置 `.enableEncrypt(true)`。SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加解密 input/output，开发者无需处理密钥管理 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

- **传输加密（HTTP 手动模式）**：  
  1. 调用 `GET /api/v1/public-keys/latest` 获取 `public_key` 和 `public_key_id`；  
  2. 生成随机 AES-256 密钥，用 RSA 公钥加密该密钥；  
  3. 用 AES 密钥加密 `input` 字段原始 JSON；  
  4. 将加密后的 AES 密钥放入 `X-DashScope-EncryptionKey` 请求头，加密后的 `input` 放入请求体。

- **AI 安全护栏**：  
  在请求头中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'` 即可启用输入/输出双检。也可在业务空间维度统一开关（控制台 > 业务空间管理 > 高级配置），避免代码侵入 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

- **PrivateLink 私网访问**：  
  1. 控制台 > 设置 > 网络配置 > 添加私网连接（需授权角色、开通 PrivateLink）；  
  2. 业务空间 > 高级配置 > 关联私网连接；  
  3. 替换 API `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

- **安全存储空间私网访问**：  
  必须按顺序完成：创建安全存储空间 → 配置反向终端节点 → 配置 MSE 网关与可用区 VIP → 配置 OSS/ADB/ES 白名单与授权 → 激活空间。全过程依赖华北2（北京）地域，且不兼容通用 PrivateLink [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 限制和注意事项

- **地域限制**：  
  - AI 安全护栏仅华北2（北京）可用；  
  - 安全存储空间全套方案（文档 7–11）仅支持华北2（北京）；  
  - PrivateLink 私网访问支持北京、上海、杭州、深圳、乌兰察布、张家口六地（见文档 5）。

- **API Key 生命周期**：  
  自 2026年3月25日起，华北2（北京）新创建的 API Key 均归属主账号；此前由 RAM 用户创建的 API Key 与该用户绑定，删除 RAM 用户将级联删除其 API Key 且不可恢复 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

- **权限继承规则**：  
  API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与创建者账号的控制台页面权限无关；即 RAM 用户即使无“模型体验”页面权限，只要其 API Key 所属空间已授权某模型，仍可通过该 Key 调用 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

- **数据隐私承诺**：  
  阿里云百炼明确声明：**绝不会将您的输入数据用于模型训练**；所有传输数据默认经 AES-256 加密；日志与调用数据按《阿里云百炼服务协议》约定存储与处理 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

- **备案责任主体**：  
  应用/小程序上架时，开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部法定义务；百炼仅提供所用模型的备案号与合作协议模板，不替代开发者履行主体责任 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


