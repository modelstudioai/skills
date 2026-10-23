# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、权限精细化管控、模型备案、AI内容安全护栏及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地调用大模型服务。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段（含 `messages`）进行 AES-256 对称加密，密钥通过 RSA 公钥加密传输，全程保障敏感数据在公网链路中的机密性与完整性。该能力适用于所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`），[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档提供了完整流程。
- **私网访问**：支持通过 PrivateLink 建立 VPC 到百炼服务的内网直连，流量全程不经过公网；同时支持为安全存储业务空间配置专属私有网络资源（OSS/ADB/ES）及 MSE 云原生网关，实现数据存储与访问的物理隔离。相关能力详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md) 和 [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)。
- **AI 安全护栏**：默认启用基础内容过滤，可按需开通增强型 AI 安全护栏服务，对输入（`input`）和输出（`output`）分别执行涉政、涉黄、广告等高风险内容识别。该服务与模型自动绑定，无需为不同模型单独配置，具体接入方式见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **模型备案**：所有接入百炼的主流大模型（千问、万相、DeepSeek、Moonshot 等）均已取得国家网信办算法备案号及大模型备案号，信息在控制台及文档中实时公示，便于开发者完成上架合规材料准备，详见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)。

## 关键参数

| 参数 | 位置 | 说明 | 示例值 |
|------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | SDK 调用参数 | 启用传输加密的布尔开关，SDK 自动处理公钥获取、AES 密钥生成与加解密 | `True` (Python), `true` (Java) |
| `X-DashScope-EncryptionKey` | HTTP 请求头 | 加密后的 AES 密钥（Base64 编码），由 SDK 自动注入，手动调用时需自行填充 | `"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."` |
| `X-DashScope-DataInspection` | HTTP 请求头 | 启用 AI 安全护栏的 JSON 字符串，指定 input/output 检查策略 | `'{"input":"cip","output":"cip"}'` |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应体 | 用于手动加密的 RSA 公钥元数据，每次调用返回最新有效公钥 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` |
| IP 白名单 | API Key 管理页 | 限制该 API Key 仅允许从指定 IP 或 CIDR 段发起请求，全局生效 | `192.168.1.0/24`, `203.0.113.42` |

> **注意**：文档 2 中关于“API Key 的状态随归属用户操作的变化”表格存在过时风险——其注明“自 2026年3月25日开始，华北2（北京）地域的所有新创建的 API Key 均归属主账号”，但当前日期为 2025 年，该时间点尚未到达，实际行为请以控制台最新提示为准。

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   - 安装最新 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）；  
   - 在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True` 或 `.enableEncrypt(true)`；  
   - SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入请求头，响应自动解密。  
   > 手动 HTTP 调用需先调用 [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 接口，再自行实现混合加密逻辑。

2. **私网访问**  
   - 在百炼控制台 **设置 > 网络配置 > VPC私网访问** 中添加私网连接（需授权 `AliyunServiceRoleForBackrouterAccessNet` 角色）；  
   - 在 **业务空间管理** 中将目标业务空间与私网连接关联；  
   - 替换 API `base_url` 为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。

3. **AI 安全护栏**  
   - 访问 [AI 安全护栏购买页](https://common-buy.aliyun.com/?commodityCode=lvwang_guardrail_public_cn) 开通服务；  
   - 在百炼控制台 **设置 > 安全管理** 页面完成角色授权；  
   - 在模型调用请求头中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`。

4. **权限管理**  
   - 超级管理员（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）通过全局管理菜单（如 [北京](https://bailian.console.aliyun.com/settings/workspace)）跨空间管理模型限流、用户与 API Key；  
   - 业务空间管理员仅能管理本空间内模型调用/训练/部署授权及用户控制台页面权限；  
   - API Key 权限严格继承其归属业务空间的模型授权，与用户控制台权限无关。

## 限制和注意事项

- **传输加密限制**：仅支持 Java 和 Python SDK 的自动加密；其他语言需手动实现 HTTP 调用流程；不支持自定义 AES 密钥，密钥由 SDK 随机生成。
- **私网访问限制**：PrivateLink 私网连接仅支持华北2（北京）、华东2（上海）等 6 个地域；安全存储业务空间的私网配置（终端节点、可用区IP、MSE网关）目前仅限公共云“华北2（北京）”地域，且专有网络必须包含至少两个指定可用区（G/H/L）。
- **AI 安全护栏限制**：`X-DashScope-DataInspection` 头部值必须为合法 JSON 字符串（双引号转义），若格式错误将导致 400 错误；启用后，违规输入会直接返回 `data_inspection_failed` 错误，无模型推理结果。
- **数据隐私承诺**：阿里云百炼**绝不会将您的输入数据用于模型训练**，所有传输数据默认使用 AES-256 加密；但根据协议，调用日志（含输入输出）将被存储用于审计与合规目的，详情见 [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)。
- **备案责任边界**：百炼提供所接入模型的算法备案号与主体信息，但应用/小程序开发者作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务，阿里云不替代开发者履行备案主体责任。

## 来源文档

- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)


