# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态输出等方面的固有局限。插件可被智能体应用、工作流应用或 Assistant API 主动调用，实现“规划-调用-推理”闭环。所有插件均需在控制台完成授权、配置与发布后方可使用。

## 支持的模型/功能

- **支持模型**：当前仅 `qwen-plus` 和 `qwen-max` 两个模型支持插件调用，其他模型暂不兼容。具体兼容性请以[选择模型](raw/model-user-guide/get-started-with-models/models.md)文档及控制台实际执行结果为准。  
- **插件类型**：  
  - **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 执行）、`calculator`（数学计算）、`text_to_image`（文生图）、`quark_search`（实时搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 搜索）等。详情见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。  
  - **三方插件**：来自阿里云云市场，覆盖商业服务、教育、音视频等领域，需开通后使用。  
  - **自定义插件**：支持用户通过 API 接入自有服务，支持鉴权（Header/Query）、多工具路径、复杂参数映射与在线调试。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。  

> **注意**：文档 1 中称“各模型对插件的兼容性可能有差异”，但未明确列出不支持的模型；文档 2 和 3 均未提及其他模型支持状态。建议开发者以控制台实际可用模型列表为准，避免依赖未验证的模型标识符。

## 关键参数

- **工具 ID**：唯一标识一个工具，API 调用时必需。可在插件详情页的“插件工具”区域悬停工具名称图标复制（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。  
- **输入参数**：  
  - `传参方式` 必须准确设置为 `大模型识别`（从用户输入中抽取）或 `业务透传`（由外部传入，需通过 `biz_params` 或 `user_defined_params` 传递）；  
  - `参数描述` 必须清晰、含示例（如 `city: "杭州"`），直接影响大模型参数提取准确率；  
  - Object 类型参数的子属性**不能为空**，否则发布失败（错误码 130022，见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。  
- **输出参数**：所有出参均为必填，定义应精简、扁平化（避免深层嵌套），便于大模型筛选重组后生成最终回复。  
- **鉴权配置**：支持 `basic`/`bearer`/`appcode` 三种 Type，[Token](../concepts/token.md) 位置可选 Header 或 Query；若开启鉴权，调试与 API 调用时均需提供有效凭证。

## 使用方式

1. **控制台集成（推荐快速验证）**：  
   - 官方/三方插件：在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 授权后，通过“添加至智能体”关联到同业务空间的智能体应用（最多 10 个工具）；  
   - 自定义插件：需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；  
2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖大模型自动规划；  
3. **API 调用**：  
   - Assistant API：在 `tools` 字段中声明工具 ID 及描述，系统自动触发调用（参考 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)）；  
   - DashScope SDK / HTTP：需在请求中显式传入 `tool_choice` 及 `tools`，业务透传参数与鉴权信息通过 `biz_params` 传递（见 [应用的参数传递](raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)）。

## 限制和注意事项

- **权限要求**：首次使用插件前，主账号或 RAM 子账号必须授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；子账号需额外授予 `ram:CreateServiceLinkedRole` 权限（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。  
- **功能限制**：  
  - `code_interpreter` 不支持网络访问、本地文件上传，依赖库版本固定（如 `matplotlib`, `pandas`, `sympy` 等）；  
  - `quark_search` 和 `github_search` 仅返回网页标题、关键词、摘要，**不支持访问原始网页或项目详情页**；  
  - 自定义插件的工具路径必须以 `/` 开头，且同一插件下所有工具共享插件 URL 域名；  
- **发布约束**：  
  - 工具名称长度 ≤ 20 字符，超长将导致发布失败（错误码提示 `22/20`）；  
  - 工具必须处于 **已发布** 且 **调试成功** 状态才可被调用；  
  - 删除插件或工具将导致关联应用立即失效，操作不可逆。  
- **计费说明**：官方插件中 `text_to_image` 和 `quark_search` 为限时免费，需单独申请开通；其余官方插件及已开通的三方插件按实际调用量计费。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


