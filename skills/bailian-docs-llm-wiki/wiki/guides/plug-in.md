# plug in

百炼插件是一个工具集合，用于扩展大模型的能力边界。一个插件下可包含多个工具（API），每个工具实现特定功能。通过将插件集成到大模型应用中，可弥补大模型在获取最新信息、精确计算、图像处理等方面的不足。百炼支持官方插件、三方插件和自定义插件三类。详见[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 插件分类

- **官方插件**：组件广场预置，无需配置输入输出参数即可直接调用。
- **三方插件**：涵盖商业服务、图像视频、学习教育等领域，经过效果测试，开通后直接调用，无需额外配置。
- **自定义插件**：当官方和三方插件无法满足业务需求时，用户可创建或从云市场导入自定义插件，集成到应用中。

## 官方插件列表

| 插件名称 | 工具 ID | 说明 | [计费](../concepts/billing.md)方案 |
| --- | --- | --- | --- |
| Python 代码解释器 | `code_interpreter` | 执行 Python 代码片段，如数学计算、数据分析与可视化、数据处理 | 免费 |
| 计算器 | `calculator` | 进行复杂数学计算，例如计算 `12313x13232` | 免费 |
| 图片生成 | `text_to_image` | 基于文本生成图片，例如"请画一只在笑的小狗" | 限时免费，需申请开通 |
| 夸克搜索 | `quark_search` | 搜索实时信息，查找公开网络知识和信息 | 限时免费，需申请开通 |
| 生成二维码 | `generate_qrcode` | 根据网站链接地址生成二维码 | 免费 |
| GitHub 搜索 | `github_search` | 在 GitHub 中搜索相关项目列表 | 免费 |

> **注意**：夸克搜索插件目前支持检索网页标题、关键词和摘要，但不支持直接访问网页详情。GitHub 搜索插件支持检索项目标题、链接和摘要，不支持访问项目详情。Python 代码解释器不支持对外访问网络以及上传本地文件。

Python 代码解释器可用依赖包括：matplotlib、pandas、scipy、seaborn、sympy、pillow、pydantic~=1.10.8、requests~=2.31.0、oss2~=2.18.1、pdfminer-six、pypdf、python-pptx、wordcloud 等。详见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。

## 支持的模型

插件调用对模型有一定要求，目前支持以下模型：

| 模型 | 模型标识符 |
| --- | --- |
| 通义千问-Turbo | qwen-turbo |
| 通义千问-Plus | qwen-plus |
| 通义千问-Max | qwen-max |
| 通义千问VL-Max | qwen-vl-max |
| 通义千问VL-Plus | qwen-vl-plus |

> **注意**：各模型对插件的兼容性可能有差异，最新兼容性状态以控制台实际执行结果为准。

## 插件调用机制

调用插件的本质是调用插件下的工具。百炼支持通过[智能体应用](../concepts/agent-application.md)、[工作流](../concepts/workflow.md)应用以及 Assistant API 调用插件。

- **[智能体应用](../concepts/agent-application.md) / Assistant API**：大模型根据用户输入内容、工具名称和工具描述判断是否调用工具。需要调用时，模型选择合适工具，应用内部完成调用后将工具返回结果与用户内容合并再次输入模型，由模型生成最终结果；无需调用时直接生成结果输出。
- **[工作流](../concepts/workflow.md)应用**：插件作为[工作流](../concepts/workflow.md)的一个节点，按用户编排的方式执行特定任务，而非由模型主动规划和调用。

## 使用方式

### 首次访问授权

主账号或 RAM 用户首次访问插件页面时，需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`（权限策略 `AliyunServiceRolePolicyForSFMAccessCloudAPI`），用于授权百炼访问云市场商品清单并根据插件配置进行 API 调用。

- **主账号**：在插件页面勾选条款，单击"授权并进入"即可。
- **RAM 用户（子账号）**：会因缺少创建服务关联角色权限报错（错误码 140052）。需先由主账号在 RAM 控制台创建自定义权限策略（Action 为 `ram:CreateServiceLinkedRole`，Condition 中 `ram:ServiceName` 为 `cloundapi-access.sfm.aliyuncs.com`），并授予子账号该策略后，再完成授权。

### 调用插件

- **方式一（插件页面）**：在插件页面将工具添加至[智能体应用](../concepts/agent-application.md)。官方插件只能与位于相同[业务空间](../concepts/workspace.md)里的[智能体应用](../concepts/agent-application.md)关联。每个[智能体应用](../concepts/agent-application.md)最多支持添加 10 个工具，应用会根据输入选择调用一个或多个工具。
- **方式二（应用管理页面）**：在指定智能体或工作流应用内添加插件，测试效果并发布应用。
- **方式三（Assistant API）**：通过 Assistant API 调用工具，需正确传递工具 ID。

子[业务空间](../concepts/workspace.md)调用官方插件前，需先在插件详情页为子[业务空间](../concepts/workspace.md)授权；默认[业务空间](../concepts/workspace.md)无需此步骤。

### 获取工具 ID

通过 API 调用工具时需正确传递工具 ID。在插件页面找到目标插件，单击"查看详情"，在"插件工具"下获取工具 ID（例如 `calculator`）。

## 自定义插件

当官方和三方插件无法满足业务需求时，可创建自定义插件。详见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

### 工作流程

1. **创建/导入插件**：定义插件基础信息，或直接从云市场导入。
2. **添加工具**（导入插件无需此步）：配置 API 路径、请求参数和返回数据。
3. **调试与发布**：在线测试 API 连通性，功能正常后发布。只有已发布的工具才能在应用中被调用。
4. **在应用中使用**：将插件关联到智能体，通过对话测试或 API 集成调用。

### 创建插件关键参数

- **插件名称**：支持中英文，需具语义。
- **插件描述**：对插件功能和使用场景的简要说明，帮助大模型判断是否调用，使用自然语言描述。
- **插件 URL**：插件访问地址。同一域名下不同路径拆分为不同 API（工具路径）。
- **是否鉴权**：支持服务级鉴权和用户级鉴权。鉴权信息可放在 Header（默认参数名 `Authorization`）或 Query 中；Type 支持 `basic`（[Token](../concepts/token.md) 前不增加内容）、`bearer`（[Token](../concepts/token.md) 前增加 "Bearer"）、`appcode`（[Token](../concepts/token.md) 前增加 "APPCODE"）。

### 创建工具关键参数

- **工具名称**：支持中英文，有字符数限制（20 字符）。
- **工具描述**：帮助大模型判断是否调用该工具，尽量给出使用示例。
- **工具路径**：指向插件 URL 的相对路径，必须以正斜杠（/）开头。
- **请求方法**：GET 或 POST。
- **提交方式**：`application/json` 或 `application/x-www-form-urlencoded`。
- **输入参数传参方式**：
  - **大模型识别**：参数值由大模型从用户输入中提取。
  - **业务透传**：参数值从外部主动透传，通过 `biz_params` 和 `user_defined_params` 传递。
- **高级配置**：提供调用示例（Query 与期望入参 Value），减少漏召回和误召回。

> **注意**：Object 类型下的子属性不能为空，需点击对象行末图标新增子属性。GET 请求方法下的输入参数不支持 Object 类型。

### 从云市场导入

云市场提供丰富 API，可在云市场开通后导入至百炼插件列表。导入的插件为草稿状态，需测试、发布后使用。导入时系统自动填充出入参，但可能存在信息缺失，发布时需根据错误提示修正。

### 使用自定义插件

控制台内可将插件发布为 MCP 服务，再在[智能体应用](../concepts/agent-application.md)编排页面的 MCP 区块添加该服务；也可直接在应用管理页面的[智能体应用](../concepts/agent-application.md)编排中添加 MCP 服务。无鉴权插件可直接对话测试；用户级/服务级鉴权需在对话前配置鉴权 [Token](../concepts/token.md)；业务透传参数需配置变量值。从云市场导入的插件无需在对话页输入鉴权 [Token](../concepts/token.md)。

通过 API 调用时，若应用关联的插件存在业务透传参数或开启了用户级鉴权，需通过 `biz_params` 传递鉴权信息或透传参数。

## 限制和注意事项

- 官方插件只能与位于相同[业务空间](../concepts/workspace.md)的[智能体应用](../concepts/agent-application.md)关联。
- 每个[智能体应用](../concepts/agent-application.md)最多添加 10 个工具。
- 只有已发布且启用状态、调试状态为成功的工具才能用于调用。
- 删除插件会删除其下所有工具，调用该插件的应用会失效，操作不可撤回。
- 编辑插件信息后立即生效；修改 URL、Header、鉴权信息可能影响工具调用，需重新测试并发布工具。
- 工具信息修改后需重新测试并发布才能生效。

### 常见错误码

| 错误码 | 错误信息 | 说明 |
| --- | --- | --- |
| 130040 | xx 缺少参数描述信息 | 参数描述缺失，补充后重新发布 |
| 130022 | 保存工具信息异常/请检查示例参数是否正确 | 原因一：Object 类型参数子属性为空，需新增子属性；原因二：GET 请求下存在 Object 类型输入参数，需选择其他类型 |

## 常见问题

**夸克搜索和联网搜索（enable_search）有什么区别？**

- **夸克搜索插件**：模型直接调用插件执行搜索，将搜索结果以文本形式返回，可直接用于生成最终输出。
- **联网搜索（enable_search）**：同样基于夸克搜索，但模型仅利用互联网信息丰富生成内容，不会完全依赖或返回互联网搜索结果。

## 来源文档

- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)




















