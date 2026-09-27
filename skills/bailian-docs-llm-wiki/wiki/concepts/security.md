# 内容安全与合规

内容安全与合规是百炼平台面向生成式AI应用提供的核心横切能力，指对用户输入、模型输出、知识库内容、记忆数据等全链路文本/图像内容进行实时风险识别（如涉黄、暴恐、政治敏感、违法违禁等），并确保整体技术栈满足《生成式人工智能服务管理暂行办法》等监管要求的综合防护机制。该能力默认启用、深度集成，覆盖开发、运行、数据与交付各阶段，无需额外编码即可获得基础防护，同时支持按需增强审计与策略管控。

## 在百炼平台的不同场景中，这个概念如何使用

内容安全与合规能力在百炼平台中以“分层嵌入、按需激活”方式落地，贯穿以下关键场景：

- **Flow Agent 与 Managed Agent**：自动对用户输入（Prompt）和模型输出（Response）执行双路内容安全检测；Managed Agent 还在工具调用前拦截高风险指令（如含恶意 payload 的 Shell 命令），保障运行时行为安全。  
- **RAG 知识库**：上传文件时自动预扫描（PDF/DOCX 等格式 OCR+文本分析），入库后持续检测知识片段风险；检索阶段同步校验召回内容安全性，防止投毒数据污染响应。  
- **Memory 模块**：对记忆的读写操作进行内容安全过滤，避免敏感信息被意外存储或泄露，保障对话上下文安全。  
- **模型调用 API 层**：通过 `X-DashScope-DataInspection` 请求头显式启用 AI 安全护栏，实现输入/输出双通道实时风控，适用于自建前端、SDK 或直连 HTTP 调用。  
- **安全存储业务空间**：在高敏专属环境中，内容安全检测与私网隔离、传输加密协同工作，确保数据“不出域、不裸传、不越界”。

> ⚠️ 注意：默认防护自动生效，但高级策略（如自定义关键词库、细粒度风险等级处置）需在控制台 **Security > 高级防护 > 安全策略** 中手动开启；当前高级防护仅提供监测与告警，**不支持自动阻断**，风险事件需人工确认处理。

## 关键参数和配置

| 参数/配置项 | 类型 | 说明 | 使用位置 |
|-------------|------|------|----------|
| `X-DashScope-DataInspection` | HTTP Header（string） | 启用 AI 安全护栏的开关，值为 `{"input":"cip","output":"cip"}`（字符串格式，非 JSON 对象） | HTTP API 调用、DashScope SDK（低层封装） |
| `scene` | string（可选） | 检测场景标识，影响策略权重，如 `"chat"`（对话）、`"search"`（搜索）、`"generation"`（生成），默认 `"general"` | Security API `/v1/security/text` 或 `/v1/security/image` |
| `enable_ocr` | boolean（可选） | 图像检测时是否启用 OCR 文本识别，默认 `false`；启用后延迟增加约 300ms | Security API 图像检测请求体 |
| `risk_level` | integer（响应字段） | 检测结果风险等级：`0`=安全，`1`=低危，`2`=中危，`3`=高危（**非字符串枚举**） | 所有 Security API 同步/异步响应体 |
| `content` / `image_url` | string | 待检测文本（≤65536 字符）或图片公网 HTTPS URL（≤10MB，支持防盗链白名单） | Security API 必填参数 |
| 高级防护策略开关 | 控制台配置 | 包括“内容安全”、“RAG 投毒识别”、“记忆内容检测”等独立开关，默认关闭，需手动开启 | 控制台 **Security > 高级防护 > 安全策略** |

## 面向开发者，简洁实用

- ✅ **快速启用**：HTTP 调用时加一行 Header 即可启用双路风控：  
  ```http
  X-DashScope-DataInspection: {"input":"cip","output":"cip"}
  ```
- ✅ **SDK 更省心**：Python 使用 `dashscope.Generation.call(..., extra_headers={"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'})`；Java 同理，无需改业务逻辑。  
- ✅ **批量/大图用异步**：对多图或高并发场景，优先调用 `/v1/security/async/submit` 提交任务，再轮询 `/v1/security/async/result` 获取结果（超时 30 分钟）。  
- ✅ **调试看日志**：开启推理日志（需先授权 SLS 投递）后，可在日志中查看原始 `input`/`output` 及对应 `risk_level`，精准复现风控决策依据。  
- ⚠️ **避坑提醒**：  
  - `risk_level` 是整数，不是 `"high"` 字符串；  
  - 图像检测需确保 `image_url` 公网可访问且在白名单内；  
  - 高级防护不拦截，仅告警——高风险响应仍会返回，务必在业务侧做 `if response.risk_level > 2: reject()` 判断；  
  - 所有检测结果仅保留 7 天，关键审计需自行落库。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application support](../guides/application-support.md)
- [model monitoring](../guides/model-monitoring.md)


