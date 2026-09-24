# sandbox

sandbox 是百炼平台提供的安全隔离执行环境，用于运行用户提交的代码、浏览器脚本或 AI 工具链（如 AIO），所有操作均在受限容器中完成，保障系统与数据安全。它支持按需创建、自动销毁，并可通过 SDK 或 API 集成到应用工作流中。开发者可基于预置模板快速启动，也可自定义沙箱配置。

## 支持的模型/功能

sandbox 当前支持三类执行模式：
- **Code Interpreter Sandbox**：执行 Python 代码，内置 NumPy、Pandas、Matplotlib 等科学计算库，适用于数据分析与轻量计算任务；
- **Browser Use Sandbox**：启动无头 Chromium 实例，支持 DOM 操作、表单提交、截图等网页交互能力；
- **AIO Sandbox**：集成多步 AI 工具调用链（如搜索+摘要+格式化），面向复杂自动化场景。

各模式的能力边界详见 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)、[使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

## 关键参数

创建 sandbox 实例时需指定以下关键参数（全部为必填）：
- `type`: 取值为 `"code_interpreter"`、`"browser_use"` 或 `"aio"`；
- `timeout`: 执行超时时间（秒），范围 5–300，超出后强制终止；
- `template_id`: 模板 ID，用于复用预配置的依赖、环境变量和启动命令；
- `input`: JSON 格式输入数据，结构由 `type` 决定（例如 `browser_use` 要求含 `url` 字段）。

> **注意**：`template_id` 必须通过 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) 创建并获取，直接传入未注册的 ID 将返回 404 错误。

## 使用方式

推荐通过 SDK 初始化并调用：
```python
from aliyun_bailian import SandboxClient
client = SandboxClient(api_key="YOUR_API_KEY")
resp = client.create_instance(
    type="code_interpreter",
    template_id="tmpl-py39-data-v1",
    input={"code": "print(2 + 2)"},
    timeout=60
)
print(resp.instance_id)  # 后续用此 ID 查询结果
```
完整调用流程与错误码说明见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。

## 限制和注意事项

- 单次执行最大内存为 2GB，CPU 配额为 2 vCPU，不支持 GPU；
- Code Interpreter Sandbox 禁止访问外网（除白名单域名如 `pypi.org` 用于 pip install）、禁止文件持久化写入 `/home/user` 以外路径；
- Browser Use Sandbox 默认启用 `--no-sandbox` 标志以兼容容器环境，但已通过 namespace 隔离加固，实际风险可控；
- 所有 sandbox 实例在执行完成后 5 分钟内自动销毁，无法手动保留；若需长期调试，请使用 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 中描述的本地开发模式。

> **注意**：文档 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 中提及“支持 WebSocket 实时日志流”，但当前 SDK v2.3.0 仅支持轮询 `get_result()` 获取最终输出，该功能尚未上线，属过时描述。

## 来源文档

- [Sandbox](../../raw/application-user-guide/sandbox.md)


