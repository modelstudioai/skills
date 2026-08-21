# 安装SDK

您可以使用阿里云百炼官方的 DashScope SDK（支持 Python 和 Java），也可以通过 OpenAI 官方提供的多语言 SDK（如 Python、Node.js、Java、Go）来调用阿里云百炼的 OpenAI 兼容接口。

## **安装SDK**

## Python

需要`python >= 3.8`。

您可以通过OpenAI的Python SDK或DashScope的Python SDK来调用阿里云百炼平台上的模型。

### 安装 OpenAI Python SDK

通过运行以下命令安装或升级 OpenAI Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U openai
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917092.png)

当终端出现`Successfully installed ... openai-x.x.x`的提示后，表示您已经成功安装OpenAI Python SDK。

### 安装 DashScope Python SDK

通过运行以下命令安装或升级 DashScope Python SDK：

```
# 如果运行失败，您可以将pip替换成pip3再运行
pip install -U dashscope
```

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917093.png)

当终端出现`Successfully installed ... dashscope-x.x.x`的提示后，表示您已经成功安装DashScope Python SDK。

## Java

## DashScope

在项目中添加 [DashScope Java SDK](https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java) 依赖，并将 `the-latest-version` 替换为最新的版本号。

### **Gradle**

```
dependencies {
    implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
}
```

### **Maven**

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>the-latest-version</version>
</dependency>
```

## OpenAI

在项目中添加 [OpenAI Java SDK](https://github.com/openai/openai-java?tab=readme-ov-file#openai-java-api-library) 依赖，并将 `the-latest-version` 替换为最新的版本号。（推荐设置为`3.5.0`）

需要`Java8 或更高版本`。

### **Gradle**

```
dependencies {
    implementation("com.openai:openai-java:the-latest-version")
}
```

### **Maven**

```
<dependency>
  <groupId>com.openai</groupId>
  <artifactId>openai-java</artifactId>
  <version>the-latest-version</version>
</dependency>
```

## Node.js

## OpenAI

您可以在终端运行以下命令：

```
npm install --save openai
# 或者
yarn add openai
```

**说明**

如果安装失败，您可以通过配置镜像源的方法来完成安装，如：

```
npm config set registry https://registry.npmmirror.com/
```

配置镜像源后，您可以重新运行安装SDK的命令。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0405879371/p917106.png)

当终端出现`added xx package in xxs`的提示后，表示您已经成功安装OpenAI SDK。您可以使用`npm list openai`查询具体版本信息。

## Go

## OpenAI

OpenAI 提供了[Go 语言的 SDK](https://github.com/openai/openai-go#openai-go-api-library)（需要 `Go 1.22+`），您可以在项目目录下通过以下命令来安装：

```
go get 'github.com/openai/openai-go/v3'
```

或者设置固定的版本进行安装：

```
go get -u 'github.com/openai/openai-go/v3@v3.8.1'
```

> 如访问服务器超时，可设置阿里云镜像代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`

在代码中使用以下命令进行导入：

```
import (
	"github.com/openai/openai-go/v3" // imported as openai
)
```

## **后续步骤**

成功完成 SDK 的安装后，您可以：

-   查阅百炼控制台选择适合您业务场景的模型。
    
-   使用[文本生成模型](https://help.aliyun.com/zh/model-studio/qwen-api-reference/)、[图像生成模型](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)、[视频生成模型](https://help.aliyun.com/zh/model-studio/legacy-image-to-video-api-reference/)、[语音合成模型](https://help.aliyun.com/zh/model-studio/cosyvoice-python-sdk)、[语音识别模型](https://help.aliyun.com/zh/model-studio/paraformer-real-time-speech-recognition-python-sdk)、[向量模型](https://help.aliyun.com/zh/model-studio/text-embedding-synchronous-api)、[排序模型](https://help.aliyun.com/zh/model-studio/text-rerank-api)开始构建您的应用。
    
-   了解 [与 OpenAI API 的兼容性详情](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)。
