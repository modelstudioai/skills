# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等 API）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可直接调用官方/三方插件，或创建自定义插件以对接私有服务。插件调用由大模型自主规划（智能体/Assistant API）或显式编排（工作流）驱动。

## 支持的模型与功能

- **支持模型**：当前仅 `qwen-plus` 和 `qwen-max` 两个模型支持插件调用，其他模型暂不兼容。具体兼容性请以[选择模型](raw/model-user-guide/get-started-with-models/models.md)文档及控制台实际执行结果为准。
- **功能类型**：
  - **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等。详情见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
  - **三方插件**：来自云市场，覆盖商业服务、教育、音视频等领域，开通后即可调用，无需额外配置。使用说明参见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
  - **自定义插件**：支持从零创建或从云市场导入，可对接任意 HTTP API。需明确定义插件 URL、工具路径、输入/输出参数及鉴权方式。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 中称“各模型对插件的兼容性可能有差异”，而文档 3 未明确列出兼容模型；但两文档均一致指出 `qwen-plus` 和 `qwen-max` 是当前支持插件的模型，因此以该范围为准，其他模型标识符（如 `qwen-turbo`）不在支持列表内。

## 关键参数

- **插件级参数**：
  - `插件URL`：工具路径的根域名，例如 `https://example.com`；所有工具路径均以此为前缀拼接。
  - `是否鉴权`：启用后需配置鉴权类型（`basic`/`bearer`/`appcode`）、位置（`Header` 或 `Query`）及 `Token`（服务级）或 `参数名`（用户级）。
- **工具级参数**：
  - `工具路径`：必须以 `/` 开头的相对路径（如 `/query`），与插件 URL 拼接构成完整请求地址。
  - `输入参数`：需定义 `参数名称`、`参数描述`（自然语言，含示例更佳）、`类型`（`String`/`Number`/`Object` 等）、`传参方式`（`大模型识别` 或 `业务透传`）。
  - `输出参数`：必填，用于指导大模型解析 API 响应；嵌套层级应尽量扁平，避免空子属性（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 130022）。
- **高级配置（可选）**：提供 `Value` 字段填写用户 Query 与期望入参的映射示例（如 `"查询杭州明天天气" → {"city": "杭州", "date": "2025-04-25"}`），显著提升大模型参数提取准确率。

## 使用方式

- **控制台集成**：
  - 官方/三方插件：在 [插件](https://bailian.console.aliyun.com/#/plugin-market) 页面点击 **添加至智能体**，选择目标智能体应用（注意：官方插件仅支持同业务空间的应用），最多添加 10 个工具。
  - 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块**中添加；若含 `业务透传` 参数或 `用户级鉴权`，需在对话前手动配置 `biz_params` 或 [Token](../concepts/token.md)。
- **API 集成**：
  - 通过 Assistant API 调用：在 `tools` 字段中声明工具 ID，并在 `tool_choice` 中指定策略（`auto`/`required`/具体 ID）。参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)。
  - 通过 DashScope SDK 或 HTTP 接口调用智能体/工作流应用时，`biz_params` 用于传递业务透传参数或用户级鉴权信息（见 [应用的参数传递](raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。
- **工作流应用**：将插件作为独立节点拖入画布，按需配置输入输出映射，不依赖大模型自动决策。

## 限制和注意事项

- **权限限制**：首次访问插件市场需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。主账号可直接授权；RAM 用户（子账号）需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **功能限制**：
  - `code_interpreter` 插件禁止网络访问与本地文件上传，仅支持预装依赖（如 `pandas`, `matplotlib`, `sympy` 等）。
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、关键词、摘要，**不支持访问原始网页或仓库详情页**（文档 1 和文档 3 均明确强调此限制）。
  - `text_to_image` 和 `quark_search` 为限时免费，需单独申请开通。
- **配置限制**：
  - 工具名称长度 ≤ 20 字符（超长将导致发布失败，见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
  - GET 请求不支持 `Object` 类型输入参数（错误码 130022）。
- **运维风险**：删除插件将**不可逆地移除其下所有工具**，并导致已关联的应用失效；编辑插件 URL 或鉴权配置后，必须重新测试并发布工具方可生效。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


