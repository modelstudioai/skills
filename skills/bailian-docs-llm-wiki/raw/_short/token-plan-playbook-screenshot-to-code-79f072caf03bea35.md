# 截图变代码 · 数据看板照结构还原

上传数据看板截图，Qwen3.8-flash 视觉理解照结构还原，图表用纯 CSS 绘制、数字照抄，产出零外部依赖的单文件 HTML。

上传一张数据看板截图，模型照结构还原成单文件网页，图表用纯 CSS 画、数字一个不改。

**说明**

**免责声明**：本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台「用量详情」为准。

本篇以一张自建的电商运营日报看板跑通：截图里有 4 个 KPI 卡、近 7 日 GMV 柱状图、渠道占比条形图和 TOP5 商品表，画面上一共 64 个数字。要求 qwen3.8-flash 把数字全部照抄、图表只用纯 CSS 画（不引图表库）、柱子高度按数值等比，产出可直接在浏览器打开的单文件 HTML。素材由本项目自建、每个数字已知，所以产出页面与原图可以并排逐格核对。

调用链：qwen3.8-flash（看板截图 base64 传入 → 单文件 HTML）。视觉理解，产出零外部依赖。

## 实测产出

两轮指令后的还原页面：

![实测产出 · 模型还原的页面](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fbc.png)

_实测产出 · 模型还原的页面_

可点击试用：[运营日报看板 · 还原产出页](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/files/6a4b3c2d1e0f9fc0.html)

## 示例输入

![示例输入 · 喂给模型的完整看板截图（本项目自建素材，非网图）](https://g-adoc.alcasset.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fbd.png)

_示例输入 · 喂给模型的完整看板截图（本项目自建素材，非网图）_

## 步骤一：上传截图并给出还原要求

把看板截图与下面的指令一起发给 qwen3.8-flash：

```
<image_url: base64 149 KB>
把这张运营看板截图还原成 HTML/CSS 代码。要求：
① 所有数字、商品名、SKU 编号、日期照抄截图，不许编；
② 柱状图和横向条形图用纯 CSS 画，柱子高度和条形长度要与截图里的数值成比例，不许引入 ECharts 等任何外部依赖；
③ KPI 卡的环比涨跌沿用截图配色（涨红、跌绿），库存状态三色标签的语义配色要对；
④ 布局用 Flex/Grid，响应式；
⑤ 输出单个可直接在浏览器打开的完整 HTML 文件。
```

## 步骤二：把产出贴回去，补上按钮交互

第一轮只要了“还原结构”，所以产出页面右上角的「导出报表」点不动。把上一轮的 HTML 原文贴回去，只追加交互要求（并把“其余一律不许改”写进指令）：

```
这是你上一轮把运营看板截图还原出来的完整 HTML，现在只补一件事。

问题：右上角那个「导出报表」按钮点下去没有任何反应。

要求：
① 给「导出报表」加上可用的交互，纯前端 mock，不许引入任何外部依赖或联网资源；
② 点击后把「热销商品 TOP 5」表格的表头与全部行导成 CSV 触发浏览器下载，
   文件名带上页面顶部那个数据日期；CSV 要带 UTF-8 BOM，避免 Excel 打开中文乱码；
③ 点击后必须同时给一个页面内可见的状态反馈（例如按钮短暂变为进行中、
   再弹出一个两三秒后自动消失的成功提示），因为在某些环境里浏览器下载可能被拦，
   只要提示还在，用户就能确认按钮是响应了的；
④ 除实现上述交互必需的新增代码外，页面里所有数字、文案、标签、结构层级、
   配色与间距一律不许改动，一个字都不要动；
⑤ 仍然只输出一个可以直接在浏览器打开的完整 HTML 文件。

<随指令一起贴回的上一轮产出：247 行 HTML 原文>
```

查看实测产出 · 补上导出交互后的完整单文件 HTML（338 行，可直接打开）

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>运营日报</title>
<style>
  :root{
    --bg:#eef0f4;
    --card:#ffffff;
    --ink:#1f2329;
    --muted:#8a919f;
    --line:#eef0f3;
    --blue:#2563eb;
    --blue-soft:#c7d6f7;
    --red:#e02f2f;
    --green:#16a34a;
    --orange:#d9820a;
    --radius:12px;
    --shadow:0 1px 3px rgba(30,40,70,.06),0 4px 14px rgba(30,40,70,.04);
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    background:var(--bg);
    color:var(--ink);
    padding:28px 24px;
    -webkit-font-smoothing:antialiased;
  }
  .wrap{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:20px;}

  /* ---------- 顶栏 ---------- */
  .topbar{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;}
  .topbar-title{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;}
  .topbar-title h1{font-size:22px;font-weight:700;letter-spacing:.5px;}
  .asof{font-size:13px;color:var(--muted);}
  .topbar-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
  .pill{
    background:var(--card);border:1px solid var(--line);border-radius:8px;
    padding:8px 14px;font-size:13px;color:var(--muted);box-shadow:var(--shadow);
  }
  .pill b{color:var(--ink);font-weight:600;}
  .btn{
    background:var(--blue);color:#fff;border:none;border-radius:8px;
    padding:9px 18px;font-size:13px;font-weight:600;cursor:pointer;
    box-shadow:0 2px 6px rgba(37,99,235,.35);
  }
  .btn:hover{background:#1d55d4;}

  /* ---------- 卡片通用 ---------- */
  .card{background:var(--card);border-radius:var(--radius);box-shadow:var(--shadow);padding:22px 24px;}
  .panel-title{font-size:16px;font-weight:700;margin-bottom:4px;}
  .panel-sub{font-size:12px;color:var(--muted);margin-bottom:18px;}
  .panel-sub .sep{margin:0 8px;}

  /* ---------- KPI ---------- */
  .kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}
  .kpi-label{font-size:13px;color:var(--muted);margin-bottom:12px;}
  .kpi-value{font-size:30px;font-weight:800;letter-spacing:.5px;line-height:1.1;}
  .kpi-value span{font-size:14px;font-weight:600;color:var(--ink);margin-left:2px;}
  .kpi-foot{margin-top:12px;font-size:12px;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap;}
  .delta{font-weight:700;}
  .delta.up{color:var(--red);}
  .delta.down{color:var(--green);}

  /* ---------- 中部两栏 ---------- */
  .mid-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:20px;}

  /* 柱状图 */
  .bars{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;height:212px;padding-top:8px;}
  .bar-col{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;gap:8px;min-width:0;}
  .bar-val{font-size:12px;color:var(--muted);}
  .bar{width:56%;max-width:44px;min-width:20px;background:var(--blue-soft);border-radius:4px 4px 0 0;}
  .bar.hot{background:var(--blue);}
  .bar-day{font-size:12px;color:var(--muted);}

  /* 横向条形图 */
  .hbars{display:flex;flex-direction:column;gap:18px;padding-top:6px;}
  .hbar{display:grid;grid-template-columns:52px 1fr 48px;align-items:center;gap:12px;}
  .hbar-name{font-size:13px;color:var(--ink);}
  .hbar-track{height:8px;background:#eef1f6;border-radius:99px;overflow:hidden;}
  .hbar-fill{height:100%;background:var(--blue);border-radius:99px;}
  .hbar-val{font-size:13px;font-weight:700;text-align:right;}

  /* ---------- 表格 ---------- */
  .table-scroll{overflow-x:auto;}
  table{width:100%;border-collapse:collapse;font-size:13px;min-width:720px;}
  thead th{
    text-align:left;color:var(--muted);font-weight:600;font-size:12px;
    background:#f7f8fa;padding:11px 12px;
  }
  thead th:first-child{border-radius:8px 0 0 8px;}
  thead th:last-child{border-radius:0 8px 8px 0;}
  tbody td{padding:15px 12px;border-bottom:1px solid var(--line);vertical-align:middle;}
  tbody tr:last-child td{border-bottom:none;}
  .num{text-align:right;font-variant-numeric:tabular-nums;}
  thead .num{text-align:right;}
  .tag{display:inline-block;padding:3px 10px;border-radius:6px;font-size:12px;font-weight:600;}
  .tag.ok{background:#e7f6ee;color:var(--green);}
  .tag.warn{background:#fdf3e0;color:var(--orange);}
  .tag.err{background:#fdeaea;color:var(--red);}

  /* ---------- 响应式 ---------- */
  @media (max-width:960px){
    .kpi-grid{grid-template-columns:repeat(2,1fr);}
    .mid-grid{grid-template-columns:1fr;}
  }
  @media (max-width:560px){
    body{padding:16px;}
    .kpi-grid{grid-template-columns:1fr;}
    .topbar{flex-direction:column;align-items:flex-start;}
    .bar{width:70%;}
  }
</style>
</head>
<body>
<div class="wrap">

  <!-- 顶栏 -->
  <header class="topbar">
    <div class="topbar-title">
      <h1>运营日报</h1>
      <span class="asof">数据截至 2026-08-26 24:00</span>
    </div>
    <div class="topbar-actions">
      <div class="pill">店铺：<b>旗舰店</b></div>
      <div class="pill">对比：<b>前一日</b></div>
      <button class="btn">导出报表</button>
    </div>
  </header>

  <!-- KPI 卡片 -->
  <section class="kpi-grid">
    <div class="card">
      <div class="kpi-label">成交金额 GMV</div>
      <div class="kpi-value">86.4<span>万</span></div>
      <div class="kpi-foot">
        <span>环比 <span class="delta up">↑ 12.3%</span></span>
        <span>昨日 76.9 万</span>
      </div>
    </div>
    <div class="card">
      <div class="kpi-label">订单量</div>
      <div class="kpi-value">4,182<span>单</span></div>
      <div class="kpi-foot">
        <span>环比 <span class="delta up">↑ 8.6%</span></span>
        <span>昨日 3,851 单</span>
      </div>
    </div>
    <div class="card">
      <div class="kpi-label">客单价</div>
      <div class="kpi-value">206.6<span>元</span></div>
      <div class="kpi-foot">
        <span>环比 <span class="delta up">↑ 3.4%</span></span>
        <span>昨日 199.8 元</span>
      </div>
    </div>
    <div class="card">
      <div class="kpi-label">退款率</div>
      <div class="kpi-value">2.7<span>%</span></div>
      <div class="kpi-foot">
        <span>环比 <span class="delta down">↓ 0.4pt</span></span>
        <span>昨日 3.1%</span>
      </div>
    </div>
  </section>

  <!-- 中部：趋势 + 渠道 -->
  <section class="mid-grid">
    <div class="card">
      <h2 class="panel-title">近 7 日 GMV 趋势</h2>
      <p class="panel-sub">单位：万元<span class="sep">·</span>周末两日显著高于工作日</p>
      <div class="bars">
        <div class="bar-col"><span class="bar-val">52.1</span><div class="bar" style="height:84px"></div><span class="bar-day">08-20</span></div>
        <div class="bar-col"><span class="bar-val">48.7</span><div class="bar" style="height:79px"></div><span class="bar-day">08-21</span></div>
        <div class="bar-col"><span class="bar-val">61.3</span><div class="bar" style="height:99px"></div><span class="bar-day">08-22</span></div>
        <div class="bar-col"><span class="bar-val">79.5</span><div class="bar" style="height:129px"></div><span class="bar-day">08-23</span></div>
        <div class="bar-col"><span class="bar-val">72.8</span><div class="bar" style="height:118px"></div><span class="bar-day">08-24</span></div>
        <div class="bar-col"><span class="bar-val">76.9</span><div class="bar" style="height:125px"></div><span class="bar-day">08-25</span></div>
        <div class="bar-col"><span class="bar-val">86.4</span><div class="bar hot" style="height:140px"></div><span class="bar-day">08-26</span></div>
      </div>
    </div>

    <div class="card">
      <h2 class="panel-title">渠道成交占比</h2>
      <p class="panel-sub">按 GMV 口径统计</p>
      <div class="hbars">
        <div class="hbar"><span class="hbar-name">直播间</span><div class="hbar-track"><div class="hbar-fill" style="width:42.1%"></div></div><span class="hbar-val">42.1%</span></div>
        <div class="hbar"><span class="hbar-name">搜索</span><div class="hbar-track"><div class="hbar-fill" style="width:26.8%"></div></div><span class="hbar-val">26.8%</span></div>
        <div class="hbar"><span class="hbar-name">推荐流</span><div class="hbar-track"><div class="hbar-fill" style="width:18.3%"></div></div><span class="hbar-val">18.3%</span></div>
        <div class="hbar"><span class="hbar-name">短视频</span><div class="hbar-track"><div class="hbar-fill" style="width:9.2%"></div></div><span class="hbar-val">9.2%</span></div>
        <div class="hbar"><span class="hbar-name">其他</span><div class="hbar-track"><div class="hbar-fill" style="width:3.6%"></div></div><span class="hbar-val">3.6%</span></div>
      </div>
    </div>
  </section>

  <!-- 热销商品表格 -->
  <section class="card">
    <h2 class="panel-title">热销商品 TOP 5</h2>
    <p class="panel-sub">按当日成交金额排序，库存状态取自 WMS 实时同步</p>
    <div class="table-scroll">
      <table>
        <thead>
          <tr>
            <th>排名</th>
            <th>商品名称</th>
            <th>SKU</th>
            <th class="num">成交金额</th>
            <th class="num">销量</th>
            <th class="num">库存</th>
            <th>库存状态</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>1</td><td>轻氧蓬松洗发水 500ml</td><td>SKU-88213</td>
            <td class="num">18.62 万</td><td class="num">1,204</td><td class="num">3,850</td>
            <td><span class="tag ok">充足</span></td>
          </tr>
          <tr>
            <td>2</td><td>控油头皮精华 120ml</td><td>SKU-88097</td>
            <td class="num">14.35 万</td><td class="num">726</td><td class="num">412</td>
            <td><span class="tag warn">预警</span></td>
          </tr>
          <tr>
            <td>3</td><td>氨基酸洁面慕斯 150ml</td><td>SKU-87566</td>
            <td class="num">11.08 万</td><td class="num">893</td><td class="num">2,166</td>
            <td><span class="tag ok">充足</span></td>
          </tr>
          <tr>
            <td>4</td><td>护发精油旅行套装</td><td>SKU-89402</td>
            <td class="num">9.74 万</td><td class="num">651</td><td class="num">0</td>
            <td><span class="tag err">缺货</span></td>
          </tr>
          <tr>
            <td>5</td><td>头皮按摩梳 木质款</td><td>SKU-86011</td>
            <td class="num">6.21 万</td><td class="num">1,038</td><td class="num">1,509</td>
            <td><span class="tag ok">充足</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

</div>

<script>
(function () {
  const btn = document.querySelector('.btn');
  const asof = document.querySelector('.asof');
  const table = document.querySelector('.table-scroll table');
  if (!btn || !asof || !table) return;

  const originalText = btn.textContent;
  let busy = false;

  function escapeCsv(value) {
    const text = String(value);
    return /[",\r\n]/.test(text) ? '"' + text.replace(/"/g, '""') + '"' : text;
  }

  function showToast(message) {
    const oldToast = document.getElementById('export-toast');
    if (oldToast && oldToast.parentNode) oldToast.parentNode.removeChild(oldToast);

    const toast = document.createElement('div');
    toast.id = 'export-toast';
    toast.setAttribute('role', 'status');
    toast.textContent = message;
    toast.style.cssText = 'position:fixed;right:24px;bottom:24px;z-index:9999;background:#16a34a;color:#ffffff;font-size:13px;font-weight:600;padding:10px 14px;border-radius:8px;box-shadow:0 1px 3px rgba(30,40,70,.06),0 4px 14px rgba(30,40,70,.04);opacity:0;transition:opacity .2s;pointer-events:none;';
    document.body.appendChild(toast);

    requestAnimationFrame(function () {
      toast.style.opacity = '1';
    });

    setTimeout(function () {
      toast.style.opacity = '0';
      setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 250);
    }, 2200);
  }

  btn.addEventListener('click', function () {
    if (busy) return;
    busy = true;

    btn.style.minWidth = btn.offsetWidth + 'px';
    btn.textContent = '导出中';

    setTimeout(function () {
      try {
        const dateMatch = asof.textContent.match(/(\d{4}-\d{2}-\d{2})/);
        const dataDate = dateMatch ? dateMatch[1] : new Date().toISOString().slice(0, 10);

        const headers = Array.from(table.querySelectorAll('thead th')).map(function (th) {
          return th.textContent.trim();
        });

        const rows = Array.from(table.querySelectorAll('tbody tr')).map(function (tr) {
          return Array.from(tr.children).map(function (td) {
            return td.textContent.trim();
          });
        });

        const csv = [headers].concat(rows).map(function (row) {
          return row.map(escapeCsv).join(',');
        }).join('\r\n');

        const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = '运营日报_热销商品TOP5_' + dataDate + '.csv';
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();

        setTimeout(function () {
          if (link.parentNode) link.parentNode.removeChild(link);
          URL.revokeObjectURL(url);
        }, 1000);

        showToast('导出成功，CSV 已开始下载');
      } catch (err) {
        showToast('导出失败，请重试');
      } finally {
        btn.textContent = originalText;
        btn.style.minWidth = '';
        busy = false;
      }
    }, 700);
  });
})();
</script>
</body>
</html>
```

## 说明

-   消耗：本玩法涉及视觉理解 + 文本生成（qwen3.8-flash）。截图本身会转成 image\_tokens 计入输入侧，图越大越清晰、输入消耗越高；产出是一份完整单文件 HTML，输出侧消耗高于纯文本问答属正常现象。
-   注意：布局用 Flex/Grid 重写，属于结构级还原、不是像素级复刻，配色与间距与原图有细微出入，要求高保真复刻的场景请以设计稿为准。
-   注意：截图还原前请先确认对该页面的设计与数据有使用权，本例素材为本项目自建。
