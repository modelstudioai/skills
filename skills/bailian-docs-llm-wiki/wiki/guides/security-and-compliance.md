# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、模型备案及数据隐私等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了 SDK 自动加密与 HTTP 手动加密两种接入路径。
- **私网访问**：提供双重私网方案：  
  - **PrivateLink 终端节点**：适用于标准业务空间，通过接口终端节点直连百炼 API，流量全程走阿里云内网，支持北京、新加坡地域；[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 是其核心实现文档。  
  - **安全存储业务空间**：专为高合规要求场景设计，需配合反向终端节点、MSE 云原生网关及 VPC 内部资源（ElasticSearch、ADB、OSS）构建全链路私有网络，仅限开通该空间类型的客户使用。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection`，启用输入/输出双路内容安全检测（如涉政、涉黄、广告等），适用于所有已接入护栏服务的文本与图像模型，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：平台公示所接入模型的算法备案号与大模型备案号，覆盖千问、万相、DeepSeek、Moonshot 等主流模型，供开发者上架应用时直接引用，[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 提供完整清单与查询指引。

> **注意**：文档 7–10 描述的“安全存储业务空间”配置流程（含反向终端节点、MSE 网关、可用区 VIP 等）与文档 5 中标准 PrivateLink 方案存在本质差异：前者是独立部署的增强型私有网络架构，后者是通用型 VPC 内网直连方案。二者适用场景、开通条件与控制台入口均不同，不可混用。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `enable_encryption` / `enableEncrypt` | boolean | SDK 启用传输加密的开关，设为 `true` 后自动完成公钥获取、AES 密钥生成、加解密全流程 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | string (base64) | HTTP 调用时携带的加密后 AES 密钥，由 RSA 公钥加密生成 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | string (JSON) | 启用 AI 安全护栏的请求头，值为 `{"input":"cip","output":"cip"}` 形式的 JSON 字符串 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `public_key_id` & `public_key` | string | 通过 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据，用于手动加密场景 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **传输加密（推荐 SDK）**：安装 DashScope SDK（Java ≥2.12.0 / Python ≥1.14.0），调用 `Generation.call()` 时传入 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java），SDK 自动处理全部加解密逻辑。无需手动调用公钥接口。
- **传输加密（HTTP 手动）**：先调用 `GET /api/v1/public-keys/latest` 获取最新 `public_key`，本地生成 AES 密钥并加密 `input`，将加密后 `input` 和 `X-DashScope-EncryptionKey`（RSA 加密后的 AES 密钥）放入请求头发送。
- **PrivateLink 私网访问**：在 VPC 控制台创建接口终端节点，服务选择 `com.aliyuncs.dashscope`，启用自定义服务域名后，将 API 请求的 `base_url` 替换为终端节点域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/api/v1`）。
- **AI 安全护栏**：在任意 SDK 或 OpenAI 兼容模式调用中，于请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` 即可启用双路检测。
- **模型备案材料准备**：直接引用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中的备案编号，或按 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 指引，在 `beian.cac.gov.cn` 系统中截图验证。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持北京、新加坡地域；美国（弗吉尼亚）地域暂不支持；安全存储业务空间当前仅支持华北2（北京）。
- **模型与功能绑定**：AI 安全护栏服务按模型自动匹配，非所有模型默认启用；具体支持列表及计费请查阅官方文档。传输加密仅适用于 `Generation` 类接口，不支持知识库检索、[Prompt 工程](../concepts/prompt-engineering.md)等其他 API。
- **API Key 权限继承**：API Key 的模型调用权限、限流策略完全继承自其归属的**业务空间**，与创建该 Key 的用户角色无关；普通用户即使拥有 API Key，也无法绕过业务空间管理员设置的模型禁用或限流规则。
- **安全存储业务空间依赖强**：OSS Bucket 若被释放、ADB/ES 若停止计费或被释放，将导致整个安全存储业务空间**不可用且无法恢复**，必须重建新空间。
- **合规责任主体**：阿里云百炼作为“服务技术支持者”提供模型备案信息与基础设施合规资质（如 SOC 2），但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户权益保护、算法备案（如适用）等全部法定义务。[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md) 明确强调此责任边界。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


