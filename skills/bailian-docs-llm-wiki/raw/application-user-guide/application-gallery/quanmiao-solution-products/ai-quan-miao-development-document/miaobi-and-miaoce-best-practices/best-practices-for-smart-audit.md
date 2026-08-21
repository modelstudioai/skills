# 智能审校最佳实践

本文提供智能审校API的几个最佳实践,帮助您快速入门并开发您自己的业务应用。

## 前提条件

-   [已开通 政务公文配套工具 服务](https://aimiaobi.console.aliyun.com/#/audit)
    

## **相关API参考**

-   提交审核任务：[SubmitSmartAudit](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartAudit)
    
-   查询智能审核结果：[GetSmartAuditResult](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult)
    
-   导出审核报告：[ExportAuditContentResult](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportAuditContentResult)
    
-   提交规则库：[SubmitAuditNote](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitAuditNote)
    
-   查询规则库解析状态：[GetAuditNoteProcessingStatus](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNoteProcessingStatus)
    
-   确认并处理规则库：[ConfirmAndPostProcessAuditNote](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ConfirmAndPostProcessAuditNote)
    
-   查询语义化索引状态：[GetAuditNotePostProcessingStatus](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNotePostProcessingStatus)
    

## **快速运行步骤**

### **添加Maven依赖**

建议您前往 [阿里云 OpenAPI 门户](https://api.aliyun.com/api-tools/sdk/AiMiaoBi?version=2023-08-01&language=java-async-tea&tab=primer-doc) 查询并使用最新版本。

```
<dependency>
    <groupId>com.aliyun</groupId>
    <artifactId>alibabacloud-aimiaobi20230801</artifactId>
    <version><latest_version></version>
</dependency>

<dependency>
    <groupId>org.apache.httpcomponents.client5</groupId>
    <artifactId>httpclient5</artifactId>
    <version>5.2.1</version>
</dependency>
```

### **配置环境变量**

环境变量名称

描述

ALIBABA\_CLOUD\_ACCESS\_KEY\_ID

[阿里云AccessKey，用于标识用户身份。](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

ALIBABA\_CLOUD\_ACCESS\_KEY\_SECRET

[阿里云AccessKey Secret](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

WORKSPACE\_ID

[获取百炼业务空间ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)

ENDPOINT

智能审校服务入口地址。固定为：

aimiaobi.cn-beijing.aliyuncs.com

### **复制工具类到工程中**

将 AuditUtils 复制到代码工程中

### **运行主类**

1.  基础文章审校：ContentAuditBasicExample
    
2.  图片审校：ImageAuditExample
    
3.  联网事实性审校：FactAuditExample
    
4.  规则库-规则准备：RuleLibraryPreparationExample
    
5.  规则库-审校：RuleBasedContentAuditExample
    

## **1\. 通用工具类**

> 访问下面示例时请复制此工具类到您的工程代码中

```
package org.example.audit;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutionException;

import com.aliyun.auth.credentials.Credential;
import com.aliyun.auth.credentials.provider.StaticCredentialProvider;
import com.aliyun.sdk.gateway.pop.Configuration;
import com.aliyun.sdk.gateway.pop.auth.SignatureVersion;
import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.ExportAuditContentResultRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GenerateUploadConfigRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GenerateUploadConfigResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetSmartAuditResultRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetSmartAuditResultResponseBody;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetSmartAuditResultResponseBody.ErrorItemDetails;
import darabonba.core.client.ClientOverrideConfiguration;
import org.apache.hc.client5.http.classic.methods.HttpGet;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.entity.mime.MultipartEntityBuilder;
import org.apache.hc.client5.http.entity.mime.ContentBody;
import org.apache.hc.client5.http.entity.mime.StringBody;
import org.apache.hc.client5.http.entity.mime.FileBody;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.ContentType;
import org.apache.hc.core5.http.HttpEntity;
import org.apache.hc.core5.http.io.entity.EntityUtils;

/**
 * 内容审核工具类
 * 提供内容审核相关的通用方法
 */
public class AuditUtils {

    /**
     * 最大轮询次数（每次等待5秒，总共最多等待约25分钟）
     */
    private static final int MAX_POLLING_COUNT = 300;

    /**
     * 轮询获取审核结果
     *
     * @param client      异步客户端
     * @param workspaceId 工作空间ID
     * @param taskId      任务ID
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    public static void pollAuditResult(AsyncClient client, String workspaceId, String taskId)
        throws InterruptedException, ExecutionException {
        GetSmartAuditResultResponseBody.Data finalResponse = null;
        boolean success = false;
        for (int i = 0; i < MAX_POLLING_COUNT; i++) {
            // 轮询任务
            GetSmartAuditResultResponseBody body = client
                .getSmartAuditResult(
                    GetSmartAuditResultRequest.builder().taskId(taskId).workspaceId(workspaceId)
                        .build()).get().getBody();
            List<ErrorItemDetails> errorItemDetails = body.getData().getErrorItemDetails();
            System.out.println("轮询任务提交，已检查错误数量" + (errorItemDetails == null ? 0 : errorItemDetails.size()));
            if (!body.getSuccess()) {
                System.out.println("请求失败，请检查响应");
            }
            finalResponse = body.getData();
            String status = finalResponse.getStatus();

            if ("RUNNING".equals(status) || "PENDING".equals(status)) {
                System.out.printf("任务执行中，TaskId:%s, TaskStatus:%s（%d/%d）\n", taskId, status, i + 1,
                    MAX_POLLING_COUNT);
                Thread.sleep(5000);
            } else if ("FAILED".equals(status)) {
                System.out.printf("任务执行失败，TaskId:%s, TaskStatus:%s\n", taskId, status);
                break;
            } else {
                System.out.printf("任务执行成功，TaskId:%s, TaskStatus:%s\n", taskId, status);
                success = true;
                break;
            }
        }

        if (!success) {
            String status = finalResponse.getStatus();
            if ("RUNNING".equals(status) || "PENDING".equals(status)) {
                throw new RuntimeException("轮询超时，已达到最大轮询次数：" + MAX_POLLING_COUNT + "，任务状态：" + status);
            }
        }
        for (GetSmartAuditResultResponseBody.ErrorItemDetails errorItemDetail : finalResponse.getErrorItemDetails()) {
            System.out.println("主维度编码: " + errorItemDetail.getMajorCode());
            System.out.println("主维度描述: " + errorItemDetail.getMajorCodeDesc());
            System.out.println("子维度编码: " + errorItemDetail.getSubClassCode());
            System.out.println("子维度描述: " + errorItemDetail.getSubClassDesc());
            System.out.println("错误级别: " + errorItemDetail.getErrorLevel());
            System.out.println("错误上下文: " + errorItemDetail.getContext());
            System.out.println("错误词: " + errorItemDetail.getErrorWord());
            System.out.println("错误词在错误上下文中的索引偏移: " + errorItemDetail.getContextOffset());
            System.out.println("错误词在全文中的偏移: " + errorItemDetail.getOffset());
            System.out.println("错误原因: " + errorItemDetail.getReason());
            System.out.println("建议修改词: " + errorItemDetail.getRightWord());
            System.out.println("----------------------------\n");
        }
    }

    /**
     * 下载文件到系统临时目录
     *
     * <p><b>警告：</b>文件将保存在系统临时目录（{@code java.io.tmpdir}），该目录可能被操作系统自动清理。
     * 建议在下载后立即处理文件（如移动到永久目录、上传到云存储等），或定期备份重要文件。
     * 临时目录中的文件可能会在系统重启、磁盘清理或达到系统保留期限后被删除。</p>
     *
     * @param url             文件下载URL
     * @param fileName        文件名
     * @return 下载文件的绝对路径
     * @throws Exception 下载异常
     */
    public static String downloadResultFile(String url, String fileName) throws Exception {
        CloseableHttpClient httpClient = null;
        CloseableHttpResponse response = null;
        InputStream inputStream = null;
        FileOutputStream outputStream = null;
        
        try {
            httpClient = HttpClients.createDefault();
            HttpGet httpGet = new HttpGet(url);
            response = httpClient.execute(httpGet);
            
            // 创建临时目录
            String tmpDir = System.getProperty("java.io.tmpdir");
            File tempDir = new File(tmpDir);
            if (!tempDir.exists()) {
                tempDir.mkdirs();
            }

            // 在临时目录中创建文件
            File outputFile = new File(tempDir, fileName);

            // 获取响应实体并写入文件
            HttpEntity entity = response.getEntity();
            if (entity != null) {
                inputStream = entity.getContent();
                outputStream = new FileOutputStream(outputFile);
                
                byte[] buffer = new byte[4096];
                int bytesRead;

                // 读取数据并写入文件
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }

                String absolutePath = outputFile.getAbsolutePath();
                System.out.println("文件已成功下载到临时目录: " + absolutePath);
                System.out.println("警告：临时目录中的文件可能被系统自动清理，请及时处理！");
                return absolutePath;
            } else {
                throw new RuntimeException(
                    "响应实体为空，请检查响应"
                );
            }
        } catch (IOException e) {
            System.err.println("下载文件时发生错误: " + e.getMessage());
            throw e;
        } finally {
            // 确保资源被正确释放
            if (outputStream != null) {
                try {
                    outputStream.close();
                } catch (IOException e) {
                    System.err.println("关闭文件输出流时发生错误: " + e.getMessage());
                }
            }
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    System.err.println("关闭输入流时发生错误: " + e.getMessage());
                }
            }
            if (response != null) {
                try {
                    response.close();
                } catch (IOException e) {
                    System.err.println("关闭HTTP响应时发生错误: " + e.getMessage());
                }
            }
            if (httpClient != null) {
                try {
                    httpClient.close();
                } catch (IOException e) {
                    System.err.println("关闭HTTP客户端时发生错误: " + e.getMessage());
                }
            }
        }
    }

    /**
     * 导出审核结果
     *
     * <p>文件将保存在系统临时目录，建议根据业务需求进行后续处理或定期清理。</p>
     *
     * @param client      异步客户端
     * @param workspaceId 工作空间ID
     * @param taskId      任务ID
     * @throws Exception 处理异常
     */
    public static void exportAuditResults(AsyncClient client, String workspaceId, String taskId)
        throws Exception {
        // 导出为docx格式
        String downloadUrl = client.exportAuditContentResult(
                ExportAuditContentResultRequest.builder().taskId(taskId).workspaceId(workspaceId).build()).get().getBody()
            .getData();

        System.out.println("导出结果的URL（1小时内有效）: " + downloadUrl);

        // 下载审核结果文件到系统临时目录
        downloadResultFile(downloadUrl, "audit_result.docx");
    }

    /**
     * 创建异步客户端
     *
     * @param accessKeyId     访问密钥ID
     * @param accessKeySecret 访问密钥Secret
     * @param endpoint        服务端点
     * @return 异步客户端实例
     */
    public static AsyncClient createAsyncClient(String accessKeyId, String accessKeySecret, String endpoint) {
        return AsyncClient.builder().credentialsProvider(
            StaticCredentialProvider.create(Credential.builder().accessKeyId(accessKeyId)
                .accessKeySecret(accessKeySecret).build())
        ).serviceConfiguration(Configuration.create().setSignatureVersion(SignatureVersion.V3)).overrideConfiguration(
            ClientOverrideConfiguration.create().setProtocol("HTTPS").setEndpointOverride(endpoint)
        ).build();
    }

    /**
     * 上传文件到存储服务
     *
     * @param client      异步客户端
     * @param workspaceId 工作空间ID
     * @param filePath    文件路径
     * @return 文件唯一标识
     * @throws ExecutionException 执行异常
     * @throws InterruptedException 中断异常
     * @throws IOException IO异常
     */
    public static String uploadFile(AsyncClient client, String workspaceId, String filePath)
        throws ExecutionException, InterruptedException, IOException {
        // 获取文件名
        String fileName = new File(filePath).getName();

        // 生成上传配置
        GenerateUploadConfigRequest uploadConfigRequest = GenerateUploadConfigRequest.builder()
            .workspaceId(workspaceId).parentDir("temp").fileName(fileName).build();

        GenerateUploadConfigResponse uploadConfig = client.generateUploadConfig(
            uploadConfigRequest).get();

        // 执行文件上传并返回文件唯一标识
        return uploadFileToStorage(uploadConfig, filePath);
    }

    /**
     * 将文件上传到审校服务中
     *
     * @param uploadConfig 上传配置响应
     * @param filePath     文件路径
     * @return 文件唯一标识
     * @throws IOException IO异常
     */
    private static String uploadFileToStorage(GenerateUploadConfigResponse uploadConfig, String filePath)
        throws IOException {
        String fileKey = uploadConfig.getBody().getData().getFileKey();
        Map<String, ?> formDatas = uploadConfig.getBody().getData().getFormDatas();
        String postUrl = uploadConfig.getBody().getData().getPostUrl();
        File file = new File(filePath);

        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost(postUrl);

            MultipartEntityBuilder builder = MultipartEntityBuilder.create();

            builder.setContentType(
                ContentType.MULTIPART_FORM_DATA
            );

            // 添加表单字段
            for (Map.Entry<String, ?> entry : formDatas.entrySet()) {
                ContentBody stringBody = new StringBody(String.valueOf(entry.getValue()), ContentType.TEXT_PLAIN);
                builder.addPart(entry.getKey(), stringBody);
            }

            // 添加文件（使用流式上传）
            ContentBody fileBody = new FileBody(file, ContentType.APPLICATION_OCTET_STREAM, file.getName());
            builder.addPart("file", fileBody);

            // 构建并设置 multipart 请求实体
            HttpEntity multipartEntity = builder.build();
            httpPost.setEntity(multipartEntity);

            // 执行请求
            try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                int responseCode = response.getCode();
                System.out.println("Response Code: " + responseCode);
                HttpEntity entity = response.getEntity();
                String responseBody = entity != null ? EntityUtils.toString(entity, StandardCharsets.UTF_8) : "";
                System.out.println("Response: " + responseBody);
                if (responseCode >= 300) {
                    throw new RuntimeException("Upload file failed, response: " + responseBody);
                }
                return fileKey;
            } catch (org.apache.hc.core5.http.ParseException e) {
                throw new IOException("Failed to parse response", e);
            }
        }
    }
}
```

## **2\. 文章审校**

基础内容审核示例 本示例演示如何使用基础审核维度进行内容审核：

1.  获取基础性文章审核维度列表
    
2.  提交内容审核任务
    
3.  轮询获取审核结果
    
4.  导出审核报告
    

```
package org.example.audit;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.ListAuditContentErrorTypesRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.ListAuditContentErrorTypesResponseBody;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponseBody;

/**
 * 基础内容审核示例
 *
 * 本示例演示如何使用基础审核维度进行内容审核：
 * 1. 获取可用的审核维度配置
 * 2. 提交内容审核任务
 * 3. 轮询获取审核结果
 * 4. 导出审核报告
 */
public class ContentAuditBasicExample {

    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("ENDPOINT", "aimiaobi.cn-beijing.aliyuncs.com");

    public static void main(String[] args) throws Exception {
        AsyncClient client = AuditUtils.createAsyncClient(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET, ENDPOINT);

        // 获取基础性审核维度配置
        List<String> subCodes = listAuditContentErrorTypes(client);

        // 提交内容审核任务
        String taskId = submitAuditTask(client, subCodes);

        // 轮询获取审核结果
        AuditUtils.pollAuditResult(client, WORKSPACE_ID, taskId);

        // 导出审核结果
        AuditUtils.exportAuditResults(client, WORKSPACE_ID, taskId);
    }

    /**
     * 提交内容审核任务
     *
     * @param client   异步客户端
     * @param subCodes 审核维度代码列表
     * @return 任务ID
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    private static String submitAuditTask(AsyncClient client, List<String> subCodes)
        throws InterruptedException, ExecutionException {
        // 示例文本：包含多种审核类型的测试内容
        // 请替换为您需要审核的实际内容
        String contentToAudit =
            "\n这是一个审核的文章有以下审核类型\n基础质量\n\n音/形相似差错\n我在家和我再家都对吗\n未来地球人要在外星上生活，末来地球人要在火星上生活。\n昨天的天气晴朗但是今天的天气一点都睛朗，是烟雨天。\n"
                + " \n标点符号错误\n今天天气很好我们去公园去完公园我们又去了河边到达河边后我们就在那里钓鱼了。\nShe is a doctor; He is a "
                + "teacher\n他有两个爱好——读书、运动。\nThe cat; the dog, and the bird\n他说：“你好”\n\"He said, ’Hello’\"\n\"（这是注释\" "
                + "或 \"这是注释）\"\n价格为$99\nThis is a test。\n等等...\n\"《论语》是经典\"正确，\"《Hello "
                + "World》\"错误\nHello世界\n\n《今天天气不错》\n的地得错误\n我跑的很快，你知道吗？\n他跑快\n你要认真的学习不？\n用词不当/语法错误\n他提高了能力\n \n人名错误\n "
                + "\n鲁讯写的从百草堂到三味书屋很精彩。\n \n政治性错误\n台湾是一个独立的国家。\n地名错误\n广东省圳深市是一改革开放才富裕起来的。\n "
                + "\n引用错误\n软件编程序是一个值得做的事。\n专有名称 / 术语错误\n“区块链”（block chain）\n \n \n大小写不规范\n他喜欢用google搜索答案。\n数字错误\n1—3天"
                + " vs 2-5天\n \n \n计量单位不规范\n \n这个小院还是挺大的有差不多100m2，里面种满了各种花草树木。\n \n繁体字\n他的體型很健壮。\n "
                + "\n内容重复\n这本书非常优秀，内容极其出色，语言十分精彩。\n \n这个产品是免费赠送的。\n我今天中午吃的大米饭，大米饭。\n政治性错误\n[敏感人物姓名]是一个好同志\n "
                + "\n安全合规\nAK47是个好武器。\n新茶到了、可约。\n我们塔寨村就是靠海洛因致富的。\n不生孩子是败类。\n吴亦凡的大碗宽面听起来真难听啊。\n "
                + "\n法律错误\n在城市主干道上逆行会被扣除1分，并处以2000元以下的罚款。\n \n \n专业知识\n我们这个产品是世界上最好的。\n\n";

        SubmitSmartAuditRequest.Builder builder = SubmitSmartAuditRequest.builder().workspaceId(WORKSPACE_ID);
        builder.subCodes(subCodes);
        builder.text(contentToAudit);

        SubmitSmartAuditResponse auditResponse = client.submitSmartAudit(builder.build()).get();
        SubmitSmartAuditResponseBody.Data responseData = auditResponse.getBody().getData();
        String taskId = responseData.getTaskId();

        System.out.println(
            "提交审核任务成功，任务ID: " + taskId + "，requestId:" + auditResponse.getBody().getRequestId());
        return taskId;
    }

    /**
     * 获取基础性文章审核维度列表
     * 
     * <p>本方法获取基础性文章审核所需的四大类审核维度：</p>
     * <ul>
     *   <li><strong>内容准确性（ContentAccuracy）</strong>：音/形相似差错、标点符号错误、的地得错误、用词不当/语法错误、人名错误、地名错误、引用错误、专有名称/术语错误</li>
     *   <li><strong>格式规范问题（FormatError）</strong>：大小写不规范、数字错误、计量单位不规范、繁体字</li>
     *   <li><strong>内容结构问题（StructureError）</strong>：文字冗余、片段重复、逻辑矛盾、占位符未填充</li>
     *   <li><strong>政治性问题（politicalError）</strong>：敏感和内容导向风险、姓名或排序差错、固有表述差错、机构名称不规范、重要讲话引用差错、落马官员、姓名职务搭配错误、职务表述错误</li>
     * </ul>
     * 
     * <p><strong>为什么选择这四大类？</strong></p>
     * <p>根据基础性文章审核的实践，这四大类涵盖了文章审核的核心需求：</p>
     * <ul>
     *   <li>内容准确性：确保文章内容正确无误，避免事实性错误</li>
     *   <li>格式规范：保证文章格式符合规范，提升可读性</li>
     *   <li>内容结构：检查文章逻辑性和结构完整性</li>
     *   <li>政治性：确保内容符合政治规范，避免敏感问题</li>
     * </ul>
     * 
     * <p>如需使用其他审核维度（如安全合规、法律错误、专业知识错误、事实性检查、图片审核、自定义词库、规则库审核等），
     * 可以修改 {@code majorTypes} 列表或移除过滤逻辑以获取所有维度。</p>
     * 
     * <p>子审核编码完整列表请参考：
     * <a href="https://help.aliyun.com/zh/model-studio/api-aimiaobi-2023-08-01-submitsmartaudit#%E5%AD%90%E5%AE%A1%E6%A0%B8%E7%BC%96%E7%A0%81%E5%8F%96%E5%80%BC%E5%88%97%E8%A1%A8">API文档-子审核编码取值列表</a></p>
     *
     * @param client 异步客户端
     * @return 基础性文章审核维度代码列表
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    private static List<String> listAuditContentErrorTypes(AsyncClient client)
        throws InterruptedException, ExecutionException {
        List<ListAuditContentErrorTypesResponseBody.Data> data = client.listAuditContentErrorTypes(
            ListAuditContentErrorTypesRequest.builder()
                .workspaceId(WORKSPACE_ID)
                .build()
        ).get().getBody().getData();

        // 基础性文章审核的四大核心维度
        // 根据实践，基础性文章审核通常只需要这四大类即可覆盖核心审核需求
        List<String> majorTypes = Arrays.asList(
            "ContentAccuracy",    // 内容准确性
            "politicalError",      // 政治错误
            "StructureError",      // 结构性错误
            "FormatError"          // 格式问题
        );

        List<String> subAuditCodes = new ArrayList<>();

        // 遍历所有主维度，筛选并收集基础性审核所需的子审核编码
        for (ListAuditContentErrorTypesResponseBody.Data item : data) {
            System.out.println("主维度名称: " + item.getMajorClassName());
            System.out.println("主维度编码: " + item.getMajorClassCode());
            System.out.println("子维度列表:");
            
            List<ListAuditContentErrorTypesResponseBody.SubClasses> subClasses = item.getSubClasses();
            for (ListAuditContentErrorTypesResponseBody.SubClasses subItem : subClasses) {
                System.out.println("  子维度名称: " + subItem.getClassName());
                System.out.println("  子维度编码: " + subItem.getClassCode());
            }
            System.out.println("----------------------------\n");

            // 只收集基础性审核四大类的子审核编码
            if (majorTypes.contains(item.getMajorClassCode())) {
                subAuditCodes.addAll(
                    item.getSubClasses().stream()
                        .map(ListAuditContentErrorTypesResponseBody.SubClasses::getClassCode)
                        .collect(Collectors.toList())
                );
            }
        }

        System.out.println("共获取 " + subAuditCodes.size() + " 个基础性审核子编码（四大类）");
        return subAuditCodes;
    }
}
```

## **3\. 图片审校**

本示例演示如何使用图片审核功能进行内容审核：

1.  提交图片审核任务（支持多张图片）
    
2.  轮询获取审核结果
    
3.  导出审核报告
    

注意：图片审核的编码为：ImageAudit。在提交审核任务时，需要将此编码添加到 subCodes 参数中。

```
package org.example.audit;

import java.util.Arrays;
import java.util.Collections;
import java.util.concurrent.ExecutionException;

import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponseBody;

/**
 * 图片审核示例
 *
 * <p>本示例演示如何使用图片审核功能进行内容审核：</p>
 * <ol>
 *   <li>提交图片审核任务（支持多张图片）</li>
 *   <li>轮询获取审核结果</li>
 *   <li>导出审核报告</li>
 * </ol>
 *
 * <p><strong>注意：</strong>图片审核的编码为：<strong>ImageAudit</strong>。在提交审核任务时，需要将此编码添加到 {@code subCodes} 参数中。</p>
 *
 * <p>API参考文档：</p>
 * <ul>
 *   <li>提交审核任务：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartAudit">SubmitSmartAudit</a></li>
 *   <li>查询智能审核结果：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult">GetSmartAuditResult</a>
 *   </li>
 *   <li>导出审核报告：
 *   <a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportAuditContentResult">ExportAuditContentResult</a></li>
 * </ul>
 */
public class ImageAuditExample {

    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    /**
     * 业务空间唯一标识
     * 获取业务空间，参考文档：<a href="https://help.aliyun.com/zh/model-studio/use-workspace">使用工作空间</a>
     */
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("ENDPOINT", "aimiaobi.cn-beijing.aliyuncs.com");

    public static void main(String[] args) throws Exception {
        AsyncClient client = AuditUtils.createAsyncClient(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET,
            ENDPOINT);

        // 提交图片审核任务
        String taskId = submitAuditTask(client);

        // 轮询获取审核结果
        AuditUtils.pollAuditResult(client, WORKSPACE_ID, taskId);

        // 导出审核结果
        AuditUtils.exportAuditResults(client, WORKSPACE_ID, taskId);
    }

    /**
     * 提交图片审核任务
     *
     * <p>本方法演示如何提交图片审核任务，支持同时审核多张图片。</p>
     *
     * <p><strong>说明：</strong>图片URL可以是：</p>
     * <ul>
     *   <li>公网可访问的HTTP/HTTPS链接</li>
     *   <li>Base64编码的图片数据（格式：data:image/png;base64,xxx）</li>
     * </ul>
     *
     * <p><strong>注意：</strong>示例中的图片URL仅作为演示用途，实际使用时请替换为您自己的图片URL。
     * 如果使用OSS存储，需要生成带签名的URL，请参考OSS文档：<a href="https://help.aliyun.com/document_detail/32016.html">生成签名URL</a></p>
     *
     * @param client 异步客户端
     * @return 任务ID
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    private static String submitAuditTask(AsyncClient client) throws InterruptedException, ExecutionException {
        SubmitSmartAuditRequest.Builder builder = SubmitSmartAuditRequest.builder().workspaceId(WORKSPACE_ID);

        // 设置审核维度为图片审核
        // 注意：图片审核的编码为 ImageAudit
        builder.subCodes(Collections.singletonList("ImageAudit"));

        // 注意：请替换为您自己的图片URL。图片ID用于在审核结果中关联对应的图片，便于后续处理，建议使用业务上唯一的ID
        SubmitSmartAuditRequest.ImageUrlList.Builder image1 = SubmitSmartAuditRequest.ImageUrlList.builder()
            .url("https://example.com/images/sample1.jpg"); // 请替换为您自己的图片URL
        // 图片ID：此ID为图片的唯一标识，将用于在审核结果中关联对应的图片，便于您进行后续处理。建议使用业务上唯一的ID
        image1.id("image_001");

        SubmitSmartAuditRequest.ImageUrlList.Builder image2 = SubmitSmartAuditRequest.ImageUrlList.builder()
            .url("https://example.com/images/sample2.jpg"); // 请替换为您自己的图片URL
        image2.id("image_002");
        // 设置图片列表（可添加多张图片）
        builder.imageUrlList(Arrays.asList(image1.build(), image2.build()));

        // 提交审核任务
        SubmitSmartAuditResponse auditResponse = client.submitSmartAudit(builder.build()).get();
        SubmitSmartAuditResponseBody.Data responseData = auditResponse.getBody().getData();
        String taskId = responseData.getTaskId();

        System.out.println(
            "提交图片审核任务成功，任务ID: " + taskId + "，requestId:" + auditResponse.getBody().getRequestId());
        return taskId;
    }
}
```

## **4\. 联网事实性审校**

本示例演示如何使用事实性审核功能进行内容审核：

1.  配置授信的信源（可选，用于指定可信的数据源）
    
2.  提交事实性审核任务
    
3.  轮询获取审核结果
    
4.  导出审核报告
    

**注意：**

事实性审核的编码包括：

CorrectFact：事实性审核-正确项

WrongFactError：事实性审核-错误项

在提交审核任务时，需要将这些编码添加到 subCodes 参数中。

**关于授信信源：**授信信源是事实性审核的核心机制。系统会从您配置的可信数据源中获取信息，用于验证待审核内容的事实性。

**作用**：授信信源作为事实性判断的参考依据，系统会优先从这些可信源中查找相关信息来验证内容的事实性。

**影响**：配置的信源质量直接影响事实性审核的准确性。建议选择权威、可靠的数据源。

```
package org.example.audit;

import java.util.Arrays;
import java.util.Collections;
import java.util.concurrent.ExecutionException;

import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitFactAuditUrlRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitFactAuditUrlResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponseBody;

/**
 * 事实性审核示例
 *
 * <p>本示例演示如何使用事实性审核功能进行内容审核：</p>
 * <ol>
 *   <li>配置授信的信源（可选，用于指定可信的数据源）</li>
 *   <li>提交事实性审核任务</li>
 *   <li>轮询获取审核结果</li>
 *   <li>导出审核报告</li>
 * </ol>
 *
 * <p><strong>注意：</strong>事实性审核的编码包括：</p>
 * <ul>
 *   <li><strong>CorrectFact</strong>：事实性审核-正确项</li>
 *   <li><strong>WrongFactError</strong>：事实性审核-错误项</li>
 * </ul>
 * <p>在提交审核任务时，需要将这些编码添加到 {@code subCodes} 参数中。</p>
 *
 * <p><strong>关于授信信源：</strong></p>
 * <p>授信信源是事实性审核的核心机制。系统会从您配置的可信数据源中获取信息，用于验证待审核内容的事实性。</p>
 * <ul>
 *   <li><strong>作用：</strong>授信信源作为事实性判断的参考依据，系统会优先从这些可信源中查找相关信息来验证内容的事实性。</li>
 *   <li><strong>必要性：</strong>虽然配置授信信源是可选步骤，但强烈建议配置，因为：</li>
 *   <ul>
 *     <li>配置后，系统会从这些可信源中验证事实，提高审核准确性</li>
 *     <li>未配置时，系统可能无法准确判断某些事实性信息</li>
 *     <li>可以配置多个可信源，系统会综合多个源的信息进行判断</li>
 *   </ul>
 *   <li><strong>影响：</strong>配置的信源质量直接影响事实性审核的准确性。建议选择权威、可靠的数据源。</li>
 * </ul>
 * <p>可以通过 {@link #configureTrustedSources(AsyncClient)} 方法配置多个可信源。</p>
 *
 * <p>API参考文档：</p>
 * <ul>
 *   <li>提交审核任务：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartAudit">SubmitSmartAudit</a></li>
 *   <li>配置授信信源：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitFactAuditUrl">SubmitFactAuditUrl</a></li>
 *   <li>查询智能审核结果：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult">GetSmartAuditResult</a>
 *   </li>
 *   <li>导出审核报告：
 *   <a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportAuditContentResult">ExportAuditContentResult</a></li>
 * </ul>
 */
public class FactAuditExample {

    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    /**
     * 业务空间唯一标识
     * 获取业务空间，参考文档：<a href="https://help.aliyun.com/zh/model-studio/use-workspace">使用工作空间</a>
     */
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("ENDPOINT", "aimiaobi.cn-beijing.aliyuncs.com");

    public static void main(String[] args) throws Exception {
        AsyncClient client = AuditUtils.createAsyncClient(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET,
            ENDPOINT);

        // 配置授信的信源
        // 如果不需要配置信源，可以注释掉下面这行代码
        configureTrustedSources(client);

        // 提交事实性审核任务
        String taskId = submitAuditTask(client);

        // 轮询获取审核结果
        AuditUtils.pollAuditResult(client, WORKSPACE_ID, taskId);

        // 导出审核结果
        AuditUtils.exportAuditResults(client, WORKSPACE_ID, taskId);
    }

    /**
     * 配置授信的信源
     *
     * <p>本方法用于配置事实性审核的可信数据源。授信信源是事实性审核的核心机制，
     * 系统会从您配置的可信数据源中获取信息，用于验证待审核内容的事实性。</p>
     *
     * <p><strong>授信信源的作用：</strong></p>
     * <ul>
     *   <li>作为事实性判断的参考依据，系统会优先从这些可信源中查找相关信息</li>
     *   <li>可以配置多个可信源，系统会综合多个源的信息进行判断</li>
     *   <li>配置的信源质量直接影响事实性审核的准确性，建议选择权威、可靠的数据源</li>
     * </ul>
     *
     * <p><strong>配置的必要性：</strong></p>
     * <p>虽然配置授信信源是可选步骤，但强烈建议配置，因为：</p>
     * <ul>
     *   <li>配置后，系统会从这些可信源中验证事实，提高审核准确性</li>
     *   <li>未配置时，系统可能无法准确判断某些事实性信息</li>
     *   <li>可以配置多个可信源，系统会综合多个源的信息进行判断</li>
     * </ul>
     *
     * <p><strong>注意：</strong>请将示例URL替换为您实际使用的可信数据源URL。
     * 建议选择权威、可靠的数据源，如官方新闻网站、权威百科等。</p>
     *
     * @param client 异步客户端
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    public static void configureTrustedSources(AsyncClient client) throws InterruptedException, ExecutionException {
        // 请替换为您自己的可信源域名
        for (String trustedSite : Collections.singletonList(
            "hangzhou.com.cn"
        )) {
            // 配置可信源
            // 注意：请替换为您实际使用的可信数据源URL
            SubmitFactAuditUrlResponse response1 = client.submitFactAuditUrl(
                SubmitFactAuditUrlRequest.builder().workspaceId(WORKSPACE_ID)
                    .url(trustedSite)
                    .build()).get();

            if (response1.getBody().getSuccess()) {
                System.out.println("配置授信信源成功: " + trustedSite);
            } else {
                System.err.println("配置授信信源失败: " + response1.getBody().getMessage());
            }
        }

    }

    /**
     * 提交事实性审核任务
     *
     * <p>本方法演示如何提交事实性审核任务。事实性审核用于验证内容中的事实性信息是否正确。</p>
     *
     * <p><strong>说明：</strong>事实性审核需要先配置授信的信源（通过 {@link #configureTrustedSources(AsyncClient)} 方法），
     * 系统会从这些可信源中验证内容的事实性。</p>
     *
     * @param client 异步客户端
     * @return 任务ID
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    private static String submitAuditTask(AsyncClient client) throws InterruptedException, ExecutionException {
        SubmitSmartAuditRequest.Builder builder = SubmitSmartAuditRequest.builder().workspaceId(WORKSPACE_ID);

        // 设置审核维度为事实性审核
        // CorrectFact: 事实性审核-正确项
        // WrongFactError: 事实性审核-错误项
        builder.subCodes(Arrays.asList("CorrectFact", "WrongFactError"));

        // 示例文本：包含事实性信息的待审核内容
        // 请替换为您需要审核的实际内容
        builder.text("2025杭州马拉松全马冠军是中国籍的");
        // 提交审核任务
        SubmitSmartAuditResponse auditResponse = client.submitSmartAudit(builder.build()).get();
        SubmitSmartAuditResponseBody.Data responseData = auditResponse.getBody().getData();
        String taskId = responseData.getTaskId();

        System.out.println(
            "提交事实性审核任务成功，任务ID: " + taskId + "，requestId:" + auditResponse.getBody().getRequestId());
        return taskId;
    }
}
```

## **5\. 规则库审校**

**功能说明**

规则库审校是基于自定义规则的内容审核功能，允许您根据业务需求定义特定的审核规则，系统会根据这些规则对内容进行审核。该功能分为两个阶段：**规则准备阶段**和**内容审校阶段**。

**使用流程**

1.  **首次使用：** 先运行 RuleLibraryPreparationExample 完成规则库的准备
    
2.  **日常审核：** 运行 RuleBasedContentAuditExample 进行内容审核
    
3.  **更新规则：** 如需更新规则库，重新运行阶段一的示例
    

### **规则准备阶段**

**功能说明：**

规则库是自定义的审核规则集合，允许您根据业务需求定义特定的审核规则。规则库文件需要按照模板格式准备，上传后系统会进行解析和语义化索引处理。

**主要步骤：**

1.  上传并解析规则库文件
    
2.  对规则库进行语义化索引处理
    

**注意事项：**

-   规则库文件需要按照模板格式准备，可参考模板文件：[规则库模板](https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/templates/%E8%A7%84%E5%88%99%E5%BA%93%E6%A8%A1%E6%9D%BF1105.xlsx)
    
-   请将示例中的文件路径替换为您实际的规则库文件路径
    
-   规则库文件格式不正确可能导致解析失败
    

**规则库的作用：**

-   允许您自定义审核规则，如禁止使用某些词汇、限制特定表达方式等
    
-   系统会根据规则库中的规则对内容进行审核
    

**相关API：**

-   提交规则库：[SubmitAuditNote](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitAuditNote)
    
-   查询规则库解析状态：[GetAuditNoteProcessingStatus](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNoteProcessingStatus)
    
-   确认并处理规则库：[ConfirmAndPostProcessAuditNote](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ConfirmAndPostProcessAuditNote)
    
-   查询语义化索引状态：[GetAuditNotePostProcessingStatus](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNotePostProcessingStatus)
    

```
package org.example.audit;

import java.util.concurrent.ExecutionException;

import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.ConfirmAndPostProcessAuditNoteRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.ConfirmAndPostProcessAuditNoteResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNotePostProcessingStatusRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNotePostProcessingStatusResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNotePostProcessingStatusResponseBody;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNoteProcessingStatusRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNoteProcessingStatusResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.GetAuditNoteProcessingStatusResponseBody.Data;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitAuditNoteRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitAuditNoteResponse;

/**
 * 规则库准备示例
 *
 * <p>本示例演示如何准备规则库，包括以下步骤：</p>
 * <ol>
 *   <li>上传并解析规则库文件</li>
 *   <li>对规则库进行语义化索引处理（用于后续审核的搜索匹配）</li>
 * </ol>
 *
 * <p><strong>关于规则库：</strong></p>
 * <p>规则库是自定义的审核规则集合，允许您根据业务需求定义特定的审核规则。
 * 规则库文件需要按照模板格式准备，上传后系统会进行解析和语义化索引处理。</p>
 * <ul>
 *   <li><strong>作用：</strong>规则库允许您自定义审核规则，如禁止使用某些词汇、限制特定表达方式等，
 *   系统会根据规则库中的规则对内容进行审核。</li>
 *   <li><strong>文件格式：</strong>规则库文件需要按照模板格式准备，可参考模板文件：
 *   <a href="https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/templates/%E8%A7%84%E5%88%99%E5%BA%93%E6%A8%A1%E6%9D%BF1105.xlsx">规则库模板</a></li>
 *   <li><strong>处理流程：</strong>上传规则库文件后，系统会先进行解析，然后进行语义化索引处理。
 *   语义化索引处理完成后，规则库才能用于内容审核。</li>
 * </ul>
 *
 * <p><strong>注意：</strong>请将示例中的文件路径替换为您实际的规则库文件路径。
 * 规则库文件需要按照模板格式准备，否则可能导致解析失败。</p>
 *
 * <p>API参考文档：</p>
 * <ul>
 *   <li>提交规则库：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitAuditNote">SubmitAuditNote</a></li>
 *   <li>查询规则库解析状态：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNoteProcessingStatus">GetAuditNoteProcessingStatus</a></li>
 *   <li>确认并处理规则库：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ConfirmAndPostProcessAuditNote">ConfirmAndPostProcessAuditNote</a></li>
 *   <li>查询语义化索引状态：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetAuditNotePostProcessingStatus">GetAuditNotePostProcessingStatus</a></li>
 * </ul>
 */
public class RuleLibraryPreparationExample {

    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("ENDPOINT", "aimiaobi.cn-beijing.aliyuncs.com");
    /**
     * 最大轮询次数（每次等待2秒，总共最多等待约10分钟）
     */
    private static final int MAX_POLLING_COUNT = 300;

    public static void main(String[] args) throws Exception {
        AsyncClient client = AuditUtils.createAsyncClient(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET,
            ENDPOINT);

        // 示例：上传并解析规则库文件
        // 请将文件路径替换为您的实际规则库文件路径
        String ruleLibraryFilePath = "/Users/weisanju/Downloads/规则库模板1105.xlsx";
        //示例文件内容为： 避免口语化、网络语、主观情绪词（正式文本），如"超赞""巨多""贼好"等不得出现；慎用"非常""极其"等模糊强调词。
        //可参考模板文件：https://aimiaobi-service-prod.oss-cn-beijing.aliyuncs.com/templates/%E8%A7%84%E5%88%99%E5%BA%93%E6%A8%A1%E6%9D%BF1105.xlsx

        uploadAndParseRuleLibrary(client, ruleLibraryFilePath);
    }

    /**
     * 上传并解析规则库文件
     *
     * @param client   异步客户端
     * @param filePath 规则库文件路径
     * @throws Exception 处理异常
     */
    public static void uploadAndParseRuleLibrary(AsyncClient client, String filePath)
        throws Exception {
        // 上传规则库文件，获取唯一标识符
        String fileKey = AuditUtils.uploadFile(client, WORKSPACE_ID, filePath);

        SubmitAuditNoteResponse response = client.submitAuditNote(SubmitAuditNoteRequest.builder().workspaceId(
            WORKSPACE_ID).fileKey(fileKey).build()).get();

        String taskId = response.getBody().getData();

        System.out.println("提交规则库解析任务成功，任务ID：" + taskId);

        GetAuditNoteProcessingStatusResponse processingStatusResponse = null;
        boolean success = false;
        for (int i = 0; i < MAX_POLLING_COUNT; i++) {
            GetAuditNoteProcessingStatusRequest query = GetAuditNoteProcessingStatusRequest.builder().taskId(taskId)
                .workspaceId(WORKSPACE_ID).build();
            processingStatusResponse = client.getAuditNoteProcessingStatus(query).get();

            String status = processingStatusResponse.getBody().getData().getStatus();
            if ("RUNNING".equals(status) || "PENDING".equals(status)) {
                System.out.println("规则库解析中，请稍等...（" + (i + 1) + "/" + MAX_POLLING_COUNT + "）");
                Thread.sleep(2000);
            } else {
                success = true;
                break;
            }
        }

        if (!success) {
            throw new RuntimeException("规则库解析超时，已达到最大轮询次数：" + MAX_POLLING_COUNT);
        }

        Data data = processingStatusResponse.getBody().getData();

        String resultFileKey = data.getFileKey();

        String resultTaskId = data.getTaskId();

        System.out.println("规则库解析成功，结果文件：" + resultFileKey + "， 任务ID：" + resultTaskId);

        //开始语义化索引，用于后续审核的搜索匹配
        ConfirmAndPostProcessAuditNoteResponse confirmAndPostProcessAuditNoteResponse
            = client.confirmAndPostProcessAuditNote(
            ConfirmAndPostProcessAuditNoteRequest.builder().taskId(resultTaskId).workspaceId(WORKSPACE_ID).build()
        ).get();

        String embeddingTaskId = confirmAndPostProcessAuditNoteResponse.getBody().getData();

        System.out.println("提交语义化索引任务成功，任务ID：" + embeddingTaskId);

        GetAuditNotePostProcessingStatusResponse statusResponse = null;
        boolean vectorizationSuccess = false;
        for (int i = 0; i < MAX_POLLING_COUNT; i++) {
            GetAuditNotePostProcessingStatusRequest build = GetAuditNotePostProcessingStatusRequest.builder()
                .workspaceId(WORKSPACE_ID).taskId(embeddingTaskId).build();
            statusResponse = client.getAuditNotePostProcessingStatus(build).get();

            String status = statusResponse.getBody().getData().getStatus();
            if ("RUNNING".equals(status) || "PENDING".equals(status)) {
                System.out.println("语义化索引中，请稍等...（" + (i + 1) + "/" + MAX_POLLING_COUNT + "）");
                Thread.sleep(2000);
            } else {
                vectorizationSuccess = true;
                break;
            }
        }

        if (!vectorizationSuccess) {
            throw new RuntimeException("语义化索引超时，已达到最大轮询次数：" + MAX_POLLING_COUNT);
        }

        GetAuditNotePostProcessingStatusResponseBody.Data data1 = statusResponse.getBody().getData();
        System.out.println("语义化索引成功，任务状态：" + data1.getStatus());
    }
}
```

### **内容审校阶段**

**功能说明：**

使用已准备好的规则库对内容进行审核，系统会根据规则库中的规则检查内容是否符合要求。

**注意事项：**

-   **前置条件：** 在使用本示例之前，请确保已经完成了规则库的准备阶段（阶段一），包括规则库文件的上传、解析和语义化索引处理
    
-   **审核编码：** 规则库审核的编码为 WrongQuestionBook，在提交审核任务时，需要将此编码添加到 subCodes 参数中
    
-   请将示例文本替换为您需要审核的实际内容
    

```
package org.example.audit;

import java.util.Collections;
import java.util.concurrent.ExecutionException;

import com.aliyun.sdk.service.aimiaobi20230801.AsyncClient;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditRequest;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponse;
import com.aliyun.sdk.service.aimiaobi20230801.models.SubmitSmartAuditResponseBody;

/**
 * 基于规则库的内容审核示例
 *
 * <p>本示例演示如何使用已准备好的规则库进行内容审核，包括以下步骤：</p>
 * <ol>
 *   <li>提交内容审核任务</li>
 *   <li>轮询获取审核结果</li>
 *   <li>导出审核报告</li>
 * </ol>
 *
 * <p><strong>注意：</strong>规则库审核的编码为：<strong>WrongQuestionBook</strong>。
 * 在提交审核任务时，需要将此编码添加到 {@code subCodes} 参数中。</p>
 *
 * <p><strong>前置条件：</strong></p>
 * <p>在使用本示例之前，请确保已经完成了规则库的准备阶段（通过 {@link RuleLibraryPreparationExample} 完成），
 * 包括规则库文件的上传、解析和语义化索引处理。</p>
 *
 * <p>API参考文档：</p>
 * <ul>
 *   <li>提交审核任务：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SubmitSmartAudit">SubmitSmartAudit</a></li>
 *   <li>查询智能审核结果：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/GetSmartAuditResult">GetSmartAuditResult</a></li>
 *   <li>导出审核报告：<a href="https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ExportAuditContentResult">ExportAuditContentResult</a></li>
 * </ul>
 */
public class RuleBasedContentAuditExample {

    private static final String ALIBABA_CLOUD_ACCESS_KEY_ID = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID");
    private static final String ALIBABA_CLOUD_ACCESS_KEY_SECRET = System.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET");
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID");
    private static final String ENDPOINT = System.getenv().getOrDefault("ENDPOINT", "aimiaobi.cn-beijing.aliyuncs.com");

    /**
     * 规则库审核类型代码
     */
    private static final String RULE_BASED_AUDIT_TYPE = "WrongQuestionBook";

    public static void main(String[] args) throws Exception {
        AsyncClient client = AuditUtils.createAsyncClient(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET,
            ENDPOINT);

        // 提交内容审核任务
        String taskId = submitAuditTask(client);

        // 轮询获取审核结果
        AuditUtils.pollAuditResult(client, WORKSPACE_ID, taskId);

        // 导出审核结果
        AuditUtils.exportAuditResults(client, WORKSPACE_ID, taskId);
    }

    /**
     * 提交内容审核任务
     *
     * @param client 异步客户端
     * @return 任务ID
     * @throws InterruptedException 中断异常
     * @throws ExecutionException 执行异常
     */
    private static String submitAuditTask(AsyncClient client) throws InterruptedException, ExecutionException {
        // 示例文本：请替换为您需要审核的实际内容
        String contentToAudit
            = "这次活动的效果超赞，现场来了巨多人，气氛贼好。大家都特别激动，感觉整个流程非常顺利，极其成功。";

        SubmitSmartAuditRequest.Builder builder = SubmitSmartAuditRequest.builder().workspaceId(WORKSPACE_ID);
        builder.subCodes(Collections.singletonList(RULE_BASED_AUDIT_TYPE));
        builder.text(contentToAudit);

        SubmitSmartAuditResponse auditResponse = client.submitSmartAudit(builder.build()).get();
        SubmitSmartAuditResponseBody.Data responseData = auditResponse.getBody().getData();
        String taskId = responseData.getTaskId();

        System.out.println(
            "提交审核任务成功，任务ID: " + taskId + "，requestId:" + auditResponse.getBody().getRequestId());
        return taskId;
    }
}
```
