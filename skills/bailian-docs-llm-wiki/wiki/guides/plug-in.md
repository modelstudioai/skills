# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）集成到大模型工作流中，弥补其在实时信息获取、精确计算、代码执行、图像生成等领域的固有局限。插件支持官方预置、三方市场及自定义开发三类形态，可被智能体应用、工作流应用或 Assistant API 主动调用或编排使用。开发者需关注模型兼容性、参数配置规范及权限授权要求。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件调用的支持程度可能存在差异，**实际兼容性请以控制台运行结果为准**，而非静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置输入/输出参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自阿里云云市场，覆盖商业服务、图像视频、教育等领域，需开通后方可调用。
- **自定义插件**：开发者可基于自有 API 创建，支持完整参数映射、鉴权（Header/Query、basic/bearer/appcode）、多工具管理，并可通过发布为 MCP 服务接入智能体 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 在“常见问题”中明确指出“联网搜索（enable_search）也是基于夸克搜索”，且二者行为存在本质区别——前者返回结构化搜索结果供模型直接引用，后者仅辅助内容生成而不暴露原始结果。该差异非矛盾，而是功能层级不同；但开发者须注意：`quark_search` 插件 ≠ `enable_search` 开关，不可混用。

## 关键参数

插件调用依赖两类关键参数：

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，如 `calculator`、`text_to_image`。必须在 API 请求中显式传递，否则无法路由。获取方式：在插件详情页悬浮工具名称旁图标并复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入/输出参数**：
  - 输入参数需明确定义 `参数名称`、`参数描述`、`类型`（String/Number/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
  - 输出参数用于指导模型解析 API 响应，所有字段均为必填，描述应精简准确，嵌套层级宜浅。
  - 高级配置中的 `Value` 字段可提供调用示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数提取准确率。

## 使用方式

插件可通过三种方式集成：

1. **控制台可视化集成**：
   - 官方/三方插件：在[插件市场](https://bailian.console.aliyun.com/#/plugin-market)页面单击“添加至智能体”，选择目标智能体应用（注意：官方插件仅支持与**同业务空间**的智能体关联），最多添加 10 个工具 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块**中添加 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
2. **工作流应用节点**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖模型自主决策 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
3. **API 调用**：
   - Assistant API：在 `tools` 数组中声明工具定义，请求时由模型自动选择并调用。
   - DashScope SDK / HTTP 接口：通过 `biz_params` 传递业务透传参数或用户级鉴权 Token [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限前提**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需额外获得 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`），否则无法进入插件市场或导入云市场 API [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **计费与开通**：`text_to_image` 和 `quark_search` 为“限时免费，需申请开通”；其余官方插件免费。三方插件按所选套餐计费；自定义插件调用产生的云资源费用由开发者自行承担。
- **安全限制**：`code_interpreter` 插件**不支持对外网络访问及本地文件上传**，可用依赖已固化（如 `requests~=2.31.0`、`pandas`、`matplotlib` 等），不可扩展 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **调试与发布**：自定义插件的工具必须经“测试工具”验证成功并**发布**后才可在应用中调用；草稿状态工具不可用。发布失败常见原因包括：Object 参数子属性为空、GET 请求下误配 Object 入参、参数描述缺失等 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **模型行为边界**：插件调用由模型基于用户输入、工具名及工具描述自主触发，无法强制指定；工作流中则完全由人工编排控制。两者适用场景不同，不可替代。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


