# plug in

插件是百炼平台扩展大模型能力的核心机制，通过将外部工具（如代码执行、实时搜索、图像生成等）以标准化方式接入，弥补大模型在精确计算、实时信息获取、多模态输出等方面的固有局限。开发者可直接调用官方插件、开通三方插件，或基于自有 API 创建自定义插件，所有插件均通过统一的工具 ID 和参数契约被智能体或工作流调度。插件调用依赖服务关联角色授权与业务空间级权限控制，需严格遵循配置规范。

## 支持的模型/功能

- **支持模型**：当前明确兼容插件调用的模型为 `qwen-plus` 和 `qwen-max`。其他模型的兼容性以控制台实际执行结果为准，[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md) 中明确指出“各模型对插件的兼容性可能有差异”。
- **核心功能类型**：
  - **官方插件**：开箱即用，无需配置输入/输出参数，包括 `code_interpreter`（Python 执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）。
  - **三方插件**：覆盖商业服务、图像视频、学习教育等领域，需在云市场开通后调用，详见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
  - **自定义插件**：支持通过插件 URL + 工具路径（如 `/query`）集成任意 HTTP API，并可配置鉴权（Header/Query）、输入/输出参数映射及高级调用示例，完整流程见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 2 均列出 `quark_search` 插件，但文档 1 称其“限时免费，需申请开通”，而文档 2 未提开通要求；实际开通状态请以控制台插件市场页面为准。

## 关键参数

- **工具 ID（`tool_id`）**：唯一标识一个工具，API 调用时必须传入。可在插件详情页的“插件工具”区域或自定义插件的工具卡片上悬停图标复制（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md) 和 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **输入参数（`input_parameters`）**：
  - `传参方式`：分为 `大模型识别`（从用户输入中抽取）和 `业务透传`（由外部系统通过 `biz_params` 或 `user_defined_params` 透传）。
  - `参数名称` 与 `参数描述` 必须语义清晰，直接影响大模型参数提取准确性。
- **输出参数（`output_parameters`）**：定义 API 返回数据的结构，大模型据此筛选并重组结果。Object 类型子属性不能为空，否则发布失败（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 130022）。
- **鉴权配置**：支持 `basic`/`bearer`/`appcode` 类型，可置于 Header 或 Query 中；自定义插件需在创建时显式开启“是否鉴权”开关。

## 使用方式

1. **权限准备**：主账号或 RAM 用户需具备 `AliyunServiceRoleForSFMAccessCloudAPI` 服务关联角色权限。RAM 用户需先由主账号授予 `ram:CreateServiceLinkedRole` 权限（策略脚本见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
2. **插件接入**：
   - **官方/三方插件**：在插件市场页面点击“添加至智能体”，选择目标智能体应用（最多 10 个工具），或在应用编排页的 MCP 区块中添加。
   - **自定义插件**：需先创建插件 → 添加并调试工具 → 发布工具 → 发布为 MCP 服务 → 在智能体应用中添加该 MCP 服务。
3. **调用触发**：通过智能体应用（Agent 1.0）、工作流应用节点或 Assistant API 的 `tools` 字段传入工具 ID 及参数。大模型根据用户输入、工具名称和描述自主决策是否调用（见 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)）。
4. **参数透传（API 场景）**：若工具含 `业务透传` 参数或启用用户级鉴权，需通过 `biz_params` 字段传递对应值（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 限制和注意事项

- **业务空间隔离**：官方插件仅能与**相同业务空间**内的智能体应用关联；子业务空间首次调用前需单独授权（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
- **功能边界**：
  - `code_interpreter` 不支持网络访问及本地文件上传，依赖库版本固定（见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)）。
  - `quark_search` 和 `github_search` 仅返回网页/项目标题、关键词、摘要，**不支持访问原始网页或仓库详情页**（两文档均强调此限制）。
- **配置强约束**：
  - 自定义插件的 Object 类型输入/输出参数，子属性不能为空，否则发布失败（错误码 130022）。
  - GET 请求方法下，输入参数不支持 Object 类型（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。
- **安全与维护**：删除插件将导致所有关联应用失效且不可恢复；编辑插件 URL 或鉴权信息后，必须重新测试并发布工具（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)）。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


