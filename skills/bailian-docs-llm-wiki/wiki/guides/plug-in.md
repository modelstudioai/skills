# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）集成到大模型工作流中，可有效弥补模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场及完全自定义三种形态，适用于智能体应用、工作流应用和 Assistant API 三种调用路径。开发者需关注模型兼容性、权限配置与参数定义准确性。

## 支持的模型/功能

当前插件能力仅在以下模型上可用：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的调用稳定性与响应格式可能存在差异，**实际兼容性请以控制台运行结果为准**，而非文档静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置输入/输出参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 搜索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云市场，覆盖商业服务、教育、音视频等领域，需开通后使用。
- **自定义插件**：开发者可基于自有 API 创建，支持完整鉴权（Header/Query、Basic/Bearer/AppCode）、多工具路径、JSON Schema 级参数定义与在线调试 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在“常见问题”中补充说明“联网搜索（enable_search）也是基于夸克搜索”，但未明确二者是否为同一能力。实践中，`quark_search` 是独立插件工具，`enable_search` 是模型级开关，二者调用路径与返回结构不同，不可混用。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，调用时必须传入。可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数（input parameters）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户 query 提取）或 `业务透传`（由外部传入，如 `biz_params`）；
  - `类型` 需严格匹配（Number/String/Object），Object 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
  - `参数描述` 必须清晰，直接影响大模型参数提取准确率，缺失将导致错误码 `130040`。
- **鉴权配置**（仅自定义插件）：
  - 支持 Header 或 Query 位置；
  - `Type` 为 `bearer` 时，实际请求头为 `Authorization: Bearer <TOKEN>`；
  - 用户级鉴权需在对话前通过控制台配置 [Token](../concepts/token.md)，或通过 API 的 `biz_params` 透传。

## 使用方式

插件可通过三种方式接入：
1. **智能体应用（Agent 1.0）**：在插件市场选择工具 → “添加至智能体” → 关联目标应用（**注意：官方插件仅支持与同业务空间的智能体关联**）[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)；
2. **工作流应用**：将插件作为独立节点拖入画布，按编排顺序执行，不依赖大模型自主决策；
3. **Assistant API**：在 `tools` 字段中声明工具列表，模型自动规划调用；需确保 `tool_id` 与参数 schema 与控制台定义一致 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

自定义插件需先发布为 MCP 服务，再在智能体应用的 **MCP 区块**中添加；若含 `业务透传` 参数或用户级鉴权，必须通过 `biz_params` 或控制台配置传入 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限前提**：首次使用插件需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可一键授权；RAM 子账号需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略 Condition 中 `ram:ServiceName` 值应为 `cloundapi-access.sfm.aliyuncs.com`）[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **数量限制**：单个智能体应用最多关联 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **Python 解释器限制**：`code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（如 `requests~=2.31.0`、`pandas`、`matplotlib` 等），详见文档 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **发布要求**：自定义插件的工具必须处于 **已发布 + 启用** 状态才可调用；草稿状态或调试失败的工具无法生效 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **删除风险**：删除插件或工具将导致所有关联应用失效，且操作不可逆 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


