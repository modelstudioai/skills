# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限控制、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者通过配置、API 或 SDK 快速集成，无需自行构建底层安全基础设施。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-RSA 混合加密，适用于敏感数据场景。该能力已集成至 DashScope SDK（Java/Python），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，避免公网暴露。仅限华北2（北京）、中国香港地域 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出内容合规检测，覆盖涉黄、涉政、广告等风险类型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储业务空间**：面向高敏感场景（如金融、政务）提供独立网络域，支持对接客户自有 OSS、ADB、ElasticSearch，并通过 MSE 网关统一管控流量 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 6（`secure-storage.md`）仅列出子文档索引，未提供实质配置说明；实际操作应严格依据其引用的子文档（如文档 7、8、13、14）执行。文档 5 与文档 7 均描述私网连接，但适用范围不同：文档 5 面向通用模型/API 调用，文档 7 专用于“安全存储业务空间”，二者不可混用。

## 关键参数

| 参数名 | 说明 | 来源 |
|--------|------|------|
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的开关，SDK 自动调用公钥接口并管理 AES 密钥 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非对象），必须转义双引号 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时，用于传递 RSA 加密后的 AES 密钥的请求头 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | 仅支持 `cip`（内容安全检查）值，不支持 `none` 或空字符串；设为非法值将导致 400 错误 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |

## 使用方式

### 1. 传输加密（推荐 SDK 方式）
- 安装最新 DashScope SDK（Python ≥ 1.14.0，Java ≥ 2.12.0）。
- 在 `Generation.call()` 或 `GenerationParam.builder()` 中启用 `enable_encryption=True` / `.enableEncrypt(true)`。
- SDK 自动完成：获取公钥 → 生成 AES 密钥 → 加密 `input` → 设置 `X-DashScope-EncryptionKey` → 解密响应。
- **无需手动调用** `/api/v1/public-keys/latest` 接口 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 2. 私网访问
- **通用模型/API**：在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加私网连接，关联业务空间后，将 API `base_url` 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。
- **安全存储业务空间**：需额外完成反向终端节点创建、可用区 VIP 配置、MSE 网关服务注册及路由发布，流程更复杂，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

### 3. AI 安全护栏
- **前提**：主账号需在 **安全管理** 页面开通并授权服务（RAM 用户无法操作）。
- **调用时**：在请求头中添加 `X-DashScope-DataInspection`，值为 `{"input":"cip","output":"cip"}` 的 JSON 字符串（注意双引号转义）。
- **响应处理**：违规请求返回 `400` + `data_inspection_failed` 错误码，需捕获异常并提示用户。

## 限制和注意事项

- **地域限制**：
  - PrivateLink 私网访问仅支持 **华北2（北京）、中国香港** 地域，其他地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - 安全存储业务空间仅支持 **华北2（北京）**，且专有网络必须包含可用区 G/H/L 中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

- **权限与账号约束**：
  - API Key 仅归属**单个地域内的单个业务空间和单个用户**，不可跨空间/用户转移。
  - 自 2026年3月25日起，**华北2（北京）地域所有新创建的 API Key 均归属主账号**，不再支持 RAM 用户创建 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
  - OpenAPI 接口权限（如知识库、Prompt 工程）**仅主账号可授权**，RAM 用户需主账号在 RAM 控制台添加 `AliyunBailianDataFullAccess` 等策略。

- **数据与合规**：
  - 百炼**绝不会将您的数据用于模型训练**，所有传输数据默认使用 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
  - 应用上架需自行完成算法备案，百炼提供千问、万相等模型的备案号及查询指引，但**开发者作为服务提供者须独立承担全部法律责任** [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
  - 模型备案信息以 [互联网信息服务算法备案系统](https://beian.cac.gov.cn) 实时结果为准，备案号可能更新，建议定期核验。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


