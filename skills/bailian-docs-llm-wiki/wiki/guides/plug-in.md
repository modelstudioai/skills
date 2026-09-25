# plug in

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如计算、搜索、图像生成等）以标准化方式接入，弥补大模型在实时信息获取、精确计算、多模态生成等方面的固有局限。开发者可直接调用官方/三方插件，或基于业务需求创建自定义插件，实现灵活的功能增强。插件调用由大模型自主规划（智能体/Assistant API）或人工编排（工作流）驱动，无需修改模型本身。

## 支持的模型与功能

百炼当前支持在以下模型上启用插件能力：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max`、`qwen-vl-plus`。各模型对插件的兼容性可能存在差异，实际可用性请以控制台执行结果为准 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

官方插件提供开箱即用的常用能力，包括：
- `code_interpreter`：执行 Python 代码（数学计算、数据分析、可视化），依赖固定版本库（如 `pandas`, `matplotlib`, `sympy`），**不支持网络访问与本地文件上传**；
- `calculator`：高精度复杂数学运算；
- `text_to_image`：文生图（限时免费，需申请开通）；
- `quark_search`：实时网络搜索（返回标题、关键词、摘要，**不支持网页详情访问**）；
- `generate_qrcode`：URL 转二维码；
- `github_search`：GitHub 项目检索（返回标题、链接、摘要，**不支持项目详情访问**）。

三方插件覆盖商业服务、图像视频、教育等领域，需在插件市场开通后使用；自定义插件支持通过 API 接入任意业务系统，详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档1与文档2均指出 `quark_search` 和 `github_search` 不支持访问网页/项目详情，但文档2额外强调其返回内容为“标题、关键词和摘要”，而文档1仅提“标题、关键词和摘要”，二者一致，无矛盾。但文档2明确 `quark_search` 与 `enable_search` 的区别：前者直接返回结构化搜索结果供模型使用，后者仅为模型生成提供辅助信息，此细节在文档1中未体现，属补充说明。

## 关键参数

- **工具 ID**：唯一标识插件下的具体工具（如 `calculator`），API 调用时必需。可通过插件详情页悬浮图标复制 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **输入参数**：配置时需指定名称、描述、类型（String/Number/Object 等）、传参方式（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，否则发布失败 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **输出参数**：定义 API 返回数据中需提取的字段，影响模型最终回答的准确性，所有参数均为必填。
- **鉴权配置**：支持 Header（`Authorization`）或 Query（如 `api_key`）方式，鉴权类型包括 `basic`、`bearer`、`appcode`；[Token](../concepts/token.md) 值需按类型自动拼接前缀。

## 使用方式

插件可通过三种方式集成：
1. **智能体应用（Agent 1.0）**：在插件市场选择工具 → 添加至目标智能体 → 发布应用。官方插件仅支持与**同业务空间**的智能体关联 [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。
2. **工作流应用**：将插件作为独立节点拖入画布，按需编排执行顺序，不依赖模型自主决策。
3. **Assistant API**：在请求体 `tools` 字段中声明工具列表，模型根据用户输入自动选择并调用 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

自定义插件需先发布为 MCP 服务，再在智能体编排页面的 **MCP 区块** 中添加；若含 `业务透传` 参数或用户级鉴权，需通过 `biz_params` 透传值 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 限制和注意事项

- **权限要求**：首次使用插件需主账号或具备 `ram:CreateServiceLinkedRole` 权限的 RAM 用户授权角色 `AliyunServiceRoleForSFMAccessCloudAPI`，否则无法访问插件市场 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **数量限制**：单个智能体应用最多关联 10 个工具。
- **自定义插件调试**：工具必须**发布成功**且状态为“已发布”+“启用”方可调用；发布失败常见原因包括 Object 参数子属性为空、GET 请求误配 Object 入参、工具名称超 20 字符等 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。
- **安全限制**：`code_interpreter` 插件禁止网络访问及本地文件操作，仅限沙箱内执行；所有插件调用均受百炼平台安全策略约束，不可绕过。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)


