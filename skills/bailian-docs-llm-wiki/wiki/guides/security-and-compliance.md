# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖身份权限、传输加密、私网隔离、内容安全、模型备案及数据隐私等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足国内监管要求（如《生成式人工智能服务管理暂行办法》）的同时，构建高可信的AI应用。

## 支持的模型/功能

- **模型范围**：所有接入百炼平台的官方模型（如 Qwen 系列、万相、可灵、DeepSeek、Moonshot 等）均默认启用基础内容安全过滤，并支持按需接入 AI 安全护栏服务进行增强检测。具体模型与算法备案对应关系详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。
- **安全功能**：
  - 输入/输出内容安全检测（涉黄、涉政、广告等违规内容识别）
  - TLS 1.2+ 全链路 HTTPS 加密传输
  - RSA-AES 混合加密（支持 `enable_encryption=True` 自动启用）
  - PrivateLink 私网访问（VPC 内流量全程内网，不经过公网）
  - 安全存储业务空间（专用于敏感数据场景，需独立开通并配置私有网络资源）
- **合规资质**：百炼已通过 SOC 2 Type II 无保留意见审计，符合国际安全、可用性与保密性标准；所有大模型均完成国家网信办算法备案及大模型备案，备案信息实时同步至 [互联网信息服务算法备案系统](https://beian.cac.gov.cn)。

> **注意**：文档 7–10 描述的“安全存储业务空间”为独立产品形态，仅限已签约开通的客户使用，其私网架构（反向终端节点 + MSE 网关 + 专属 VPC 资源）与文档 6 中面向通用用户的 PrivateLink 私网访问（正向终端节点）在技术路径、控制台入口和适用范围上存在本质差异，二者不可混用。开发者应根据实际场景选择：通用 API 调用请参考 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)，高敏数据隔离场景请咨询商务获取安全存储空间开通权限。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `X-DashScope-DataInspection` | 启用 AI 安全护栏的请求头，值为 JSON 字符串 | `{"input":"cip","output":"cip"}` | [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) |
| `enable_encryption` / `enableEncrypt` | SDK 中启用混合加密的布尔开关 | `True` (Python), `true` (Java) | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `X-DashScope-EncryptionKey` | HTTP 手动调用时携带的 AES 密钥（经 RSA 公钥加密后 Base64 编码） | `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` | [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) |
| `Authorization: Bearer <API_KEY>` | 所有 API 调用必需的身份凭证 | `Bearer sk-xxx` | [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) |

## 使用方式

### 1. 权限控制
- 使用**超级管理员**（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在全局管理菜单（[北京](https://bailian.console.aliyun.com/settings/workspace) 等）统一配置业务空间、模型授权、API Key 及限流策略。
- **业务空间管理员**可在所属空间内管理用户页面权限、模型调用/训练/部署开关，但无法跨空间操作。
- API Key 的模型调用权限完全继承自其归属业务空间的模型授权设置，与用户控制台权限无关。

### 2. 传输加密
- **SDK 快速启用**：Python 中设置 `enable_encryption=True`，Java 中设置 `.enableEncrypt(true)`，SDK 自动完成公钥获取、AES 密钥生成、加解密全流程。
- **HTTP 手动调用**：
  1. 调用 `GET /api/v1/public-keys/latest` 获取最新 RSA 公钥及 ID；
  2. 生成随机 AES 密钥，用 RSA 公钥加密该密钥，Base64 编码后放入 `X-DashScope-EncryptionKey` 请求头；
  3. 用 AES 密钥加密 `input` 字段（如 `messages`），发送请求。

### 3. 私网访问
- **通用场景（推荐）**：在百炼控制台「网络配置」中添加 PrivateLink 私网连接，关联业务空间后获取私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），替换 API `base_url` 即可调用。
- **高敏数据场景（需开通）**：通过 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 等系列文档配置安全存储业务空间，实现 VPC 内网直连 + MSE 网关 + 专属 ADB/ES/OSS 隔离存储。

### 4. 内容安全
- 开通 AI 安全护栏服务后，在请求头中添加 `X-DashScope-DataInspection`，指定 `"input"` 和 `"output"` 的检测策略（`"cip"` 表示启用内容安全检查）。
- 检测失败时返回 HTTP 400 及 `data_inspection_failed` 错误码，响应体含详细拒绝原因。

## 限制和注意事项

- **API Key 生命周期**：自 2026年3月25日起，华北2（北京）地域新创建的 API Key 均归属主账号；此前由 RAM 用户创建的 API Key 在其被删除时将同步失效且不可恢复。建议生产环境优先使用主账号 API Key 或确保 RAM 用户生命周期管理与 API Key 使用解耦。
- **加密限制**：DashScope SDK 的自动加密功能仅支持 Java 和 Python；其他语言需自行实现混合加密逻辑，参见 [HTTP调用（手动密钥管理）](https://help.aliyun.com/zh/model-studio/encrypted-access-to-model-inference#f9489ce581691)。
- **私网域名解析**：PrivateLink 私网域名仅在所选 VPC 内可解析，ECS/容器等计算资源必须部署于该 VPC 下才能访问；跨账号共享 VPC 需提前完成 [跨账号访问](#cross-account-vpc-sharing) 授权。
- **数据隐私承诺**：阿里云百炼**绝不会**将您的输入数据用于模型再训练；所有传输数据默认采用 AES-256 加密，静默数据按《阿里云百炼服务协议》约定存储与处理。
- **备案责任主体**：根据《生成式人工智能服务管理暂行办法》，应用/小程序开发者是法定“服务提供者”，须独立承担内容审核、用户保护、算法备案等全部义务；百炼仅作为“服务技术支持者”提供模型及备案信息，不替代开发者履行主体责任。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


