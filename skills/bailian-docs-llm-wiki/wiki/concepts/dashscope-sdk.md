# DashScope SDK

DashScope SDK 是阿里云百炼平台提供的原生开发工具包，用于通过编程方式调用百炼平台上的大模型服务和应用。SDK 封装了 DashScope API 的认证、请求构建与响应解析，支持 Python 和 Java 两种语言。

## 定位与适用场景

百炼平台同时支持 OpenAI 兼容 SDK 和 DashScope 原生 SDK 两种接入方式：

- **OpenAI 兼容 SDK**：迁移成本低，适合已有 OpenAI 代码库的场景，但功能覆盖受协议约束。
- **DashScope SDK**：功能集最完整，参数支持最丰富，适合需要使用百炼原生全部能力的场景。

当模型仅支持 DashScope 协议（如 Qwen-Audio、Qwen-Deep-Research）或需要使用原生独有参数时，必须使用 DashScope SDK。

## 在百炼平台的使用场景

### 模型 API 调用

通过 DashScope SDK 可调用百炼平台上的文本生成、图像生成、语音合成/识别、向量/排序等模型。以文本生成为例，DashScope 原生接口提供最完整的采样参数与插件支持。

### 应用调用

百炼应用（智能体、工作流）通过 DashScope SDK 的 `Application.call` 方法调用，请求发送至 `/api/v1/apps/{APP_ID}/completion` 端点。相比 OpenAI 兼容模式，DashScope 原生 API 在功能覆盖和性能方面具有优势。

### 专用模型调用

部分专用模型（如法律模型 `farui-plus`、深度研究模型 `qwen-deep-research`）仅支持或推荐通过 DashScope SDK 调用。

## 安装方式

### Python

```bash
pip install -U dashscope
```

要求 Python >= 3.8。

### Java

通过 Maven 或 Gradle 引入依赖：

```xml
<dependency>
  <groupId>com.alibaba</groupId>
  <artifactId>dashscope-sdk-java</artifactId>
</dependency>
```

建议版本 >= 2.12.0。

## 关键配置

### 认证

SDK 通过 [API Key](api-key.md) 进行鉴权，推荐将密钥配置到环境变量 `DASHSCOPE_API_KEY`，SDK 会自动读取：

```bash
export DASHSCOPE_API_KEY='your-api-key'
```

也可在调用时通过 `api_key` 参数显式传入。

### 基础端点

DashScope 原生 API 的基础域名为 `https://dashscope.aliyuncs.com`。不同地域的端点有所差异：

| 地域 | 端点 |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com` |

百炼还推出了[业务空间](workspace.md)专属域名，建议迁移以获得更好的推理性能与稳定性。

### 常用调用参数

- `model`（string，必选）：指定模型名称。
- `prompt` / `messages`（必选）：输入内容，单轮对话用 `prompt`，多轮对话用 `messages` 数组。
- `stream`（bool，可选）：是否开启流式输出。
- `api_key`（string，可选）：显式指定 [API Key](api-key.md)，优先级高于环境变量。

## 与 [OpenAI 兼容接口](openai-compatible-interface.md)的对比

| 维度 | DashScope SDK | OpenAI 兼容 SDK |
| --- | --- | --- |
| 功能完整度 | 最全，支持全部原生参数和插件 | 受 OpenAI 协议约束，部分参数不暴露 |
| 迁移成本 | 需学习 DashScope API 结构 | 改三个参数即可复用现有 OpenAI 代码 |
| 模型覆盖 | 全部百炼模型 | 大部分模型（Qwen-Audio 等除外） |
| 生态兼容 | 百炼原生 | 可复用 OpenAI 生态工具链 |

## 注意事项

- 不同地域的 [API Key](api-key.md) 不通用，切换地域时需同步更换。
- `qwen-deep-research` 当前仅支持 Python DashScope SDK，不支持 Java SDK。
- Node.js 和 Go 语言目前无 DashScope 原生 SDK，建议使用 OpenAI 兼容 SDK 或直接发起 HTTP 请求。
- 设置环境变量后需重启 IDE 或终端窗口才能生效。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [more models](../api/more-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [preparations](../api/preparations.md)


