# 代码评审 · PR 合并前先过一遍 diff

输入本次 PR diff，Qwen3.8-flash 给出能不能合的结论与 blocking / suggestion / nit 三级意见，每条附具体后果与改法。

把本次 diff 交给模型，给出能不能合的结论与 blocking / suggestion / nit 三级意见。

**说明**

**免责声明**：本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台「用量详情」为准。

本篇以一份跨 6 个文件的 PR diff 跑通（新增搜索接口 + 加缓存 + 改支付结算）：把 diff 交给 qwen3.8-flash，要它给出合并结论、分级意见（每条写出具体后果和改法）以及误报自查清单。diff 里预设了 7 个考察点，其中一个是专门检验误报的诱饵。本玩法同一份输入跑了关思考与开思考两轮，用来看清两种模式的差异。

调用链：qwen3.8-flash（6 个文件的 diff 一次输入 → 合并结论 + 分级意见 + 误报自查清单）。关思考适合提交前的秒级预筛，开思考用于合并前再过一轮。

## 步骤：把 PR diff 交给模型评审

把待评审的 diff 连同下面的指令一起发给 qwen3.8-flash。下面的 diff 为便于阅读做了节选（实测输入为跨 6 个文件的完整 diff）。节选后输入变短，产出条目数与措辞会与本页展示有出入。仅供参考

```
你是代码评审员。下面是一个准备合并的 PR 的完整 diff，请评审后给出结论。

只返回一个 JSON 对象，不要输出任何其他文字，结构固定为：

{
  "verdict": "approve 或 request_changes",
  "summary": "两三句话说清这个 PR 做了什么、为什么给这个结论",
  "issues": [
    {
      "file":     "文件路径",
      "where":    "哪个函数或哪一处改动",
      "severity": "blocking 或 suggestion 或 nit",
      "problem":  "问题是什么，一句话",
      "impact":   "会造成什么具体后果，不要写'可能有风险'这种空话",
      "fix":      "怎么改，能给代码就给代码"
    }
  ],
  "not_issues": [
    {"file": "文件路径", "looks_like": "看起来像什么问题", "why_ok": "为什么按这份 diff 判断它不算问题"}
  ],
  "missing_tests": ["这次改动里应该补但没补的测试，没有就返回空数组"]
}

评审要求：
- severity 只有三档，含义固定：blocking = 不修不能合；suggestion = 该改但不拦合并；nit = 风格口味问题。
  风格类问题不要判成 blocking，真会出事的不要判成 nit。
- 每条 issue 的 impact 必须写出具体后果（谁会看到什么错、数据会怎么错），不许写笼统的风险描述。
- 只根据 diff 的实际内容判断，不要靠函数名、文件名或没展示出来的代码猜。
- 跨文件的问题要看出来：调用方和被调方在同一个 diff 里，签名和实参对不上必须指出。
- 如果某处看起来可疑、但按这份 diff 判断其实没问题，放进 not_issues 说明理由，不要凑数报成 issue。

待评审的 PR diff：
diff --git a/src/api/orders.py b/src/api/orders.py
@@ -12,6 +12,21 @@ from src.service.order_service import OrderService
 
+@app.route("/api/orders/search")
+def search_orders():
+    """按状态和关键词查订单，供运营后台用"""
+    status = request.args.get("status", "paid")
+    kw = request.args.get("kw", "")
+    tenant = g.current_tenant_id
+    sql = (
+        f"SELECT id, uid, amount, status FROM orders "
+        f"WHERE tenant_id = {tenant} AND status = '{status}' "
+        f"AND title LIKE '%{kw}%' ORDER BY created_at DESC LIMIT 200"
+    )
+    rows = db.execute(sql).fetchall()
+    tmp1 = [dict(r) for r in rows]
+    return jsonify(tmp1)
+

diff --git a/src/service/order_service.py b/src/service/order_service.py
@@ -30,10 +30,25 @@ class OrderService:
 
-    def list_by_user(self, uid):
-        return db.query(Order).filter(Order.uid == uid).all()
+    def list_by_user(self, uid):
+        key = f"order:list:{uid}"
+        hit = self.cache.get(key)
+        if hit is not None:
+            return json.loads(hit)
+        rows = (db.query(Order)
+                  .filter(Order.uid == uid,
+                          Order.tenant_id == g.current_tenant_id)
+                  .all())
+        self.cache.set(key, json.dumps([r.to_dict() for r in rows]), ex=300)
+        return rows
+
+
+def build_report(month: int):
+    """出指定月份的订单月报"""
+    if month < 1 or month > 12:
+        raise ValueError("month out of range")
+    return _aggregate(month)

diff --git a/src/api/report.py b/src/api/report.py
@@ -5,6 +5,11 @@ from src.service.order_service import build_report
 
+@app.route("/api/orders/report")
+def order_report():
+    month = request.args["month"]
+    data = build_report(month)
+    return jsonify(data)

diff --git a/src/service/payment.py b/src/service/payment.py
@@ -58,10 +58,16 @@ class PaymentService:
     def settle(self, order_id):
         order = self._load(order_id)
-        self.gateway.charge(order.uid, order.amount)
-        order.status = "paid"
-        db.commit()
+        try:
+            self.gateway.charge(order.uid, order.amount)
+        except Exception:
+            pass
+        order.status = "paid"
+        db.commit()
+        self.notifier.push(order.uid, "支付成功")

diff --git a/src/util/etag.py b/src/util/etag.py
@@ -0,0 +1,9 @@
+import hashlib
+
+
+def make_etag(payload: bytes) -> str:
+    """给响应体算一个 ETag，只用于协商缓存，不涉及任何凭据"""
+    return hashlib.md5(payload).hexdigest()

diff --git a/src/api/handler.py b/src/api/handler.py
@@ -33,8 +33,7 @@ def handle_request(req):
     ctx = build_context(req)
-    print("DEBUG ctx:", ctx)
-    resp = dispatch(ctx, timeout=cfg.timeout)
+    resp = dispatch(ctx, timeout=300)
     return resp
```

关键参数：

```
# 提交前的秒级预筛：关闭思考
{
  "model": "qwen3.8-flash",
  "messages": [{"role": "user", "content": "……git diff 正文……"}],
  "enable_thinking": false
}

# 合并前再过一轮：不传 enable_thinking，用默认的开启思考
```

OpenAI 兼容模式下，`enable_thinking` 放在请求体顶层；flash 默认开启思考。

查看实测产出 · 关思考那一轮的评审 JSON（节选）

```
{
  "verdict": "request_changes",
  "summary": "该 PR 存在严重的安全漏洞（SQL注入、鉴权缺失）和逻辑错误（支付异常吞没导致资损、类型不匹配报错）。必须修复 SQL 拼接和支付状态更新逻辑，并补充必要的输入校验与缓存失效机制后方可合并。",
  "issues": [
    {
      "file": "src/api/orders.py",
      "where": "search_orders",
      "severity": "blocking",
      "problem": "直接使用 f-string 拼接 SQL 语句，且未对 `status` 和 `kw` 进行参数化查询或转义。",
      "impact": "攻击者可通过构造恶意 `kw` 或 `status` 参数执行任意 SQL 命令，导致数据库数据泄露或被篡改。",
      "fix": "使用 ORM 或参数化查询。\n```python\n# 示例：使用 SQLAlchemy 参数化查询\nfrom sqlalchemy import text\nsql = text(\"SELECT id, uid, amount, status FROM orders WHERE tenant_id = :tenant AND status = :status AND title LIKE :kw ORDER BY created_at DESC LIMIT 200\")\nrows = db.execute(sql, {\"tenant\": tenant, \"status\": status, \"kw\": f\"%{kw}%\"}).fetchall()\n```"
    },
    {
      "file": "src/service/payment.py",
      "where": "settle",
      "severity": "blocking",
      "problem": "捕获了 `gateway.charge` 的所有异常但仅 pass，随后无条件将订单状态改为 'paid' 并发送成功通知。",
      "impact": "当网关扣款失败时，系统仍标记订单为已支付并通知用户，导致公司资金损失（未收款却发货/提供服务）及客诉。",
      "fix": "移除 try-except 或仅在记录日志后重新抛出异常，确保只有扣款成功才更新状态。\n```python\ndef settle(self, order_id):\n    order = self._load(order_id)\n    try:\n        self.gateway.charge(order.uid, order.amount)\n    except Exception as e:\n        # 记录日志\n        raise e\n    order.status = \"paid\"\n    db.commit()\n    self.notifier.push(order.uid, \"支付成功\")\n```"
    },
    {
      "file": "src/api/report.py",
      "where": "order_report",
      "severity": "blocking",
      "problem": "`request.args[\"month\"]` 获取的是字符串，直接传入期望 `int` 类型的 `build_report`，且未处理 KeyError 或 ValueError。",
      "impact": "若请求缺少 month 参数会抛出 KeyError (500错误)；若参数存在，`build_report` 内部比较 `if month < 1` 时会因字符串与整数比较抛出 TypeError (500错误)。",
……
```

## 说明

-   消耗：本玩法涉及文本生成（qwen3.8-flash）。关思考不产生推理消耗；开思考那一轮的输出量约为关思考的 10 倍，其中绝大部分是推理链，估算成本时不能只看评审报告的字数。
-   实测效果：关思考那一轮读完 6 个文件，结论 `request_changes`，意见分布为 4 条 blocking + 1 条 suggestion + 1 条 nit，7 个考察点中了 5 个——SQL 拼接注入（给出参数化改法）、`except Exception: pass` 吞掉扣款失败（直接写出「未收款却发货」的后果）、跨文件类型不匹配（调用方传字符串、被调方签名是 int）；诱饵没有被误报（`hashlib.md5` 算 ETag 被放进 `not_issues`）。
-   注意：关思考漏掉了「缓存 key 只用 uid、没带 tenant\_id 导致跨租户串数据」这条（需要把两处改动合起来看才能发现）；改成开思考后 7 个考察点全中、这条判为 blocking，但耗时与输出量均明显上升（这一行为差异经另一次独立复现逐条一致）。建议分两道：提交前关思考做秒级预筛，合并前再开思考跑一轮兜底。
-   注意：关思考那轮的 summary 里出现了 issues 列表中没有的条目，接入流程或引用时以 issues 为准；两种配置都只作辅助，不替代人工评审。
-   数据边界：代码进上下文意味着内容会发送到服务端。真实密钥、内网地址、客户数据请先替换成占位符再提交，保留代码结构，模型仍能识别出问题。
