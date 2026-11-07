# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限管控、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成和使用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES 对称加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 模式**：适用于标准业务空间，通过终端节点将 VPC 流量直连百炼网关，无需修改应用代码，仅需替换 API 域名为私网域名，详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **安全存储空间模式**：专为高合规要求场景设计，需配置反向终端节点、MSE 网关、OSS/ADB/ES 等后端资源，实现全链路私有网络隔离，其完整配置流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：仅在华北2（北京）地域可用，支持对输入（`input`）和输出（`output`）内容进行实时违规检测（涉黄、涉政、广告等）。调用时需设置 `X-DashScope-DataInspection` 请求头，或在业务空间维度统一开启开关，具体参见 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案信息**：平台已公示所接入大模型的算法备案号与大模型备案号，涵盖千问、万相、DeepSeek、Moonshot 等主流模型，开发者可直接用于应用上架合规申报，详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 6（`secure-storage.md`）标题为“私网访问配置”，但其子文档（文档 7–10）实际描述的是**安全存储业务空间**（一种专属私有部署形态），与文档 5 中面向通用业务空间的 **PrivateLink 私网连接** 属于不同技术路径和适用场景。前者需额外购买 MSE、ADB、ES 等资源并完成复杂网络配置；后者仅需控制台开通 PrivateLink 并绑定业务空间即可生效。二者不可混用，选型应基于合规等级与运维能力综合判断。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `enable_encryption=True` (Python) / `.enableEncrypt(true)` (Java) | DashScope SDK 启用自动加解密的开关，SDK 内部自动调用公钥接口并管理 AES 密钥生命周期 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非嵌套对象），`cip` 表示启用内容安全检查 | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密模式下，用于传递经 RSA 公钥加密后的 AES 密钥的请求头 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id` & `public_key` | 从 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据，用于手动加密流程 | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

1. **传输加密（推荐 SDK 自动模式）**  
   安装最新版 DashScope SDK（Java ≥2.12.0，Python ≥2.0.1），在调用 `Generation.call()` 或 `client.chat.completions.create()` 时传入 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）。SDK 将自动完成公钥获取、AES 密钥生成、`input` 加密、密钥封装与响应解密，开发者仅处理明文输入输出。

2. **私网访问（PrivateLink）**  
   - 在百炼控制台「设置 > 网络配置」中开通 PrivateLink 并添加 VPC 终端节点；
   - 在「业务空间管理」中编辑目标空间，在「高级配置」中关联该终端节点；
   - 获取生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换原 API `base_url` 后发起调用。

3. **AI 安全护栏**  
   - 仅限北京地域，需先在「安全管理」页面完成服务开通与授权；
   - 调用时在请求头中添加 `X-DashScope-DataInspection`，值为 `{"input":"cip","output":"cip"}` 的字符串化 JSON；
   - 或在业务空间设置页开启全局开关，避免逐请求配置。

4. **合规备案材料准备**  
   - 直接引用 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中的备案编号与主体信息；
   - 通过 [互联网信息服务算法备案系统](https://beian.cac.gov.cn) 输入备案号验证并截图；
   - 如需合作协议，联系商务经理申请含【算法名称】与【备案编号】的正式协议文本。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅在北京地域可用；PrivateLink 私网连接支持北京、上海、杭州、深圳、乌兰察布、张家口六地；安全存储业务空间当前仅支持北京地域（华北2）。
- **API Key 生命周期**：自 2026年3月25日起，北京地域新创建的 API Key 归属主账号，与 RAM 用户解耦；此前创建的 RAM 用户级 API Key 在用户被删除时将同步失效且不可恢复。
- **模型权限粒度**：业务空间管理员无法管理模型调用/训练/部署权限，该能力仅对超级管理员开放；默认业务空间不支持任何模型级限流或授权控制。
- **加密兼容性**：DashScope SDK 的自动加密仅支持 Java 和 Python；其他语言需使用 HTTP 手动模式，并自行实现 AES/RSA 加解密逻辑。
- **数据隐私承诺**：阿里云明确声明**绝不会将客户数据用于模型训练**，所有传输数据默认采用 AES-256 加密，符合 SOC 2 审计要求，详情见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

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
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


