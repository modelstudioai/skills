# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限控制、内容安全、模型备案及数据隐私保护等关键维度。所有功能均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地调用大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES 加密，并通过 RSA 公钥安全分发 AES 密钥，全程保障敏感数据在公网传输中的机密性与完整性。该能力适用于所有支持 `Generation` 接口的文本类模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了加解密流程与 SDK 集成方式。
- **私网访问**：支持两种私网方案：
  - **PrivateLink 方式**：通过百炼控制台配置 VPC 私网连接，将流量完全限制在阿里云内网，适用于通用模型与应用 API 调用，[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 提供完整配置步骤；
  - **安全存储空间模式**：专为高敏感场景设计，需配合反向终端节点、MSE 网关及专属云资源（OSS/ADB/ES）构建全链路私有网络，详见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。
- **AI 安全护栏**：支持在请求头中启用输入/输出内容安全检测（`X-DashScope-DataInspection`），自动拦截涉黄、涉政、广告等违规内容，目前覆盖文本与图片类模型。
- **模型备案信息**：所有上架模型均完成国家网信办算法备案与大模型备案，备案号及主体信息在 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md) 中公开可查，满足《生成式人工智能服务管理暂行办法》第十七条要求。

## 关键参数

| 参数名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | boolean | SDK 启用传输加密的开关 | `True`（Python）、`true`（Java） |
| `X-DashScope-EncryptionKey` | string | HTTP 请求头，携带经 RSA 加密的 AES 密钥（仅手动调用时需设置） | `"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB\n-----END PUBLIC KEY-----"` |
| `X-DashScope-DataInspection` | string (JSON) | 启用 AI 安全护栏的请求头，值为 JSON 字符串（非对象） | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` | string | 从 `/api/v1/public-keys/latest` 接口返回的公钥标识符，用于密钥轮转 | `"1"` |

> **注意**：`X-DashScope-EncryptionKey` 仅在手动 HTTP 调用时需显式构造；使用 DashScope SDK 时只需设置 `enable_encryption=True`，SDK 自动完成公钥获取、AES 密钥生成与加解密，无需手动处理 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 接口。

## 使用方式

### 1. 传输加密（推荐 SDK 自动模式）
- **前提**：已配置 `DASHSCOPE_API_KEY` 环境变量（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）。
- **Python 示例**：
  ```python
  import dashscope
  response = dashscope.Generation.call(
      model="qwen-plus",
      messages=[{"role": "user", "content": "敏感问题"}],
      enable_encryption=True  # 自动启用加密
  )
  ```
- **Java 示例**：
  ```java
  GenerationParam param = GenerationParam.builder()
      .model("qwen-plus")
      .messages(messages)
      .enableEncrypt(true)  // 自动启用加密
      .build();
  ```

### 2. 私网访问（PrivateLink 模式）
- 在百炼控制台 **管理 > 网络配置 > VPC私网访问** 添加连接；
- 将业务空间关联该私网连接；
- 替换 API `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`），例如：
  ```python
  dashscope.base_http_api_url = "https://ws-abc123-vpc-xyz456.cn-beijing.maas.aliyuncs.com/api/v1"
  ```

### 3. AI 安全护栏
- 开通服务并授权（需主账号操作）：访问 [安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1) 页面；
- 在请求头中添加：
  ```http
  X-DashScope-DataInspection: {"input":"cip","output":"cip"}
  ```
  （注意：值为 JSON 字符串，非嵌套对象；DashScope SDK 使用 `headers={...}`，OpenAI SDK 使用 `extra_headers={...}`）

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持 **华北2（北京）** 和 **中国香港** 地域；安全存储空间模式当前仅支持 **华北2（北京）**；其他地域暂不支持 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **API Key 归属**：自 2026年3月25日起，华北2（北京）地域所有新创建的 API Key 均归属主账号，不可分配给 RAM 用户；RAM 用户的 API Key 在其被移出业务空间后立即失效（重新加入可恢复）[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **加密约束**：传输加密仅支持 Java 和 Python SDK；不支持自定义 AES 密钥；HTTP 手动调用需自行实现加解密逻辑，且必须调用 `/api/v1/public-keys/latest` 获取最新公钥 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。
- **安全存储空间依赖强**：OSS Bucket 或 ADB/ES 实例一旦被释放，将导致整个安全存储业务空间**不可恢复**，必须重建 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **备案责任主体**：阿里云提供模型算法备案号及合作协议模板，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户保护、安全评估及全部法律责任 [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)


