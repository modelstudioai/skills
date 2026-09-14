# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和多模态解决方案。所有应用均基于通义系列大模型构建，支持一键部署、参数微调与 API 集成。应用列表持续更新，具体能力以 [原文标题](../../raw/application-user-guide/application-gallery.md) 中所列为准。

## 支持的模型与功能

应用广场中的每个应用均绑定特定模型栈与核心能力，例如：
- **通义听悟Agent**：基于 Qwen-Audio 与语音理解模型，支持会议纪要生成、发言角色分离；
- **通义 UI Agent**：依赖 Qwen-VL + Qwen2.5-72B，实现网页/截图理解与自动化操作；
- **通义法睿**：集成 Qwen1.5-7B-Chat 与法律知识图谱，提供法规检索与类案推理；
- **千问联网检索Agent**：组合 Qwen2.5-72B + Bing 搜索插件，支持实时信息获取。

全部官方应用及其技术底座详见 [原文标题](../../raw/application-user-guide/application-gallery.md)。注意：部分轻应用（如“全妙轻应用系列”）底层模型未公开，其推理链路不可定制，与 [原文标题](../../raw/application-user-guide/application-gallery.md) 中标注的“多模态交互开发套件”等可扩展应用存在能力边界差异。

## 关键参数

各应用在部署时暴露以下通用参数（部分应用额外支持 domain-specific 参数）：
- `temperature`: 控制输出随机性，默认 `0.3`，取值范围 `[0.0, 1.0]`；
- `max_tokens`: 限制响应长度，默认 `2048`；
- `enable_search`: 布尔值，仅对联网类应用（如千问联网检索Agent）生效；
- `system_prompt`: 可覆盖默认系统指令，需符合平台 [prompt](prompt.md) 安全策略。

参数说明与约束详见 [原文标题](../../raw/application-user-guide/application-gallery.md) 中各应用链接跳转后的技术文档页。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」页；
2. 点击目标应用卡片 → 「立即部署」；
3. 在部署页配置参数（见上节），选择计算资源规格；
4. 部署成功后获取 API Endpoint 与 `Authorization` [Token](../concepts/token.md)；
5. 调用示例（cURL）：
   ```bash
   curl -X POST "$ENDPOINT" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"input": {"query": "如何查询合同违约责任？"}, "parameters": {"temperature": 0.1}}'
   ```

## 限制和注意事项

- 所有应用默认启用内容安全过滤，拒绝含违法、暴力、隐私信息的输入；
- 免费试用额度仅限首次部署的前 7 天，超限后需绑定计费项；
- **注意**：`通义音频播客生成` 当前仅支持中文输入与 MP3 输出，不支持批量生成或多语种混排——该限制未在 [原文标题](../../raw/application-user-guide/application-gallery.md) 中明确说明，需以控制台实际部署页提示为准；
- 应用间不共享上下文，若需跨应用状态管理，须由开发者自行实现 session 层；
- 非官方应用（用户自建并发布至广场）不受平台 SLA 保障，其模型版本与接口稳定性由发布者负责。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


