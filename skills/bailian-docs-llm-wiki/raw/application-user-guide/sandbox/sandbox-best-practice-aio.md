# 使用 AIO Sandbox

面向“浏览器自动化 + 代码执行 + 文件处理”连续任务的最佳实践：基于全能型镜像创建模版，在同一沙箱中完成网页访问、截图、下载、数据清洗与结果导出。

AIO Sandbox 面向“浏览器自动化 + 代码执行 + 文件处理”连续发生的 Agent 任务。推荐基于全能型镜像（`all-in-one`）创建模版：3000 端口提供 browser 服务，5000 端口提供 Code Interpreter/envd 服务。Agent 可以在同一个隔离环境中完成网页访问、截图、下载、数据清洗、代码计算和结果导出。

如果任务只需要访问网页、点击按钮、截图或下载文件，优先使用 [Browser Use Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)；只有浏览器产物需要立即交给 Python/Node.js 继续处理时，才选择 AIO Sandbox。

**警告**沙箱公网 URL 应视为访问凭证：未设置应用层鉴权时，持有 URL 的人可完全控制沙箱内浏览器（含已登录态与 Cookie）。请勿公开分享，也不要写入日志或前端代码。

## 适用场景

**场景**

**说明**

网页采集后分析

通过浏览器访问动态页面，保存 HTML、截图或下载文件，再用 Python 清洗、汇总和导出

自动化测试报告

运行浏览器 E2E 测试后，在同一沙箱中分析日志、截图和测试结果

内容生产 Agent

生成网页截图、PDF、表格、JSON 和归档文件

多工具 Agent

在同一会话中组合浏览器、终端命令、Code Interpreter 和文件 API

## 推荐流程

1.  基于全能型镜像（`all-in-one`）创建模版并获取 `templateCode`，详见[模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)。
2.  使用模版创建沙箱，并设置足够的超时时间。浏览器冷启动、页面加载和代码执行会共同消耗时间。
3.  通过 `sandbox.getHost(3000)` 获取 browser 服务公网 host。
4.  轮询 `/health`，确认 browser 服务已经就绪。
5.  通过 CDP 端点连接 Playwright 或 Puppeteer，执行网页访问、交互、截图和下载。
6.  将浏览器产物写入沙箱文件系统，再通过 Code Interpreter 或命令继续处理。
7.  下载结果文件，记录 URL、动作摘要、截图路径、脚本版本和输出结果。
8.  任务结束后销毁沙箱，清理临时凭证和中间文件。

## 准备本地环境

以下示例使用 Node.js 连接沙箱中的浏览器，并在同一沙箱中执行 Python 代码。业务侧只需要安装 SDK 和 Playwright Core，浏览器运行在沙箱内。

```
{
  "name": "aio-sandbox-demo",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@e2b/code-interpreter": "2.6.1",
    "e2b": "2.31.0",
    "playwright-core": "^1.49.0"
  },
  "devDependencies": {
    "tsx": "^4.23.0",
    "typescript": "^6.0.3"
  }
}
```

**说明**`e2b` 与 `@e2b/code-interpreter` 固定为示例验证版本（2.31.0 / 2.6.1），更高版本的 SDK 创建实例时返回 405。

## 示例代码

示例流程：

1.  创建沙箱。
2.  等待 browser 服务 `/health` 返回 200。
3.  通过 CDP 连接云端浏览器，访问 `https://example.com`，并将截图写入沙箱任务目录。
4.  使用 Code Interpreter 读取浏览器产物，生成结构化摘要。

```
import { Sandbox } from "@e2b/code-interpreter";
import { chromium } from "playwright-core";

const ALIYUN_UID = "your aliyunUid";
const BAILIAN_API_KEY = "sk-...";
const BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox";
const TEMPLATE = "你的模版 code";

const BROWSER_PORT = 3000;
const TARGET_URL = "https://example.com";
const TASK_DIR = "/tmp/aio-task";
const SCREENSHOT_PATH = `${TASK_DIR}/page.png`;

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

async function collectPage(cdpUrl) {
  const browser = await chromium.connectOverCDP(cdpUrl);
  const contexts = browser.contexts();
  const context = contexts.length ? contexts[0] : await browser.newContext();
  const page = await context.newPage();

  try {
    await page.goto(TARGET_URL, {
      waitUntil: "domcontentloaded",
      timeout: 30_000,
    });

    const result = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      textLength: document.body.innerText.length,
    }));

    const screenshot = await page.screenshot({ fullPage: true });
    return { result, screenshot };
  } finally {
    await page.close();
    await browser.close();
  }
}

let sandbox;

try {
  sandbox = await Sandbox.create(TEMPLATE, {
    apiUrl: BASE_URL,
    apiKey: `e2b_${ALIYUN_UID}`,
    apiHeaders: { Authorization: `Bearer ${BAILIAN_API_KEY}` },
    timeoutMs: 900_000,
    secure: true,
  });

  const host = sandbox.getHost(BROWSER_PORT);
  const cdpUrl = `wss://${host}/ws/automation`;

  await waitUntilHealthy(sandbox, host);

  await sandbox.files.makeDir(TASK_DIR);
  const { result: pageResult, screenshot } = await collectPage(cdpUrl);
  await sandbox.files.write(SCREENSHOT_PATH, toArrayBuffer(screenshot));

  const execution = await sandbox.runCode(`
import json
from pathlib import Path

page = ${JSON.stringify(JSON.stringify(pageResult))}
data = json.loads(page)
summary = {
    "status": "ok",
    "source": "aio-sandbox",
    "title": data["title"],
    "url": data["url"],
    "text_length": data["textLength"],
    "artifacts": [str(Path("${SCREENSHOT_PATH}"))],
}
print(json.dumps(summary, ensure_ascii=False))
`);

  console.log(execution.logs.stdout);
} finally {
  if (sandbox) {
    await sandbox.kill();
  }
}
```

## 接入建议

-   使用固定的任务目录，例如 `/tmp/aio-task/<task-id>`，把截图、HTML、下载文件、脚本和结果文件放在同一目录。
-   浏览器阶段和代码阶段分别记录输入、输出、日志和错误。排查问题时先确认是页面操作失败，还是后续脚本处理失败。
-   对下载文件先做类型、大小和路径校验，再交给代码阶段处理。
-   网页内容和下载文件都可能携带 prompt injection，不要把网页文本直接当作系统指令或高权限工具指令。
-   浏览器账号、Cookie、模型 Key 和业务凭证通过运行时注入，不写入模版镜像。
-   设置最大页面数、最大下载文件大小、命令超时和沙箱生命周期，避免 Agent 无限制爬取或计算。
-   需要实时观察浏览器时，使用镜像内置的 noVNC 页面：`https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true`。`path` 不能省略且必须以 `/` 开头，写成相对路径会解析到 `/static/ws/livestream` 并连接失败；根路径 `/vnc.html` 为 404。WebSocket 可直接连接 `wss://<sandbox-host>/ws/livestream`（等价别名 `/ws/liveview`）。

## 下一步

-   [使用 Browser Use Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)：纯网页自动化类任务的最佳实践
-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：基于全能型镜像创建模版
-   [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)：实例生命周期与数据面操作
