# 通过模板ID调用通义晓蜜CCAI-对话分析AIO应用

## **前提条件**

-   本文向您介绍通义晓蜜CCAI-对话分析AIO应用SDK的安装、使用及注意事项。
    
-   如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。
    
-   各API详细出入参说明请查看左侧目录中的[API目录](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-dir/)。
    

## **接口入参位置**

### **workspaceId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9493376271/p851107.png)

1.  访问[**业务空间管理**](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面。
    
2.  业务空间管理列表中Workspace ID为入参中workspaceId。
    

### **appId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3298853471/p935542.png)

1.  访问**应用广场**页面，点击通义晓蜜CCAI-对话分析AIO的**查看详情**。
    
2.  点击上方**我的应用**，展示应用卡片列表。
    
3.  每个卡片上的应用ID即为接口参数中appId。
    

### **templateIds**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9493376271/p851114.png)

1.  访问**[应用广场](https://bailian.console.aliyun.com/#/app-market)**，点击通义晓蜜CCAI-对话分析AIO的**查看详情**。
    
2.  点击上方**我的应用**，展示应用卡片列表。
    
3.  点击**管理**进入对应的应用卡片。
    
4.  点击**自定义指令**模板，切换为**专业构建模式**。
    
5.  点击右上方**指令模板管理**。
    
6.  **自定义模板**列表中**模板ID**为入参中templateIds。
    
7.  如果还未创建自定义模板，请直接点击右上角**保存指令模板**按钮。
    

## **安装SDK**

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

## 异步流式调用

**说明**

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，templateIds替换示例中的YOUR\_TEMPLATE，代码才能正常运行。

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

    private static String workspaceId="YOUR_WORKSPACEID";
    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String appId="YOUR_APPID";
    private static Long templateId=1L; //替换为您在模板管理中的模板ID

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
       //对话内容
        List<RunCompletionRequest.Sentences> sentenceDTOList = new ArrayList<>();
        RunCompletionRequest.Sentences sentenceDto1 = RunCompletionRequest.Sentences.builder().role("user").text("我要办理信用卡").build();
        RunCompletionRequest.Sentences sentenceDto2 = RunCompletionRequest.Sentences.builder().role("agent").text("好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息").build();
        sentenceDTOList.add(sentenceDto1);
        sentenceDTOList.add(sentenceDto2);
        RunCompletionRequest.Dialogue dialogue = RunCompletionRequest.Dialogue.builder().sessionId("session_01_asdfasdfasd")
                .sentences(sentenceDTOList).build();

        //属性信息
        List<RunCompletionRequest.Fields> fieldList = new ArrayList<>();
        RunCompletionRequest.Fields field1 = RunCompletionRequest.Fields.builder().name("姓名").desc("用户的名称").build();
        RunCompletionRequest.Fields field2 = RunCompletionRequest.Fields.builder().name("信用卡号").desc("用户的信用卡号").build();
        fieldList.add(field1);
        fieldList.add(field2);

        //构建请求参数
        RunCompletionRequest completionParam = RunCompletionRequest.builder()
                .workspaceId(workspaceId).appId(appId).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).modelCode("tyxmTurbo").dialogue(dialogue).fields(fieldList).templateIds(Arrays.asList(templateId)).stream(true).build();
        System.out.println(JSON.toJSONString(completionParam));

        //发送请求
        ResponseIterable<RunCompletionResponseBody> x = client.runCompletionWithResponseIterable(completionParam);
        ResponseIterator<RunCompletionResponseBody> iterator = x.iterator();
        String lastTxt="";
        while (iterator.hasNext()) {
            RunCompletionResponseBody event = iterator.next();
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

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，templateIds替换示例中的YOUR\_TEMPLATE，代码才能正常运行。

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

    private static String workspaceId="YOUR_WORKSPACEID";
    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String appId="YOUR_APPID";
    private static Long templateId=1L; //替换为您在模板管理中的模板ID

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
        //对话内容
        List<RunCompletionRequest.Sentences> sentenceDTOList = new ArrayList<>();
        RunCompletionRequest.Sentences sentenceDto1 = RunCompletionRequest.Sentences.builder().role("user").text("我要办理信用卡").build();
        RunCompletionRequest.Sentences sentenceDto2 = RunCompletionRequest.Sentences.builder().role("agent").text("好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息").build();
        sentenceDTOList.add(sentenceDto1);
        sentenceDTOList.add(sentenceDto2);
        RunCompletionRequest.Dialogue dialogue = RunCompletionRequest.Dialogue.builder().sessionId("session_01_asdfasdfasd")
                .sentences(sentenceDTOList).build();

        //属性信息
        List<RunCompletionRequest.Fields> fieldList = new ArrayList<>();
        RunCompletionRequest.Fields field1 = RunCompletionRequest.Fields.builder().name("姓名").desc("用户的名称").build();
        RunCompletionRequest.Fields field2 = RunCompletionRequest.Fields.builder().name("信用卡号").desc("用户的信用卡号").build();
        fieldList.add(field1);
        fieldList.add(field2);
        
        //构建请求参数
        RunCompletionRequest completionParam = RunCompletionRequest.builder()
                .workspaceId(workspaceId).appId(appId).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).dialogue(dialogue).fields(fieldList).templateIds(Arrays.asList(templateId)).stream(false).build();
        System.out.println(JSON.toJSONString(completionParam));

        //发送请求
        CompletableFuture<RunCompletionResponse> x = client.runCompletion(completionParam);
        RunCompletionResponse generateCompletionResponse = x.get(10, TimeUnit.SECONDS);
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody()));
        System.out.println(generateCompletionResponse.getBody().getText());
        System.out.println(generateCompletionResponse.getBody().getRequestId());      
    }
}
```

Python

```
import asyncio

from alibabacloud_contactcenterai20240603.client import Client

import alibabacloud_contactcenterai20240603
import alibabacloud_tea_openapi
from alibabacloud_tea_openapi.models import Config
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest, \
    RunCompletionRequestDialogueSentences, RunCompletionRequestDialogue, RunCompletionRequestFields, \
    RunCompletionRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequestMessages

ak = "YOUR_ACCESS_KEY_ID"
sk = "YOUR_ACCESS_KEY_SECRET"
workSpace = "YOUR_WORKSPACEID"
appId = "YOUR_APPID"
templateId = "YOUR_TEMPLATE"

async def run_async():
    config = Config()
    config.access_key_id = ak
    config.access_key_secret = sk
    config.endpoint = "contactcenterai.cn-shanghai.aliyuncs.com"
    config.region_id = "cn-shanghai"

    client = Client(config)
    # 对话
    sentence1 = RunCompletionRequestDialogueSentences("chat01", "user", "我要办理信用卡")
    sentence2 = RunCompletionRequestDialogueSentences("chat02", "agent",
                                                      "好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息")
    sentenceList = [sentence1, sentence2]
    dialogue = RunCompletionRequestDialogue(sentenceList, "session_01_asdfasdfasd")
    # 属性填充
    fields1 = RunCompletionRequestFields("", "用户的名称", None, "姓名")
    fields2 = RunCompletionRequestFields("", "用户的信用卡号", None, "信用卡号")
    fieldsList = [fields1, fields2]
    # 构建请求参数
    templateIds = [templateId]

    request = RunCompletionRequest()
    request.dialogue = dialogue
    request.fields = fieldsList
    request.model_code = "tyxmTurbo"
    request.stream = False
    request.template_ids = templateIds

    response = await client.run_completion_async(workSpace, appId, request)
    body = response.body
    print(body)

if __name__ == '__main__':
    asyncio.run(run_async())
```

## 同步非流式调用

**说明**

请将workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，templateIds替换示例中的YOUR\_TEMPLATE，代码才能正常运行。

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

    private static String workspaceId="YOUR_WORKSPACEID";
    private static String accessKeyId="YOUR_ACCESS_KEY_ID";
    private static String accessKeySecret="YOUR_ACCESS_KEY_SECRET";
    private static String appId="YOUR_APPID";
    private static Long templateId=1L; //替换为您在模板管理中的模板ID

    public static void main(String[] args) throws Exception{
        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);

        RunCompletionRequest request = new RunCompletionRequest();
        //对话信息
        List<RunCompletionRequest.RunCompletionRequestDialogueSentences> sentenceDTOList = new ArrayList<>();
        RunCompletionRequest.RunCompletionRequestDialogueSentences sentenceDto1 = new RunCompletionRequest.RunCompletionRequestDialogueSentences();
        sentenceDto1.setRole("user").setText("我要办理信用卡");
        RunCompletionRequest.RunCompletionRequestDialogueSentences sentenceDto2 = new RunCompletionRequest.RunCompletionRequestDialogueSentences();
        sentenceDto2.setRole("agent").setText("好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息");
        sentenceDTOList.add(sentenceDto1);
        sentenceDTOList.add(sentenceDto2);

        //属性填充
        List<RunCompletionRequest.RunCompletionRequestFields> fieldList = new ArrayList<>();
        RunCompletionRequest.RunCompletionRequestFields field1 = new RunCompletionRequest.RunCompletionRequestFields();
        field1.setName("姓名").setDesc("用户的名称");
        RunCompletionRequest.RunCompletionRequestFields field2 = new RunCompletionRequest.RunCompletionRequestFields();
        field2.setName("信用卡号").setDesc("用户的信用卡号");
        fieldList.add(field1);
        fieldList.add(field2);

        RunCompletionRequest.RunCompletionRequestDialogue dialogue = new RunCompletionRequest.RunCompletionRequestDialogue();
        dialogue.setSessionId("session_01_asdfasdfasd").setSentences(sentenceDTOList);
        //构建请求参数
        request.setDialogue(dialogue).setStream(false).setModelCode("tyxmTurbo").setFields(fieldList).setTemplateIds(Arrays.asList(templateId));

        RunCompletionResponse runCompletionResponse = client.runCompletion(workspaceId, appId, request);
        RunCompletionResponseBody responseBody = runCompletionResponse.getBody();
        System.out.println(JSON.toJSONString(responseBody));
    }
}
```

Python

```
from alibabacloud_contactcenterai20240603.client import Client

import alibabacloud_contactcenterai20240603
import alibabacloud_tea_openapi
from alibabacloud_tea_openapi.models import Config
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest, \
    RunCompletionRequestDialogueSentences, RunCompletionRequestDialogue, RunCompletionRequestFields, \
    RunCompletionRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequest
from alibabacloud_contactcenterai20240603.models import RunCompletionMessageRequestMessages

ak = "YOUR_ACCESS_KEY_ID"
sk = "YOUR_ACCESS_KEY_SECRET"
workSpace = "YOUR_WORKSPACEID"
appId = "YOUR_APPID"
templateId = "YOUR_TEMPLATE"

if __name__ == '__main__':
    config = Config()
    config.access_key_id = ak
    config.access_key_secret = sk
    config.endpoint = "contactcenterai.cn-shanghai.aliyuncs.com"
    config.region_id = "cn-shanghai"

    client = Client(config)
    # 对话
    sentence1 = RunCompletionRequestDialogueSentences("chat01", "user", "我要办理信用卡")
    sentence2 = RunCompletionRequestDialogueSentences("chat02", "agent", "好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息")
    sentenceList = [sentence1, sentence2]
    dialogue = RunCompletionRequestDialogue(sentenceList, "session_01_asdfasdfasd")
    # 属性填充
    fields1 = RunCompletionRequestFields("", "用户的名称", None, "姓名")
    fields2 = RunCompletionRequestFields("", "用户的信用卡号", None, "信用卡号")
    fieldsList = [fields1, fields2]
    # 构建请求参数
    templateIds = [templateId]
 
    request = RunCompletionRequest()
    request.dialogue = dialogue
    request.fields = fieldsList
    request.model_code = "tyxmTurbo"
    request.stream = False
    request.template_ids = templateIds

    response = client.run_completion(workSpace, appId, request)
    body = response.body
    print(body)
```
