# SDK 接入

SDK 接入是指通过阿里云百炼提供的官方 SDK 或 OpenAI 兼容 SDK，将百炼的大模型推理、应用调用、向量化排序、实时[多模态](multimodal.md)交互等能力集成到业务代码中的过程。百炼支持 Python、Java、Node.js、Go 等多语言接入路径，统一以 API Key 鉴权。

## 接入路径

百炼提供两条主流接入路径，开发者可按语言栈与场景选择：

- **阿里云官方 DashScope SDK**：覆盖 Python、Java，原生封装百炼协议，支持模型调用、应用调用、向量化、排序、实时[多模态](multimodal.md)等全部能力。Java 版本建议 >= 2.12.0。
- **OpenAI 多语言 SDK**：通过百炼的 OpenAI 兼容接口接入，覆盖 Python、Java、Node.js、Go 等。开发者通常只需调整 `api_key`、`base_url`、`model` 三项即可复用现有 OpenAI 代码与生态工具，迁移成本最低。

> Qwen-Audio 不支持 OpenAI 兼容协议，仅支持 DashScope 协议；如需调用 Qwen-Audio，必须使用 DashScope SDK。

## 前置准备

1. **获取 API Key**：在百炼控制台密钥管理页面创建。按量付费 Key 新格式以 `sk-ws` 开头，旧 `sk-` 开头 Key 可继续使用。Token Plan 与 Coding Plan 使用 `sk-sp-` 开头的专属 Key。
2. **配置环境变量**：将 API Key 写入 `DASHSCOPE_API_KEY`，避免硬编码泄露。SDK 会自动读取该变量。
3. **安装对应语言 SDK**：按下方安装方式引入依赖。
4. **（应用调用场景）获取应用 ID**：在应用管理页面创建智能体应用或工作流应用，复制 `APP_ID`。若应用位于子业务空间，还需获取 `WORKSPACE_ID`。

## 安装方式

### Python

需 Python >= 3.8（LlamaIndex 框架需 3.9+）。

```
# OpenAI Python SDK
pip install -U openai

# DashScope Python SDK
pip install -U dashscope
```

### Java

- **DashScope Java SDK**：通过 Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`，应用调用建议版本 >= 2.12.0。
- **OpenAI Java SDK**：需 Java 8+，引入 `com.openai:openai-java`（推荐 3.5.0 及以上）。
- **Spring AI Alibaba**：需 Spring Boot 3.x、JDK 17+，在 `pom.xml` 添加 `spring-ai-alibaba-starter-dashscope`（示例版本 `1.0.0.2`）。

### Node.js

```
npm install --save openai
# 或
yarn add openai
```

安装失败可临时切换镜像源：`npm config set registry https://registry.npmmirror.com/`。应用调用场景也可直接使用 `axios` 发起 HTTP 请求。

### Go

需 Go 1.22+，使用 OpenAI Go SDK：

```
go get 'github.com/openai/openai-go/v3'
```

访问超时可设置阿里云镜像代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 关键配置

无论使用哪种 SDK，迁移到百炼时都需要替换以下三项：

- **api_key**：百炼 API Key，建议通过 `DASHSCOPE_API_KEY` 环境变量注入。新加坡与北京地域的 Key 不互通，切换地域需同步更换。
- **base_url**：推荐使用业务空间专属域名，格式为 `https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`。弗吉尼亚地域使用固定域名 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`，不带 `{WorkspaceId}`。
- **model**：替换为百炼各接口支持的模型名称清单中的值。

| 地域 | base_url（SDK 配置） |
| --- | --- |
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

## 典型调用示例

### 模型调用（OpenAI 兼容）

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

completion = client.chat.completions.create(
    model="qwen-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(completion.choices[0].message.content)
```

### 应用调用（DashScope SDK）

智能体应用与工作流应用调用方式一致，均通过 `Application.call` / `POST /apps/{app_id}/completion` 触发：

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)

if response.status_code != HTTPStatus.OK:
    print(f'request_id={response.request_id}, code={response.status_code}, message={response.message}')
else:
    print(response.output.text)
```

工作流应用支持多轮对话：使用 `session_id` 由云端托管历史（有效期 1 小时，最多 50 轮），或自行维护 `messages` 数组（推荐，控制更灵活）。若同时传 `session_id` 与 `messages`，系统优先使用 `messages`。

### 实时[多模态](multimodal.md)交互

Qwen-Omni-Realtime 通过 WebSocket 长连接接入，北京地域地址为 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`，新加坡为 `wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`。会话通过 `session.turn_detection` 切换 VAD 自动检测与 Manual 手动控制两种模式，提供 Python/Java SDK。

## 框架集成

- **LlamaIndex（Python 3.9+）**：将本地文件上传到百炼构建云端知识库，再基于检索引擎构建 RAG 应用。使用百炼云端智能文档切分与官方向量模型，不支持自定义切分与嵌入模型。关键参数包括 `similarity_top_k`、`similarity_cutoff`、`top_n`，可通过 `SimilarityPostprocessor`、`DashScopeRerank` 等 `node_postprocessors` 做后处理。
- **Spring AI Alibaba（Java，Spring Boot 3.x，JDK 17+）**：集成百炼智能体应用/工作流应用（流式与非流式）并检索百炼知识库。仅支持智能体应用与工作流应用两类。环境变量约定：应用集成用 `DASHSCOPE_API_KEY`、`APP_ID`、`WORKSPACE_ID`；知识库检索用 `AI_DASHSCOPE_API_KEY`、`AI_DASHSCOPE_WORKSPACE_ID`。关键是 `application.yml` 中 `${...}` 占位符与实际变量名保持一致。

## 安全与配额

- API Key 无失效日期，手动删除后即失效；RAM 用户被禁用或删除后，其创建的 API Key 全部失效。
- 不可信环境（浏览器、移动 App）应通过后端调用令牌接口生成临时 API Key 下发客户端，默认有效期 60 秒，可通过 `expire_in_seconds` 设置（范围 [1, 1800] 秒）。临时 Key 继承生成它的永久 Key 全部权限，无法进一步收窄，且必须与永久 Key 属同一地域。
- 单个主账号在华北2/新加坡/日本/德国地域每个地域最多 50 个 API Key；弗吉尼亚地域每个归属账号最多 20 个。
- 异步任务管理接口（图像生成、视频生成等）限流 20 QPS，任务结果通常保留 24 小时；高并发或对实时性要求高的场景建议接入 EventBridge 事件通知，避免轮询触发限流。

## 常见排查

- `echo` 能读到环境变量但代码仍报找不到 API Key：常见于只设了临时变量而 IDE/应用未重启加载，或通过 `systemd`/`supervisord` 启动的服务未在服务配置中显式添加环境变量，或使用 `sudo` 运行脚本未继承用户环境变量（改用 `sudo -E`）。
- 切换地域调用失败：各地域 API Key 不互通，需同步更换对应地域的 Key 与 base_url。
- 三方直供模型调用失败：仅在中国站的中国内地地域可用，调用前需先在百炼控制台开通对应服务。

## 关联主题页

- [preparations](../api/preparations.md)
- [frameworks](../api/frameworks.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more about models](../api/more-about-models.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)


