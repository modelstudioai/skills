# DashScope SDK Expert

DashScope Python SDK 内置的 SDK 智能助手——只描述需求即可拿到校验过版本的可运行代码，贴报错或给文件路径即可自动诊断、修复并验证。

DashScope SDK Expert（下称 SDK Expert）是 dashscope Python SDK（≥1.27.3）内置的 SDK 智能助手 CLI。本页是通用使用指南：教怎么用 SDK Expert 开发与排障。各接口完整参数见侧栏单接口参考页，能力域见下方"覆盖能力一览"。

## 快速开始

1.  **准备 API Key 与 base\_url**：在[百炼控制台](https://bailian.console.aliyun.com)「API Key」创建 Key（`sk-` 前缀），各地域 Key 独立。配置环境变量或会话内 `/setup`：
    
    ```
    export DASHSCOPE_API_KEY=sk-xxxxxxxx
    export DASHSCOPE_HTTP_BASE_URL=https://{workspace-id}.{region}.maas.aliyuncs.com/api/v1
    ```
    
    各 region 的 base\_url 不同，域名对照见 [Base URL 总览](raw/model-user-guide/get-started-with-models/base-url.md)。
    
2.  **安装/升级 SDK**：SDK Expert 随 dashscope Python SDK 1.27.3 引入。
    
    ```
    # 如果运行失败，可以将 pip 替换成 pip3
    pip install -U dashscope
    ```
    
3.  **启动 CLI**：终端执行 `dashscope`（不带子命令）进入 SDK Expert 交互式会话；也可 `python -m dashscope.acli`（acli 即 SDK Expert 的 CLI 入口模块）。首次启动会提示下载 SDK Expert 知识包（含 api-doc/diagnose 等专项 skill）；也可手动装：
    
    ```
    dashscope
    # 或手动装 SDK Expert 知识包
    python -m dashscope.acli example download dashscope-sdk-expert
    ```
    
4.  **查看帮助**：会话中输入 `/help` 查看全部 command 与 skill。command 是会话操作（如 `/clear` `/help` `/exit`）；skill 是领域能力开关（`/skill <名称>`）。不确定就直接自然语言提问，SDK Expert 自动匹配 skill。
    
5.  **按需提问**：自然语言描述需求即可，例如：
    
    -   "用 qwen-plus 流式输出并统计 token 消耗"
    -   "这段报错 `Throttling.RateQuota` 是什么意思，怎么修？"
    -   "读 gen.py 诊断 InvalidParameter 报错的根因"
    
    也支持 Ctrl+T 语音输入、`@文件路径` 贴附文件让 SDK Expert 直接读取、↑ 翻历史命令。
    

**重要**SDK Expert 会校验本机 dashscope 版本，过旧会提醒先 `pip install -U dashscope` 升级。

**重要**多模态或通义以外模型：`pip install -U 'dashscope[acli-all]'`。

## 覆盖能力一览

装 SDK Expert 知识包后，可用以下 skill（`/skill` 查看全部）：

skill

用途

示例

api-doc

查 SDK API 文档

`/skill api-doc Generation`

sdk-example

生成示例代码

`/skill sdk-example TextEmbedding`

error-code

错误码含义与修复建议

`/skill error-code InvalidApiKey`

diagnose

读取代码文件，定位根因

`/skill diagnose ./my_code.py`

explain-code

解释指定代码逻辑

`/skill explain-code <代码>`

translate

多语言翻译

`/skill translate en 你好世界`

update-sdk

更新知识库索引

`/skill update-sdk <sdk路径>`

SDK Expert 覆盖 DashScope SDK 全部能力域——文本生成、多模态、语音、检索、微调与部署、Agent 等。查某接口文档/示例用 `api-doc`/`sdk-example`，生成代码或排障直接自然语言提问即可。

**说明**SDK Expert 是完整 agentic CLI，还支持多 Agent 协作、MCP（Model Context Protocol，外部工具接入标准）server、定时任务（`/cron`）、审计（`/audit`）、会话压缩与历史（`/compress`、`/history`）等。会话内常用 `/` 命令按类别分组：

-   **会话管理**：`/help` `/clear` `/info` `/stats` `/setup` `/exit` `/feedback`
-   **能力与工具**：`/skill` `/mcp` `/voice` `/tts` `/copy`
-   **历史与审计**：`/history` `/compress` `/cron` `/audit` `/dev` `/example`

完整列表以 `/help` 输出为准。

## 最佳实践一：只提需求，不读文档，直接产出可运行代码

**痛点**：SDK 接口多、版本迭代快，开发者常需翻文档确认参数名、输入格式、模型清单。

**做法**：描述需求给 SDK Expert，SDK Expert 会自动完成：

1.  匹配内置 SDK 知识库（模型列表/参数/输入输出结构/错误码）
2.  校验本机 SDK 版本（不一致会提醒升级）
3.  生成可运行代码并实际执行，展示输出

**示例对话**：

```
> 用 qwen-plus 流式输出一段话，并统计 token 消耗

SDK Expert：
1. 匹配 api-doc/sdk-example skill，核对本机 dashscope 版本
2. 生成脚本并执行，展示流式输出与 token 统计（见下）
```
```
import os, dashscope
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
for chunk in dashscope.Generation.call(
    model="qwen-plus",
    messages=[{"role": "user", "content": "写一首关于秋天的诗"}],
    result_format="message", stream=True, incremental_output=True,
):
    if chunk.status_code == 200:
        print(chunk.output.choices[0].message.content, end="", flush=True)
# 最后一个 chunk 含 usage（input/output tokens）
```
```
秋风扫落叶...（流式逐字输出）
usage: input=10 output=52
```

**小技巧**：

-   指定语言/框架：如"封装成 FastAPI 接口"、"用 async/await 异步调用"
-   指定版本："我们用 dashscope 1.20.x，这个参数支持吗？"——SDK Expert 核对安装版本后回答
-   追问细节："参数取值范围？""还有哪些可选模型？"

## 最佳实践二：排查问题，让它自动定位并修复 Bug

**痛点**：调用报错时错误码含义不明、堆栈指向 SDK 内部，难判是代码还是参数问题。

**做法**（三条路径，按场景选用）：

1.  **贴错误码/报错信息** → `/skill error-code <错误码>`（如 `/skill error-code Throttling.RateQuota`）→ SDK Expert 输出错误码含义 + 可执行修复建议（调并发/改参数/申请配额）+ 可选代码片段。
2.  **给出问题代码文件路径** → `/skill diagnose <文件路径>`（如 `/skill diagnose gen.py`）→ SDK Expert 读取源码，对照常见根因（混用旧版 prompt 格式、messages 结构错误、api\_key/workspace 未配置、异步任务未正确轮询）输出疑似根因 + 建议修改点。
3.  **自动修复闭环** → `/skill diagnose` 定位根因 → 生成 diff 预览供你确认 → 确认后 SDK Expert 应用修改并重跑脚本验证 → 形成"读取 → 诊断 → 修复 → 验证"流程。SDK Expert 改文件前会征求确认，可回滚。

**示例对话**：

```
> 运行 gen.py 报 InvalidParameter: url error，帮我修

SDK Expert：
1. /skill diagnose gen.py → 定位 image_url 传了本地路径
2. 生成 diff 供确认（见下）
3. 确认后应用，重跑脚本，返回 200
```
```
- image_url="/tmp/photo.jpg"
+ image_url="https://example.com/photo.jpg"
```

**小技巧**：

-   报错附 `request_id` 便于对应服务端日志（`request_id` 在响应体 `response.request_id` 字段或报错对象属性中）
-   复杂问题先让 SDK Expert "解释这段代码逻辑"（`/skill explain-code`）确认理解一致再修复
-   SDK 本身缺陷或未满足需求时，可到 [GitHub](https://github.com/dashscope/dashscope-sdk-python/issues) 提 Issue 反馈

## 常见疑问

**SDK Expert 会擅自改我的源码吗？** 不会。改文件前 SDK Expert 会生成 diff 预览征求你确认，确认后才应用，支持回滚。

**离线能用吗？** 不能。SDK Expert 需调用模型推理（消耗 token，按百炼计费），必须联网 + 配置有效的 API Key。

**生成的代码能直接跑生产吗？** SDK Expert 生成校验过版本的可运行代码，但生产前需自行审查配额、并发、错误处理与敏感信息。

**能生成非 Python 代码吗？** 能生成其他语言的代码文本，但不校验非 Python SDK 版本（版本体系不同，需自行核对）。

**我的代码会被上传吗？** 诊断（`/skill diagnose`）或贴附代码时，代码内容会发给模型推理，敏感数据请注意。
