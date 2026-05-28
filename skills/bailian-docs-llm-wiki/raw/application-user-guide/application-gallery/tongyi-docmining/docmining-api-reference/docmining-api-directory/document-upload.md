# 文档上传

本文为您介绍通义数据挖掘文档上传API的语法及示例。

## **1\. 申请上传租约**

### **请求语法**

```
POST /zhiwen-file/apply_upload_lease HTTP/1.1
```

### **请求参数**

**名称**

**类型**

**必填**

**描述**

**示例值**

fileName

string

是

文档名称

阿里云百炼.pdf

sizeBytes

number

是

上传文档的大小，单位字节

28123

md5

string

是

文档md5

### **返回参数**

**名称**

**类型**

**描述**

code

int

状态码

data

object

相应数据

\-param

object

用于上传文档的 HTTP 请求参数

\-headers

object

第2步上传文档时，需要放到 Header 中的 K-V 字段，K 和 V 均为字符串

\-x-bailian-extra

string

\-Content-Type

string

\-method

string

HTTP 调用方法

\-url

string

第2步上传文档时请求的url

\-type

string

文档的上传方式

\-lease\_id

string

租约唯一 ID，第3步提交文档解析接口时，需要使用该参数

requestId

string

请求ID

success

boolean

是否成功

message

string

响应消息

### **示例**

正常返回示例

`JSON`格式

```
{
  "code": 200,
  "data": {
    "param": {
      "headers": {
        "x-bailian-extra": "PkdiMDOidwEwMTE4KnY2MQ==",
        "Content-Type": "text/plain"
      },
      "method": "PUT",
      "url": "https://dashscope-file-datacenter-prod-01.oss-cn-beijing.aliyuncs.com/1880205101189661/10064170/zhiwen/3631bf9f24ea4ac7b362a135deee7fec.1753176187488.txt?Expires=1753182187&OSSAccessKeyId=TestID&Signature=4%2Ba%2B9UoSjdSIj7a4FErUqBwOSfc%3D"
    },
    "type": "OSS.PreSignedUrl",
    "lease_id": "3631bf9f24ea4ac7b3dr5135deee7fec.1752176287488"
  },
  "requestId": "e1cdcfab-897d-9b7b-8c38-72aa39a13c87",
  "success": true,
  "message": "成功"
}
```

## **2\. 上传文档到OSS**

使用上一步（申请文档上传租约）返回的`data.param.url`、`data.param.method`、`data.param.headers`中`x-bailian-extra`和`Content-Type`等参数，将您在本地的文档上传至OSS。示例代码如下。

Python

```
# 示例代码仅供参考，请勿在生产环境中直接使用
import requests

def upload_file(pre_signed_url, file_path):
    try:
        # 设置请求头
        headers = {
            "x-bailian-extra": "请替换为您在上一步中调用申请上传租约接口实际返回的data.param.headers中X-bailian-extra字段的值",
            "Content-Type": "请替换为您在上一步中调用申请上传租约接口实际返回的data.param.headers中Content-Type字段的值"
        }

        # 读取文档并上传
        with open(file_path, 'rb') as file:
            # 下方设置请求方法用于文档上传，需与您在上一步中调用申请上传租约接口实际返回的data.param中method字段的值一致
            response = requests.put(pre_signed_url, data=file, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload the file. ResponseCode: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":

    pre_signed_url_or_http_url = "请替换为您在上一步中调用申请上传租约接口实际返回的data.param中url字段的值"

    # 文档来源是本地，上传本地文档至OSS
    file_path = "请替换为您需要上传文档的实际本地路径"
    upload_file(pre_signed_url_or_http_url, file_path)
```

Java

```
// 示例代码仅供参考，请勿在生产环境中直接使用
import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class UploadFile{

    public static void uploadFile(String preSignedUrl, String filePath) {
        HttpURLConnection connection = null;
        try {
            // 创建URL对象
            URL url = new URL(preSignedUrl);
            connection = (HttpURLConnection) url.openConnection();

            // 设置请求方法用于文档上传，需与您在上一步中调用申请上传租约接口实际返回的data.param中method字段的值一致
            connection.setRequestMethod("PUT");

            // 允许向connection输出，因为这个连接是用于上传文档的
            connection.setDoOutput(true);

            connection.setRequestProperty("x-bailian-extra", "请替换为您在上一步中调用申请上传租约接口实际返回的data.param.headers中x-bailian-extra字段的值");
            connection.setRequestProperty("Content-Type", "请替换为您在上一步中调用申请上传租约接口实际返回的data.param.headers中Content-Type字段的值");

            // 读取文档并通过连接上传
            try (DataOutputStream outStream = new DataOutputStream(connection.getOutputStream());
                 FileInputStream fileInputStream = new FileInputStream(filePath)) {
                byte[] buffer = new byte[4096];
                int bytesRead;

                while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                    outStream.write(buffer, 0, bytesRead);
                }

                outStream.flush();
            }

            // 检查响应
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 文档上传成功处理
                System.out.println("File uploaded successfully.");
            } else {
                // 文档上传失败处理
                System.out.println("Failed to upload the file. ResponseCode: " + responseCode);
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }

    public static void main(String[] args) {

        String preSignedUrlOrHttpUrl = "请替换为您在上一步中调用申请上传租约接口实际返回的data.param中url字段的值";

        // 文档来源是本地，上传本地文档至OSS
        String filePath = "请替换为您需要上传文档的实际本地路径";
        uploadFile(preSignedUrlOrHttpUrl, filePath);
    }
}
```

## **3\. 提交解析文档**

### **请求语法**

```
POST /zhiwen-file/submit_parse_file HTTP/1.1
```

### **请求参数**

**名称**

**类型**

**必填**

**描述**

**示例值**

leaseId

string

是

租约唯一 ID，通过申请租约获取。

3631bf9f24ea4ac7b3dr5135deee7fec.1752176287488

### **返回参数**

**名称**

**类型**

**描述**

code

int

状态码

data

object

\-fileSize

string

文档大小

\-docId

string

docId

\-name

string

文档名称

\-pageSize

number

页数

\-type

string

文档类型

\-url

string

文档地址

\-fileId

string

文档ID，后续对话需使用此ID

requestId

string

请求ID

success

boolean

是否成功

message

string

响应消息

### **示例**

正常返回示例

`JSON`格式

```
{
  "code": 200,
  "data": {
    "fileSize": "280931",
    "docId": "1397267735092973568",
    "name": "阿里云百炼",
    "pageSize": 5,
    "type": "pdf",
    "url": "https://dashscope-file-datacenter-prod-01.oss-cn-beijing.aliyuncs.com/1880205101189661/10064170/zhiwen/3631bf9f24ea4ac7b362a135deee7fec.1753176187488.pdf?Expires=1753435388&OSSAccessKeyId=TestID&Signature=PfS0v1YqpH7MsbEJ7Ma%2FsablW50%3D",
    "fileId": "file_zhiwen_XXX"
  },
  "requestId": "e33ba5e9-fef6-96ae-b8b0-1b4a0c151e2b",
  "success": true,
  "message": "成功"
}
```

## **调用示例**

Python

```
import hashlib
import os
import requests
from http import HTTPStatus

'''
API名称：文档上传
API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/apply_upload_lease
        https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/submit_parse_file
环境要求：Python >= 3.7
'''

apply_lease_url = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/apply_upload_lease"
submit_file_url = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/submit_parse_file"
request_headers = {
    "Authorization": os.environ.get("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处替换您的API-KEY
    "Content-Type": "application/json"
}

file_path = "./test.txt"
file_name = os.path.basename(file_path)
file_size = os.path.getsize(file_path)
with open(file_path, 'rb') as f:
    md5 = hashlib.md5()
    while True:
        data = f.read(4096)  # 每次读取4KB数据
        if not data:
            break
        md5.update(data)
file_md5 = md5.hexdigest()

# 1. 申请租约
response = requests.post(apply_lease_url,
                         json={
                             "fileName": file_name,
                             "sizeBytes": file_size,
                             "md5": file_md5
                         },
                         headers=request_headers)
lease_data = {}
if response.status_code == HTTPStatus.OK:
    print("1. Lease applied successfully.")
    print(response.json())
    lease_data = response.json()['data']
else:
    print(f'response={response.json()}')
    print(f'code={response.status_code}')

# 2. 上传文档
upload_headers = {
    "X-bailian-extra": lease_data['param']['headers']['x-bailian-extra'],
    "Content-Type": lease_data['param']['headers']['Content-Type']
}
with open(file_path, 'rb') as file:
    # 下方设置请求方法用于文档上传，需与您在上一步中调用ApplyFileUploadLease接口实际返回的Data.Param中Method字段的值一致
    response = requests.put(lease_data['param']['url'], data=file, headers=upload_headers)
if response.status_code == HTTPStatus.OK:
    print("2. File uploaded successfully.")
else:
    print(f"Failed to upload the file. ResponseCode: {response.status_code}")

# 3.提交解析
response = requests.post(submit_file_url,
                         json={
                             'leaseId': lease_data['lease_id']
                         },

                         headers=request_headers)
if response.status_code == HTTPStatus.OK:
    print("3. File submit parse successfully.")
    print(response.json())
else:
    print(f'response={response.json()}')
    print(f'code={response.status_code}')
```

Java

```
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.http.HttpResponse;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.FileEntity;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * API名称：文档上传
 * API路径：https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/apply_upload_lease
 *         https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/submit_parse_file
 * 环境要求：Java 8及以上
 */
public class FileUploadDemo {
    // Step 1. API 地址和配置
    private static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");    // 填写百炼平台的 API KEY
    private static final String APPLY_UPLOAD_URL = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/apply_upload_lease";
    private static final String SUBMIT_PARSE_URL = "https://dashscope.aliyuncs.com/api/v2/apps/zhiwen-file/submit_parse_file";
    private static final String CHARSET = "UTF-8";
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) {
        String filePath = "your_file_path";
        try {
            File file = new File(filePath);
            if (!file.exists()) {
                System.out.println("文档不存在: " + filePath);
                return;
            }
            // Step 2. 申请上传租约
            Map<String, String> leaseInfo = applyUploadLease(file.getName(), file.length());
            String leaseId = leaseInfo.get("lease_id");
            String uploadUrl = leaseInfo.get("url");

            Map<String, String> uploadHeaders = new HashMap<>();
            uploadHeaders.put("x-bailian-extra", leaseInfo.get("x-bailian-extra"));
            uploadHeaders.put("Content-Type", leaseInfo.get("Content-Type"));

            // Step 3. 上传文档到百炼OSS
            boolean uploadSuccess = uploadFileToOSS(uploadUrl, uploadHeaders, file);

            if (uploadSuccess) {
                // Step 4. ：提交解析
                String parseResult = submitFileForParsing(leaseId);
                System.out.println("\n解析结果: ");
                // 返回结果中的 fileId 字段用于后续文档对话使用
                System.out.println(parseResult);
            } else {
                System.out.println("文档上传失败.");
            }
        } catch (Exception e) {
            System.err.println("Error occurred:");
            e.printStackTrace();
        }
    }

    /**
     * 申请上传租约
     * 该方法用于向服务器申请一个上传租约，包括上传所需的URL和相关参数
     *
     * @param fileName 文档名，用于标识要上传的文档
     * @param fileSize 文档大小，以字节为单位，用于申请合适的存储空间
     * @return 返回一个包含上传所需信息的Map，包括租约ID、上传URL和额外的请求头参数
     * @throws Exception 如果申请上传租约失败或在处理过程中发生错误，则抛出异常
     */
    private static Map<String, String> applyUploadLease(String fileName, long fileSize) throws Exception {
        // 创建请求体，包含文档名、文档大小和MD5值
        ObjectNode requestBodyMap = objectMapper.createObjectNode();
        requestBodyMap.put("fileName", fileName);
        requestBodyMap.put("sizeBytes", fileSize);
        // md5值可任意填写
        requestBodyMap.put("md5", "md5");
        String requestBody = objectMapper.writeValueAsString(requestBodyMap);
        // 配置请求的超时时间
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(30 * 1000).build();

        HttpPost httpPost = new HttpPost(APPLY_UPLOAD_URL);
        httpPost.setHeader("Authorization", API_KEY);
        httpPost.setHeader("Content-Type", "application/json");
        httpPost.setEntity(new StringEntity(requestBody, CHARSET));

        try (CloseableHttpClient httpClient = HttpClients.custom().setDefaultRequestConfig(requestConfig).build()) {
            HttpResponse response = httpClient.execute(httpPost);
            int statusCode = response.getStatusLine().getStatusCode();
            if (statusCode != 200) {
                throw new IOException("HTTP request failed with status code: " + statusCode);
            }
            String responseBody = EntityUtils.toString(response.getEntity());
            JsonNode rootNode = objectMapper.readTree(responseBody);
            if (!rootNode.path("success").asBoolean()) {
                throw new RuntimeException("Apply upload lease failed: " + responseBody);
            }

            JsonNode dataNode = rootNode.path("data");
            JsonNode paramNode = dataNode.path("param");
            JsonNode headersNode = paramNode.path("headers");

            Map<String, String> result = new HashMap<>();
            result.put("lease_id", dataNode.path("lease_id").asText());
            result.put("url", paramNode.path("url").asText());
            result.put("x-bailian-extra", headersNode.path("x-bailian-extra").asText());
            result.put("Content-Type", headersNode.path("Content-Type").asText());

            result.forEach((key, value) -> System.out.println(key + ": " + value));
            return result;
        }
    }

    /**
     * 将文档上传到OSS(对象存储服务)
     *
     * @param uploadUrl 文档上传的URL
     * @param headers HTTP请求的头部信息
     * @param file 要上传的文档
     * @return 如果文档上传成功返回true，否则返回false
     * @throws Exception 如果文档读取或网络请求发生错误
     */
    private static boolean uploadFileToOSS(String uploadUrl, Map<String, String> headers, File file) throws Exception {
        // 配置请求的连接超时时间
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(30 * 1000).build();

        try (CloseableHttpClient httpClient = HttpClients.custom().setDefaultRequestConfig(requestConfig).build()) {
            HttpPut httpPut = new HttpPut(uploadUrl);

            // 设置请求头
            if (headers != null) {
                headers.forEach(httpPut::setHeader);
            }

            // 使用流式上传
            FileEntity entity = new FileEntity(file);
            httpPut.setEntity(entity);

            try (CloseableHttpResponse response = (CloseableHttpResponse) httpClient.execute(httpPut)) {
                int statusCode = response.getStatusLine().getStatusCode();
                if (statusCode == 200) {
                    System.out.println("上传文档成功");
                    return true;
                } else {
                    String errorBody = EntityUtils.toString(response.getEntity());
                    System.err.println("上传文档失败: " + errorBody);
                    return false;
                }
            }
        }
    }

    /**
     * 提交文档进行解析
     *
     * @param leaseId 租约ID，用于标识和追踪文档解析请求
     * @return 解析成功的响应内容，通常包含解析后的数据
     * @throws Exception 如果文档解析过程中发生错误，抛出此异常
     */
    private static String submitFileForParsing(String leaseId) throws Exception {
        if (leaseId == null || leaseId.isEmpty()) {
            throw new IllegalArgumentException("leaseId 不能为空");
        }
        // 创建请求体并设置租约ID
        ObjectNode requestBody = objectMapper.createObjectNode();
        requestBody.put("leaseId", leaseId);

        // 配置HTTP请求的超时设置
        RequestConfig requestConfig = RequestConfig.custom().setConnectTimeout(30 * 1000).build();

        HttpPost httpPost = new HttpPost(SUBMIT_PARSE_URL);
        httpPost.setHeader("Authorization", API_KEY);
        httpPost.setHeader("Content-Type", "application/json");
        httpPost.setEntity(new StringEntity(requestBody.toString(), CHARSET));

        try (CloseableHttpClient httpClient = HttpClients.custom()
                .setDefaultRequestConfig(requestConfig)
                .build();
             CloseableHttpResponse response = httpClient.execute(httpPost)) {
            if (response == null || response.getEntity() == null) {
                throw new IOException("HTTP 响应为空");
            }
            String responseBody = EntityUtils.toString(response.getEntity(), CHARSET);
            if (response.getStatusLine().getStatusCode() != 200) {
                throw new RuntimeException("文档解析失败: " + responseBody);
            }

            System.out.println("文档解析成功");
            return responseBody;
        }
    }
}
```

## **错误码**

请参见[错误码-通义数据挖掘](https://help.aliyun.com/zh/model-studio/docmining-error-code)。
