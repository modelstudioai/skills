# 通过上传离线任务数据进行通义晓蜜CCAI-对话分析

本文向您介绍一个通过上传离线任务数据进行通义晓蜜CCAI-对话分析的最佳实践。

-   关于Java SDK的更多说明，请参见[开始使用](https://help.aliyun.com/zh/sdk/developer-reference/get-started-with-alibaba-cloud-classic-sdk-for-java)。
    
-   关于各API的详细出入参说明，请参见[API目录](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-dir/)。
    

## 前提条件

-   如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。
    

## **获取**Workspace **ID和App ID**

### **Workspace ID**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1229853471/p935590.png)

1.  访问[**业务空间管理**](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面。
    
2.  在业务空间管理列表中获取的Workspace ID为入参中workspaceId。
    

### **App ID**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1229853471/p935591.png)

1.  访问**[应用广场](https://bailian.console.aliyun.com/#/app-market)**页面，点击**应用实践**。
    
2.  在应用实践列表中找到点击通义晓蜜CCAI-对话分析AIO的**立即查看**。
    
3.  点击上方**我的应用**，展示应用卡片列表。
    
4.  每个卡片上的应用ID即为需要获取的App ID。
    

## 安装SDK

## 同步Java

<dependency>

<groupId>com.aliyun</groupId>

<artifactId>contactcenterai20240603</artifactId>

<version>3.6.4</version>

</dependency>

## 代码示例

**说明**

请用已获取的Workspace ID替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，App ID替换示例中的YOUR\_APPID，代码才能正常运行。为防止密钥泄露，建议将AccessKeyID和AccessKeySecret设置为环境变量。

## 创建语音任务

```
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import lombok.extern.slf4j.Slf4j;
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

        CreateTaskRequest request=new CreateTaskRequest();

    
        request.setTaskType("audio");
        request.setResultTypes(Arrays.asList("summary"));
        request.setModelCode("tyxmPlus");

        CreateTaskRequest.CreateTaskRequestTranscription transcription=new CreateTaskRequest.CreateTaskRequestTranscription();
        transcription.setFileName("***.mkv");
        transcription.setVoiceFileUrl("https://***.oss-cn-beijing.aliyuncs.com/****/***.mkv");
        request.setTranscription(transcription);

        CreateTaskResponse response=client.createTask(workspaceId,appId,request);
        System.out.println(JSONObject.toJSONString(response.getBody()));
    }
     
}
```

## 创建文本任务

```
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import lombok.extern.slf4j.Slf4j;
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

        CreateTaskRequest request=new CreateTaskRequest();

        CreateTaskRequest.CreateTaskRequestDialogue dialogue = new CreateTaskRequest.CreateTaskRequestDialogue();

        List<CreateTaskRequest.CreateTaskRequestDialogueSentences> sentences = new ArrayList<>();
        CreateTaskRequest.CreateTaskRequestDialogueSentences sentences1 = new CreateTaskRequest.CreateTaskRequestDialogueSentences();
        sentences1.setRole("agent");
        sentences1.setText("请问有什么事，你什么性别,胖不胖");
        sentences.add(sentences1);

        CreateTaskRequest.CreateTaskRequestDialogueSentences  sentences2 = new  CreateTaskRequest.CreateTaskRequestDialogueSentences ();
        sentences2.setRole("user");
        sentences2.setText("我要买保险，我是男的，很瘦");
        sentences.add(sentences2);
        dialogue.setSentences(sentences);
        dialogue.setSessionId("sessionId-01");

        request.setDialogue(dialogue);
        
        request.setTaskType("text");
        request.setResultTypes(Arrays.asList("summary"));
        request.setModelCode("tyxmPlus");

        CreateTaskResponse response=client.createTask(workspaceId,appId,request);
        System.out.println(JSONObject.toJSONString(response.getBody()));
    }

 
}
```

## 获取任务结果

```
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import lombok.extern.slf4j.Slf4j;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class CcaiPaasTest {   
    
    public static void main(String[] args) throws Exception{
        String accessKeyId = "YOUR_ACCESS_KEY_ID";
        String accessKeySecret = "YOUR_ACCESS_KEY_SECRET";
     
        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);

        String taskId = "*****-****-****-*****-****";
        GetTaskResultRequest request = new GetTaskResultRequest();
        request.setTaskId(taskId);
        GetTaskResultResponse response = client.getTaskResult(request);
        System.out.println(JSONObject.toJSONString(response));
    }
}
```

## **相关文档**

关于任务类型，请参[通过上传离线任务数据进行通义晓蜜CCAI-对话分析](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-createtask)见中resultTypes字段的描述。
