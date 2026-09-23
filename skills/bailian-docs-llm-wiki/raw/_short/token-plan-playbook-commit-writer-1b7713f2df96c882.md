# 提交信息 · 一上午的改动自动拆 commit

输入未提交的 git diff，Qwen3.8-flash 自动拆成多条 commit，写出符合 Conventional Commits 的标题正文并标注破坏性改动。

把未提交的多文件 diff 交给模型，让它判断该拆几条 commit、每条带哪些文件、有没有破坏调用方。

**说明**

**免责声明**：本页展示内容均为 AI 模型生成，仅供参考，不构成任何效果承诺；实际产出效果与 Credits 消耗以控制台「用量详情」为准。

本篇以一份混了三类不相关改动的多文件 diff 跑通（修 bug + 加功能 + 顺手清理）：把 diff 交给 qwen3.8-flash，它自行判断拆分粒度，为每条 commit 写出符合 Conventional Commits 的标题与正文，标注是否破坏调用方，并给出 PR 标题与提交前提醒。diff 里预设了 5 个陷阱，用来检验它是读 diff 还是靠函数名猜。

调用链：qwen3.8-flash（未提交的 diff 一次输入 → commit 列表 + PR 标题 + 提交前提醒）。关闭思考模式，输入短、输出更短。

## 步骤：把 diff 交给模型拆分

把 `git diff` 的内容连同下面的指令一起发给 qwen3.8-flash。写 commit 是一天要跑好几次的动作，同样建议关闭思考。下面的 diff 为便于阅读做了节选：

```
你是 Git 提交助手。下面是我工作区里攒了一上午、还没提交的改动。
请判断这些改动该拆成几个 commit，并为每个 commit 写好提交信息。

只返回一个 JSON 对象，不要输出任何其他文字，结构固定为：

{
  "commits": [
    {
      "subject":  "符合 Conventional Commits 的标题，格式 type(scope): 描述，不超过 50 个字符",
      "body":     "说明这么改的原因和影响，两三句话；没什么可说的就填空字符串",
      "files":    ["属于这个 commit 的文件路径"],
      "breaking": true 或 false
    }
  ],
  "pr_title": "如果这批改动一起发一个 PR，PR 标题写什么",
  "notes": ["提交前值得提醒我的事，没有就返回空数组"]
}

要求：
- 不相关的改动必须拆开，不要糊成一条。相关的改动要合在一起，也不要拆得过碎。
- subject 写清楚改了什么行为，不要写"更新代码""修改若干文件"这种没有信息量的话。
- body 说清楚为什么这么改、影响到谁，不要把 diff 逐行复述一遍。
- 如果某个改动会破坏调用方（函数签名变了、返回值变了、行为不兼容），
  breaking 置为 true，并在 body 里点明调用方要怎么改。
- 只根据 diff 的实际内容判断，不要靠函数名或文件名猜。

待提交的改动：
diff --git a/src/service/user_service.py b/src/service/user_service.py
@@ -45,7 +45,10 @@ class UserService:
     def get_profile(self, uid):
         raw = self.cache.get(uid)
-        return json.loads(raw)
+        if raw is None:
+            return None
+        return json.loads(raw)
 
@@ -78,9 +81,9 @@ class UserService:
-    def validateCache(self, uid):
-        ts = self.cache.ttl(uid)
-        return ts > 0
+    def validateCache(self, uid):
+        ts = self.cache.ttl(uid)
+        # 原来只看 ttl 是否为正，跨天的键会被判为有效
+        return ts > 0 and (time.time() - self.cache.mtime(uid)) < 86400

diff --git a/src/api/export.py b/src/api/export.py
@@ -0,0 +1,24 @@
+import csv
+from io import StringIO
+
+@app.route("/api/users/export")
+def export_users():
+    """按筛选条件导出用户列表为 CSV"""
+    rows = UserService().query(request.args)
+    buf = StringIO()
+    w = csv.writer(buf)
+    w.writerow(["uid", "name", "created_at", "status"])
+    for r in rows:
+        w.writerow([r.uid, r.name, r.created_at, r.status])
+    # TODO: 后面补测试
+    return Response(buf.getvalue(), mimetype="text/csv")

diff --git a/src/service/exporter.py b/src/service/exporter.py
@@ -12,8 +12,8 @@ class UserExporter:
-    def export(self, rows, encoding, with_header):
-        out = self._render(rows, encoding, with_header)
+    def export(self, rows, with_header):
+        out = self._render(rows, "utf-8", with_header)
         return out

diff --git a/src/api/handler.py b/src/api/handler.py
@@ -33,7 +33,6 @@ def handle_request(req):
     ctx = build_context(req)
-    print("DEBUG ctx:", ctx)
     return dispatch(ctx)

diff --git a/README.md b/README.md
@@ -8,7 +8,7 @@
-本项目依赖 Python 3.9 以上版本，安转前请先创建虚拟环境。
+本项目依赖 Python 3.9 以上版本，安装前请先创建虚拟环境。

diff --git a/requirements.txt b/requirements.txt
@@ -3,4 +3,4 @@ flask==3.0.0
-redis==4.5.1
+redis==5.0.1
 requests==2.31.0
```

关键参数：

```
{
  "model": "qwen3.8-flash",
  "messages": [{"role": "user", "content": "……git diff 正文……"}],
  "enable_thinking": false
}
```

OpenAI 兼容模式下，`enable_thinking` 放在请求体顶层。

查看实测产出 · 5 条 commit + PR 标题 + 提交前提醒（节选）

```
{
  "commits": [
    {
      "subject": "fix(service): handle cache miss and improve TTL validation",
      "body": "修复 get_profile 在缓存未命中时因解析 None 导致的崩溃，返回 None。修正 validateCache 逻辑，增加 mtime 检查以防止跨天键被误判为有效。",
      "files": [
        "src/service/user_service.py"
      ],
      "breaking": false
    },
    {
      "subject": "feat(api): add user CSV export endpoint",
      "body": "新增 /api/users/export 接口支持按条件导出用户数据为 CSV。该功能目前缺少测试覆盖，需后续补充。",
      "files": [
        "src/api/export.py"
      ],
      "breaking": false
    },
    {
      "subject": "refactor(exporter): remove encoding param from export method",
      "body": "简化 UserExporter.export 签名，内部固定使用 UTF-8 编码。调用方若显式传递了 encoding 参数，需移除该参数以适配新签名。",
      "files": [
        "src/service/exporter.py"
      ],
      "breaking": true
    },
    {
      "subject": "chore: remove debug print and fix README typo",
      "body": "清理 handler.py 中的调试输出语句，避免生产环境日志污染。修正 README.md 中“安装”一词的拼写错误。",
      "files": [
        "src/api/handler.py",
        "README.md"
      ],
      "breaking": false
    },
    {
      "subject": "build: upgrade redis client to v5.0.1",
      "body": "将 redis 依赖从 4.5.1 升级至 5.0.1。请确认现有 Redis 连接配置与 v5 客户端兼容，特别是超时和重试相关设置。",
      "files": [
        "requirements.txt"
      ],
      "breaking": false
    }
  ],
  "pr_title": "Fix cache handling, add CSV export, refactor exporter API, and update deps",
  "notes": [
    "UserExporter.export 方法签名变更属于破坏性修改，合并前请全局搜索并更新所有调用点，移除 encoding 参数。",
    "Redis 大版本升级（4.x -> 5.x）可能引入行为差异，建议在预发环境重点验证连接稳定性及命令执行结果。",
    "新增的 CSV 导出接口尚未包含单元测试，建议尽快补充以保障数据安全性和格式正确性。"
  ]
}
```

## 说明

-   消耗：本玩法涉及文本生成（qwen3.8-flash，关闭思考）。输入与输出两边都不长，是本批 7 个玩法里耗时与消耗最低的一个。
-   实测效果：6 个文件的改动被拆成 5 条 commit、文件归属全部正确。预设的 5 个陷阱都处理正确，典型的三个：`UserExporter.export()` 删参数被判为 breaking 并写明调用方要怎么改；函数名叫 `validateCache` 但实际改的是过期时间计算，它读的是 diff 不是函数名；diff 里的 `# TODO: 后面补测试` 没被抄进提交信息，而是升级成了提交前提醒。
-   注意：指令要求 subject 不超过 50 个字符，5 条里有 2 条超出，字数这类硬约束建议在提交钩子里再卡一道。
-   注意：本页展示的 diff 是节选，照页面抄着跑时输入长度与实测那一轮会有出入，拆分结果也可能随之变化。
