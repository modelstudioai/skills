# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、网络隔离、权限控制、内容安全、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`, `qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 提供完整实现路径。
- **私网访问**：支持通过阿里云 PrivateLink 建立 VPC 到百炼服务的内网连接，流量全程不经过公网。当前仅华北2（北京）、中国香港地域支持，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 文档详细说明配置流程。
- **AI 安全护栏**：支持在请求头中设置 `X-DashScope-DataInspection`，启用输入输出双路内容安全检测（涉黄、涉政、广告等），适用于所有已接入该服务的文本与图像模型，[输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md) 提供调用示例与错误处理说明。
- **模型备案信息**：平台所接入的千问、万相、DeepSeek 等主流模型均已取得国家网信办算法备案号及大模型备案号，相关信息在控制台及文档中公示，[模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 和 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 两篇文档分别提供备案号列表与上架材料指引。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `X-DashScope-EncryptionKey` | Header (string) | 封装加密后的 AES 密钥（Base64 编码），仅在手动加密时需显式设置 | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `X-DashScope-DataInspection` | Header (JSON string) | 启用 AI 安全护栏的开关，值为 JSON 字符串而非对象 | `'{"input":"cip","output":"cip"}'` |
| `enable_encryption` / `enableEncrypt` | SDK boolean | DashScope Python/Java SDK 中启用自动加解密的开关 | `True` / `true` |
| `public_key_id` | Response field | 从 `/api/v1/public-keys/latest` 接口返回，用于标识当前生效的 RSA 公钥版本 | `"1"` |

> **注意**：`X-DashScope-DataInspection` 的值必须是合法 JSON 字符串（即用单引号包裹的双引号 JSON），若传入嵌套 JSON 对象（如 `{input: "cip"}`）将导致 400 错误。详见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 使用方式

### 1. 传输加密（推荐使用 SDK 自动模式）
- **前提**：确保 DashScope SDK 版本 ≥ 1.14.0（Python）或 ≥ 2.12.0（Java）。
- **Python 示例**：
  ```python
  import dashscope
  response = dashscope.Generation.call(
      model="qwen-plus",
      messages=[{"role": "user", "content": "敏感问题"}],
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      enable_encryption=True  # SDK 自动获取公钥、生成 AES 密钥、加解密
  )
  ```
- **手动模式**（仅限 HTTP 调用）：先调用 `/api/v1/public-keys/latest` 获取 `public_key` 和 `public_key_id`，再自行完成 AES 加密与 RSA 加密，最后将密文放入 `input` 并设置 `X-DashScope-EncryptionKey` 头。详情见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 2. 私网访问（PrivateLink）
- 在百炼控制台 **管理 > 网络配置 > VPC私网访问** 中添加私网连接，选择目标 VPC 与可用区。
- 在业务空间高级配置中关联该私网连接。
- 将 API 请求的 `base_url` 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供各 SDK 的替换示例。

### 3. AI 安全护栏
- 开通服务并完成授权（需主账号操作）：进入 **安全管理 > 全局设置** 页面点击“去授权”。
- 在请求头中添加 `X-DashScope-DataInspection`，值为 `'{"input":"cip","output":"cip"}'`（注意外层单引号）。
- 若检测失败，响应状态码为 `400`，`code` 字段为 `data_inspection_failed` 或 `DataInspectionFailed`。

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港地域；安全存储业务空间（含反向终端节点）目前仅支持华北2（北京）地域，且专有网络需满足可用区 G/H/L 组合要求。[配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) 明确了该约束。
- **权限继承规则**：API Key 的模型调用权限完全继承自其归属的**业务空间**，与创建该 Key 的用户（RAM 用户）在控制台的页面权限无关。例如，某 RAM 用户被禁止访问“模型体验”页面，但其 API Key 仍可调用已授权模型。详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **安全存储业务空间特殊性**：该类型空间（非默认业务空间）需额外配置 OSS/ADB/ES 等私有网络资源，并通过 MSE 网关路由。其开通流程与普通业务空间完全不同，且一旦释放 OSS/ES/ADB 实例，将导致整个安全存储空间不可恢复。相关配置请严格遵循 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) 文档。
- **合规责任主体**：阿里云百炼作为“服务技术支持者”，已提供所接入模型的算法备案号与合作协议模板；但根据《生成式人工智能服务管理暂行办法》，应用/小程序的最终上架主体（即开发者）是法定的“服务提供者”，须独立承担内容审核、用户保护、安全评估等全部法定义务。[千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md) 明确强调此责任划分。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


