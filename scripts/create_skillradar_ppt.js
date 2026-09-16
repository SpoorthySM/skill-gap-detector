const path = require("path");
const pptxgen = require("/Users/spoorthy/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Spoorthy";
pptx.subject = "SkillRadar project presentation";
pptx.title = "SkillRadar - Skill Gap Intelligence System";
pptx.company = "Mini Project";
pptx.lang = "en-US";
pptx.theme = {
  headFontFace: "Aptos Display",
  bodyFontFace: "Aptos",
  lang: "en-US"
};
pptx.defineLayout({ name: "CUSTOM_WIDE", width: 13.333, height: 7.5 });
pptx.layout = "CUSTOM_WIDE";

const C = {
  navy: "102A43",
  ink: "243B53",
  muted: "627D98",
  line: "D9E2EC",
  bg: "F7FAFC",
  panel: "FFFFFF",
  teal: "0B7285",
  green: "2F9E44",
  red: "C92A2A",
  amber: "F08C00",
  violet: "5F3DC4",
  blue: "1864AB"
};

const ROOT = "/Users/spoorthy/Desktop/skill-gap-ml";
const OUT = path.join(ROOT, "SkillRadar_Project_Presentation.pptx");
const CHART = path.join(ROOT, "model_comparison.png");

function slide(title, subtitle) {
  const s = pptx.addSlide();
  s.background = { color: C.bg };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 0.16, fill: { color: C.teal }, line: { color: C.teal } });
  if (title) {
    s.addText(title, { x: 0.55, y: 0.35, w: 11.9, h: 0.42, fontFace: "Aptos Display", fontSize: 24, bold: true, color: C.navy, margin: 0 });
  }
  if (subtitle) {
    s.addText(subtitle, { x: 0.57, y: 0.82, w: 10.8, h: 0.26, fontSize: 9.5, color: C.muted, margin: 0 });
  }
  s.addText("Presented by 23261A6718 | 23261A6741", { x: 9.25, y: 7.15, w: 3.45, h: 0.2, fontSize: 8, color: C.muted, align: "right", margin: 0 });
  return s;
}

function card(s, x, y, w, h, opts = {}) {
  s.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.08,
    fill: { color: opts.fill || C.panel },
    line: { color: opts.line || C.line, width: 0.8 },
    shadow: opts.shadow ? { type: "outer", color: "DDE5EE", opacity: 0.35, blur: 1, angle: 45, distance: 1 } : undefined
  });
}

function stat(s, x, y, value, label, color = C.teal) {
  card(s, x, y, 2.25, 1.03);
  s.addText(value, { x: x + 0.16, y: y + 0.16, w: 1.9, h: 0.35, fontSize: 24, bold: true, color, margin: 0, fit: "shrink" });
  s.addText(label, { x: x + 0.18, y: y + 0.62, w: 1.9, h: 0.22, fontSize: 8.8, color: C.muted, margin: 0, fit: "shrink" });
}

function bulletList(s, items, x, y, w, fontSize = 13, color = C.ink, gap = 0.43) {
  items.forEach((item, i) => {
    s.addShape(pptx.ShapeType.ellipse, { x, y: y + i * gap + 0.09, w: 0.08, h: 0.08, fill: { color: item.color || C.teal }, line: { color: item.color || C.teal } });
    s.addText(item.text || item, { x: x + 0.18, y: y + i * gap, w, h: 0.28, fontSize, color, margin: 0, fit: "shrink" });
  });
}

function tag(s, text, x, y, color, w = 1.4) {
  s.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.32, rectRadius: 0.06, fill: { color }, line: { color } });
  s.addText(text, { x: x + 0.08, y: y + 0.08, w: w - 0.16, h: 0.13, fontSize: 8, bold: true, color: "FFFFFF", align: "center", margin: 0, fit: "shrink" });
}

function miniTitle(s, text, x, y, w, color = C.navy) {
  s.addText(text, { x, y, w, h: 0.28, fontSize: 13.5, bold: true, color, margin: 0, fit: "shrink" });
}

function addNotes(s, notes) {
  s.addNotes(notes);
}

// 1. Title
{
  const s = pptx.addSlide();
  s.background = { color: C.bg };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 7.5, fill: { color: C.bg }, line: { color: C.bg } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 0.18, fill: { color: C.teal }, line: { color: C.teal } });
  s.addText("SkillRadar", { x: 0.65, y: 1.0, w: 6.4, h: 0.7, fontFace: "Aptos Display", fontSize: 44, bold: true, color: C.navy, margin: 0 });
  s.addText("Skill Gap Intelligence System", { x: 0.7, y: 1.78, w: 6.9, h: 0.35, fontSize: 18, color: C.teal, bold: true, margin: 0 });
  s.addText("AI + ML powered placement readiness analyzer for students", { x: 0.7, y: 2.24, w: 7.2, h: 0.32, fontSize: 15, color: C.ink, margin: 0 });
  card(s, 8.25, 0.95, 4.15, 4.45, { fill: "FFFFFF", shadow: true });
  s.addText("Project Snapshot", { x: 8.55, y: 1.28, w: 2.7, h: 0.3, fontSize: 15, bold: true, color: C.navy, margin: 0 });
  stat(s, 8.58, 1.86, "3.3M+", "job postings analyzed", C.blue);
  stat(s, 10.72, 1.86, "10", "supported tech roles", C.green);
  stat(s, 8.58, 3.15, "78.35%", "deployed ML accuracy", C.violet);
  stat(s, 10.72, 3.15, "Gemini", "AI resume extraction", C.amber);
  s.addText("Presented by 23261A6718", { x: 0.72, y: 5.72, w: 4.5, h: 0.3, fontSize: 15, bold: true, color: C.navy, margin: 0 });
  s.addText("23261A6741", { x: 0.72, y: 6.08, w: 5.8, h: 0.25, fontSize: 15, bold: true, color: C.navy, margin: 0 });
  tag(s, "Python", 0.72, 6.62, C.blue);
  tag(s, "Flask", 2.18, 6.62, C.ink);
  tag(s, "Random Forest", 3.64, 6.62, C.green, 1.7);
  tag(s, "Gemini API", 5.42, 6.62, C.amber, 1.55);
  addNotes(s, "Start by positioning the project as a placement-readiness tool, not only a resume parser. Mention that it combines Gemini for extraction, ML for role intelligence, and rule-based gap analysis for explainable recommendations.");
}

// 2. Problem
{
  const s = slide("Problem Statement", "Students often prepare for placements without a role-specific view of their strengths and gaps.");
  const items = [
    ["Unclear role expectations", "A student may know Python or SQL, but not whether that is enough for Data Analyst, ML Engineer, or Backend roles."],
    ["Generic preparation", "Common advice does not tell the student which missing skill should be learned first."],
    ["No measurable readiness", "Students need a simple score and explanation before applying for a target role."],
    ["Manual resume review is slow", "Skill extraction from resumes is repetitive and can miss hidden technical skills."]
  ];
  items.forEach((it, i) => {
    const x = i % 2 === 0 ? 0.75 : 6.95;
    const y = i < 2 ? 1.55 : 4.05;
    card(s, x, y, 5.45, 1.55, { shadow: true });
    s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.24, y: y + 0.25, w: 0.55, h: 0.35, fontSize: 17, bold: true, color: C.teal, margin: 0 });
    miniTitle(s, it[0], x + 0.9, y + 0.22, 4.1);
    s.addText(it[1], { x: x + 0.9, y: y + 0.62, w: 4.2, h: 0.56, fontSize: 10.5, color: C.ink, margin: 0.02, breakLine: false, fit: "shrink" });
  });
  addNotes(s, "Explain the gap from a student's point of view: they usually have a list of skills but no map between those skills and a chosen job role. SkillRadar turns that uncertainty into a concrete readiness report.");
}

// 3. Objectives
{
  const s = slide("Project Objectives", "The system was built around explainable, action-oriented outputs.");
  const steps = [
    ["Extract", "Identify skills from manual input or uploaded resume using Gemini and local parsing."],
    ["Compare", "Map user skills against role-wise technical, soft-skill, and tool requirements."],
    ["Score", "Generate readiness score, tech score, and role label from matched/partial/missing skills."],
    ["Guide", "Recommend learning resources and AI-generated next steps for missing high-priority skills."]
  ];
  steps.forEach((st, i) => {
    const x = 0.75 + i * 3.15;
    card(s, x, 1.65, 2.62, 3.8, { shadow: true });
    s.addShape(pptx.ShapeType.ellipse, { x: x + 0.28, y: 1.98, w: 0.6, h: 0.6, fill: { color: [C.blue, C.teal, C.green, C.amber][i] }, line: { color: [C.blue, C.teal, C.green, C.amber][i] } });
    s.addText(String(i + 1), { x: x + 0.49, y: 2.16, w: 0.18, h: 0.15, fontSize: 10, bold: true, color: "FFFFFF", margin: 0, align: "center" });
    miniTitle(s, st[0], x + 0.28, 2.85, 2.05);
    s.addText(st[1], { x: x + 0.3, y: 3.35, w: 2.0, h: 1.0, fontSize: 10.5, color: C.ink, margin: 0.02, fit: "shrink" });
  });
  s.addText("Final deliverable: a web dashboard that explains what the user has, what the job expects, and what to learn next.", { x: 1.35, y: 6.2, w: 10.6, h: 0.32, fontSize: 13, bold: true, color: C.navy, align: "center", margin: 0 });
  addNotes(s, "Use this slide to show that the project is not just AI extraction. The important contribution is the full loop: extract, compare, score, and guide.");
}

// 4. Workflow
{
  const s = slide("User Workflow", "A simple placement-readiness flow from input to personalized roadmap.");
  const flow = [
    ["1", "Enter skills or upload resume", C.blue],
    ["2", "Select target job role", C.teal],
    ["3", "Extract and normalize skills", C.violet],
    ["4", "Run gap analysis", C.green],
    ["5", "Show score, flags, roadmap", C.amber]
  ];
  flow.forEach((f, i) => {
    const x = 0.65 + i * 2.55;
    s.addShape(pptx.ShapeType.chevron, { x, y: 2.45, w: 2.1, h: 1.15, fill: { color: f[2] }, line: { color: f[2] } });
    s.addText(f[0], { x: x + 0.23, y: 2.72, w: 0.35, h: 0.26, fontSize: 16, bold: true, color: "FFFFFF", margin: 0, align: "center" });
    s.addText(f[1], { x: x + 0.64, y: 2.63, w: 1.1, h: 0.42, fontSize: 9.7, bold: true, color: "FFFFFF", margin: 0, fit: "shrink" });
  });
  card(s, 1.05, 4.45, 3.7, 1.3);
  miniTitle(s, "Green flags", 1.35, 4.72, 2.8, C.green);
  s.addText("Matched skills and bonus strengths already present in the user profile.", { x: 1.35, y: 5.12, w: 3.0, h: 0.36, fontSize: 9.8, color: C.ink, margin: 0, fit: "shrink" });
  card(s, 4.95, 4.45, 3.7, 1.3);
  miniTitle(s, "Red flags", 5.25, 4.72, 2.8, C.red);
  s.addText("Missing high-priority technical skills required by the selected job role.", { x: 5.25, y: 5.12, w: 3.0, h: 0.36, fontSize: 9.8, color: C.ink, margin: 0, fit: "shrink" });
  card(s, 8.85, 4.45, 3.7, 1.3);
  miniTitle(s, "Learning plan", 9.15, 4.72, 2.8, C.amber);
  s.addText("Resources, platforms, estimated time, and Gemini-generated advice.", { x: 9.15, y: 5.12, w: 3.0, h: 0.36, fontSize: 9.8, color: C.ink, margin: 0, fit: "shrink" });
  addNotes(s, "Walk through the app from the user's perspective. The key output is not only a score; it is an explanation of strengths, missing skills, and next learning steps.");
}

// 5. Architecture
{
  const s = slide("System Architecture", "Flask coordinates AI extraction, ML inference, gap analysis, and dashboard responses.");
  const layers = [
    ["Frontend", "HTML, CSS, Vanilla JS, Chart.js", C.blue],
    ["Backend API", "Flask routes: analyze, upload resume, compare roles", C.teal],
    ["AI Layer", "Gemini 2.0 Flash extracts skills and recommendations", C.amber],
    ["ML Layer", "TF-IDF vectorizer + Random Forest classifier", C.violet],
    ["Gap Engine", "Matched, partial, missing, bonus skills, resources", C.green],
    ["Data", "Role skill database + LinkedIn postings dataset", C.ink]
  ];
  layers.forEach((l, i) => {
    const y = 1.35 + i * 0.78;
    card(s, 0.9, y, 11.6, 0.52);
    s.addShape(pptx.ShapeType.rect, { x: 0.9, y, w: 0.12, h: 0.52, fill: { color: l[2] }, line: { color: l[2] } });
    s.addText(l[0], { x: 1.2, y: y + 0.13, w: 1.5, h: 0.2, fontSize: 10.5, bold: true, color: l[2], margin: 0 });
    s.addText(l[1], { x: 3.05, y: y + 0.13, w: 8.8, h: 0.2, fontSize: 10.2, color: C.ink, margin: 0, fit: "shrink" });
  });
  addNotes(s, "Mention that the app uses Flask as the central layer. Gemini is used where AI is useful, while the gap engine remains explainable so the output can be trusted and debugged.");
}

// 6. Gemini
{
  const s = slide("AI Component: Gemini Skill Extraction", "Gemini handles flexible resume language; the app still falls back to local extraction if needed.");
  card(s, 0.8, 1.35, 5.7, 4.7, { shadow: true });
  miniTitle(s, "Resume upload flow", 1.15, 1.72, 4.8);
  bulletList(s, [
    "Accepts PDF and TXT resumes",
    "Extracts resume text using PyPDF2 or UTF-8 decoding",
    "Prompts Gemini to return strict JSON",
    "Stores skills, experience level, and short summary",
    "Falls back to regex/known-skill extraction on API errors"
  ], 1.18, 2.22, 4.8, 11, C.ink, 0.48);
  card(s, 7.05, 1.35, 5.1, 4.7, { fill: "F8FBFD", shadow: true });
  miniTitle(s, "Gemini output schema", 7.4, 1.72, 4.3);
  s.addText("{\n  \"skills\": [\"Python\", \"SQL\", \"Machine Learning\"],\n  \"experience_level\": \"fresher\",\n  \"summary\": \"Candidate profile summary\"\n}", {
    x: 7.4, y: 2.35, w: 4.25, h: 1.45, fontFace: "Courier New", fontSize: 11, color: C.ink, margin: 0.1,
    fill: { color: "FFFFFF" }, line: { color: C.line }
  });
  s.addText("Why AI here?", { x: 7.4, y: 4.25, w: 2.5, h: 0.25, fontSize: 13, bold: true, color: C.teal, margin: 0 });
  s.addText("Resumes use varied wording. AI improves extraction for natural-language descriptions, project sections, and mixed technical/soft skills.", { x: 7.4, y: 4.68, w: 4.2, h: 0.6, fontSize: 10.5, color: C.ink, margin: 0, fit: "shrink" });
  addNotes(s, "Explain that Gemini is not used blindly. The app asks for strict JSON and includes a fallback parser, which makes the feature more robust during demos.");
}

// 7. ML
{
  const s = slide("ML Pipeline", "The classifier learns role patterns from real job descriptions, then supports role-fit analysis.");
  stat(s, 0.8, 1.35, "3.3M", "LinkedIn postings in source dataset", C.blue);
  stat(s, 3.25, 1.35, "3,579", "tech postings extracted", C.teal);
  stat(s, 5.7, 1.35, "500", "TF-IDF features", C.violet);
  stat(s, 8.15, 1.35, "200", "Random Forest trees", C.green);
  stat(s, 10.6, 1.35, "78.35%", "held-out accuracy", C.amber);
  const pipe = [
    "Load dataset",
    "Filter tech roles",
    "TF-IDF + bigrams",
    "Train/test split",
    "Train models",
    "Evaluate accuracy"
  ];
  pipe.forEach((p, i) => {
    const x = 0.72 + i * 2.05;
    card(s, x, 3.65, 1.72, 0.9);
    s.addText(String(i + 1), { x: x + 0.18, y: 3.92, w: 0.25, h: 0.18, fontSize: 10, bold: true, color: C.teal, margin: 0, align: "center" });
    s.addText(p, { x: x + 0.52, y: 3.86, w: 1.03, h: 0.25, fontSize: 9.2, bold: true, color: C.ink, margin: 0, fit: "shrink" });
    if (i < pipe.length - 1) {
      s.addShape(pptx.ShapeType.line, { x: x + 1.72, y: 4.1, w: 0.33, h: 0, line: { color: C.muted, width: 1.1, beginArrowType: "none", endArrowType: "triangle" } });
    }
  });
  s.addText("Role prediction is combined with rule-based skill matching, so the app can give both confidence and a clear explanation.", { x: 1.2, y: 5.75, w: 11.0, h: 0.35, fontSize: 13, bold: true, color: C.navy, align: "center", margin: 0 });
  addNotes(s, "Keep this concise during presentation: dataset, feature engineering, model choice, and where the ML result appears in the app.");
}

// 8. Scoring
{
  const s = slide("Gap Analysis and Scoring", "The final score is explainable: every required skill is classified before the percentage is calculated.");
  card(s, 0.85, 1.35, 5.65, 4.95, { shadow: true });
  miniTitle(s, "Skill status labels", 1.18, 1.72, 4.8);
  const rows = [
    ["Matched", "1.0 point", "User has the required skill", C.green],
    ["Partial", "0.5 point", "Related or overlapping skill found", C.amber],
    ["Missing", "0 point", "Required skill is absent", C.red]
  ];
  rows.forEach((r, i) => {
    const y = 2.35 + i * 0.72;
    s.addShape(pptx.ShapeType.rect, { x: 1.2, y, w: 0.18, h: 0.36, fill: { color: r[3] }, line: { color: r[3] } });
    s.addText(r[0], { x: 1.55, y: y + 0.05, w: 1.0, h: 0.18, fontSize: 10.5, bold: true, color: r[3], margin: 0 });
    s.addText(r[1], { x: 2.72, y: y + 0.05, w: 1.0, h: 0.18, fontSize: 9.8, color: C.ink, margin: 0 });
    s.addText(r[2], { x: 3.75, y: y + 0.05, w: 1.8, h: 0.18, fontSize: 9.2, color: C.muted, margin: 0, fit: "shrink" });
  });
  s.addText("Readiness Score = (matched + partial x 0.5) / total required x 100", {
    x: 1.2, y: 4.78, w: 4.95, h: 0.42, fontFace: "Courier New", fontSize: 12, bold: true, color: C.navy, margin: 0.05,
    fill: { color: "F8FBFD" }, line: { color: C.line }
  });
  card(s, 7.05, 1.35, 5.25, 4.95, { shadow: true });
  miniTitle(s, "Readiness labels", 7.38, 1.72, 4.2);
  const labels = [
    [">= 80%", "Job Ready", C.green],
    [">= 60%", "Almost There", C.amber],
    [">= 40%", "Needs Work", "E67700"],
    ["< 40%", "Early Stage", C.red]
  ];
  labels.forEach((l, i) => {
    s.addShape(pptx.ShapeType.roundRect, { x: 7.45, y: 2.25 + i * 0.62, w: 1.25, h: 0.34, rectRadius: 0.05, fill: { color: l[2] }, line: { color: l[2] } });
    s.addText(l[0], { x: 7.56, y: 2.35 + i * 0.62, w: 1.0, h: 0.12, fontSize: 8.2, bold: true, color: "FFFFFF", margin: 0, align: "center" });
    s.addText(l[1], { x: 8.95, y: 2.31 + i * 0.62, w: 2.2, h: 0.2, fontSize: 10.5, bold: true, color: C.ink, margin: 0 });
  });
  s.addText("Outputs include matched skills, missing skills, partial matches, tech score, bonus skills, and prioritized resources.", { x: 7.42, y: 5.15, w: 4.4, h: 0.45, fontSize: 10.5, color: C.ink, margin: 0, fit: "shrink" });
  addNotes(s, "This slide is important for guide questions because it shows the scoring is transparent. Mention that technical skills are also scored separately.");
}

// 9. Dashboard outputs
{
  const s = slide("Dashboard Outputs", "The report is designed to be immediately useful for a student.");
  const cols = [
    ["Score", "Overall readiness and technical score with role label.", C.blue],
    ["Green flags", "Skills already matching the job role requirements.", C.green],
    ["Red flags", "High-priority missing skills the user should learn first.", C.red],
    ["Resources", "Curated platforms with links and estimated learning time.", C.amber]
  ];
  cols.forEach((c, i) => {
    const x = 0.75 + i * 3.05;
    card(s, x, 1.45, 2.55, 2.15, { shadow: true });
    s.addShape(pptx.ShapeType.ellipse, { x: x + 0.22, y: 1.78, w: 0.44, h: 0.44, fill: { color: c[2] }, line: { color: c[2] } });
    miniTitle(s, c[0], x + 0.78, 1.86, 1.7, c[2]);
    s.addText(c[1], { x: x + 0.28, y: 2.55, w: 1.95, h: 0.48, fontSize: 9.5, color: C.ink, margin: 0, fit: "shrink" });
  });
  card(s, 1.0, 4.35, 11.25, 1.6);
  miniTitle(s, "Example recommendation", 1.35, 4.72, 3.2);
  s.addText("Missing skill: Machine Learning | Platform: Coursera / Andrew Ng | Estimated time: 8-10 weeks | Priority: High", {
    x: 1.35, y: 5.15, w: 9.9, h: 0.28, fontSize: 12, color: C.ink, margin: 0, fit: "shrink"
  });
  addNotes(s, "Use an example role such as Data Scientist. Explain how the same user profile can be compared against different roles, which helps students choose a suitable path.");
}

// 10. Model results
{
  const s = slide("Model Comparison and Selection", "SVM had the highest test accuracy, but Random Forest was selected for deployment suitability.");
  s.addImage({ path: CHART, x: 0.72, y: 1.3, w: 7.3, h: 3.65 });
  card(s, 8.55, 1.35, 3.95, 3.85, { shadow: true });
  miniTitle(s, "Why Random Forest?", 8.9, 1.75, 3.1);
  bulletList(s, [
    "Fast inference for real-time web use",
    "Native predict_proba() for confidence scores",
    "More interpretable than a pure black-box choice",
    "Only about 2% lower than SVM accuracy"
  ], 8.92, 2.25, 3.05, 10.5, C.ink, 0.46);
  s.addText("Deployment choice: Random Forest at 78.35% accuracy", { x: 1.05, y: 5.65, w: 10.8, h: 0.3, fontSize: 13, bold: true, color: C.navy, align: "center", margin: 0 });
  addNotes(s, "A guide may ask why not deploy SVM. Answer: SVM scored slightly higher, but Random Forest made the dashboard easier because probability estimates and faster inference fit the web app better.");
}

// 11. Features and endpoints
{
  const s = slide("Implementation Highlights", "The backend exposes focused APIs and keeps the analysis logic modular.");
  card(s, 0.85, 1.35, 5.8, 4.95, { shadow: true });
  miniTitle(s, "Core API endpoints", 1.18, 1.75, 4.8);
  const endpoints = [
    ["GET /api/roles", "List supported roles"],
    ["POST /api/analyze", "Run skill gap analysis"],
    ["POST /api/upload-resume", "Extract resume skills"],
    ["POST /api/compare-roles", "Compare fit across roles"]
  ];
  endpoints.forEach((e, i) => {
    s.addText(e[0], { x: 1.2, y: 2.35 + i * 0.63, w: 2.0, h: 0.18, fontFace: "Courier New", fontSize: 9.5, bold: true, color: C.teal, margin: 0 });
    s.addText(e[1], { x: 3.55, y: 2.35 + i * 0.63, w: 2.4, h: 0.18, fontSize: 9.7, color: C.ink, margin: 0, fit: "shrink" });
  });
  card(s, 7.2, 1.35, 5.0, 4.95, { shadow: true });
  miniTitle(s, "Supported roles", 7.55, 1.75, 4.1);
  bulletList(s, [
    "Software Development Engineer",
    "Data Scientist / Data Analyst",
    "Machine Learning Engineer",
    "Frontend / Backend Developer",
    "DevOps, Product Manager, Cybersecurity",
    "Quantitative Analyst profile"
  ], 7.58, 2.25, 3.95, 10.3, C.ink, 0.43);
  addNotes(s, "This slide helps show that the implementation is complete, with both front-end and back-end support. Mention that app.py handles routes and analyzer.py handles the scoring logic.");
}

// 12. Future scope
{
  const s = slide("Limitations and Future Scope", "The current system is functional; the next step is making it more dynamic and semantically stronger.");
  card(s, 0.85, 1.35, 5.8, 4.95, { shadow: true });
  miniTitle(s, "Current limitations", 1.18, 1.75, 4.8, C.red);
  bulletList(s, [
    "Role skill database is curated, not continuously updated",
    "Partial matching is lexical and may miss deeper semantic similarity",
    "Resume extraction depends on clean PDF text extraction",
    "Resources are useful but not yet personalized by learning level"
  ], 1.2, 2.3, 4.9, 10.5, C.ink, 0.5);
  card(s, 7.2, 1.35, 5.0, 4.95, { shadow: true });
  miniTitle(s, "Future enhancements", 7.55, 1.75, 4.1, C.green);
  bulletList(s, [
    "Live job posting APIs for fresh market demand",
    "BERT or sentence embeddings for semantic skill matching",
    "Progress tracking dashboard for weekly learning goals",
    "Company-specific readiness profiles",
    "Interview prep links mapped to missing skills"
  ], 7.58, 2.3, 3.95, 10.5, C.ink, 0.5);
  addNotes(s, "Frame limitations honestly. Then show future scope as a clear extension path, especially semantic matching and real-time job data.");
}

// 13. Closing
{
  const s = slide("Conclusion", "SkillRadar converts a resume or skill list into a role-specific placement plan.");
  card(s, 1.0, 1.45, 11.25, 3.65, { shadow: true });
  s.addText("What the project demonstrates", { x: 1.45, y: 1.85, w: 5.0, h: 0.28, fontSize: 15, bold: true, color: C.navy, margin: 0 });
  bulletList(s, [
    "Practical AI integration using Gemini for skill extraction and recommendations",
    "ML model training and deployment using TF-IDF and Random Forest",
    "Explainable scoring through matched, partial, and missing skill logic",
    "Student-focused output: green flags, red flags, and learning roadmap"
  ], 1.48, 2.42, 9.7, 12, C.ink, 0.5);
  s.addText("Live Demo: skill-gap-detector-gp3o.onrender.com", { x: 1.45, y: 5.78, w: 5.6, h: 0.26, fontSize: 11.5, color: C.teal, bold: true, margin: 0 });
  s.addText("GitHub: github.com/SpoorthySM/skill-gap-detector", { x: 1.45, y: 6.18, w: 5.8, h: 0.26, fontSize: 11.5, color: C.teal, bold: true, margin: 0 });
  s.addText("Thank you", { x: 8.55, y: 5.7, w: 2.7, h: 0.45, fontSize: 28, bold: true, color: C.navy, align: "center", margin: 0 });
  s.addText("Questions?", { x: 8.95, y: 6.24, w: 1.9, h: 0.25, fontSize: 14, color: C.muted, align: "center", margin: 0 });
  addNotes(s, "Close by summarizing the value: the project helps students know where they stand and what to learn next for a specific role.");
}

pptx.writeFile({ fileName: OUT });
console.log(OUT);
