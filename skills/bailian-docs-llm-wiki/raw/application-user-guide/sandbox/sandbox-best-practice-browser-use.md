# 使用 Browser Use Sandbox

面向网页自动化类 Agent 的最佳实践：基于浏览器镜像创建模版，通过 CDP 连接 Puppeteer、Playwright 或 BrowserUse，完成网页访问、交互、截图与结果归档。

Browser Use Sandbox 面向需要访问网页、点击按钮、填写表单、截图归档或抓取动态页面的 Agent。推荐基于浏览器镜像（`browser`）创建模版：3000 端口提供 browser 服务，可通过 CDP 连接 Puppeteer、Playwright 或 BrowserUse。

如果任务只涉及网页访问、点击、截图、下载文件和轻量结果提取，使用 Browser Use Sandbox 即可；浏览器产物还需要在同一会话中交给 Python/Node.js 做数据清洗、表格分析或报告生成时，优先使用 [AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

**警告**沙箱公网 URL 应视为访问凭证：未设置应用层鉴权时，持有 URL 的人可完全控制沙箱内浏览器（含已登录态与 Cookie）。请勿公开分享，也不要写入日志或前端代码。

## 适用场景

**场景**

**说明**

网页数据采集

访问动态页面，提取标题、正文、表格、链接或业务字段

运营后台自动化

登录后台，填写表单，点击按钮，下载报表或截图归档

页面巡检

定时打开页面，验证关键元素、截图、性能或可用性

轻量 E2E 测试

在隔离浏览器环境中运行端到端测试，避免污染 CI Worker

浏览器工具型 Agent

让 Agent 通过 BrowserUse 等框架完成多步骤网页任务

## 推荐流程

1.  基于浏览器镜像（`browser`）创建模版并获取 `templateCode`，详见[模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)。
2.  使用模版创建沙箱，并设置合理的超时时间。
3.  通过 `sandbox.getHost(3000)` 获取 browser 服务公网 host。
4.  轮询 `/health`，确认 browser 服务已经就绪。
5.  通过 `wss://<sandbox-host>/ws/automation` 连接 Puppeteer、Playwright 或 BrowserUse。
6.  执行网页访问、点击、输入、截图、PDF 生成或下载。
7.  将结构化结果、截图、HTML、PDF 或下载文件保存到沙箱任务目录。
8.  业务侧读取结果后销毁沙箱。

## 准备本地环境

以下示例使用 Node.js 与 Puppeteer Core。业务侧不需要安装完整浏览器，Chromium/Chrome 已运行在沙箱中。

```
{
  "name": "browser-use-sandbox-demo",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "e2b": "2.31.0",
    "puppeteer-core": "^24.0.0"
  }
}
```

**说明**`e2b` 固定为 2.31.0（示例验证版本），更高版本的 SDK 创建实例时返回 405。

下文 BrowserUse 接入的 Python 示例还需安装：

```
pip install "browser-use==0.13.10" "e2b==2.31.0"
```

BrowserUse 示例中的模型调用使用百炼 OpenAI 兼容接口，`api_key` 填百炼 API Key（必填），`model` 可选，默认 `qwen-vl-max`。

## Puppeteer 示例

示例流程：

1.  创建沙箱。
2.  等待 browser 服务 `/health` 返回 200。
3.  通过 CDP 连接云端浏览器。
4.  打开 `https://example.com`，提取页面信息并保存截图。

```
import { writeFile } from "node:fs/promises";
import puppeteer from "puppeteer-core";
import { Sandbox } from "e2b";

const ALIYUN_UID = "your aliyunUid";
const BAILIAN_API_KEY = "sk-...";
const BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox";
const TEMPLATE = "你的模版 code";

const BROWSER_PORT = 3000;
const TARGET_URL = "https://example.com";
const TASK_DIR = "/tmp/browser-task";
const SCREENSHOT_PATH = `${TASK_DIR}/browser-example.png`;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function toArrayBuffer(bytes) {
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

async function waitUntilHealthy(sandbox, host, timeoutMs = 60_000) {
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    let result;
    try {
      result = await sandbox.commands.run(
        `curl -sS -o /dev/null -w '%{http_code}' -m 4 ` +
          `https://${host}/health`,
        { timeoutMs: 10_000 },
      );
    } catch (error) {
      result = error;
    }

    const code = (result.stdout || "").trim();
    if (code === "200") {
      return;
    }
    await sleep(2_000);
  }

  throw new Error(`browser 服务在 ${timeoutMs}ms 内未就绪`);
}

let sandbox;

try {
  sandbox = await Sandbox.create(TEMPLATE, {
    apiUrl: BASE_URL,
    apiKey: `e2b_${ALIYUN_UID}`,
    apiHeaders: { Authorization: `Bearer ${BAILIAN_API_KEY}` },
    timeoutMs: 300_000,
    secure: true,
  });

  const host = sandbox.getHost(BROWSER_PORT);

  await sandbox.files.makeDir(TASK_DIR);
  await waitUntilHealthy(sandbox, host);

  const browser = await puppeteer.connect({
    browserWSEndpoint: `wss://${host}/ws/automation`,
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1365, height: 768 });
  await page.goto(TARGET_URL, {
    waitUntil: "networkidle2",
    timeout: 60_000,
  });

  const screenshot = await page.screenshot({ fullPage: true });
  await sandbox.files.write(SCREENSHOT_PATH, toArrayBuffer(screenshot));
  await writeFile("browser-example.png", screenshot);

  const result = await page.evaluate(() => ({
    url: location.href,
    title: document.title,
    text: document.body.innerText.replace(/\s+/g, " ").slice(0, 500),
  }));

  await browser.close();
  console.log(result);
} finally {
  if (sandbox) {
    await sandbox.kill();
  }
}
```

## BrowserUse 接入

对于以自然语言驱动网页操作的 Agent，可让 BrowserUse 连接沙箱暴露的 CDP 地址。业务服务负责创建和销毁沙箱；BrowserUse 只连接这个沙箱中的浏览器会话。

```
import asyncio

from browser_use import Agent, BrowserSession, ChatOpenAI
from browser_use.browser import BrowserProfile
from e2b import Sandbox

BROWSER_PORT = 3000
BAILIAN_API_KEY = "sk-..."

async def main():
    browser_session = None
    sandbox = Sandbox.create(
        api_url="https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
        api_key="e2b_your aliyunUid",
        headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
        template="你的模版 code",
        timeout=600,
        secure=True,
    )

    try:
        host = sandbox.get_host(BROWSER_PORT)
        cdp_url = f"wss://{host}/ws/automation"

        browser_session = BrowserSession(
            cdp_url=cdp_url,
            browser_profile=BrowserProfile(
                headless=False,
                keep_alive=True,
            ),
        )

        agent = Agent(
            task="访问 https://example.com 并提取页面标题，总结首屏正文",
            llm=ChatOpenAI(
                model="qwen-vl-max",
                api_key=BAILIAN_API_KEY,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
            browser_session=browser_session,
            use_vision=True,
        )
        result = await agent.run(max_steps=20)
        print(result)
    finally:
        if browser_session is not None:
            await browser_session.stop()
        sandbox.kill()

if __name__ == "__main__":
    asyncio.run(main())
```

这类接入方式适合搜索、比较、填写表单、点击确认和生成截图证据。需要稳定产物时，让 Agent 把关键结果写成 JSON，同时保留截图或 HTML 片段，便于人工复核和问题追踪。

## 上线建议

-   把每个浏览器任务限制在明确的 URL 范围内，必要时增加域名白名单。
-   限制下载文件类型、单文件大小、总输出大小和任务生命周期。
-   通过 `max_steps` 控制 Agent 任务的最大步数，避免模型重复执行同类动作。
-   页面内容可能包含 prompt injection，不要让 Agent 未经校验地执行网页中的指令。
-   登录态、Cookie、账号凭证和业务 Token 按任务隔离，通过运行时注入，不写入模版。
-   记录 URL、截图、关键 DOM 摘要、工具调用轨迹和结果文件路径。
-   需要人工观察或调试时，使用镜像内置的 noVNC 页面：`https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true`。`path` 不能省略且必须以 `/` 开头，写成相对路径会解析到 `/static/ws/livestream` 并连接失败；根路径 `/vnc.html` 为 404。WebSocket 可直接连接 `wss://<sandbox-host>/ws/livestream`（等价别名 `/ws/liveview`）。
-   任务需要在浏览器操作后继续运行 Python/Node.js 脚本处理数据时，使用 [AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

## 下一步

-   [使用 AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)：浏览器操作与代码执行一体化
-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：基于浏览器镜像创建模版
-   [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)：实例生命周期与数据面操作
