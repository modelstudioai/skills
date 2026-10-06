# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）封装为可调用的标准化组件，弥补大模型在实时信息获取、精确计算、代码执行、图像生成等场景下的固有局限。插件支持官方预置、三方集成与自定义开发三种形态，可被智能体应用、工作流应用及 Assistant API 统一调度。其设计目标是让开发者以最小集成成本获得可信赖的增强能力。

## 支持的模型/功能

百炼插件当前支持以下模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的支持程度存在差异，实际兼容性请以控制台运行结果为准，[选择模型](raw/model-user-guide/get-started-with-models/models.md) 文档提供了模型能力详情。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等。详细说明见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：覆盖商业服务、图像视频、学习教育等领域，经效果验证，开通后即可调用。
- **自定义插件**：支持开发者接入自有 API 或云市场 API，通过定义插件 URL、工具路径、输入/输出参数完成集成，完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在“常见问题”中补充说明“联网搜索（enable_search）也是基于夸克搜索”，且强调其“不会完全依赖或返回互联网搜索结果”。二者描述角度不同，但均指向同一底层能力；实际使用中，`quark_search` 插件返回结构化摘要，而 `enable_search` 是模型层开关，非独立插件，开发者应优先使用 `quark_search` 工具 ID 显式调用。

## 关键参数

插件调用的核心参数由工具定义决定，关键字段包括：
- **工具 ID（tool_id）**：唯一标识符，如 `calculator`、`code_interpreter`，API 调用时必须传入。获取方式见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 的“获取工具ID”章节。
- **输入参数（input parameters）**：需在创建自定义插件时明确定义，包括参数名、类型（String/Number/Object）、传参方式（`大模型识别` 或 `业务透传`）及是否必填。Object 类型子属性不能为空，否则发布失败（错误码 130022）。
- **鉴权配置**：自定义插件可选 Header 或 Query 方式传递 [Token](../concepts/token.md)，支持 `basic`/`bearer`/`appcode` 类型。RAM 用户需提前授予 `ram:CreateServiceLinkedRole` 权限方可完成 SLR 授权，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 的权限说明。

## 使用方式

插件可通过三种方式集成：
1. **控制台可视化集成**：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面，将工具添加至智能体应用（最多 10 个），或在工作流应用中作为节点编排；自定义插件需先发布为 MCP 服务再添加。
2. **API 集成**：通过 DashScope SDK 或 HTTP 接口调用应用时，将 `tool_id` 及必要参数（如 `biz_params` 用于透传参数或用户级鉴权 [Token](../concepts/token.md)）传入请求体。
3. **Assistant API**：在 Assistant API 请求中通过 `tools` 字段声明可用工具列表，并在 `messages` 中触发调用，具体语法参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。

所有方式均要求插件/工具状态为“已发布”且“已启用”，未发布的工具无法被调用。

## 限制和注意事项

- **权限限制**：主账号与 RAM 用户首次访问插件市场均需授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色。RAM 用户无创建 SLR 权限时，须由主账号授予 `ram:CreateServiceLinkedRole` 权限策略（含 `cloundapi-access.sfm.aliyuncs.com` 服务名条件），否则无法完成授权或导入云市场插件 —— 此流程在 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中均有详细说明。
- **功能限制**：`code_interpreter` 插件禁止网络访问与本地文件上传，仅支持指定依赖库；`quark_search` 和 `github_search` 均仅返回摘要信息，不支持深度页面抓取。
- **调试与发布**：自定义插件的工具必须通过在线调试并成功运行后才能发布；发布失败常见原因为参数描述缺失（错误码 130040）或 GET 请求误配 Object 类型入参（错误码 130022）。
- **业务空间隔离**：官方插件仅能与**同业务空间**内的智能体应用关联，跨空间调用需重新授权。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


