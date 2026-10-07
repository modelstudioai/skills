# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的 AI 能力封装，覆盖教育、语音处理、多模态交互、法律、金融、客服、数据挖掘、翻译、搜索等多个垂直场景。所有应用均基于百炼统一模型服务框架构建，支持快速集成与二次开发。开发者可通过控制台或 API 直接调用，无需自行部署底层模型。

## 支持的模型/功能

应用广场中的每个应用均绑定特定模型栈与能力组合，例如：
- `通义拍照解题辅导` 基于 Qwen-VL 多模态模型 + 教育领域微调策略，支持图像识别与数学推理；
- `通义听悟Agent` 依赖 Qwen-Audio 模型 + ASR/NLU 流式 pipeline；
- `千问联网检索Agent` 集成 Qwen2.5 + RAG 检索增强模块与实时网页抓取适配器。

全部官方应用列表及对应能力说明详见 [应用广场](../../raw/application-user-guide/application-gallery.md)。部分轻量级应用（如 `全妙轻应用系列`）默认使用共享推理资源池，其底层模型版本由平台统一维护，具体模型映射关系请参考 [官方应用-全妙轻应用系列](../../raw/application-user-guide/application-gallery/quanmiao-light-application-series.md)。

## 关键参数

调用应用时需传入以下通用参数（部分应用支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用广场」页获取，例如 `edu-tutor` 或 `tingwu-agent` |
| `input` | object | 是 | 输入结构体，格式因应用而异（如 `tongyi-dianjin` 要求 `{"query": "...", "industry": "finance"}`） |
| `timeout` | integer | 否 | 请求超时（秒），默认 60，最大支持 300；超过将触发 `RequestTimeoutError` |

> **注意**：`web-search-agent` 的 `input` 中 `query` 字段长度上限为 512 字符，但 [通义深度搜索](../../raw/application-user-guide/application-gallery/tongyi-deepsearch.md) 文档中声明为 1024 字符——实际以 `web-search-agent` 当前运行时限制为准，建议客户端做截断校验。

## 使用方式

1. **控制台调用**：进入百炼控制台 →「应用广场」→ 选择目标应用 → 点击「在线调试」填写 input 并执行；
2. **API 调用**：使用 `POST /v1/applications/{app_id}/invoke` 接口，需携带 `Authorization: Bearer <api_key>`；
3. **SDK 调用**（Python 示例）：
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = BailianClient(...)
   req = bailian_models.InvokeApplicationRequest(
       app_id="tingwu-agent",
       input={"audio_url": "https://example.com/audio.mp3"}
   )
   resp = client.invoke_application(req)
   ```

详细接口定义与错误码见 [官方应用-通义听悟Agent](../../raw/application-user-guide/application-gallery/official-application-tingwu-agent.md)。

## 限制和注意事项

- 单账号默认 QPS 上限为 5（可提工单申请提升），突发流量可能触发 `RateLimitExceeded` 错误；
- 所有应用不支持跨区域调用（如杭州集群部署的应用不可通过上海 endpoint 访问）；
- `ui-agent` 和 `multimodal-products` 类应用暂不开放自定义 [prompt](prompt.md) 覆盖，输入必须严格遵循 schema 定义；
- 非官方应用（如用户自主发布的应用）不在本广场范围内，其管理与调用方式参见独立文档。

> **注意**：`xiyan-gbi`（析言GBI）当前仅支持结构化数据库连接（MySQL/PostgreSQL），但 [官方应用-析言GBI](../../raw/application-user-guide/application-gallery/xiyan-gbi.md) 中提及的“Excel 文件直连”功能尚未上线，该描述已过时，请勿依赖。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


