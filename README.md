# Open Course Compiler / OCW 入脑助手 全功能开发文档

> 版本：v0.1 全规格工程设计稿  
> 日期：2026-07-09  
> 目标读者：AI 编码代理、自动化工程代理、代码审查代理、测试生成代理  
> 开发方式：全规格模块化构建，不采用 MVP 先行策略  
> 产品定位：本地优先的开放课程编译系统，把开放大学课程材料转成个人化、互动式、可测验、可复盘的学习系统。

---

## 目录

1. [项目总定义](#1-项目总定义)
2. [事实基线与外部约束](#2-事实基线与外部约束)
3. [终态产品范围](#3-终态产品范围)
4. [课程模式与适配性边界](#4-课程模式与适配性边界)
5. [全栈技术选型](#5-全栈技术选型)
6. [系统总架构](#6-系统总架构)
7. [本地文件系统布局](#7-本地文件系统布局)
8. [Monorepo 代码结构](#8-monorepo-代码结构)
9. [核心领域模型](#9-核心领域模型)
10. [数据库设计](#10-数据库设计)
11. [向量索引设计](#11-向量索引设计)
12. [Provider Adapter System](#12-provider-adapter-system)
13. [MIT OCW Provider](#13-mit-ocw-provider)
14. [Open Yale Courses Provider](#14-open-yale-courses-provider)
15. [Catalog System](#15-catalog-system)
16. [Course Suitability Engine](#16-course-suitability-engine)
17. [Goal Understanding Engine](#17-goal-understanding-engine)
18. [Learning Path Planner](#18-learning-path-planner)
19. [Asset Download Manager](#19-asset-download-manager)
20. [Content Parser System](#20-content-parser-system)
21. [Media Processing System](#21-media-processing-system)
22. [Course Structure Builder](#22-course-structure-builder)
23. [AI Provider Layer](#23-ai-provider-layer)
24. [Lesson Compiler](#24-lesson-compiler)
25. [Quiz / Assessment Generator](#25-quiz--assessment-generator)
26. [Grading Engine](#26-grading-engine)
27. [Mastery Engine](#27-mastery-engine)
28. [Retrieval / RAG / Citation System](#28-retrieval--rag--citation-system)
29. [Job System 与任务 DAG](#29-job-system-与任务-dag)
30. [Backend API 设计](#30-backend-api-设计)
31. [Frontend UI 设计](#31-frontend-ui-设计)
32. [Token Ledger 与成本控制](#32-token-ledger-与成本控制)
33. [隐私、安全与许可策略](#33-隐私安全与许可策略)
34. [测试体系](#34-测试体系)
35. [AI 编码代理任务契约](#35-ai-编码代理任务契约)
36. [完成定义](#36-完成定义)
37. [参考来源](#37-参考来源)

---

## v0.1 分阶段实现计划

本阶段计划用于把 v0.1 全规格产品范围拆成 10 个连续交付阶段。每个阶段都必须在终态接口、契约测试和可集成实现的前提下推进，不允许以 mock-only 或临时硬编码替代最终能力。

### Stage 1 — Monorepo foundation, local runtime, configuration, shared types, SQLite schema baseline

建立 monorepo、开发脚本、本地运行方式、配置系统、共享类型包和 SQLite schema 基线；同时定义目录规范、迁移机制、基础任务模型与最小契约测试，为后续 Provider、解析、索引、AI、GUI 和导出能力提供稳定工程地基。

### Stage 2 — Provider Adapter System, MIT OCW provider, Open Yale Courses provider, catalog refresh/search/filter

实现可扩展 Provider Adapter System、MIT OCW Provider、Open Yale Courses Provider 和插件接口；完成 catalog refresh / search / filter、课程元数据规范化、provider capability 标记、许可字段采集和 provider 契约测试。

### Stage 3 — Course suitability engine, goal understanding, clarification flow, learning path planner

实现课程适配性判断、用户学习目标解析、澄清式问答和学习路径规划；系统必须能够解释选课与排除理由，结合 deterministic rule guardrails 与结构化 AI 输出，生成跨 provider、可追踪、可调整的学习路径。

### Stage 4 — Asset download manager, resumable queues, file object store, license/attribution tracking

实现课程资源按需下载、断点续传、下载队列、文件对象存储、资源校验、重试策略、去重策略、许可与 attribution 追踪；每个下载资产都必须与课程、provider、来源 URL、许可信息和本地对象位置建立可审计关联。

### Stage 5 — Content parsers for HTML, PDF, transcripts, subtitles, media metadata, course structure builder

实现 HTML / PDF / transcript / subtitle / media metadata parser，并构建 course structure builder；系统必须能够解析 assignments、exams、readings、lecture notes、媒体清单等资源，重建课程单元、学习单元与原始课程题目来源关系。

### Stage 6 — Media processing, local ASR, keyframe/OCR support, chunking, embeddings, LanceDB indexing

实现视频/音频处理、本地 ASR、已有 transcript 优先策略、关键帧截图与 OCR 支持、内容 chunking、embedding 生成和 LanceDB 索引；产物必须支持本地知识库搜索、课程问答 RAG、引用定位和后续讲义/测验生成。

### Stage 7 — AI provider abstraction, OpenAI/local model support, structured outputs, token ledger

实现 AI provider abstraction，支持 OpenAI、本地模型、API key 配置、结构化输出、模型能力声明、错误重试、速率限制和 token 成本记录；所有 AI 调用必须可审计、可替换，并能输出符合下游 schema 的结果。

### Stage 8 — Lesson compiler, notes, audio-script generation, glossary, concept cards, citation tracking

实现 lesson compiler、学习单元切分、带引用讲义生成、可听版脚本生成、术语表生成、概念卡片生成和引用追踪；所有生成内容必须保留来源 chunk、原始资产、许可和 attribution 信息。

### Stage 9 — Quiz/assessment generation, grading engine, rubric handling, mastery engine, remediation, spaced review

实现测验生成、原题复用、rubric 生成、客观题评分、短答题语义评分、论文/开放题反馈、代码题测试支持、错因诊断、补救学习生成、掌握度状态机、延迟复测和间隔复习；reference_only 课程必须遵守掌握度边界，不得被标记为 mastered。

### Stage 10 — Desktop GUI, backend API integration, exports, RAG course Q&A, full-system tests, final v0.1 verification

实现本地桌面 GUI、本地 FastAPI 后端集成、导出 Markdown / PDF / Anki / JSON、本地知识库搜索、课程问答 RAG、全系统测试、干净安装验证和端到端用户闭环；最终验证必须逐项确认 `README.md` section `3.1 必须实现的全功能` 中的每个条目均已实现或被明确验收。

**Completion gate:** v0.1 is not complete unless all 50 items in `README.md` section `3.1 必须实现的全功能` pass acceptance checks and the completion criteria in `README.md` section `36. 完成定义` are satisfied.

---

## 1. 项目总定义

### 1.1 产品一句话

**Open Course Compiler 是一个本地运行的开放课程编译系统，将 MIT OpenCourseWare、Open Yale Courses 等开放课程材料编译为个人化学习路径、结构化讲义、可听版本、互动测验、错题复盘和掌握度推进系统。**

中文产品名可暂定：

- OCW 入脑助手
- 开放课程编译器
- Open Course Compiler
- CourseWeaver
- OpenCourse Brain

正式公开名称不得暗示 MIT、Yale 或其他课程源对产品背书。

### 1.2 正确开发哲学

本项目不采用 MVP 思路。

错误方式：

```text
做一点功能 → 看看能不能跑 → 之后再重构 → 之后再补模块
```

正确方式：

```text
定义完整终态 → 固定模块契约 → 分组件完整实现 → 契约测试 → 系统集成 → 全功能闭环
```

每个组件从第一版起就按终态接口设计，不写临时逻辑，不硬编码某一门课、某一类题、某一个模型、某一个学校。

### 1.3 核心闭环

```text
用户学习目标
  ↓
多课程源检索
  ↓
课程候选池
  ↓
课程可编译性判断
  ↓
个性化学习路径
  ↓
按需下载课程资源
  ↓
解析 transcript / PDF / HTML / 视频 / 音频 / 作业 / 考试
  ↓
课程结构重建
  ↓
学习单元切分
  ↓
讲义 / 可听版 / 术语表 / 测验 / 卡片生成
  ↓
学习界面
  ↓
答题与评分
  ↓
错因诊断
  ↓
补救学习
  ↓
延迟复测
  ↓
掌握度更新
  ↓
下一单元解锁
```

产品价值来自完整闭环，任何单点功能都不是最终产品。

---

## 2. 事实基线与外部约束

本节记录会影响工程设计的外部事实。开发代理不得忽视这些约束。

### 2.1 MIT OpenCourseWare

MIT OpenCourseWare 官方说明其提供来自 MIT 本科和研究生课程的超过 2500 门开放课程资源。[1][2]

MIT OCW 的课程材料一般采用 **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International，CC BY-NC-SA 4.0**。这意味着：

- 可以分享；
- 可以改编；
- 必须署名；
- 只能非商业使用；
- 改编作品必须以相同许可共享；
- 不能暗示 MIT 对产品背书；
- 需要尊重第三方内容例外和额外限制。[3]

工程限制：MIT 支持页面说明，课程 zip 下载包通常不包含视频文件；视频需要通过课程的下载页、播放器或相关媒体入口单独下载。[4]

因此：

```text
MIT Catalog ≠ MIT Course Pack ≠ MIT Video Assets
```

系统必须把 MIT 课程索引、课程包下载、视频/音频发现分开处理。

### 2.2 Open Yale Courses

Open Yale Courses 课程页说明：课程讲座提供可下载视频、音频版本，并提供 searchable transcripts；课程还可能包含 syllabus、readings、exams、problem sets 等材料。[5][6]

OYC 条款说明：大多数讲座和课程材料采用 **Creative Commons Attribution-Noncommercial-Share Alike 3.0，CC BY-NC-SA 3.0**；第三方内容除非在 credits 中明确授权，否则不包含在 Creative Commons 许可内，可能受到额外限制。[7]

因此：

```text
Open Yale Courses 特别适合 lecture/transcript/readings/exams 型课程编译。
但系统必须追踪第三方内容例外，不得默认所有页面内容都可改编。
```

### 2.3 技术栈事实

- Tauri 2 支持用任意前端框架构建跨平台桌面应用，适合作为轻量桌面壳。[8]
- FastAPI 是基于 Python type hints 的现代高性能 API 框架，适合作为本地后端。[9]
- SQLite 是 self-contained、serverless、zero-configuration、transactional SQL database engine，适合作为本地单用户主库。[10]
- LanceDB 是面向 AI/ML 工作负载的向量与多模态数据层，适合本地语义检索和 chunk 索引。[11]
- OpenAI Structured Outputs 可要求模型输出符合 JSON Schema 的结构化结果，适合课程分类、题目生成、评分结果等严格结构化任务。[12]
- OpenAI embeddings 将文本表示为浮点向量，向量距离可用于相关性检索。[13]
- Ollama 本地 API 默认运行在 `http://localhost:11434/api`，适合作为本地 LLM provider。[14]
- faster-whisper 是基于 CTranslate2 的 Whisper 重实现，项目说明其可在同等准确度下更快且内存使用更低。[15]

---

## 3. 终态产品范围

### 3.1 必须实现的全功能

系统最终必须包含：

```text
1. 本地桌面 GUI
2. 本地 FastAPI 后端
3. SQLite 主数据库
4. LanceDB 向量索引
5. 文件对象存储
6. Provider Adapter System
7. MIT OCW Provider
8. Open Yale Courses Provider
9. 可扩展 Provider 插件接口
10. Catalog refresh / search / filter
11. 课程适配性判断
12. 用户学习目标解析
13. 澄清式问答
14. 学习路径规划
15. 课程资源按需下载
16. 断点续传与下载队列
17. HTML / PDF / transcript / subtitle / media parser
18. 视频/音频处理
19. 本地 ASR
20. 关键帧截图与 OCR 支持
21. 内容 chunking
22. embedding 索引
23. 课程结构重建
24. 学习单元切分
25. 讲义生成
26. 可听版脚本生成
27. 术语表生成
28. 概念卡片生成
29. 测验生成
30. 原题复用
31. rubric 生成
32. 客观题评分
33. 短答题语义评分
34. 论文/开放题反馈
35. 代码题测试支持
36. 错因诊断
37. 补救学习生成
38. 掌握度状态机
39. 延迟复测
40. 间隔复习
41. 本地知识库搜索
42. 课程问答 RAG
43. 引用追踪
44. token 成本记录
45. AI provider abstraction
46. 本地模型支持
47. API key 支持
48. 导出 Markdown / PDF / Anki / JSON
49. 许可与 attribution 追踪
50. 全系统测试
```

### 3.2 明确非目标

以下不是本项目目标：

```text
1. 做一个托管课程平台
2. 做一个 SaaS 课程市场
3. 默认把课程材料上传到云端
4. 默认再分发 MIT / Yale 课程材料
5. 用广告变现课程内容
6. 冒充 MIT / Yale 官方产品
7. 对实验课、硬件课、实体创作课作自动权威评分
8. 对团队项目作自动权威评分
9. 用 AI 给所有开放题做最终教授级成绩
```

---

## 4. 课程模式与适配性边界

所有课程必须被分类为以下模式之一。

### 4.1 `full_learn`

适合完整编译为互动学习系统。

典型特征：

```text
- lecture-based
- text-based
- theory-heavy
- 有 transcript 或 lecture notes
- 有 syllabus / calendar / lecture order
- 有 readings / exams / problem sets 更佳
- 学习输出主要是解释、选择题、短答、证明、计算、论文
- 不依赖实体设备
- 不依赖实验室
- 不依赖现场协作
```

支持：

```text
讲义生成
可听版生成
测验生成
评分
错因诊断
补救学习
掌握度判定
复测
解锁下一单元
```

### 4.2 `assisted`

适合辅助学习，但不适合全自动硬判掌握。

典型特征：

```text
- 编程课
- 写作课
- 小型项目课
- 论文型课程
- 有 rubric 但开放性较强
- 可被 AI 提供反馈，但不适合作为唯一权威评分者
```

支持：

```text
任务拆解
讲义整理
概念解释
代码测试
代码审阅
论文结构反馈
rubric feedback
阶段性建议
```

限制：

```text
不作教授级最终成绩
低置信度不得 hard pass
大型项目不得标为 fully mastered
```

### 4.3 `reference_only`

适合参考资料整理，不适合完整互动课程。

典型特征：

```text
- 实验室课程
- 硬件课程
- 电路板/机器人/无人机/机械加工
- 湿实验
- studio / drawing / sculpture / performance
- fieldwork
- team project
- physical artifact
- capstone project 作为核心产出
```

支持：

```text
材料索引
概念解释
预备知识测验
安全/实践提示
阅读辅助
```

限制：

```text
不做 mastered
不做自动通过/不通过
不判断实体作品质量
不判断团队协作成果
```

### 4.4 `unsupported`

不可稳定处理，或许可/资源状态不允许处理。

触发条件：

```text
- 许可不明且材料不可安全解析
- 需要登录或付费访问
- 资源缺失严重
- 第三方内容占主体且不可使用
- 课程没有足够文本/音频/视频材料
```

---

## 5. 全栈技术选型

### 5.1 Desktop

```text
Tauri 2
React
TypeScript
Vite
TanStack Router
TanStack Query
Zustand
Radix UI / shadcn/ui
```

原因：

```text
- 桌面壳轻量
- 前端生态成熟
- 可启动本地 sidecar 后端
- 跨平台
- 与浏览器式学习 UI 适配度高
```

### 5.2 Backend

```text
Python 3.12+
FastAPI
Pydantic v2
SQLAlchemy 2 / SQLModel
Alembic
httpx
selectolax / BeautifulSoup
trafilatura
PyMuPDF
pdfplumber
ffmpeg-python / subprocess ffmpeg
faster-whisper
pytesseract 或 easyocr 可选
pytest
ruff
mypy
```

原因：

```text
- Python 适合抓取、解析、ASR、AI pipeline、PDF、视频处理
- FastAPI 提供稳定本地 API
- Pydantic 适合 strict schema
- 测试生态成熟
```

### 5.3 Storage

```text
SQLite：业务主库
LanceDB：向量索引和语义检索
Local File Store：课程材料、视频、音频、截图、生成内容
```

### 5.4 AI Layer

必须支持：

```text
OpenAI-compatible API provider
Ollama local provider
Anthropic-compatible provider optional
Gemini-compatible provider optional
Mock provider for tests
Local embedding provider
OpenAI-compatible embedding provider
Local ASR provider
```

### 5.5 Packaging

```text
Tauri bundle
Python backend sidecar
uv 或 PyInstaller 打包后端
平台数据目录：
- macOS: ~/Library/Application Support/OpenCourseCompiler
- Windows: %APPDATA%/OpenCourseCompiler
- Linux: ~/.local/share/OpenCourseCompiler
```

---

## 6. 系统总架构

```text
┌──────────────────────────────────────────────────────┐
│ Desktop Shell: Tauri + React                         │
│                                                      │
│  Setup UI                                            │
│  Catalog UI                                          │
│  Goal / Clarification UI                             │
│  Path Planner UI                                     │
│  Course Detail UI                                    │
│  Lesson Reader / Player                              │
│  Quiz UI                                             │
│  Review / Mastery UI                                 │
│  Export / Settings / Logs                            │
└───────────────────────┬──────────────────────────────┘
                        │ localhost HTTP / IPC
┌───────────────────────▼──────────────────────────────┐
│ Local Backend: FastAPI                                │
│                                                      │
│  API Routes                                           │
│  Job Runner                                           │
│  Provider Adapters                                    │
│  Catalog Service                                      │
│  Download Manager                                     │
│  Parser System                                        │
│  Media Processor                                      │
│  AI Provider Layer                                    │
│  Suitability Engine                                   │
│  Path Planner                                         │
│  Lesson Compiler                                      │
│  Quiz Generator                                       │
│  Grading Engine                                       │
│  Mastery Engine                                       │
│  Citation Validator                                   │
└───────────────┬─────────────────────┬────────────────┘
                │                     │
┌───────────────▼──────────────┐ ┌────▼────────────────┐
│ SQLite                        │ │ LanceDB             │
│ relational state              │ │ vector/chunk index  │
└───────────────┬──────────────┘ └────┬────────────────┘
                │                     │
┌───────────────▼─────────────────────▼────────────────┐
│ Local File Store                                      │
│ catalog / manifests / assets / media / transcripts    │
│ chunks / compiled lessons / quizzes / exports / cache │
└──────────────────────────────────────────────────────┘
```

---

## 7. 本地文件系统布局

```text
OpenCourseCompiler/
  config/
    settings.json
    ai_providers.json
    provider_registry.json

  db/
    app.sqlite3
    migrations/

  vector/
    lancedb/

  catalog/
    raw/
      mit_ocw/
      open_yale/
    normalized/

  courses/
    {provider_id}/
      {course_id}/
        manifest.json
        license.json
        attribution.json
        assets/
          raw/
          parsed/
        media/
          video/
          audio/
          frames/
        transcripts/
        chunks/
        compiled/
          lessons/
          quizzes/
          flashcards/
          audio_scripts/
        exports/

  jobs/
    logs/
    checkpoints/

  cache/
    http/
    ai/
    embeddings/
    thumbnails/

  logs/
    app.log
    backend.log
    jobs.log
    errors.log
```

规则：

```text
1. catalog 只放轻量元数据。
2. courses 只放用户显式选择后下载的内容。
3. generated 内容必须保存来源引用和 prompt_version。
4. exports 必须附带 attribution 和 license。
5. cache 可清理，db 与 courses 不可无提示清理。
```

---

## 8. Monorepo 代码结构

```text
open-course-compiler/
  apps/
    desktop/
      package.json
      vite.config.ts
      src/
        main.tsx
        app.tsx
        routes/
          setup.tsx
          catalog.tsx
          goal.tsx
          path.tsx
          course.tsx
          lesson.tsx
          quiz.tsx
          review.tsx
          search.tsx
          exports.tsx
          settings.tsx
          jobs.tsx
          logs.tsx
        components/
        lib/
          api.ts
          query.ts
          state.ts
          schemas.ts
      src-tauri/
        tauri.conf.json
        src/main.rs

    backend/
      pyproject.toml
      app/
        main.py
        config.py
        paths.py
        logging.py
        errors.py
        db/
          models.py
          session.py
          migrations/
        schemas/
          base.py
          provider.py
          course.py
          assets.py
          lesson.py
          quiz.py
          mastery.py
          jobs.py
        providers/
          base.py
          mit_ocw.py
          open_yale.py
          registry.py
        catalog/
          service.py
          search.py
          dedupe.py
          metadata_embedding.py
        suitability/
          rules.py
          classifier.py
          schema.py
        goals/
          parser.py
          clarification.py
        paths/
          planner.py
          prerequisites.py
        downloader/
          manager.py
          http_client.py
          checksum.py
          rate_limit.py
        parsers/
          html.py
          pdf.py
          transcript.py
          subtitle.py
          assignment.py
          exam.py
          solution.py
          code.py
        media/
          ffmpeg.py
          asr.py
          frames.py
          ocr.py
          alignment.py
        vector/
          embeddings.py
          lancedb_store.py
          retrieval.py
        ai/
          providers/
            base.py
            openai_compatible.py
            ollama.py
            mock.py
          structured.py
          prompts.py
          token_ledger.py
          cache.py
        structure/
          unit_builder.py
          concept_extractor.py
        compiler/
          lessons.py
          audio_scripts.py
          glossary.py
          flashcards.py
          citations.py
        assessment/
          quiz_generator.py
          item_bank.py
          rubric.py
        grading/
          objective.py
          semantic.py
          code_runner.py
          essay_feedback.py
          confidence.py
        mastery/
          state_machine.py
          scheduler.py
          remediation.py
        jobs/
          runner.py
          registry.py
          models.py
          checkpoints.py
        api/
          routes_health.py
          routes_settings.py
          routes_catalog.py
          routes_courses.py
          routes_goals.py
          routes_paths.py
          routes_lessons.py
          routes_quiz.py
          routes_mastery.py
          routes_jobs.py
          routes_exports.py

      tests/
        fixtures/
          mit_ocw/
          open_yale/
          courses/
          media/
          parsed/
        test_provider_contract.py
        test_mit_provider.py
        test_yale_provider.py
        test_catalog.py
        test_suitability.py
        test_goal_parser.py
        test_path_planner.py
        test_downloader.py
        test_parsers.py
        test_media.py
        test_vector.py
        test_unit_builder.py
        test_lesson_compiler.py
        test_quiz_generator.py
        test_grading.py
        test_mastery.py
        test_citations.py
        test_api.py

  packages/
    shared-schema/
      package.json
      src/
        course.ts
        asset.ts
        lesson.ts
        quiz.ts
        job.ts
        mastery.ts

  docs/
    DEVELOPMENT.md
    PROVIDER_CONTRACT.md
    LICENSE_POLICY.md
    AGENT_TASKS.md
    API.md
```

---

## 9. 核心领域模型

### 9.1 枚举

```python
from enum import Enum

class ProviderId(str, Enum):
    MIT_OCW = "mit_ocw"
    OPEN_YALE = "open_yale"

class CourseMode(str, Enum):
    FULL_LEARN = "full_learn"
    ASSISTED = "assisted"
    REFERENCE_ONLY = "reference_only"
    UNSUPPORTED = "unsupported"

class AssetType(str, Enum):
    HTML = "html"
    PDF = "pdf"
    VIDEO = "video"
    AUDIO = "audio"
    TRANSCRIPT = "transcript"
    SUBTITLE = "subtitle"
    SLIDES = "slides"
    ASSIGNMENT = "assignment"
    EXAM = "exam"
    SOLUTION = "solution"
    READING = "reading"
    IMAGE = "image"
    CODE = "code"
    DATASET = "dataset"
    ZIP = "zip"
    UNKNOWN = "unknown"

class ProcessingState(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
```

### 9.2 Provider Course Record

```python
from pydantic import BaseModel, HttpUrl, Field
from typing import Literal

class LicenseInfo(BaseModel):
    code: str | None = None
    name: str | None = None
    url: str | None = None
    attribution_required: bool = True
    noncommercial: bool = True
    sharealike: bool = True
    third_party_exceptions_possible: bool = True
    notes: str | None = None

class RawCourseRecord(BaseModel):
    provider_id: str
    provider_course_id: str
    canonical_url: str
    title: str
    course_number: str | None = None
    department: str | None = None
    instructors: list[str] = Field(default_factory=list)
    term: str | None = None
    level: str | None = None
    description: str | None = None
    topics: list[str] = Field(default_factory=list)
    license: LicenseInfo
    raw_metadata: dict = Field(default_factory=dict)
```

### 9.3 Asset

```python
class RawAsset(BaseModel):
    provider_id: str
    course_id: str
    asset_type: AssetType
    url: str | None = None
    title: str | None = None
    local_path: str | None = None
    mime_type: str | None = None
    downloadable: bool = True
    license_scope: Literal[
        "course", "third_party_unknown", "public_domain", "unknown"
    ] = "unknown"
    source_page_url: str | None = None
    metadata: dict = Field(default_factory=dict)
```

### 9.4 Chunk

```python
class SourceRef(BaseModel):
    provider_id: str
    course_id: str
    asset_id: str | None = None
    url: str | None = None
    page_start: int | None = None
    page_end: int | None = None
    timestamp_start: float | None = None
    timestamp_end: float | None = None
    section_title: str | None = None

class ContentChunk(BaseModel):
    chunk_id: str
    course_id: str
    unit_id: str | None = None
    asset_id: str | None = None
    chunk_type: str
    text: str
    source_ref: SourceRef
    token_count: int | None = None
    metadata: dict = Field(default_factory=dict)
```

---

## 10. 数据库设计

### 10.1 SQL Schema

```sql
CREATE TABLE providers (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  base_url TEXT NOT NULL,
  terms_url TEXT,
  license_default TEXT,
  enabled INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE courses (
  id TEXT PRIMARY KEY,
  provider_id TEXT NOT NULL REFERENCES providers(id),
  provider_course_id TEXT NOT NULL,
  canonical_url TEXT NOT NULL,
  title TEXT NOT NULL,
  course_number TEXT,
  department TEXT,
  instructors_json TEXT NOT NULL DEFAULT '[]',
  term TEXT,
  level TEXT,
  language TEXT NOT NULL DEFAULT 'en',
  description TEXT,
  topics_json TEXT NOT NULL DEFAULT '[]',
  license_code TEXT,
  license_url TEXT,
  attribution_text TEXT,
  third_party_exceptions_possible INTEGER NOT NULL DEFAULT 1,
  supported_mode TEXT,
  teachability_score REAL,
  suitability_reason TEXT,
  catalog_state TEXT NOT NULL DEFAULT 'indexed',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(provider_id, provider_course_id)
);

CREATE TABLE course_suitability (
  id TEXT PRIMARY KEY,
  course_id TEXT NOT NULL REFERENCES courses(id),
  supported_mode TEXT NOT NULL,
  teachability_score REAL NOT NULL,
  ai_grading_reliability TEXT NOT NULL,
  requires_lab INTEGER NOT NULL DEFAULT 0,
  requires_physical_equipment INTEGER NOT NULL DEFAULT 0,
  requires_group_work INTEGER NOT NULL DEFAULT 0,
  requires_final_project INTEGER NOT NULL DEFAULT 0,
  requires_artifact_submission INTEGER NOT NULL DEFAULT 0,
  has_sufficient_transcript_or_notes INTEGER NOT NULL DEFAULT 0,
  has_assessments INTEGER NOT NULL DEFAULT 0,
  risk_flags_json TEXT NOT NULL DEFAULT '[]',
  evidence_json TEXT NOT NULL DEFAULT '[]',
  reason TEXT NOT NULL,
  classifier_version TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE course_assets (
  id TEXT PRIMARY KEY,
  course_id TEXT NOT NULL REFERENCES courses(id),
  asset_type TEXT NOT NULL,
  url TEXT,
  title TEXT,
  local_path TEXT,
  source_page_url TEXT,
  mime_type TEXT,
  size_bytes INTEGER,
  checksum TEXT,
  license_scope TEXT NOT NULL DEFAULT 'unknown',
  downloadable INTEGER NOT NULL DEFAULT 1,
  processing_state TEXT NOT NULL DEFAULT 'pending',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE content_chunks (
  id TEXT PRIMARY KEY,
  course_id TEXT NOT NULL REFERENCES courses(id),
  unit_id TEXT,
  asset_id TEXT REFERENCES course_assets(id),
  chunk_type TEXT NOT NULL,
  text TEXT NOT NULL,
  source_ref_json TEXT NOT NULL,
  token_count INTEGER,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);

CREATE TABLE course_units (
  id TEXT PRIMARY KEY,
  course_id TEXT NOT NULL REFERENCES courses(id),
  parent_unit_id TEXT,
  unit_index INTEGER NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  estimated_minutes INTEGER,
  source_asset_ids_json TEXT NOT NULL DEFAULT '[]',
  concepts_json TEXT NOT NULL DEFAULT '[]',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(course_id, unit_index)
);

CREATE TABLE learning_goals (
  id TEXT PRIMARY KEY,
  raw_goal TEXT NOT NULL,
  parsed_goal_json TEXT NOT NULL,
  preferred_language TEXT NOT NULL DEFAULT 'zh',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE learning_paths (
  id TEXT PRIMARY KEY,
  goal_id TEXT NOT NULL REFERENCES learning_goals(id),
  title TEXT NOT NULL,
  description TEXT,
  depth TEXT,
  weekly_hours INTEGER,
  language TEXT NOT NULL DEFAULT 'zh',
  planner_version TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE learning_path_courses (
  id TEXT PRIMARY KEY,
  path_id TEXT NOT NULL REFERENCES learning_paths(id),
  course_id TEXT NOT NULL REFERENCES courses(id),
  sequence_index INTEGER NOT NULL,
  role TEXT NOT NULL,
  inclusion_reason TEXT NOT NULL,
  mode_override TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE lessons (
  id TEXT PRIMARY KEY,
  unit_id TEXT NOT NULL REFERENCES course_units(id),
  title TEXT NOT NULL,
  lesson_markdown TEXT NOT NULL,
  audio_script TEXT,
  summary TEXT,
  source_citations_json TEXT NOT NULL,
  prompt_version TEXT NOT NULL,
  model_info_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE quiz_items (
  id TEXT PRIMARY KEY,
  lesson_id TEXT NOT NULL REFERENCES lessons(id),
  item_type TEXT NOT NULL,
  prompt TEXT NOT NULL,
  choices_json TEXT,
  correct_answer_json TEXT,
  rubric_json TEXT,
  difficulty TEXT NOT NULL DEFAULT 'medium',
  source_citations_json TEXT NOT NULL,
  origin TEXT NOT NULL DEFAULT 'generated',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE attempts (
  id TEXT PRIMARY KEY,
  quiz_item_id TEXT NOT NULL REFERENCES quiz_items(id),
  user_answer TEXT NOT NULL,
  grade_json TEXT NOT NULL,
  score REAL,
  passed INTEGER NOT NULL DEFAULT 0,
  confidence REAL,
  created_at TEXT NOT NULL
);

CREATE TABLE mastery_records (
  id TEXT PRIMARY KEY,
  unit_id TEXT NOT NULL REFERENCES course_units(id),
  status TEXT NOT NULL,
  mastery_score REAL NOT NULL DEFAULT 0,
  weak_concepts_json TEXT NOT NULL DEFAULT '[]',
  last_attempt_at TEXT,
  next_review_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(unit_id)
);

CREATE TABLE jobs (
  id TEXT PRIMARY KEY,
  job_type TEXT NOT NULL,
  status TEXT NOT NULL,
  input_json TEXT NOT NULL,
  output_json TEXT,
  error_json TEXT,
  progress REAL NOT NULL DEFAULT 0,
  checkpoint_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  started_at TEXT,
  finished_at TEXT
);

CREATE TABLE token_ledger (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  task_type TEXT NOT NULL,
  course_id TEXT,
  unit_id TEXT,
  input_tokens INTEGER,
  output_tokens INTEGER,
  estimated_cost_usd REAL,
  cache_hit INTEGER NOT NULL DEFAULT 0,
  prompt_version TEXT,
  created_at TEXT NOT NULL
);
```

### 10.2 设计规则

```text
1. 所有 JSON 字段必须由 Pydantic schema 校验。
2. 所有长任务通过 jobs 表记录状态。
3. generated content 必须记录 prompt_version 和 model_info。
4. 任何 lesson/quiz 没有 citations 不允许入库。
5. courses 表只放当前 catalog 状态，不放大型文本。
6. content_chunks 是 RAG 和 citation 的最小可信单元。
```

---

## 11. 向量索引设计

### 11.1 LanceDB Tables

```text
course_metadata_vectors
- course_id
- provider_id
- title
- description
- topics
- supported_mode
- teachability_score
- embedding
- metadata_json

course_chunk_vectors
- chunk_id
- course_id
- unit_id
- asset_id
- provider_id
- asset_type
- chunk_type
- text
- source_ref_json
- license_scope
- embedding
- metadata_json
```

### 11.2 检索策略

不同任务使用不同检索范围：

```text
目标解析/课程推荐：检索 course_metadata_vectors
学习路径规划：检索 course_metadata_vectors + prerequisites metadata
单元讲义生成：检索目标 unit chunks + 相邻 unit chunks
测验生成：只检索 lesson 绑定的 source chunks
课程问答：默认限定当前课程；用户明确要求跨课程时才跨课程
错题补救：检索错题 source chunks + weak concept chunks
```

### 11.3 引用策略

每个检索结果必须包含：

```text
provider_id
course_id
asset_id
chunk_id
source URL
page or timestamp
license scope
```

没有可追踪 source_ref 的内容不得作为核心知识来源。

---

## 12. Provider Adapter System

### 12.1 目标

将 MIT OCW、Open Yale Courses 和未来课程源隔离为 provider 插件。业务层只处理统一 schema。

### 12.2 接口

```python
from typing import Protocol

class CourseProvider(Protocol):
    provider_id: str
    name: str
    base_url: str

    async def refresh_catalog(self) -> list[RawCourseRecord]:
        """Fetch lightweight catalog metadata only."""

    async def fetch_course_manifest(self, provider_course_id: str) -> RawCourseManifest:
        """Fetch per-course page structure and asset references."""

    async def list_assets(self, manifest: RawCourseManifest) -> list[RawAsset]:
        """Discover downloadable and parseable assets."""

    async def normalize_course(self, manifest: RawCourseManifest) -> NormalizedCourse:
        """Return normalized course metadata."""
```

### 12.3 Provider 必须遵守

```text
1. refresh_catalog 只能抓轻量元数据，不下载课程包。
2. fetch_course_manifest 可以抓单门课程页面结构。
3. list_assets 只发现资源，不自动下载。
4. normalize_course 必须输出统一 schema。
5. 所有 provider 必须提供 license 默认值和 terms URL。
6. 第三方内容许可不明确时 license_scope = third_party_unknown 或 unknown。
7. provider 不得绕过 robots、登录、付费墙或 DRM。
```

---

## 13. MIT OCW Provider

### 13.1 Provider ID

```text
mit_ocw
```

### 13.2 许可默认值

```json
{
  "code": "CC-BY-NC-SA-4.0",
  "name": "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International",
  "url": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
  "attribution_required": true,
  "noncommercial": true,
  "sharealike": true,
  "third_party_exceptions_possible": true
}
```

### 13.3 Catalog 抓取策略

优先使用公开搜索/课程列表/站点地图。不得假设所有课程页面结构相同。

输出字段：

```text
title
course_number
department
level
term
instructors
description
topics
canonical_url
```

### 13.4 Manifest 发现

单门课程 manifest 应发现：

```text
syllabus
calendar
lecture notes
assignments
exams
solutions
readings
download course materials link
video pages
audio links
transcript/subtitle links if available
```

### 13.5 特别规则

```text
1. 不得假设 course zip 包含视频。
2. 课程 zip、视频、音频、subtitle 必须作为不同 asset。
3. 下载课程 zip 后仍需解析内部 HTML/PDF。
4. 视频发现失败不能导致课程失败，应降级为 notes/transcript-based。
5. OCW 中存在硬件、实验、项目类课程；必须交给 Suitability Engine 判断，不得默认 full_learn。
```

---

## 14. Open Yale Courses Provider

### 14.1 Provider ID

```text
open_yale
```

### 14.2 许可默认值

```json
{
  "code": "CC-BY-NC-SA-3.0-US",
  "name": "Creative Commons Attribution-Noncommercial-Share Alike 3.0 United States",
  "url": "https://creativecommons.org/licenses/by-nc-sa/3.0/us/",
  "attribution_required": true,
  "noncommercial": true,
  "sharealike": true,
  "third_party_exceptions_possible": true
}
```

### 14.3 Catalog 抓取策略

OYC 课程列表通常可以解析出：

```text
course title
department
professor/instructor
semester/year
course URL
```

### 14.4 Manifest 发现

单门课程 manifest 应发现：

```text
course home
syllabus
sessions/lectures
transcript pages
audio downloads
low-bandwidth video
high-bandwidth video
readings
exams
problem sets
```

### 14.5 特别规则

```text
1. 如果课程已有 transcript，优先使用 transcript，不强制 ASR。
2. transcript 必须按 lecture/session 组织。
3. audio/video 可按需下载，不在 catalog refresh 时下载。
4. third-party readings 不得默认改编；只记录为 reading reference 或 unknown license asset。
```

---

## 15. Catalog System

### 15.1 职责

```text
刷新 provider catalog
去重
标准化
存储
全文搜索
语义搜索
课程筛选
课程适配性状态展示
```

### 15.2 Catalog Refresh Job

```text
job_type: catalog.refresh
input:
  providers: [mit_ocw, open_yale]
steps:
  1. fetch provider catalog
  2. validate RawCourseRecord
  3. normalize fields
  4. upsert courses
  5. enqueue suitability classification
  6. embed course metadata
  7. update refresh summary
```

### 15.3 搜索功能

必须支持：

```text
keyword search
semantic search
provider filter
department filter
topic filter
mode filter
teachability score filter
has video / transcript / readings / exams filter
license filter
```

### 15.4 去重规则

```text
provider_id + provider_course_id 唯一
canonical_url 近似唯一
同 provider 重复标题需保留 term/version
跨 provider 不合并，只做 related_courses
```

---

## 16. Course Suitability Engine

### 16.1 目标

判断课程是否适合被编译为完整交互课程。

### 16.2 输入

```text
NormalizedCourse metadata
RawCourseManifest
Asset list
syllabus text
course description
assignment/exam metadata
keywords
provider-specific hints
```

### 16.3 输出 Schema

```json
{
  "course_type": "lecture_based",
  "supported_mode": "full_learn",
  "teachability_score": 0.91,
  "ai_grading_reliability": "high",
  "requires_lab": false,
  "requires_physical_equipment": false,
  "requires_group_work": false,
  "requires_final_project": false,
  "requires_artifact_submission": false,
  "has_sufficient_transcript_or_notes": true,
  "has_assessments": true,
  "risk_flags": [],
  "evidence": [
    "has lecture transcripts",
    "has exams/problem sets",
    "outputs are text-based"
  ],
  "reason": "Lecture-based course with transcripts, readings, and exams."
}
```

### 16.4 Rule-based 预分类

强降级关键词：

```text
lab
laboratory
studio
workshop
hardware
circuit board
Arduino
robot
robotics hardware
drone
fabrication
machining
wet lab
experiment
fieldwork
team project
group project
prototype
physical model
performance
recital
painting
sculpture
design-build
```

可辅助但需谨慎关键词：

```text
final paper
essay
project proposal
programming assignment
capstone
term project
presentation
peer review
portfolio
```

强适配关键词：

```text
lecture
transcript
notes
readings
exam
problem set
quiz
syllabus
discussion questions
essay questions
```

### 16.5 打分公式

```text
teachability_score =
  0.25 * content_completeness
+ 0.20 * transcript_or_notes_quality
+ 0.20 * assessment_availability
+ 0.15 * sequential_structure
+ 0.10 * text_based_output_ratio
+ 0.10 * license_clarity
- 0.35 * physical_dependency
- 0.25 * open_project_dependency
- 0.20 * group_dependency
```

模式判定：

```text
if physical_dependency >= 0.6:
    reference_only
elif group_dependency >= 0.6:
    reference_only
elif open_project_dependency >= 0.7:
    assisted
elif score >= 0.75:
    full_learn
elif score >= 0.45:
    assisted
else:
    reference_only or unsupported
```

### 16.6 绝对禁止规则

```text
如果 requires_physical_equipment = true，则不得 full_learn。
如果 requires_lab = true，则不得 full_learn。
如果 requires_artifact_submission = true 且 artifact 为实体或艺术作品，则不得 full_learn。
如果 requires_group_work = true 且团队项目为课程核心，则不得 full_learn。
```

---

## 17. Goal Understanding Engine

### 17.1 输入

用户自然语言目标：

```text
我想学哲学
我想学政治哲学
我想从零开始学 AI
我想补完 MIT 本科数学
我想系统学经济学
```

### 17.2 输出 Schema

```json
{
  "raw_goal": "我想学哲学",
  "domain": "philosophy",
  "subdomains": ["ethics", "political_philosophy", "philosophy_of_mind"],
  "depth": "unknown",
  "preferred_language": "zh",
  "preferred_course_mode": "full_learn",
  "time_budget_hours_per_week": null,
  "needs_clarification": true,
  "clarifying_questions": [
    {
      "id": "q1",
      "question": "你更想学哪一种哲学路径？",
      "options": [
        {"id": "intro", "label": "通识入门"},
        {"id": "ethics", "label": "伦理学"},
        {"id": "political", "label": "政治哲学"},
        {"id": "mind", "label": "心灵哲学"},
        {"id": "science", "label": "科学哲学"}
      ]
    }
  ]
}
```

### 17.3 行为规则

```text
1. 目标不明确时必须追问。
2. 追问必须给选项。
3. 追问不得超过必要数量。
4. 用户拒绝回答时使用默认路径，但标记 assumption。
5. Goal parser 不直接选择课程，只输出 learning intent。
```

---

## 18. Learning Path Planner

### 18.1 输入

```text
ParsedGoal
Clarification answers
Course candidates
Suitability results
Provider metadata
Prerequisite hints
User constraints
```

### 18.2 输出 Schema

```json
{
  "title": "哲学系统入门路径",
  "description": "从哲学问题、论证方法到伦理学和政治哲学的系统学习路径。",
  "language": "zh",
  "depth": "undergraduate_intro",
  "estimated_total_hours": 80,
  "courses": [
    {
      "course_id": "open_yale-phil-176",
      "sequence_index": 1,
      "role": "foundation",
      "supported_mode": "full_learn",
      "reason": "Provides a structured introductory foundation with lecture transcripts."
    }
  ],
  "supplemental_courses": [],
  "excluded_courses": [
    {
      "course_id": "mit-xyz",
      "reason": "Course is lab-heavy and classified as reference_only."
    }
  ],
  "assumptions": [
    "User did not specify weekly time budget; default path assumes moderate pace."
  ]
}
```

### 18.3 规则

```text
1. full_learn 主路径只包含 full_learn 课程。
2. assisted 可作为 optional workshop 或 writing/code practice。
3. reference_only 只作为 supplemental reference。
4. 每门课必须有 inclusion reason。
5. 每个排除项必须有 exclusion reason。
6. 路径必须按概念依赖排序，不按搜索相关度简单排序。
```

---

## 19. Asset Download Manager

### 19.1 职责

```text
按需下载
断点续传
校验 checksum
限速
失败重试
用户取消
磁盘空间预估
重复文件去重
下载记录入库
```

### 19.2 状态机

```text
queued
checking_existing
downloading
paused
verifying
completed
failed
cancelled
```

### 19.3 下载策略

```text
1. catalog refresh 不下载大型资产。
2. 用户接受学习路径后，才下载路径内课程 manifest。
3. 用户点击 compile course 后，才下载该课程所需资产。
4. 视频/音频默认可选下载；已有 transcript 时不强制下载视频。
5. 下载前显示预计大小、token 估计、磁盘空间。
```

### 19.4 去重规则

```text
same URL + same checksum → 复用
same checksum → 建立 hardlink/copy reference
same URL but checksum changed → 保留版本记录
```

---

## 20. Content Parser System

### 20.1 支持解析器

```text
HTML Parser
PDF Parser
Transcript Parser
SRT/VTT Subtitle Parser
Markdown Parser
Plain Text Parser
Assignment Parser
Exam Parser
Solution Parser
Reading List Parser
Code Parser
Dataset Metadata Parser
```

### 20.2 Parser 输出

```json
{
  "asset_id": "asset_123",
  "course_id": "course_123",
  "chunks": [
    {
      "chunk_type": "lecture_transcript",
      "text": "...",
      "source_ref": {
        "url": "...",
        "timestamp_start": 120.5,
        "timestamp_end": 185.2,
        "section_title": "Lecture 1"
      }
    }
  ],
  "parser_version": "transcript_parser_v1",
  "warnings": []
}
```

### 20.3 Chunking 规则

```text
1. 不跨越 lecture/session 边界。
2. 不跨越 PDF section 边界，除非 section 太短。
3. transcript chunk 保留 timestamp。
4. PDF chunk 保留 page range。
5. 每个 chunk 目标长度 300-900 tokens。
6. 公式、代码、题目不得被切坏。
7. assignment/exam 原题作为独立 chunk。
```

---

## 21. Media Processing System

### 21.1 职责

```text
视频信息探测
音频抽取
本地转录
字幕导入
transcript 对齐
关键帧提取
黑板/幻灯片截图
OCR
视觉材料挂接到时间戳
```

### 21.2 处理优先级

```text
1. 已有 transcript：使用 transcript
2. 已有字幕：使用字幕
3. 已有音频：ASR 转录
4. 只有视频：抽取音频后 ASR
5. 视觉内容：关键帧 + OCR 作为辅助
```

### 21.3 输出

```text
timestamped transcript chunks
media frame assets
OCR chunks
alignment metadata
warnings
```

### 21.4 限制

```text
OCR 不可靠时不得用其作为唯一来源生成关键题。
ASR 低置信度段落必须标记。
有官方 transcript 时不得无故覆盖。
```

---

## 22. Course Structure Builder

### 22.1 目标

把课程材料重建为稳定学习单元。

### 22.2 输入优先级

```text
1. syllabus / calendar
2. lecture/session list
3. transcript titles
4. video order
5. PDF lecture note numbering
6. assignment/exam references
7. LLM-assisted inference
```

### 22.3 Unit Schema

```json
{
  "unit_index": 1,
  "title": "Introduction and Course Overview",
  "source_asset_ids": ["asset_lecture_1", "asset_syllabus"],
  "estimated_minutes": 35,
  "concepts": ["argument", "validity", "soundness"],
  "child_units": []
}
```

### 22.4 拆分规则

```text
短讲座：1 lecture = 1 unit
长讲座：1 lecture = 多个 child units
课程阅读：挂到相关 lecture/unit
assignments/exams：挂到覆盖概念最多的 unit 或 module
```

---

## 23. AI Provider Layer

### 23.1 接口

```python
class LLMProvider(Protocol):
    provider_id: str

    async def generate_text(self, request: TextGenerationRequest) -> TextGenerationResult:
        ...

    async def generate_structured(self, request: StructuredGenerationRequest) -> StructuredGenerationResult:
        ...

class EmbeddingProvider(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...

class ASRProvider(Protocol):
    async def transcribe(self, audio_path: str, options: dict) -> TranscriptionResult:
        ...
```

### 23.2 Provider 实现

```text
openai_compatible
ollama
mock
local_embedding
openai_embedding
faster_whisper_asr
```

### 23.3 结构化输出要求

下列任务必须使用 JSON Schema 结构化输出：

```text
课程适配性分类
目标解析
澄清问题生成
学习路径生成
课程单元结构推断
术语表生成
题目生成
rubric 生成
评分结果
错因诊断
补救建议
```

### 23.4 Prompt Registry

每个 prompt 必须有：

```text
prompt_id
prompt_version
task_type
input_schema
output_schema
safety_rules
citation_rules
examples
tests
```

---

## 24. Lesson Compiler

### 24.1 输入

```text
CourseUnit
Source chunks
User preferred language
Depth
Course mode
RAG context
```

### 24.2 输出

```text
lesson_markdown
audio_script
summary
glossary
flashcards
source citations
```

### 24.3 讲义结构

```markdown
# 单元标题

## 学习目标

## 课前问题

## 背景导入

## 核心概念

## 课程材料解释

## 例子

## 常见误解

## 与前后单元的关系

## 本节总结

## 来源
```

### 24.4 引用要求

```text
1. 每个核心定义必须引用 chunk。
2. 每个历史事实必须引用 chunk。
3. 每个公式/推导必须引用 chunk。
4. AI 辅助类比可以不引用，但必须标记为 explanation。
5. 未在课程材料中找到的补充知识必须明确标记。
```

---

## 25. Quiz / Assessment Generator

### 25.1 题型

```text
multiple_choice
true_false
fill_blank
short_answer
calculation
proof
code
essay_outline
argument_analysis
reading_comprehension
socratic_followup
```

### 25.2 生成规则

```text
1. 优先使用课程原有 exams/problem sets/assignments。
2. 原题必须标记 origin = source_original。
3. AI 生成题必须标记 origin = generated。
4. 每道题必须绑定 source_chunk_ids。
5. 开放题必须有 rubric。
6. 没有标准答案的题不得 hard gate。
```

### 25.3 QuizItem Schema

```json
{
  "type": "short_answer",
  "prompt": "Explain the difference between validity and soundness.",
  "expected_answer": "A valid argument preserves truth from premises to conclusion; a sound argument is valid and has true premises.",
  "rubric": [
    {"criterion": "defines validity", "points": 2},
    {"criterion": "defines soundness", "points": 2},
    {"criterion": "distinguishes the two", "points": 1}
  ],
  "source_chunk_ids": ["chunk_123", "chunk_124"],
  "difficulty": "easy",
  "origin": "generated"
}
```

---

## 26. Grading Engine

### 26.1 评分类型

```text
objective grading：选择题、判断题、填空题
symbolic grading：数学/计算题，必要时 CAS 支持
semantic grading：短答题
rubric grading：开放短答/论述题
code test grading：代码题
essay feedback：论文反馈
```

### 26.2 输出 Schema

```json
{
  "score": 0.82,
  "passed": true,
  "confidence": 0.91,
  "feedback": "Your answer correctly distinguishes validity from soundness, but the explanation of truth-preservation could be clearer.",
  "mistake_type": "partial_definition",
  "weak_concepts": ["truth preservation"],
  "remediation_needed": false,
  "source_refs": ["chunk_123"]
}
```

### 26.3 规则

```text
1. 客观题 deterministic grading。
2. 短答题可语义评分，但必须输出 confidence。
3. confidence < 0.75 不允许 hard pass。
4. essay feedback 不作为最终权威成绩。
5. reference_only 课程不产生 mastery pass。
6. 实体作品、实验结果、团队项目不评分。
```

---

## 27. Mastery Engine

### 27.1 状态机

```text
locked
available
in_progress
failed
needs_remediation
passed_once
review_due
mastered
```

### 27.2 状态转移

```text
locked → available
available → in_progress
in_progress → failed
in_progress → passed_once
failed → needs_remediation
needs_remediation → in_progress
passed_once → review_due
review_due → mastered
review_due → needs_remediation
```

### 27.3 Full Learn 通过规则

```text
objective_score >= 0.80
关键题必须正确
short_answer_rubric_score >= 0.70
low_confidence_count = 0
错题复盘完成
延迟复测通过
```

### 27.4 Assisted 规则

```text
显示：completed / feedback_given / needs_revision
谨慎显示：provisionally_mastered
不得对大型项目或论文给最终权威 mastered
```

### 27.5 Reference Only 规则

```text
允许：read, reviewed, practiced
禁止：mastered
禁止：hard_pass
禁止：unlock based on physical completion
```

---

## 28. Retrieval / RAG / Citation System

### 28.1 RAG 原则

```text
1. 默认检索当前课程。
2. 生成 lesson 默认检索当前 unit。
3. 生成 quiz 只使用 lesson 已引用 source chunks。
4. 用户问跨课程问题时才跨课程检索。
5. RAG 回答必须显示来源。
```

### 28.2 Citation Validator

```python
def validate_generated_lesson(lesson: LessonDraft) -> None:
    for block in lesson.blocks:
        if block.kind in {"definition", "core_claim", "formula", "historical_fact"}:
            if not block.source_chunk_ids:
                raise CitationError("Core lesson block requires citations")


def validate_quiz_item(item: QuizItemDraft) -> None:
    if not item.source_chunk_ids:
        raise CitationError("Quiz item requires at least one source chunk")
    if item.type in {"short_answer", "essay_outline", "argument_analysis"} and not item.rubric:
        raise CitationError("Open-ended item requires rubric")
```

### 28.3 无来源处理

如果没有来源，UI 必须显示：

```text
课程材料中未找到足够依据。以下内容为 AI 的一般解释，不作为课程来源内容。
```

---

## 29. Job System 与任务 DAG

### 29.1 Job 设计原则

每个长任务必须：

```text
idempotent
resumable
cancellable
checkpointed
logged
retryable
validated
```

### 29.2 Job 状态

```text
queued
running
paused
completed
failed
cancelled
retrying
```

### 29.3 全系统 DAG

```text
bootstrap_app
  ├─ init_paths
  ├─ init_db
  ├─ init_vector_store
  ├─ start_backend
  └─ open_ui

catalog_refresh
  ├─ provider_refresh:mit_ocw
  ├─ provider_refresh:open_yale
  ├─ normalize_catalog
  ├─ upsert_courses
  ├─ classify_suitability
  ├─ embed_course_metadata
  └─ publish_catalog

goal_to_path
  ├─ parse_goal
  ├─ ask_clarifying_questions
  ├─ retrieve_candidate_courses
  ├─ filter_by_suitability
  ├─ rank_candidates
  ├─ build_path
  └─ persist_path

compile_course
  ├─ fetch_manifest
  ├─ list_assets
  ├─ download_assets
  ├─ parse_assets
  ├─ process_media
  ├─ chunk_content
  ├─ embed_chunks
  ├─ build_units
  ├─ compile_lessons
  ├─ generate_quizzes
  ├─ validate_citations
  └─ publish_compiled_course

study_unit
  ├─ render_lesson
  ├─ run_inline_questions
  ├─ administer_quiz
  ├─ grade_attempts
  ├─ diagnose_errors
  ├─ generate_remediation
  ├─ update_mastery
  └─ unlock_or_schedule_review
```

---

## 30. Backend API 设计

### 30.1 Health / Settings

```http
GET /health
GET /settings
PATCH /settings
GET /settings/ai-providers
PATCH /settings/ai-providers
```

### 30.2 Catalog

```http
POST /catalog/refresh
GET /catalog/courses
GET /catalog/courses/{course_id}
GET /catalog/search?q=philosophy&provider=open_yale&mode=full_learn
GET /catalog/providers
```

### 30.3 Goals / Paths

```http
POST /goals/parse
POST /goals/{goal_id}/answer-clarification
POST /paths/propose
GET /paths/{path_id}
POST /paths/{path_id}/accept
```

### 30.4 Courses

```http
POST /courses/{course_id}/manifest
POST /courses/{course_id}/download
POST /courses/{course_id}/compile
GET /courses/{course_id}/compile-status
GET /courses/{course_id}/assets
GET /courses/{course_id}/units
GET /courses/{course_id}/license
```

### 30.5 Lessons / Quiz / Mastery

```http
GET /units/{unit_id}/lesson
POST /units/{unit_id}/regenerate-lesson
GET /lessons/{lesson_id}/quiz
POST /quiz-items/{item_id}/attempt
GET /attempts/{attempt_id}
GET /units/{unit_id}/mastery
POST /units/{unit_id}/review
```

### 30.6 Search / RAG

```http
POST /search/chunks
POST /courses/{course_id}/ask
POST /paths/{path_id}/ask
```

### 30.7 Jobs

```http
GET /jobs
GET /jobs/{job_id}
POST /jobs/{job_id}/pause
POST /jobs/{job_id}/resume
POST /jobs/{job_id}/cancel
POST /jobs/{job_id}/retry
```

### 30.8 Export

```http
POST /exports/markdown
POST /exports/pdf
POST /exports/anki
POST /exports/json
GET /exports/{export_id}
```

---

## 31. Frontend UI 设计

### 31.1 页面

```text
Setup
Catalog
Goal Intake
Clarification
Path Builder
Course Detail
Download / Compile Status
Lesson Reader
Media Player
Transcript Viewer
Quiz
Feedback
Remediation
Review Queue
Mastery Dashboard
Search / Ask Course
Exports
Settings
Jobs
Logs
License Center
```

### 31.2 Setup UI

必须配置：

```text
数据目录
AI provider
API key 或 Ollama endpoint
是否允许云端 LLM
token 预算
下载策略
本地 ASR 开关
许可确认
```

### 31.3 Catalog UI

必须显示：

```text
课程标题
provider
department
term
instructors
supported_mode
teachability_score
has transcript
has video
has readings
has exams
license
```

### 31.4 Path Builder UI

必须显示：

```text
选中课程
排序理由
排除课程
排除理由
预计下载大小
预计 token 成本
课程模式风险
```

### 31.5 Lesson UI

必须支持：

```text
讲义阅读
可听版
原文/译文切换
来源侧栏
概念卡片
内联问题
笔记
返回原课程材料
```

### 31.6 Quiz UI

必须支持：

```text
一题一答
即时反馈
rubric 展示
来源跳转
错因说明
补救题
复测安排
```

---

## 32. Token Ledger 与成本控制

### 32.1 记录字段

```text
provider
model
task_type
course_id
unit_id
input_tokens
output_tokens
estimated_cost_usd
cache_hit
prompt_version
timestamp
```

### 32.2 默认策略

```text
catalog refresh 不使用 LLM
课程初筛先 rule-based
必要时才 LLM classify
embedding 批量处理
lesson 按 unit 生成
quiz 按 lesson 生成
objective grading 不调用 LLM
同 prompt+source+model 命中缓存则不重复调用
```

### 32.3 用户预算

UI 显示：

```text
本路径预计 token
本课程预计 token
本单元预计 token
本月累计 token
按 provider 估计成本
```

---

## 33. 隐私、安全与许可策略

### 33.1 本地优先

```text
默认不上传课程材料
默认不上传学习记录
默认不启用云同步
使用云端 LLM 前显示将发送的文本范围
允许完全本地模型模式
```

### 33.2 许可策略

每门课必须显示：

```text
课程来源
原始 URL
provider
教师/讲师
访问日期
许可代码
许可 URL
第三方内容例外提示
生成内容保存位置
```

每个导出必须附带：

```text
attribution
source URLs
license info
generated-by notice
non-affiliation notice
```

### 33.3 品牌策略

禁止：

```text
MIT Tutor
Yale Tutor
MIT AI University
Yale AI Courseware
```

必须显示：

```text
This application is not affiliated with or endorsed by MIT, Yale University, or any course provider.
```

---

## 34. 测试体系

### 34.1 Unit Tests

必须覆盖：

```text
provider contract
MIT parser
Yale parser
catalog normalization
suitability rules
goal parsing schema
path planning constraints
downloader retry
PDF parser
HTML parser
transcript parser
chunking
embedding store
unit builder
lesson citation validator
quiz validator
grading confidence
mastery state machine
license propagation
```

### 34.2 Integration Tests

必须覆盖：

```text
refresh catalog → search course
search course → fetch manifest
fetch manifest → download assets
assets → parse chunks
chunks → vector search
unit → lesson
lesson → quiz
quiz → attempt
attempt → mastery update
path → compile selected courses
```

### 34.3 Golden Fixtures

创建固定 fixture：

```text
lecture_based_course_fixture
lab_based_course_fixture
project_heavy_course_fixture
essay_course_fixture
coding_course_with_tests_fixture
course_with_transcript_fixture
course_without_transcript_with_audio_fixture
course_with_third_party_readings_fixture
```

### 34.4 关键验收测试

```text
lab-heavy 课程永远不能 full_learn
hardware-heavy 课程永远不能 full_learn
reference_only 永远不能 mastered
无 citations 的 lesson 不能入库
无 citations 的 quiz 不能入库
低 confidence 评分不能 hard pass
MIT zip 不假设包含 video
OYC transcript 优先于 ASR
```

---

## 35. AI 编码代理任务契约

### 35.1 总指令

```text
Build the complete full-spec Open Course Compiler system, not an MVP.

The product is a local-first desktop application that compiles open university course materials into personalized, interactive learning systems.

Do not implement temporary shortcuts, hardcoded course flows, fake mock-only UI, or MVP-only logic. Every module must be designed according to the final architecture and connected through stable contracts.

The system must include:
1. Tauri + React desktop shell
2. Python FastAPI local backend
3. SQLite relational database
4. LanceDB vector index
5. Provider adapter system
6. MIT OCW provider
7. Open Yale Courses provider
8. Catalog refresh and search
9. Course suitability classification
10. Goal understanding
11. Learning path planning
12. Asset download manager
13. HTML/PDF/transcript/media parsers
14. Video/audio processing and ASR
15. Course structure builder
16. Lesson compiler
17. Quiz generator
18. Grading engine
19. Mastery engine
20. Complete study UI
21. Export system
22. License and attribution tracking
23. Token accounting
24. Local and API AI provider abstraction
25. Full-system integration tests

The system must distinguish course modes:
- full_learn
- assisted
- reference_only
- unsupported

Lab-heavy, hardware-heavy, studio-heavy, fieldwork-heavy, physical-artifact-heavy, or team-project-heavy courses must never be treated as fully automatable.

All generated lessons and quiz items must cite source chunks. All downloads must preserve source URLs and license metadata. The application must not host, redistribute, advertise, or monetize course content.

Every component must be implemented to final-contract quality before integration.
```

### 35.2 组件任务格式

每个任务必须包含：

```text
Task ID
Goal
Dependencies
Input schemas
Output schemas
Files to create
Files allowed to modify
Acceptance tests
Forbidden shortcuts
```

### 35.3 示例任务

```text
Task ID: suitability_engine.full_contract

Goal:
Implement the full course suitability engine that classifies courses into full_learn, assisted, reference_only, or unsupported.

Dependencies:
- schemas.course
- providers.base
- db.models.Course

Files to create:
- app/suitability/rules.py
- app/suitability/classifier.py
- app/suitability/schema.py
- tests/test_suitability.py

Acceptance tests:
- lab-heavy fixture => reference_only
- hardware fixture => reference_only
- lecture+transcript+exam fixture => full_learn
- essay-heavy fixture => assisted
- project-heavy fixture => assisted or reference_only depending on physical dependency
- no course with requires_physical_equipment=true can be full_learn

Forbidden shortcuts:
- Do not classify solely by provider.
- Do not classify all MIT or Yale courses as full_learn.
- Do not use LLM-only classification without deterministic rule guardrails.
```

---

## 36. 完成定义

项目完成不是“能打开界面”。项目完成必须满足：

```text
1. 用户可以刷新 MIT OCW 和 Open Yale catalog。
2. 用户可以输入学习目标并得到澄清问题。
3. 系统可以生成跨 provider 的学习路径。
4. 系统能解释为什么选课、为什么排除课程。
5. 系统能按需下载课程材料。
6. 系统能解析 transcript / PDF / HTML / assignments / exams。
7. 系统能对视频/音频做 ASR 或使用已有 transcript。
8. 系统能重建课程单元。
9. 系统能生成带引用的讲义。
10. 系统能生成带引用的测验。
11. 系统能复用原始课程题目。
12. 系统能评分并输出置信度。
13. 系统能诊断错因并生成补救内容。
14. 系统能维护掌握度状态机。
15. reference_only 课程永远不会被标记为 mastered。
16. 所有生成内容保留来源、许可和 attribution。
17. 用户可以导出学习材料。
18. 应用可在干净安装环境中运行。
19. 全系统测试通过。
20. 无关键流程依赖 mock-only 实现。
```
