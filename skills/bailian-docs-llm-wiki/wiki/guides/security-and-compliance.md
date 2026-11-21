# security and compliance

阿里云百炼平台提供覆盖模型调用、数据传输、权限管理、内容安全与合规备案的全栈安全与合规能力，面向企业级开发者设计。所有功能均基于最小权限原则与纵深防御理念构建，核心能力包括细粒度权限控制、端到端加密传输、[AI 安全护栏](../concepts/security-guardrails.md)、私网隔离访问及完整的算法与大模型备案支持。开发者需结合自身业务场景，主动配置并验证各项安全策略。

## 支持的模型/功能

- **[AI 安全护栏](../concepts/security-guardrails.md)**：仅在华北2（北京）地域可用，支持文本与图片类模型的输入/输出内容检测（涉黄、涉政、广告等），需显式设置请求头 `X-DashScope-DataInspection` 或通过[业务空间维度开关](raw/model-user-guide/security-and-compliance/content-security.md)全局启用。
- **加密传输**：支持 AES-RSA 混合加密，对 `input` 字段进行端到端加密，防止公网传输中敏感数据泄露；该能力由 DashScope SDK 自动封装（Java/Python），或通过 HTTP 手动调用 [获取RSA的公钥](raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md) 接口实现。
- **私网访问**：支持 PrivateLink 私网连接（标准 VPC 场景）与反向终端节点（安全存储业务空间专用），流量全程走阿里云内网，不经过公网；其中标准私网连接适用于通用模型/API 调用，而反向终端节点仅面向已开通的[安全存储业务空间](raw/model-user-guide/security-and-compliance/secure-storage.md)用户。
- **模型备案信息**：所有接入百炼的模型均完成国家网信办算法备案与大模型备案，备案号及主体信息在[模型备案信息公示](raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)中完整公开，可用于应用上架合规材料准备。

> **注意**：文档 9–12 描述的“安全存储业务空间”反向终端节点方案与文档 7 描述的通用 PrivateLink 方案存在定位差异——前者是为满足高等级数据不出域要求的定制化部署（需商务开通），后者是面向所有用户的标准化私网接入能力。二者不可混用，开发者应根据业务安全等级选择对应路径。

## 关键参数

- `X-DashScope-DataInspection`：启用 [AI 安全护栏](../concepts/security-guardrails.md)的必需请求头，值为 JSON 字符串，如 `{"input":"cip","output":"cip"}`，表示同时开启输入与输出检测。
- `X-DashScope-EncryptionKey`：加密调用时用于传递 RSA 加密后的 AES 密钥的请求头，由 DashScope SDK 自动填充，手动调用时需自行构造。
- `expire_in_seconds`：生成临时 API Key 时指定有效期（1–1800 秒），默认 60 秒，超时自动失效且不可提前删除。
- `public_key_id`：从 `/api/v1/public-keys/latest` 接口返回的公钥标识，用于确保客户端使用与服务端解密一致的密钥对。

## 使用方式

- **权限控制**：通过超级管理员（主账号或拥有 `AliyunBailianFullAccess` 策略的 RAM 用户）在[全局管理菜单](raw/model-user-guide/security-and-compliance/permission-management-overview.md)中新建业务空间、分配模型调用/训练/部署权限，并为各业务空间配置独立 API Key；普通用户仅能访问被授权的业务空间及页面。
- **API Key 安全实践**：生产环境必须使用一业务一 Key 原则，配合 IP 白名单（最多 20 个）、模型范围限制（最多 30 个）、预算告警与达预算即停；客户端场景强制使用后端签发的临时 API Key（`st-` 前缀），禁止前端直连长期 Key。
- **加密调用**：启用 DashScope SDK 的 `enable_encryption=True`（Python）或 `.enableEncrypt(true)`（Java）即可自动完成加解密；若需自定义密钥或使用其他语言，须先调用 `/api/v1/public-keys/latest` 获取公钥，再手动执行 AES+RSA 加密流程。
- **私网调用**：标准场景下，在百炼控制台「网络配置」中添加 PrivateLink，关联目标业务空间后，将 API 请求的 `base_url` 替换为生成的私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）；安全存储业务空间用户则需按[配置终端节点并发起连接](raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)流程完成反向终端节点创建与绑定。

## 限制和注意事项

- **地域限制**：AI 安全护栏仅北京地域可用；私网连接支持地域以控制台下拉列表为准（含北京、上海、杭州、深圳等），但安全存储业务空间反向终端节点目前仅支持“华北2（北京）”。
- **API Key 生命周期**：2026 年 3 月 25 日起创建的 API Key 不会因归属 RAM 用户被删除而级联失效，必须单独重置或删除 Key；旧版 Key 可能仍支持列表中直接复制明文，新版仅创建时显示一次。
- **日志追溯能力**：审计日志默认开启、保留 30 天，但**不包含输入输出内容**；推理日志需手动开启并投递至 SLS，且仅对未来调用生效，历史调用无法补录。
- **合规责任边界**：阿里云提供模型备案号、合作协议模板及基础安全能力，但应用/小程序作为《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户标识、安全评估等全部法定义务；备案信息应以[互联网信息服务算法备案系统](https://beian.cac.gov.cn/#/index)实时查询结果为准。
- **加密与私网非互斥**：加密传输保护载荷内容，私网连接保护网络路径，二者可叠加使用；但加密调用不改变请求路由，仍需通过公网或私网域名发起。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [API Key 防泄漏最佳实践](../../raw/model-user-guide/security-and-compliance/api-key-leak-prevention.md)
- [API Key 泄漏排查](../../raw/model-user-guide/security-and-compliance/api-key-leak-investigation.md)
- [传输安全](../../raw/model-user-guide/security-and-compliance/transmission-security.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [私网访问配置](../../raw/model-user-guide/security-and-compliance/secure-storage.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [输入输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [模型备案信息公示](../../raw/model-user-guide/security-and-compliance/model-filing-information-publicity.md)
- [千问大模型应用上架及合规备案](../../raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)


