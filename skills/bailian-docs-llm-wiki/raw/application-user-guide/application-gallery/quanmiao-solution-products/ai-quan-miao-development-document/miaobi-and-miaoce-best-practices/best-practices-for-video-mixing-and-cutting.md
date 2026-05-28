# 全妙视频混剪最佳实践

本文档是关于全妙视频混剪代码调用的操作介绍文档。

## **传统视频剪辑痛点**

传统视频剪辑通常高度依赖专业剪辑软件，操作门槛高、流程繁琐，需要人工完成素材筛选、剪辑、转场、字幕添加等环节，耗时耗力。同时，传统方式难以实现批量处理和自动化生成，尤其在面对大量短视频生产需求时，效率低下且成本高昂。

## **视频混剪优势**

视频混剪通过AI技术有效解决了上述痛点：它无需安装复杂软件，支持一键自动剪辑，能够智能识别精彩片段、自动配乐、生成字幕、优化画面节奏，并可基于模板快速批量产出高质量视频。这不仅大幅降低了剪辑门槛，还显著提升了内容生产效率，满足了企业及个人在短视频时代对高效、智能化视频制作的需求。

## **视频混剪支持场景及效果**

目前视频混剪适合的领域是营销广告领域，主要支持三个视频剪辑场景：

1.  基于一个长视频素材，用户输入脚本的主题要求，系统会结合长视频素材和生成的脚本，最后剪辑成一个短视频；
    
2.  基于若干素材视频，用户输入脚本的主题要求，系统会结合多个视频素材和生成的脚本，最后剪辑成一个短视频；
    
3.  模型首先会学习用户上传的样本视频和视频内脚本的特点，基于用户上传的视频素材，用户输入脚本的主题要求，系统会结合学习到的样本视频的特点，以及新的视频素材和脚本内容，最后剪辑成一个新的短视频。
    

## 前提条件

-   获取WorkSpaceId [获取Workspace ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id#732535cfc959h)；
    
-   引入全妙SDK [注意获取最新SDK版本](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc)。
    

使⽤视频混剪功能，是使⽤SDK⽅式，MAVEN依赖如下：

```
<dependency>
 <groupId>com.aliyun</groupId>
 <artifactId>alibabacloud-aimiaobi20230801</artifactId>
 <version>1.0.68</version>
</dependency>
```

**重要**

## **调用前必读**

1.  接口调用顺序：asyncUploadVideo（上传素材阶段）-> asyncCreateClipsTimeLine（生成剪辑timeline阶段）-> asyncCreateClipsTask（生成剪辑视频阶段）；
    
2.  定时使用getAutoClipsTaskInfo获取每个阶段的任务状态，每个阶段结束才能进入下一阶段；
    
3.  视频混剪的接口地址：[妙笔-视频混剪](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-wonderful-pen-video-mixed-cut/)。
    

## **接口调用的步骤**

### **第一步上传视频素材**

1.  上传视频素材；
    

**说明**

视频素材的大小要求：一个视频素材不超过200M，全部视频素材总时长不超过20分钟。

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncUploadVideoRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncUploadVideoResponse;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncUploadVideoRequest.SourceVideos;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncUploadVideoRequest.ReferenceVideo;

public class asyncUploadVideo {
    public static void main(String[] args) {
        try{
            String akSwap = "xxxx";
            String skSwap = "xxxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")
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

            List<SourceVideos> sourceVideos = new ArrayList<>();

            SourceVideos sv001= SourceVideos.builder()
                    .videoUrl("https://xxx")
                    .videoName("万国觉醒-骑兵.mp4")
                    .build();
            sourceVideos.add(sv001);

            SourceVideos sv002 = SourceVideos.builder()
                    .videoUrl("https://xxx")
                    .videoName("万国觉醒-连弩.mp4")
                    .build();
            sourceVideos.add(sv002);

            SourceVideos sv003 = SourceVideos.builder()
                    .videoUrl("https://xxx")
                    .videoName("万国觉醒-白起.mp4")
                    .build();
            sourceVideos.add(sv003);

            /*
            ReferenceVideo refVideo = ReferenceVideo .builder()
                    .videoUrl("https://xxx")
                    .videoName("小紫瓶精华第六代-参考.mp4")
                    .build();
            */

            AsyncUploadVideoRequest request = AsyncUploadVideoRequest.builder()
                    .workspaceId("llm-xxxx")
                    .splitInterval(1)
                    .sourceVideos(sourceVideos)
                    //.referenceVideo(refVideo)
                    .build();

            CompletableFuture<AsyncUploadVideoResponse> future = client.asyncUploadVideo(request);
            AsyncUploadVideoResponse response = future.get();

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

2.  确认视频是否上传成功，上传完成后可操作第二步。
    

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoResponse;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.concurrent.CompletableFuture;

public class getAutoClipsTaskInfo {
    public static void main(String[] args) {
        try{
            String akSwap = "xxxx";
            String skSwap = "xxxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")
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

            GetAutoClipsTaskInfoRequest request = GetAutoClipsTaskInfoRequest.builder()
                    .workspaceId("llm-xxxx")
                    .taskId("xxxx")
                    .build();

            CompletableFuture<GetAutoClipsTaskInfoResponse> future = client.getAutoClipsTaskInfo(request);
            GetAutoClipsTaskInfoResponse response = future.get();

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

### **第二步生成剪辑timeline阶段**

1.  调用接口生成剪辑的timeline；
    

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncCreateClipsTimeLineRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.AsyncCreateClipsTimeLineResponse;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.concurrent.CompletableFuture;

public class asyncCreateClipsTimeLine {
    public static void main(String[] args) {
        try{
            String akSwap = "xxxx";
            String skSwap = "xxxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")// Region ID
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

            AsyncCreateClipsTimeLineRequest request = AsyncCreateClipsTimeLineRequest.builder()
                    .workspaceId("llm-xxxx")
                    .taskId("xxxx")
                    .processPrompt("口播内容是游戏《万国觉醒》的宣传广告，视频中间不要出现\"万国觉醒字样\"，视频的结束画面要有《万国觉醒》字样的画面。")
                    //.processModel("qwen-plus-latest")
                    .customContent("有小伙伴问古代战场，什么兵种可以克制步兵，当然是骑兵！在游戏《万国觉醒》中霍去病带领的大汉铁骑，\n" +
                            "曹操统帅的虎豹骑，不但有10%的行军速度，还有30%的攻击加成，是战场上的碾压步兵的无敌兵种。那小伙伴们又问了《万国觉醒》中有什么兵种可以克制骑兵吗，\n" +
                            "当然有，诸葛亮率领的连弩兵活力迅猛且杀伤力极强，可以在远程对骑兵形成有效压制，骑兵还没有冲过来就已经被诸葛亮的连弩射中身亡了，连弩绝对是杀伤骑兵最有效的兵种。\n" +
                            "虽然骑兵和连弩兵各有特色，一旦以少胜多敌多，还是力不从心。但你可能不知道《万国觉醒》中有一位英雄最擅长以少敌多，他就是杀神白起，白起率领的部队击杀敌人越多，普通伤害就越高，白起更能全面强化\n" +
                            "残血部队的攻防，让其成为名副其实的战场绞肉机，敌人越多约厉害。想体验这一切吗，快来《万国觉醒》战个痛快。")
                    .build();

            CompletableFuture<AsyncCreateClipsTimeLineResponse> future = client.asyncCreateClipsTimeLine(request);
            AsyncCreateClipsTimeLineResponse response = future.get();

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

2.  确认视频剪辑的timeline是否生成完成，生成完成后可操作第三步。
    

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoResponse;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.concurrent.CompletableFuture;

public class getAutoClipsTaskInfo {
    public static void main(String[] args) {
        try{
            String akSwap = "xxxx";
            String skSwap = "xxxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")
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

            GetAutoClipsTaskInfoRequest request = GetAutoClipsTaskInfoRequest.builder()
                    .workspaceId("llm-xxxx")
                    .taskId("xxxx")
                    .build();

            CompletableFuture<GetAutoClipsTaskInfoResponse> future = client.getAutoClipsTaskInfo(request);
            GetAutoClipsTaskInfoResponse response = future.get();

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

### **第三步生成剪辑视频阶段**

1.  最后生成新视频；
    

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.ArrayList;
import java.util.List;

import java.util.concurrent.CompletableFuture;

public class asyncCreateClipsTask {
    public static void main(String[] args) {
        try{
            String akSwap = "xxx";
            String skSwap = "xxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")// Region ID
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

            List<AsyncCreateClipsTaskRequest.ColorWords> colorWords = new ArrayList<>();
            AsyncCreateClipsTaskRequest.ColorWords cw = AsyncCreateClipsTaskRequest.ColorWords.builder()
                    .y(0.1F)
                    .x(0.1F)
                    .content("冰川保湿露，随时补水")
                    .effectColorStyle("CS0002-000007")
                    .fontSize(120)
                    .timelineIn(0)
                    .timelineOut(5)
                    .build();
            colorWords.add(cw);
            AsyncCreateClipsTaskRequest request = AsyncCreateClipsTaskRequest.builder()
                    .workspaceId("llm-xxx")
                    .taskId("xxx")
                    //.colorWords(colorWords)
                    .build();

            CompletableFuture<AsyncCreateClipsTaskResponse> future = client.asyncCreateClipsTask(request);
            AsyncCreateClipsTaskResponse response = future.get();

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

2.  确认新视频是否剪辑完成。
    

```
package com.aliyun.sdk.service.aimiaobi20230801;

import com.alibaba.fastjson.JSON;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAutoClipsTaskInfoResponse;
import com.aliyun.sdk.service.aimiaobi20230801.utils.Util;
import darabonba.core.client.ClientOverrideConfiguration;

import java.util.concurrent.CompletableFuture;

public class getAutoClipsTaskInfo {
    public static void main(String[] args) {
        try{
            String akSwap = "xxxx";
            String skSwap = "xxxx";

            StaticCredentialProvider provider = StaticCredentialProvider.create(
                    Credential.builder()
                            .accessKeyId(akSwap)
                            .accessKeySecret(skSwap)
                            .build()
            );

            AsyncClient client = AsyncClient.builder()
                    .region("cn-beijing")
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

            GetAutoClipsTaskInfoRequest request = GetAutoClipsTaskInfoRequest.builder()
                    .workspaceId("llm-xxxx")
                    .taskId("xxxx")
                    .build();

            CompletableFuture<GetAutoClipsTaskInfoResponse> future = client.getAutoClipsTaskInfo(request);
            GetAutoClipsTaskInfoResponse response = future.get();

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
