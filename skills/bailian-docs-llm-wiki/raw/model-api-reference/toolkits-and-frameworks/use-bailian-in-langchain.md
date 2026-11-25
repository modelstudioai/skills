# 在LangChain中使用阿里云百炼

本文主要介绍如何将阿里云百炼提供的模型集成到大模型应用开发框架LangChain中。

<a id="前提条件"></a>

<a id="1dd449b3bc5sf"></a>

## 前提条件

-   已开通阿里云百炼服务并获得API Key， 请参考[获取与配置 API Key](../preparations/get-api-key.md)。
-   已[将API Key配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="聊天模型-chat-model"></a>

<a id="8503294497krr"></a>

## 聊天模型（Chat Model）

<a id="sec-tabs"></a>

<a id="python"></a>

<a id="python-h4"></a>

#### Python

<a id="sec-tabs-2"></a>

<a id="openai"></a>

<a id="openai-h4"></a>

#### OpenAI

只支持阿里云百炼的部分模型。完整列表请参考：[OpenAI 兼容模式支持的模型列表](compatibility-of-openai-with-dashscope.md#eadfc13038jd5)。调用费用、输入输出上限等请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。

使用前需要安装以下依赖：

<a id="code-block"></a>

```bash
pip install langchain_openai
```

模型调用：

<a id="code-block-2"></a>

```python
from langchain_openai import ChatOpenAI
import os

chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus",  # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # other params...
)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"}]
response = chatLLM.invoke(messages)
print(response.model_dump_json())
```

工具调用等进阶技巧请前往 LangChain 官方的 [ChatOpenAI](https://python.langchain.com/docs/integrations/chat/openai/)。完整的 API参考文档请前往 LangChain 官方的 [ChatOpenAI API Reference](https://python.langchain.com/api_reference/openai/chat_models/langchain_openai.chat_models.base.ChatOpenAI.html)。

<a id="dashscope"></a>

<a id="dashscope-h4"></a>

#### DashScope

支持阿里云百炼所有的文本生成模型，完整列表与调用费用请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。（也支持[部署](../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)后的模型）

使用前需要安装以下依赖：

<a id="code-block-3"></a>

```bash
pip install langchain-community
pip install dashscope
```

模型调用：

<a id="code-block-4"></a>

```python
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage
import os

chatLLM = ChatTongyi(
    model="qwen-plus",   # 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    dashscope_api_key=os.getenv("DASHSCOPE_API_KEY"),
    streaming=True,
    # other params...
)
res = chatLLM.stream([HumanMessage(content="hi")], streaming=True)
for r in res:
    print("chat resp:", r.content)
```

多模态调用、工具调用等进阶技巧请前往 LangChain 官方的 [ChatTongyi](https://python.langchain.com/docs/integrations/chat/tongyi/)。完整的 API参考文档请前往 LangChain 官方的 [ChatTongyi API Reference](https://python.langchain.com/api_reference/community/chat_models/langchain_community.chat_models.tongyi.ChatTongyi.html)。

<a id="javascript"></a>

<a id="javascript-h4"></a>

#### JavaScript

<a id="sec-tabs-3"></a>

<a id="openai-2"></a>

<a id="openai-2-h4"></a>

#### OpenAI

只支持阿里云百炼的部分模型。完整列表请参考：[OpenAI 兼容模式支持的模型列表](compatibility-of-openai-with-dashscope.md#eadfc13038jd5)。调用费用、输入输出上限等请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。

使用前需要安装以下依赖：

<a id="code-block-5"></a>

```bash
npm install @langchain/openai @langchain/core
```

模型调用：

<a id="code-block-6"></a>

```javascript
import { ChatOpenAI } from "@langchain/openai";

const llm = new ChatOpenAI({
  // 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
  model: "qwen-plus",
  apiKey: process.env.DASHSCOPE_API_KEY,
  configuration: {
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    // other params...
  },
  // other params...
});

const aiMsg = await llm.invoke([
  {
    role: "system",
    content:
      "You are a helpful assistant that translates English to French. Translate the user sentence.",
  },
  {
    role: "user",
    content: "I love programming.",
  },
]);
console.log('---------------------------');
console.log(aiMsg.content);
```

工具调用等进阶技巧请前往 LangChain 官方的 [ChatOpenAI](https://js.langchain.com/docs/integrations/chat/openai/)。完整的 API参考文档请前往 LangChain 官方的 [ChatOpenAI API Reference](https://v03.api.js.langchain.com/classes/_langchain_openai.ChatOpenAI.html)。

<a id="dashscope-2"></a>

<a id="dashscope-2-h4"></a>

#### DashScope

支持阿里云百炼所有的文本生成模型，完整列表与调用费用请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。（也支持[部署](../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)后的模型）

使用前需要安装以下依赖：

<a id="code-block-7"></a>

```bash
npm install @langchain/community @langchain/core
```

模型调用：

<a id="code-block-8"></a>

```javascript
import { ChatAlibabaTongyi } from "@langchain/community/chat_models/alibaba_tongyi";
import { HumanMessage } from "@langchain/core/messages";

// Default model is qwen-plus
const qwenPlus = new ChatAlibabaTongyi({
  alibabaApiKey: process.env.DASHSCOPE_API_KEY,
  // other params...
});

// Use qwen-plus
const qwenPlus = new ChatAlibabaTongyi({
// 此处以qwen-plus为例，您可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
  model: "qwen-plus",
  temperature: 1,
  alibabaApiKey: process.env.DASHSCOPE_API_KEY,
  // other params...
});

const messages = [new HumanMessage("Hello")];

const res = await qwenTurbo.invoke(messages);

const res2 = await qwenPlus.invoke(messages);

console.log('---------------------------');
console.log(res.content);
console.log('---------------------------');
console.log(res2.content);
```

多模态调用、工具调用等进阶技巧请前往 LangChain 官方的 [ChatTongyi](https://js.langchain.com/docs/integrations/chat/alibaba_tongyi/)。完整的 API参考文档请前往 LangChain 官方的 [ChatTongyi API Reference](https://v03.api.js.langchain.com/classes/_langchain_community.chat_models_alibaba_tongyi.ChatAlibabaTongyi.html)。

<a id="java"></a>

<a id="java-h4"></a>

#### Java

> LangChain4j 1.0.0-beta3 需要 Java 17 及以上版本。使用较低版本（如 Java 11）编译时会出现 `Unsupported class file major version 61` 错误。

<a id="sec-tabs-4"></a>

<a id="openai-3"></a>

<a id="openai-3-h4"></a>

#### OpenAI

只支持阿里云百炼的部分模型。完整列表请参考：[OpenAI 兼容模式支持的模型列表](compatibility-of-openai-with-dashscope.md#eadfc13038jd5)。调用费用、输入输出上限等请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。

借助LangChain4j开源库，您可以使用Java编码以实现相关功能。有Plain Java（纯Java）和Spring Boot这两种实现方式，更多的接口细节和代码示例，请参见[LangChain4j OpenAI官网](https://docs.langchain4j.dev/integrations/language-models/open-ai)。

<a id="sec-tabs-5"></a>

<a id="plain-java"></a>

<a id="plain-java-h4"></a>

#### Plain Java

1.  添加依赖
    
    以Maven为例，在pom.xml中添加如下依赖：
    

<a id="code-block-9"></a>

```xml
<!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-open-ai -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-open-ai</artifactId>
    <version>1.0.0-beta3</version>
</dependency>
```

2.  编写代码，调用模型

<a id="code-block-10"></a>

```java
import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;

public class LangChainOpenAITest {
    public static void main(String[] args) {
        ChatLanguageModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .modelName("qwen-plus")
                .build();

        SystemMessage systemMessage = SystemMessage.from("你是心理专家");
        UserMessage userMessage = UserMessage.from("你好");

        System.out.println(model.chat(systemMessage, userMessage).aiMessage().text());
    }
}
```

<a id="spring-boot"></a>

<a id="spring-boot-h4"></a>

#### Spring Boot

1.  添加依赖
    
    以Maven为例，在pom.xml中添加如下依赖：
    

<a id="code-block-11"></a>

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-open-ai-spring-boot-starter -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
	<artifactId>langchain4j-open-ai-spring-boot-starter</artifactId>
	<version>1.0.0-beta3</version>
    </dependency>
</dependencies>
```

2.  配置模型信息
    
    在application.properties中配置模型、端口号等信息：
    

<a id="code-block-12"></a>

```properties
langchain4j.open-ai.chat-model.api-key=${DASHSCOPE_API_KEY}
langchain4j.open-ai.chat-model.model-name=qwen-plus
langchain4j.open-ai.chat-model.base-url=https://dashscope.aliyuncs.com/compatible-mode/v1

server.port=9000
```

3.  编写代码，调用模型

<a id="code-block-13"></a>

```java
import dev.langchain4j.model.chat.ChatLanguageModel;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatLanguageModelController {
    ChatLanguageModel chatLanguageModel;

    ChatLanguageModelController(ChatLanguageModel chatLanguageModel) {
        this.chatLanguageModel = chatLanguageModel;
    }

    @GetMapping("/chat")
    public String chat(@RequestParam(value = "message", defaultValue = "你好") String message) {
        return chatLanguageModel.chat(message);
    }
}
```

<a id="dashscope-3"></a>

<a id="dashscope-3-h4"></a>

#### DashScope

支持阿里云百炼所有的文本生成模型，完整列表与调用费用请参考：[选择模型](../../model-user-guide/get-started-with-models/models.md)。（也支持[部署](../../model-user-guide/model-high-speed-inference/model-deployment-index/model-deployment-introduction.md)后的模型）

借助LangChain4j开源库，您可以使用Java编码以实现相关功能。有Plain Java（纯Java）和Spring Boot这两种实现方式，更多的接口细节和代码示例，请参见[LangChain4j DashScope官网](https://docs.langchain4j.dev/integrations/language-models/dashscope)。

<a id="sec-tabs-6"></a>

<a id="plain-java-2"></a>

<a id="plain-java-2-h4"></a>

#### Plain Java

1.  添加依赖
    
    以Maven为例，在pom.xml中添加如下依赖：
    

<a id="code-block-14"></a>

```xml
<!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-community-dashscope -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-community-dashscope</artifactId>
    <version>1.0.0-beta3</version>
</dependency>
```

2.  编写代码，调用模型

<a id="code-block-15"></a>

```java
import dev.langchain4j.community.model.dashscope.QwenChatModel;
import dev.langchain4j.community.model.dashscope.QwenStreamingChatModel;
import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.data.message.SystemMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.chat.StreamingChatLanguageModel;
import dev.langchain4j.model.chat.request.ChatRequest;
import dev.langchain4j.model.chat.response.ChatResponse;
import dev.langchain4j.model.chat.response.StreamingChatResponseHandler;

public class LangChainDashScopeTest {
    public static void main(String[] args) {
        chatLanguageModelTest();
//        streamingChatLanguageModelTest();
    }

    public static void chatLanguageModelTest() {
        ChatLanguageModel qwenModel = QwenChatModel.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .modelName("qwen-plus")
                .build();
//        System.out.println(qwenModel.chat("你好"));
        ChatRequest request = ChatRequest.builder().messages(new ChatMessage[]{SystemMessage.from("你是心理专家"), UserMessage.from("你好")}).build();
        System.out.println(qwenModel.chat(request).aiMessage().text());
    }

    public static void streamingChatLanguageModelTest() {
        StreamingChatLanguageModel model = QwenStreamingChatModel.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .modelName("qwen-plus")
                .build();
        model.chat("你好", new StreamingChatResponseHandler() {
            @Override
            public void onPartialResponse(String s) {
                System.out.println(s);
            }

            @Override
            public void onCompleteResponse(ChatResponse chatResponse) {
                System.out.println("对话结束");
                System.exit(0);
            }

            @Override
            public void onError(Throwable throwable) {
                System.out.println("出现异常");
                System.exit(0);
            }
        });
    }
}
```

<a id="spring-boot-2"></a>

<a id="spring-boot-2-h4"></a>

#### Spring Boot

1.  添加依赖
    
    以Maven为例，在pom.xml中添加如下依赖：
    

<a id="code-block-16"></a>

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>

    <!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-community-dashscope-spring-boot-starter -->
    <dependency>
        <groupId>dev.langchain4j</groupId>
	<artifactId>langchain4j-community-dashscope-spring-boot-starter</artifactId>
	<version>1.0.0-beta3</version>
    </dependency>
</dependencies>
```

2.  配置模型信息
    
    在application.properties中配置模型、端口号等信息：
    

<a id="code-block-17"></a>

```properties
langchain4j.community.dashscope.chat-model.api-key=${DASHSCOPE_API_KEY}
langchain4j.community.dashscope.chat-model.model-name=qwen-plus

server.port=9000
```

3.  编写代码，调用模型

<a id="code-block-18"></a>

```java
import dev.langchain4j.community.model.dashscope.QwenChatModel;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class QwenChatModelController {
    QwenChatModel qwenChatModel;

    QwenChatModelController(QwenChatModel qwenChatModel) {
        this.qwenChatModel = qwenChatModel;
    }

    @GetMapping("/chat")
    public String chat(@RequestParam(value = "message", defaultValue = "你好") String message) {
        return qwenChatModel.chat(message);
    }
}
```

<a id="文本嵌入模型-embedding-model"></a>

<a id="e43d66bb40rpq"></a>

## 文本嵌入模型（Embedding Model）

<a id="支持的模型"></a>

<a id="8dde9a2a902qv"></a>

#### 支持的模型：

> MTEB、CMTEB是 Embedding 模型的通用评估指标，数值越大，模型效果越好。text-embedding-v3 与 text-embedding-v4模型当前无法通过 LangChain 框架接口指定向量维度，默认采用 1024 维度作为输出向量维度值。

| 模型 | MTEB | MTEB（Retrieval task） | CMTEB | CMTEB (Retrieval task) |
| --- | --- | --- | --- | --- |
| text-embedding-v1 | 58.30 | 45.47 | 59.84 | 56.59 |
| text-embedding-v2 | 60.13 | 49.49 | 62.17 | 62.78 |
| text-embedding-v3（1024维度） | 63.39 | 55.41 | 68.92 | 73.23 |
| text-embedding-v4（1024维度） | 68.36 | 59.30 | 70.14 | 73.98 |

<a id="sec-tabs-7"></a>

<a id="python-2"></a>

<a id="python-2-h4"></a>

#### Python

<a id="sec-tabs-8"></a>

<a id="dashscope-4"></a>

<a id="dashscope-4-h4"></a>

#### DashScope

使用前需要安装以下依赖：

<a id="code-block-19"></a>

```bash
pip install langchain-community
pip install dashscope
```

模型调用：

<a id="code-block-20"></a>

```python
from langchain_community.embeddings import DashScopeEmbeddings
embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    # other params...
)

text = "This is a test document."

query_result = embeddings.embed_query(text)
print("文本向量长度：", len(query_result), sep='')

doc_results = embeddings.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?",
        "My friends call me World",
        "Hello World!"
    ])
print("文本向量数量：", len(doc_results), "，文本向量长度：", len(doc_results[0]), sep='')
```

详细介绍与更多使用方式请前往 LangChain 官方的 [DashScope Embeddings](https://python.langchain.com/docs/integrations/text_embedding/dashscope/)。完整的 API参考文档请前往 LangChain 官方的 [Embedding API Reference](https://python.langchain.com/api_reference/community/embeddings/langchain_community.embeddings.dashscope.DashScopeEmbeddings.html)。

<a id="javascript-2"></a>

<a id="javascript-2-h4"></a>

#### JavaScript

<a id="sec-tabs-9"></a>

<a id="dashscope-5"></a>

<a id="dashscope-5-h4"></a>

#### DashScope

使用前需要安装以下依赖：

<a id="code-block-21"></a>

```bash
npm install @langchain/community @langchain/core
```

模型调用：

<a id="code-block-22"></a>

```javascript
import { AlibabaTongyiEmbeddings } from "@langchain/community/embeddings/alibaba_tongyi";

const model = new AlibabaTongyiEmbeddings({
  apiKey: process.env.DASHSCOPE_API_KEY,
  modelName: "text-embedding-v4",
  // other params...
  });
const res = await model.embedQuery(
  "What would be a good company name a company that makes colorful socks?",
);
console.log('---------------------------');
console.log({ res });
```

详细介绍与更多使用方式请前往 LangChain 官方的 [DashScope Embeddings](https://js.langchain.com/docs/integrations/text_embedding/alibaba_tongyi/)。完整的 API参考文档请前往 LangChain 官方的 [Embedding API Reference](https://v03.api.js.langchain.com/classes/_langchain_community.embeddings_alibaba_tongyi.AlibabaTongyiEmbeddings.html)。

<a id="java-2"></a>

<a id="java-2-h4"></a>

#### Java

<a id="sec-tabs-10"></a>

<a id="dashscope-6"></a>

<a id="dashscope-6-h4"></a>

#### DashScope

借助LangChain4j开源库，您可以使用Java编码以实现相关功能。更多的接口细节和代码示例，请参见[LangChain4j DashScope官网](https://docs.langchain4j.dev/integrations/language-models/dashscope)。

1.  添加依赖
    
    以Maven为例，在pom.xml中添加如下依赖：
    

<a id="code-block-23"></a>

```xml
<!-- https://mvnrepository.com/artifact/dev.langchain4j/langchain4j-community-dashscope -->
<dependency>
    <groupId>dev.langchain4j</groupId>
    <artifactId>langchain4j-community-dashscope</artifactId>
    <version>1.0.0-beta3</version>
</dependency>
```

2.  编写代码，调用模型

<a id="code-block-24"></a>

```java
import dev.langchain4j.community.model.dashscope.QwenEmbeddingModel;
import dev.langchain4j.data.embedding.Embedding;

import java.util.List;

import static dev.langchain4j.data.segment.TextSegment.textSegment;
import static java.util.Arrays.asList;

public class LangChainEmbeddingsTest {
    public static void main(String[] args) {
        QwenEmbeddingModel model = QwenEmbeddingModel.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .modelName("text-embedding-v4")
                .build();

        List<Embedding> embeddings = model.embedAll(asList(textSegment("hello"), textSegment("how are you?")))
                .content();
        System.out.println(embeddings.size());
    }
}
```

<a id="重排序模型-reranker-model"></a>

<a id="510526a06d8by"></a>

## 重排序模型（Reranker Model）

<a id="支持的模型-2"></a>

<a id="dd9114527blo8"></a>

#### 支持的模型：

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>最大Document数量</strong></p></th><th><p><strong>单条最大输入Token</strong></p></th><th><p><strong>请求最大输入Token</strong></p></th><th><p><strong>语种支持</strong></p></th><th><p><strong>单价（每千Token）</strong></p></th><th><p><strong>免费额度</strong></p></th><th><p><strong>应用场景</strong></p></th></tr></thead><tbody><tr><td><p>qwen3-vl-rerank</p></td><td><p>100</p></td><td><p>8,000</p></td><td rowspan="2"><p>120,000</p></td><td><p>中、英、日、韩、法、德等33种主流语言</p></td><td><p>图片：0.0018元</p><p>文字：0.0007元</p></td><td rowspan="3"></td><td><ul><li><p>图像聚类</p></li><li><p>跨模态搜索</p></li><li><p>图片检索</p></li></ul></td></tr><tr><td><p>qwen3-rerank</p></td><td rowspan="2"><p>500</p></td><td rowspan="2"><p>4,000</p></td><td><p>中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种</p></td><td><p>0.0005元</p></td><td rowspan="2"><ul><li><p>文本语义检索</p></li><li><p>RAG应用</p></li></ul></td></tr><tr><td><p>gte-rerank-v2</p></td><td><p>30,000</p></td><td><p>中、英、日、韩、泰语、西、法、葡、德、印尼语、阿拉伯语等50余语种</p></td><td><p>0.0008元</p></td></tr></tbody></table>

<a id="sec-tabs-11"></a>

<a id="python-3"></a>

<a id="python-3-h4"></a>

#### Python

<a id="sec-tabs-12"></a>

<a id="dashscope-7"></a>

<a id="dashscope-7-h4"></a>

#### DashScope

使用前需要安装以下依赖：

<a id="code-block-25"></a>

```bash
pip install langchain-community
pip install dashscope
```

模型调用：

<a id="code-block-26"></a>

```python
from langchain_community.document_compressors.dashscope_rerank import DashScopeRerank

sequence = ["text1", "text2", "text3"]

reranker = DashScopeRerank(
    model="gte-rerank-v2",
    # other params...
)
print(reranker.rerank(documents=sequence, query="文本3", top_n=2))
```

详细介绍与更多使用方式请前往 LangChain 官方的 [DashScope Rerank](https://python.langchain.com/docs/integrations/document_transformers/dashscope_rerank/)。完整的 API参考文档请前往 LangChain 官方的 [Rerank API Reference](https://python.langchain.com/api_reference/community/document_compressors/langchain_community.document_compressors.dashscope_rerank.DashScopeRerank.html)。
