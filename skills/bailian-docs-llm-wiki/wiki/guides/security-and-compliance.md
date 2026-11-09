# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限控制、内容安全、算法备案及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足监管要求的前提下安全、可控地使用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，密钥通过平台托管的 RSA 公钥安全分发，适用于敏感数据场景。该能力已集成至 DashScope SDK（Python/Java），开箱即用 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：提供两种私网方案：
  - **PrivateLink 终端节点**：适用于标准业务空间，通过 VPC 内网直连百炼 API，流量全程不经过公网 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)；
  - **安全存储业务空间**：专为高安全要求场景设计，需配合 MSE 云原生网关、反向终端节点及可用区 VIP 配置，实现对 OSS/ADB/ES 等后端资源的完全私有化访问 [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)。
- **AI 安全护栏**：仅华北2（北京）地域可用，支持对输入/输出内容进行实时合规检测（如涉黄、涉政、广告等），需在请求头中显式设置 `X-DashScope-DataInspection` [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **算法与模型备案**：平台已为接入的主流大模型（如千问、万相、DeepSeek、Moonshot 等）完成《生成式人工智能服务管理暂行办法》要求的算法备案及大模型备案，备案信息可公开查询 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 12 与文档 13 均列出“千问”的备案号为 `网信算备330110507206401230035号`，但文档 12 中描述其算法名称为“达摩院交互式多能型合成算法”，而文档 13 表格中对应列为“达摩院交互式多能型合成算法”——二者一致；然而文档 12 的“备案主体”写为“阿里巴巴达摩院(杭州)科技有限公司”，文档 13 未重复声明主体，属信息互补，**无实质性矛盾**。但需注意：文档 12 明确指出“备案信息应以互联网信息服务算法备案系统实时查询结果为准”，开发者必须自行核验。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `enable_encryption=True` (Python) / `enableEncrypt=true` (Java) | SDK 启用传输加密的开关 | `True` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-DataInspection` | AI 安全护栏开关，JSON 字符串格式 | `'{"input":"cip","output":"cip"}'` | [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动加密时，用于传递 RSA 加密后的 AES 密钥 | Base64 编码字符串 | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `public_key_id`, `public_key` | 从 `/api/v1/public-keys/latest` 接口获取的 RSA 公钥元数据 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8..."` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

- **传输加密**：
  - SDK 方式（推荐）：安装 `dashscope>=2.0.1`（Python）或 `dashscope-java>=2.12.0`（Java），调用时设置 `enable_encryption=True` 或 `.enableEncrypt(true)`，SDK 自动完成公钥获取、AES 密钥生成、加解密全流程。
  - HTTP 方式：先调用 `GET /api/v1/public-keys/latest` 获取最新 `public_key` 和 `public_key_id`，再用该 RSA 公钥加密随机生成的 AES 密钥，并将密文放入 `X-DashScope-EncryptionKey` 请求头，同时对 `input` 字段进行 AES 加密。
- **私网访问**：
  - PrivateLink：在百炼控制台「网络配置」中添加私网连接 → 关联目标业务空间 → 获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）→ 替换 SDK 或 OpenAI 兼容模式的 `base_url`。
  - 安全存储空间：需按顺序完成「配置终端节点并发起连接」→「配置可用区IP」→「配置私有网络中的资源（OSS/ADB/ES）」→「配置MSE云原生网关」→「激活业务空间」[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：
  - 控制台开关（仅北京）：超级管理员可在「安全管理」页面全局开通，或在业务空间高级配置中开启输入/输出检测开关。
  - 请求头方式（通用）：在任意调用请求的 header 中添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`（注意是 JSON 字符串，非对象）。
- **合规材料获取**：
  - 算法备案截图：访问 [互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)，用文档 13 中公示的备案编号（如 `网信算备330110507206401230035号`）搜索并截图完整页面。
  - 合作协议：联系商务经理申请含【算法名称】和【备案编号】的正式合作协议。

## 限制和注意事项

- **地域限制**：
  - AI 安全护栏仅在华北2（北京）地域可用，其他地域调用该 header 将被忽略 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
  - 安全存储业务空间当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **权限与生命周期**：
  - API Key 严格绑定单一业务空间和用户，不可跨空间或跨用户转移；2026年3月25日后新创建的 API Key 归属主账号，与 RAM 用户解耦，删除 RAM 用户不再导致 API Key 失效 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
  - 默认业务空间无法设置模型调用/训练/部署授权及限流，仅自定义业务空间支持精细化管控。
- **安全实践强制要求**：
  - API Key 必须配置在环境变量中，禁止硬编码于源码或配置文件内 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
  - OSS Bucket 必须设置标签 `bailian-safe-workspace-oss-access: ReadAndWrite` 才能被安全存储空间识别和授权 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **数据与合规责任**：
  - 阿里云百炼承诺不将客户数据用于模型训练，并采用 AES-256 加密传输 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
  - **开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担应用/小程序的全部合规责任**，包括但不限于内容审核、用户标识、安全评估及算法备案，阿里云仅提供技术支持与备案信息 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


