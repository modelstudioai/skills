# security and compliance

阿里云百炼平台提供端到端的[安全与合规](../concepts/security.md)能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段的 AES-256 对称加密 + RSA 公钥封装密钥的混合加密机制，适用于所有支持 `Generation` 接口的文本、多模态模型（如 `qwen-plus`, `qwen-flash`, `wanxiang` 等）[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，适用于华北2（北京）、中国香港地域的模型与应用 API；安全存储业务空间还支持更严格的反向终端节点架构，对接 ElasticSearch、ADB、OSS 等客户私有资源 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：默认启用基础内容过滤，可显式开启增强版输入/输出双路检测（`X-DashScope-DataInspection`），支持文本与图片类模型 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示，涵盖千问、万相、DeepSeek、Moonshot 等主流模型 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6 和文档 14 均提及“安全存储业务空间”，但文档 6 明确限定适用范围为“已申请开通百炼安全存储业务空间的用户”，而文档 14 仅作为目录页未说明准入条件。实际使用前请务必确认业务空间类型是否为“安全存储空间”，普通业务空间不支持反向终端节点等高级私网能力。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | boolean | SDK 中启用传输加密的开关 | `True` (Python), `true` (Java) |
| `X-DashScope-EncryptionKey` | string | HTTP 请求头，携带 RSA 加密后的 AES 密钥（Base64 编码） | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `X-DashScope-DataInspection` | string (JSON) | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非对象） | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` | string | 从 `/api/v1/public-keys/latest` 接口获取的当前有效公钥 ID | `"1"` |
| `Authorization` | string | API Key 鉴权头，格式为 `Bearer <API_KEY>` | `"Bearer sk-xxx"` |

## 使用方式

### 1. 传输加密（推荐 SDK 自动模式）
- 安装最新 DashScope SDK（Java ≥2.12.0，Python ≥1.14.0）；
- 调用时设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）；
- SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加解密 input/output，开发者无需处理密钥生命周期 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 2. 私网访问
- **公网模型/API**：在控制台 **管理 > 网络配置** 添加私网连接，关联业务空间后获取私网域名 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`，替换 SDK 或 OpenAI 兼容模式的 `base_url`；
- **安全存储业务空间**：需额外执行四步流程：① 创建反向终端节点；② 配置可用区 VIP；③ 在 VPC 内配置 OSS/ADB/ES 等资源白名单与授权；④ 配置 MSE 云原生网关路由 [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)。

### 3. AI 安全护栏
- 开通服务并完成控制台授权（需主账号操作）；
- 在请求 header 中添加 `X-DashScope-DataInspection`，值为 JSON 字符串（注意引号转义）；
- 检测失败时返回 `400` 状态码与 `data_inspection_failed` 错误码，无模型响应体。

## 限制和注意事项

- **权限粒度**：业务空间是权限最小管理单元，**默认业务空间无法设置模型调用/训练/部署限流**，仅自建业务空间支持精细化管控 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **地域限制**：
  - 私网访问（PrivateLink）仅支持华北2（北京）、中国香港地域；
  - 安全存储业务空间相关功能（反向终端节点、MSE 网关）**仅支持华北2（北京）**，且专有网络必须包含可用区 G/H/L 中的至少两个。
- **API Key 绑定**：单个 API Key 严格绑定一个地域、一个业务空间、一个用户，不可跨空间/跨用户复用；华北2（北京）地域自 2026年3月25日起，新创建 API Key 默认归属主账号。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型再训练**，所有传输数据默认 AES-256 加密 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
- **备案责任主体**：使用百炼调用已备案模型（如千问）时，开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立履行内容审核、用户标识、安全评估等法定义务，阿里云仅提供备案信息与技术支持。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)


