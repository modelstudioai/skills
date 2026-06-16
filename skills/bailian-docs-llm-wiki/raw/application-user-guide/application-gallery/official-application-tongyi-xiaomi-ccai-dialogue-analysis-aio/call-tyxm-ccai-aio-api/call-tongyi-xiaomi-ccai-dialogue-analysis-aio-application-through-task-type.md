# 通过任务类型调用通义晓蜜CCAI-对话分析AIO应用

本文向您介绍通义晓蜜CCAI-对话分析AIO应用Java SDK的安装、使用及注意事项。

-   关于Java SDK的更多说明，请参见[开始使用](https://help.aliyun.com/zh/sdk/developer-reference/get-started-with-alibaba-cloud-classic-sdk-for-java)。
    
-   关于各API的详细出入参说明，请参见[API目录](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-dir/)。
    
-   关于任务类型，请参见[通过任务类型调用通义晓蜜CCAI-对话分析AIO应用](https://help.aliyun.com/zh/model-studio/api-contactcenterai-2024-06-03-analyzeconversation)中resultTypes字段的描述。
    

## 前提条件

-   如果您还未创建AccessKeyID和AccessKeySecret，请参考[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   如果您使用子账号调用接口，请参考[通义晓蜜CCAI-对话分析RAM子账号使用方式和授权操作](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-users-for-ccai-dialogue-analysis)。
    

## **获取workspaceId和appId**

### **workspaceId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6398853471/p935587.png)

1.  访问[**业务空间管理**](https://bailian.console.aliyun.com/?admin=1#/efm/business_management)页面。
    
2.  业务空间管理列表中Workspace ID为入参中workspaceId。
    

### **appId**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6398853471/p935588.png)

1.  访问**[应用广场](https://bailian.console.aliyun.com/#/app-market)**页面，点击通义晓蜜CCAI-对话分析AIO的**查看详情**。
    
2.  点击上方**我的应用**，展示应用卡片列表。
    
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

## 代码示例

**说明**

请用workspaceId替换示例中的YOUR\_WORKSPACEID，AccessKeyID替换示例中的YOUR\_ACCESS\_KEY\_ID，AccessKeySecret替换示例中的YOUR\_ACCESS\_KEY\_SECRET，appId替换示例中的YOUR\_APPID，代码才能正常运行。为防止密钥泄露，建议将AccessKeyID和AccessKeySecret设置为环境变量。

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

        List<AnalyzeConversationRequest.Sentences>  messageList = new ArrayList<>();
        messageList.add(AnalyzeConversationRequest.Sentences.builder().role("agent").text("请问您想咨询五险一金哪方面的问题呢").build());
        messageList.add(AnalyzeConversationRequest.Sentences.builder().role("user").text("怎么领取五险一金呢").build());

        List<String> resultTypes=new ArrayList<>();
        resultTypes.add("summary");

        AnalyzeConversationRequest.Dialogue dialogue=AnalyzeConversationRequest.Dialogue.builder().sessionId("session-01")
                .sentences(messageList).build();

        AnalyzeConversationRequest completionParam = AnalyzeConversationRequest.builder().modelCode("tyxmPlus").resultTypes(resultTypes)
                .workspaceId(workspaceId).appId(appId).dialogue(dialogue).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).stream(true).build();
        System.out.println(JSON.toJSONString(completionParam));

        ResponseIterable<AnalyzeConversationResponseBody> x = client.analyzeConversationWithResponseIterable(completionParam);
        ResponseIterator<AnalyzeConversationResponseBody> iterator = x.iterator();
        String lastTxt="";
        while (iterator.hasNext()) {
            AnalyzeConversationResponseBody event = iterator.next();
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

    public static void main(String[] args) throws Exception{

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
        List<com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences> sentenceList = new ArrayList<>();
        com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences sentences1 = new com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences();
        sentences1.setRole("agent");
        sentences1.setText("请问您想咨询五险一金哪方面的问题呢");
        sentenceList.add(sentences1);

        com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences sentences2 = new com.aliyun.contactcenterai20240603.models.AnalyzeConversationRequest.AnalyzeConversationRequestDialogueSentences();
        sentences2.setRole("user");
        sentences2.setText("怎么查询账户呢");
        sentenceList.add(sentences2);
        dialogue.setSentences(sentenceList);
        dialogue.setSessionId("session-1111");
        request.setDialogue(dialogue);

        request.setSceneName("中国移动");
        request.setResultTypes(Arrays.asList("summary"));
        request.setStream(false);

        com.aliyun.contactcenterai20240603.models.AnalyzeConversationResponse response = client.analyzeConversation(workspaceId, appId, request);
        System.out.println(JSONObject.toJSONString(response));
    }

}
```

Go

```
// 示例代码，其中阿里云AK、SK，CCAI的业务空间ID（workspaceId）和应用ID（appId），替换为用户当前的。
// tea-utils使用这个版本，go get github.com/alibabacloud-go/tea-utils/v2@v2.0.5-0.20240708091240-f3d7eca052de

// This file is auto-generated, don't edit it. Thanks.
package main

import (
	"fmt"
	"io"
	"os"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	openapiutil "github.com/alibabacloud-go/openapi-util/service"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

/**
 * API 相关
 * @param path params
 * @return OpenApi.Params
 */
func CreateApiInfo() (_result *openapi.Params) {
	params := &openapi.Params{
		// 接口名称
		Action: tea.String("AnalyzeConversation"),
		// 接口版本
		Version: tea.String("2024-06-03"),
		// 接口协议
		Protocol: tea.String("HTTPS"),
		// 接口 HTTP 方法
		Method:   tea.String("POST"),
		AuthType: tea.String("AK"),
		Style:    tea.String("ROA"),
		// 接口 PATH
		Pathname: tea.String("/YOUR_CCAI_WORKSPACEID/ccai/app/YOUR_CCAI_APP_ID/analyze_conversation"),
		// 接口请求体内容格式
		ReqBodyType: tea.String("json"),
		// 接口响应体内容格式，注意一定得是binary格式，CallApi才会透传出response body进行ReadAsSSE
		BodyType: tea.String("binary"),
	}
	_result = params
	return _result
}

func _main(args []*string) (_err error) {
	// 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
	// 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378661.html。
	config := &openapi.Config{
		AccessKeyId:     tea.String("YOUR_ALIYUN_AK"),
		AccessKeySecret: tea.String("YOUR_ALIYUN_SK"),
	}
	config.Endpoint = tea.String("contactcenterai.cn-shanghai.aliyuncs.com")
	client, err := openapi.NewClient(config)
	if err != nil {
		return err
	}

	params := CreateApiInfo()
	// query params
	queries := map[string]interface{}{}
	queries["workspaceId"] = tea.String("YOUR_CCAI_WORKSPACEID")
	queries["appId"] = tea.String("YOUR_CCAI_APP_ID")

	body := map[string]interface{}{
		"dialogue": map[string]interface{}{
			"sentences": []map[string]*string{map[string]*string{
				"role": tea.String("agent"),
				"text": tea.String("您好，请问有什么问题需要解决"),
			}, map[string]*string{
				"role": tea.String("user"),
				"text": tea.String("怎么领取游戏币呢"),
			}, map[string]*string{
				"role": tea.String("agent"),
				"text": tea.String("请登录个人账号，在账号下，看看是否有推荐的待领取的游戏币呢，如果有会推送给您的"),
			}, map[string]*string{
				"role": tea.String("user"),
				"text": tea.String("好，谢谢"),
			}},
			"sessionId": "2323",
		},
		"modelCode":   "tyxmPlus",
		"resultTypes": []*string{tea.String("question_solution")},
		"stream":      false,
	}

	// runtime options
	runtime := &util.RuntimeOptions{}
	request := &openapi.OpenApiRequest{
		Query: openapiutil.Query(queries),
		Body:  body,
		//Body:  tea.String("{\n  \"stream\": false,\n  \"modelCode\": \"tyxmPlus\",\n  \"dialogue\": {\n    \"sentences\": [\n      {\n        \"role\": \"user\",\n        \"text\": \"号主开挂了模拟宇宙无线祝福\\n联系方式: ******\\n图片上传:\\n视频上传:\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"乘客您好，欢迎登录本次星穹列车帕~麻烦您提供一下以下信息：*游戏项目：\\n*被举报角色UID：\"\n      },\n      {\n        \"role\": \"user\",\n        \"text\": \"通行证id******\\n\\n2024-06-10 18:25:52 [玩家] ***:\\nuid******\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"您的问题我们之前已经记录反馈了，会进行核实的~如有结果我们会在服务进度或在线服务中告知，您可以留意相关提示。十分抱歉给您带来不便\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"您的问题咨询完成啦，那客服娘贴心提示，不要忘记消耗开拓力哦~祝愿您在完成探索的途中获得美好的回忆哦~希望您抽空也记得给客服娘进行下评价，挥挥~~\\n\"\n      }\n    ],\n    \"sessionId\": \"ss01\"\n  },\n  \"resultTypes\": [\n    \"question_solution\"\n  ],\n  \"serviceInspection\": {\n    \"inspectionIntroduction\": \"请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等\",\n    \"sceneIntroduction\": \"保险销售场景\",\n    \"inspectionContents\": [\n      {\n        \"title\": \"客服是否过度承诺\",\n        \"content\": \"客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。\"\n      }\n    ]\n  },\n  \"fields\": [\n    {\n      \"code\": \"name\",\n      \"name\": \"姓名\",\n      \"desc\": \"用户的姓名\"\n    },\n    {\n      \"code\": \"question\",\n      \"name\": \"问题\",\n      \"desc\": \"用户的问题\"\n    }\n  ]\n}"),
	}

	// 复制代码运行请自行打印 API 的返回值
	// 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
	resp, err := client.CallApi(params, request, runtime)
	if err != nil {
		return err
	}

	fmt.Println(resp["headers"])
        fmt.Println(resp["statusCode"])

        // 迭代读取SSE内容
        events, err := util.ReadAsString(resp["body"].(io.ReadCloser))

        if err != nil {
	    fmt.Printf("Error: %v\n", err)
	    return err
        }

        fmt.Println(tea.StringValue(events))

        return nil
}

func main() {
	err := _main(tea.StringSlice(os.Args[1:]))
	if err != nil {
		panic(err)
	}
}
```

## 异步非流式调用

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

        List<AnalyzeConversationRequest.Sentences> messageList = new ArrayList<>();
        messageList.add(AnalyzeConversationRequest.Sentences.builder().role("agent").text("请问您想咨询五险一金哪方面的问题呢").build());
        messageList.add(AnalyzeConversationRequest.Sentences.builder().role("user").text("怎么查询账户呢").build());

        List<String> resultTypes = new ArrayList<>();
        resultTypes.add("summary");

        AnalyzeConversationRequest.Dialogue dialogue = AnalyzeConversationRequest.Dialogue.builder().sessionId("session-01")
                .sentences(messageList).build();

        AnalyzeConversationRequest completionParam = AnalyzeConversationRequest.builder().modelCode("tyxmPlus").resultTypes(resultTypes)
                .workspaceId(workspaceId).appId(appId).dialogue(dialogue).requestConfiguration(RequestConfiguration.create()
                        .setHttpMethod(HttpMethod.POST)).stream(false).build();
        System.out.println(JSON.toJSONString(completionParam));

        CompletableFuture<AnalyzeConversationResponse> x = client.analyzeConversation(completionParam);
        AnalyzeConversationResponse generateCompletionResponse = x.get(10, TimeUnit.SECONDS);
        System.out.println("ALL***********************");
        System.out.println(JSON.toJSONString(generateCompletionResponse.getBody()));
        System.out.println(generateCompletionResponse.getBody().getText());
        System.out.println(generateCompletionResponse.getBody().getRequestId());

    }
}
```

## 同步流式调用

Go

```
// 示例代码，其中阿里云AK、SK，CCAI的业务空间ID（workspaceId）和应用ID（appId），替换为用户当前的。
// tea-utils使用这个版本，go get github.com/alibabacloud-go/tea-utils/v2@v2.0.5-0.20240708091240-f3d7eca052de

// This file is auto-generated, don't edit it. Thanks.
package main

import (
	"fmt"
	"io"
	"os"

	openapi "github.com/alibabacloud-go/darabonba-openapi/v2/client"
	openapiutil "github.com/alibabacloud-go/openapi-util/service"
	util "github.com/alibabacloud-go/tea-utils/v2/service"
	"github.com/alibabacloud-go/tea/tea"
)

/**
 * API 相关
 * @param path params
 * @return OpenApi.Params
 */
func CreateApiInfo() (_result *openapi.Params) {
	params := &openapi.Params{
		// 接口名称
		Action: tea.String("AnalyzeConversation"),
		// 接口版本
		Version: tea.String("2024-06-03"),
		// 接口协议
		Protocol: tea.String("HTTPS"),
		// 接口 HTTP 方法
		Method:   tea.String("POST"),
		AuthType: tea.String("AK"),
		Style:    tea.String("ROA"),
		// 接口 PATH
		Pathname: tea.String("/YOUR_CCAI_WORKSPACEID/ccai/app/YOUR_CCAI_APP_ID/analyze_conversation"),
		// 接口请求体内容格式
		ReqBodyType: tea.String("json"),
		// 接口响应体内容格式，注意一定得是binary格式，CallApi才会透传出response body进行ReadAsSSE
		BodyType: tea.String("binary"),
	}
	_result = params
	return _result
}

func _main(args []*string) (_err error) {
	// 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
	// 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378661.html。
	config := &openapi.Config{
		AccessKeyId:     tea.String("YOUR_ALIYUN_AK"),
		AccessKeySecret: tea.String("YOUR_ALIYUN_SK"),
	}
	config.Endpoint = tea.String("contactcenterai.cn-shanghai.aliyuncs.com")
	client, err := openapi.NewClient(config)
	if err != nil {
		return err
	}

	params := CreateApiInfo()
	// query params
	queries := map[string]interface{}{}
	queries["workspaceId"] = tea.String("YOUR_CCAI_WORKSPACEID")
	queries["appId"] = tea.String("YOUR_CCAI_APP_ID")

	body := map[string]interface{}{
		"dialogue": map[string]interface{}{
			"sentences": []map[string]*string{map[string]*string{
				"role": tea.String("agent"),
				"text": tea.String("您好，请问有什么问题需要解决"),
			}, map[string]*string{
				"role": tea.String("user"),
				"text": tea.String("怎么领取游戏币呢"),
			}, map[string]*string{
				"role": tea.String("agent"),
				"text": tea.String("请登录个人账号，在账号下，看看是否有推荐的待领取的游戏币呢，如果有会推送给您的"),
			}, map[string]*string{
				"role": tea.String("user"),
				"text": tea.String("好，谢谢"),
			}},
			"sessionId": "2323",
		},
		"modelCode":   "tyxmPlus",
		"resultTypes": []*string{tea.String("question_solution")},
		"stream":      true,
	}

	// runtime options
	runtime := &util.RuntimeOptions{}
	request := &openapi.OpenApiRequest{
		Query: openapiutil.Query(queries),
		Body:  body,
		//Body:  tea.String("{\n  \"stream\": false,\n  \"modelCode\": \"tyxmPlus\",\n  \"dialogue\": {\n    \"sentences\": [\n      {\n        \"role\": \"user\",\n        \"text\": \"号主开挂了模拟宇宙无线祝福\\n联系方式: ******\\n图片上传:\\n视频上传:\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"乘客您好，欢迎登录本次星穹列车帕~麻烦您提供一下以下信息：*游戏项目：\\n*被举报角色UID：\"\n      },\n      {\n        \"role\": \"user\",\n        \"text\": \"通行证id******\\n\\n2024-06-10 18:25:52 [玩家] ***:\\nuid******\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"您的问题我们之前已经记录反馈了，会进行核实的~如有结果我们会在服务进度或在线服务中告知，您可以留意相关提示。十分抱歉给您带来不便\\n\"\n      },\n      {\n        \"role\": \"agent\",\n        \"text\": \"您的问题咨询完成啦，那客服娘贴心提示，不要忘记消耗开拓力哦~祝愿您在完成探索的途中获得美好的回忆哦~希望您抽空也记得给客服娘进行下评价，挥挥~~\\n\"\n      }\n    ],\n    \"sessionId\": \"ss01\"\n  },\n  \"resultTypes\": [\n    \"question_solution\"\n  ],\n  \"serviceInspection\": {\n    \"inspectionIntroduction\": \"请检测客服是否存在服务不当的行为，包括：过度承诺、故意套取客户隐私信息等\",\n    \"sceneIntroduction\": \"保险销售场景\",\n    \"inspectionContents\": [\n      {\n        \"title\": \"客服是否过度承诺\",\n        \"content\": \"客服在服务客户过程中，基于已有的服务标准是否存在过度承诺的行为，如：最快到货时间是12小时，无法给客户承诺更快的到货时间。\"\n      }\n    ]\n  },\n  \"fields\": [\n    {\n      \"code\": \"name\",\n      \"name\": \"姓名\",\n      \"desc\": \"用户的姓名\"\n    },\n    {\n      \"code\": \"question\",\n      \"name\": \"问题\",\n      \"desc\": \"用户的问题\"\n    }\n  ]\n}"),
	}

	// 复制代码运行请自行打印 API 的返回值
	// 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
	resp, err := client.CallApi(params, request, runtime)
	if err != nil {
		return err
	}

	fmt.Println(resp["headers"])
	fmt.Println(resp["statusCode"])

	// 迭代读取SSE内容
	eventChan, errChan := util.ReadAsSSE(resp["body"].(io.ReadCloser))
	for {
		select {
		case event, ok := <-eventChan:
			if !ok {
				return nil
			}
			fmt.Println("-------------------------------------")
			fmt.Printf("Event ID: %s, Event name: %s, Data: %s\n", event.ID, event.Event, event.Data)
		case err, ok := <-errChan:
			if ok && err != nil {
				fmt.Printf("Error: %v\n", err)
				return err
			}
		}
	}

}

func main() {
	err := _main(tea.StringSlice(os.Args[1:]))
	if err != nil {
		panic(err)
	}
}
```
