# plug in

插件是百炼平台用于拓展大模型能力的工具集合，旨在弥补模型在实时信息获取、复杂计算和代码执行等方面的局限性。开发者可将官方、第三方或自定义 API 封装为插件绑定至应用，使大模型根据用户意图自动调度工具、合并返回结果并生成最终答复。完整架构与调用链路说明请参考[插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)。

## 支持的模型与功能类型
- **支持模型**：通义千问-Turbo (`qwen-turbo`)、Plus (`qwen-plus`)、Max (`qwen-max`)、VL-Max (`qwen-vl-max`)、VL-Plus (`qwen-vl-plus`)。
- **插件分类**：
  - **官方插件**：平台预置（如 `calculator`、`code_interpreter`、`quark_search`、`text_to_image` 等），开箱即用，无需手动配置参数。详细说明与开通条件见[官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)。
  - **三方插件**：覆盖商业服务、图像视频、学习教育等场景，经效果验证，开通后可直接调用。
  - **自定义插件**：支持手动创建或从云市场导入 API，适配个性化业务逻辑。配置规范与调试流程见[自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)。

## 关键参数与配置
- **工具标识 (`Tool ID`)**：唯一标识插件内的具体 API。通过 API 调用时必须准确传入该 ID。
- **鉴权机制**：
  - **位置**：Header（默认字段 `Authorization`）或 Query（需指定参数名）。
  - **类型**：`basic`、`bearer`（自动追加前缀）、`appcode`（自动追加前缀）。
  - **级别**：服务级鉴权（静态 Token）与用户级鉴权（会话前动态传入）。
- **参数映射**：
  - **入参配置**：支持 `大模型识别`（模型从对话提取值）或 `业务透传`（通过 SDK/HTTP 请求的 `biz_params` 或 `user_defined_params` 显式传递）。
  - **出参配置**：模型依据出参结构过滤和重组 API 响应。支持 `Object` 嵌套，但子属性严禁为空。
- **请求规范**：支持 `GET`/`POST`，编码格式支持 `application/json` 与 `application/x-www-form-urlencoded`。
  > **注意**：`GET` 请求的输入参数不支持 `Object` 类型，若需传递复杂结构请改用 `POST`。

## 使用方式
1. **控制台接入**：
   - 在**插件市场**选择目标工具，添加至 `[[智能体应用]]`（单应用最多绑定 10 个工具，且官方插件需与应用位于同一业务空间）。
   - 将自定义插件发布为 `[[MCP服务]]` 后，在智能体编排页的 MCP 区块中挂载。
   - 在 `[[工作流应用]]` 中作为独立节点按预设编排执行，而非依赖模型自主规划。
2. **API 接入**：
   - **Assistant API**：在请求体 `tools` 字段中声明工具 ID，模型自动完成路由、执行与上下文拼接。
   - **应用直调 API**：若插件配置了用户级鉴权或业务透传入参，需在调用请求中通过 `biz_params` 传递对应键值对。

## 限制与注意事项
- **权限依赖**：首次访问插件页面或从云市场导入时，需完成 `AliyunServiceRoleForSFMAccessCloudAPI` 角色授权。RAM 用户默认无创建服务关联角色权限，需主账号授予包含 `ram:CreateServiceLinkedRole` 的策略。
- **网络与安全边界**：官方 `code_interpreter` 隔离运行，不支持外网访问及本地文件上传。`quark_search` 与 `github_search` 仅返回标题、关键词/链接与摘要，不支持直接抓取或解析目标网页详情。
- **生命周期管理**：修改插件 URL、Header 或工具参数后，必须重新在线调试并发布，仅保存草稿不会生效。删除插件/工具为不可逆操作，将直接导致关联应用失效。
- > **注意**：不同版本文档对插件挂载路径的描述存在演进差异。旧版文档推荐“直接在应用内添加工具”，新版控制台已逐步统一至 `[[MCP服务]]` 协议进行自定义插件的集成与管理。实际开发请以当前控制台界面提示为准。各模型对插件的触发策略可能存在细微差异，生产环境上线前建议进行充分边界测试。

## 来源文档

- [插件概述](../../raw/application-user-guide/plug-in/plug-in-overview.md)
- [官方和第三方插件](../../raw/application-user-guide/plug-in/plugins.md)
- [自定义插件](../../raw/application-user-guide/plug-in/custom-plug-ins.md)

