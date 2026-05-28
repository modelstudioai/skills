# 妙读最佳实践

本文提供妙读写作链路 API的几个最佳实践，帮助您快速入门并开发您自己的业务应用。

## 前提条件

-   已开通服务；
    
-   获取WorkSpaceId [获取Workspace ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id#732535cfc959h)；
    
-   引入妙读SDK [注意获取最新SDK版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)。
    

使⽤妙读功能，是使⽤SDK⽅式，MAVEN依赖如下：

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>1.0.86</version>
</dependency>
```

## **操作步骤**

### **第一步：上传文档到文档库**

通过[UploadDoc - 文档上传](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploaddoc)接口上传文档到妙读文档库，如下为示例代码：

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.UploadDocRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.UploadDocResponse;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.List;

import java.util.concurrent.CompletableFuture;

/**
 * packageName quanmiao
 *
 * @author zhujin
 * @version JDK 8
 * @className uploadDocTest
 * @date 2024/8/15
 * @description 文档上传测试
 */
public class uploadDocTest {
    public static void main(String[] args) {
        try{

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(Constant.accessKeyId)
                            .accessKeySecret(Constant.accessKeySecret)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing") // Region ID
                    .credentialsProvider(provider)
                    .serviceConfiguration(Configuration.create()
                            .setSignatureVersion(SignatureVersion.V3)
                    )
                    .overrideConfiguration(
                            ClientOverrideConfiguration.create()
                                    .setProtocol("HTTPS")
                                    .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                    )
                    .build();

            List<UploadDocRequest.Docs> docsList = new ArrayList<>();
            UploadDocRequest.Docs doc = UploadDocRequest.Docs.builder()
                    .docName("测试文档.pdf")
                    .fileUrl("https://xxx.oss-cn-beijing.aliyuncs.com/test/测试文档.pdf")
                    .build();
            docsList.add(doc);

            UploadDocRequest request = UploadDocRequest.builder()
                    .workspaceId(Constant.workspaceId)
                    .docs(docsList)
                    .build();

            CompletableFuture<UploadDocResponse> future = client.uploadDoc(request);

            UploadDocResponse response = future.get();

            System.out.println("ALL***********************");
            System.out.println("请求成功的请求头值：");
            System.out.println(response.getStatusCode());
            System.out.println(response.getHeaders());
            String jsonStr = JSON.toJSONString(response.getBody());
            System.out.println(jsonStr);
        }catch (Exception ex){
            System.out.println("///////exception happen is " + ex);
        }
    }
}
```

### **第二步：获得上传的⽂档信息**

上传完文档后需要使用[GetDocInfo - 获取文档信息](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocinfo)接口获取文档是否上传成功的信息。

```
import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetDocInfoRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetDocInfoResponse;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import darabonba.core.client.ClientOverrideConfiguration;
import java.util.concurrent.CompletableFuture;
public class getDocInfo {
 public static void main(String[] args) {
 try{
 StaticCredentialProvider provider = StaticCredentialProvider.create(
 Credential.builder()
 .accessKeyId("")
 .accessKeySecret("")
 .build()
 );
 AsyncClient client = AsyncClient.builder()
 .region("cn-beijing") // Region ID
 .credentialsProvider(provider)
 // Service-level configuration
 .serviceConfiguration(Configuration.create()
 .setSignatureVersion(SignatureVersion.V3)
 )
 // Client-level configuration rewrite, can set Endpoint, Http request parameters, etc.
 .overrideConfiguration(
 ClientOverrideConfiguration.create()
 .setProtocol("HTTPS")
 .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
 )
 .build();
 GetDocInfoRequest request = GetDocInfoRequest.builder()
 .workspaceId("llm-xxx")
 .docId("xxx")
 .build();
CompletableFuture<GetDocInfoResponse> future = client.getDocInfo(request);
 GetDocInfoResponse response = future.get();
 System.out.println("ALL***********************");
 System.out.println("请求成功的请求头值：");
 System.out.println(response.getStatusCode());
 System.out.println(response.getHeaders());
 String jsonStr = JSON.toJSONString(response.getBody());
 System.out.println(jsonStr);
 }catch (Exception ex){
 System.out.println("///////exception happen is " + ex);
             }
      }
 }
```

### **第三步：文档辅助阅读能力（包含导读、脑图、问答等）**

您可以为指定的文档进行辅助阅读的操作，妙读提供导读、脑图、文档问答等辅助阅读能力。下面是文档导读、全文脑图、文档问答的示例代码：

1.  ##### [RunDocIntroduction - 文档导读](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocintroduction)
    

-   针对一篇文章、视频或者URL，生成文章的导读内容，包含全文总结、关键要点、章节速览（即分段、每段的总结、段落摘要）。此外支持多种多语言的输入和输出。
    
-   如果用户仅需要对文章进行全文总结，可使用RunDocSummary接口实现，具体请参《[RunDocSummary - 文档摘要](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocsummary)》。
    

如下为示例代码：

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import com.google.gson.Gson;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

/**
 * packageName quanmiao
 *
 * @author zhujin
 * @version JDK 8
 * @className runDocIntroductionTest
 * @date 2024/8/15
 * @description 文档导读测试
 */
public class runDocIntroductionTest {
    public static void main(String[] args) {
        try{

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(Constant.accessKeyId)
                            .accessKeySecret(Constant.accessKeySecret)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing") // Region ID
                    .credentialsProvider(provider)
                    .serviceConfiguration(Configuration.create()
                            .setSignatureVersion(SignatureVersion.V3)
                    )
                    .overrideConfiguration(
                            ClientOverrideConfiguration.create()
                                    .setProtocol("HTTPS")
                                    .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                    )
                    .build();

            RunDocIntroductionRequest request = RunDocIntroductionRequest.builder()
                    .workspaceId(Constant.workspaceId)
                    .sessionId("sessionId_xxx")
                    .docId("xxxx-xxx-xxxx-xxx-xxxxxxx")
                    .build();

            ResponseIterable<RunDocIntroductionResponseBody> x = client.runDocIntroductionWithResponseIterable(request);

            ResponseIterator<RunDocIntroductionResponseBody> iterator = x.iterator();
            while (iterator.hasNext()) {
                System.out.println("----event----");
                RunDocIntroductionResponseBody event = iterator.next();
                System.out.println(new Gson().toJson(event));
                //System.out.println(event.getMessage());
            }

            System.out.println("ALL***********************");
            System.out.println("请求成功的请求头值：");
            System.out.println(x.getStatusCode());
            System.out.println(x.getHeaders());
        }catch (Exception ex){
            System.out.println("///////exception happen is " + ex);
        }
    }
}
```

2.  ##### [RunDocBrainmap - 全文脑图](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocbrainmap)
    

-   针对文章或者书，生成三级脑图，且支持生成多语种，支持控制脑图第二级数量，支持控制叶子节点的字数。
    

如下为示例代码：

```
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunDocBrainmapRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunDocBrainmapResponseBody;
import com.google.gson.Gson;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

public class runDocBrainmap {
    public static void main(String[] args) {
        try {
            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId("")
                            .accessKeySecret("")
                            .build()
            );
            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing") // Region ID
                    .credentialsProvider(provider)
                    // Service-level configuration
                    .serviceConfiguration(Configuration.create()
                            .setSignatureVersion(SignatureVersion.V3)
                    )
                    // Client-level configuration rewrite, can set Endpoint, Http request parameters, etc.
                    .overrideConfiguration(
                            ClientOverrideConfiguration.create()
                                    .setProtocol("HTTPS")
                                    .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                    )
                    .build();
            RunDocBrainmapRequest request = RunDocBrainmapRequest.builder()
                    .workspaceId("llm-xxx")
                    .sessionId("sessionId_test")
                    .docId("xxxxx")
                    .build();
            ResponseIterable<RunDocBrainmapResponseBody> x = client.runDocBrainmapWithResponseIterable(request);
            ResponseIterator<RunDocBrainmapResponseBody> iterator = x.iterator();
            while (iterator.hasNext()) {
                System.out.println("----event----");
                RunDocBrainmapResponseBody event = iterator.next();
                System.out.println(new Gson().toJson(event));
                //System.out.println(event.getMessage());
            }
            System.out.println("ALL***********************");
            System.out.println("请求成功的请求头值：");
            System.out.println(x.getStatusCode());
            System.out.println(x.getHeaders());
        } catch (Exception ex) {
            System.out.println("///////exception happen is " + ex);
        }
    }
}
```

2.  ##### [RunDocQa - 文档问答（文章问答/多模态文件问答）](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-rundocqa)
    

-   针对一个自然语言类的query，在指定的文章范围内给出文字答案（有图则会配图），并显示溯源信息。 多模态文件问答：针对一个自然语言类的query，在指定的多模态文件范围内给出文字答案，并带上相关的图片、视频片段或者文字，并显示溯源信息。
    

如下为示例代码：

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunDocQaRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.RunDocQaResponseBody;
import com.google.gson.Gson;
import darabonba.core.ResponseIterable;
import darabonba.core.ResponseIterator;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.List;

/**
 * packageName quanmiao
 *
 * @author zhujin
 * @version JDK 8
 * @className runDocQATest
 * @date 2024/8/15
 * @description 文档问答测试
 */
public class runDocQATest {
    public static void main(String[] args) {
        try{

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(Constant.accessKeyId)
                            .accessKeySecret(Constant.accessKeySecret)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing") // Region ID
                    .credentialsProvider(provider)
                    .serviceConfiguration(Configuration.create()
                            .setSignatureVersion(SignatureVersion.V3)
                    )
                    .overrideConfiguration(
                            ClientOverrideConfiguration.create()
                                    .setProtocol("HTTPS")
                                    .setEndpointOverride("aimiaobi.cn-beijing.aliyuncs.com")
                    )
                    .build();

            List<String> docIds = new ArrayList<>();
            docIds.add("xxx-xxxx-xxxx-xxx-xxxxxxx");

            RunDocQaRequest   request = RunDocQaRequest .builder()
                    .workspaceId(Constant.workspaceId)
                    .sessionId("sessionId_xxx")
                    .searchSource("fromDoc")
                    .query("ai妙读能够实现什么功能")
                    .docIds(docIds)
                    .build();

            ResponseIterable<RunDocQaResponseBody> x = client.runDocQaWithResponseIterable(request); 

            ResponseIterator<RunDocQaResponseBody> iterator = x.iterator();
            while (iterator.hasNext()) {
                System.out.println("----event----");
                RunDocQaResponseBody event = iterator.next();
                System.out.println(new Gson().toJson(event));
                //System.out.println(event.getMessage());
            }

            System.out.println("ALL***********************");
            System.out.println("请求成功的请求头值：");
            System.out.println(x.getStatusCode());
            System.out.println(x.getHeaders());
        }catch (Exception ex){
            System.out.println("///////exception happen is " + ex);
        }
    }
}
```

## **接口调用常见FAQ**

问：文件上传成功后，马上调用妙读的导读和脑图的接口时，为什么返回的Errorcode是Failed，显示文件内容为空？

答：[UploadDoc - 文档上传](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-uploaddoc)为异步调用接口，需要先用[GetDocInfo - 获取文档信息](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-getdocinfo)接口获取其真实的状态，当状态为成功后，才可对文档进行生成文档脑图、文档摘要、进行文档问答等操作。
