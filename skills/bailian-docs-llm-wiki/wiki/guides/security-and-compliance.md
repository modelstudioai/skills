# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，涵盖权限管理、数据传输加密、内容安全审核、私网访问、安全存储以及合规备案等方面。开发者可根据业务场景按需组合这些能力，构建从开发到生产的全链路安全体系。

## 权限管理

百炼基于**[业务空间](../concepts/workspace.md)**进行精细化权限管理，[业务空间](../concepts/workspace.md)是权限控制和账单分账的最小管理单元。权限体系包含三种角色：

- **超级管理员**：拥有 `AliyunBailianFullAccess` 系统策略的阿里云主账号或 RAM 用户，可跨空间统一管理用户权限、模型授权、限流和 API Key。
- **[业务空间](../concepts/workspace.md)管理员**：负责特定[业务空间](../concepts/workspace.md)内的用户权限和资源管理。
- **普通用户**：根据分配的权限使用资源。

| 权限项 | 超级管理员 | [业务空间](../concepts/workspace.md)管理员 | 普通用户 |
|--------|-----------|--------------|---------|
| 模型调用 & 限流 | 支持 | 不支持 | 不支持 |
| 模型调优/部署 | 支持 | 不支持 | 不支持 |
| 用户管理 | 支持 | 支持 | 不支持 |
| [API Key 管理](../concepts/api-key-management.md) | 支持 | 支持 | 不支持 |

### API Key 权限

单个 API Key 归属一个地域内的一个[业务空间](../concepts/workspace.md)和一个用户，不可转移。API Key 的可调用功能和模型限流与归属[业务空间](../concepts/workspace.md)一致，不受用户控制台权限管理的影响。华北2（北京）地域的 API Key 支持设置 IP 访问白名单。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的数据、知识库、[Prompt 工程](../concepts/prompt-engineering.md)等功能的 OpenAPI。需要阿里云主账号在 RAM 控制台为 RAM 用户添加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 权限。详见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 生产环境建议

- **按环境划分空间**（推荐）：为开发、测试、生产创建独立[业务空间](../concepts/workspace.md)，实现环境隔离。
- **限流策略**：将主账号总配额按比例分配给各[业务空间](../concepts/workspace.md)，预留缓冲应对突发流量。

## 数据传输加密

百炼支持对请求体中的 `input` 字段进行加密传输，采用混合加密机制：数据由 AES 对称算法加密，AES 密钥通过 RSA 非对称加密保护传输。

### DashScope SDK（自动加密）

Java SDK 设置 `enableEncrypt(true)`，Python SDK 设置 `enable_encryption=True` 即可开箱即用，SDK 自动完成加解密。

### HTTP 调用（手动密钥管理）

需要手动完成以下步骤：

1. 调用 `/api/v1/public-keys/latest` 获取 RSA 公钥（详见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)）。
2. 生成 AES 密钥并加密 `input` 内容。
3. 用 RSA 公钥加密 AES 密钥，放入 `X-DashScope-EncryptionKey` 请求头。
4. 对响应数据用 AES 密钥解密。

> **注意**：此加密机制仅适用于 DashScope 的 Endpoint，OpenAI 兼容模式的 Endpoint 不支持。

详见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

## 私网访问

### 通过 PrivateLink 私网访问 API

在 VPC 中创建接口终端节点，通过 PrivateLink 建立单向私网连接，流量不经过公网。支持的地域包括华北2（北京）和新加坡。

关键步骤：

1. 在终端节点控制台创建接口终端节点，终端节点服务选择 `com.aliyuncs.dashscope`。
2. 获取终端节点服务域名（默认域名仅支持 HTTP，自定义域名支持 HTTPS）。
3. 将 API `base_url` 中的域名替换为终端节点服务域名。

跨地域访问时，同境内可启用跨地域端点，跨境则需通过 CEN 实现 VPC 互通。详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## AI 安全护栏

百炼支持接入 AI 安全护栏服务，对输入输出内容进行违规信息识别。使用方式：

1. 开通内容审核服务。
2. 在安全管理页面完成授权。
3. 在请求头中设置 `X-DashScope-DataInspection`：

```json
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

当输入内容违规时，API 返回 `data_inspection_failed` 错误。详见 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 安全存储[业务空间](../concepts/workspace.md)

百炼提供安全存储[业务空间](../concepts/workspace.md)，支持在私有网络环境中部署应用，数据存储在客户自有的 ElasticSearch、AnalyticDB 和 OSS 中。配置流程：

1. **创建安全存储[业务空间](../concepts/workspace.md)**并配置反向终端节点。
2. **配置可用区 IP**：创建 MSE 云原生网关，获取可用区 VIP 并配置。
3. **配置私有网络资源**：分别配置 OSS Bucket（需设置 `bailian-safe-workspace-oss-access` 标签）、ADB 实例和 ES 实例。
4. **配置 MSE 云原生网关**：创建服务和路由，激活安全存储[业务空间](../concepts/workspace.md)。

> **注意**：安全存储[业务空间](../concepts/workspace.md)需要联系商务人员申请开通，且仅支持华北2（北京）地域。OSS Bucket 或 ES 实例被释放将导致安全存储空间不可用且无法恢复。

## 合规与备案

### 合规资质

百炼已通过 SOC 2 审计，在安全、可用性和保密性方面符合国际标准。详见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

### 隐私保护

阿里云不会将用户数据用于模型训练。传输数据经过 AES-256 加密，调用产生的数据按法规要求存储。

### 算法备案信息

根据《生成式人工智能服务管理暂行办法》，使用大模型的应用上架需完成合规备案。百炼平台主要模型的备案信息：

| 模型 | 算法名称 | 备案编号 |
|------|---------|---------|
| 千问 | 达摩院交互式多能型合成算法 | 网信算备330110507206401230035号 |
| 万相（图像） | 达摩院图像合成算法 | 网信算备330110507206401230027号 |
| 万相（视频） | 通义万相视频生成算法 | 网信算备330106003156001240091号 |

第三方模型（智谱 AI、DeepSeek、Moonshot、MiniMax、阶跃星辰等）的备案信息详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

### 上架合规流程

面向 C 端用户的应用需提供：算法备案信息、应用主体与阿里云的合作协议。具有舆论属性的应用还需完成安全评估报告和算法备案。详见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)








