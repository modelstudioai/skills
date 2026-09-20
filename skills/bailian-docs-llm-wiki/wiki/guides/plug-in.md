# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（API）封装为可被大模型识别、规划和调用的标准化接口，弥补模型在实时信息获取、精确计算、代码执行、图像生成等方面的固有局限。插件支持官方预置、三方市场及用户自定义三种来源，可在智能体应用、工作流应用及 Assistant API 中统一集成与调用。其设计目标是让开发者以最小配置成本实现能力增强，而非替代模型本身。

## 支持的模型/功能

百炼插件当前支持以下模型：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件调用的支持程度存在差异，**实际兼容性请以控制台运行结果为准**，不建议依赖文档静态列表做兼容性判断 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

插件功能分为三类：
- **官方插件**：开箱即用，无需配置参数，包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（URL 转二维码）、`github_search`（GitHub 项目检索）等 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，需开通后使用；
- **自定义插件**：用户自主开发并注册的 API 封装，支持完全定制化逻辑与鉴权方式 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 1 与文档 3 均列出 `quark_search` 插件说明，但文档 1 称其“限时免费，需申请开通”，而文档 3 未提申请要求；同时文档 3 明确指出“夸克搜索插件目前支持检索出网页标题、关键词和摘要，但不支持直接访问网页详情”，该限制在文档 1 中仅以 > 引用形式出现，未作为正式限制项强调。建议以文档 3 的表述为准，即该插件**不支持网页详情访问**，且开通流程应以控制台实际指引为准。

## 关键参数

插件调用依赖两类关键参数：

- **插件级参数**（定义在插件创建时）：
  - `plugin_url`：插件根域名，如 `https://myapi.example.com`；
  - `is_auth_required` + 鉴权配置（Header/Query、Type、Token）：决定调用是否携带认证信息；
  - `plugin_description`：自然语言描述，直接影响大模型是否触发该插件。

- **工具级参数**（定义在每个工具下）：
  - `tool_name` 和 `tool_description`：语义化命名与功能说明，必须使用自然语言并建议含示例；
  - `tool_path`：以 `/` 开头的相对路径，拼接 `plugin_url` 构成完整 API 地址；
  - 输入参数（`in_params`）：需明确 `parameter_name`、`description`、`type`（String/Number/Object 等）、`passing_method`（`model_recognition` 或 `biz_pass_through`）；
  - 输出参数（`out_params`）：定义返回数据结构，大模型据此提取并组织最终响应；
  - 高级配置（`advanced_config`）：可选调用示例（`value` 字段），用于提升复杂参数场景下的召回准确率。

所有 Object 类型参数的子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 使用方式

插件可通过以下三种方式集成：

1. **控制台智能体应用**：在插件市场选择插件 → 单击“添加至智能体” → 选择目标智能体 → 测试对话 → 发布应用；
2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖大模型自动规划；
3. **API 调用**：
   - 通过 DashScope SDK 或 HTTP 接口调用已发布的智能体/工作流应用；
   - 若含 `biz_pass_through` 参数或用户级鉴权，需通过 `biz_params` 透传；
   - 工具 ID 可在插件详情页工具行悬停图标处复制，用于调试与日志追踪 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

> **注意**：官方插件仅能与**同业务空间**内的智能体应用关联；子业务空间首次使用需先完成插件授权操作 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 限制和注意事项

- **调用上限**：单次请求最多支持调用 10 个工具（含同一插件下多个工具或跨插件组合）；
- **Object 类型限制**：GET 请求方法下**不支持 Object 类型输入参数**；若需嵌套结构，必须使用 POST + `application/json` [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)；
- **安全限制**：
  - `code_interpreter` 插件禁止网络访问与本地文件上传，仅限沙箱内执行，依赖库版本固定；
  - `quark_search` 和 `github_search` 均仅返回摘要级结果（标题、关键词、摘要），**不支持跳转或解析原始网页/仓库详情**；
- **发布与生效**：工具必须处于“已发布”且“启用”状态才可被调用；修改插件 URL 或鉴权配置后，须重新测试并发布所有关联工具；
- **RAM 用户权限**：子账号使用云市场插件或导入插件前，主账号需为其授予 `ram:CreateServiceLinkedRole` 权限，否则授权失败 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)；
- **错误处理**：常见发布失败错误码包括 `130040`（参数描述缺失）、`130022`（Object 子属性为空或 GET 含 Object 参数），需按提示修正后重试 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)


