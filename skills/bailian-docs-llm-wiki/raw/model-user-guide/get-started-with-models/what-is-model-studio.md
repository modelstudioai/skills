# 模型服务概览

提供文本、视觉、语音、全模态及向量模型 API，支持在线调用、推理调度与模型训练。

<a id="从代码调用模型"></a>

<a id="调用前确认"></a>

<a id="模型服务"></a>

<a id="开箱即用的模型"></a>

<a id="模型调优部署和评测"></a>

<a id="模型调优-部署和评测"></a>

<a id="进阶管理"></a>

<a id="产品计费"></a>

<a id="新用户免费额度"></a>

<a id="如何支付费用"></a>

<a id="查看账单与用量"></a>

<a id="模型推理与知识库的计费区分"></a>

<a id="常见问题"></a>

<a id="应用构建"></a>

<a id="你想完成什么"></a>

<a id="开始使用阿里云百炼"></a>

<a id="开发者快速开始"></a>

<a id="overview-quickstart"></a>

## 快速开始

OpenAI/Anthropic 兼容接口调用

[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)

<a id="overview-code-example"></a>

<a id="responses"></a>

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openai.svg)Responses

<a id="overview-responses-language"></a>

curlPythonJavaScript/TypeScriptJavaGoC#Ruby

<a id="code-block"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen4-max",
    "input": "你是谁？"
  }'
```

<a id="code-block-2"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
response = client.responses.create(
    model="qwen4-max",
    input="你是谁？",
)
print(response.output_text)
```

<a id="code-block-3"></a>

```javascript
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const response = await client.responses.create({
    model: "qwen4-max",
    input: "你是谁？",
});
console.log(response.output_text);
```

<a id="code-block-4"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
            .build();
        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("qwen4-max")
            .input("你是谁？")
            .build();
        Response response = client.responses().create(params);
        response.output().stream()
            .flatMap(item -> item.message().stream())
            .flatMap(message -> message.content().stream())
            .flatMap(content -> content.outputText().stream())
            .forEach(text -> System.out.println(text.text()));
    }
}
```

<a id="code-block-5"></a>

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/option"
    "github.com/openai/openai-go/v3/responses"
)

func main() {
    client := openai.NewClient(
        option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
        option.WithBaseURL("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"),
    )
    response, err := client.Responses.New(context.Background(), responses.ResponseNewParams{
        Model: "qwen4-max",
        Input: responses.ResponseNewParamsInputUnion{OfString: openai.String("你是谁？")},
    })
    if err != nil {
        panic(err)
    }
    fmt.Println(response.OutputText())
}
```

<a id="code-block-6"></a>

```csharp
#pragma warning disable OPENAI001

using System;
using System.ClientModel;
using OpenAI.Responses;

ResponsesClient client = new(
    new ApiKeyCredential(Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")!),
    new ResponsesClientOptions
    {
        Endpoint = new Uri("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
    });
ResponseResult response = client.CreateResponse(new CreateResponseOptions
{
    Model = "qwen4-max",
    InputItems = { ResponseItem.CreateUserMessageItem("你是谁？") }
});
Console.WriteLine(response.GetOutputText());
```

<a id="code-block-7"></a>

```ruby
require "openai"

client = OpenAI::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.responses.create(
  model: "qwen4-max",
  input: "你是谁？"
)
puts response.output_text
```

<a id="chat-completions"></a>

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openai.svg)Chat Completions

<a id="overview-chat-completions-language"></a>

curlPythonJavaScript/TypeScriptJavaGoC#Ruby

<a id="code-block-8"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen4-max",
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

<a id="code-block-9"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
response = client.chat.completions.create(
    model="qwen4-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

<a id="code-block-10"></a>

```javascript
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});
const response = await client.chat.completions.create({
    model: "qwen4-max",
    messages: [{ role: "user", content: "你是谁？" }]
});
console.log(response.choices[0].message.content);
```

<a id="code-block-11"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
            .build();
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
            .model("qwen4-max")
            .addUserMessage("你是谁？")
            .build();
        ChatCompletion response = client.chat().completions().create(params);
        System.out.println(response.choices().get(0).message().content().orElse(""));
    }
}
```

<a id="code-block-12"></a>

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/option"
)

func main() {
    client := openai.NewClient(
        option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
        option.WithBaseURL("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"),
    )
    response, err := client.Chat.Completions.New(context.Background(), openai.ChatCompletionNewParams{
        Model: "qwen4-max",
        Messages: []openai.ChatCompletionMessageParamUnion{
            openai.UserMessage("你是谁？"),
        },
    })
    if err != nil {
        panic(err)
    }
    fmt.Println(response.Choices[0].Message.Content)
}
```

<a id="code-block-13"></a>

```csharp
using System;
using System.ClientModel;
using OpenAI;
using OpenAI.Chat;

ChatClient client = new(
    model: "qwen4-max",
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")!),
    options: new OpenAIClientOptions
    {
        Endpoint = new Uri("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
    });
ChatCompletion response = client.CompleteChat("你是谁？");
Console.WriteLine(response.Content[0].Text);
```

<a id="code-block-14"></a>

```ruby
require "openai"

client = OpenAI::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
  model: "qwen4-max",
  messages: [{role: "user", content: "你是谁？"}]
)
puts response.choices.first.message.content
```

<a id="messages"></a>

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/anthropic.svg)Messages

<a id="overview-messages-language"></a>

curlPythonJavaScript/TypeScriptJavaGoC#RubyPHP

<a id="code-block-15"></a>

```bash
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1/messages" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen4-max",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

<a id="code-block-16"></a>

```python
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
)
response = client.messages.create(
    model="qwen4-max",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你是谁？"}]
)
for block in response.content:
    if block.type == "text":
        print(block.text)
```

<a id="code-block-17"></a>

```javascript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic",
});
const response = await client.messages.create({
    model: "qwen4-max",
    max_tokens: 1024,
    messages: [{ role: "user", content: "你是谁？" }]
});
for (const block of response.content) {
    if (block.type === "text") console.log(block.text);
}
```

<a id="code-block-18"></a>

```java
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic")
            .build();
        MessageCreateParams params = MessageCreateParams.builder()
            .model("qwen4-max")
            .maxTokens(1024L)
            .addUserMessage("你是谁？")
            .build();
        Message response = client.messages().create(params);
        response.content().stream()
            .flatMap(block -> block.text().stream())
            .forEach(text -> System.out.println(text.text()));
    }
}
```

<a id="code-block-19"></a>

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/anthropics/anthropic-sdk-go/v2"
    "github.com/anthropics/anthropic-sdk-go/v2/option"
)

func main() {
    client := anthropic.NewClient(
        option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
        option.WithBaseURL("https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"),
    )
    response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        Model: "qwen4-max",
        MaxTokens: 1024,
        Messages: []anthropic.MessageParam{
            anthropic.NewUserMessage(anthropic.NewTextBlock("你是谁？")),
        },
    })
    if err != nil {
        panic(err)
    }
    for _, block := range response.Content {
        if block.Type == "text" {
            fmt.Println(block.Text)
        }
    }
}
```

<a id="code-block-20"></a>

```csharp
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new()
{
    ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY"),
    BaseUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
};
MessageCreateParams parameters = new()
{
    Model = "qwen4-max",
    MaxTokens = 1024,
    Messages = [new UserMessageParam("你是谁？")]
};
var response = await client.Messages.Create(parameters);
foreach (var block in response.Content)
{
    if (block.TryPickText(out var text)) Console.WriteLine(text.Text);
}
```

<a id="code-block-21"></a>

```ruby
require "anthropic"

client = Anthropic::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
)
response = client.messages.create(
  model: "qwen4-max",
  max_tokens: 1024,
  messages: [{role: "user", content: "你是谁？"}]
)
response.content.each do |block|
  puts block.text if block.type == :text
end
```

<a id="code-block-22"></a>

```php
<?php
require __DIR__ . "/vendor/autoload.php";

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("DASHSCOPE_API_KEY"),
    baseUrl: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/apps/anthropic"
);
$response = $client->messages->create(
    model: "qwen4-max",
    maxTokens: 1024,
    messages: [["role" => "user", "content" => "你是谁？"]]
);
foreach ($response->content as $block) {
    if ($block->type === "text") echo $block->text . PHP_EOL;
}
```

<a id="模型"></a>

## 模型

[查看所有模型](https://bailian.console.aliyun.com/cn-beijing/model/market)

|  |  |  |
| --- | --- | --- |
| [<br><br>![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)<br><br>**Qwen4-Max**<br><br>旗舰与最强效果<br><br><br><br><br><br>](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen4-max?serviceSite=asia-pacific-china&ref=list) | [<br><br>![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)<br><br>**Qwen3.7-Plus**<br><br>均衡之选<br><br><br><br><br><br>](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.7-plus?serviceSite=asia-pacific-china&ref=list) | [<br><br>![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/qwen-color.svg)<br><br>**Qwen3.8-Flash**<br><br>极致速度与高性价比<br><br><br><br><br><br>](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-flash?serviceSite=asia-pacific-china&ref=list) |

<a id="overview-capabilities"></a>

<a id="开始构建"></a>

## 开始构建

<a id="overview-build-paths"></a>

[

**文本生成与视觉理解**

生成文本，理解图像与视频内容









](../model-experience/text-generation-model.md)[

**图像生成**

从文字描述生成图像









](../model-experience/image-and-video-generation/image-model/text-to-image.md)[

**视频生成**

从文字或图像生成视频









](../../_short/wan3-video-generation-guide-0e56f533d7040652.md)[

**语音与音频**

识别、合成语音，接入实时对话









](../model-experience/speech-and-audio.md)[

**全模态**

结合文本、视觉与音频进行交互









](../model-experience/omni-modal.md)[

**向量与检索**

使用向量与重排序提升检索效果









](../model-experience/embedding-rerank-model.md)

<a id="模型推理"></a>

## 模型推理

[

**Prime 模式**

为对输出速度敏感的场景提供高速推理









](../model-high-speed-inference/prime-mode.md)[

**吞吐预留**

预留指定模型的推理容量，保障高峰期吞吐









](../model-high-speed-inference/tpm-reservation-index/tpm-reservation.md)[

**批量推理**

异步处理无需实时响应的大批量请求









](../model-high-speed-inference/batch-inference.md)[

**专属部署**

为高并发、低延迟场景配置专属推理服务









](../model-high-speed-inference/model-deployment-index.md)[

**智能路由**

根据请求内容自动匹配合适的模型









](../model-high-speed-inference/model-routing.md)

<a id="模型训练"></a>

## 模型训练

[

**数据管理**

管理训练集与评测集，清洗和增强数据









](../model-training/model-data-overview.md)[

**模型调优**

使用业务数据训练模型，改善特定场景的表现









](../model-training/fine-tuning.md)[

**模型评测**

评估模型表现，支持模型选型与调优验证









](../model-training/model-evaluation-introduction.md)[

**模型压缩**

量化调优后的模型，降低推理部署成本









](../model-training/model-compression-introduction.md)

<a id="overview-my-models"></a>

[

**我的模型**

管理调优及导入的模型，衔接推理部署









](../model-training/my-model-center.md)

![](data:image/png;base64,)
