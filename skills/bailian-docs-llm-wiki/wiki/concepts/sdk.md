# 软件开发工具包

软件开发工具包（SDK，Software Development Kit）是百炼平台为开发者提供的封装库，屏蔽底层 HTTP 接口与鉴权细节，使开发者能在 Python、Java、Node.js、Go 等语言中通过少量代码即可调用大模型、应用与实时多模态能力。SDK 通常随官方迭代持续升级，建议通过包管理器保持最新版本以获得最新功能与稳定性修复。

## 接入路径

百炼提供两条接入路径，开发者可按工程栈与迁移成本选择：

1. **阿里云官方 DashScope SDK**：当前仅覆盖 Python 与 Java，封装了百炼原生协议（含智能体/工作流应用调用、异步任务管理、实时多模态交互等能力），适合需要使用百炼独有特性（如 Qwen-Audio、Omni Realtime）的场景。
2. **OpenAI 兼容 SDK**：通过 OpenAI 多语言 SDK（Python/Java/Node.js/Go）调用百炼的 OpenAI 兼容接口，只需调整 `api_key`、`base_url`、`model` 三处参数即可复用现有 OpenAI 代码与生态工具，迁移成本最低。

## 语言与版本要求

| 语言 | DashScope SDK | OpenAI 兼容 SDK |
| --- | --- | --- |
| Python | `pip install -U dashscope`，需 Python ≥ 3.8 | `pip install -U openai` |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`（建议 ≥ 2.12.0） | 引入 `com.openai:openai-java`，需 Java 8+，推荐 3.5.0+ |
| Node.js | 暂无官方 DashScope SDK，可改用 HTTP/`axios` 或 OpenAI SDK | `npm install --save openai` |
| Go | 暂无官方 DashScope SDK | 需 Go 1.22+，`go get github.com/openai/openai-go/v3` |

安装失败时可临时切换镜像源：Python 用国内 PyPI 镜像；Node.js 执行 `npm config set registry https://registry.npmmirror.com/`；Go 执行 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 鉴权与配置

- **API Key 注入**：所有 SDK 均读取环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码密钥。临时 API Key（有效期 1–1800 秒，前缀 `st-`）适用于浏览器、移动 App 等不可信环境。
- **base_url**：使用业务空间专属域名 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`，新加坡地域从旧域名 `dashscope-intl.aliyuncs.com` 迁移至专属域名可获得更好性能与稳定性；美国（弗吉尼亚）使用固定域名 `dashscope-us.aliyuncs.com`，不带 `{WorkspaceId}`。
- **子业务空间**：若应用或知识库位于子业务空间，需额外配置业务空间 ID 环境变量（如 Spring AI Alibaba 应用集成用 `WORKSPACE_ID`，知识库检索用 `AI_DASHSCOPE_WORKSPACE_ID`）。各地域 API Key 不互通，切换地域需同步更换 Key。

## 典型使用场景

- **模型调用**：通过 Chat Completions、Responses、Embeddings 等兼容接口调用 Qwen 系列及三方直供模型；OpenAI SDK 复用现有代码，DashScope SDK 适配百炼独有协议。
- **应用调用**：DashScope SDK 提供 `Application.call`（Python）/ `Application.call(param)`（Java）封装 `POST /apps/{app_id}/completion`，调用智能体应用与工作流应用方式一致，统一返回 `output.text` 供业务消费。
- **实时多模态交互**：Qwen-Omni-Realtime 通过 WebSocket 长连接驱动，Python/Java SDK 封装了客户端事件（`session.update`、`input_audio_buffer.append`、`response.create` 等）与服务端事件，支持 VAD 与 Manual 两种交互模式。
- **框架集成**：LlamaIndex（Python 3.9+）构建云端知识库 RAG 应用；Spring AI Alibaba（Spring Boot 3.x + JDK 17+）通过 `spring-ai-alibaba-starter-dashscope` 集成智能体/工作流应用并检索知识库。
- **异步任务**：图像/视频生成等耗时模型采用异步机制，SDK 封装创建任务、查询结果、取消任务接口（限流 20 QPS）；建议结合 EventBridge 事件通知避免轮询。

## 选用建议

- 已有 OpenAI 代码栈或需要多语言覆盖 → 优先 OpenAI 兼容 SDK，仅改三处参数即可迁移。
- 需要百炼独有能力（Qwen-Audio、Omni Realtime、智能体应用封装、异步任务管理）→ 选用 DashScope SDK（Python/Java）。
- 仅做一次性脚本或跨语言验证 → 可直接 HTTP 调用，跳过 SDK 安装。

> **注意**：使用 OpenAI 兼容接口时，新加坡与北京地域的 API Key 不同，切换地域需同步更换；Qwen-Audio 不支持 OpenAI 兼容协议，必须走 DashScope 协议。

## 关联主题页

- [preparations](../api/preparations.md)
- [frameworks](../api/frameworks.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [omni realtime api](../api/omni-realtime-api.md)


