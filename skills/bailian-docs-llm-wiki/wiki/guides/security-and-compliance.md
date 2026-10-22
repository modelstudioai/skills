# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全护栏、模型备案、权限精细化管控及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段（含 `messages` 等核心请求体）进行 AES-RSA 混合加密，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了 SDK 自动加密与 HTTP 手动加解密两种模式。
- **私网访问**：支持通过阿里云 PrivateLink 实现 VPC 内流量全程走内网，避免公网暴露。适用于华北2（北京）、中国香港地域的模型与应用 API 调用，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供完整配置流程。
- **AI 安全护栏**：支持在请求头中启用输入/输出双路内容检测（`X-DashScope-DataInspection`），自动拦截涉黄、涉政、广告等高风险内容。该能力与模型强绑定，调用时无需指定模型是否支持，系统根据模型类型自动匹配对应护栏策略，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高敏感场景提供独立部署的“安全存储业务空间”，支持通过反向终端节点 + MSE 云原生网关 + 私有云资源（OSS/ADB/ES）构建全链路私有化数据平面，相关配置见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 类型 | 作用 | 是否必需 | 来源文档 |
|--------|------|------|----------|----------|
| `enable_encryption` (Python) / `enableEncrypt` (Java) | boolean | 启用 DashScope SDK 自动加解密流程 | 否（默认 `false`） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | string (JSON) | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | 否（启用护栏时必需） | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | string | HTTP 手动加密模式下，携带 RSA 加密后的 AES 密钥 | 是（手动加密时） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `Authorization: Bearer <API_KEY>` | string | 全局身份认证凭证，绑定至单个业务空间与用户 | 是 | [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)（被多篇文档引用） |

> **注意**：文档 1 中明确指出“API Key 的可调用的功能和模型限流与**归属业务空间**的权限保持一致，不受用户（账号）控制台权限管理的影响”，但文档 5 的私网访问示例代码中未体现业务空间 ID 与私网域名的绑定逻辑，实际使用时必须确保 API Key 所属业务空间已关联目标私网连接，否则私网调用将失败。

## 使用方式

1. **加密调用（推荐）**  
   使用 DashScope SDK（Java/Python）并设置 `enable_encryption=True`，SDK 自动完成公钥获取、AES 密钥生成、`input` 加密、密钥封装与响应解密。无需手动调用 `/api/v1/public-keys/latest` 接口，详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

2. **私网调用**  
   - 在百炼控制台 **管理 > 网络配置** 添加私网连接（需授权 `AliyunServiceRoleForBackrouterAccessNet` 角色）；  
   - 在 **业务空间管理** 中将目标业务空间与私网连接关联；  
   - 替换 API 请求的 `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），其他参数（如 `model`, `messages`）保持不变。

3. **启用安全护栏**  
   在任意 SDK 或 HTTP 请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`。若输入/输出触发风控，将返回 `400` 错误及 `data_inspection_failed` 错误码，不产生 token 计费。

4. **配置安全存储空间**  
   仅限已开通“安全存储空间”资质的客户：依次完成 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) → [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) → [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) → [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)，最后激活空间。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储空间当前仅支持华北2（北京）地域及特定可用区（G/H/L）。
- **模型限制**：AI 安全护栏目前仅支持文本与图片类模型，不支持语音合成等非文本模态（见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)）；加密功能仅支持 Java/Python SDK，其他语言需自行实现 HTTP 手动加密。
- **权限继承规则**：API Key 权限完全继承自其归属的**业务空间**，与创建者账号的控制台页面权限无关；但 OpenAPI 接口（如知识库、Prompt 工程）需主账号在 RAM 控制台额外授权 `AliyunBailianDataFullAccess` 等策略（见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **数据留存**：百炼会存储模型与应用调用产生的日志数据用于审计与监控，但**绝不会将客户数据用于模型训练**，所有传输数据默认经 AES-256 加密（见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)）。
- **备案责任主体**：应用/小程序上架所需的算法备案号由阿里云提供（如千问对应 `网信算备330110507206401230035号`），但开发者作为服务提供者，仍须独立承担内容审核、用户权益保障等全部法定义务（见 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)）。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


