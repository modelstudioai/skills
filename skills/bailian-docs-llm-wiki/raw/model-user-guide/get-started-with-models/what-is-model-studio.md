# 模型服务概览

提供文本、视觉、语音、全模态及向量模型 API，支持在线调用、推理调度与模型训练。

## 快速开始

OpenAI/Anthropic 兼容接口调用

[获取 API Key 和 Base URL](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openai.svg)Responses

curlPythonJavaScript/TypeScriptJavaGoC#Ruby

```
curl "$OPENAI_BASE_URL/responses" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "input": "你是谁？"
  }'
```

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)
response = client.responses.create(
    model="qwen3.8-max",
    input="你是谁？",
)
print(response.output_text)
```

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: process.env.OPENAI_BASE_URL,
});
const response = await client.responses.create({
    model: "qwen3.8-max",
    input: "你是谁？",
});
console.log(response.output_text);
```

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl(System.getenv("OPENAI_BASE_URL"))
            .build();
        ResponseCreateParams params = ResponseCreateParams.builder()
            .model("qwen3.8-max")
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

```
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
        option.WithBaseURL(os.Getenv("OPENAI_BASE_URL")),
    )
    response, err := client.Responses.New(context.Background(), responses.ResponseNewParams{
        Model: "qwen3.8-max",
        Input: responses.ResponseNewParamsInputUnion{OfString: openai.String("你是谁？")},
    })
    if err != nil {
        panic(err)
    }
    fmt.Println(response.OutputText())
}
```

```
#pragma warning disable OPENAI001

using System;
using System.ClientModel;
using OpenAI.Responses;

ResponsesClient client = new(
    new ApiKeyCredential(Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")!),
    new ResponsesClientOptions
    {
        Endpoint = new Uri(Environment.GetEnvironmentVariable("OPENAI_BASE_URL"))
    });
ResponseResult response = client.CreateResponse(new CreateResponseOptions
{
    Model = "qwen3.8-max",
    InputItems = { ResponseItem.CreateUserMessageItem("你是谁？") }
});
Console.WriteLine(response.GetOutputText());
```

```
require "openai"

client = OpenAI::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: ENV.fetch("OPENAI_BASE_URL")
)
response = client.responses.create(
  model: "qwen3.8-max",
  input: "你是谁？"
)
puts response.output_text
```

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openai.svg)Chat Completions

curlPythonJavaScript/TypeScriptJavaGoC#Ruby

```
curl "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)
response = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁？"}]
)
print(response.choices[0].message.content)
```

```
import OpenAI from "openai";

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: process.env.OPENAI_BASE_URL,
});
const response = await client.chat.completions.create({
    model: "qwen3.8-max",
    messages: [{ role: "user", content: "你是谁？" }]
});
console.log(response.choices[0].message.content);
```

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletion;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl(System.getenv("OPENAI_BASE_URL"))
            .build();
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
            .model("qwen3.8-max")
            .addUserMessage("你是谁？")
            .build();
        ChatCompletion response = client.chat().completions().create(params);
        System.out.println(response.choices().get(0).message().content().orElse(""));
    }
}
```

```
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
        option.WithBaseURL(os.Getenv("OPENAI_BASE_URL")),
    )
    response, err := client.Chat.Completions.New(context.Background(), openai.ChatCompletionNewParams{
        Model: "qwen3.8-max",
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

```
using System;
using System.ClientModel;
using OpenAI;
using OpenAI.Chat;

ChatClient client = new(
    model: "qwen3.8-max",
    credential: new ApiKeyCredential(Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY")!),
    options: new OpenAIClientOptions
    {
        Endpoint = new Uri(Environment.GetEnvironmentVariable("OPENAI_BASE_URL"))
    });
ChatCompletion response = client.CompleteChat("你是谁？");
Console.WriteLine(response.Content[0].Text);
```

```
require "openai"

client = OpenAI::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: ENV.fetch("OPENAI_BASE_URL")
)
response = client.chat.completions.create(
  model: "qwen3.8-max",
  messages: [{role: "user", content: "你是谁？"}]
)
puts response.choices.first.message.content
```

![](https://unpkg.com/@lobehub/icons-static-svg@latest/icons/anthropic.svg)Messages

curlPythonJavaScript/TypeScriptJavaGoC#RubyPHP

```
curl "$ANTHROPIC_BASE_URL/v1/messages" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.8-max",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "你是谁？"}]
  }'
```

```
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["ANTHROPIC_BASE_URL"],
)
response = client.messages.create(
    model="qwen3.8-max",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你是谁？"}]
)
for block in response.content:
    if block.type == "text":
        print(block.text)
```

```
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: process.env.ANTHROPIC_BASE_URL,
});
const response = await client.messages.create({
    model: "qwen3.8-max",
    max_tokens: 1024,
    messages: [{ role: "user", content: "你是谁？" }]
});
for (const block of response.content) {
    if (block.type === "text") console.log(block.text);
}
```

```
import com.anthropic.client.AnthropicClient;
import com.anthropic.client.okhttp.AnthropicOkHttpClient;
import com.anthropic.models.messages.Message;
import com.anthropic.models.messages.MessageCreateParams;

public class Main {
    public static void main(String[] args) {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .baseUrl(System.getenv("ANTHROPIC_BASE_URL"))
            .build();
        MessageCreateParams params = MessageCreateParams.builder()
            .model("qwen3.8-max")
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

```
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
        option.WithBaseURL(os.Getenv("ANTHROPIC_BASE_URL")),
    )
    response, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
        Model: "qwen3.8-max",
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

```
using System;
using Anthropic;
using Anthropic.Models.Messages;

AnthropicClient client = new()
{
    ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY"),
    BaseUrl = Environment.GetEnvironmentVariable("ANTHROPIC_BASE_URL")
};
MessageCreateParams parameters = new()
{
    Model = "qwen3.8-max",
    MaxTokens = 1024,
    Messages = [new UserMessageParam("你是谁？")]
};
var response = await client.Messages.Create(parameters);
foreach (var block in response.Content)
{
    if (block.TryPickText(out var text)) Console.WriteLine(text.Text);
}
```

```
require "anthropic"

client = Anthropic::Client.new(
  api_key: ENV.fetch("DASHSCOPE_API_KEY"),
  base_url: ENV.fetch("ANTHROPIC_BASE_URL")
)
response = client.messages.create(
  model: "qwen3.8-max",
  max_tokens: 1024,
  messages: [{role: "user", content: "你是谁？"}]
)
response.content.each do |block|
  puts block.text if block.type == :text
end
```

```
<?php
require __DIR__ . "/vendor/autoload.php";

use Anthropic\Client;

$client = new Client(
    apiKey: getenv("DASHSCOPE_API_KEY"),
    baseUrl: getenv("ANTHROPIC_BASE_URL")
);
$response = $client->messages->create(
    model: "qwen3.8-max",
    maxTokens: 1024,
    messages: [["role" => "user", "content" => "你是谁？"]]
);
foreach ($response->content as $block) {
    if ($block->type === "text") echo $block->text . PHP_EOL;
}
```

## 模型

[查看所有模型](https://bailian.console.aliyun.com/cn-beijing/model/market)

[

**Qwen3.8-Max**

旗舰与最强效果

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-max?serviceSite=asia-pacific-china&ref=list)

[

**Qwen3.7-Plus**

均衡之选

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.7-plus?serviceSite=asia-pacific-china&ref=list)

[

**Qwen3.8-Flash**

极致速度与高性价比

](https://bailian.console.aliyun.com/cn-beijing/model/market/detail/qwen3.8-flash?serviceSite=asia-pacific-china&ref=list)

## 开始构建

[

**文本生成与视觉理解**

生成文本，理解图像与视频内容。

](raw/model-user-guide/model-experience/text-generation-model.md)[

**图像生成**

从文字描述生成图像。

](raw/model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md)[

**视频生成**

从文字或图像生成视频。

](raw/_short/wan3-video-generation-guide-0e56f533d7040652.md)[

**语音与音频**

识别、合成语音，接入实时对话。

](raw/model-user-guide/model-experience/speech-and-audio.md)[

**全模态**

结合文本、视觉与音频进行交互。

](raw/model-user-guide/model-experience/omni-modal.md)[

**向量与检索**

使用向量与重排序提升检索效果。

](raw/model-user-guide/model-experience/embedding-rerank-model.md)
