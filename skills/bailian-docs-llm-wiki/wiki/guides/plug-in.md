# plug in

插件是百炼平台扩展大模型能力的核心机制，用于弥补大模型在实时信息获取、精确计算、外部系统交互等方面的固有局限。通过集成官方、三方或自定义插件，开发者可将特定功能（如联网搜索、代码执行、图像生成）无缝注入智能体或工作流应用中，实现复杂任务的自动化编排与执行。插件以“工具集合”形式组织，每个工具对应一个可调用的 API 接口。

## 支持的模型/功能

百炼当前支持插件调用的模型包括：`qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-max` 和 `qwen-vl-plus`。各模型对插件的兼容性可能存在差异，**实际可用性请以控制台调试结果为准**，不建议依赖文档静态声明。  
插件按来源分为三类：
- **官方插件**：预置于组件广场，开箱即用，无需配置参数。包括 `code_interpreter`（Python 代码执行）、`calculator`（复杂数学计算）、`text_to_image`（文生图）、`quark_search`（实时网络搜索）、`generate_qrcode`（二维码生成）、`github_search`（GitHub 项目检索）等。详情见 [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
- **三方插件**：来自云市场，覆盖商业服务、图像视频、教育等领域，开通后即可调用，无需手动配置输入/输出参数。
- **自定义插件**：开发者自主开发并托管的 Web API，需明确定义插件 URL、工具路径、鉴权方式及参数 Schema。完整流程详见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

> **注意**：文档 3 中列出的模型兼容性表格未说明具体插件类型支持范围，而文档 1 和文档 2 均未提及模型限制；实践中 `qwen-turbo` 对部分复杂工具（如嵌套 Object 输入）支持较弱，建议优先使用 `qwen-plus` 或 `qwen-max` 进行插件集成验证。

## 关键参数

插件配置涉及两级参数：**插件级**与**工具级**。
- **插件级参数**：
  - `插件URL`：工具路径的公共基础域名（如 `https://example.com`），必须为 HTTPS 协议。
  - `是否鉴权`：启用后需配置鉴权类型（`basic`/`bearer`/`appcode`）、位置（`Header` 或 `Query`）及 `Token`（服务级）或 `参数名`（用户级）。
- **工具级参数**（每个工具独立配置）：
  - `工具路径`：以 `/` 开头的相对路径（如 `/query`），拼接至插件 URL 构成完整请求地址。
  - `请求方法`：仅支持 `GET` 或 `POST`；**注意**：文档 1 明确指出 `GET` 请求不支持 Object 类型输入参数，而文档 2 和 3 未提及此限制，该约束以 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 为准。
  - `输入参数`：需指定 `参数名称`、`参数描述`（影响模型识别准确率）、`类型`（String/Number/Object 等）、`传参方式`（`大模型识别` 或 `业务透传`）。Object 类型子属性**不能为空**，须显式添加。
  - `输出参数`：所有字段必填，定义模型如何解析 API 返回值；嵌套层级应尽量扁平。
  - `高级配置`（可选）：提供 `Value` 示例（如 `{"city": "杭州", "date": "2025-04-25"}`），显著提升模型参数构造准确率。

## 使用方式

插件需发布为 MCP 服务后方可被应用调用：
- **控制台方式**：
  1. 在插件列表页，对目标插件单击 **发布为MCP服务**；
  2. 进入智能体应用编排页面，在 **MCP 区块** → **+** → **选择MCP服务** → 切换至 **自定义MCP** 页签，添加该服务；
  3. 若含用户级鉴权或业务透传参数，需在对话前点击配置图标（![icon](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1891396371/p905403.png)）传入 `biz_params` 或鉴权 [Token](../concepts/token.md)。
- **API 方式**：
  - 工具 ID 通过插件详情页悬浮图标复制获取；
  - 调用 Assistant API 时，在 `tools` 字段中传入工具定义，并在 `messages` 中触发调用；
  - 业务透传参数与用户级鉴权 [Token](../concepts/token.md) 必须通过 `biz_params` 字段传递，详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。

## 限制和注意事项

- **数量限制**：单个智能体应用最多关联 10 个工具（含不同插件下的工具）。
- **参数约束**：
  - `GET` 请求禁止配置 Object 类型输入参数（见 [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 错误码 130022 说明）；
  - 工具名称长度上限为 20 字符，超限时发布失败（红色计数提示 `22/20`）；
  - 输出参数定义必须完整，缺失 `参数描述` 将导致发布失败（错误码 130040）。
- **权限与授权**：
  - 主账号首次访问插件市场需授权 `AliyunServiceRoleForSFMAccessCloudAPI` 角色；
  - RAM 子账号需主账号额外授予 `ram:CreateServiceLinkedRole` 权限（策略条件中 `ram:ServiceName` 应为 `cloundapi-access.sfm.aliyuncs.com`），否则无法导入云市场插件或进入插件页面。
- **调试与发布**：工具必须经 **测试工具** 验证成功且状态为 **已发布**，才可在应用中生效；编辑后需重新测试并发布，草稿状态不可用。
- **安全提示**：自定义插件的 `插件URL` 必须为公网可访问 HTTPS 地址，且服务端需正确处理跨域（CORS）及鉴权逻辑；云市场插件的鉴权信息（AppKey/AppSecret）需妥善保管，避免泄露。

## 来源文档

- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)


