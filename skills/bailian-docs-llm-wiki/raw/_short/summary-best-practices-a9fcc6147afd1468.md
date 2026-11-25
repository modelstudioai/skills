# 摘要生成（含摘要/标题/关键词）最佳实践

本文向您介绍一个通过伶鹊CCAI-AIO对话分析进行摘要总结的最佳实践。

<a id="应用场景"></a>

<a id="5527a21767t3r"></a>

## 应用场景

通过伶鹊CCAI-AIO的总结摘要能力自动提取文档中的重要信息，如对话摘要总结、标题生成、关键词等，从而提高工作效率，减少人工处理成本。

<a id="方案概览"></a>

<a id="e897314a7eoue"></a>

## 方案概览

使用伶鹊CCAI-AIO对话分析进行摘要总结，只需几步：

1.  开通阿里云百炼服务：首先我们需要开通阿里云百炼服务，开通调用服务后才能测试模型体验、调用模型或应用体验服务。
2.  开通并创建伶鹊CCAI-AIO对话分析应用：通过阿里云百炼创建一个伶鹊CCAI-AIO对话分析应用，并获取调用伶鹊CCAI-AIO对话分析应用 API 的相关凭证。
3.  基于API实现对话分析：安装SDK，填充API中应用信息和对话内容，进行摘要总结。

<a id="方案架构"></a>

<a id="cb4403a188p6y"></a>

## 方案架构

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8779763871/CAEQURiBgMCMwbTpnRkiIGY5ODI0YzFiZjA5MTQ2MjhhNGUzYTVmNThjYWQyODdl4811491_20241206164318.181.svg)

<a id="开通阿里云百炼服务"></a>

<a id="15a8e219c1a4i"></a>

## 开通阿里云百炼服务

开通阿里云百炼服务：请参考[产品开通](https://help.aliyun.com/zh/model-studio/activate-alibaba-cloud-model-studio)。

<a id="开通并创建伶鹊ccai-aio对话分析应用"></a>

<a id="138d1b2939q5y"></a>

## 开通并创建伶鹊CCAI-AIO对话分析应用

开通并创建伶鹊CCAI-AIO对话分析并创建应用，请参考[使用指南](lingque-ccai-aio-user-guide-d428f7e859327f56.md)。

<a id="获取accesskeyid和accesskeysecret"></a>

<a id="65d90f1480kyk"></a>

## 获取AccessKeyID和AccessKeySecret

如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。

如果您使用子账号调用接口，请参考[伶鹊CCAI-对话分析RAM子账号使用方式和授权操作](use-and-authorize-ram-users-for-ccai-dialogue-an-e83b0ec9dc63d2ff.md)。

<a id="获取workspace-id和app-id"></a>

<a id="f30c7d3d31yvp"></a>

## 获取Workspace ID和App ID

获取Workspace ID和App ID，请参考[获取APP ID 和 Workspace ID](../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md)。

<a id="安装sdk"></a>

<a id="acd7931e70w6n"></a>

## 安装SDK

<a id="sec-tabs"></a>

<a id="java"></a>

<a id="java-h4"></a>

#### Java

<dependency>

<groupId>com.aliyun</groupId>

<artifactId>contactcenterai20240603</artifactId>

<version>3.6.4</version>

</dependency>

<a id="代码示例"></a>

<a id="33bc2083e24y0"></a>

## 代码示例

> **说明**
>
> 请用workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。为防止密钥泄露，建议将AccessKeyID和AccessKeySecret设置为环境变量。

<a id="sec-tabs-2"></a>

<a id="同步非流式调用"></a>

<a id="同步非流式调用-h4"></a>

#### 同步非流式调用

<a id="code-block"></a>

```java
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
        com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest request = new com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest();

        com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogue dialogue = new com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogue();
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

        // summary 表示总结摘要任务
        // keywords 表示关键词抽取
        // title 表示抽取标题
        request.setResultTypes(Arrays.asList("summary"));
        request.setStream(false);

        com.aliyun.contactcenterai20240603.models.AnalyzeConversationResponse response = client.analyzeConversation(workspaceId, appId, request);
        System.out.println(JSONObject.toJSONString(response));
    }

}
```
