# 网页翻译JSSDK

## 功能描述

基于翻译大模型的页面翻译插件，提供页面翻译功能。您可以通过JSSDK，一键完成网站的多语言改造。

## 技术流程

## 接入JSSDK

## 当前版本

项目

值

**版本号**

`3.0.1`

CDN 根路径

`[https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/)`

下文示例中的版本号均以 `3.0.1` 为准，升级时请同步替换 CDN 链接中的版本号。

* * *

SDK 提供两种翻译模式：

-   页面翻译（`pageTranslate`）：直接替换页面原文为译文，适合“单语展示”场景。
-   段落对照翻译（`paragraphTranslate`）：在原文后插入译文，适合“原文+译文对照阅读”场景。

同时支持：

-   懒加载翻译（只翻译可视区域）
-   动态内容翻译（DOM 变化后自动翻译）
-   术语表与翻译记忆
-   细粒度 hooks（翻译前/后插入自定义逻辑）

* * *

## 引入方式

通过 Script 标签从 CDN 引入，支持两种方式：

### 方式一：全量引入（推荐上手）

一次引入 `index.js`（已包含核心 + 全部插件），即可同时使用页面翻译与段落对照：

文件

说明

地址

`index.js`

全量包（核心 + 插件）

[](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.0/index.js)[https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js)

```
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js"></script>
```

### 方式二：按需拆包引入

先加载 `core.js`，再按需加载对应插件脚本：

文件

说明

地址

`core.js`

核心 SDK

[](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.0/core.js)[https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/core.js](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/core.js)

`page.js`

页面翻译插件

[](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.0/page.js)[https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/page.js](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/page.js)

`paragraph.js`

段落对照插件

[](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.0/paragraph.js)[https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/paragraph.js](https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/paragraph.js)

```
<!-- 页面翻译 -->
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/core.js"></script>
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/page.js"></script>

<!-- 段落对照：将 page.js 换成 paragraph.js -->
<!-- 两种模式都要用：同时引入 page.js 与 paragraph.js -->
```

说明：

-   全量引入只需一个文件；拆包引入必须先加载 `core.js`，再加载插件。
-   全局对象为 `window.AliTranslate`，同时提供别名 `window.__AliTranslate`（两者指向同一实例）。

* * *

## 快速开始

### 页面翻译（Pure Page）

```
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js"></script>
<script>
  AliTranslate.pageTranslate({
    getToken: async (params) => {
      const res = await fetch('https://your-sign-api.example.com/signature', {
        method: 'POST',
        body: JSON.stringify(params),
      });
      return (await res.json()).data;
    },
    srcLanguage: 'auto',
    tgtLanguage: 'en',
    targetSelectors: ['#app'],
    excludeSelectors: ['.no-translate', 'code', 'pre'],
    translateAttributes: ['placeholder'],
    lazyload: true,
    dynamic: true,
  });
</script>
```

### 段落对照翻译（Paragraph Compare）

```
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js"></script>
<script>
  AliTranslate.paragraphTranslate({
    getToken: async (params) => {
      const res = await fetch('https://your-sign-api.example.com/signature', {
        method: 'POST',
        body: JSON.stringify(params),
      });
      return (await res.json()).data;
    },
    srcLanguage: 'auto',
    tgtLanguage: 'en',
    targetSelectors: ['#article'],
    excludeSelectors: ['.no-translate', 'code', 'pre'],
    translateAttributes: ['placeholder'],
    lazyload: true,
    dynamic: true,
    extraBlockSelectors: ['.article-title', 'h1', 'h2', 'h3'],
    extraInlineSelectors: ['.breadcrumb', '.tag-inline'],
  });
</script>
```

* * *

## 初始化参数（SDKConfig）

`AliTranslate.pageTranslate` / `AliTranslate.paragraphTranslate` 中共用的 SDK 级参数如下：

参数

类型

必填

说明

`getToken`

`(params) => Promise<SignedRequest>`

是

鉴权签名函数，返回可直接请求翻译服务的签名请求

`terminologies`

`Array<{ src, tgt }>`

否

术语表，提升领域词一致性

`examples`

`Array<{ src, tgt }>`

否

翻译记忆

`domainHint`

`string`

否

业务领域（透传至翻译请求）

`chunkSize`

`number`

否

分块阈值（影响请求合并与吞吐）

`maxRetries`

`number`

否

翻译失败最大重试次数

`afterTranslate`

`(result) => void`

否

翻译完成回调

* * *

## 页面翻译参数（PageTranslateConfig）

参数

类型

必填

说明

`tgtLanguage`

`LANGUAGE`

是

目标语种

`srcLanguage`

`LANGUAGE`

否

源语种，不传默认自动检测

`targetSelectors`

`string | string[]`

否

翻译根节点，默认 `body`

`excludeSelectors`

`string | string[]`

否

排除节点（命中后整棵子树不翻译）

`translateAttributes`

`string | string[]`

否

翻译支持的元素属性

`lazyload`

`boolean`

否

是否启用懒加载翻译

`lazyOffset`

`number`

否

懒加载视口偏移（px）

`lazySelectors`

`string | string[]`

否

懒翻译选择器（当前版本为预留字段，建议优先使用 `targetSelectors`）

`dynamic`

`boolean`

否

是否监听 DOM 变化并自动翻译

`translateDelay`

`number`

否

初始化等待/动态翻译节流延迟（ms）

`rules`

`Array<{ selector; style?; className? }>`

否

页面翻译规则（作用于原文容器）

`onBeforeInsertTrans`

`(ctx) => void | HTMLElement | Promise<...>`

否

插入译文前回调

`onTranslatingStart`

`(ctx) => void | Promise<void>`

否

单节点翻译开始回调

`onTranslatingEnd`

`(ctx) => void | Promise<void>`

否

单节点翻译结束回调

* * *

## 段落对照参数（ParagraphTranslateConfig）

参数

类型

必填

说明

`tgtLanguage`

`LANGUAGE`

是

目标语种

`srcLanguage`

`LANGUAGE`

否

源语种，不传默认自动检测

`targetSelectors`

`string | string[]`

否

翻译根节点，默认 `body`

`excludeSelectors`

`string | string[]`

否

排除节点（命中后不参与段落提取）

`translateAttributes`

`string | string[]`

否

翻译支持的元素属性

`lazyload`

`boolean`

否

是否启用懒加载翻译

`lazyOffset`

`number`

否

懒加载视口偏移（px）

`lazySelectors`

`string | string[]`

否

懒翻译选择器（当前版本为预留字段，建议优先使用 `targetSelectors`）

`dynamic`

`boolean`

否

是否监听 DOM 变化并自动翻译

`translateDelay`

`number`

否

初始化等待/动态翻译节流延迟（ms）

`extraBlockSelectors`

`string | string[]`

否

强制按 block 方式插入译文（独占一行）

`extraInlineSelectors`

`string | string[]`

否

强制按 inline 方式插入译文（同行展示）

`rules`

`TransStyleRule[]`

否

对照翻译样式规则

`onBeforeInsertTrans`

`(ctx) => void | HTMLElement | Promise<...>`

否

插入 `<trans>` 之前回调

`onTranslatingStart`

`(ctx) => void | Promise<void>`

否

单段落翻译开始回调

`onTranslatingEnd`

`(ctx) => void | Promise<void>`

否

单段落翻译结束回调

### `TransStyleRule` 说明

```
interface TransStyleRule {
  selector: string
  transStyle?: Record<string, string> // 作用于译文节点 <trans>
  style?: Record<string, string>      // 作用于命中 selector 的父容器
  className?: string                  // 作用于命中 selector 的父容器
}
```

* * *

## Hooks 与可回滚 DOM 变更

SDK 提供了 `mutator`（可回滚变更操作器），支持在 hooks 中做安全 DOM 操作，并在 `removeTranslations()` 时自动回滚。

```
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js"></script>
<script>
  AliTranslate.paragraphTranslate({
    getToken: async (params) => {
      const res = await fetch('https://your-sign-api.example.com/signature', {
        method: 'POST',
        body: JSON.stringify(params),
      });
      return (await res.json()).data;
    },
    tgtLanguage: 'en',
    onTranslatingStart: (ctx) => {
      const loading = document.createElement('span');
      loading.className = 'loading';
      loading.textContent = '翻译中...';
      loading.setAttribute('data-source-hash', ctx.sourceHash);
      ctx.mutator.appendNode(ctx.paragraph.commonAncestor, loading);
    },
    onTranslatingEnd: (ctx) => {
      const loading = ctx.paragraph.commonAncestor.querySelector(
        `.loading[data-source-hash="${ctx.sourceHash}"]`,
      );
      if (loading) ctx.mutator.removeNode(loading);
    },
    onBeforeInsertTrans: (ctx) => {
      ctx.transNode.style.color = '#4f46e5';
      return ctx.transNode;
    },
  });
</script>
```

`mutator` 可用能力：

-   `setStyle(el, prop, value, priority?)`
-   `addClass(el, className)`
-   `removeClass(el, className)`
-   `appendNode(parent, node)`
-   `removeNode(node)`

* * *

## 语种与枚举值

常用语种值示例：

-   `auto`（自动检测）
-   `zh`、`en`、`ja`、`ko`、`fr`、`de`、`es`、`ru`、`ar`、`th`、`vi`

完整语言枚举请参考 SDK 类型定义 `LANGUAGE`。

* * *

## 常用 API

```
// 移除翻译结果（保留 SDK 实例）
AliTranslate.removeTranslations()

// 销毁 SDK（释放资源，插件与事件解绑）
AliTranslate.destroy()
```

* * *

## 完整示例（段落对照 + rules + hooks）

```
<script src="https://g.alicdn.com/code/npm/@alife/translate-js-sdk/3.0.1/index.js"></script>
<script>
  AliTranslate.paragraphTranslate({
    getToken: async (params) => {
      const res = await fetch('https://your-sign-api.example.com/signature', {
        method: 'POST',
        body: JSON.stringify(params),
      });
      return (await res.json()).data;
    },
    srcLanguage: 'auto',
    tgtLanguage: 'en',
    targetSelectors: ['#article'],
    excludeSelectors: ['.no-translate', 'code', 'pre'],
    lazyload: true,
    lazyOffset: 120,
    dynamic: true,
    translateDelay: 200,
    extraBlockSelectors: ['.title', 'h1', 'h2'],
    extraInlineSelectors: ['.breadcrumb'],
    rules: [
      {
        selector: '.highlight',
        transStyle: { color: '#4f46e5' },
        style: { background: '#eef2ff' },
        className: 'translated-highlight',
      },
    ],
    onBeforeInsertTrans: (ctx) => {
      // 自定义译文节点样式，给所有翻译前(排除h1, h2, h3)添加一个border
      if (ctx.paragraph.commonAncestor.matches('h1, h2, h3')) {
        return ctx.transNode;
      }
      ctx.transNode.style.borderLeft = '2px solid #e94560';
      ctx.transNode.style.paddingLeft = '0.75rem';
      ctx.transNode.style.marginTop = '0.5rem';
    },
    onTranslatingStart: (ctx) => {
      // 为翻译中的节点添加 loading
      const loading = document.createElement('span');
      loading.className = 'loading';
      loading.setAttribute('data-source-hash', ctx.sourceHash);
      loading.textContent = '翻译中...';
      ctx.mutator.appendNode(ctx.paragraph.commonAncestor, loading);
    },
    onTranslatingEnd: (ctx) => {
      // 移除自定义添加的 loading
      const root = ctx.paragraph.commonAncestor;
      const loading = root.querySelector(`.loading[data-source-hash="${ctx.sourceHash}"]`);
      if (loading) ctx.mutator.removeNode(loading);
    },
  });
</script>
```

* * *

如需同时支持“页面翻译”和“段落对照翻译”，推荐直接使用全量包 `index.js`，并在业务 UI 中明确区分两种模式的切换与清理流程。

## 获取Token服务

使用阿里云SDK的V3版本请求体&签名机制进行请求签名

javascript

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
    console.log('signature=YOUR_SIGNATURE>', signature);
    // 步骤 4：拼接 Authorization
    const authorization = `${ALGORITHM} Credential=${accessKeyId},SignedHeaders=${signedHeaders},Signature=YOUR_SIGNATURE
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

java

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
            System.out.println("signature=YOUR_SIGNATURE>" + signature);
            // 步骤 4：拼接 Authorization
            String authorization = String.format("%s Credential=%s,SignedHeaders=%s,Signature=YOUR_SIGNATURE",
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

## 注意事项（生产接入建议）

-   **必须配置**`getToken`：由业务侧完成鉴权签名后再发起翻译请求。
-   **引入方式二选一**：全量引入 `index.js` 即可；若按需拆包，页面翻译需引入 `page.js`，段落对照需引入 `paragraph.js`。
-   **重复翻译建议先清理**：多次切换参数/语言前建议先执行 `removeTranslations()`，避免旧状态干扰新配置验证。
-   **目标与排除选择器要收敛**：`targetSelectors` 建议限定业务容器，`excludeSelectors` 排除导航、代码块、编辑区等。
-   **避免翻译敏感区域**：如输入框、编辑器、业务脚本节点、模板容器。
-   **Hook 里避免重逻辑**：`onTranslatingStart/End` 触发频率高，避免耗时操作阻塞主线程。
-   **动态内容场景建议开启**`dynamic`：适配懒渲染和流式加载页面。

## 常见问题

### 调用无效果

-   检查是否已正确引入脚本（全量 `index.js`，或 `core.js` + 对应插件）。
-   检查 `targetSelectors` 是否命中。
-   检查 `excludeSelectors` 是否误伤目标区域。
-   检查签名接口是否返回合法请求结构。

### rules / hooks 未生效

-   确认传参写在 `pageTranslate` / `paragraphTranslate` 的同一层级。
-   重复执行前先 `removeTranslations()` 再重新翻译。
-   检查 `selector` 是否可命中段落 `commonAncestor` 或其祖先。

### loading 看不到

-   翻译速度很快时会瞬时消失，建议在业务侧设置最小可见时长（如 300-500ms）。
-   用 `data-source-hash` 做唯一标识，避免并发段落相互覆盖。

### AK/SK在哪里获取？

-   在[阿里云](https://ram.console.aliyun.com/profile/access-keys)平台的AccessKey模块中获取

### 获取Token服务中的workspaceId从哪里获取？

-   登录AK/SK对应的阿里云账号后，在[百炼](https://bailian.console.aliyun.com/)左下角的业务空间详情中获取
-   弹窗中的**业务空间id**即对应所需的workspaceId，单击字段右侧的复制图标可直接复制。

### 网络接口调用报没有权限

-   未开通 通义多模态翻译 产品：需要使用AK所属的阿里云主账号，在百炼通义多模态翻译上进行开通

* * *

## 变更记录

#### 2026年3月

发布版本

发布时间

发布内容

3.0.1

2026年8月6日

支持页面元素的属性内容翻译（配置参数）

3.0.0

2026年7月16日

大版本升级，增加按需引入、术语/语料/domain配置、样式干预、更多的配置参数

2.0.6

2026年3月5日

双语对照翻译增加lazyload和lazyOffset两个参数
