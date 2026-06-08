# security and compliance

阿里云百炼平台提供多层次的安全与合规能力，覆盖权限管理、内容安全、传输加密、私网访问、安全存储以及算法备案等维度。开发者可根据业务场景选择性启用各项安全功能，满足从开发测试到生产环境的全链路安全需求。

## 权限管理

百炼的权限体系基于**[业务空间](../concepts/workspace.md)**作为最小管理单元，支持三种角色：

| 角色 | 关键能力 |
|------|----------|
| 超级管理员 | 跨空间管理模型授权、限流、用户和 API Key |
| [业务空间](../concepts/workspace.md)管理员 | 管理所属空间内的用户权限和 API Key |
| 普通用户 | 使用被授权的空间、页面和资源 |

**API Key 权限**：单个 API Key 归属一个地域内的一个[业务空间](../concepts/workspace.md)和一个用户，可调用模型与归属空间的权限保持一致，无需为不同模型类型创建不同 Key。自 2026 年 3 月 25 日起，华北2（北京）地域新创建的 API Key 均归属主账号。

**生产环境建议**：按环境划分业务空间（dev/test/prod），并将主账号总配额按比例分配给各空间，预留缓冲应对突发流量。详见[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。

**OpenAPI 接口权限**：RAM 用户默认无权调用百炼应用的数据、知识库等 OpenAPI，需主账号在 RAM 控制台添加 `AliyunBailianDataFullAccess` 或 `AliyunBailianDataReadOnlyAccess` 策略。

## 内容安全（AI 安全护栏）

百炼支持接入 AI 安全护栏服务，对模型输入输出进行违规内容检测（涉黄、涉政、广告等）。配置步骤：

1. 开通内容审核服务（购买页一键开通）
2. 在百炼安全管理页面完成授权
3. 在请求头中添加 `X-DashScope-DataInspection` 参数：

```json
{
  "X-DashScope-DataInspection": {
    "input": "cip",
    "output": "cip"
  }
}
```

触发内容安全拦截时，API 返回错误码 `data_inspection_failed`（HTTP 400）。目前支持文本和图片类型的模型。详见[输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。

## 传输安全

### 加密推理调用

对请求体中的 `input` 字段进行 AES+RSA 混合加密，防止数据在传输中被窃听或篡改：

- **DashScope SDK（推荐）**：设置 `enableEncrypt(true)`（Java）或 `enable_encryption=True`（Python）即可，SDK 自动处理加解密
- **HTTP 手动加密**：生成 AES 密钥 → 加密 input → 用 RSA 公钥加密 AES 密钥 → 在 `X-DashScope-EncryptionKey` 头中传递密钥信息

RSA 公钥通过 `GET /api/v1/public-keys/latest` 接口获取。详见[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

> **注意**：加密调用仅适用于 DashScope Endpoint，OpenAI 兼容模式（Chat Completions API 和 Responses API）的 Endpoint 不支持此加密机制。

### PrivateLink 私网访问

通过在 VPC 中创建接口终端节点，将百炼 API 调用流量限制在阿里云内网：

1. 创建接口终端节点，选择服务 `com.aliyuncs.dashscope`
2. 获取终端节点服务域名
3. 将 API base_url 中的域名替换为终端节点域名

支持地域：华北2（北京）、新加坡（美国弗吉尼亚暂不支持）。跨地域私网访问可通过启用跨地域端点或 CEN 实现。详见[通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。

## 安全存储业务空间

面向对数据隔离有严格要求的场景，百炼提供安全存储业务空间，将数据存储在用户自有的私有网络资源中（ElasticSearch、AnalyticDB、OSS）。配置流程：

1. 创建安全存储业务空间并配置反向终端节点
2. 配置可用区 IP（创建 MSE 云原生网关 → 获取 NLB VIP）
3. 配置私有网络资源（OSS Bucket、ADB 实例、ES 实例）
4. 配置 MSE 路由并激活空间

> **注意**：安全存储业务空间需要商务开通。OSS Bucket 或 ES 被释放将导致空间不可用且无法恢复，需重新创建。

## 合规与备案

### 合规资质

百炼已通过 SOC 2 审计（无保留意见），在安全、可用性和保密性方面符合国际标准。阿里云不会将用户数据用于模型训练，传输数据经 AES-256 加密。

### 算法备案

平台接入的主要模型备案信息：

| 模型 | 备案编号 |
|------|----------|
| 千问 | 网信算备330110507206401230035号 |
| 万相（图像） | 网信算备330110507206401230027号 |
| 万相（视频） | 网信算备330106003156001240091号 |
| DeepSeek | 网信算备110108970550101240011号 |
| 智谱 AI | 网信算备110108105858001230027号 |

开发者上架使用百炼模型的应用需提供算法备案信息和合作协议。面向 C 端且具有舆论属性的应用还需完成安全评估报告和自主算法备案。详见[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

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


