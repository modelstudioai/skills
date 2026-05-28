# ROA风格请求体&签名机制

通过公共请求头设置接口必要的参数信息，在签名机制的实现上屏蔽了接口风格的差异，更标准、更简单。本文提供了详细的指南，用于帮助您了解和实施阿里云SDK V3版的请求结构和签名过程。您会了解如何构造标准的HTTP请求，以及如何使用正确的签名算法来验证请求的身份，确保传输的数据的完整性和安全性。如果您想自研阿里云OpenAPI的请求签名，您可以参考本文。

## 请求编码

请求及返回结果都使用UTF-8字符集进行编码。

### RequestHeader（公共请求头）

一个完整的阿里云 OpenAPI 请求，包含以下部分。

**名称**

**类型**

**是否必选**

**描述**

**示例值**

x-acs-action

String

是

API的名称。

RunInstances

x-acs-version

String

是

API 版本。

2014-05-26

Authorization

String

非匿名请求必须

用于验证请求合法性的认证信息，格式为Authorization:SignatureAlgorithmCredential=AccessKeyId,SignedHeaders=SignedHeaders,Signature=Signature。其中SignatureAlgorithm为签名加密方式，为ACS3-HMAC-SHA256。

Credential为用户的访问密钥ID。您可以在[RAM 控制台](https://ram.console.aliyun.com/manage/ak)查看您的 AccessKeyId。如需创建 AccessKey，请参见[创建AccessKey](https://help.aliyun.com/zh/document_detail/53045.html)。SignedHeaders为请求头中包含的参与签名字段键名，【说明】：除Authorization外的所有公共请求头，只要存在必须被加入签名。

Signature为请求签名，取值参见签名机制。

ACS3-HMAC-SHA256 Credential=YourAccessKeyId,SignedHeaders=host;x-acs-action;x-acs-content-sha256;x-acs-date;x-acs-signature-nonce;x-acs-version,Signature=e521358f7776c97df52e6b2891a8bc73026794a071b50c3323388c4e0df64804

x-acs-signature-nonce

String

否

签名唯一随机数。用于防止网络重放攻击，建议您每一次请求都使用不同的随机数。

d410180a5abf7fe235dd9b74aca91fc0

x-acs-date

String

是

按照ISO 8601标准表示的UTC时间，格式为yyyy-MM-ddTHH:mm:ssZ，例如2018-01-01T12:00:00Z。值为请求发出前15分钟内的时间。

2023-10-26T09:01:01Z

host

String

是

即 Endpoint。您可以查阅不同云产品的服务接入地址文档，查阅不同服务区域下的服务地址。

ecs.cn-shanghai.aliyuncs.com

x-acs-content-sha256

String

是

请求正文Hash摘要后再base-16编码的结果，与HashedRequestPayload一致。

e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

x-acs-security-token

String

STS认证必传

为调用Assumerole接口返回值中SecurityToken的值。

## 签名机制

为保证API的安全调用，在调用API时阿里云会对每个API请求通过签名（Signature）进行身份验证。无论使用HTTP还是HTTPS协议提交请求，都需要在请求中包含签名信息。本文指导您如何进行签名处理。

### **步骤一：构造规范化请求**

使用AK/SK方式进行签名与认证，首先需要规范请求内容，然后再进行签名。客户端与云服务API网关使用相同的请求规范，可以确保同一个HTTP请求的前后端得到相同的签名结果，从而完成身份校验。

构造规范化请求（CanonicalRequest）的伪代码如下：

```
CanonicalRequest =
  HTTPRequestMethod + '\n' +    //http请求方法，全大写
  CanonicalURI + '\n' +         //规范化URI
  CanonicalQueryString + '\n' + //规范化查询字符串
  CanonicalHeaders + '\n' +     //规范化消息头
  SignedHeaders + '\n' +        //已签名消息头
  HashedRequestPayload
```

-   #### **请求方法（HTTPRequestMethod）**
    
    即大写的HTTP方法名，如GET、POST。
    
-   #### **规范化URI（CanonicalURI）**
    
    即URL的资源路径部分经过编码得到，资源路径部分指URL中host与查询字符串之间的部分，包含host之后的`/`但不包含查询字符串前的`?`。用户发起请求时的URI应使用规范化URI，编码方式使用UTF-8字符集按照[RFC3986](http://tools.ietf.org/html/rfc3986)的规则对URI中的每一部分（即被`/`分割开的字符串）进行编码：
    
    -   字符A~Z、a~z、0~9以及字符`-`、`_`、`.`、`~`不编码。
        
    -   其他字符编码成`%`加字符对应ASCII码的16进制。示例：半角双引号（`"`）对应`%22`。
        
    -   空格（ ）编码成`%20`，而不是加号（`+`）、星号（`*`）替换为`%2A`、`%7E`替换为波浪号（`~`）。
        
        如果您使用的是Java标准库中的`java.net.URLEncoder`，可以先用标准库中`encode`编码，随后将编码后的字符中加号（`+`）替换为`%20`、星号（`*`）替换为`%2A`、`%7E`替换为波浪号（`~`），即可得到上述规则描述的编码字符串。
        
    
    **重要**
    
    RPC风格API使用正斜杠(`/`)作为CanonicalURI，
    
    ROA风格API该参数为元数据文件中`path`的值，例如/api/v1/clusters。
    
-   #### **规范化查询字符串（CanonicalQueryString）**
    
    构造方法如下：
    
    1.  将查询字符串中的参数按照参数名的字符代码升序排列，具有重复名称的参数应按值进行排序。
        
    2.  使用UTF-8字符集按照[RFC3986](http://tools.ietf.org/html/rfc3986)的规则对每个参数的参数名和参数值分别进行URI编码，具体规则与上一节中的CanonicalURI编码规则相同。
        
    3.  使用等号（`=`）连接编码后的请求参数名和参数值，对于没有值的参数使用空字符串。
        
    4.  按照步骤4中的顺序使用与号（`&`）连接编码后的请求参数。
        
    
    **重要**
    
    当请求的查询字符串为空时，使用空字符串作为规范化查询字符串。
    
-   #### **规范化请求头（CanonicalizedHeaders）**
    
    一个非标准HTTP头部信息。需要将请求中包含以`x-acs-`为前缀、`host`、`content-type`的参数信息，添加到规范化请求头中，构造方法如下：
    
    1.  将所有需要签名的参数的名称转换为小写。
        
    2.  将所有参数按照参数名称的字符顺序以升序排列。
        
    3.  将参数的值除去首尾空格。对于有多个值的参数，将多个值分别除去首尾空格后按值升序排列，然后用逗号（`,`）连接。
        
    4.  将步骤2、3的结果以英文冒号（`:`）连接，并在尾部添加换行符，组成一个规范化消息头（`CanonicalHeaderEntry`）。
        
    5.  如果没有需要签名的消息头，使用空字符串作为规范化消息头列表。
        
    
    **重要**
    
    除Authorization外的所有公共请求头，只要符合要求的参数都必须被加入签名。
    
-   #### **已签名消息头列表（SignedHeaders）**
    
    用于说明此次请求包含了哪些消息头参与签名，与CanonicalHeaders中包含的消息头是一一对应的，构造方法如下：
    
    -   将CanonicalHeaders中包含的请求头的名称转为小写。
        
    -   多个请求头名称（小写）按首字母升序排列并以英文分号（`;`）分隔，例如`content-type;host;x-acs-date`。
        
    -   伪代码如下：
        
        ```
        CanonicalHeaderEntry = Lowercase(HeaderName) + ':' + Trim(HeaderValue) + '\n'
        
        CanonicalHeaders = 
            CanonicalHeaderEntry0 + CanonicalHeaderEntry1 + ... + CanonicalHeaderEntryN
        ```
        
-   #### **HashedRequestPayload**
    
    当请求体（body）为空时，RequestPayload固定为空字符串，否则RequestPayload的值为请求体（body）对应的JSON字符串。再使用哈希函数对RequestPayload进行转换得到HashedRequestPayload，转换规则用伪代码可表示为`HashedRequestPayload = HexEncode(Hash(RequestPayload))`。
    
    -   Hash表示消息摘要函数，目前支持SHA256算法，例如，当签名协议使用ACS3-HMAC-SHA256时，应使用SHA256作为Hash函数。
        
    -   HexEncode表示以小写的十六进制的形式返回摘要的编码函数（即Base16编码）。
        
    
    表1：签名协议与签名算法、摘要函数的对应关系
    
    签名协议（SignatureAlgorithm）
    
    处理RequestPayload以及CanonicalRequest时使用的摘要函数（Hash）
    
    计算签名时实际使用的签名算法
    
    （SignatureMethod）
    
    ACS3-HMAC-SHA256
    
    SHA256
    
    HMAC-SHA256
    

### **步骤二：构造待签名字符串**

按照以下伪代码构造待签名字符串（stringToSign）：

```
StringToSign =
    SignatureAlgorithm + '\n' +
    HashedCanonicalRequest
```

-   SignatureAlgorithm
    
    签名协议，目前支持ACS3-HMAC-SHA256，不再支持基于MD5或SHA1的算法。
    
-   HashedCanonicalRequest
    
    规范化请求摘要串，计算方法伪代码如下：
    
    ```
    HashedCanonicalRequest = HexEncode(Hash(CanonicalRequest))
    ```
    

1.  使用哈希函数（Hash）对步骤一中得到的规范化请求（CanonicalRequest）进行摘要处理，具体使用的Hash函数取决于签名协议（SignatureAlgorithm），参见表1，例如，当签名协议为ACS3-HMAC-SHA256时，应使用SHA256作为Hash函数。
    
2.  将上一步得到的摘要结果以小写的十六进制形式编码。
    

### **步骤三：计算签名**

按照以下伪代码计算签名值（Signature）

```
Signature = HexEncode(SignatureMethod(Secret, StringToSign))
```

-   StringToSign：步骤二中构造的待签名字符串，UTF-8编码。
    
-   SignatureMethod：签名算法，具体使用的算法取决于签名协议（SignatureAlgorithm），其对应关系如表1。
    
-   Secret：用户的签名密钥，为二进制数据。
    
-   HexEncode：以小写的十六进制的形式返回摘要的编码函数（即Base16编码）。
    

### **步骤四：将签名添加到请求中**

计算完签名后，构造Authorization请求头，格式为：`Authorization:<SignatureAlgorithm>Credential=<AccessKeyId>,SignedHeaders=<SignedHeaders>,Signature=<Signature>`

## **接口签名示例**

运行Java示例，需要您在pom.xml中添加以下Maven依赖。

```
<dependency>
    <groupId>org.apache.httpcomponents</groupId>
    <artifactId>httpclient</artifactId>
    <version>4.5.14</version>
</dependency>
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>fastjson</artifactId>
    <version>2.0.60</version>
</dependency>
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.18.36</version>
    <scope>provided</scope>
</dependency>
```

```
package org.example.service;

import com.alibaba.fastjson.JSONObject;

import lombok.extern.slf4j.Slf4j;
import org.apache.http.client.methods.*;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import javax.xml.bind.DatatypeConverter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URISyntaxException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.text.SimpleDateFormat;
import java.util.*;

@Slf4j
public class RoaDemo {

    /**
     * 日期格式化工具，用于将日期时间字符串格式化为"yyyy-MM-dd'T'HH:mm:ss'Z'"的格式。
     */
    private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");

    private static class Request {
        // HTTP Method
        private final String httpMethod;
        // 请求路径，当资源路径为空时，使用正斜杠(/)作为CanonicalURI
        private final String canonicalUri;
        // endpoint
        private final String host;
        // API name
        private final String xAcsAction;
        // API version
        private final String xAcsVersion;
        // headers
        TreeMap<String, Object> headers = new TreeMap<>();
        // 调用API所需要的参数，参数位置在body。Json字符串
        String body;
        // 调用API所需要的参数，参数位置在query，参数按照参数名的字符代码升序排列
        TreeMap<String, Object> queryParam = new TreeMap<>();

        public Request(String httpMethod, String canonicalUri, String host, String xAcsAction, String xAcsVersion) {
            this.httpMethod = httpMethod;
            this.canonicalUri = canonicalUri;
            this.host = host;
            this.xAcsAction = xAcsAction;
            this.xAcsVersion = xAcsVersion;
            initBuilder();
        }

        // init headers
        private void initBuilder() {
            headers.put("host", host);
            headers.put("x-acs-action", xAcsAction);
            headers.put("x-acs-version", xAcsVersion);
            SDF.setTimeZone(new SimpleTimeZone(0, "GMT")); // 设置日期格式化时区为GMT
            headers.put("x-acs-date", SDF.format(new Date()));
            headers.put("x-acs-signature-nonce", UUID.randomUUID().toString());
        }
    }

    /**
     * 这里通过环境变量获取Access Key ID和Access Key Secret，
     */
    private final static String ACCESS_KEY_ID = "YOUR_ACCESS_KEY_ID";
    private final static String ACCESS_KEY_SECRET = "YOUR_ACCESS_KEY_SECRET";

    /**
     * 签名协议
     */
    private static final String ALGORITHM = "ACS3-HMAC-SHA256";

    public static void main(String[] args) throws Exception {

        String workspaceId = "YOUR_WORKSPACEID";
        String appId = "YOUR_APPID";
        // RPC接口请求
        String httpMethod = "POST"; // 请求方式
        String canonicalUri = "/" + percentCode(workspaceId) + "/ccai/app/" + percentCode(appId) + "/completion";
        String host = "contactcenterai.cn-shanghai.aliyuncs.com";  // endpoint
        String xAcsAction = "RunCompletion";  // API名称
        String xAcsVersion = "2024-06-03"; // API版本号
        Request request = new Request(httpMethod, canonicalUri, host, xAcsAction, xAcsVersion);

        // 调用API所需要的参数，参数按照参数名的字符代码升序排列，具有重复名称的参数应按值进行排序。
        request.queryParam.put("RegionId", "cn-shanghai");
        request.headers.put("content-type", "application/json; charset=utf-8");

        //请求体
        setBody(request);
        // 签名过程
        getAuthorization(request);
        // 调用API
        callApi(request);

    }

    private static void setBody(Request requestIn) {
        Map<String, Object> bodyMap = buildRunCompletionRequestMap();
        requestIn.body = JSONObject.toJSONString(bodyMap);
    }

    private static Map<String, Object> buildRunCompletionRequestMap() {

        // 对话内容
        List<Map<String, String>> sentenceDTOList = new ArrayList<>();
        Map<String, String> sentenceDTO1 = new HashMap<>();
        sentenceDTO1.put("ChatId", "chat_1");
        sentenceDTO1.put("Role", "user");
        sentenceDTO1.put("Text", "我要办理信用卡");
        Map<String, String> sentenceDTO2 = new HashMap<>();
        sentenceDTO2.put("ChatId", "chat_2");
        sentenceDTO2.put("Role", "agent");
        sentenceDTO2.put("Text", "好的，稍等10分钟，我现在为您办理，请先提供相关的个人信息");

        sentenceDTOList.add(sentenceDTO1);
        sentenceDTOList.add(sentenceDTO2);

        Map<String, Object> dialogue = new HashMap<>();
        dialogue.put("SessionId", "session_01_asdfasdfasd");
        dialogue.put("Sentences", sentenceDTOList);

        // 信息抽取的字段（非信息抽取场景可以不填）
        List<Map<String, String>> fieldList = new ArrayList<>();
        Map<String, String> field1 = new HashMap<>();
        field1.put("Name", "姓名");
        field1.put("Desc", "用户的名称");
        Map<String, String> field2 = new HashMap<>();
        field2.put("Name", "信用卡号");
        field2.put("Desc", "用户的信用卡号");
        fieldList.add(field1);
        fieldList.add(field2);
        
        //templateIds需填写真实的模板ID，47L为示例ID
        Map<String, Object> body = new java.util.HashMap<>();
        body.put("Dialogue", dialogue);
        //body.put("Dimensions", new java.util.ArrayList<>());
        body.put("Fields", fieldList);
        body.put("ModelCode", "tyxmTurbo");
        body.put("Stream", false);
        body.put("TemplateIds", Arrays.asList(47L));

        return body;
    }

    private static void callApi(Request request) throws Exception {
        try {
            // 通过HttpClient发送请求
            String url = "https://" + request.host + request.canonicalUri;

            URIBuilder uriBuilder = new URIBuilder(url);
            // 添加请求参数
            for (Map.Entry<String, Object> entry : request.queryParam.entrySet()) {
                uriBuilder.addParameter(entry.getKey(), String.valueOf(entry.getValue()));
            }
            HttpRequestBase httpRequest;
            switch (request.httpMethod) {
                case "GET":
                    httpRequest = new HttpGet(uriBuilder.build());
                    break;
                case "POST":
                    HttpPost httpPost = new HttpPost(uriBuilder.build());
                    if (request.body != null) {
                        StringEntity postEntity = new StringEntity(request.body, StandardCharsets.UTF_8);
                        httpPost.setEntity(postEntity);
                    }
                    httpRequest = httpPost;
                    break;
                case "DELETE":
                    httpRequest = new HttpDelete(uriBuilder.build());
                    break;
                case "PUT":
                    HttpPut httpPut = new HttpPut(uriBuilder.build());
                    if (request.body != null) {
                        StringEntity putEntity = new StringEntity(request.body);
                        httpPut.setEntity(putEntity);
                    }
                    httpRequest = httpPut;
                    break;
                default:
                    System.out.println("Unsupported HTTP method: " + request.body);
                    throw new IllegalArgumentException("Unsupported HTTP method");
            }

            // 添加http请求头
            for (Map.Entry<String, Object> entry : request.headers.entrySet()) {
                httpRequest.addHeader(entry.getKey(), String.valueOf(entry.getValue()));
            }
            System.out.println("curl  "+toCurlCommand(httpRequest));

            // 发送请求
            try (CloseableHttpClient httpClient = HttpClients.createDefault(); CloseableHttpResponse response = httpClient.execute(httpRequest)) {
                String result = EntityUtils.toString(response.getEntity(), "UTF-8");
                System.out.println(result);
            } catch (IOException e) {
                // 异常处理
                System.out.println("Failed to send request");
                e.printStackTrace();
            }
        } catch (URISyntaxException e) {
            // 异常处理
            System.out.println("Invalid URI syntax");
            e.printStackTrace();
        } catch (UnsupportedEncodingException e) {
            // 异常处理
            System.out.println("UnsupportedEncodingException");
            e.printStackTrace();
        }
    }

    public static String toCurlCommand(HttpRequestBase request) throws Exception{
        StringBuilder curlCommand = new StringBuilder("curl -X ");
        curlCommand.append(request.getMethod()); // GET, POST, etc.

        // Add headers
        for (org.apache.http.Header header : request.getAllHeaders()) {
            curlCommand.append(" -H '");
            curlCommand.append(header.getName());
            curlCommand.append(": ");
            curlCommand.append(header.getValue());
            curlCommand.append("'");
        }

        // Add body if it's a POST or PUT request
        if (request instanceof HttpPost || request instanceof HttpPut) {
            // TODO: Handle entity
             curlCommand.append(" -d '");
             curlCommand.append(EntityUtils.toString(((HttpEntityEnclosingRequestBase) request).getEntity()));
             curlCommand.append("'");
        }

        // Add URL
        curlCommand.append(" '");
        curlCommand.append(request.getURI().toString());
        curlCommand.append("'");

        return curlCommand.toString();
    }

    /**
     * 该方法用于根据传入的HTTP请求方法、规范化的URI、查询参数等，计算并生成授权信息。
     */
    private static void getAuthorization(Request request) {
        try {
            // 步骤 1：拼接规范请求串
            // 请求参数，当请求的查询字符串为空时，使用空字符串作为规范化查询字符串
            StringBuilder canonicalQueryString = new StringBuilder();
            request.queryParam.entrySet().stream().map(entry -> percentCode(entry.getKey()) + "=" + percentCode(String.valueOf(entry.getValue()))).forEachOrdered(queryPart -> {
                // 如果canonicalQueryString已经不是空的，则在新查询参数前添加"&"
                if (canonicalQueryString.length() > 0) {
                    canonicalQueryString.append("&");
                }
                canonicalQueryString.append(queryPart);
            });

            // 请求体，当请求正文为空时，比如GET请求，RequestPayload固定为空字符串
            String requestPayload = "";
            if (request.body != null) {
                requestPayload = request.body;
            }

            // 计算请求体的哈希值
            String hashedRequestPayload = sha256Hex(requestPayload);
            request.headers.put("x-acs-content-sha256", hashedRequestPayload);
            // 构造请求头，多个规范化消息头，按照消息头名称（小写）的字符代码顺序以升序排列后拼接在一起
            StringBuilder canonicalHeaders = new StringBuilder();
            // 已签名消息头列表，多个请求头名称（小写）按首字母升序排列并以英文分号（;）分隔
            StringBuilder signedHeadersSb = new StringBuilder();
            request.headers.entrySet().stream().filter(entry -> entry.getKey().toLowerCase().startsWith("x-acs-") || entry.getKey().equalsIgnoreCase("host") || entry.getKey().equalsIgnoreCase("content-type")).sorted(Map.Entry.comparingByKey()).forEach(entry -> {
                String lowerKey = entry.getKey().toLowerCase();
                String value = String.valueOf(entry.getValue()).trim();
                canonicalHeaders.append(lowerKey).append(":").append(value).append("\n");
                signedHeadersSb.append(lowerKey).append(";");
            });
            String signedHeaders = signedHeadersSb.substring(0, signedHeadersSb.length() - 1);
            String canonicalRequest = request.httpMethod + "\n" + request.canonicalUri + "\n" + canonicalQueryString + "\n" + canonicalHeaders + "\n" + signedHeaders + "\n" + hashedRequestPayload;
            System.out.println("canonicalRequest=========>\n" + canonicalRequest);

            // 步骤 2：拼接待签名字符串
            String hashedCanonicalRequest = sha256Hex(canonicalRequest); // 计算规范化请求的哈希值
            String stringToSign = ALGORITHM + "\n" + hashedCanonicalRequest;
            System.out.println("stringToSign=========>\n" + stringToSign);

            // 步骤 3：计算签名
            String signature = DatatypeConverter.printHexBinary(hmac256(ACCESS_KEY_SECRET.getBytes(StandardCharsets.UTF_8), stringToSign)).toLowerCase();
            System.out.println("signature=========>" + signature);

            // 步骤 4：拼接 Authorization
            String authorization = ALGORITHM + " " + "Credential=" + ACCESS_KEY_ID + ",SignedHeaders=" + signedHeaders + ",Signature=" + signature;
            System.out.println("authorization=========>" + authorization);
            request.headers.put("Authorization", authorization);
        } catch (Exception e) {
            // 异常处理
            System.out.println("Failed to get authorization");
            e.printStackTrace();
        }
    }

    /**
     * 使用HmacSHA256算法生成消息认证码（MAC）。
     *
     * @param key 密钥，用于生成MAC的密钥，必须保密。
     * @param str 需要进行MAC认证的消息。
     * @return 返回使用HmacSHA256算法计算出的消息认证码。
     * @throws Exception 如果初始化MAC或计算MAC过程中遇到错误，则抛出异常。
     */
    public static byte[] hmac256(byte[] key, String str) throws Exception {
        // 实例化HmacSHA256消息认证码生成器
        Mac mac = Mac.getInstance("HmacSHA256");
        // 创建密钥规范，用于初始化MAC生成器
        SecretKeySpec secretKeySpec = new SecretKeySpec(key, mac.getAlgorithm());
        // 初始化MAC生成器
        mac.init(secretKeySpec);
        // 计算消息认证码并返回
        return mac.doFinal(str.getBytes(StandardCharsets.UTF_8));
    }

    /**
     * 使用SHA-256算法计算字符串的哈希值并以十六进制字符串形式返回。
     *
     * @param str 需要进行SHA-256哈希计算的字符串。
     * @return 计算结果为小写十六进制字符串。
     * @throws Exception 如果在获取SHA-256消息摘要实例时发生错误。
     */
    public static String sha256Hex(String str) throws Exception {
        //// 获取SHA-256消息摘要实例
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        //// 计算字符串s的SHA-256哈希值
        byte[] d = md.digest(str.getBytes(StandardCharsets.UTF_8));
        //// 将哈希值转换为小写十六进制字符串并返回
        return DatatypeConverter.printHexBinary(d).toLowerCase();
    }

    /**
     * 对指定的字符串进行URL编码。
     * 使用UTF-8编码字符集对字符串进行编码，并对特定的字符进行替换，以符合URL编码规范。
     *
     * @param str 需要进行URL编码的字符串。
     * @return 编码后的字符串。其中，加号"+"被替换为"%20"，星号"*"被替换为"%2A"，波浪号"%7E"被替换为"~"。
     */
    public static String percentCode(String str) {
        if (str == null) {
            throw new IllegalArgumentException("输入字符串不可为null");
        }
        try {
            return URLEncoder.encode(str, "UTF-8").replace("+", "%20").replace("*", "%2A").replace("%7E", "~");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException("UTF-8编码不被支持", e);
        }
    }

}
```

## 签名失败常见报错

Code

Message

解决方案

SignatureDoesNotMatch

Specified signature does not match our calculation.

在签名过程中，您可能遗漏了对参数进行升序排序，也可能是多加了空格。请您仔细阅读签名机制的讲解，可以根据提供的固定参数示例验证您的签名过程是否正确。

IncompleteSignature

The request signature does not conform to Aliyun standards.
