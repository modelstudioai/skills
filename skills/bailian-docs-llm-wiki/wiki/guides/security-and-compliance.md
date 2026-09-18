# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容审核、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了混合加密流程与 SDK 集成方式。
- **私网访问**：支持通过阿里云 PrivateLink 建立 VPC 到百炼服务的内网通道，流量全程不经过公网。当前仅支持华北2（北京）和中国香港地域，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供了完整的控制台配置与 SDK 调用示例。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection` 启用输入/输出双路内容安全检测，覆盖涉黄、涉政、广告等高风险内容。该能力与模型自动绑定，无需额外开通模型实例，详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高合规要求场景（如金融、政务），提供独立部署的“安全存储业务空间”，支持通过反向终端节点 + MSE 网关 + 专有网络资源（OSS/ADB/ES）构建全链路私有化数据平面，其配置流程见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

> **注意**：文档 5（`secure-storage.md`）仅列出子文档索引，未提供实质配置说明；实际操作应严格依据其引用的子文档（文档 6–9）执行。文档 6–9 构成完整闭环，但文档 6 中“安全组不需要配置任何出网和入网规则”的描述与文档 4、7 中明确要求安全组放行 443 端口存在矛盾。**请以文档 4 和文档 7 的实践为准：必须为安全组配置入方向 443 端口放行规则**。

## 关键参数

| 参数名 | 位置 | 类型 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | SDK 调用参数 | bool | 启用传输加密（自动获取公钥、生成 AES 密钥、加解密） | `True` (Python), `true` (Java) |
| `X-DashScope-EncryptionKey` | HTTP Header | string | 加密后的 AES 密钥（Base64 编码），由 SDK 自动填充 | `AQAA...` |
| `X-DashScope-DataInspection` | HTTP Header | string | JSON 字符串，指定输入/输出检测策略 | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应体 | string | 用于手动加密的 RSA 公钥材料，需定期轮换 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` |
| `Authorization` | HTTP Header | string | API Key 认证凭证，**必须配置在环境变量中**，禁止硬编码 | `"Bearer d1**2a"` |

## 使用方式

1. **传输加密（推荐）**  
   - Python：安装 `dashscope>=1.14.0`，调用时传入 `enable_encryption=True`，SDK 自动完成公钥获取、AES 加密、密钥封装与响应解密。  
   - Java：安装 `dashscope-sdk-java>=2.12.0`，设置 `.enableEncrypt(true)`。  
   - 手动 HTTP 调用：先调用 `GET /api/v1/public-keys/latest` 获取最新公钥，再用该公钥加密 AES 密钥，最后将加密后 input 与密钥头一并发送。详情见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

2. **私网访问**  
   - 在百炼控制台 **管理 > 网络配置** 开通 PrivateLink 并添加 VPC 连接；  
   - 在 **业务空间管理** 中将目标空间关联该私网连接；  
   - 将 API 请求的 `base_url` 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

3. **AI 安全护栏**  
   - 在请求 Header 中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`；  
   - 检测失败时返回 `400` 状态码与 `data_inspection_failed` 错误码，无模型响应。

4. **安全存储空间（高合规场景）**  
   - 申请开通“安全存储空间”类型业务空间；  
   - 依次完成：创建反向终端节点 → 配置 MSE 网关与可用区 VIP → 授权 OSS/ADB/ES → 激活空间。全流程依赖文档 6–9，不可跳步。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储空间当前仅支持华北2（北京）且需特定可用区（G/H/L）。
- **API Key 绑定**：每个 API Key 严格绑定**单个地域、单个业务空间、单个用户**，不可跨空间/跨地域复用；自 2026年3月25日起，华北2（北京）新创建的 API Key 默认归属主账号。
- **权限继承关系**：API Key 的模型调用权限与限流策略**完全继承自其归属业务空间的配置**，与用户（RAM 账号）的控制台页面权限无关；OpenAPI 接口权限（如知识库、Prompt 工程）需主账号在 RAM 控制台单独授权，普通 RAM 用户默认无权调用。
- **模型备案责任**：百炼公示的算法备案号（如 `网信算备330110507206401230035号`）和大模型备案号（如 `ZheJiang-TongYiQianWen-20230901`）仅证明技术提供方已履行备案义务；**应用/小程序开发者作为服务提供者，仍须独立承担上架合规责任**，包括但不限于签署合作协议、完成安全评估、补充算法备案（如适用）。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**；所有传输数据默认使用 AES-256 加密；日志与调用数据按《阿里云百炼服务协议》约定存储与处理。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)


