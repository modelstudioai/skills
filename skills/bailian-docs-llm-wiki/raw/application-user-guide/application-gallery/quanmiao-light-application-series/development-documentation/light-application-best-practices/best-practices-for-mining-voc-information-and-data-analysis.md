# 挖掘VOC信息和数据分析的最佳实践

本文的主要介绍借助**全妙-泛企业VOC挖掘**和**析言GBI**两个产品挖掘VOC信息并进行数据分析。

## **目标**

针对海量非结构化的VOC数据快速打标，整理成结构化标签数据，在通过ChatBI的方式进行实时标签分析，帮助企业完成VOC洞察的一整套流程。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910970.png)

* * *

## **前提条件**

-   已开通阿里云百炼中的下面两个产品：
    
    -   全妙-泛企业VOC挖掘【[https://bailian.console.aliyun.com/?spm=5176.29619931.J\_\_Z58Z6CX7MY\_\_Ll8p1ZOR.1.74cd59fcHNZmnE#/app/app-market/quanmiao/voc](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.74cd59fcHNZmnE#/app/app-market/quanmiao/voc)】；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910980.png)
        
    -   析言GBI【[https://bailian.console.aliyun.com/xiyan?switchAgent=10037901&productCode=p\_efm#/home](https://bailian.console.aliyun.com/xiyan?switchAgent=10037901&productCode=p_efm#/home)】。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910981.png)
        
-   已获取WorkspaceID：[获取Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。
    
-   已获取AccessKey ID和AccessKey Secret：[获取 AccessKey 与 AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)。
    
-   RAM用户已添加`AliyunDataAnalysisGBIFullAccess`权限策略：[为RAM用户授权](https://help.aliyun.com/zh/ram/user-guide/grant-permissions-to-the-ram-user)。
    

* * *

## **安装依赖**

1.  获取析言GBI和全秒-泛企业VOC挖掘[JAVA SDK](https://api.aliyun.com/api-tools/sdk/DataAnalysisGBI?version=2024-08-23&language=java-async-tea&tab=primer-doc)最新版本号。
    
2.  打开您的Maven项目的`pom.xml`文件。
    
3.  在`<dependencies>`标签内添加以下依赖信息，并将`<version></version>`标签中的版本号替换为最新的版本号。
    

```
<dependency>
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-dataanalysisgbi20240823</artifactId>
  <version>1.0.0</version>
  </dependency>
 
  <groupId>com.aliyun</groupId>
  <artifactId>alibabacloud-aimiaobi20230801</artifactId>
  <version>取最新版本</version>
  </dependency>
 
  <dependency>
  <groupId>org.projectlombok</groupId>
  <artifactId>lombok</artifactId>
  <version>1.18.30</version>
  </dependency>
 
  <dependency>
  <groupId>com.alibaba.fastjson2</groupId>
  <artifactId>fastjson2</artifactId>
  <version>2.0.21</version>
  </dependency>
 
  <dependency>
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <version>5.8.1</version>
  </dependency>
```

4.  保存`pom.xml`文件。
    
5.  更新项目依赖，将SDK添加到您的项目中。
    

* * *

## **操作步骤**

### **步骤一：通过全妙-泛企业VOC挖掘提取内容标签**

基于全妙泛企业VOC挖掘的接口[妙策-企业VOC挖掘](https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-dir-miaoce-enterprise-voc-mining/)（例如：本示例中的`SubmitEnterpriseVocAnalysisTask`接口），来帮您实现对已有工单类数据的Voc挖掘、标签提取。

请将代码示例中的`accessKeyId`、`accessKeySecret`及`workspaceId`替换为实际值，以确保代码正常运行并返回正确的结果。

```
import com.alibaba.fastjson2.JSONArray;
import com.alibaba.fastjson2.JSONObject;
import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.*;
import darabonba.core.client.ClientOverrideConfiguration;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

/**
 * 企业VOC挖掘API示例
 * 前置依赖
 * ```xml
 * <groupId>com.aliyun</groupId>
 * <artifactId>alibabacloud-aimiaobi20230801</artifactId>
 * <version>取最新版本</version>
 * </dependency>
 *
 * <dependency>
 * <groupId>org.projectlombok</groupId>
 * <artifactId>lombok</artifactId>
 * <version>1.18.30</version>
 * </dependency>
 *
 * <dependency>
 * <groupId>com.alibaba.fastjson2</groupId>
 * <artifactId>fastjson2</artifactId>
 * <version>2.0.21</version>
 * </dependency>
 *
 * <dependency>
 * <groupId>org.junit.jupiter</groupId>
 * <artifactId>junit-jupiter</artifactId>
 * <version>5.8.1</version>
 * </dependency>
 * <p>
 * ```
 */
@Slf4j
public class EnterpriseVocTest {

    /**
     * JSON参数
     */
    private String jsonParam = "{\"MaterialType\":\"dialogue\",\"ModelId\":\"qwen-max\",\"TaskType\":\"lightAppSass\",\"ContentTags\":[{\"TagValueDefinePrompt\":\"\",\"TagName\":\"产品反馈-产品名称\",\"TagTaskType\":\"singleTagValue\",\"TagDefinePrompt\":\"客户反馈的产品主要名称\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"产品反馈-产品优点\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"从数据中挖掘出对用户来说目前对产品比较满意和认可的点，也就是用户认为产品有哪些优点\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"产品反馈-产品缺点\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"从数据中挖掘出对用户来说目前产品不满意的点，也就是用户认为产品有哪些缺点\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"产品反馈-用户期望建议\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"从数据中收集用户对产品有哪些期望和建议。比如用户希望增加某些功能等等。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"产品反馈-设计与外观\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对产品外观相关的评价。外观包括但不限于设计风格/颜色/尺寸/大小等方面。\"},{\"TagValueDefinePrompt\":\"正向,中立,负向\",\"TagName\":\"产品反馈-用户情感倾向\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对产品整体的情感倾向。比如觉得产品整体都不好，以后不会买，则属于负向情绪。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"服务评价-售前服务\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对企业的售前销售提供的咨询、介绍等服务的满意度。比如对销售人员的专业性、服务态度等方面的评价。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"服务评价-售后服务\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对企业在产品售后提供的维修、退换货、咨询等服务的满意度。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"服务评价-物流配送\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对产品的配送速度、包装完整性等方面的评价。例如，用户可能对快递的送达时间、包装是否严实等提出意见。\"},{\"TagValueDefinePrompt\":\"正向,中立,负向\",\"TagName\":\"服务评价-情感正负向\",\"TagTaskType\":\"singleTagValue\",\"TagDefinePrompt\":\"用户对体验到的服务抱持什么态度、观点和情感。比如，觉得服务特别贴心，而且持续跟踪自己的使用反馈，帮忙解决使用中的各种问题，从而表现出对服务的认可。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"用户需求与痛点-使用场景\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户是怎样用产品的，把产品用在什么场景。\"},{\"TagValueDefinePrompt\":\"是,否\",\"TagName\":\"用户需求与痛点-是否有未被满足的需求\",\"TagTaskType\":\"singleTagValue\",\"TagDefinePrompt\":\"在整体的评价中，用户是否表达出了一些未被满足的需求。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"用户需求与痛点-未被满足的需求\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"挖掘用户目前仍然未被满足的需求。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"用户需求与痛点-痛点问题\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"分析挖掘出用户在相关过程中遇到的问题、困扰等，急需待解决的问题。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"竞争对手比较-竞争对手信息\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"客户提到当前产品的竞争对手相关的信息，包括竞品名称等。通常是用来对比当前产品。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"竞争对手比较-对竞争对手的评价\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"挖掘出用户对竞争对手的评价信息，包括优势劣势看法等等。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"竞争对手比较-选择竞争对手的原因\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"如果数据显示用户想或者已经选择了竞争对手，请分析出选择竞争对手的原因。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"品牌形象与口碑-品牌印象\",\"TagTaskType\":\"multiTagValues\",\"TagDefinePrompt\":\"用户对品牌的价值观、形象定位等方面的理解和感受。例如，用户可能认为某个品牌代表着高品质、创新等特点。\"},{\"TagValueDefinePrompt\":\"是,否\",\"TagName\":\"品牌形象与口碑-是否愿意推荐给他人\",\"TagTaskType\":\"singleTagValue\",\"TagDefinePrompt\":\"对当前产品或品牌，分析用户推荐给其他人的意愿程度。\"},{\"TagValueDefinePrompt\":\"\",\"TagName\":\"品牌形象与口碑-推荐意愿原因分析\",\"TagTaskType\":\"summaryAndOverview\",\"TagDefinePrompt\":\"对当前产品或服务，用户是否愿意推荐给其他人，做一个原因概括分析。\"},{\"TagName\":\"情感正负向\",\"TagDefinePrompt\":\"用户对体验到的服务抱持什么态度、观点和情感。比如，觉得服务特别贴心，而且持续跟踪自己的使用反馈，帮忙解决使用中的各种问题，从而表现出对服务的认可。\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"正向,中立,负向\"},{\"TagName\":\"用户id\",\"TagDefinePrompt\":\"当前用户的唯一标识符id\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"提交时间\",\"TagDefinePrompt\":\"当前工单发生的时间\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"问题类型一级标签\",\"TagDefinePrompt\":\"请帮我分析当前问题属于哪个一级类型\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"故障反馈,配件咨询\"},{\"TagName\":\"问题类型二级标签\",\"TagDefinePrompt\":\"当前问题类型一级标签的哪个子属性，属于配件咨询的有装配问题和缺错件，属于配件咨询类型的有电器问题\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"装配问题,电器问题,缺错件\"},{\"TagName\":\"问题类型三级标签\",\"TagDefinePrompt\":\"当前问题属于问题类型二级标签的哪个子属性，属于装配问题的有装配问题，属于电器问题的有电器件质量和外观件设计，属于缺错件的问题有配件发错和配件缺件\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"配件发错,配件缺件,外观件设计,电器件质量,装配问题\"},{\"TagName\":\"问题描述\",\"TagDefinePrompt\":\"对当前用户反馈工单的问题进行汇总描述\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"故障件\",\"TagDefinePrompt\":\"当前用户反馈的问题如果设计故障件，则在此添加故障的配件，没有则为空\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"刹车,座椅\"},{\"TagName\":\"服务经销商名称\",\"TagDefinePrompt\":\"当前用户反馈的问题，属于哪个服务经销商的问题，如果没有提到经销商相关，则无需填写。\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"服务站省\",\"TagDefinePrompt\":\"当前用户反馈的工单属于哪个省，如果没有则无需填写\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"服务站市\",\"TagDefinePrompt\":\"当前用户反馈的问题属于哪个市，如果没有提及则无需填写\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"服务站区\",\"TagDefinePrompt\":\"当前用户反馈的问题属于哪个区，如果用户没有提及则不用填写\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"\"},{\"TagName\":\"工单来源\",\"TagDefinePrompt\":\"当前工单的来源，是从哪里提交的，如果没有提及，默认是电话\\n\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"微信公众号,电话,门店\"},{\"TagName\":\"机型\",\"TagDefinePrompt\":\"当前工单涉及到的机型，如果没有提及则为空\",\"TagTaskType\":\"singleTagValue\",\"TagValueDefinePrompt\":\"机型1,机型2\"}],\"Contents\":[{\"Text\":\"客服一号 2025-01-05 09:36\\n您好我是客服一号，请问有什么可以帮到您\\nYoyo Qin 10:19 用户id:892-889-222\\n为什么现在续航这么差！原先充满电可以开30公里，现在只能开20公里！\\nYY酒店 10:20\\n这个非常抱歉 我这边跟技术反馈一下，请问您所在的地区以及电动车的型号是？\\nYoyo Qin 10:21\\n吉林省长春市\\nYoyo Qin 10:21\\n机型1\\nYY酒店 10:24\\n十分抱歉Qin女士 给您造成不好的体验，因为你所在的地区比较寒冷，可能会造成耗电比较高的情况， 这边下次您有机会来门店，给您安排一次换电监测，您看可以嘛\\nYoyo Qin 10:35\\n好叭\\n\",\"ExtraInfo\":\"顾客Yoyo Qin在购买电动车后和客服一号的工单对话\"}]}";

    /**
     * 业务空间ID
     */
    private String workspaceId = "workspaceId";

    public static AsyncClient asyncClient() {
        //accessKeyId
        String accessKeyId = "accessKeyId";

        //accessKeySecret
        String accessKeySecret = "accessKeySecret";

        //域名:aimiaobi.cn-hangzhou.aliyuncs.com
        String domain = "aimiaobi.cn-beijing.aliyuncs.com";

        return AsyncClient.builder().credentialsProvider(StaticCredentialProvider.create(Credential.builder()
                .accessKeyId(accessKeyId).accessKeySecret(accessKeySecret).build())).serviceConfiguration(Configuration.create()
                .setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(ClientOverrideConfiguration.create().setProtocol("HTTPS")
                .setEndpointOverride(domain)).build();
    }

    @Test
    public void createEnterpriseVoc() throws ExecutionException, InterruptedException {
        AsyncClient asyncClient = asyncClient();
        //提交任务
        String taskId = doSubmitTask(asyncClient);

        //轮询任务成功之后，获取明细列表
        if (pollTask(asyncClient, taskId)) {

            CompletableFuture<ListAnalysisTagDetailByTaskIdResponse> responseFuture =
                    asyncClient.listAnalysisTagDetailByTaskId(ListAnalysisTagDetailByTaskIdRequest.builder().taskId(taskId).workspaceId(workspaceId).build());

            ListAnalysisTagDetailByTaskIdResponse response = responseFuture.get();

            StringBuilder detailInfo = new StringBuilder();

            for (ListAnalysisTagDetailByTaskIdResponseBody.Data datum : response.getBody().getData()) {
                detailInfo.append("VOC内容：").append(datum.getContent().substring(0, Math.min(50, datum.getContent().length()))).append("\n");
                detailInfo.append("挖掘的标签列表：\n");
                for (ListAnalysisTagDetailByTaskIdResponseBody.ContentTags contentTag : datum.getContentTags()) {
                    detailInfo.append("\t标签名：").append(contentTag.getTagName()).append("\n");
                    if (contentTag.getTags() != null) {
                        detailInfo.append("\t标签值：").append(String.join(",", contentTag.getTags())).append("\n");
                    }
                    if (contentTag.getSummaryOverview() != null) {
                        detailInfo.append("\t总结概览：").append(contentTag.getSummaryOverview()).append("\n");
                    }
                    detailInfo.append("\n");
                }
                detailInfo.append("\n");
            }

            System.out.println(detailInfo);
        }

    }

    private String doSubmitTask(AsyncClient asyncClient) throws ExecutionException, InterruptedException {
        JSONObject param = JSONObject.parseObject(jsonParam);

        String materialType = param.getString("MaterialType");

        String modelId = param.getString("ModelId");

        String fileKey = param.getString("FileKey");

        String PositiveSample = param.getString("PositiveSample");

        String PositiveSampleFileKey = param.getString("PositiveSampleFileKey");

        SubmitEnterpriseVocAnalysisTaskRequest.Builder builder = SubmitEnterpriseVocAnalysisTaskRequest.builder();

        builder.modelId(modelId).materialType(materialType).workspaceId(workspaceId);
        if (fileKey != null) {
            builder.fileKey(fileKey);
        }

        if (PositiveSample != null) {
            builder.positiveSample(PositiveSample);
        }

        if (PositiveSampleFileKey != null) {
            builder.positiveSampleFileKey(PositiveSampleFileKey);
        }

        JSONArray contents = param.getJSONArray("Contents");
        if (contents != null) {
            List<SubmitEnterpriseVocAnalysisTaskRequest.Contents> collect = contents.stream().map(x -> {
                return SubmitEnterpriseVocAnalysisTaskRequest.Contents.build((JSONObject) x, SubmitEnterpriseVocAnalysisTaskRequest.Contents.create());
            }).collect(Collectors.toList());
            builder.contents(collect);
        }
        JSONArray contentTags = param.getJSONArray("ContentTags");
        if (contentTags != null) {
            List<SubmitEnterpriseVocAnalysisTaskRequest.ContentTags> collect = contentTags.stream().map(x -> {
                return SubmitEnterpriseVocAnalysisTaskRequest.ContentTags.build((JSONObject) x, SubmitEnterpriseVocAnalysisTaskRequest.ContentTags.create());
            }).collect(Collectors.toList());
            builder.contentTags(collect);
        }

        JSONArray filterTags = param.getJSONArray("FilterTags");
        if (filterTags != null) {
            List<SubmitEnterpriseVocAnalysisTaskRequest.FilterTags> collect = filterTags.stream().map(x -> {
                return SubmitEnterpriseVocAnalysisTaskRequest.FilterTags.build((JSONObject) x, SubmitEnterpriseVocAnalysisTaskRequest.FilterTags.create());
            }).collect(Collectors.toList());
            builder.filterTags(collect);
        }

        SubmitEnterpriseVocAnalysisTaskRequest build = builder.build();

        CompletableFuture<SubmitEnterpriseVocAnalysisTaskResponse> enterpriseVocAnalysisTask = asyncClient.submitEnterpriseVocAnalysisTask(build);

        SubmitEnterpriseVocAnalysisTaskResponse response = enterpriseVocAnalysisTask.get();

        if (!response.getBody().getSuccess()) {
            log.error("提交VOC任务失败，错误码：{}，错误信息：{}", response.getBody().getCode(), response.getBody().getMessage());
            return null;
        }

        return response.getBody().getData().getTaskId();
    }

    private boolean pollTask(AsyncClient asyncClient, String taskId) throws InterruptedException, ExecutionException {
        //轮询热点播报任务结果
        while (true) {
            CompletableFuture<GetEnterpriseVocAnalysisTaskResponse> future = asyncClient.getEnterpriseVocAnalysisTask(GetEnterpriseVocAnalysisTaskRequest.builder().workspaceId(workspaceId).taskId(taskId).build());

            GetEnterpriseVocAnalysisTaskResponseBody body = future.get().getBody();
            if (!body.getSuccess()) {
                log.error("查询任务失败，错误码：{}，错误信息：{}", body.getCode(), body.getMessage());
                return false;
            }
            //只有 PENDING、RUNNING才轮询
            GetEnterpriseVocAnalysisTaskResponseBody.Data data = body.getData();
            if (data.getStatus().equals("PENDING") || data.getStatus().equals("RUNNING")) {
                log.info("VOC分析任务执行中，TaskId:{},TaskStatus:{}", taskId, data.getStatus());
                Thread.sleep(4000);
                continue;
            }

            if (!data.getStatus().equals("SUCCESSED")) {
                log.error("VOC分析任务执行失败，错误码：{}，错误信息：{}", body.getCode(), body.getMessage());
                return false;
            }

            GetEnterpriseVocAnalysisTaskResponseBody.Usage usage = data.getUsage();
            //输入Token、输出Token
            Long inputToken = usage.getInputTokens();
            Long outputToken = usage.getOutputTokens();

            log.info("VOC分析任务执行成功，TaskId:{},TaskStatus:{},输入Token:{},输出Token:{}", taskId, data.getStatus(), inputToken, outputToken);

            GetEnterpriseVocAnalysisTaskResponseBody.StatisticsOverview statisticsOverview = data.getStatisticsOverview();
            log.info("总数据条数：{}", statisticsOverview.getCount());
            log.info("过滤标签统计：{}", statisticsOverview.getFilterDimensionStatistics());
            log.info("内容标签统计：{}", statisticsOverview.getTagDimensionStatistics());
            return true;
        }
    }

}
```

在如上的代码示例中，企业Voc挖掘接口，会将如下图所示的工单数据：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910968.png)

提取出我们所需要的各种信息、标签类型，并以结构化信息的形式返回：

```
[
    {
        "tagName": "产品反馈-用户情感倾向",
        "tags": [
            "负向"
        ]
    },
    {
        "tagName": "产品反馈-产品缺点",
        "tags": [
            "续航差"
        ]
    },
    {
        "tagName": "工单来源",
        "tags": [
            "电话"
        ]
    },
    {
        "tagName": "情感正负向",
        "tags": [
            "负向"
        ]
    },
    {
        "tagName": "提交时间",
        "tags": [
            "2025-01-05 09:36"
        ]
    },
    {
        "tagName": "故障件",
        "tags": [
            "电池"
        ]
    },
    {
        "tagName": "服务站市",
        "tags": [
            "长春市"
        ]
    },
    {
        "tagName": "服务站省",
        "tags": [
            "吉林省"
        ]
    },
    {
        "tagName": "服务评价-情感正负向",
        "tags": [
            "中立"
        ]
    },
    {
        "tagName": "服务评价-售后服务",
        "tags": [
            "换电监测服务"
        ]
    },
    {
        "tagName": "机型",
        "tags": [
            "机型1"
        ]
    },
    {
        "tagName": "用户id",
        "tags": [
            "892-889-222"
        ]
    },
    {
        "tagName": "用户需求与痛点-痛点问题",
        "tags": [
            "电池续航下降"
        ]
    },
    {
        "tagName": "用户需求与痛点-未被满足的需求",
        "tags": [
            "更长的续航里程"
        ]
    },
    {
        "tagName": "用户需求与痛点-是否有未被满足的需求",
        "tags": [
            "是"
        ]
    },
    {
        "tagName": "问题描述",
        "tags": [
            "电动车续航能力降低，从原来的30公里降至20公里"
        ]
    },
    {
        "tagName": "问题类型一级标签",
        "tags": [
            "故障反馈"
        ]
    },
    {
        "tagName": "问题类型三级标签",
        "tags": [
            "电器件质量"
        ]
    },
    {
        "tagName": "问题类型二级标签",
        "tags": [
            "电器问题"
        ]
    }
]
```

### **步骤二：将内容标签的结构化数据转存到数据库**

根据企业Voc挖掘结果中的tagName，将其构建成数据库中的列名并生成数据库DDL语句，构建数据库。以MySQL数据库为例。

```
CREATE TABLE `analyze_table` (
  `Uid` varchar(50) COLLATE utf8mb4_unicode_520_ci NOT NULL COMMENT '用户的id',
  `服务站省` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单提交的省份',
  `服务站市` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单提交的市区',
  `服务站区` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单提交的站区',
  `服务里程` int DEFAULT NULL COMMENT '表示当前电动车行驶了多少里程',
  `提交时间` datetime DEFAULT NULL COMMENT '表示当前工单的提交时间',
  `提交来源` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单的提交来源',
  `经销商名称` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前的经销商的名字',
  `经销商编码` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前经销商的唯一编码',
  `机型` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前电动车的机型',
  `情绪情感` varchar(20) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单文本的情感',
  `问题描述` text COLLATE utf8mb4_unicode_520_ci COMMENT '当前工单的原始问题描述',
  `故障件` varchar(100) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '当前工单提出问题的出现故障的零件',
  `问题类型一级标签` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单的一级标签，是大类问题',
  `问题类型二级标签` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单的二级标签，是一级标签的下属问题',
  `问题类型三级标签` varchar(50) COLLATE utf8mb4_unicode_520_ci DEFAULT NULL COMMENT '表示当前工单的三级标签，是二级标签的下属问题',
  PRIMARY KEY (`Uid`),
  UNIQUE KEY `经销商编码` (`经销商编码`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci COMMENT='分析表，包含所有工单相关信息';
```

并将tags的内容当作具体的列值插入数据库。

```
INSERT INTO `chat_bi`.`analyze_table` (`Uid`, `服务站省`, `服务站市`, `服务站区`, `服务里程`, `提交时间`, `提交来源`, `经销商名称`, `经销商编码`, `机型`, `情绪情感`, `问题描述`, `故障件`, `问题类型一级标签`, `问题类型二级标签`, `问题类型三级标签`) VALUES ('001eeb2d-bd96-4bbe-a2f9-15b05d65ff7c', '辽宁省', '大连市', '中山区', 774, '2025-01-02 20:07:00', '电话', '经销商C', 'ed1de1b2-3b5b-4564-b881-5fab9f29fbb1', '机型1', '负向', '关于车架的故障问题进行了描述。', '车架', '配件咨询', '配件开箱破损（含售后衍生品）', '配件内物破损');
```

### **步骤三：将数据库关联到析言GBI并进行对话分析**

-   在[析言GBI](https://bailian.console.aliyun.com/xiyan/#/dataManagement/dataSourceM?back=back)中将刚刚配置好的数据库与析言GBI进行关联配置。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910972.png)
    
-   无需额外的配置，即可对刚刚关联的数据库内容进行问答，并获取数据结果以及相关可视化分析展示。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910973.png)
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910971.png)
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7431988371/p910969.png)
    

### **（可选）步骤四：将析言GBI的对话接口集成到业务系统**

可以采用析言GBI云服务所提供的[RunDataAnalysis - Chat对话接口](https://help.aliyun.com/zh/model-studio/api-dataanalysisgbi-2024-08-23-rundataanalysis)来实现如图所示的chatbi能力，并集成到自己的业务系统。

代码示例参考：[操作步骤](https://help.aliyun.com/zh/model-studio/gbi-best-practices#71c9235ce84u5)
