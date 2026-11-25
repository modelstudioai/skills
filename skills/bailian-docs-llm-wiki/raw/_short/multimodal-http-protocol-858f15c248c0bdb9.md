# HTTP协议

本文介绍基于 HTTP 协议的多模态交互 API。

多模态交互开发套件中的HTTP协议支持使用纯文本或图片发起**http-sse**请求，获取大模型处理结果。

> **重要**
>
> 使用HTTP协议接入多模态交互开发套件，不支持以下功能：
>
> -   不支持纯视觉应用
>     
> -   不支持使用以下Agent：
>     
>     视频通话、极速视频/语音通话、语音翻译、新闻电台、儿童故事、录音纪要、主动导览、主动陪伴。

<a id="前提条件"></a>

<a id="fd568ddbe20oa"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 对于客户端调用的场景，在客户端处理API Key有安全风险，建议从服务端用API Key获取临时鉴权Token，再把Token下发给客户端使用。具体方法请参考：[生成临时API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)。

<a id="服务地址"></a>

<a id="aded0e18ae7we"></a>

## 服务地址

<a id="code-block"></a>

```text
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

> **说明**
>
> 发起HTTP请求时，请求的header里要有**X-DashScope-SSE: enable**

<a id="鉴权"></a>

<a id="f33e29403a9i8"></a>

## 鉴权

需要在发起HTTP请求时，把API Key放在HTTP Header里（需要将your\_api\_key替换为真实的API Key）：

<a id="code-block-2"></a>

```text
"Authorization": "Bearer your_api_key"
```

<a id="消息类型"></a>

<a id="e3a7c0fbdfzuh"></a>

## 消息类型

当前HTTP协议仅包含文本消息。文本消息是JSON格式字符串。

<a id="发起请求"></a>

<a id="48b2452228o2z"></a>

### 发起请求

<a id="request-input-message"></a>

<a id="adbc2405d6mz1"></a>

#### Request - Input Message

发起HTTP请求。

<table><tbody><tr><td><p><strong>一级参数</strong></p></td><td><p><strong>二级参数</strong></p></td><td><p><strong>类型</strong></p></td><td><p><strong>是否必选</strong></p></td><td><p><strong>说明</strong></p></td></tr><tr><td><p>model</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>阿里云百炼模型名称，固定为&quot;multimodal-dialog&quot;，请直接复制使用</p></td></tr><tr><td rowspan="4"><p>input</p></td><td><p>directive</p></td><td><p>string</p></td><td><p>是</p></td><td><p>指令名称：<strong>Request</strong></p></td></tr><tr><td><p>app_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>客户创建的应用ID（<a href="../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#2612f896detsz">获取APP ID</a>），可在<strong>多模态交互开发套件</strong>控制台的“我的应用”页面查看</p></td></tr><tr><td><p>dialog_id</p></td><td><p>string</p></td><td><p>否</p></td><td><p>对话id，默认不填时是新对话，服务端会自动生成并在返回结果中下发，格式示例：&quot;12345678-1234-1234-1234-1234567890ab&quot;，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog_id在这里传入</p></td></tr><tr><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>要处理的文本。</p><ul><li><p>调用部分agent时，text可以是&quot;&quot;空字符串，服务端需要使用parameters中的images或者biz_params参数处理。具体参考<a href="official-agent-297b22931e69e622.md">调用官方Agent</a>。</p></li></ul></td></tr><tr><td rowspan="4"><p>parameters</p></td><td><p>client_info</p></td><td><p>object</p></td><td><p>是</p></td><td><p>参数说明参考下方 <a href="multimodal-http-protocol-858f15c248c0bdb9.md">parameters.client_info的参数说明</a>表格</p></td></tr><tr><td><p>history</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>客户自己组织的问答历史，会覆盖服务内默认维护的问答历史，影响后续所有问答。</p></td></tr><tr><td><p>images</p></td><td><p>list[]</p></td><td><p>否</p></td><td><p>需要分析的图片数据，仅多模态应用可支持图片问答，参数说明参考下方<a href="multimodal-http-protocol-858f15c248c0bdb9.md">parameters.images的参数说明</a>表格</p></td></tr><tr><td><p>biz_params</p></td><td><p>object</p></td><td><p>否</p></td><td><p>按需配置，参数说明参考下方<a href="multimodal-http-protocol-858f15c248c0bdb9.md">parameters.biz_params的参数说明</a>表格</p></td></tr></tbody></table>

**parameters.client\_info**的参数说明如下：

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>user_id</p></td><td></td><td><p>string</p></td><td><p>是</p></td><td><p>终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。</p></td></tr><tr><td><p>device</p></td><td><p>uuid</p></td><td><p>string</p></td><td><p>否</p></td><td><p>客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user_id相同。</p></td></tr><tr><td><p>network</p></td><td><p>ip</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方公网IP</p></td></tr><tr><td rowspan="3"><p>location</p></td><td><p>latitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方纬度信息，在需要客户端精确位置的业务场景提交</p></td></tr><tr><td><p>longitude</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方经度信息，在需要客户端精确位置的业务场景提交</p></td></tr><tr><td><p>city_name</p></td><td><p>string</p></td><td><p>否</p></td><td><p>调用方所在城市，指明客户端粗略位置</p></td></tr></tbody></table>

**parameters.history**内每条记录的参数说明如下：

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| role | string | 是 | 本记录是哪个角色说的，只支持user, assistant两种。<br><br>注意：不支持设为system |
| content | string | 是 | 具体文本内容 |

**parameters.images**内每个图片的参数说明如下：

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>type</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片类型，支持两种：base64/url</p></td></tr><tr><td><p>value</p></td><td><p>string</p></td><td><p>是</p></td><td><p>图片内容。</p><ul><li><p>当type为base64时，这里是图片的base64字符串。</p></li><li><p>当type为url时，这里是图片的url地址。</p></li></ul></td></tr></tbody></table>

**parameters.biz\_params**的参数说明如下：

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| user\_defined\_params | json object | 否 | 需要透传给agent的参数，各类agent传递的参数参考[调用官方Agent](official-agent-297b22931e69e622.md)文档说明 |
| user\_prompt\_params | json object | 否 | 用于设置用户自定义prompt变量，由用户自定义设置json中的key和value。管控台上配置自定义prompt变量的方法参考[应用配置-提示词](multimodal-app-configuration-8919f99b339e17da.md#cbbc5f73caixw) |
| user\_query\_params | json object | 否 | 用于设置用户自定义对话变量，由用户自定义设置json中的key和value。管控台上配置自定义对话变量的方法参考[应用配置-对话变量](multimodal-app-configuration-8919f99b339e17da.md#6abc9330e2yx9) |

<a id="ec6f61532etc8"></a>

##### 示例如下

<a id="code-block-3"></a>

```json
{
    "model": "multimodal-dialog",
    "input": {
        "directive": "Request",
        "app_id": "****************",
        "text":"你好，北京今天的天气怎么样？"
    },
    "parameters": {
        "client_info": {
            "user_id": "bi**********07",
            "device":{
              "uuid": "432k*********k449"
            },
            "network":{
              "ip": "x.x.x.x"
            },
            "location":{
               "city_name": "北京市"
            }
        },
        "images":[{
              "type": "base64",
              "value": "base64String"
          }]
    }
}
```

<a id="文本下发事件"></a>

<a id="588b9df38azvr"></a>

### 文本下发事件

<a id="respondingcontent-output-message"></a>

<a id="3b421d978fco5"></a>

#### RespondingContent - Output Message

<table><thead><tr><th><p><strong>一级参数</strong></p></th><th><p><strong>二级参数</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必选</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>event</p></td><td><p>string</p></td><td><p>是</p></td><td><p>事件名称：<strong>RespondingContent</strong></p></td></tr><tr><td></td><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td></td><td><p>round_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本轮交互的ID</p></td></tr><tr><td></td><td><p>llm_request_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>调用llm的request_id</p></td></tr><tr><td></td><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>系统对外输出的文本，流式<strong>增量</strong>输出</p></td></tr><tr><td></td><td><p>spoken</p></td><td><p>string</p></td><td><p>是</p></td><td><p>合成语音时使用的文本，流式<strong>增量</strong>输出</p></td></tr><tr><td></td><td><p>finished</p></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td></td><td><p>finish_reason</p></td><td><p>string</p></td><td><p>否</p></td><td><p>结束原因，目前只有一种：</p><ul><li><p>stop 表示正常结束</p></li></ul></td></tr><tr><td></td><td><p>extra_info</p></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><ul><li><p>commands: 命令字符串，<strong>此字段为JSON字符串，需要进行二次解析。</strong>各类agent使用的命令字符串可以参考<a href="official-agent-297b22931e69e622.md">调用官方Agent</a>的说明。</p></li><li><p>agent_info: 智能体信息</p></li><li><p>tool_calls: 插件返回的信息</p></li><li><p>tool_infos: 工具信息</p></li></ul></td></tr></tbody></table>

<a id="c185bd47284gb"></a>

##### 示例如下：

<a id="code-block-4"></a>

```json
{
    "output": {
        "event": "RespondingContent",
        "dialog_id": "e788xxxx-xxxx-xxxx-xxxx-xxxx9637",
        "round_id": "d8****************************29",
        "llm_request_id": "fb****************************67",
        "text": "你好",
        "spoken": "你好",
        "finished": true,
        "finish_reason":"stop",
        "extra_info": {
            "agent_info": {
                "round": 1,
                "device": {
                    "device_id": ""
                },
                "intent_infos": [
                    {
                        "intent": "***",
                        "domain": "***"
                    }
                ]
            },
            "query": "你好，北京今天的天气怎么样？"
        }
    },
    "request_id": "6481xxxx-xxxx-xxxx-xxxx-xxxx1aed0"
}
```

<a id="错误事件"></a>

<a id="61f76efaaci3b"></a>

### 错误事件

报错信息。错误码说明可以参考官方文档：[多模态交互套件-错误码](multimodal-error-code-27e8073eb3267722.md)

<a id="error-output-message"></a>

<a id="480a36a0b3w8k"></a>

#### Error - Output Message

| 一级参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| code | string | 是 | 错误码 |
| message | string | 是 | 错误消息 |
| request\_id | string | 是 | 请求id |

<a id="code-block-5"></a>

```json
{
    "code": "InternalLLMError",
    "message": "Internal LLM error",
    "request_id": "0aa0xxxx-xxxx-xxxx-xxxx-xxxxaa21"
}
```

<a id="调用示例"></a>

<a id="197418ee77fek"></a>

## 调用示例

请求示例如下：

header里要有**X-DashScope-SSE: enable**。

> **说明**
>
> 注意把your\_api\_key，app\_id，text，以及parameters里的其他参数都替换为实际使用的值。

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer your_api_key" \
--header "X-DashScope-SSE: enable" \
--data '{
    "model": "multimodal-dialog",
    "input": {
            "directive": "Request",
            "app_id": "****************",
            "text":"你好，北京今天的天气怎么样？"
        },
    "parameters": {
            "images":[{
              "type": "base64",
              "value": "base64String"
                }],
            "client_info": {
                "user_id": "bin********207",
                "device":{
                  "uuid": "432k*********k449"
                },
                "network":{
                  "ip": "x.x.x.x"
                },
                "location":{
                  "city_name": "北京市"
                }
            }
        }
}'
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
import okhttp3.*;
import okhttp3.sse.EventSource;
import okhttp3.sse.EventSourceListener;
import okhttp3.sse.EventSources;
import org.jetbrains.annotations.Nullable;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;

public class SseTest {

  public static void main(String[] args){
    String sseUrl = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation";
    String apiKey = "your_api_key";
    String appId = "your_app_id";
    String model = "multimodal-dialog";

    OkHttpClient okHttpClient = new OkHttpClient();

    // 构建 Headers
    okhttp3.Headers.Builder headersBuilder = new okhttp3.Headers.Builder();
    headersBuilder.add("Accept", "text/event-stream");
    headersBuilder.add("Content-Type", "application/json");
    headersBuilder.add("Authorization", "Bearer " + apiKey);
    headersBuilder.add("X-DashScope-SSE", "enable");

    MediaType mediaType = MediaType.parse("application/json; charset=utf-8");
    String body = "{\n" +
                "    \"model\": \"" + model + "\",\n" +
                "    \"input\": {\n" +
                "            \"app_id\": \""+appId+"\",\n" +
                "            \"text\":\"你好，北京今天的天气怎么样？\",\n" +
                "            \"directive\": \"Request\"\n" +
                "        },\n" +
                "    \"parameters\": {\n" +
                "            \"client_info\": {\n" +
                "                \"user_id\": \"xxxxxxxxxxxxxxx\",\n" +
                "                \"device\": {\n" +
                "                    \"uuid\": \"xxxxxx\"\n" +
                "                }\n" +
                "            }\n" +
                "        }\n" +
                "}";

    Request request = new Request.Builder()
      .url(sseUrl)
      .headers(headersBuilder.build())
      .post(RequestBody.create(mediaType, body))
      .build();

    CountDownLatch latch = new CountDownLatch(1);

    EventSourceListener listener = new EventSourceListener() {
      @Override
      public void onOpen(EventSource eventSource, Response response) {
        System.out.println("onOpen response: " + response);
      }

      @Override
      public void onEvent(EventSource eventSource, @Nullable String id, @Nullable String type, String data) {
        System.out.println("onEvent: id: " + id + "｜ data: " + data);
      }

      @Override
      public void onClosed(EventSource eventSource) {
        System.out.println("onClosed");
        latch.countDown();
      }

      @Override
      public void onFailure(EventSource eventSource, @Nullable Throwable t, @Nullable Response response) {
        System.out.println("onFailure "+t + " | response: " + response);
                if(response != null && response.body() != null){
                    try {
                        System.err.println("onFailure response body: " + response.body().string());
                    } catch (IOException e) {
                      System.err.println("onFailure response body RuntimeException: " + e);
                        throw new RuntimeException(e);
                    }
                }
        latch.countDown();
      }
    };

    EventSource.Factory factory = EventSources.createFactory(okHttpClient);

    System.out.println("Connecting to SSE endpoint...");

    EventSource eventSource = factory.newEventSource(request, listener);

    // 阻塞主线程，直到连接关闭
    try {
      latch.await();
    } catch (InterruptedException e) {
      System.err.println("latch.await RuntimeException: " + e.getMessage());
      e.printStackTrace();
    } finally {
      //清理资源
      eventSource.cancel();
      okHttpClient.dispatcher().executorService().shutdown();
      okHttpClient.connectionPool().evictAll();
    }

    System.out.println("SSE Connection closed!");
  }
}
```
