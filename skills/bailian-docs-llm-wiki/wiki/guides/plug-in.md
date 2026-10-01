# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可直接调用官方/三方插件，或基于自有 API 创建自定义插件，所有插件均以“工具”为最小可调用单元，由大模型根据语义自动决策是否触发。

## 支持的模型/功能

- **支持模型**：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的支持能力存在差异，[最新兼容性状态请以控制台实际执行结果为准](raw/application-user-guide/plug-in/plug-in-overview.md)。
- **三类插件类型**：
  - **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）。详情见 [官方和第三方插件](raw/application-user-guide/plug-in/plugins.md)。
  - **三方插件**：来自阿里云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用，无需额外配置。
  - **自定义插件**：支持从零创建或从云市场导入，需明确定义插件 URL、工具路径、输入/输出参数及鉴权方式。完整流程详见 [自定义插件](raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 和文档 3 均列出 `quark_search` 工具 ID，但文档 1 中描述其“不支持直接访问网页详情”，而文档 3 仅复述该限制，未新增说明；两处一致，无矛盾。但文档 1 明确指出“夸克搜索插件目前支持检索出网页标题、关键词和摘要”，而文档 3 简化为“检索网页标题、关键词和摘要”，语义等价，无需修正。

## 关键参数

- **工具 ID**：全局唯一标识符，用于 API 调用时指定目标工具（如 `calculator`）。获取方式：在插件详情页悬浮工具名称旁图标后复制 [官方和第三方插件](raw/application-user-guide/plug-in/plugins.md)。
- **输入参数**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户输入中抽取）或 `业务透传`（由外部系统传入，需通过 `biz_params` 或 `user_defined_params` 传递）。
  - `参数名称` 和 `参数描述` 需语义清晰，直接影响大模型参数提取准确率；Object 类型参数子属性不可为空。
- **鉴权配置**（自定义插件）：
  - 支持 `Header`（默认 `Authorization` 字段）或 `Query`（如 `api_key=xxx`）方式。
  - `Type` 可选 `basic` / `bearer` / `appcode`，决定 Token 前缀（如 `Bearer <TOKEN>`）。
- **高级配置**（可选）：提供 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升复杂参数场景下的调用召回率与准确性。

## 使用方式

- **控制台集成**：
  - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 页面单击 **添加至智能体**，选择目标智能体应用完成绑定（最多 10 个工具）；子业务空间需先单独授权 [官方和第三方插件](raw/application-user-guide/plug-in/plugins.md)。
  - 自定义插件：需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加 [自定义插件](raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **API 调用**：
  - Assistant API：在请求 `tools` 字段中传入工具定义（含 `function.name`、`description`、`parameters`），并确保 `tool_choice` 合理设置。
  - DashScope SDK / HTTP 接口：通过 `tools` 参数传入工具 ID 列表，并在 `biz_params` 中透传鉴权或业务参数 [自定义插件](raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限依赖**：主账号或 RAM 用户首次使用插件前，必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限，否则无法完成授权 [官方和第三方插件](raw/application-user-guide/plug-in/plugins.md)。
- **功能边界**：
  - `code_interpreter` 不支持网络访问与本地文件上传，仅预装指定依赖（如 `pandas`、`matplotlib`、`requests` 等）。
  - `quark_search` 和 `github_search` 仅返回网页/项目元数据（标题、摘要、链接），**不支持抓取正文或仓库代码内容**。
  - 自定义插件中，GET 请求方法**不支持 Object 类型输入参数**；Object 参数必须使用 POST。
- **发布要求**：自定义插件下的工具必须处于 **已发布** 且 **调试成功** 状态才可被调用；编辑后需重新测试并发布，否则变更不生效 [自定义插件](raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **计费提示**：`text_to_image` 和 `quark_search` 为限时免费，需主动申请开通；其余官方插件当前免费，但策略可能调整，请以控制台实际展示为准。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)


