# 通过通义晓蜜CCAI-对话分析AIO应用进行图片分析

本文向您介绍一个通过通义晓蜜CCAI-对话分析AIO应用进行图片分析的最佳实践。

-   关于Java SDK的更多说明，请参见[开始使用](https://help.aliyun.com/zh/sdk/developer-reference/get-started-with-alibaba-cloud-classic-sdk-for-java)。
    
-   关于各API的详细出入参说明，请参见[API目录](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-dir/)。
    

## 前提条件

-   如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。
    

## **获取**Workspace **ID和App ID**

### **Workspace ID**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9268853471/p935593.png)

1.  访问[**业务空间管理**](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面。
    
2.  在业务空间管理列表中获取的Workspace ID为入参中workspaceId。
    

### **App ID**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9268853471/p935592.png)

1.  访问**[应用广场](https://bailian.console.aliyun.com/#/app-market)**页面，点击通义晓蜜CCAI-对话分析AIO的**查看详情**。
    
2.  点击上方**我的应用**，展示应用卡片列表。
    
3.  每个卡片上的应用ID即为需要获取的App ID。
    

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

## 代码示例

**说明**

请用已获取的Workspace ID替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，App ID替换示例中的YOUR\_APPID，代码才能正常运行。为防止密钥泄露，建议将AccessKeyID和AccessKeySecret设置为环境变量。

## 同步非流失调用

```
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class CcaiPaasTest {

  public static void main(String[] args) throws Exception{
        String accessKeyId = "YOUR_ACCESS_KEY_ID";
        String accessKeySecret = "YOUR_ACCESS_KEY_SECRET";
        String workspaceId = "YOUR_WORKSPACEID";
        String appId = "YOUR_APPID";

        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);

        AnalyzeImageRequest request = new AnalyzeImageRequest();
        request.setStream(false);
        request.setResultTypes(Arrays.asList("watermark"));

        List<String> imageList = new ArrayList<>();
        imageList.add("http://img.alicdn.com/imgextra/i3/O1CN01sRvtsv1WKi6WlKiiP_!!6000000002770-0-tps-1024-1024.jpg");
        request.setImageUrls(imageList);

        AnalyzeImageResponse response=client.analyzeImage(workspaceId,appId,request);
        System.out.println(response);
    }
     
}
```

## 异步非流式调用

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

        List<String> imageList = new ArrayList<>();
        imageList.add("https://img.alicdn.com/imgextra/i3/O1CN01sRvtsv1WKi6WlKiiP_!!6000000002770-0-tps-1024-1024.jpg");

        AnalyzeImageRequest request =  AnalyzeImageRequest.builder().appId(appId).workspaceId(workspaceId)
                .resultTypes(Arrays.asList("watermark")).stream(false).imageUrls(imageList).build();

        CompletableFuture<AnalyzeImageResponse> x = client.analyzeImage(request);
        AnalyzeImageResponse generateCompletionResponse = x.get(10, TimeUnit.SECONDS);
        System.out.println("ALL**********************");
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody()));
        System.out.println(generateCompletionResponse.getBody().getRequestId());
       
    }
}
```

## 异步流式调用

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

        List<String> imageList = new ArrayList<>();
        imageList.add("https://img.alicdn.com/imgextra/i3/O1CN01sRvtsv1WKi6WlKiiP_!!6000000002770-0-tps-1024-1024.jpg");
        
        AnalyzeImageRequest request = AnalyzeImageRequest.builder().appId(appId).workspaceId(workspaceId)
                .resultTypes(Arrays.asList("watermark")).stream(true).imageUrls(imageList).build();

        ResponseIterable<AnalyzeImageResponseBody> x = client.analyzeImageWithResponseIterable(request);
        ResponseIterator<AnalyzeImageResponseBody> iterator = x.iterator();
        String lastTxt = "";
        while (iterator.hasNext()) {
            AnalyzeImageResponseBody event = iterator.next();
            lastTxt = event.getText();
            System.out.println(JSON.toJSONString(event));
        }

        System.out.println("ALL***********************");
        System.out.println(lastTxt);
        System.out.println("请求成功的请求头值：");
    }
}
```
