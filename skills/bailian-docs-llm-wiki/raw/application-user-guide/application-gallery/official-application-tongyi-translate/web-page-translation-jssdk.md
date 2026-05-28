# 网页翻译JSSDK

## **功能描述**

基于翻译大模型的页面翻译插件，提供页面翻译功能。您可以通过JSSDK，一键完成网站的多语言改造。

## **技术流程**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3845767571/p997475.png)

## 接入JSSDK

#### **步骤一：在HTML插入脚本**

```
<html>
  <head></head>
  <body>
    <!-- 在文档的末尾插入翻译脚本 -->
    <script src="https://g.alicdn.com/translate-js-sdk/translate-js-sdk-stable/2.0.6/light.js"></script>
  </body>
</html>
```

#### **步骤二：配置JSSDK**

```
interface ITokenResponseData {
  code: 200;
  data: {
    url: string,
    host: string,
    method: "POST",
    headers: {
      "host": string,
      "x-acs-action": "BatchTranslateForHtml",
      "x-acs-version": string,
      "x-acs-date": string;
      "x-acs-signature-nonce": string;
      "content-type": "application/json",
      "x-acs-content-sha256": string;
      Authorization: string;
    };
    body: string;
  };
}

interface ITokenRequestData {
  sourceLanguage: string;
  targetLanguage: string;
  streaming: false,
  text: {[index: number]: string}
  scene: 'mt-turbo',
  fallbackTimeoutMs: number;
}

interface ISetupConfig {
  getToken: (data: ITokenRequestData) => Promise<ITokenResponseData>;
}

// 只用初始化一次，不需要每次翻译都初始化
__AliTranslate.setup({
  getToken: async (data) => {
    const res = await fetch('YOUR_GET_TOEKN_URL', { method: 'post', body: JSON.stringify(data) });
    return (await res.json()).data;
  }
});
```

#### **步骤三：调用页面翻译**

**仅展示译文**

```
interface IPageTranslate {
  srcLanguage?: string; // 默认语种，默认为auto
  tgtLanguage?: string; // 目标语种，默认为en
  lazyload?: boolean; // 是否只翻译可视区域，默认为false
  lazyOffset?: number; // 可视区域的扩展
  target?: HTMLElement; // 要翻译的目标区域，默认为body
  except?: string; // 要排除翻译的区域，默认为空
}

const instance = __AliTranslate.pageTranslate({
  // 详细参数见PageTranslate参数
  lazyload: true,
  lazyOffset: 500
});
```

**双语对照翻译**

```
interface IParagraphTranslate {
  srcLanguage?: string; // 默认语种，默认为auto
  tgtLanguage?: string; // 目标语种，默认为en
  target?: HTMLElement; // 要翻译的目标区域，默认为body
  dynamic?: boolean; // 是否支持动态翻译，默认为false
}

const instance = __AliTranslate.paragraphTranslate({
  // 详细参数见ParagrapthTranslate参数
  srcLanguage: 'zh',
  tgtLanguage: 'en'
});
```

#### **步骤四：取消翻译**

```
// 触发取消翻译后，页面将回到原始文案
instance.destroy();
```

### **PageTranslate参数**

参数

说明

类型

默认值

srcLanguage

默认的原语种

String

auto（会根据页面文案自动选择）

tgtLanguage

默认的目标语种

String

en

lazyload

是否只翻译可视区域

Boolean

false

lazyOffset

当lazyload为true时，可视区域扩展

Number

\-1 (-1表示不做任何offset)

target

要翻译的目标区域

HTMLElement | HTMLElement\[\]

body

except

不翻译的区域

Selector(String)

空

### **ParagraphTranslate参数**

参数

说明

类型

默认值

srcLanguage

默认的原语种

String

auto（会根据页面文案自动选择）

tgtLanguage

默认的目标语种

String

en

target

要翻译的目标区域

HTMLElement | HTMLElement\[\]

body

dynamic

是否动态翻译。如果开启，如果页面发生变化，会自动翻译。如果不开启，则只翻译一次

Boolean

false

lazyload

是否只翻译可视区域

Boolean

false

lazyOffset

当lazyload为true时，可视区域扩展

Number

300

## **获取Token服务**

使用阿里云SDK的[V3版本请求体&签名机制](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)进行请求签名

Node.js

```
// 通过calculateSignature方法生成签名
import * as crypto from 'crypto';

export interface SignatureRequest {
  httpMethod: string;
  canonicalUri: string;
  host: string;
  xAcsAction: string;
  xAcsVersion: string;
  headers: Record<string, string>;
  body: any;
  queryParam: Record<string, any>;
}

export interface BatchTranslateRequest {
  scene: string;
  sourceLanguage: string;
  streaming: boolean;
  targetLanguage: string;
  text: { [key: string]: string };
}

export class Request implements SignatureRequest {
  httpMethod: string;
  canonicalUri: string;
  host: string;
  xAcsAction: string;
  xAcsVersion: string;
  headers: Record<string, string>;
  body: any;
  queryParam: Record<string, any>;

  constructor(httpMethod: string, canonicalUri: string, host: string, xAcsAction: string, xAcsVersion: string) {
    this.httpMethod = httpMethod;
    this.canonicalUri = canonicalUri || '/';
    this.host = host;
    this.xAcsAction = xAcsAction;
    this.xAcsVersion = xAcsVersion;
    this.headers = {};
    this.body = null;
    this.queryParam = {};
    this.initHeader();
  }

  private initHeader() {
    const date = new Date();
    this.headers = {
      'host': this.host,
      'x-acs-action': this.xAcsAction,
      'x-acs-version': this.xAcsVersion,
      'x-acs-date': date.toISOString().replace(/\..+/, 'Z'),
      'x-acs-signature-nonce': crypto.randomBytes(16).toString('hex')
    }
  }
}

const ALGORITHM = 'ACS3-HMAC-SHA256';
const accessKeyId = process.env.ACCESS_KEY_ID; // 这里填入阿里云的AK
const accessKeySecret = process.env.ACCESS_KEY_SECRET; // 这里填入阿里云的SK
const workspaceId = process.env.WORKSPACE_ID; // 这里填入百炼的WorkspaceId
const encoder = new TextEncoder();
const httpMethod = 'POST';
const canonicalUri = '/anytrans/translate/batchForHtml';
const xAcsAction = 'BatchTranslateForHtml';
const xAcsVersion = '2025-07-07';
const host = 'anytrans.cn-beijing.aliyuncs.com';

export interface SignedRequest {
  url: string;
  method: string;
  host: string;
  headers: Record<string, string>;
  body?: any; // 可能是 Uint8Array 或 Base64 字符串
}

export function getAuthorization(signRequest: SignatureRequest): SignedRequest {
  try {
    const newQueryParam: Record<string, any> = {};
    processObject(newQueryParam, "", signRequest.queryParam);
    signRequest.queryParam = newQueryParam;

    // 步骤 1：拼接规范请求串
    const canonicalQueryString = Object.entries(signRequest.queryParam)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([key, value]) => `${percentCode(key)}=${percentCode(value)}`)
      .join('&');

    // 请求体，当请求正文为空时，比如GET请求，RequestPayload固定为空字符串
    const requestPayload = signRequest.body || encoder.encode('');
    const hashedRequestPayload = sha256Hex(requestPayload);
    signRequest.headers['x-acs-content-sha256'] = hashedRequestPayload;

    // 将所有key都转换为小写
    signRequest.headers = Object.fromEntries(
      Object.entries(signRequest.headers).map(([key, value]) => [key.toLowerCase(), value])
    );

    const sortedKeys = Object.keys(signRequest.headers)
      .filter(key => key.startsWith('x-acs-') || key === 'host' || key === 'content-type')
      .sort();

    // 已签名消息头列表，多个请求头名称（小写）按首字母升序排列并以英文分号（;）分隔
    const signedHeaders = sortedKeys.join(";")

    // 构造请求头，多个规范化消息头，按照消息头名称（小写）的字符代码顺序以升序排列后拼接在一起
    const canonicalHeaders = sortedKeys.map(key => `${key}:${signRequest.headers[key]}`).join('\n') + '\n';

    const canonicalRequest = [
      signRequest.httpMethod,
      signRequest.canonicalUri,
      canonicalQueryString,
      canonicalHeaders,
      signedHeaders,
      hashedRequestPayload
    ].join('\n');
    console.log('canonicalRequest=========>\n', canonicalRequest);

    // 步骤 2：拼接待签名字符串
    const hashedCanonicalRequest = sha256Hex(encoder.encode(canonicalRequest));
    const stringToSign = `${ALGORITHM}\n${hashedCanonicalRequest}`;
    console.log('stringToSign=========>', stringToSign);

    // 步骤 3：计算签名
    const signature = hmac256(accessKeySecret!, stringToSign);
    console.log('signature=========>', signature);

    // 步骤 4：拼接 Authorization
    const authorization = `${ALGORITHM} Credential=${accessKeyId},SignedHeaders=${signedHeaders},Signature=${signature}`;
    console.log('authorization=========>', authorization);
    signRequest.headers['Authorization'] = authorization;

    // 构建完整的URL
    let url = `https://${signRequest.host}${signRequest.canonicalUri}`;
    if (signRequest.queryParam && Object.keys(signRequest.queryParam).length > 0) {
      const query = new URLSearchParams(signRequest.queryParam);
      url += '?' + query.toString();
    }

    return {
      url,
      host: signRequest.host,
      method: signRequest.httpMethod.toUpperCase(),
      headers: signRequest.headers,
      body: signRequest.body
    };
  } catch (error) {
    console.error('Failed to get authorization');
    console.error(error);
    throw error;
  }
}

function percentCode(str: string): string {
  return encodeURIComponent(str)
    .replace(/\+/g, '%20')
    .replace(/\*/g, '%2A')
    .replace(/~/g, '%7E');
}

function hmac256(key: string, data: string): string {
  const hmac = crypto.createHmac('sha256', key);
  hmac.update(data, 'utf8');
  return hmac.digest('hex').toLowerCase();
}

function sha256Hex(bytes: any): string {
  const hash = crypto.createHash('sha256');
  const digest = hash.update(bytes).digest('hex');
  return digest.toLowerCase();
}

function processObject(map: Record<string, any>, key: string, value: any): void {
  // 如果值为空，则无需进一步处理
  if (value === null) {
    return;
  }
  if (key === null) {
    key = "";
  }

  // 当值为Array类型时，遍历Array中的每个元素，并递归处理
  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      processObject(map, `${key}.${index + 1}`, item);
    });
  } else if (typeof value === 'object' && value !== null) {
    // 当值为Object类型时，遍历Object中的每个键值对，并递归处理
    Object.entries(value).forEach(([subKey, subValue]) => {
      processObject(map, `${key}.${subKey}`, subValue);
    });
  } else {
    // 对于以"."开头的键，移除开头的"."以保持键的连续性
    if (key.startsWith('.')) {
      key = key.slice(1);
    }
    map[key] = String(value);
  }
}

export function formDataToString(formData: Record<string, any>): string {
  const tmp: Record<string, any> = {};
  processObject(tmp, "", formData);
  let queryString = '';
  for (let [key, value] of Object.entries(tmp)) {
    if (queryString !== '') {
      queryString += '&';
    }
    queryString += encodeURIComponent(key) + '=' + encodeURIComponent(value);
  }
  return queryString;
}

// 固定变量签名计算方法
export interface FixedSignatureResult {
  httpMethod: string;
  canonicalUri: string;
  host: string;
  xAcsAction: string;
  xAcsVersion: string;
  signature: string;
  date: string;
  nonce: string;
  workspaceId: string;
  authorization: string;
}

export function calculateSignature(req: BatchTranslateRequest): SignedRequest {
  // 创建请求实例
  const signRequest = new Request(httpMethod, canonicalUri, host, xAcsAction, xAcsVersion);

  // 设置查询参数
  signRequest.queryParam = {
    RegionId: 'cn-beijing',
  };

  // 创建 body 的 Uint8Array
  const bodyUint8Array = encoder.encode(JSON.stringify({
    ...req,
    workspaceId,
  }));

  // 用于签名计算的 body
  signRequest.body = bodyUint8Array;

  signRequest.headers['content-type'] = 'application/json';

  // 获取签名
  const result = getAuthorization(signRequest);

  // 将 body 转换为 Base64 字符串用于传输
  const bodyBase64 = Buffer.from(bodyUint8Array).toString('base64');

  return {
    ...result,
    body: bodyBase64 // 返回 Base64 字符串而不是 Uint8Array
  };
}
```

Java

```
// 通过calculateSignature方法生成签名
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.time.Instant;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.net.URLEncoder;
import java.io.UnsupportedEncodingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.JsonProcessingException;

/**
 * 签名请求接口
 */
interface SignatureRequest {
    String getHttpMethod();
    String getCanonicalUri();
    String getHost();
    String getXAcsAction();
    String getXAcsVersion();
    Map<String, String> getHeaders();
    byte[] getBody();
    Map<String, Object> getQueryParam();
    
    void setHeaders(Map<String, String> headers);
    void setBody(byte[] body);
    void setQueryParam(Map<String, Object> queryParam);
}

/**
 * 批量翻译请求数据类
 */
class BatchTranslateRequest {
    private String scene;
    private String sourceLanguage;
    private boolean streaming;
    private String targetLanguage;
    private Map<String, String> text;
    
    // 构造函数
    public BatchTranslateRequest() {}
    
    public BatchTranslateRequest(String scene, 
                               String sourceLanguage, boolean streaming, 
                               String targetLanguage, Map<String, String> text) {
        this.scene = scene;
        this.sourceLanguage = sourceLanguage;
        this.streaming = streaming;
        this.targetLanguage = targetLanguage;
        this.text = text;
    }
    
    // Getters and Setters
    public String getScene() { return scene; }
    public void setScene(String scene) { this.scene = scene; }
    
    public String getSourceLanguage() { return sourceLanguage; }
    public void setSourceLanguage(String sourceLanguage) { this.sourceLanguage = sourceLanguage; }
    
    public boolean isStreaming() { return streaming; }
    public void setStreaming(boolean streaming) { this.streaming = streaming; }
    
    public String getTargetLanguage() { return targetLanguage; }
    public void setTargetLanguage(String targetLanguage) { this.targetLanguage = targetLanguage; }
    
    public Map<String, String> getText() { return text; }
    public void setText(Map<String, String> text) { this.text = text; }
}

/**
 * 请求实现类
 */
class Request implements SignatureRequest {
    private String httpMethod;
    private String canonicalUri;
    private String host;
    private String xAcsAction;
    private String xAcsVersion;
    private Map<String, String> headers;
    private byte[] body;
    private Map<String, Object> queryParam;
    
    public Request(String httpMethod, String canonicalUri, String host, 
                  String xAcsAction, String xAcsVersion) {
        this.httpMethod = httpMethod;
        this.canonicalUri = canonicalUri != null ? canonicalUri : "/";
        this.host = host;
        this.xAcsAction = xAcsAction;
        this.xAcsVersion = xAcsVersion;
        this.headers = new HashMap<>();
        this.body = null;
        this.queryParam = new HashMap<>();
        initHeader();
    }
    
    private void initHeader() {
        Instant now = Instant.now();
        String date = DateTimeFormatter.ISO_INSTANT.format(now);
        String nonce = generateRandomHex(16);
        
        this.headers.put("host", this.host);
        this.headers.put("x-acs-action", this.xAcsAction);
        this.headers.put("x-acs-version", this.xAcsVersion);
        this.headers.put("x-acs-date", date);
        this.headers.put("x-acs-signature-nonce", nonce);
    }
    
    private String generateRandomHex(int length) {
        SecureRandom random = new SecureRandom();
        byte[] bytes = new byte[length];
        random.nextBytes(bytes);
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
    
    // Getters
    @Override
    public String getHttpMethod() { return httpMethod; }
    @Override
    public String getCanonicalUri() { return canonicalUri; }
    @Override
    public String getHost() { return host; }
    @Override
    public String getXAcsAction() { return xAcsAction; }
    @Override
    public String getXAcsVersion() { return xAcsVersion; }
    @Override
    public Map<String, String> getHeaders() { return headers; }
    @Override
    public byte[] getBody() { return body; }
    @Override
    public Map<String, Object> getQueryParam() { return queryParam; }
    
    // Setters
    @Override
    public void setHeaders(Map<String, String> headers) { this.headers = headers; }
    @Override
    public void setBody(byte[] body) { this.body = body; }
    @Override
    public void setQueryParam(Map<String, Object> queryParam) { this.queryParam = queryParam; }
}

/**
 * 签名后的请求结果
 */
class SignedRequest {
    private String url;
    private String method;
    private String host;
    private Map<String, String> headers;
    private String body; // Base64 字符串
    
    public SignedRequest(String url, String method, String host, 
                        Map<String, String> headers, String body) {
        this.url = url;
        this.method = method;
        this.host = host;
        this.headers = headers;
        this.body = body;
    }
    
    // Getters
    public String getUrl() { return url; }
    public String getMethod() { return method; }
    public String getHost() { return host; }
    public Map<String, String> getHeaders() { return headers; }
    public String getBody() { return body; }
}

/**
 * 固定签名结果接口
 */
interface FixedSignatureResult {
    String getHttpMethod();
    String getCanonicalUri();
    String getHost();
    String getXAcsAction();
    String getXAcsVersion();
    String getSignature();
    String getDate();
    String getNonce();
    String getWorkspaceId();
    String getAuthorization();
}

/**
 * Node签名计算主类
 */
public class NodeSignature {
    private static final String ALGORITHM = "ACS3-HMAC-SHA256";
    private static final String ACCESS_KEY_ID = System.getenv("ACCESS_KEY_ID"); // 这里填入阿里云的AK
    private static final String ACCESS_KEY_SECRET = System.getenv("ACCESS_KEY_SECRET"); // 这里填入阿里云的SK
    private static final String WORKSPACE_ID = System.getenv("WORKSPACE_ID"); // 这里填入百炼的WorkspaceId
    
    private static final String HTTP_METHOD = "POST";
    private static final String CANONICAL_URI = "/anytrans/translate/batchForHtml";
    private static final String X_ACS_ACTION = "BatchTranslateForHtml";
    private static final String X_ACS_VERSION = "2025-07-07";
    private static final String HOST = "anytrans.cn-beijing.aliyuncs.com";
    
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    /**
     * 获取授权信息
     */
    public static SignedRequest getAuthorization(SignatureRequest signRequest) {
        try {
            Map<String, Object> newQueryParam = new HashMap<>();
            processObject(newQueryParam, "", signRequest.getQueryParam());
            signRequest.setQueryParam(newQueryParam);
            
            // 步骤 1：拼接规范请求串
            String canonicalQueryString = signRequest.getQueryParam().entrySet().stream()
                .sorted(Map.Entry.comparingByKey())
                .map(entry -> percentCode(entry.getKey()) + "=" + percentCode(String.valueOf(entry.getValue())))
                .collect(Collectors.joining("&"));
            
            // 请求体，当请求正文为空时，比如GET请求，RequestPayload固定为空字符串
            byte[] requestPayload = signRequest.getBody() != null ? signRequest.getBody() : new byte[0];
            String hashedRequestPayload = sha256Hex(requestPayload);
            signRequest.getHeaders().put("x-acs-content-sha256", hashedRequestPayload);
            
            // 将所有key都转换为小写
            Map<String, String> lowerCaseHeaders = signRequest.getHeaders().entrySet().stream()
                .collect(Collectors.toMap(
                    entry -> entry.getKey().toLowerCase(),
                    Map.Entry::getValue
                ));
            signRequest.setHeaders(lowerCaseHeaders);
            
            List<String> sortedKeys = lowerCaseHeaders.keySet().stream()
                .filter(key -> key.startsWith("x-acs-") || key.equals("host") || key.equals("content-type"))
                .sorted()
                .collect(Collectors.toList());
            
            // 已签名消息头列表，多个请求头名称（小写）按首字母升序排列并以英文分号（;）分隔
            String signedHeaders = String.join(";", sortedKeys);
            
            // 构造请求头，多个规范化消息头，按照消息头名称（小写）的字符代码顺序以升序排列后拼接在一起
            String canonicalHeaders = sortedKeys.stream()
                .map(key -> key + ":" + lowerCaseHeaders.get(key))
                .collect(Collectors.joining("\n")) + "\n";
            
            String canonicalRequest = String.join("\n", Arrays.asList(
                signRequest.getHttpMethod(),
                signRequest.getCanonicalUri(),
                canonicalQueryString,
                canonicalHeaders,
                signedHeaders,
                hashedRequestPayload
            ));
            System.out.println("canonicalRequest=========>\n" + canonicalRequest);
            
            // 步骤 2：拼接待签名字符串
            String hashedCanonicalRequest = sha256Hex(canonicalRequest.getBytes(StandardCharsets.UTF_8));
            String stringToSign = ALGORITHM + "\n" + hashedCanonicalRequest;
            System.out.println("stringToSign=========>" + stringToSign);
            
            // 步骤 3：计算签名
            String signature = hmac256(ACCESS_KEY_SECRET, stringToSign);
            System.out.println("signature=========>" + signature);
            
            // 步骤 4：拼接 Authorization
            String authorization = String.format("%s Credential=%s,SignedHeaders=%s,Signature=%s",
                ALGORITHM, ACCESS_KEY_ID, signedHeaders, signature);
            System.out.println("authorization=========>" + authorization);
            lowerCaseHeaders.put("authorization", authorization);
            
            // 构建完整的URL
            String url = "https://" + signRequest.getHost() + signRequest.getCanonicalUri();
            if (signRequest.getQueryParam() != null && !signRequest.getQueryParam().isEmpty()) {
                String query = signRequest.getQueryParam().entrySet().stream()
                    .map(entry -> {
                        try {
                            return URLEncoder.encode(entry.getKey(), "UTF-8") + "=" + 
                                   URLEncoder.encode(String.valueOf(entry.getValue()), "UTF-8");
                        } catch (UnsupportedEncodingException e) {
                            throw new RuntimeException(e);
                        }
                    })
                    .collect(Collectors.joining("&"));
                url += "?" + query;
            }
            
            String bodyString = signRequest.getBody() != null ? 
                Base64.getEncoder().encodeToString(signRequest.getBody()) : null;
            
            return new SignedRequest(url, signRequest.getHttpMethod().toUpperCase(), 
                                   signRequest.getHost(), lowerCaseHeaders, bodyString);
                                   
        } catch (Exception error) {
            System.err.println("Failed to get authorization");
            error.printStackTrace();
            throw new RuntimeException(error);
        }
    }
    
    /**
     * URL编码
     */
    private static String percentCode(String str) {
        try {
            return URLEncoder.encode(str, "UTF-8")
                .replace("+", "%20")
                .replace("*", "%2A")
                .replace("~", "%7E");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }
    
    /**
     * HMAC-SHA256加密
     */
    private static String hmac256(String key, String data) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKeySpec = new SecretKeySpec(key.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
            mac.init(secretKeySpec);
            byte[] hmacBytes = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(hmacBytes).toLowerCase();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    /**
     * SHA256哈希
     */
    private static String sha256Hex(byte[] bytes) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = digest.digest(bytes);
            return bytesToHex(hashBytes).toLowerCase();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
    
    /**
     * 字节数组转十六进制字符串
     */
    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
    
    /**
     * 处理对象，将嵌套对象展平
     */
    private static void processObject(Map<String, Object> map, String key, Object value) {
        // 如果值为空，则无需进一步处理
        if (value == null) {
            return;
        }
        if (key == null) {
            key = "";
        }
        
        // 当值为Array类型时，遍历Array中的每个元素，并递归处理
        if (value instanceof List) {
            List<?> list = (List<?>) value;
            for (int i = 0; i < list.size(); i++) {
                processObject(map, key + "." + (i + 1), list.get(i));
            }
        } else if (value instanceof Object[] || value.getClass().isArray()) {
            Object[] array = (Object[]) value;
            for (int i = 0; i < array.length; i++) {
                processObject(map, key + "." + (i + 1), array[i]);
            }
        } else if (value instanceof Map) {
            // 当值为Object类型时，遍历Object中的每个键值对，并递归处理
            Map<?, ?> objectMap = (Map<?, ?>) value;
            for (Map.Entry<?, ?> entry : objectMap.entrySet()) {
                processObject(map, key + "." + entry.getKey(), entry.getValue());
            }
        } else {
            // 对于以"."开头的键，移除开头的"."以保持键的连续性
            if (key.startsWith(".")) {
                key = key.substring(1);
            }
            map.put(key, String.valueOf(value));
        }
    }
    
    /**
     * 表单数据转字符串
     */
    public static String formDataToString(Map<String, Object> formData) {
        Map<String, Object> tmp = new HashMap<>();
        processObject(tmp, "", formData);
        
        return tmp.entrySet().stream()
            .map(entry -> {
                try {
                    return URLEncoder.encode(entry.getKey(), "UTF-8") + "=" + 
                           URLEncoder.encode(String.valueOf(entry.getValue()), "UTF-8");
                } catch (UnsupportedEncodingException e) {
                    throw new RuntimeException(e);
                }
            })
            .collect(Collectors.joining("&"));
    }
    
    /**
     * 固定变量签名计算方法
     */
    public static SignedRequest calculateSignature(BatchTranslateRequest req) {
        try {
            // 创建请求实例
            Request signRequest = new Request(HTTP_METHOD, CANONICAL_URI, HOST, X_ACS_ACTION, X_ACS_VERSION);
            
            // 设置查询参数
            Map<String, Object> queryParam = new HashMap<>();
            queryParam.put("RegionId", "cn-beijing");
            signRequest.setQueryParam(queryParam);
            
            // 创建请求体数据
            Map<String, Object> bodyData = new HashMap<>();
            bodyData.put("scene", req.getScene());
            bodyData.put("sourceLanguage", req.getSourceLanguage());
            bodyData.put("streaming", req.isStreaming());
            bodyData.put("targetLanguage", req.getTargetLanguage());
            bodyData.put("text", req.getText());
            bodyData.put("workspaceId", WORKSPACE_ID);
            
            // 创建 body 的字节数组
            String jsonString = objectMapper.writeValueAsString(bodyData);
            byte[] bodyBytes = jsonString.getBytes(StandardCharsets.UTF_8);
            
            // 用于签名计算的 body
            signRequest.setBody(bodyBytes);
            signRequest.getHeaders().put("content-type", "application/json");
            
            // 获取签名
            SignedRequest result = getAuthorization(signRequest);
            
            return result;
            
        } catch (JsonProcessingException e) {
            throw new RuntimeException("JSON序列化失败", e);
        }
    }
}
```

## **常见问题**

#### **1\. AK/SK在哪里获取？**

在[阿里云](https://ram.console.aliyun.com/profile/access-keys)平台的AccessKey模块中获取

#### **2\. 获取Token服务中的workspaceId从哪里获取？**

登录AK/SK对应的阿里云账号后，在[百炼](https://bailian.console.aliyun.com/)左下角的业务空间详情中获取

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3845767571/p997485.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3845767571/p997486.png)

#### **3\. 网络接口调用报没有权限**

未开通通义多模态翻译产品：需要使用AK所属的阿里云主账号，在百炼通义多模态翻译上进行开通

## **变更记录**

#### **2026年3月**

发布版本

发布时间

发布内容

2.0.6

2026年3月5日

双语对照翻译增加lazyload和lazyOffset两个参数
