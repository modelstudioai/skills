# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等 API）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。插件可被智能体（Agent 1.0）、工作流应用及 Assistant API 主动调用或编排执行，实现任务自动化与能力增强。所有插件均需经授权、配置与发布后方可使用。

## 支持的模型/功能

- **支持模型**：当前仅 `qwen-plus` 和 `qwen-max` 明确支持插件调用；其他模型兼容性以控制台实际执行结果为准（参见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。
- **插件类型**：
  - **官方插件**：预置于组件广场，开箱即用，无需配置输入/输出参数，包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 搜索）等。
  - **三方插件**：来自云市场，覆盖商业服务、教育、音视频等领域，需开通后使用（参见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
  - **自定义插件**：支持用户基于自有 API 创建，需定义插件 URL、工具路径、鉴权方式、输入/输出参数，并完成调试与发布（参见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

> **注意**：文档 1 中称“各模型对插件的兼容性可能有差异”，但未明确列出不支持的模型；文档 2 和 3 均未提及其他模型支持状态。开发者应以控制台实际调用结果为最终依据，避免依赖未验证的模型标识符。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页悬浮图标复制（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **输入参数**：
  - `传参方式`：`大模型识别`（从用户输入中抽取）或 `业务透传`（由外部通过 `biz_params` 或 `user_defined_params` 传入）；
  - `类型`：支持 `String`、`Number`、`Object` 等，`Object` 类型子属性不可为空（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；
  - `高级配置`：可设置 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），提升大模型参数构造准确率。
- **鉴权配置**（自定义插件）：
  - 支持 `Header`（如 `Authorization: Bearer <TOKEN>`）或 `Query`（如 `?api_key=xxx`）方式；
  - `Type` 可选 `basic` / `bearer` / `appcode`，决定 [Token](../concepts/token.md) 前缀；
  - RAM 用户需主账号授予 `ram:CreateServiceLinkedRole` 权限方可创建服务关联角色（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。

## 使用方式

1. **控制台集成**：
   - **智能体应用**：在插件市场选择插件 → 单击“添加至智能体” → 选择目标应用 → 发布后测试（最多支持 10 个工具）；
   - **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序（参见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）；
   - **MCP 服务**（自定义插件）：发布插件为 MCP 服务 → 在智能体编排页 MCP 区块添加 → 配置鉴权/透传参数（如启用）→ 测试并发布。

2. **API 调用**：
   - **Assistant API**：在 `tools` 字段中声明工具列表，工具 ID 必须与控制台一致（参见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
   - **DashScope SDK / HTTP 接口**：若含 `业务透传` 参数或用户级鉴权，需通过 `biz_params` 传递对应值（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **权限限制**：主账号或 RAM 用户首次访问插件市场前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 用户需额外获得 `ram:CreateServiceLinkedRole` 权限（[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **功能限制**：
  - `code_interpreter` 不支持网络访问、本地文件上传，可用依赖版本已固化（参见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
  - `quark_search` 和 `github_search` 仅返回网页标题/关键词/摘要，不支持访问原始网页或项目详情页；
  - 自定义插件中，GET 请求不支持 `Object` 类型输入参数（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **发布约束**：
  - 工具名称长度 ≤ 20 字符，超长将导致发布失败；
  - 删除插件或工具将导致已关联的应用失效，且操作不可逆；
  - 从云市场导入的插件需手动测试并发布，系统填充的参数可能存在缺失，需人工校验（[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


