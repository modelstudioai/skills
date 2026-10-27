# DashScope SDK连接复用配置

在调用大模型服务时，高并发场景下可能会出现请求超时、资源消耗大等问题。为解决这些问题，可通过连接复用优化网络连接的使用效率。

## 连接复用

DashScope SDK 支持通过复用已有的连接来减少资源消耗，提高请求处理效率。

-   **Java SDK**：内置连接池机制，支持配置连接数、超时时间等参数，默认启用。
-   **Python SDK**：支持通过传入自定义 HTTP 客户端实现连接复用，包括同步和异步两种方式。

## Java SDK

DashScope Java SDK 内置了连接池机制，默认启用。建议您根据具体业务合理调整连接池的连接数和超时时间，优化连接复用效果。

### 配置参数说明

**参数**

**含义**

**默认值**

**单位**

**备注**

connectTimeout

建立连接的超时时间。

120

秒

在低延迟场景中，通常需要设置较短的连接超时时间，以减少等待时间，提高响应速度。

readTimeout

读取数据的超时时间。

300

秒

writeTimeout

写入数据的超时时间。

60

秒

connectionIdleTimeout

连接池中空闲连接的超时时间。

300

秒

在高并发场景下，适当延长空闲连接超时时间，有利于避免频繁创建连接，从而降低资源消耗。

connectionPoolSize

连接池中的最大连接数。

32

个

在高并发场景下：

-   连接数过低时，可能导致请求阻塞或超时，或者频繁创建连接，增加资源消耗；
    
-   连接数过高时，可能导致服务端负载过大。
    

建议根据业务需求调整配置。

maximumAsyncRequests

最大并发请求数。全局的并发请求数限制（包含所有主机）。需要小于或等于最大连接数，否则可能出现请求阻塞的情况。

32

个

maximumAsyncRequestsPerHost

单台主机的最大并发请求数。需要小于或等于最大并发请求数。

32

个

### 代码示例

运行代码前，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#fcceb7b5d2pqx)并[安装最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk#75aa2ffbb2afo)。

以下代码示例展示了如何配置连接池相关参数（如超时时间、最大连接数等），并调用大模型服务。您可以根据实际需求调整相关参数，以优化并发性能和资源利用率。

```
// 建议DashScope SDK的版本 >= 2.12.0
import java.time.Duration;
import java.util.Arrays;

import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.protocol.ConnectionConfigurations;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();

        System.out.println(userMsg.getContent());
        return gen.call(param);
    }
    public static void main(String[] args) {
        // 连接池配置
        Constants.connectionConfigurations = ConnectionConfigurations.builder()
                .connectTimeout(Duration.ofSeconds(10))  // 建立连接的超时时间, 默认 120s
                .readTimeout(Duration.ofSeconds(300)) // 读取数据的超时时间, 默认 300s
                .writeTimeout(Duration.ofSeconds(60)) // 写入数据的超时时间, 默认 60s
                .connectionIdleTimeout(Duration.ofSeconds(300)) // 连接池中空闲连接的超时时间, 默认 300s
                .connectionPoolSize(256) // 连接池中的最大连接数, 默认 32
                .maximumAsyncRequests(256)  // 最大并发请求数, 默认 32
                .maximumAsyncRequestsPerHost(256) // 单个主机的最大并发请求数, 默认 32
                .build();

        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

## Python SDK

DashScope Python SDK 支持通过传入自定义 HTTP 客户端（`httpx.Client` / `httpx.AsyncClient`）实现连接复用，提供[HTTP异步](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration#41cb49b5d22i8)（协程）和[HTTP同步](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration#21a3c6f345ipv)两种调用方式。

### HTTP异步调用方式

在异步调用场景中，您可以通过 `httpx.AsyncClient` 配合 `httpx.Limits` 实现连接复用。`httpx.Limits` 支持配置连接数限制等参数：

**参数**

**含义**

**默认值**

**备注**

max\_connections

总连接数限制

None（无限制）

控制最大连接数。在高并发场景下，适当增加此值可以提高并发能力。

max\_keepalive\_connections

保持长连接的最大数量

None（无限制）

控制连接池中保持活跃的连接数，避免对单一服务端造成过大压力。

keepalive\_expiry

长连接保活时间

5.0（秒）

空闲长连接的超时时间，超过该时长后自动关闭连接。

#### 代码示例

运行代码前，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#fcceb7b5d2pqx)并[安装最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk#75aa2ffbb2afo)。

以下代码示例展示了如何在异步场景下配置连接复用，并调用大模型服务：

```
import asyncio
import httpx
import os
import dashscope

async def main():
    # 配置连接参数
    limits = httpx.Limits(
        max_connections=100,           # 总连接数限制
        max_keepalive_connections=30,  # 保持长连接的最大数量
    )

    # 创建自定义 HTTP 客户端并传入 Client 构造
    async with httpx.AsyncClient(limits=limits) as http_client:
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
        aclient = dashscope.AsyncClient(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            http_client=http_client,  # 传入自定义 HTTP 客户端
        )
        response = await aclient.chat.completions.create(
            model='qwen-plus',
            messages=[{"role": "user", "content": '你好，请介绍一下你自己'}],
        )
        print(response)

asyncio.run(main())
```

### HTTP同步调用方式

在同步调用场景中，您可以通过 `httpx.Client` 实现连接复用。在同一个 HTTP 客户端内的多次请求会复用底层 TCP 连接，避免重复建立连接的开销。

#### 代码示例

运行代码前，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen#fcceb7b5d2pqx)并[安装最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk#75aa2ffbb2afo)。

以下代码示例展示了如何在同步场景下配置连接复用，并调用大模型服务：

```
import httpx
import os
import dashscope

# 使用 with 语句确保 HTTP 客户端正确关闭
with httpx.Client() as http_client:
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    client = dashscope.Client(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        http_client=http_client,  # 传入自定义 HTTP 客户端
    )
    response = client.chat.completions.create(
        model='qwen-plus',
        messages=[{"role": "user", "content": '你好'}],
    )
    print(response)
```

如果需要在多次调用中复用同一个 HTTP 客户端，可以采用以下方式：

```
import httpx
import os
import dashscope

# 创建 HTTP 客户端对象，并配置连接复用参数
http_client = httpx.Client(
    limits=httpx.Limits(
        max_connections=100,          # 总连接数限制
        max_keepalive_connections=30, # 保持长连接的最大数量
    ),
)

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    http_client=http_client,  # 传入自定义 HTTP 客户端
)

try:
    # 多次调用复用同一个 HTTP 客户端
    response1 = client.chat.completions.create(
        model='qwen-plus',
        messages=[{"role": "user", "content": '你好'}],
    )
    print(response1)

    response2 = client.chat.completions.create(
        model='qwen-plus',
        messages=[{"role": "user", "content": '介绍一下你自己'}],
    )
    print(response2)
finally:
    # 确保 HTTP 客户端正确关闭
    http_client.close()
```

## 最佳实践

-   **Java SDK**：根据业务并发量合理配置 `connectionPoolSize`、`maximumAsyncRequests` 等参数，避免连接数过高或过低。
-   **Python SDK**：推荐使用 `with` 语句自动管理 HTTP 客户端的生命周期，确保资源正确释放。
-   **选择合适的调用方式**：如果您的应用是异步架构（如使用 asyncio、FastAPI 等），建议使用异步调用方式；如果是传统同步架构，使用同步调用方式即可。

## 错误码

如果模型调用失败（Python SDK 会抛出 `DashScopeError` 异常，HTTP 调用返回报错信息），请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
