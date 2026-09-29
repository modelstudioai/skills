# security and compliance

阿里云百炼平台提供端到端的安全与合规能力，覆盖传输加密、私网隔离、内容安全、权限管控、模型备案及数据隐私保护等关键维度。所有能力均面向企业级生产环境设计，支持开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控地集成大模型能力。

## 支持的模型/功能

- **传输加密**：支持对 `input` 字段进行 AES-256 对称加密，密钥通过 RSA 公钥安全分发，适用于敏感数据场景。该能力对所有支持文本输入的模型（如 `qwen-plus`、`qwen-flash`）通用，[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md) 文档详细说明了混合加密流程。
- **私网访问**：支持通过 PrivateLink 实现 VPC 内流量全程走阿里云内网，避免公网暴露。当前仅华北2（北京）、中国香港地域支持，且需在百炼控制台完成网络配置与业务空间关联，详见 [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)。
- **AI 安全护栏**：支持在请求头中启用 `X-DashScope-DataInspection`，对输入输出内容进行涉黄、涉政、广告等高风险内容识别。该能力与模型自动绑定，目前覆盖文本和图片类模型，具体支持范围见 [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)。
- **安全存储空间**：面向高敏感数据场景提供独立部署的“安全存储空间”，支持通过反向终端节点、MSE 网关、OSS/ADB/ES 等私有资源构建全链路私网闭环，相关配置指南见 [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)。

## 关键参数

| 参数名 | 位置 | 类型 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `enable_encryption` / `enableEncrypt` | SDK 调用参数 | Boolean | 启用传输加密开关，SDK 自动处理 AES 密钥生成、RSA 加密及加解密全流程 | `True` (Python), `true` (Java) |
| `X-DashScope-DataInspection` | HTTP Header | JSON string | 启用 AI 安全护栏，指定 input/output 检查策略 | `'{"input":"cip","output":"cip"}'` |
| `X-DashScope-EncryptionKey` | HTTP Header | Base64 string | （手动调用时）封装加密后的 AES 密钥 | `"AQABAAE..."` |
| `public_key_id` & `public_key` | `/api/v1/public-keys/latest` 响应体 | String | RSA 公钥元信息，用于手动加密场景 | `"1"`, `"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnojrB579xgPQN5f46SvoRAiQBPWBaPzWh7hp51fWI+OsQk7KqH0qMcw8i0eK5rfOvJIPujOQgnes1ph9/gKAst9NzXVIl9JJYUSPtzTvOabhp4yvS3KBf9g3xHYVjYgW33SOY74Ue/tgbCXn717rV6gXb4sVvq9XK/1BrDcGbEOQEZEgBTFkm/g3lpWLQtACwwqHffoA9eQtkkz15ZFKosAgbR8LedfIvxAl2zk15REzxXiRcFgc9/tLF0U1t2Sxt9FkQefxYwn6EZawTsRJvf4kqF3MaPdTcDbOp0iSNvCl2qzPSf/F+Oll2CUM1tFAEu81oa4l0WaDR3UtvqOtyQIDAQAB"` |
| `X-DashScope-Client-IP` | HTTP Header | String | （可选）用于 IP 白名单校验，需与 API Key 绑定的白名单一致 | `"203.205.128.0/20"` |

> **注意**：文档 6 (`raw/model-user-guide/security-and-compliance/secure-storage.md`) 将“私网访问配置”作为一级标题，但其内容实际是安全存储空间的子流程（即反向终端节点配置），与文档 5 中的正向 PrivateLink（VPC → 百炼）属不同架构。二者不可混用：文档 5 适用于标准业务空间的私网调用；文档 6 及其子文档（7–10）专用于“安全存储空间”这一特殊空间类型，需商务开通。开发者应根据业务空间类型选择对应路径。

## 使用方式

1. **传输加密（推荐 SDK 方式）**  
   - 安装最新 DashScope SDK（Java ≥ 2.12.0，Python ≥ 1.14.0）  
   - 在 `Generation.call()` 或 `GenerationParam.builder()` 中设置 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）  
   - SDK 自动调用 `/api/v1/public-keys/latest` 获取公钥、生成 AES 密钥、加密 `input` 并注入 `X-DashScope-EncryptionKey` 头  

2. **私网访问（PrivateLink）**  
   - 在百炼控制台 **管理 > 网络配置** 开通 PrivateLink 服务并添加 VPC 连接  
   - 在 **业务空间管理** 中将目标业务空间与私网连接关联  
   - 替换 API 调用域名：将 `{WorkspaceId}.{RegionId}.maas.aliyuncs.com` 替换为 `{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`  

3. **AI 安全护栏**  
   - 开通服务并授权（需主账号在 [安全管理](https://bailian.console.aliyun.com/settings/security?globalset=1) 页面操作）  
   - 在请求头中添加 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'`  
   - 触发违规时返回 `400` 状态码及 `data_inspection_failed` 错误码  

4. **安全存储空间（需商务开通）**  
   - 创建“安全存储空间”类型业务空间  
   - 依次完成：配置反向终端节点 → 配置 MSE 网关与可用区 VIP → 授权 OSS/ADB/ES → 激活空间  
   - 全程使用内网地址，不暴露公网入口  

## 限制和注意事项

- **地域限制**：PrivateLink 私网访问仅支持华北2（北京）、中国香港；安全存储空间当前仅支持华北2（北京）地域，且专有网络必须包含可用区 G/H/L 中的至少两个。
- **权限边界**：API Key 的模型调用权限完全继承自其归属的**业务空间**，与用户（RAM 账号）的控制台页面权限无关；超级管理员可跨空间管理，但业务空间管理员无法管理其他空间的模型限流或部署权限（参见 [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)）。
- **加密约束**：DashScope SDK 的自动加密仅支持 Java 和 Python；HTTP 手动调用需自行实现 AES/RSA 加解密逻辑，且不支持自定义密钥。
- **数据留存**：百炼默认存储模型与应用调用日志（含输入输出），用于审计与问题排查；若需禁用，请联系商务确认是否符合安全存储空间部署条件。
- **备案责任**：阿里云提供所接入模型的算法备案号与大模型备案号（见 [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)），但应用/小程序上架的最终合规责任主体为开发者自身，需独立完成安全评估、算法备案及合作协议签署。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


