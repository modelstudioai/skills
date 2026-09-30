# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业场景解决方案和能力组件。所有应用均基于百炼模型服务构建，支持直接调用、二次开发或嵌入自有系统。应用按功能类型分类管理，部分应用需开通对应模型权限后方可使用。

## 支持的模型与功能

应用广场中的应用底层依赖不同模型能力，例如：
- 通义法睿、通义点金、析言GBI 等金融/法律类应用主要调用 `qwen-max` 或 `qwen-plus`；
- 多模态交互开发套件、通义多模态翻译 依赖 `qwen-vl` 和 `qwen-audio`；
- 通义 UI Agent、千问联网检索Agent 等工具增强型应用需启用 `qwen-turbo` 或 `qwen-max` 并配置插件权限。

具体模型绑定关系详见 [应用广场](../../raw/application-user-guide/application-gallery.md) 中各子应用链接所指向的文档，如 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md) 明确要求 `qwen-audio` + `qwen-turbo` 双模型协同。

> **注意**：[官方应用-伶鹊CCAI-客服对话Agent](../../raw/application-user-guide/application-gallery/official-application-voicepica-ccai-beebot-agent.md) 文档中声明支持 `qwen-plus`，但最新控制台实际部署时仅允许选择 `qwen-max` —— 请以控制台可选模型为准，该文档已过时。

## 关键参数

调用应用广场应用时，通用关键参数包括：
- `app_id`：应用唯一标识（在控制台「应用广场」页点击应用后 URL 中的 `id` 参数）；
- `input`：结构化输入对象，字段依应用而异（如 `text`、`image_url`、`audio_url`、`query` 等），详见各应用文档；
- `stream`：布尔值，控制是否启用流式响应（默认 `false`）；
- `timeout`：请求超时时间（单位秒），建议设为 `60` 以上，尤其对深度搜索、UI Agent 等长耗时应用。

参数格式与校验规则严格遵循 [应用广场](../../raw/application-user-guide/application-gallery.md) 所列各子应用的接口定义，例如 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 要求 `input` 必须包含 `query` 和 `max_results` 字段。

## 使用方式

1. **控制台接入**：登录百炼控制台 → 进入「应用广场」→ 选择目标应用 → 点击「立即使用」获取 `app_id` 和调试界面；
2. **API 调用**：使用 `POST /v1/applications/{app_id}/chat` 接口，携带认证 Header（`Authorization: Bearer <api_key>`）及上述参数；
3. **SDK 集成**：Python SDK 示例：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client(...)

   response = client.chat_app(
       app_id="app-xxx",
       input={"query": "2024年Q3 AI芯片出货量"},
       stream=False
   )
   ```

完整调用流程与错误码说明见 [应用广场](../../raw/application-user-guide/application-gallery.md) 主文档及各子应用页。

## 限制和注意事项

- 单应用并发调用数默认上限为 5，可通过工单申请提升；
- 音频/视频类应用（如通义听悟Agent、通义音频播客生成）对输入文件大小、格式、时长有严格限制（如 MP3 ≤ 100MB，时长 ≤ 2 小时），详见对应子文档；
- 所有应用均不支持跨区域调用（例如华东1区创建的应用不可通过华北2区 endpoint 访问）；
- 应用广场中的「官方应用-全妙轻应用系列」目前仅限阿里云内部客户白名单使用，外部开发者暂不可见 —— 此限制未在 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md) 中明确说明，属平台运行时策略。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


