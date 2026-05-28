# 通过原生Prompt调用通义晓蜜CCAI-对话分析AIO应用

## **前提条件**

-   本文向您介绍通义晓蜜CCAI-对话分析AIO应用Java SDK的安装、使用及注意事项。
    
    关于Java SDK的更多说明，请参见[开始使用](https://help.aliyun.com/zh/sdk/developer-reference/get-started-with-alibaba-cloud-classic-sdk-for-java)。
    
-   如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。
    
-   各API详细出入参说明请查看左侧目录中的[API目录](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-dir/)。
    

## 接口入参位置

### **workspaceId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9998853471/p935585.png)

1.  访问[**业务空间管理**](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面。
    
2.  业务空间管理列表中Workspace ID为入参中workspaceId。
    

### **appId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9998853471/p935586.png)

1.  访问[应用广场应用实践](https://bailian.console.aliyun.com/#/app-market/lightApplication)页面，选择**通义晓蜜CCAI-对话分析AIO**，单击**立即查看**。
    
2.  单击上方**我的应用**，展示应用卡片列表。
    
3.  每个卡片上的应用ID即为接口参数中appId。
    

## 安装SDK

## 同步Java

<dependency>

<groupId>com.aliyun</groupId>

<artifactId>contactcenterai20240603</artifactId>

<version>3.6.4</version>

</dependency>

## 异步Java

<dependency>

<groupId>com.aliyun</groupId>

<artifactId>alibabacloud-contactcenterai20240603</artifactId>

<version>3.0.12</version>

</dependency>

## Python

pip install alibabacloud\_contactcenterai20240603

## **异步流式调用**

**说明**

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。

```
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.core.http.HttpMethod;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureAlgorithm;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.contactcenterai20240603.AsyncClient;
import com.aliyun.sdk.service.contactcenterai20240603.models.*;
import darabonba.core.RequestConfiguration;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class CcaiPaasTest {

    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String workspaceId="YOUR_WORKSPACEID";
    private static String appId="YOUR_APPID";

    private static StaticCredentialProvider provider = StaticCredentialProvider.create(
            Credential.builder()
                    .accessKeyId(accessKeyId)
                    .accessKeySecret(accessKeySecret)
                    .build()
    );

    private static AsyncClient client = AsyncClient.builder()
            .region("cn-shanghai") 
            .credentialsProvider(provider)
            .serviceConfiguration(Configuration.create()
                    .setSignatureVersion(SignatureVersion.V3)
                    .setSignatureAlgorithmV3(SignatureAlgorithm.ACS3_HMAC_SHA256)
            ).overrideConfiguration(
                    ClientOverrideConfiguration.create()
                            .setProtocol("HTTPS")
                            .setEndpointOverride("contactcenterai.cn-shanghai.aliyuncs.com")
            ).build();

    public static void main(String[] args) throws Exception{
        //Prompt
        List<RunCompletionMessageRequest.Messages> messageList = new ArrayList<>();
        messageList.add(RunCompletionMessageRequest.Messages.builder().role("system").content("You are a helpful assistant.").build());
        messageList.add(RunCompletionMessageRequest.Messages.builder().role("user").content("请阅读以下对话内容，按照要求执行指令任务。\\n```\\n\\n客服:你自己的话```\\n任务指令如下：\\n```\\n你是一个智能办公助理，可以对对话分析内容生成简单的摘要\\n```\\n请依据上述指令，确保准确无误地完成任务。").build());

        RunCompletionMessageRequest completionParam = RunCompletionMessageRequest.builder()
                .workspaceId(workspaceId).appId(appId).messages(messageList).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).stream(true).build();
        System.out.println(JSON.toJSONString(completionParam));

        ResponseIterable<RunCompletionMessageResponseBody> x = client.runCompletionMessageWithResponseIterable(completionParam);
        ResponseIterator<RunCompletionMessageResponseBody> iterator = x.iterator();
        String lastTxt="";
        while (iterator.hasNext()) {
            RunCompletionMessageResponseBody event = iterator.next();
            //System.out.println(event.getText());
            //System.out.println(event.getFinishReason());
            //System.out.println(event.getRequestId());
            lastTxt=event.getText();
        }

        System.out.println("ALL***********************");
        System.out.println(lastTxt);
        System.out.println("请求成功的请求头值：");
        System.out.println(x.getStatusCode());
        System.out.println(x.getHeaders());      
    }
}
```

## **异步非流式调用**

**说明**

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。

Java

```
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.core.http.HttpMethod;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureAlgorithm;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.contactcenterai20240603.AsyncClient;
import com.aliyun.sdk.service.contactcenterai20240603.models.*;
import darabonba.core.RequestConfiguration;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class CcaiPaasTest {

    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String workspaceId="YOUR_WORKSPACEID";
    private static String appId="YOUR_APPID";

    private static StaticCredentialProvider provider = StaticCredentialProvider.create(
            Credential.builder()
                    .accessKeyId(accessKeyId)
                    .accessKeySecret(accessKeySecret)
                    .build()
    );

    private static AsyncClient client = AsyncClient.builder()
            .region("cn-shanghai") 
            .credentialsProvider(provider)
            .serviceConfiguration(Configuration.create()
                    .setSignatureVersion(SignatureVersion.V3)
                    .setSignatureAlgorithmV3(SignatureAlgorithm.ACS3_HMAC_SHA256)
            ).overrideConfiguration(
                    ClientOverrideConfiguration.create()
                            .setProtocol("HTTPS")
                            .setEndpointOverride("contactcenterai.cn-shanghai.aliyuncs.com")
            ).build();

    public static void main(String[] args) throws Exception{
         //Prompt
        List<RunCompletionMessageRequest.Messages> messageList = new ArrayList<>();
        messageList.add(RunCompletionMessageRequest.Messages.builder().role("system").content("You are a helpful assistant.").build());
        messageList.add(RunCompletionMessageRequest.Messages.builder().role("user").content("请阅读以下对话内容，按照要求执行指令任务。\\n```\\n\\n客服:你自己的话```\\n任务指令如下：\\n```\\n你是一个智能办公助理，可以对对话分析内容生成简单的摘要\\n```\\n请依据上述指令，确保准确无误地完成任务。").build());

        RunCompletionMessageRequest completionParam = RunCompletionMessageRequest.builder()
                .workspaceId(workspaceId).appId(appId).messages(messageList).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).stream(false).build();
        System.out.println(JSON.toJSONString(completionParam));

        CompletableFuture<RunCompletionMessageResponse> generateCompletionResponseCompletableFuture = client.runCompletionMessage(completionParam);
        RunCompletionMessageResponse generateCompletionResponse = generateCompletionResponseCompletableFuture.get(10, TimeUnit.SECONDS);
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody().getText()));
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody().getFinishReason()));
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody().getRequestId()));
    }
}
```

Python

```
import asyncio

from alibabacloud_contactcenterai20240603.client import Client

from alibabacloud_tea_openapi.models import Config
from alibabacloud_contactcenterai20240603.models import (RunCompletionRequestDialogueSentences,
                                                         RunCompletionRequestDialogue,
                                                         RunCompletionRequestFields,
                                                         RunCompletionRequest)
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequestMessages

ak = "YOUR_ACCESS_KEY_ID"
sk = "YOUR_ACCESS_KEY_SECRET"
workSpace = "YOUR_WORKSPACEID"
appId = "YOUR_APPID"

async def run_async_sse():
    config = Config()
    config.access_key_id = ak
    config.access_key_secret = sk
    config.endpoint = "contactcenterai.cn-shanghai.aliyuncs.com"
    config.region_id = "cn-shanghai"

    client = Client(config)

    # Prompt
    role = "system"
    content = "You are a helpful assistant."
    requestMessage1 = RunCompletionMessageRequestMessages(content, role)
    role = "user"
    content = "请阅读以下对话内容，按照要求执行指令任务。\n```\n\n客服:你自己的话\n客户:你自己要号手机\n客户:31\n客服:他是1公分\n客户:那年后，我看\n客户:后来点开看\n客户:嗯，要不是以前的\n客户:这不看你看\n客服:那年后我是按后来改成按执行的时间延后了，要不以前的时间延后，你根本就没法延\n客服:你在这跟到后面来\n客服:这里不是大多少天都会员了吗\n客户:那你不是大于多少天都结了吗\n客服:嗯\n客户:嗯\n客服:我们有1个\n客户:就是你这个\n客服:他说你这里面也按照\n客户:他有多少是蒙细别的吗\n客户:这3天之后\n客服:当前执行的\n客服:这些，其实你这个也是\n客户:那你这个颜色\n客服:按照他给了预期了，是不是结多少天\n客户:按照他给的利息嘛，是不是延延延多少天啊，没\n客服:那是什么问题\n客服:你3天的时候关内\n客户:你要是原来那个\n客户:你基本上就那你要看\n客服:你要是原来的，你，你基本上都要不要\n客服:5天\n客户:对的\n客户:啊，关于\n客户:15新啊\n客户:上面录的\n\n```\n任务指令如下：\n```\n你是一个智能办公助理，可以对对话分析内容生成简单的摘要\n```\n请依据上述指令，确保准确无误地完成任务。"
    requestMessage2 = RunCompletionMessageRequestMessages(content, role)

    listRequestMessage = [requestMessage1, requestMessage2]
    
    request = RunCompletionMessageRequest()
    request.messages = listRequestMessage
    request.model_code = "tyxmTurbo"
    request.stream = False

    # 发送请求
    response = await client.run_completion_message_async(workSpace, appId, request)
    body = response.body
    print(body)

if __name__ == '__main__':
    asyncio.run(run_async_sse())
```

## 同步非流式调用

**说明**

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。

Java

```
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import java.util.*;

public class CcaiPaasTest {

    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String workspaceId="YOUR_WORKSPACEID";
    private static String appId="YOUR_APPID";

    public static void main(String[] args) throws Exception{
        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);

        //Prompt
        RunCompletionMessageRequest request = new RunCompletionMessageRequest();
        List<RunCompletionMessageRequest.RunCompletionMessageRequestMessages> messageList = new ArrayList<>();
        RunCompletionMessageRequest.RunCompletionMessageRequestMessages message1 = new RunCompletionMessageRequest.RunCompletionMessageRequestMessages();
        message1.setRole("system").setContent("You are a helpful assistant.");
        RunCompletionMessageRequest.RunCompletionMessageRequestMessages message2 = new RunCompletionMessageRequest.RunCompletionMessageRequestMessages();
        message2.setRole("user").setContent("请阅读以下对话内容，按照要求执行指令任务。\\n```\\n\\n客服:你自己的话\\n客户:你自己要号手机\\n客户:31\\n客服:他是1公分\\n客户:那年后，我看\\n客户:后来点开看\\n客户:嗯，要不是以前的\\n客户:这不看你看\\n客服:那年后我是按后来改成按执行的时间延后了，要不以前的时间延后，你根本就没法延\\n客服:你在这跟到后面来\\n客服:这里不是大多少天都会员了吗\\n客户:那你不是大于多少天都结了吗\\n客服:嗯\\n客户:嗯\\n客服:我们有1个\\n客户:就是你这个\\n客服:他说你这里面也按照\\n客户:他有多少是蒙细别的吗\\n客户:这3天之后\\n客服:当前执行的\\n客服:这些，其实你这个也是\\n客户:那你这个颜色\\n客服:按照他给了预期了，是不是结多少天\\n客户:按照他给的利息嘛，是不是延延延多少天啊，没\\n客服:那是什么问题\\n客服:你3天的时候关内\\n客户:你要是原来那个\\n客户:你基本上就那你要看\\n客服:你要是原来的，你，你基本上都要不要\\n客服:5天\\n客户:对的\\n客户:啊，关于\\n客户:15新啊\\n客户:上面录的\\n\\n```\\n任务指令如下：\\n```\\n你是一个智能办公助理，可以对对话分析内容生成简单的摘要\\n```\\n请依据上述指令，确保准确无误地完成任务。");
        messageList.add(message1);
        messageList.add(message2);

        request.setMessages(messageList);
        request.setStream(false);
        request.setModelCode("tyxmTurbo");

        RunCompletionMessageResponse responseBody = client.runCompletionMessage(workspaceId, appId, request);
        RunCompletionMessageResponseBody body = responseBody.getBody();
        System.out.println(JSON.toJSONString(body));
    }
}
```

Python

```
from alibabacloud_contactcenterai20240603.client import Client

import alibabacloud_contactcenterai20240603
import alibabacloud_tea_openapi
from alibabacloud_tea_openapi.models import Config
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequestMessages

ak = "YOUR_ACCESS_KEY_ID"
sk = "YOUR_ACCESS_KEY_SECRET"
workSpace = "YOUR_WORKSPACEID"
appId = "YOUR_APPID"

if __name__ == '__main__':
    config = Config()
    config.access_key_id = ak
    config.access_key_secret = sk
    config.endpoint = "contactcenterai.cn-shanghai.aliyuncs.com"
    config.region_id = "cn-shanghai"

    client = Client(config)

    # Prompt
    role = "system"
    content = "You are a helpful assistant."
    requestMessage1 = RunCompletionMessageRequestMessages(content, role)
    role = "user"
    content = "请阅读以下对话内容，按照要求执行指令任务。\n```\n\n客服:你自己的话\n客户:你自己要号手机\n客户:31\n客服:他是1公分\n客户:那年后，我看\n客户:后来点开看\n客户:嗯，要不是以前的\n客户:这不看你看\n客服:那年后我是按后来改成按执行的时间延后了，要不以前的时间延后，你根本就没法延\n客服:你在这跟到后面来\n客服:这里不是大多少天都会员了吗\n客户:那你不是大于多少天都结了吗\n客服:嗯\n客户:嗯\n客服:我们有1个\n客户:就是你这个\n客服:他说你这里面也按照\n客户:他有多少是蒙细别的吗\n客户:这3天之后\n客服:当前执行的\n客服:这些，其实你这个也是\n客户:那你这个颜色\n客服:按照他给了预期了，是不是结多少天\n客户:按照他给的利息嘛，是不是延延延多少天啊，没\n客服:那是什么问题\n客服:你3天的时候关内\n客户:你要是原来那个\n客户:你基本上就那你要看\n客服:你要是原来的，你，你基本上都要不要\n客服:5天\n客户:对的\n客户:啊，关于\n客户:15新啊\n客户:上面录的\n\n```\n任务指令如下：\n```\n你是一个智能办公助理，可以对对话分析内容生成简单的摘要\n```\n请依据上述指令，确保准确无误地完成任务。"
    requestMessage2 = RunCompletionMessageRequestMessages(content, role)

    listRequestMessage = [requestMessage1, requestMessage2]
   
    request = RunCompletionMessageRequest()
    request.messages = listRequestMessage
    request.model_code = "tyxmTurbo"
    request.stream = False

    # 发送请求
    response = client.run_completion_message(workSpace, appId, request)
    body = response.body
    print(body)
```
