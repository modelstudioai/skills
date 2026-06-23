# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖权限管理、传输加密、私网访问、内容安全护栏、安全存储以及合规备案等方面。开发者可根据业务场景组合使用这些能力，满足从开发到生产环境的安全合规要求。

## 权限管理

百炼的权限体系以**[业务空间](../concepts/workspace.md)**为最小管理单元，支持基于控制台页面级和模型级的多维度权限控制，适用于多地域、多用户的组织架构。

### 角色体系

平台定义了三种角色：

| 角色 | 主要权限 |
|------|---------|
| **超级管理员**（阿里云主账号或拥有 AliyunBailianFullAccess 策略的 RAM 用户） | 跨空间管理用户权限、模型授权与限流、API Key 管理 |
| **[业务空间](../concepts/workspace.md)管理员** | 管理特定空间内的用户权限和 API Key |
| **普通用户** | 使用被授权的空间、页面和资源 |

### [业务空间](../concepts/workspace.md)权限

单个[业务空间](../concepts/workspace.md)不能跨地域存在，每个地域的默认[业务空间](../concepts/workspace.md)也是独立的空间。超级管理员可在空间内执行以下管控操作：

- **限制模型调用**：控制特定模型的调用权限，并设置请求数和 Token 限流（默认空间不支持此限制）
- **限制模型训练与部署**：管理模型的调优和部署权限
- **用户控制台权限管理**：控制 RAM 用户可使用的控制台功能页面

### API Key 权限

API Key 归属于特定地域内的一个[业务空间](../concepts/workspace.md)和一个用户，不能转移。其可调用的功能和模型限流与归属[业务空间](../concepts/workspace.md)一致，不受用户控制台权限的影响。

> **注意**：自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号。

### OpenAPI 接口权限

RAM 用户默认无权调用百炼应用的 Open API（知识库、[Prompt 工程](../concepts/prompt-engineering.md)、长期记忆等）。需要阿里云主账号在 RAM 控制台授予 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

详细的权限管理配置请参见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

### 生产环境最佳实践

- **空间规划**：建议按环境（dev/test/prod）或按业务线划分[业务空间](../concepts/workspace.md)，实现隔离
- **限流策略**：将主账号总配额按比例分配给各空间，并预留缓冲应对突发流量

## 传输安全

### 加密调用模型推理

当请求内容包含敏感信息时，可对请求体中的 `input` 字段进行加密传输。平台采用**混合加密机制**：数据由 AES 对称算法加密，AES 密钥通过 RSA 非对称加密传输。

**[DashScope SDK](../concepts/dashscope-sdk.md) 方式（推荐）**：SDK 封装了加解密逻辑，只需启用加密功能即可：

```python
# Python SDK
response = dashscope.Generation.call(
    model="qwen-plus",
    messages=messages,
    enable_encryption=True
)
```

```java
// Java SDK
GenerationParam param = GenerationParam.builder()
    .model("qwen-plus")
    .enableEncrypt(true)
    .build();
```

**HTTP 手动加密方式**：需自行生成 AES 密钥、获取 RSA 公钥（通过 `GET /api/v1/public-keys/latest` 接口）、加密 `input` 内容，并在请求头中携带 `X-DashScope-EncryptionKey`。此方式仅适用于 DashScope Endpoint，不支持 OpenAI 兼容 Endpoint。

详细加解密流程请参见 [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)，公钥接口说明请参见 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)。

### 私网访问（PrivateLink）

通过创建接口终端节点，可在 VPC 内直接调用百炼 API，流量不经过公网。

**支持地域**：华北2（北京）、新加坡（美国弗吉尼亚暂不支持）。

**核心步骤**：

1. 在终端节点控制台创建接口终端节点，选择 `com.aliyuncs.dashscope` 服务
2. 获取终端节点服务域名（默认域名仅支持 HTTP，自定义域名支持 HTTPS）
3. 将 API 请求中的域名替换为终端节点服务域名

**跨地域访问**：

- 同境内/同境外跨地域：启用跨地域端点
- 跨境跨地域：通过 CEN 实现 VPC 互通

详细配置请参见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 输入输出 AI 安全护栏

百炼支持接入 AI 安全护栏服务，对模型的输入输出内容进行违规识别（涉黄、涉政、广告等），在模型自有合规检查之上提供额外保障。

**接入步骤**：

1. 开通内容审核服务
2. 在安全管理页面完成授权
3. 在请求头中设置 `X-DashScope-DataInspection` 参数：

```json
{
    "X-DashScope-DataInspection": {
       "input": "cip",
       "output": "cip"
    }
}
```

当输入或输出触发安全护栏时，接口将返回 `data_inspection_failed` 错误码。详细说明请参见 [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 安全存储

百炼提供**安全存储[业务空间](../concepts/workspace.md)**，面向对数据隔离有严格要求的企业用户。安全存储空间通过私网终端节点将百炼平台与用户自有的云资源（OSS、AnalyticDB、ElasticSearch）连通，确保数据在用户控制的环境中存储和处理。

配置流程：

1. [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md) — 创建反向终端节点，建立私网通道
2. [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md) — 创建 MSE 云原生网关并配置可用区 VIP
3. [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md) — 配置 OSS Bucket、ADB、ElasticSearch 实例
4. [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md) — 创建服务与路由，激活安全存储空间

> **注意**：安全存储功能需要提前申请开通，请咨询商务人员。OSS Bucket 或 ES 实例被释放将导致安全存储空间不可用且无法恢复。

## 合规与备案

### 合规资质

百炼已通过 SOC 2 审计（无保留意见），在安全、可用性和保密性方面符合国际标准。

### 隐私保护

- 阿里云**不会**将用户数据用于模型训练
- 传输数据经过 AES-256 加密
- 根据法规要求，百炼会存储模型与应用调用时产生的数据，具体条款详见《阿里云百炼服务协议》

详细说明请参见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。

### 模型备案

百炼平台接入的大模型均已完成算法备案，涵盖千问、万相、智谱、DeepSeek、Moonshot、MiniMax、阶跃星辰等模型。开发者如需将接入百炼模型的应用上架应用市场，需根据《生成式人工智能服务管理暂行办法》提供备案信息和合作协议等材料。备案信息可在[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)查询。

详细的备案编号列表请参见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)，上架指南请参见 [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)




