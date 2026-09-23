# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API）集成到大模型工作流中，可有效弥补模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场及自定义开发三种来源，适用于智能体应用、工作流应用和 Assistant API 三种调用路径。开发者需关注模型兼容性、参数配置规范及权限授权要求。

## 支持的模型/功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的实际支持情况可能存在差异，**请以控制台实际执行结果为准**，而非文档静态列表 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件按来源分为三类：
- **官方插件**：组件广场预置，开箱即用，无需配置输入/输出参数，包括 `code_interpreter`（Python 执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等；
- **三方插件**：来自阿里云市场，覆盖商业服务、教育、音视频等领域，需开通后使用；
- **自定义插件**：开发者可基于自有 API 创建，支持完整鉴权（Header/Query、basic/bearer/appcode）、多工具管理及 MCP 服务发布 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件说明，但文档 2 明确指出其“不支持直接访问网页详情”，而文档 1 仅模糊表述为“不支持直接访问网页详情”——二者一致；但文档 2 新增关键对比：“夸克搜索插件”与“联网搜索（`enable_search`）”本质不同：前者返回结构化搜索结果供模型直接引用，后者仅为模型生成提供辅助信息，**不可混用** [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必须传入，可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **输入参数（入参）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户 query 中抽取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 携带）；
  - `参数描述` 需简洁准确（如 `city: 城市名称，中文，例如"杭州"`），缺失将导致发布失败（错误码 130040）；
- **输出参数（出参）**：所有字段必填，类型建议扁平化（避免深层嵌套 Object），大模型据此解析并重组响应；
- **鉴权配置**（仅自定义插件）：支持 Header 或 Query 方式，`Type` 可选 `basic`/`bearer`/`appcode`；若选 `bearer`，实际请求头为 `Authorization: Bearer <TOKEN>`。

## 使用方式

1. **权限准备**：主账号或 RAM 子账号首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（含特定 `Condition` 约束），否则无法进入插件市场 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
2. **插件接入**：
   - 官方/三方插件：在插件市场页面单击 **添加至智能体**，选择目标智能体（同一业务空间），最多添加 10 个工具；
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加；
3. **调用路径**：
   - 智能体应用（Agent 1.0）：模型自主规划是否调用、调用哪个工具；
   - 工作流应用：插件作为显式节点，按流程编排执行；
   - Assistant API：在 `tools` 数组中声明工具定义，请求时携带 `tool_choice` 控制调用策略。

## 限制和注意事项

- **模型限制**：`qwen-turbo` 等轻量模型对复杂工具链支持较弱，建议优先在 `qwen-plus` 或 `qwen-max` 上验证；
- **功能限制**：
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（如 `requests~=2.31.0`、`pandas` 等）；
  - `quark_search` 和 `github_search` 仅返回摘要/标题/链接，**不支持抓取网页正文或项目源码**；
  - 同一插件下多个工具共享域名，工具路径（如 `/query`）需以 `/` 开头，拼接至插件 URL 构成完整 endpoint；
- **配置风险**：
  - 自定义插件发布前必须完成在线调试且状态为“成功”，否则应用调用将失败；
  - 删除插件或工具会导致已关联的应用失效，且操作不可逆；
  - GET 请求不支持 Object 类型入参（错误码 130022），应改用 POST + `application/json`；
- **计费提示**：`text_to_image` 和 `quark_search` 为限时免费，需主动申请开通；其余官方插件当前免费，但策略可能调整，请以控制台最新公告为准。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


