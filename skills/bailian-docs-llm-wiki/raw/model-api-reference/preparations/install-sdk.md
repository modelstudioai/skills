# 安装SDK

您可以使用阿里云百炼官方的 DashScope SDK（支持 Python 和 Java），也可以通过 OpenAI 官方提供的多语言 SDK（如 Python、Node.js、Java、Go）来调用阿里云百炼的 OpenAI 兼容接口。

> **说明**
>
> 如需通过 AOQ 调用 Realtime API 支持的实时语音或多模态模型，请参见[AOQ SDK 下载](../more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)。支持的模型及协议请参见[模型与协议支持范围](../realtime-api-directory/realtime-api-overview.md#rtov-s02h2)。

<a id="安装sdk"></a>

<a id="75aa2ffbb2afo"></a>

## 安装SDK

<a id="sec-tabs"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

需要`python >= 3.9`。

您可以通过OpenAI的Python SDK或DashScope的Python SDK来调用阿里云百炼平台上的模型。

<a id="sec-tabs-2"></a>

<a id="安装-openai-python-sdk"></a>

<a id="安装-openai-python-sdk-h4"></a>

#### 安装 OpenAI Python SDK

通过运行以下命令安装或升级 OpenAI Python SDK：

<a id="code-block"></a>

```bash
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U openai
```

当终端出现`Successfully installed ... openai-x.x.x`的提示后，表示您已经成功安装OpenAI Python SDK。

<a id="安装-dashscope-python-sdk"></a>

<a id="安装-dashscope-python-sdk-h4"></a>

#### 安装 DashScope Python SDK

通过运行以下命令安装或升级 DashScope Python SDK：

<a id="code-block-2"></a>

```bash
# 如果运行失败，您可以将pip替换成pip3再运行
# 文档示例基于 DashScope Python SDK 2.0，需安装 2.0.1 及以上版本
pip install -U "dashscope>=2.0.1"
```

当终端出现`Successfully installed ... dashscope-x.x.x`的提示后，表示您已经成功安装DashScope Python SDK。

> **说明**
>
> 本文档中的 Python SDK 示例均基于 DashScope Python SDK 2.0 编写，请确保安装 2.0.1 及以上版本。已使用 1.x 版本的存量项目可以继续运行（1.x 与 2.0 同包并存），迁移到 2.0 的方式请参见各示例代码。

<a id="java"></a>

<a id="java-h4"></a>

#### Java

<a id="sec-tabs-3"></a>

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

在项目中添加 [DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java) 依赖，并将 `the-latest-version` 替换为最新的版本号。

<a id="2a4ae7065aqql"></a>

### Gradle

<a id="code-block-3"></a>

```groovy
dependencies {
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
}
```

<a id="388a11b5c1ws1"></a>

### Maven

<a id="code-block-4"></a>

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>the-latest-version</version>
</dependency>
```

<a id="openai"></a>

<a id="openai-h4"></a>

#### OpenAI

在项目中添加 [OpenAI Java SDK](https://github.com/openai/openai-java?tab=readme-ov-file#openai-java-api-library) 依赖，并将 `the-latest-version` 替换为最新的版本号。（推荐设置为`3.5.0`）

需要`Java8 或更高版本`。

<a id="aabcb504d1u08"></a>

### Gradle

<a id="code-block-5"></a>

```groovy
dependencies {
    implementation("com.openai:openai-java:the-latest-version")
}
```

<a id="2d04e8a81bsn1"></a>

### Maven

<a id="code-block-6"></a>

```xml
<dependency>
  <groupId>com.openai</groupId>
  <artifactId>openai-java</artifactId>
  <version>the-latest-version</version>
</dependency>
```

<a id="node-js"></a>

<a id="node-js-h4"></a>

#### Node.js

<a id="sec-tabs-4"></a>

<a id="openai-2"></a>

<a id="openai-2-h4"></a>

#### OpenAI

您可以在终端运行以下命令：

<a id="code-block-7"></a>

```bash
npm install --save openai
# 或者
yarn add openai
```

> **说明**
>
> 如果安装失败，您可以通过配置镜像源的方法来完成安装，如：
>
> <a id="code-block-8"></a>
>
> ```bash
> npm config set registry https://registry.npmmirror.com/
> ```
>
> 配置镜像源后，您可以重新运行安装SDK的命令。

当终端出现`added xx package in xxs`的提示后，表示您已经成功安装OpenAI SDK。您可以使用`npm list openai`查询具体版本信息。

<a id="go"></a>

<a id="go-h4"></a>

#### Go

<a id="sec-tabs-5"></a>

<a id="openai-3"></a>

<a id="openai-3-h4"></a>

#### OpenAI

OpenAI 提供了[Go 语言的 SDK](https://github.com/openai/openai-go#openai-go-api-library)（需要 `Go 1.22+`），您可以在项目目录下通过以下命令来安装：

<a id="code-block-9"></a>

```go
go get 'github.com/openai/openai-go/v3'
```

或者设置固定的版本进行安装：

<a id="code-block-10"></a>

```go
go get -u 'github.com/openai/openai-go/v3@v3.8.1'
```

> 如访问服务器超时，可设置阿里云镜像代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`

在代码中使用以下命令进行导入：

<a id="code-block-11"></a>

```bash
import (
	"github.com/openai/openai-go/v3" // imported as openai
)
```

<a id="后续步骤"></a>

<a id="1d2281f6d0inh"></a>

## 后续步骤

成功完成 SDK 的安装后，您可以：

-   查阅百炼控制台选择适合您业务场景的模型。
-   使用[文本生成模型](../qwen-api-reference.md)、[图像生成模型](../image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)、[视频生成模型](../../_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)、[语音合成模型](../../_short/cosyvoice-websocket-sdk-python-47e109e34183e539.md#model-cosyvoice)、[语音识别模型](../../_short/realtime-websocket-python-sdk-paraformer-48f2eb5035b28f23.md)、[向量模型](../vector-and-sort/general-text-vector/text-embedding-synchronous-api.md)、[排序模型](../vector-and-sort/rerank-model/text-rerank-api.md)开始构建您的应用。
-   了解 [与 OpenAI API 的兼容性详情](../toolkits-and-frameworks/compatibility-of-openai-with-dashscope.md)。
