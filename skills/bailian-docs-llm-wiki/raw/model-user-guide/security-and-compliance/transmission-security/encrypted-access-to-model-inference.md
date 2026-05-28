# 以加密的方式接入模型推理功能

当请求内容涉及敏感信息或通过公网传输时，您可以对请求体中的input字段值加密，防止数据在传输过程中被窃听或篡改。

## 加解密过程

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3284226771/CAEQWhiBgMDutN2xvBkiIGU1NWJmYmRkYzEzMTQ4YTU5YTg5YmJiZWVkODk1ZWQw4860485_20250226112255.459.svg)

采用混合加密机制：数据由AES对称算法加密，其密钥通过RSA非对称加密实现安全传输。

1.  **准备请求数据。**
    
    -   生成AES对称密钥。AES是一种高效的对称加密算法，在此用于加密`input`内容。
        
        > **说明：**`input`为大模型应用调用请求中的核心对象，包含必选的提示词（`prompt`）和可选的历史对话记录（`messages`）等参数。
        
    -   使用密钥对`input`内容进行加密。
        
    -   使用RSA公钥对AES密钥进行加密。从阿里云百炼平台获取托管的RSA公钥，对AES密钥进行加密，以确保AES密钥的传输安全。
        
        > **说明：**RSA是一种非对称加密算法，包括公钥和私钥。其中公钥用于加密数据，私钥用于解密数据。
        
2.  **发起请求。**发起阿里云百炼平台调用时将加密后的`input`内容、密钥信息（封装在`X-DashScope-EncryptionKey`请求头中）传入阿里云百炼平台。
    
3.  **阿里云百炼平台处理请求。**
    
    -   阿里云百炼推理链路中全程加密。
        
    -   阿里云百炼平台在向量召回、模型推理过程中解密数据。
        
    -   使用相同的AES密钥加密生成的答案，返回加密后的推理结果。
        
4.  **处理响应结果。**用户侧收到响应内容，使用AES密钥解密推理结果，获得明文答案。
    

## 前提条件

已开通阿里云百炼服务并获得API-KEY：[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

> **重要：**建议您将API-KEY配置到环境变量中以降低API-KEY的泄漏风险，配置方法可参考[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。您也可以在代码中配置API-KEY，但是泄漏风险会提高。

## DashScope SDK调用（自动加密·开箱即用）

DashScope SDK 封装了加解密逻辑，您只需启用加密功能即可实现加密调用，无需自行实现加密和解密代码。

### 约束与限制

-   不支持自定义密钥，如需自定义密钥，请参见[HTTP调用（手动密钥管理）](#f9489ce581691)。
    
-   仅支持Java和Python，其他编程语言请参见[HTTP调用（手动密钥管理）](#f9489ce581691)。
    

### 接入流程

1.  [安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    
2.  启用加密功能。
    
    ## Java SDK
    
    将`enableEncrypt`设置为`true`即可启用加密功能。
    
    ```
    GenerationParam param = GenerationParam.builder()
      // ...这里省略其他代码
      // 启用加密功能
      .enableEncrypt(true)
      .build();
    ```
    
    ## Python SDK
    
    将`enable_encryption`设置为`True`即可启用加密功能。
    
    ```
    # ...这里省略其他代码
    response = dashscope.Generation.call(
        # ...这里省略其他代码
        # 启用加密功能
        enable_encryption=True
    )
    ```
    
3.  调用模型。使用与普通调用相同的方式发起请求，SDK会自动完成加解密处理。
    

### SDK完整示例代码

> **重要：**示例代码仅供参考，请勿直接在生产环境中使用。

> **说明：**关于请求参数的更多说明，请参见[千问API文档](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#a9b7b197e2q2v)。

## Java SDK

**请求示例**

```
import java.util.Arrays;
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("你是谁？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                // 启用加密功能
                .enableEncrypt(true)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(JsonUtils.toJson(result));
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            // 使用日志框架记录异常信息
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
        System.exit(0);
    }
}
```

**响应示例**

DashScope SDK会自动完成解密，返回的响应内容为明文，无需手动解密。

```
{
    "finish_reason": "stop",
    "text": "我是Qwen，由阿里云开发的超大规模语言模型。我的目标是帮助用户更高效地获取信息、解决各种问题并激发创造力。无论是回答问题、提供信息还是进行创意性的讨论，我都会尽力提供支持。有什么我可以帮到你的吗？"
}
```

## Python SDK

**请求示例**

```
import os
import dashscope

messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': '你是谁？'}
    ]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=messages,
    result_format='message',
    # 启用加密功能
    enable_encryption=True
)
print(response)
```

**响应示例**

DashScope SDK会自动完成解密，返回的响应内容为明文，无需手动解密。

```
{
    "finish_reason": "stop",
    "text": "我是Qwen，由阿里云开发的超大规模语言模型。我的目标是帮助用户更高效地获取信息、解决各种问题并激发创造力。无论是回答问题、提供信息还是进行创意性的讨论，我都会尽力提供支持。有什么我可以帮到你的吗？"
}
```

## HTTP调用（手动密钥管理）

> **说明：**此加密调用方式是阿里云百炼平台提供的安全功能。以下加密流程仅适用于DashScope的Endpoint，OpenAI兼容（Chat Completions API和Responses API）的Endpoint不支持此加密机制。

### 和普通调用的区别

加密调用在普通调用的基础上，需要额外做如下三个处理（详细操作请参见[接入流程](#82ebef1973q9m)）：

1.  添加`X-DashScope-EncryptionKey`请求头。
    
    `X-DashScope-EncryptionKey`请求头对应的内容是一个JSON字符串，各参数说明如下：
    
    -   `public_key_id`：公钥ID。
        
    -   `encrypt_key`：RSA公钥加密后的AES密钥。
        
    -   `iv`：初始向量IV。
        
    
    各参数的具体生成方式，请参见下方[接入流程](#82ebef1973q9m)。
    
2.  对请求参数`input`的内容进行加密。
    
    普通调用和加密调用请求数据的区别：
    
    **普通调用**
    
    **加密调用**
    
    ```
    {
        ...
        "input": {
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "你是谁？"
                }
            ]
        }
        ...
    }
    ```
    
    ```
    {
        ...
        "input": "+J2aT8GNBUD......"
        ...
    }
    ```
    
3.  对响应数据进行解密。
    

### 接入流程

接入流程分为三个阶段：首先准备请求数据（生成AES密钥、生成IV、加密input数据、加密AES密钥），然后构建并发送加密请求，最后解密响应数据。

#### 一、准备请求数据

1.  **生成AES密钥**
    
    -   **算法**：AES
        
    -   **密钥规格**：
        
        -   长度：128位（16字节）/192位（24字节）/256位 (32字节)
            
            > **说明：**密钥长度越长，安全性越高，但计算开销越大；256位安全性最高，适用于金融核心数据等高敏感数据保护。
            
        -   随机性：随机生成，建议使用密码学安全随机源
            
        -   唯一性：单次请求有效，禁止复用
            
    -   **示例代码**：
        
        Java
        
        ```
        private static SecretKey generateAesSecretKey() throws Exception {
                KeyGenerator keyGen = KeyGenerator.getInstance("AES");
                SecureRandom secureRandom = new SecureRandom();
                keyGen.init(256, secureRandom);
                return keyGen.generateKey();
        }
        ```
        
        Python
        
        ```
        def generate_aes_secret_key():
            """生成256位AES密钥"""
            return os.urandom(32)  # 32字节 = 256位
        ```
        
2.  **生成初始向量（IV）**
    
    生成GCM加密所需的随机初始化向量：使用安全的随机数生成器生成一个12字节的随机字节序列，然后将这个字节序列进行Base64编码得到IV。
    
    **示例代码**：
    
    Java
    
    ```
    private static final int GCM_IV_LENGTH = 12; // 12 字节 IV
        
    private static byte[] generateIv() {
        byte[] iv = new byte[GCM_IV_LENGTH];
        SecureRandom secureRandom = new SecureRandom(); // 随机生成确保唯一性
        secureRandom.nextBytes(iv);
        return iv;
    }
    ```
    
    Python
    
    ```
    # 常量定义
    GCM_IV_LENGTH = 12       # 12字节IV
    
    def generate_iv():
        """生成12字节随机IV"""
        return os.urandom(GCM_IV_LENGTH)
    ```
    
3.  **加密input数据**
    
    -   **算法**：AES-GCM（认证标签长度：128位）
        
    -   **参数**：
        
        -   密钥: [步骤1](#49c141a42c7zd)生成的AES密钥
            
        -   IV: [步骤2](#8093061363vcz)生成的初始向量
            
    -   **处理流程**：
        
        1.  将input序列化为JSON字符串：将下图中深色部分内容（即“`{"messages":[......]}`”）序列化
            
            ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8897562571/p976004.png)
            
        2.  对序列化后的`input`执行AES-GCM加密
            
        3.  将加密结果转成字符串格式，待后续[构建并发送请求](#a39aa25bc4i4k)时将其拼接到`input`字段中
            
    -   **示例代码**：
        
        Java
        
        ```
        private static final int GCM_TAG_LENGTH = 128; // 128 位 Tag(16 字节)
        
        private static String encryptInputWithAes(SecretKey aesSecretKey,byte[] iv, String input) throws Exception {
                byte[] content = input.getBytes(StandardCharsets.UTF_8);
        
                Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
                GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
                aesCipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(aesSecretKey.getEncoded(), "AES"), gcmParameterSpec);
        
                byte[] encryptedBytes = aesCipher.doFinal(content);
                return Base64.encodeBase64String(encryptedBytes);
        }
        ```
        
        Python
        
        ```
        def encrypt_input_with_aes(aes_key, iv, plaintext):
            """使用AES-GCM加密数据"""
            # 创建AES-GCM加密器
            aesgcm = Cipher(
                algorithms.AES(aes_key),
                modes.GCM(iv, tag=None),
                backend=default_backend()
            ).encryptor()
            
            # 关联数据设为空（根据需求可调整）
            aesgcm.authenticate_additional_data(b'')
            
            # 加密数据
            ciphertext = aesgcm.update(plaintext.encode('utf-8')) + aesgcm.finalize()
            
            # 获取认证标签
            tag = aesgcm.tag
            
            # 组合密文和标签
            encrypted_data = ciphertext + tag
            
            # 返回Base64编码结果
            return base64.b64encode(encrypted_data).decode('utf-8')
        ```
        
4.  **使用RSA公钥加密AES密钥**
    
    -   **算法**：RSA
        
    -   **处理流程**：
        
        1.  Base64编码原始AES密钥（即[步骤1](#49c141a42c7zd)生成的AES密钥）
            
        2.  使用RSA公钥（请参见[获取RSA的公钥](https://help.aliyun.com/zh/model-studio/model-interface-aes-encryption)从阿里云百炼平台获取`public_key`和`public_key_id`）对编码后的AES密钥进行加密
            
            **说明**
            
            RSA 公钥无需每次请求都重新获取，建议在客户端缓存公钥（推荐缓存时长 1 分钟），以降低高 QPS 场景下的接口调用压力。
            
            公钥在正常情况下不会变更，仅在发生安全事故时才会紧急轮转。因此建议您按如下策略处理公钥缓存：
            
            -   正常情况：使用缓存公钥，缓存过期后自动重新获取最新公钥
                
            -   请求报错时：若返回错误码 `BadRequest.IllegalInput`（错误信息：`The input parameter can not be decoded.`），说明公钥已失效，需立即重新获取最新公钥，可将影响降至最低
                
            
            采用上述策略，即使发生公钥紧急轮转，受影响时间理论上也仅为分钟级别。
            
        3.  对加密结果进行Base64编码
            
    -   **示例代码**：
        
        Java
        
        ```
        private static String encryptAesKeyWithRsaPublicKey(SecretKey aesSecretKey, String publicKey) throws Exception {
                byte[] aesKeyBytes = aesSecretKey.getEncoded();
                String base64AesKey = Base64.encodeBase64String(aesKeyBytes);
        
                byte[] publicKeyBytes = Base64.decodeBase64(publicKey);
                X509EncodedKeySpec spec = new X509EncodedKeySpec(publicKeyBytes);
                KeyFactory kf = KeyFactory.getInstance("RSA");
                PublicKey pubKey = kf.generatePublic(spec);
        
                Cipher rsaCipher = Cipher.getInstance("RSA");
                rsaCipher.init(Cipher.ENCRYPT_MODE, pubKey);
                byte[] encryptedBytes = rsaCipher.doFinal(base64AesKey.getBytes());
        
                return Base64.encodeBase64String(encryptedBytes);
        }
        ```
        
        Python
        
        ```
        def encrypt_aes_key_with_rsa(aes_key, public_key_str):
            """使用RSA公钥加密AES密钥"""
            # 解码Base64格式的公钥
            public_key_bytes = base64.b64decode(public_key_str)
            
            # 加载公钥
            public_key = serialization.load_der_public_key(
                public_key_bytes,
                backend=default_backend()
            )
            
            # 先对AES密钥进行Base64编码
            base64_aes_key = base64.b64encode(aes_key).decode('utf-8')
            
            # 使用RSA加密
            encrypted_bytes = public_key.encrypt(
                base64_aes_key.encode('utf-8'),
                padding.PKCS1v15()
            )
            
            # 返回Base64编码的加密结果
            return base64.b64encode(encrypted_bytes).decode('utf-8')
        ```
        

#### 二、构建并发送请求

添加`X-DashScope-EncryptionKey`请求头，并将原先的`input`替换为加密后的`input`，然后用和普通调用同样的方式发送请求即可。

以下是`X-DashScope-EncryptionKey`请求头的参数说明，各参数的值已在上述准备请求数据阶段生成。

-   `public_key_id`：公钥ID。
    
-   `encrypt_key`：RSA公钥加密后的AES密钥。
    
-   `iv`：初始向量IV。
    

最终发送给大模型的HTTP请求内容格式如下：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8897562571/p980080.png)

**示例代码：**

Java

```
private static String sendEncryptedRequest(String apiKey, String publicKeyId, String encryptedAesKey, byte[] iv, String encryptedInput) throws Exception {
        OkHttpClient okHttpClient = new OkHttpClient().newBuilder().build();

        JSONObject requestBodyJson = new JSONObject();
        requestBodyJson.put("model", "qwen-max");
        requestBodyJson.put("input", encryptedInput);

        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), requestBodyJson.toJSONString());

        JSONObject headerJson = new JSONObject();
        headerJson.put("Content-Type", "application/json");
        headerJson.put("Accept", "application/json");
        headerJson.put("Authorization","Bearer " + apiKey);

        String encryptionHeader = String.format("{\"public_key_id\": \"%s\", \"encrypt_key\": \"%s\", \"iv\": \"%s\"}", publicKeyId, encryptedAesKey, Base64.encodeBase64String(iv));
        headerJson.put("X-DashScope-EncryptionKey", encryptionHeader);

        Headers headers = Headers.of(JSONObject.parseObject(headerJson.toString(), Map.class));

        String url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        Request request = new Request.Builder()
                .url(url)
                .post(requestBody)
                .headers(headers)
                .build();

        return okHttpClient.newCall(request).execute().body().string();
}
```

Python

```
def send_encrypted_request(api_key, public_key_id, encrypted_aes_key, iv, encrypted_input):
    """发送加密请求到API端点"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-EncryptionKey": json.dumps({
            "public_key_id": public_key_id,
            "encrypt_key": encrypted_aes_key,
            "iv": base64.b64encode(iv).decode('utf-8')
        })
    }
    
    # 构建请求体
    payload = {
        "model": "qwen-max",
        "input": encrypted_input
    }
    
    # 发送POST请求
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    
    # 检查响应状态
    response.raise_for_status()
    return response.json()
```

#### 三、解密响应数据

-   **算法**：AES-GCM
    
-   **参数**：
    
    -   密钥：发送请求时生成的AES密钥（即准备请求数据阶段的[步骤1](#49c141a42c7zd)生成的AES密钥）。
        
    -   IV: 发送请求时使用的初始化向量（即准备请求数据阶段的[步骤2](#8093061363vcz)生成的IV）。
        
-   **处理流程**：
    
    1.  使用AES-GCM解密`output`字段对应的内容。
        
    2.  返回明文结果。
        
-   **示例代码**：
    
    Java
    
    ```
    private static String decryptResponseWithAes(SecretKey aesSecretKey, byte[] iv, String response) throws Exception {
            JSONObject responseJson = JSONObject.parseObject(response, JSONObject.class);
            String encryptedOutput = responseJson.getString("output");
    
            Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
            GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
            aesCipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(aesSecretKey.getEncoded(), "AES"), gcmParameterSpec);
    
            byte[] decryptedBytes = aesCipher.doFinal(Base64.decodeBase64(encryptedOutput));
            return new String(decryptedBytes);
    }
    ```
    
    Python
    
    ```
    def decrypt_response_with_aes(aes_key, iv, response_data):
        """使用AES-GCM解密响应"""
        # 提取加密的输出
        encrypted_output = response_data.get("output")
        if not encrypted_output:
            raise ValueError("Response missing 'output' field")
        
        # 解码Base64数据
        encrypted_data = base64.b64decode(encrypted_output)
        
        # 分离密文和标签（标签长度16字节）
        ciphertext = encrypted_data[:-16]
        tag = encrypted_data[-16:]
        
        # 创建AES-GCM解密器
        aesgcm = Cipher(
            algorithms.AES(aes_key),
            modes.GCM(iv, tag),
            backend=default_backend()
        ).decryptor()
        
        # 验证关联数据（与加密时一致）
        aesgcm.authenticate_additional_data(b'')
        
        # 解密数据
        decrypted_bytes = aesgcm.update(ciphertext) + aesgcm.finalize()
        
        return decrypted_bytes.decode('utf-8')
    ```
    

### HTTP完整示例代码

本节提供Java和Python的完整示例代码，将上述接入流程中的各步骤整合为可直接运行的完整程序。如您使用其他编程语言，请参照接入流程自行实现。

> **提示：**如需其他编程语言的实现，您可以借助大模型将以下代码转换为目标语言。

> **重要：**示例代码仅供参考，请勿直接在生产环境中使用。

> **说明：**关于请求参数的更多说明，请参见[千问API文档](https://help.aliyun.com/zh/model-studio/qwen-api-reference/#a9b7b197e2q2v)。

**请求示例**

Java

```
import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.spec.X509EncodedKeySpec;
import java.util.Map;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import org.apache.commons.codec.binary.Base64;
import com.alibaba.fastjson.JSONObject;
import okhttp3.Headers;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;

public class Main {
    // 采用AES-GCM 加密模式，以提升数据安全和完整性保护，在此指定IV、Tag长度
    private static final int GCM_TAG_LENGTH = 128; // 128 位 Tag(16 字节)
    private static final int GCM_IV_LENGTH = 12; // 12 字节 IV

    public static void main(String[] args) throws Exception {
        String publicKeyId = "xxx"; // 需要替换为实际获取到的RSA公钥 public_key_id 值
        String publicKey = "xxx"; // 需要替换为实际获取到的RSA公钥 public_key 值

        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：String apiKey = "sk-xxx"，但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        // 生成 AES 密钥
        SecretKey aesSecretKey = generateAesSecretKey();

        // 生成唯一性iv
        byte[] iv = generateIv();

        // 加密 input 数据
        String input = "{\"messages\": [{\"role\":\"user\",\"content\":\"你是谁？\"}]}";
        String encryptedInput = encryptInputWithAes(aesSecretKey, iv, input);

        // 使用 RSA 公钥加密 AES 密钥
        String encryptedAesKey = encryptAesKeyWithRsaPublicKey(aesSecretKey, publicKey);

        // 构建并发送请求
        String response = sendEncryptedRequest(apiKey, publicKeyId, encryptedAesKey, iv, encryptedInput);

        // 解密响应内容
        String decryptOutput = decryptResponseWithAes(aesSecretKey, iv, response);
        System.out.println("输出的内容是: " + decryptOutput);
    }

    private static SecretKey generateAesSecretKey() throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        SecureRandom secureRandom = new SecureRandom();
        keyGen.init(256, secureRandom); // AES密钥长度支持128、192、256 位。
        return keyGen.generateKey();
    }

    private static byte[] generateIv() {
        byte[] iv = new byte[GCM_IV_LENGTH];
        SecureRandom secureRandom = new SecureRandom(); // 随机生成确保唯一性
        secureRandom.nextBytes(iv);
        return iv;
    }

    private static String encryptAesKeyWithRsaPublicKey(SecretKey aesSecretKey, String publicKey) throws Exception {
        byte[] aesKeyBytes = aesSecretKey.getEncoded();
        String base64AesKey = Base64.encodeBase64String(aesKeyBytes);

        byte[] publicKeyBytes = Base64.decodeBase64(publicKey);
        X509EncodedKeySpec spec = new X509EncodedKeySpec(publicKeyBytes);
        KeyFactory kf = KeyFactory.getInstance("RSA");
        PublicKey pubKey = kf.generatePublic(spec);

        Cipher rsaCipher = Cipher.getInstance("RSA");
        rsaCipher.init(Cipher.ENCRYPT_MODE, pubKey);
        byte[] encryptedBytes = rsaCipher.doFinal(base64AesKey.getBytes());

        return Base64.encodeBase64String(encryptedBytes);
    }

    private static String encryptInputWithAes(SecretKey aesSecretKey, byte[] iv, String input) throws Exception {
        byte[] content = input.getBytes(StandardCharsets.UTF_8);

        Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        aesCipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(aesSecretKey.getEncoded(), "AES"), gcmParameterSpec);

        byte[] encryptedBytes = aesCipher.doFinal(content);
        return Base64.encodeBase64String(encryptedBytes);
    }

    private static String sendEncryptedRequest(String apiKey, String publicKeyId, String encryptedAesKey, byte[] iv, String encryptedInput) throws Exception {
        OkHttpClient okHttpClient = new OkHttpClient().newBuilder().build();
        JSONObject requestBodyJson = new JSONObject();
        requestBodyJson.put("model", "qwen-max");
        requestBodyJson.put("input", encryptedInput);

        RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), requestBodyJson.toJSONString());

        JSONObject headerJson = new JSONObject();
        headerJson.put("Content-Type", "application/json");
        headerJson.put("Accept", "application/json");
        headerJson.put("Authorization","Bearer " + apiKey);

        String encryptionHeader = String.format("{\"public_key_id\": \"%s\", \"encrypt_key\": \"%s\", \"iv\": \"%s\"}", publicKeyId, encryptedAesKey, Base64.encodeBase64String(iv));
        headerJson.put("X-DashScope-EncryptionKey", encryptionHeader);

        Headers headers = Headers.of(JSONObject.parseObject(headerJson.toString(), Map.class));

        String url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
        Request request = new Request.Builder()
                .url(url)
                .post(requestBody)
                .headers(headers)
                .build();

        return okHttpClient.newCall(request).execute().body().string();
    }

    private static String decryptResponseWithAes(SecretKey aesSecretKey, byte[] iv,String response) throws Exception {
        JSONObject responseJson = JSONObject.parseObject(response, JSONObject.class);
        String encryptedOutput = responseJson.getString("output");

        Cipher aesCipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
        aesCipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(aesSecretKey.getEncoded(), "AES"), gcmParameterSpec);

        byte[] decryptedBytes = aesCipher.doFinal(Base64.decodeBase64(encryptedOutput));
        return new String(decryptedBytes);
    }
}
```

Python

```
import os
import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests

# 常量定义
GCM_IV_LENGTH = 12       # 12字节IV

def main():
    public_key_id = "xxx"  # 需要替换为实际获取到的RSA公钥 public_key_id 值
    public_key = "xxx"     # 需要替换为实际获取到的RSA公钥 public_key 值
    
    # 从环境变量获取API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        # 若没有配置环境变量，请放开下面这行注释代码，并将"sk-xxx"替换为实际的阿里云百炼API Key，不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        # api_key = "sk-xxx"
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    # 生成AES密钥
    aes_secret_key = generate_aes_secret_key()
    
    # 生成IV
    iv = generate_iv()
    
    # 加密输入数据
    input_data = '{"messages": [{"role":"user","content":"你是谁？"}]}'
    encrypted_input = encrypt_input_with_aes(aes_secret_key, iv, input_data)
    
    # 使用RSA公钥加密AES密钥
    encrypted_aes_key = encrypt_aes_key_with_rsa(aes_secret_key, public_key)
    
    # 发送加密请求
    response = send_encrypted_request(api_key, public_key_id, encrypted_aes_key, iv, encrypted_input)
    
    # 解密响应
    decrypted_output = decrypt_response_with_aes(aes_secret_key, iv, response)
    print("输出的内容是:", decrypted_output)

def generate_aes_secret_key():
    """生成256位AES密钥"""
    return os.urandom(32)  # 32字节 = 256位

def generate_iv():
    """生成12字节随机IV"""
    return os.urandom(GCM_IV_LENGTH)

def encrypt_aes_key_with_rsa(aes_key, public_key_str):
    """使用RSA公钥加密AES密钥"""
    # 解码Base64格式的公钥
    public_key_bytes = base64.b64decode(public_key_str)
    
    # 加载公钥
    public_key = serialization.load_der_public_key(
        public_key_bytes,
        backend=default_backend()
    )
    
    # 先对AES密钥进行Base64编码
    base64_aes_key = base64.b64encode(aes_key).decode('utf-8')
    
    # 使用RSA加密
    encrypted_bytes = public_key.encrypt(
        base64_aes_key.encode('utf-8'),
        padding.PKCS1v15()
    )
    
    # 返回Base64编码的加密结果
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def encrypt_input_with_aes(aes_key, iv, plaintext):
    """使用AES-GCM加密数据"""
    # 创建AES-GCM加密器
    aesgcm = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv, tag=None),
        backend=default_backend()
    ).encryptor()
    
    # 关联数据设为空（根据需求可调整）
    aesgcm.authenticate_additional_data(b'')
    
    # 加密数据
    ciphertext = aesgcm.update(plaintext.encode('utf-8')) + aesgcm.finalize()
    
    # 获取认证标签
    tag = aesgcm.tag
    
    # 组合密文和标签
    encrypted_data = ciphertext + tag
    
    # 返回Base64编码结果
    return base64.b64encode(encrypted_data).decode('utf-8')

def send_encrypted_request(api_key, public_key_id, encrypted_aes_key, iv, encrypted_input):
    """发送加密请求到API端点"""
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    
    # 构建请求头
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-DashScope-EncryptionKey": json.dumps({
            "public_key_id": public_key_id,
            "encrypt_key": encrypted_aes_key,
            "iv": base64.b64encode(iv).decode('utf-8')
        })
    }
    
    # 构建请求体
    payload = {
        "model": "qwen-max",
        "input": encrypted_input
    }
    
    # 发送POST请求
    response = requests.post(
        url,
        headers=headers,
        json=payload
    )
    
    # 检查响应状态
    response.raise_for_status()
    return response.json()

def decrypt_response_with_aes(aes_key, iv, response_data):
    """使用AES-GCM解密响应"""
    # 提取加密的输出
    encrypted_output = response_data.get("output")
    if not encrypted_output:
        raise ValueError("Response missing 'output' field")
    
    # 解码Base64数据
    encrypted_data = base64.b64decode(encrypted_output)
    
    # 分离密文和标签（标签长度16字节）
    ciphertext = encrypted_data[:-16]
    tag = encrypted_data[-16:]
    
    # 创建AES-GCM解密器
    aesgcm = Cipher(
        algorithms.AES(aes_key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()
    
    # 验证关联数据（与加密时一致）
    aesgcm.authenticate_additional_data(b'')
    
    # 解密数据
    decrypted_bytes = aesgcm.update(ciphertext) + aesgcm.finalize()
    
    return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    main()
```

**响应示例**

DashScope SDK会自动完成解密，返回的响应内容为明文，无需手动解密。

```
{
    "finish_reason": "stop",
    "text": "我是Qwen，由阿里云开发的超大规模语言模型。我的目标是帮助用户更高效地获取信息、解决各种问题并激发创造力。无论是回答问题、提供信息还是进行创意性的讨论，我都会尽力提供支持。有什么我可以帮到你的吗？"
}
```

## 常见问题

**Q：为什么代码执行报错，“Invalid AES key Length: 294 bytes”？**

A：AES密钥长度支持128位（16字节）、192位（24字节）、256 位（32字节），请检查密钥长度设置是否符合要求。

**Q：OpenAI兼容（Chat Completions API 和 Responses API）的Endpoint是否支持加密推理？**

A：不支持，本文的加密流程仅适用于DashScope SDK和HTTP的Endpoint。

**Q：RSA公钥是否需要每次请求都重新获取？**

A：不需要。建议在客户端缓存 RSA 公钥（推荐缓存时长 1 分钟），公钥在正常情况下不会变更，仅在发生安全事故时才会紧急轮转。若请求返回错误码 `BadRequest.IllegalInput`（`The input parameter can not be decoded.`），则说明公钥已失效，需立即重新获取最新公钥。

## 错误码

如果调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
