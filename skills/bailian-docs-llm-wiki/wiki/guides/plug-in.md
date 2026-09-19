# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式接入，弥补大模型在计算精度、时效性、[多模态](../concepts/multimodal.md)输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或基于自有 API 创建自定义插件，所有插件均通过统一的工具 ID 和参数契约被智能体或工作流调度。插件调用需依赖服务关联角色授权，且不同使用路径（控制台/Assistant API/工作流）对配置要求存在差异。

## 支持的模型与功能

- **支持模型**：当前明确兼容插件调用的模型包括 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的触发准确率与响应格式可能存在差异，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)强调“最新的兼容性状态，请以控制台实际执行结果为准”。
- **核心功能类型**：
  - **计算增强**：`calculator`（复杂数学运算）、`code_interpreter`（Python 代码执行，支持 `pandas`、`matplotlib`、`sympy` 等 20+ 预装依赖，但**不支持网络访问与本地文件上传**）；
  - **实时信息获取**：`quark_search`（返回网页标题/关键词/摘要，**不支持访问网页详情**）、`github_search`（返回项目标题/链接/摘要，**不支持访问项目详情**）；
  - **内容生成**：`text_to_image`（文生图，限时免费且需申请开通）、`generate_qrcode`（URL 转二维码）；
  - **自定义扩展**：支持通过 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 接入任意 HTTP API，支持 GET/POST、JSON/x-www-form-urlencoded、Header/Query 鉴权（basic/bearer/appcode）。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 和 `github_search` 的限制说明，但文档 1 在“夸克搜索”小节末尾额外强调“目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，而文档 2 仅写“支持检索网页标题、关键词和摘要，但不支持直接访问网页详情”。二者实质一致，无矛盾；但文档 1 的表述更完整，建议以文档 1 为准。

## 关键参数

- **工具 ID（tool_id）**：唯一标识插件下的具体工具，API 调用时必需。可通过插件详情页的“插件工具”区域或悬浮工具名称图标复制获取（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 中“获取工具 ID”说明）。
- **输入参数（input parameters）**：
  - `传参方式` 必须明确设为 `大模型识别`（从用户 query 中抽取）或 `业务透传`（由外部 SDK/HTTP 请求通过 `biz_params` 传入）；
  - `参数描述` 需精准（如 `date` 描述为 `yyyy-MM-dd 格式日期`），缺失会导致发布失败（错误码 `130040`）；
  - GET 请求**不支持 Object 类型入参**（错误码 `130022`）。
- **输出参数（output parameters）**：定义 API 返回数据中哪些字段将被大模型提取并用于生成最终回复，必须全部填写，嵌套层级应尽量扁平。
- **鉴权配置**：自定义插件可选 Header 或 Query 方式，`Type` 为 `bearer` 时自动添加前缀 `Bearer `，`Token` 字段值由 API 提供方发放。

## 使用方式

- **控制台集成（推荐快速验证）**：
  1. 主账号或已获 `ram:CreateServiceLinkedRole` 权限的 RAM 用户，需先在 [插件市场](https://bailian.console.aliyun.com/#/plugin-market) 完成 `AliyunServiceRoleForSFMAccessCloudAPI` 角色授权（详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）；
  2. 官方插件：直接“添加至智能体”，**仅限同业务空间内应用**；三方插件：需先开通套餐再添加；
  3. 自定义插件：需先发布为 MCP 服务，再在智能体编排页的 **MCP 区块** 中添加。
- **API 集成**：
  - **Assistant API**：在 `tools` 数组中传入工具定义（含 `tool_id`、`description`、`parameters`），详见 [Assistant API 文档](https://help.aliyun.com/zh/model-studio/quick-start-of-assistant-api)；
  - **DashScope SDK / HTTP**：通过 `biz_params` 传递业务透传参数或用户级鉴权 [Token](../concepts/token.md)（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）；
  - **工作流应用**：将插件作为独立节点编排，**不依赖大模型自主规划**，而是按预设流程执行。

## 限制和注意事项

- **权限强制要求**：无论主账号或 RAM 用户，首次使用插件均需创建 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色；RAM 用户需主账号预先授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **调用范围限制**：
  - 官方插件仅支持与**同一业务空间**内的智能体应用关联；
  - 单个智能体应用最多添加 **10 个工具**；
  - `code_interpreter` 禁止网络请求与文件系统操作，依赖列表以文档 1 为准；
  - `text_to_image` 为限时免费，需单独申请开通。
- **调试与发布强约束**：
  - 自定义插件的工具必须**测试成功后发布**，草稿状态不可调用；
  - 发布失败常见原因：Object 入参用于 GET 请求（`130022`）、参数描述为空（`130040`）、工具名称超 20 字符；
  - 删除插件或工具将导致**所有关联应用立即失效，且不可恢复**。
- **功能边界明确**：所有搜索类插件（`quark_search`、`github_search`）均**仅返回元信息摘要，不提供网页/仓库原始内容抓取能力**，需自行设计后续处理逻辑。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


