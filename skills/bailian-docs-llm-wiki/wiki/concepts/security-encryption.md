# 传输加密与安全合规

传输加密与安全合规是百炼平台保障数据在传输过程中机密性、完整性及监管合规性的核心横切能力，通过端到端加密、私网隔离、请求级安全控制等机制，在模型调用全链路中满足《生成式人工智能服务管理暂行办法》等国内法规要求。

## 在百炼平台的不同场景中，这个概念如何使用

该概念贯穿模型推理、API 调用与业务空间治理三大关键场景，具体体现为：

- **模型推理调用（文本类模型）**：对 `input` 字段实施 AES-256 对称加密 + RSA 公钥封装密钥的混合加密。适用于 `qwen-plus`、`qwen-flash` 等所有文本生成模型，确保敏感提示词（如用户身份信息、企业内部指令）在公网传输中不被明文截获。SDK 自动完成密钥协商与加解密，HTTP 手动调用需显式获取公钥并实现加密逻辑。

- **API 网络通道加固**：支持两种隔离模式：
  - **私网访问（PrivateLink）**：通过阿里云内网直连模型 API，适用于华北2（北京）、中国香港等地域，避免公网暴露；需在控制台配置终端节点，并将 SDK 的 `base_url` 替换为私网域名（格式：`{WorkspaceId}-{VpcId}.{RegionId}.maas.aliyuncs.com`）。
  - **IP 白名单（仅美国弗吉尼亚地域）**：通过请求头 `X-DashScope-IP-Whitelist` 限制调用来源 IP，配合 API Key 实现双因子网络准入。

- **内容安全协同防护**：传输加密与 AI 安全护栏联动——即使输入已加密，系统仍可在服务端解密后执行内容检测（涉政、涉黄、广告等）。需显式设置请求头 `X-DashScope-DataInspection: '{"input":"cip","output":"cip"}'` 启用双路检测，确保合规输出。

> ⚠️ 注意：传输加密仅保护 `input` 字段（含 `messages` 中的 `content`），`model`、`temperature` 等元参数仍以明文传输；`output` 默认不加密，如需端到端加密，请在客户端自行实现响应解密。

## 关键参数和配置

| 参数 | 说明 | 开启方式 | 备注 |
|------|------|----------|------|
| `enable_encryption` / `enableEncrypt` | SDK 级开关，启用自动混合加密 | Python：`dashscope.Generation.call(..., enable_encryption=True)`<br>Java：`.enableEncrypt(true)` | 推荐首选方式，SDK 自动管理公钥获取、AES 密钥生成与加解密 |
| `X-DashScope-EncryptionKey` | HTTP 手动调用时，携带 RSA 加密后的 AES 密钥 | Base64 编码字符串，需先调用 `/api/v1/public-keys/latest` 获取公钥 | 仅用于自研加密逻辑，不推荐生产环境手动实现 |
| `X-DashScope-DataInspection` | 启用输入/输出内容安全检测 | 请求头值为 JSON 字符串：`'{"input":"cip","output":"cip"}'` | 必须为字符串格式（非 JSON 对象），且需提前在控制台开通并授权 AI 安全护栏服务 |
| `X-DashScope-IP-Whitelist` | 限定 API Key 可调用的 IPv4 源地址段 | 仅支持美国弗吉尼亚地域，值如 `"192.168.1.0/24,203.0.113.5"` | 需在「API 密钥管理」页面配置，生效后立即拦截非白名单请求 |

## 面向开发者，简洁实用

- ✅ **快速启用传输加密（推荐）**：  
  ```python
  import dashscope
  dashscope.api_key = "YOUR_API_KEY"
  response = dashscope.Generation.call(
      model="qwen3.7-plus",
      input={"messages": [{"role": "user", "content": "请分析这份财报摘要"}]},
      enable_encryption=True  # ← 一行开启，无需改业务逻辑
  )
  ```

- ✅ **验证是否生效**：检查响应中的 `usage.encryption_enabled: true` 字段；或抓包确认 `input` 字段为 Base64 编码的密文（非明文）。

- ✅ **私网访问三步走**：  
  1. 控制台 → 管理 > 网络配置 → 添加 PrivateLink 终端节点；  
  2. 业务空间管理 → 关联该终端节点；  
  3. SDK 初始化时设置 `base_url = "https://{WorkspaceId}-{VpcId}.cn-beijing.maas.aliyuncs.com/api/v1"`。

- ❌ **避坑提醒**：  
  - 不要混用“私网访问”（文档5）与“安全存储空间私网接入”（文档6）——二者技术栈与适用场景完全不同；  
  - `X-DashScope-DataInspection` 值必须是字符串，写成 `{"input":"cip"}` 会因 JSON 解析失败导致护栏不生效；  
  - 加密仅作用于 `input`，若需保护 `system` 角色提示词，请将其放入 `messages[0].content` 并确保 `enable_encryption=True`。

## 关联主题页

- [security and compliance](../guides/security-and-compliance.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)


