# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业场景解决方案和能力组件。所有应用均基于百炼模型服务构建，支持直接调用、二次开发或嵌入自有系统。应用按功能类型分类管理，部分应用需开通对应模型权限后方可使用。

## 支持的模型与功能

应用广场中的应用底层依赖不同模型能力，例如：
- 通义法睿、通义点金、析言GBI 等金融/法律类应用主要调用 `qwen-max` 或 `qwen-plus`；
- 多模态交互开发套件、通义多模态翻译 依赖 `qwen-vl` 和 `qwen-audio`；
- 通义 UI Agent、千问联网检索Agent 等需启用 `qwen-websearch` 插件能力。

具体模型绑定关系详见 [应用广场](../../raw/application-user-guide/application-gallery.md) 文档中各子应用链接所指向的说明页，例如 [官方应用-通义拍照解题辅导](../../raw/application-user-guide/application-gallery/edu-tutor.md) 明确要求 `qwen-vl` + `qwen-plus` 双模型协同。

> **注意**：部分旧版文档（如 [官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md)）仍标注依赖 `qwen-1.8b`，但该模型已下线；实际运行需替换为 `qwen-turbo` 或 `qwen-plus`，请以控制台实际可用模型为准。

## 关键参数

调用应用广场应用时，通用参数包括：
- `app_id`：应用唯一标识（在控制台「应用广场」页面点击应用后 URL 中的 `id` 字段）；
- `input`：结构化输入对象，字段因应用而异（如 `image_url` 用于拍照解题，`audio_url` 用于听悟Agent）；
- `stream`：布尔值，控制是否启用流式响应（默认 `false`）；
- `timeout`：最大执行时长（单位秒），多数应用默认 60s，深度搜索类应用建议设为 120s。

参数详情以各应用独立文档为准，例如 [官方应用-通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 要求必传 `query` 和可选 `filters`，而 [通义 UI Agent](../../raw/application-user-guide/application-gallery/ui-agent.md) 则需传入 `screenshot_base64` 和 `instruction`。

## 使用方式

1. 登录百炼控制台 → 进入「应用广场」；
2. 浏览或搜索目标应用 → 点击「立即体验」或「接入应用」；
3. 若为公开应用，可直接调用 API（需配置 API Key）；若为需授权的应用（如全妙系列），需先提交申请并等待审核；
4. 调用示例（Python）：
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   response = dashscope.Generation.call(
       app_id="abc123",
       input={"query": "2024年Q2中国新能源汽车销量"},
       stream=False
   )
   ```

## 限制和注意事项

- 单账号默认并发调用上限为 5 路，高并发需求需提工单申请扩容；
- 音视频类应用（如通义听悟Agent、通义音频播客生成）对文件大小和格式有严格限制（如 MP3 ≤ 100MB，WAV 采样率需为 16kHz）；
- 所有应用均不支持跨区域调用（例如华东1区创建的应用仅可在华东1区调用）；
- 应用广场中部分轻应用（如 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md)）为 SaaS 化部署，不开放源码及模型微调能力；
- 自定义应用不可发布至应用广场，该入口仅面向阿里云官方认证应用。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


