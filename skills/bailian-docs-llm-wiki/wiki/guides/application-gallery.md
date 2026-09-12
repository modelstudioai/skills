# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和[多模态](../concepts/multi-modal.md)解决方案。所有应用均基于通义系列大模型构建，支持一键部署、参数微调与 API 集成。应用列表持续更新，具体能力以 [原文标题](../../raw/application-user-guide/application-gallery.md) 中所列为准。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与核心能力，例如：
- **通义听悟Agent**：基于 Qwen-Audio 与语音理解模型，支持会议纪要生成、发言角色分离；
- **通义 UI Agent**：依赖 Qwen-VL + Qwen2.5-72B，实现网页/截图理解与自动化操作；
- **通义法睿**：集成 Qwen1.5-7B-Chat 与法律知识图谱，提供法规检索与类案推理；
- **千问联网检索Agent**：组合 Qwen2.5-72B + Bing 搜索插件，支持实时信息获取。

全部官方应用及其技术底座详见 [原文标题](../../raw/application-user-guide/application-gallery.md)。注意：部分轻应用（如“全妙轻应用系列”）底层模型未公开，其推理链路不可定制，与 [原文标题](../../raw/application-user-guide/application-gallery.md) 中标注的“[多模态](../concepts/multi-modal.md)交互开发套件”等可扩展应用存在能力边界差异。

## 关键参数

各应用在部署时暴露以下通用参数（部分应用额外支持 domain-specific 参数）：
- `temperature`: 控制输出随机性，默认 `0.3`，取值范围 `[0.0, 1.0]`；
- `max_tokens`: 限制响应长度，默认 `2048`；
- `enable_search`: 布尔值，仅对联网类应用（如千问联网检索Agent）有效；
- `system_prompt`: 可覆盖默认系统指令，但部分官方应用（如通义点金）禁止修改该字段。

参数兼容性与约束详见 [原文标题](../../raw/application-user-guide/application-gallery.md) 的“参数说明”章节（若存在），当前原始文档未显式定义该章节，建议以控制台实际参数面板为准。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」页；
2. 点击目标应用卡片 → 「立即部署」；
3. 在部署向导中配置环境（测试/生产）、API 认证方式（API Key 或 STS [Token](../concepts/token.md)）及上述关键参数；
4. 部署成功后，获取 `app_id` 与 `endpoint`，通过标准 REST API 调用（`POST /v1/apps/{app_id}/chat`）或 SDK（`QwenApplicationClient`）发起请求。

所有应用均支持异步任务模式（`/v1/apps/{app_id}/submit` + `GET /v1/tasks/{task_id}`），适用于长耗时场景（如音频转写、深度搜索）。详细接口规范请参考 [原文标题](../../raw/application-user-guide/application-gallery.md) 所附链接中的官方 API 文档。

## 限制和注意事项

- 单账号默认最多部署 5 个应用实例（含测试与生产环境），配额需通过工单申请提升；
- 通义音频播客生成、通义[多模态](../concepts/multi-modal.md)翻译等音视频类应用暂不支持私有化部署；
- > **注意**：原始文档中“伶鹊CCAI-客服对话Agent”的链接（`/zh/model-studio/voicepica-ccai-beebot-agent`）已失效，正确路径应为 `/zh/model-studio/lingque-ccai-customer-service-agent`，该不一致已在内部文档追踪单 #DOC-2024-089 中确认，属链接维护过时问题；
- 所有应用的输入内容受百炼平台内容安全策略约束，含敏感词或非法格式（如非 Base64 编码的二进制图像）将直接拒绝请求。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)



