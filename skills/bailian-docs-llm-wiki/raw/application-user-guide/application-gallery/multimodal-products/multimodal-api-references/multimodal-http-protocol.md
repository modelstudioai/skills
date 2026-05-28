# HTTP协议

本文介绍基于 HTTP 协议的多模态交互 API。

多模态交互开发套件中的HTTP协议支持使用纯文本或图片发起**http-sse**请求，获取大模型处理结果。

**重要**

使用HTTP协议接入多模态交互开发套件，不支持以下功能：

-   不支持纯视觉应用
    
-   不支持使用以下Agent：
    
    视频通话、极速视频/语音通话、语音翻译、新闻电台、儿童故事、录音纪要、主动导览、主动陪伴。
    

## **前提条件**

已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**

对于客户端调用的场景，在客户端处理API Key有安全风险，建议从服务端用API Key获取临时鉴权Token，再把Token下发给客户端使用。具体方法请参考：[生成临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。

## **服务地址**

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

**说明**

发起HTTP请求时，请求的header里要有**X-DashScope-SSE: enable**

## **鉴权**

需要在发起HTTP请求时，把API Key放在HTTP Header里（需要将your\_api\_key替换为真实的API Key）：

```
"Authorization": "Bearer your_api_key"
```

## **消息类型**

当前HTTP协议仅包含文本消息。文本消息是JSON格式字符串。

### **发起请求**

#### **Request - Input Message**

发起HTTP请求。

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

model

string

是

阿里云百炼模型名称，固定为"multimodal-dialog"，请直接复制使用

input

directive

string

是

指令名称：**Request**

app\_id

string

是

客户创建的应用ID（[获取APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)），可在**多模态交互开发套件**控制台的“我的应用”页面查看

dialog\_id

string

否

对话id，默认不填时是新对话，服务端会自动生成并在返回结果中下发，格式示例："12345678-1234-1234-1234-1234567890ab"，共36个字符。当希望继续之前的对话时，把当时服务端下发的dialog\_id在这里传入

text

string

是

要处理的文本。

-   调用部分agent时，text可以是""空字符串，服务端需要使用parameters中的images或者biz\_params参数处理。具体参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)。
    

parameters

client\_info

object

是

参数说明参考下方 [parameters.client\_info的参数说明](#8639a70e4bsn1)表格

images

list\[\]

否

需要分析的图片数据，仅多模态应用可支持图片问答，参数说明参考下方[parameters.images的参数说明](#e17e1d8629h1u)表格

biz\_params

object

否

按需配置，参数说明参考下方[parameters.biz\_params的参数说明](#314d1091471e2)表格

**parameters.client\_info**的参数说明如下：

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

user\_id

string

是

终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。最大长度36个字符。

device

uuid

string

否

客户端全局唯一的ID，需要用户自己生成并传入SDK，最大长度40个字符。一个终端用户可以有多个设备，那么每一个设备的uuid都不同，但user\_id相同。

network

ip

string

否

调用方公网IP

location

latitude

string

否

调用方纬度信息，在需要客户端精确位置的业务场景提交

longitude

string

否

调用方经度信息，在需要客户端精确位置的业务场景提交

city\_name

string

否

调用方所在城市，指明客户端粗略位置

**parameters.images**的参数说明如下：

**一级参数**

**类型**

**是否必选**

**说明**

type

string

是

图片类型，支持两种：base64/url

value

string

是

图片内容。

-   当type为base64时，这里是图片的base64字符串。
    
-   当type为url时，这里是图片的url地址。
    

**parameters.biz\_params**的参数说明如下：

**一级参数**

**类型**

**是否必选**

**说明**

user\_defined\_params

json object

否

需要透传给agent的参数，各类agent传递的参数参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)文档说明

user\_prompt\_params

json object

否

用于设置用户自定义prompt变量，由用户自定义设置json中的key和value。管控台上配置自定义prompt变量的方法参考[应用配置-提示词](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#74a8b82973u0r)

user\_query\_params

json object

否

用于设置用户自定义对话变量，由用户自定义设置json中的key和value。管控台上配置自定义对话变量的方法参考[应用配置-对话变量](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#62d90ef075ve1)

##### **示例如下**

```
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

### **文本下发事件**

#### **RespondingContent - Output Message**

**一级参数**

**二级参数**

**类型**

**是否必选**

**说明**

output

event

string

是

事件名称：**RespondingContent**

dialog\_id

string

是

对话ID

round\_id

string

是

本轮交互的ID

llm\_request\_id

string

是

调用llm的request\_id

text

string

是

系统对外输出的文本，流式**增量**输出

spoken

string

是

合成语音时使用的文本，流式**增量**输出

finished

bool

是

输出是否结束

finish\_reason

string

否

结束原因，目前只有一种：

-   stop 表示正常结束
    

extra\_info

object

否

其他扩展信息，目前支持：

-   commands: 命令字符串，**此字段为JSON字符串，需要进行二次解析。**各类agent使用的命令字符串可以参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)的说明。
    
-   agent\_info: 智能体信息
    
-   tool\_calls: 插件返回的信息
    
-   tool\_infos: 工具信息
    

##### **示例如下：**

```
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

### **错误事件**

报错信息。错误码说明可以参考官方文档：[多模态交互套件-错误码](https://help.aliyun.com/zh/model-studio/multimodal-error-code)

#### **Error - Output Message**

**一级参数**

**类型**

**是否必选**

**说明**

code

string

是

错误码

message

string

是

错误消息

request\_id

string

是

请求id

```
{
    "code": "InternalLLMError",
    "message": "Internal LLM error",
    "request_id": "0aa0xxxx-xxxx-xxxx-xxxx-xxxxaa21"
}
```

## **调用示例**

请求示例如下：

header里要有**X-DashScope-SSE: enable**。

**说明**

注意把your\_api\_key，app\_id，text，以及parameters里的其他参数都替换为实际使用的值。

## curl

```
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

## Java

```
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
