# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、模型备案、权限控制及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，开发者可通过 API、SDK 或控制台按需启用，无需修改核心业务逻辑。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 加密，密钥通过平台托管的 RSA 公钥加密传输，适用于敏感数据场景。该能力已集成至 DashScope SDK（Python/Java），调用时设置 `enable_encryption=True` 即可自动完成密钥获取、加解密全流程 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。
- **私网访问**：提供两种私网方案：
  - **PrivateLink（正向连接）**：VPC 内资源通过终端节点服务域名访问百炼 API，流量全程走阿里云内网，适用于标准模型推理调用 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
  - **反向终端节点（安全存储空间）**：专用于百炼安全存储业务空间，实现百炼服务主动访问客户 VPC 内资源（如 OSS、ADB、ES），需配合 MSE 云原生网关使用 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}`，触发输入输出内容安全检测（涉黄、涉政、广告等），失败时返回 `data_inspection_failed` 错误码 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案与合规**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示，开发者可直接用于 App/小程序上架合规材料准备 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

> **注意**：文档 4（`secure-storage.md`）将“私网访问配置”作为一级标题，但其实际内容全部指向安全存储业务空间的反向连接流程，与文档 3 中定义的面向模型 API 的 PrivateLink（正向连接）属不同架构。二者不可混用：PrivateLink 用于客户端调用百炼 API；反向终端节点仅用于百炼安全存储空间访问客户私有资源。

## 关键参数

| 参数 | 位置 | 类型 | 说明 | 示例值 |
|------|------|------|------|--------|
| `X-DashScope-DataInspection` | 请求 Header | JSON string | 启用内容安全检测，值为字符串化 JSON | `'{"input":"cip","output":"cip"}'` |
| `X-DashScope-EncryptionKey` | 请求 Header | Base64 string | SDK 自动注入，包含 RSA 加密后的 AES 密钥 | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `enable_encryption` / `enableEncrypt` | SDK 参数 | boolean | 启用传输加密（Python/Java SDK） | `True` |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应 | string | 最新 RSA 公钥 ID 及 PEM 格式公钥值，用于手动加密 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` |

## 使用方式

### 1. 传输加密（推荐使用 SDK）
- **Python**：调用 `dashscope.Generation.call()` 时传入 `enable_encryption=True`，SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入请求头 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **Java**：在 `GenerationParam.builder()` 中调用 `.enableEncrypt(true)`。
- **HTTP 手动调用**：需先 GET `/api/v1/public-keys/latest` 获取 `public_key`，自行用 RSA 公钥加密 AES 密钥，再用 AES 密钥加密 `input`，最后将加密后 `input` 和 `X-DashScope-EncryptionKey` 头一起发送。

### 2. PrivateLink 私网访问（正向）
- 在 VPC 控制台创建接口终端节点，服务选择 `com.aliyuncs.dashscope`；
- 替换 API 调用的 `base_url` 域名为终端节点服务域名（如 `https://vpc-cn-beijing.dashscope.aliyuncs.com/compatible-mode/v1`）；
- 注意：默认服务域名仅支持 HTTP，如需 HTTPS 必须开启自定义服务域名 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

### 3. AI 安全护栏
- 在任意模型调用请求头中添加 `X-DashScope-DataInspection`，值为字符串化 JSON；
- 检测失败时 HTTP 状态码为 `400`，错误码为 `data_inspection_failed`，响应体含详细提示。

### 4. 权限最小化
- 使用 RAM 子账号而非主账号操作；
- 为子账号授予 `AliyunBailianFullAccess`（超级管理员）或业务空间级管理员策略；
- 通过业务空间粒度限制模型调用、训练、部署权限，并设置 Token/请求数限流；
- API Key 绑定单一业务空间，支持 IP 白名单（美国弗吉尼亚地域仅支持 IPv4）。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问暂不支持美国（弗吉尼亚）地域；安全存储业务空间仅支持华北2（北京）地域 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **加密限制**：DashScope SDK 的 `enable_encryption` 仅支持 Python 和 Java；不支持自定义 AES 密钥；HTTP 手动加密需自行管理密钥生命周期。
- **安全存储依赖强耦合**：OSS Bucket 若被释放，将导致安全存储空间**永久不可用且无法恢复**；ADB/ES 若停止计费或被释放，同样导致空间不可用 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：即使使用百炼提供的备案号，应用/小程序开发者仍为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、算法评估等全部法定义务 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。
- **数据隐私承诺**：百炼绝不会将您的输入数据用于模型训练；所有传输数据默认经 AES-256 加密；平台已通过 SOC 2 Type II 审计 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

## 来源文档

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
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)


