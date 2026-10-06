# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足监管要求的前提下安全、可控地调用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES 加密，并通过 RSA 公钥安全传递 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了混合加密流程与 SDK 集成方式。
- **私网访问**：支持通过 PrivateLink 建立 VPC 到百炼服务的内网通道，流量全程不经过公网；同时支持为“安全存储业务空间”配置专属私有网络资源（OSS/ADB/ES）及 MSE 云原生网关，实现全链路网络隔离。相关能力仅限华北2（北京）、中国香港地域，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 分别描述了两种私网模式的适用场景与配置路径。
- **AI 安全护栏**：默认启用模型内置合规检查，同时可选配阿里云 AI 安全护栏服务，对输入输出内容进行涉黄、涉政、广告等高风险内容识别。该服务按调用量计费，需显式通过 `X-DashScope-DataInspection` 请求头启用，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 提供了完整的开通、授权与调用示例。

## 关键参数

| 参数名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `enable_encryption` / `enableEncrypt` | bool | SDK 级开关，启用后自动完成 AES 密钥生成、RSA 加密、请求体加密与响应解密 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | string | HTTP 请求头，用于传递经 RSA 加密后的 AES 密钥（Base64 编码） | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | JSON string | HTTP 请求头，值为 `{"input":"cip","output":"cip"}` 表示对输入输出均启用内容检查 | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `public_key_id` & `public_key` | string | 从 `/api/v1/public-keys/latest` 接口获取，用于手动实现加解密逻辑 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

> **注意**：文档 5 的标题为“私网访问配置”，但其内容实际指向 `secure-storage`（安全存储）子目录下的多篇文档，与文档 6 中定义的 `transmission-security/access-model-studio-through-privatelink`（PrivateLink 模式）属于不同技术栈——前者面向安全存储业务空间的专有网络资源编排，后者面向通用模型/API 的 VPC 直连。二者不可混用，开发者需根据业务空间类型（普通 vs 安全存储）选择对应方案。

## 使用方式

### 1. 传输加密（推荐使用 SDK）
- **前提**：已获取 API Key 并配置至环境变量（如 `DASHSCOPE_API_KEY`）。
- **Python SDK**：在 `Generation.call()` 中设置 `enable_encryption=True`，SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥并完成加解密。
- **Java SDK**：在 `GenerationParam.builder()` 中调用 `.enableEncrypt(true)`。
- **HTTP 手动调用**：需先调用 `GET /api/v1/public-keys/latest` 获取 `public_key`，再自行实现 AES 加密 `input`、RSA 加密 AES 密钥，并将密文填入 `X-DashScope-EncryptionKey` 头。

### 2. 私网访问
- **PrivateLink 模式（通用模型/API）**：
  1. 在百炼控制台 **管理 > 网络配置** 添加私网连接，关联目标 VPC 与可用区交换机；
  2. 在 **业务空间管理** 中将目标业务空间与该私网连接绑定；
  3. 替换 API 调用域名：将 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com` 替换为生成的私网域名 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`。
- **安全存储业务空间模式（专用网络资源）**：
  1. 创建安全存储业务空间 → 配置反向终端节点 → 关联 MSE 网关与可用区 VIP；
  2. 依次配置 OSS（含标签授权）、ADB、ES（含白名单）等后端资源；
  3. 在 MSE 网关中创建服务与路由，将请求转发至对应云产品地址。

### 3. AI 安全护栏
- 开通服务：访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 完成购买；
- 授权：在百炼控制台 **安全管理 > 全局设置** 页面单击“去授权”；
- 调用：在请求头中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`（注意：值为 JSON 字符串，非对象）。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储业务空间相关配置（如终端节点、MSE 网关）仅支持华北2（北京）。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，不再支持归属 RAM 用户。RAM 用户的 API Key 在被移出业务空间后将失效（重新加入可恢复），但在 RAM 控制台删除该用户时将永久失效。
- **模型备案责任**：百炼公示的算法备案号（如 `网信算备330110507206401230035号`）和大模型备案号（如 `ZheJiang-TongYiQianWen-20230901`）由模型提供方（如达摩院、DeepSeek）完成，[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 与 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 明确指出：**应用/小程序开发者作为服务提供者，须独立承担备案主体责任**，阿里云仅提供技术支持与备案信息查询指引。
- **加密与私网不互斥**：可在私网域名上调用加密接口（即同时启用 `enable_encryption=True` 与私网域名），此时数据在 VPC 内仍保持加密状态，提供双重防护。
- **安全存储业务空间依赖强**：OSS Bucket 或 ES 实例若被释放，将导致整个安全存储业务空间不可用且无法恢复，必须重建新空间。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)


