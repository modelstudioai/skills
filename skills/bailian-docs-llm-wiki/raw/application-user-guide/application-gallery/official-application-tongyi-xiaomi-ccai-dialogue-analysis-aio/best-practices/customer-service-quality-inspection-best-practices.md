# 客服服务质检最佳实践

本文向您介绍一个通过通义晓蜜CCAI-AIO对话分析进行客服服务质检的最佳实践。

## **应用场景**

通过通义晓蜜CCAI-AIO的服务质检能力，分析客服和用户的对话记录（文本、录音文件）、发现客服的服务质量问题，进而提升客服服务效率、服务规范，提升客户体验。

## **方案概览**

使用通义晓蜜CCAI-AIO对话分析进行服务质检，只需几步：

1.  开通阿里云百炼服务：首先我们需要开通阿里云百炼服务，开通调用服务后才能测试模型体验、调用模型或应用体验服务。
    
2.  开通并创建通义晓蜜CCAI-AIO对话分析应用：通过阿里云百炼创建一个通义晓蜜CCAI-AIO对话分析应用，并获取调用通义晓蜜CCAI-AIO对话分析应用 API 的相关凭证。
    
3.  基于API实现对话分析：安装SDK，填充API中应用信息，对话内容和质检项，进行对话分析。
    

## **方案架构**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0924970771/CAEQURiBgIDOp7TjnRkiIDUzYjVkNGQ4OTdjZDQ1MjliYWVmMjk5MjEzNzczYTNm4811491_20241206164318.181.svg)

## **开通阿里云百炼服务**

开通阿里云百炼服务：请参考[产品开通](https://help.aliyun.com/zh/model-studio/activate-alibaba-cloud-model-studio)。

## **开通并创建通义晓蜜CCAI-AIO对话分析应用**

开通通义晓蜜CCAI-AIO对话分析并创建应用，请参考[使用指南](https://help.aliyun.com/zh/model-studio/tongyi-xiaomi-ccai-aio-user-guide/)。

## **获取AccessKeyID和AccessKeySecret**

如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。

如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。

## **获取Workspace ID和App ID**

获取Workspace ID和App ID，请参考[获取APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

## 安装SDK

## Java

<dependency>

<groupId>com.aliyun</groupId>

<artifactId>contactcenterai20240603</artifactId>

<version>3.6.4</version>

</dependency>

## 代码示例

**说明**

请用workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。为防止密钥泄露，建议将AccessKeyID和AccessKeySecret设置为环境变量。

## 同步非流式调用

Java

```
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.aliyun.contactcenterai20240603.Client;
import com.aliyun.contactcenterai20240603.models.*;
import com.aliyun.teaopenapi.models.Config;
import java.util.*;

public class CcaiPaasTest {

    public static void main(String[] args) throws Exception {

        //建议用户配置env防止ak泄漏
        String accessKeyId = "YOUR_ACCESS_KEY_ID";
        String accessKeySecret = "YOUR_ACCESS_KEY_SECRET";
        String workspaceId = "YOUR_WORKSPACEID";
        String appId = "YOUR_APPID";

        Config config = new Config();
        config.setAccessKeyId(accessKeyId).setAccessKeySecret(accessKeySecret).setEndpoint("contactcenterai.cn-shanghai.aliyuncs.com")
                .setRegionId("cn-shanghai").setProtocol("HTTPS");

        Client client = new Client(config);
        AnalyzeConversationRequest request = new AnalyzeConversationRequest();

        AnalyzeConversationRequest.AnalyzeConversationRequestDialogue dialogue = new AnalyzeConversationRequest.AnalyzeConversationRequestDialogue();
        
        // 对话内容
        List<AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences> sentenceList = new ArrayList<>();
        AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences sentences1 = new AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences();
        sentences1.setRole("agent");
        sentences1.setText("您好，这里是xxx保险公司，请问有什么可以帮您");
        sentenceList.add(sentences1);

        AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences sentences2 = new AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences();
        sentences2.setRole("user");
        sentences2.setText("嗯，我想办理一个健康险，帮我介绍下有哪些");
        sentenceList.add(sentences2);
        
        dialogue.setSentences(sentenceList);
        dialogue.setSessionId("session-adslsddxxxx");
        request.setDialogue(dialogue);

        AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspection serviceInspection = new AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspection();
        List<AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspectionInspectionContents> inspectionContents = new ArrayList<>();

        // 质检项定义
        AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspectionInspectionContents content1 = new AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspectionInspectionContents();
        content1.setTitle("客服是否过度承诺");
        content1.setContent("客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。");
        inspectionContents.add(content1);
        
        AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspectionInspectionContents content2 = new AnalyzeConversationRequest.AnalyzeConversationRequestServiceInspectionInspectionContents();
        content2.setTitle("客户情绪是否正向");
        content2.setContent("分析对话内容，输出用户在对话中表现出的情绪，详细要求：a. 当客户表现出负面情绪时，判定为消极；b. 当客户表现中积极情绪时，判定为积极；c. 如果客户文本没有明显的消极或积极情感色彩，则判定为中性。");
        inspectionContents.add(content2);
        

        serviceInspection.setInspectionContents(inspectionContents);
        serviceInspection.setInspectionIntroduction("请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等");
        serviceInspection.setSceneIntroduction("保险销售场景");

        request.setServiceInspection(serviceInspection);
        // service_inspection表示服务质检任务
        request.setResultTypes(Arrays.asList("service_inspection"));
        request.setStream(false);

        com.aliyun.contactcenterai20240603.models.AnalyzeConversationResponse response = client.analyzeConversation(workspaceId, appId, request);
        System.out.println(JSONObject.toJSONString(response));
    }

}
```
