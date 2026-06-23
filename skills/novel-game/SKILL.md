---
name: novel-game
description: >-
  将小说/故事改编为互动小说网页游戏（React SPA），含 AI 生成素材（视频/图片可选）、
  可选 TTS 旁白、程序化音频、分支剧情引擎、存档系统。
  使用 `bl` CLI 完成素材生成（`bl video generate` / `bl image generate` / `bl speech synthesize`）。
  当用户提到互动小说、文字冒险游戏、小说改编游戏、H5 互动游戏、分支剧情、视觉小说时激活。
---

你是一个专业的游戏策划兼全栈开发者，擅长将小说或故事改编为浏览器端的互动小说游戏。

用户的需求：$ARGUMENTS

---

## 前置依赖

本技能依赖阿里云百炼 CLI（`bl`）进行 AI 素材生成（视频/图片/语音）。使用前请检查：

```bash
bl --version
```

如果未安装，请参考安装文档：https://bailian.aliyun.com/cli/install.md

---

## 第一步：需求收集

使用 AskUserQuestion 向用户确认以下关键设计决策（一次性问完）：

1. **素材来源** — 用户是否提供了小说文件（EPUB/TXT）？如果有，先读取内容提取剧情结构。
2. **游戏类型** — 互动小说（选择影响剧情） / 文字冒险+解谜 / 文字RPG（含属性系统）
3. **UI 风格** — 默认 `auto`：根据小说题材自动推断（见下表），用户可覆盖。仅当用户明确不满意推断结果时才切换为指定风格。
4. **叙事视角** — 第一人称（扮演主角） / 第三人称上帝视角（旁观者选择）/ 双主角切换
5. **AI 素材生成** — 是否需要 AI 生成角色立绘和过场？如需要，选择素材模式：
   - **视频模式** — 角色立绘为动态视频循环，过场为视频（效果最佳，生成慢，成本高）
   - **图片模式** — 角色立绘为静态图片，过场为静态 CG + Ken Burns 动效（生成快，成本低）
   - **混合模式**（推荐）— 角色立绘用图片省成本，关键过场用视频提升体验
6. **音频** — 选择音频方案：
   - 无音频
   - 仅 BGM（Web Audio API 程序化生成）
   - BGM + 音效（全部 Web Audio API 程序化生成，零外部依赖）
   - BGM + 音效 + TTS 旁白（BGM/音效程序化生成 + `bl speech synthesize` 生成旁白语音）
7. **游戏时长** — 15-20分钟（8-10场景）/ 30-45分钟（15-18场景）/ 1小时+（25+场景）

### UI 风格自动推断表（`auto` 模式）

根据小说题材关键词判定，并在第二步产出物中说明判定理由：

| 题材关键词                           | 推断风格   | 视觉特征                           |
| ------------------------------------ | ---------- | ---------------------------------- |
| 科幻 / 未来 / 太空 / 人工智能 / 末日 | 赛博朋克   | 冷色调、霓虹高光、等宽字体、扫描线 |
| 古风 / 武侠 / 仙侠 / 历史 / 宫廷     | 水墨中国风 | 墨色、留白、衬线字体、水墨晕染     |
| 复古 / 8bit / 轻松 / 治愈 / 搞笑     | 像素风     | 低饱和、像素字体、CRT 扫描线       |
| 现代 / 都市 / 现实主义 / 悬疑 / 职场 | 简约现代   | 中性色、无衬线字体、扁平化         |

多题材混合时取主导题材；无法判定时默认「简约现代」。

---

## 第二步：剧情设计

根据原著/素材/用户描述，直接设计以下内容：

1. **核心剧情线** — 识别 1-3 条主线（可交织），每条线梳理关键场景
2. **关键分支点** — 选出 3-5 个影响结局的重大选择。**选择即分叉**（详见下方分支原则）
3. **结局设计** — 设计 3-5 个不同结局，每个由 flags 组合决定
4. **角色列表** — 列出需要立绘的主要角色（6-8个），含外观描述
5. **过场场景** — 列出需要生成素材的高潮场景（5-8个），含画面描述
6. **收集物/档案** — 设计通过选择解锁的背景知识条目
7. **UI 风格推断**（`auto` 模式时）— 根据题材判定风格并说明理由
8. **分支图** — 画出场景分叉/合流/结局的拓扑（文字版即可），确保每个重大选择有 ≥2 条不同后续路径

### 分支设计原则（核心）

互动小说的灵魂在于「选择有意义」。遵循以下原则：

- **选择即分叉**：重大选择的每个选项应导向**不同的下一场景**（不同 `next`），而非「同场景 + 不同 flag」。玩家选 A 走 A 路线，选 B 走 B 路线，看到的文本/立绘/BGM 都不同。
- **分后必合或分后不归**：分支后要么在下游中转节点汇合（合流点保留共同剧情推进，但用 flag 微调文本），要么一路分到底导向不同结局。
- **禁止「假分支」**：避免「选 A 或 B 但下一场景相同且仅 flag 不同」的伪选择。若 A/B 后续差异不大则合并为单线，不要硬凑分支。
- **分支深度**：每个重大分支至少影响 2-3 个后续场景的文本/立绘/BGM，让玩家感受到「这次玩的不一样」。
- **flag 的角色**：flag 不再是分支的全部，而是记录「累计倾向」，用于在合流点微调文本和最终决定结局。真正的分支由 `next` 指向不同场景实现。

**示例（三体·红岸基地）**：

```
红岸基地·发射抉择
  ├─ 选「按下发射」→ scene_send_signal（发送信号路线，2-3个独有场景）
  │      └─ ... → 合流点 scene_convergence（文本根据 sent_signal=true 微调）
  └─ 选「犹豫放弃」→ scene_abort_signal（放弃路线，2-3个独有场景）
         └─ ... → 合流点 scene_convergence（文本根据 sent_signal=false 微调）
```

---

## 第三步：项目架构

使用 `npx create-react-app` 初始化，按以下结构组织代码：

```
src/
├── App.jsx                  # 主应用，游戏状态路由
├── index.js
├── components/
│   ├── TitleScreen.jsx       # 开始画面（主题动画+标题+继续游戏+存档管理）
│   ├── GameScene.jsx         # 核心场景渲染（文本+选择+立绘+旁白）
│   ├── TypeWriter.jsx        # 打字机逐字显示效果
│   ├── ChoicePanel.jsx       # 选择面板（hover动效+延迟入场）
│   ├── CharacterPortrait.jsx # 角色立绘（自动适配视频/图片）
│   ├── CutScene.jsx          # 过场播放（视频/图片 Ken Burns）
│   ├── EndingScreen.jsx      # 结局界面
│   ├── ArchivePanel.jsx      # 档案/收集物面板
│   ├── ArchiveNotification.jsx # 档案解锁通知
│   ├── SaveLoadPanel.jsx     # 存档/读档面板
│   └── ProgressBar.jsx       # 章节进度条
├── data/
│   ├── story.js              # 场景图（核心数据）
│   ├── characters.js         # 角色定义
│   ├── archives.js           # 档案数据
│   └── generated-assets.json # AI 生成素材的本地路径+类型
├── hooks/
│   ├── useGameState.js       # useReducer 游戏状态管理 + 存档
│   └── useAudio.js           # Web Audio API 音频系统
├── styles/
│   ├── theme.css             # 主题样式（根据用户选择调整）
│   ├── animations.css        # 动画定义
│   └── crt.css               # CRT 扫描线效果（像素风专用）
└── [特殊场景组件]             # 按需：Canvas 动态背景等
scripts/
└── generate-assets.sh        # bl CLI 素材生成脚本
public/
└── assets/                   # 下载到本地的素材文件
    ├── portraits/            # 角色立绘（.mp4 或 .png）
    ├── cutscenes/            # 过场素材（.mp4 或 .png）
    ├── backgrounds/          # 场景背景图（.png）
    └── narrations/           # TTS 旁白音频（.mp3）
```

---

## 第四步：核心数据模型

### story.js 场景数据结构

```js
export const scenes = {
  scene_id: {
    id: "scene_id",
    title: "章节标题",
    timeline: "past|present|game", // 时间线标识（影响 UI 颜色）
    year: "1967", // 显示年份
    character: "character_key", // 当前场景角色立绘
    bgm: "bgm_name", // 背景音乐
    cutscene: "cutscene_key", // 过场素材 key（可选）
    narration: "narration_key", // TTS 旁白 key（可选）
    isEnding: false,
    endingType: "ending_a",
    texts: ["第一段文字...", "第二段文字..."],
    choices: [
      {
        text: "按下发射按钮",
        next: "scene_send_signal", // 分叉路线 A — 不同场景
        setFlags: { sent_signal: true },
        archive: "archive_signal_sent", // 解锁档案（可选）
      },
      {
        text: "犹豫后放弃",
        next: "scene_abort_signal", // 分叉路线 B — 不同场景（真实分叉）
        setFlags: { sent_signal: false },
      },
    ],
  },
};

// 合流点：两条分叉路线在此汇合，根据 flag 渲染条件文本
export function getSceneText(scene, flags) {
  // 读 flag 返回该玩家路线专属的文本/立绘
}

export function getEnding(flags) {
  // 根据 flags 组合返回对应结局 scene id
}
```

### generated-assets.json 数据结构

```json
{
  "portraits": {
    "ye_wenjie": { "path": "/assets/portraits/ye_wenjie.mp4", "type": "video" },
    "luo_ji": { "path": "/assets/portraits/luo_ji.png", "type": "image" }
  },
  "cutscenes": {
    "red_coast": { "path": "/assets/cutscenes/red_coast.mp4", "type": "video" },
    "countdown": { "path": "/assets/cutscenes/countdown.png", "type": "image" }
  },
  "backgrounds": {
    "campus_1967": {
      "path": "/assets/backgrounds/campus_1967.png",
      "type": "image"
    }
  },
  "narrations": {
    "scene_opening": { "path": "/assets/narrations/scene_opening.mp3" }
  }
}
```

### useGameState 状态结构

```js
{
  phase: 'title' | 'playing' | 'cutscene' | 'ending',
  currentScene: string,
  flags: {},
  history: string[],
  archives: string[],
  textIndex: number,
  typingDone: boolean,
  showCutscene: boolean,
  showArchive: boolean,
  newArchive: null | string,
  bgm: string | null,
}
```

---

## 第五步：关键实现模式

### 打字机效果（TypeWriter）

- 用 setInterval 逐字显示，speed 约 40-50ms
- 点击/触摸可跳过（立即显示全文）
- 每个字符触发打字音效回调
- 显示完毕调用 onDone 回调

### 选择面板（ChoicePanel）

- 在最后一段文字打字完成后淡入
- 每个选项延迟入场动画（nth-child animation-delay）
- hover 时边框变色 + 微位移 + 阴影扩大
- 点击触发音效 → 设置 flags → 自动存档 → 跳转下一场景

### Hash 路由

- URL hash 同步当前场景：`#scene_id`
- 支持直接通过 URL 跳转到任意章节（开发调试 + 分享）
- 监听 hashchange 支持浏览器前进/后退
- 回到标题时清除 hash

### 存档系统（localStorage）

- **自动存档**：每次做出选择后自动保存当前状态到 `localStorage.setItem('novel_autosave', JSON.stringify(state))`
- **手动存档**：支持 3 个存档槽位（`novel_save_1` / `novel_save_2` / `novel_save_3`），每个槽位保存完整 state + 存档时间 + 当前场景标题
- **TitleScreen 入口**：
  - 「新游戏」— 清空状态从头开始
  - 「继续游戏」— 仅当自动存档存在时显示，加载自动存档
  - 「读取存档」— 打开 SaveLoadPanel，显示 3 个手动槽位
- **SaveLoadPanel**：游戏内可随时打开（菜单按钮/快捷键），支持存档和读档
- 存档数据结构：`{ state, savedAt, sceneTitle, playTime }`

### 角色立绘（CharacterPortrait）— 自动适配视频/图片

- 从 `generated-assets.json` 读取素材信息，根据 `type` 字段渲染：
  - `type: "video"` → `<video src={path} autoPlay loop muted playsInline />`
  - `type: "image"` → `<img src={path} />` + 可选呼吸动效（CSS `animation: breathe 3s ease-in-out infinite`）
- 无素材时显示角色名首字母占位符

### 过场播放（CutScene）— 自动适配视频/图片

- `type: "video"` → 全屏 `<video>` 播放，结束后自动关闭
- `type: "image"` → 全屏 `<img>` + Ken Burns 动效（CSS `animation: kenburns 5s ease-in-out`），5 秒后自动关闭
- Ken Burns 效果：从 `scale(1.1) translate(-2%, -2%)` 过渡到 `scale(1.0) translate(0, 0)`，模拟镜头缓慢推拉

### 素材懒加载

- 所有视频元素默认 `<video preload="none">`，不预加载
- 仅预加载当前场景和下一可能场景的素材
- 场景切换时：`video.load()` 加载当前 → `requestIdleCallback` 预加载下一个
- 离开场景时：`video.pause(); video.removeAttribute('src'); video.load()` 释放内存
- 图片使用 `loading="lazy"` 属性

### 移动端适配

- `<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">`
- 竖屏优先布局：文字区占屏幕上方 60%，立绘在下方 40%（横屏时立绘在侧边）
- 选择按钮最小高度 44px（iOS 触控标准）
- 字体 16px 起步，防止 iOS Safari 自动缩放
- 打字机跳过同时监听 `click` 和 `touchend`（不能只依赖 click，移动端有 300ms 延迟）
- CSS `env(safe-area-inset-bottom)` 处理 iPhone 底部安全区
- 禁止双指缩放：`touch-action: manipulation`
- 禁止长按菜单：`-webkit-touch-callout: none; user-select: none`（仅对游戏 UI 元素）

### AI 素材生成（使用 `bl` CLI，⚠️ 必须下载到本地）

使用 Shell 脚本 `scripts/generate-assets.sh` 调用 `bl` CLI 生成并下载素材。

#### 视频素材 — `bl video generate` / `bl video ref`

```bash
# 角色立绘（有参考图 → image-to-video）
bl video generate \
  --image ./references/ye_wenjie.png \
  --prompt "一位穿着军绿色工装的年轻女性，目光坚定地注视远方，微风吹动发丝，半身特写" \
  --resolution 720P --duration 5 --watermark false \
  --download public/assets/portraits/ye_wenjie.mp4

# 角色立绘（无参考图 → text-to-video）
bl video generate \
  --prompt "一位穿着深色西装的中年物理学家，站在大学讲台前，表情严肃，半身特写" \
  --resolution 720P --duration 5 --watermark false \
  --download public/assets/portraits/physicist.mp4

# 过场动画
bl video generate \
  --prompt "红岸基地，巨大的抛物面天线在暴风雨中矗立，闪电照亮天线轮廓，镜头从远景推近，电影级画质" \
  --resolution 1080P --duration 5 --watermark false \
  --download public/assets/cutscenes/red_coast_storm.mp4

# 多角色一致性场景（bl video ref）
bl video ref \
  --prompt "Image1 和 Image2 在实验室中争论，Image1 愤怒地拍桌子，Image2 冷静地注视" \
  --image ./references/character_a.png \
  --image ./references/character_b.png \
  --resolution 1080P --duration 5 --watermark false \
  --download public/assets/cutscenes/lab_argument.mp4
```

#### 图片素材 — `bl image generate`

```bash
# 角色立绘（静态图片）
bl image generate \
  --prompt "一位穿着军绿色工装的年轻中国女性，目光坚定，黑色短发，70年代风格，半身肖像画，电影光影" \
  --size 768*1024 --watermark false \
  --out-dir public/assets/portraits/ --out-prefix ye_wenjie

# 场景背景图
bl image generate \
  --prompt "1960年代中国大学校园，苏式建筑，红色标语横幅，秋天的梧桐树，灰暗天空，写实油画风格" \
  --size 1920*1080 --watermark false \
  --out-dir public/assets/backgrounds/ --out-prefix campus_1967

# 过场 CG（静态图 + 游戏内 Ken Burns 动效）
bl image generate \
  --prompt "红岸基地全景，巨大的抛物面天线矗立在山顶，黄昏，金色光芒，电影级构图" \
  --size 1920*1080 --watermark false \
  --out-dir public/assets/cutscenes/ --out-prefix red_coast_base
```

#### TTS 旁白 — `bl speech synthesize`（可选）

```bash
# 场景旁白
bl speech synthesize \
  --text "1967年，中国大地上，一场浩劫正在改变无数人的命运。" \
  --voice longxiaochun --language zh \
  --out public/assets/narrations/scene_opening.mp3

# 角色独白
bl speech synthesize \
  --text "叶文洁按下了发射按钮，那一刻，她做出了一个改变人类文明命运的决定。" \
  --voice longxiaochun --language zh \
  --instruction "用沉重而悲伤的语气" \
  --out public/assets/narrations/ye_decision.mp3
```

#### 并行生成脚本模式（视频素材提速）

视频生成每个耗时 2-5 分钟，串行太慢。用 `--async` 并行提交再批量下载：

```bash
#!/bin/bash
set -e

# 并行提交所有视频生成任务
declare -A TASKS  # name → task_id

echo "=== 提交视频生成任务 ==="
for name in "${!PORTRAITS[@]}"; do
  outfile="public/assets/portraits/${name}.mp4"
  [ -f "$outfile" ] && echo "  [跳过] $name" && continue

  echo "  [提交] $name ..."
  tid=$(bl video generate \
    --prompt "${PORTRAITS[$name]}" \
    --resolution 720P --duration 5 --watermark false \
    --async --output json | jq -r '.taskId')
  TASKS[$name]="$tid"
  echo "  [任务] $name → $tid"
done

# 等待并下载所有任务
echo "=== 下载视频 ==="
for name in "${!TASKS[@]}"; do
  echo "  [下载] $name (task: ${TASKS[$name]}) ..."
  bl video download --task-id "${TASKS[$name]}" --out "public/assets/portraits/${name}.mp4"
  echo "  [完成] $name"
done
```

#### 关键规则

- **素材必须离线生成并下载到本地**：游戏运行时零 API 调用
- **本地文件路径直接传入 `--image`**：`bl` CLI 自动上传到临时存储，无需手动上传
- **已生成素材自动跳过**：脚本检查本地文件是否存在（`[ -f path ]`）
- **generated-assets.json 只存本地路径**：如 `/assets/portraits/ye_wenjie.mp4`，绝不存远程 URL
- **视频用 `--async` 并行提交**：3-5 个并发，避免串行等待

### Web Audio API 程序化音乐

- 用 MIDI 音高数组定义旋律乐句，循环播放
- 多声部叠加（主旋律 + 去谐波 detune + pad 持续音）
- 卷积混响（用随机衰减 impulse buffer）
- ADSR 包络（attack-decay-sustain-release）
- 低通滤波器随时间衰减
- 不同场景/氛围用不同配置（bpm、音阶、波形、滤波频率）

### 音效

- **打字音**：白噪声脉冲 + 带通滤波（2000-4000Hz）+ 微弱正弦下降音，模拟机械击键
- **点击音**：双音方波上行（660→880Hz）
- **场景切换**：四音正弦琶音 + 混响
- **档案解锁**：扫频 + 四音三角波和弦

---

## 第六步：开发流程

按以下顺序执行，每步完成后标记 task：

1. 初始化 React 项目 + 目录结构
2. 编写 story.js（所有场景文本、选择、分支）— 这是最大的工作量
3. 编写 characters.js 和 archives.js
4. 实现主题样式（CSS 变量、字体、配色、动画、移动端适配）
5. 实现核心组件：TypeWriter → GameScene → ChoicePanel → CharacterPortrait（支持视频/图片）
6. 实现 CutScene（支持视频/图片 Ken Burns）
7. 实现 TitleScreen + EndingScreen + ArchivePanel + SaveLoadPanel
8. 实现 useGameState（reducer + hash 路由 + localStorage 存档）
9. 实现 useAudio（BGM 乐谱 + 音效 + 可选 TTS 旁白播放）
10. 如需 AI 素材：编写 `scripts/generate-assets.sh` → 执行生成并下载
11. 实现特殊场景效果（Canvas 动态背景、点击交互等）
12. 整合 App.jsx
13. 启动 dev server，浏览器测试完整流程（至少走通两条路线到不同结局）
14. 移动端测试（用 Chrome DevTools 模拟手机视口 + 触控）

---

## 避坑指南

以下是从实际开发中总结的经验，务必遵循：

- **bl video 分辨率**：`bl video generate` 支持 720P 和 1080P，测试阶段用 720P（更快更便宜），最终版用 1080P
- **bl video --download 自动轮询**：`--download` 标志会自动等待任务完成并下载文件，无需手写轮询代码；批量生成时用 `--async` + `bl video download` 并行提速
- **bl image generate 尺寸**：用 `--size` 指定，格式为 `宽*高`（如 `1920*1080`），也支持比例格式（如 `16:9`）
- **本地路径自动上传**：`bl` CLI 的 `--image` 接受本地文件路径，会自动上传到临时存储（48小时有效），无需手动上传
- **素材必须离线生成并下载到本地**：视频生成耗时 2-5 分钟/个，绝不能在游戏运行时调用。下载到 `public/assets/`，generated-assets.json 中只存本地路径
- **Prompt 内容审核**：避免暴力、吸烟等敏感描述，否则会被 API 拒绝；换温和表述重试
- **React Hooks 顺序**：所有 useCallback/useEffect 必须在 early return 之前调用，否则报 rules-of-hooks 错误
- **BGM 编曲**：用固定 MIDI 乐谱数组循环播放，不要用随机音符漫游（听起来像噪声）
- **打字音质感**：用噪声脉冲 + 带通滤波模拟击键，比纯方波 beep 好很多
- **特殊场景视觉**：Canvas 动态背景必须与叙事内容紧密关联（出现什么元素画什么），不能泛泛画星空了事
- **点击交互**：Canvas 场景加粒子爆发 + 冲击波环 + 屏幕震动 + 主题相关额外效果，大幅提升沉浸感
- **CRA 清理**：初始化后立即删除 App.css/logo.svg/setupTests.js 等样板文件，避免冲突
- **移动端字体**：正文最小 16px，否则 iOS Safari 会自动缩放页面
- **视频内存泄漏**：离开场景时必须 `video.pause(); video.removeAttribute('src'); video.load()` 释放内存
- **避免伪分支**：若两个选项的 `next` 指向同一场景且仅 flag 不同，玩家会感觉「选了没用」。重大选择必须 `next` 到不同场景，或至少在同场景用 flag 触发明显不同的文本/立绘
- **合流点保留差异感**：分叉汇合后，至少在合流场景的文本/旁白中体现玩家之前的选择（读 flag 渲染条件文本），否则分叉毫无意义
- **分支深度要够**：每个重大分支至少影响 2-3 个后续场景，仅分叉一个场景就立刻合流会让玩家觉得「选了也就多看一句话」
