const pptxgen = require("pptxgenjs");
const path = require("path");

const COLORS = {
  primary: "36454F",
  secondary: "A7BEAE",
  accent: "B85042",
  sand: "E7E8D1",
  white: "FFFFFF",
  dark: "212121",
  muted: "5A6A72",
};

function addHeader(slide, pres, title, subtitle) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0,
    y: 0,
    w: 10,
    h: 1.05,
    fill: { color: COLORS.primary },
  });
  slide.addText(title, {
    x: 0.5,
    y: 0.18,
    w: 9,
    h: 0.5,
    fontSize: 24,
    bold: true,
    color: COLORS.white,
    fontFace: "Georgia",
    margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.5,
      y: 0.62,
      w: 9,
      h: 0.3,
      fontSize: 11,
      color: COLORS.sand,
      fontFace: "Calibri",
      margin: 0,
    });
  }
}

function addBullets(slide, items, x, y, w, h) {
  slide.addText(
    items.map((text, i) => ({
      text,
      options: { bullet: true, breakLine: i < items.length - 1 },
    })),
    {
      x,
      y,
      w,
      h,
      fontSize: 14,
      color: COLORS.dark,
      fontFace: "Calibri",
      valign: "top",
    }
  );
}

function addStatCard(slide, pres, x, y, value, label) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x,
    y,
    w: 2.1,
    h: 1.35,
    fill: { color: COLORS.sand },
    line: { color: COLORS.secondary, width: 1 },
    rectRadius: 0.08,
  });
  slide.addText(value, {
    x: x + 0.1,
    y: y + 0.2,
    w: 1.9,
    h: 0.55,
    fontSize: 28,
    bold: true,
    color: COLORS.accent,
    align: "center",
    fontFace: "Georgia",
    margin: 0,
  });
  slide.addText(label, {
    x: x + 0.1,
    y: y + 0.78,
    w: 1.9,
    h: 0.4,
    fontSize: 10,
    color: COLORS.muted,
    align: "center",
    fontFace: "Calibri",
    margin: 0,
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "FGMD Team";
pres.title = "FGMD Development Plan";

// Slide 1 - Title
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.primary };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6,
    y: 1.2,
    w: 8.8,
    h: 3.2,
    fill: { color: COLORS.accent, transparency: 15 },
  });
  slide.addText("FGMD", {
    x: 0.8,
    y: 1.5,
    w: 8.4,
    h: 0.9,
    fontSize: 44,
    bold: true,
    color: COLORS.white,
    fontFace: "Georgia",
    margin: 0,
  });
  slide.addText("Funeral Goods Management Dashboard", {
    x: 0.8,
    y: 2.35,
    w: 8.4,
    h: 0.5,
    fontSize: 20,
    color: COLORS.sand,
    fontFace: "Calibri",
    margin: 0,
  });
  slide.addText("상조물품현황 · Project Development Plan", {
    x: 0.8,
    y: 3.0,
    w: 8.4,
    h: 0.4,
    fontSize: 16,
    color: COLORS.secondary,
    fontFace: "Calibri",
    margin: 0,
  });
  slide.addText("Demo v1 Complete · June 2026 · localhost:8501", {
    x: 0.8,
    y: 4.7,
    w: 8.4,
    h: 0.35,
    fontSize: 12,
    color: COLORS.sand,
    fontFace: "Calibri",
    margin: 0,
  });
}

// Slide 2 - Executive Summary
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Executive Summary", "What FGMD delivers today");
  addBullets(
    slide,
    [
      "Streamlit dashboard for regional funeral-goods inventory across Korea",
      "Editable stock table with live map visualization (1 icon = 10 boxes)",
      "Order sheet: 빈소, 가족관계, 조문객 수 with automatic box calculation",
      "Orders deduct warehouse stock, save records, print HTML sheet, email via SMTP",
      "Running locally at http://localhost:8501",
    ],
    0.6,
    1.35,
    5.8,
    3.8
  );
  addStatCard(slide, pres, 6.7, 1.55, "5", "Regions");
  addStatCard(slide, pres, 6.7, 3.1, "v1", "Demo");
  addStatCard(slide, pres, 8.0, 1.55, "10", "Modules");
  addStatCard(slide, pres, 8.0, 3.1, "8501", "Port");
}

// Slide 3 - Completed Phase 1
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Phase 1 — Completed", "Demo v1 deliverables");
  const items = [
    "Inventory table: 서울, 오산, 전라, 경상, 충청 + 합계 column",
    "Editable stock with save → map updates immediately",
    "South Korea Folium map with scaled box DivIcons",
    "Order form with warehouse selection and stock validation",
    "JSON persistence: inventory.json + orders.json",
    "Printable HTML order sheet + SMTP email to samchully",
  ];
  addBullets(slide, items, 0.6, 1.35, 8.8, 3.9);
}

// Slide 4 - Architecture
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "System Architecture", "Component structure");
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.55,
    y: 1.35,
    w: 2.7,
    h: 3.5,
    fill: { color: COLORS.sand },
    line: { color: COLORS.secondary, width: 1 },
    rectRadius: 0.06,
  });
  slide.addText("UI Layer", {
    x: 0.7,
    y: 1.5,
    w: 2.4,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: COLORS.primary,
    margin: 0,
  });
  addBullets(
    slide,
    ["app.py", "inventory_table", "map_view", "order_form"],
    0.75,
    1.95,
    2.35,
    2.5
  );

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 3.55,
    y: 1.35,
    w: 2.9,
    h: 3.5,
    fill: { color: COLORS.sand },
    line: { color: COLORS.secondary, width: 1 },
    rectRadius: 0.06,
  });
  slide.addText("Services", {
    x: 3.7,
    y: 1.5,
    w: 2.6,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: COLORS.primary,
    margin: 0,
  });
  addBullets(
    slide,
    ["order_logic", "storage", "print_service", "email_service"],
    3.75,
    1.95,
    2.55,
    2.5
  );

  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 6.75,
    y: 1.35,
    w: 2.7,
    h: 3.5,
    fill: { color: COLORS.sand },
    line: { color: COLORS.secondary, width: 1 },
    rectRadius: 0.06,
  });
  slide.addText("Data", {
    x: 6.9,
    y: 1.5,
    w: 2.4,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: COLORS.primary,
    margin: 0,
  });
  addBullets(
    slide,
    ["inventory.json", "orders.json", "secrets.toml", "config.py"],
    6.95,
    1.95,
    2.35,
    2.5
  );
}

// Slide 5 - Order Logic
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Order & Inventory Rules", "Business logic implemented");
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6,
    y: 1.4,
    w: 4.2,
    h: 3.4,
    fill: { color: COLORS.sand },
  });
  slide.addText("Box calculation", {
    x: 0.8,
    y: 1.55,
    w: 3.8,
    h: 0.35,
    fontSize: 16,
    bold: true,
    color: COLORS.accent,
    margin: 0,
  });
  addBullets(
    slide,
    [
      "조문객 수 < 300 → send 1 box",
      "Otherwise → ceil(visitors / 300) boxes",
      "가족관계 recorded, not used in logic",
      "빈소 = delivery address",
    ],
    0.8,
    2.0,
    3.7,
    2.5
  );

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 5.2,
    y: 1.4,
    w: 4.2,
    h: 3.4,
    fill: { color: COLORS.sand },
  });
  slide.addText("Inventory rules", {
    x: 5.4,
    y: 1.55,
    w: 3.8,
    h: 0.35,
    fontSize: 16,
    bold: true,
    color: COLORS.accent,
    margin: 0,
  });
  addBullets(
    slide,
    [
      "Edit regional stock in table → save",
      "Map icon size = stock ÷ 10",
      "Select 출고 창고 for fulfillment",
      "ORDER blocked if warehouse stock insufficient",
      "Stock deducted on successful order",
    ],
    5.4,
    2.0,
    3.7,
    2.8
  );
}

// Slide 6 - Phase 2 Deployment
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Phase 2 — Deployment", "Next sprint priorities");
  addBullets(
    slide,
    [
      "Push repository to GitHub (code + plan + this deck)",
      "Deploy via Streamlit Community Cloud (not Vercel — Streamlit needs a Python server)",
      "Configure production SMTP secrets in Streamlit Cloud",
      "Add README and setup documentation",
      "Optional: GitHub Actions smoke test on push",
    ],
    0.6,
    1.35,
    5.5,
    3.8
  );
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 6.4,
    y: 1.5,
    w: 3.0,
    h: 3.2,
    fill: { color: COLORS.primary },
    rectRadius: 0.08,
  });
  slide.addText("Recommended Host", {
    x: 6.55,
    y: 1.75,
    w: 2.7,
    h: 0.35,
    fontSize: 14,
    bold: true,
    color: COLORS.white,
    margin: 0,
  });
  slide.addText("Streamlit Cloud", {
    x: 6.55,
    y: 2.35,
    w: 2.7,
    h: 0.6,
    fontSize: 22,
    bold: true,
    color: COLORS.secondary,
    margin: 0,
  });
  slide.addText("Free tier · Native Streamlit support · GitHub integration", {
    x: 6.55,
    y: 3.2,
    w: 2.7,
    h: 1.0,
    fontSize: 11,
    color: COLORS.sand,
    fontFace: "Calibri",
    margin: 0,
  });
}

// Slide 7 - Phase 3 Enhancements
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Phase 3 — Enhancements", "Future feature backlog");
  const features = [
    ["Low-stock alerts", "Red map markers below threshold"],
    ["Order history", "Collapsible past orders table"],
    ["Auto warehouse", "Suggest region from 빈소 address"],
    ["PDF export", "Company letterhead order sheets"],
    ["KPI strip", "총 재고, 금일 주문, 발송 예정"],
    ["Admin auth", "Role-based access control"],
  ];
  features.forEach(([title, desc], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.6 + col * 4.7;
    const y = 1.4 + row * 1.25;
    slide.addShape(pres.shapes.OVAL, {
      x,
      y: y + 0.08,
      w: 0.35,
      h: 0.35,
      fill: { color: COLORS.accent },
    });
    slide.addText(String(i + 1), {
      x,
      y: y + 0.08,
      w: 0.35,
      h: 0.35,
      fontSize: 12,
      bold: true,
      color: COLORS.white,
      align: "center",
      valign: "middle",
      margin: 0,
    });
    slide.addText(title, {
      x: x + 0.5,
      y,
      w: 4.0,
      h: 0.3,
      fontSize: 14,
      bold: true,
      color: COLORS.primary,
      margin: 0,
    });
    slide.addText(desc, {
      x: x + 0.5,
      y: y + 0.32,
      w: 4.0,
      h: 0.3,
      fontSize: 11,
      color: COLORS.muted,
      margin: 0,
    });
  });
}

// Slide 8 - Timeline
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.white };
  addHeader(slide, pres, "Roadmap Timeline", "Suggested delivery schedule");
  const phases = [
    { label: "Phase 1", period: "Jun 2026", text: "Demo v1 local", done: true },
    { label: "Phase 2", period: "Jun 2026", text: "GitHub + Streamlit Cloud", done: false },
    { label: "Phase 3", period: "Jul 2026", text: "Alerts, history, PDF", done: false },
    { label: "Phase 4", period: "Aug 2026", text: "Production hardening", done: false },
  ];
  phases.forEach((p, i) => {
    const x = 0.7 + i * 2.3;
    slide.addShape(pres.shapes.RECTANGLE, {
      x,
      y: 2.0,
      w: 2.0,
      h: 0.12,
      fill: { color: p.done ? COLORS.accent : COLORS.secondary },
    });
    slide.addShape(pres.shapes.OVAL, {
      x: x + 0.82,
      y: 1.72,
      w: 0.36,
      h: 0.36,
      fill: { color: p.done ? COLORS.accent : COLORS.primary },
    });
    slide.addText(p.label, {
      x,
      y: 2.25,
      w: 2.0,
      h: 0.35,
      fontSize: 14,
      bold: true,
      color: COLORS.primary,
      align: "center",
      margin: 0,
    });
    slide.addText(p.period, {
      x,
      y: 2.6,
      w: 2.0,
      h: 0.3,
      fontSize: 11,
      color: COLORS.muted,
      align: "center",
      margin: 0,
    });
    slide.addText(p.text, {
      x,
      y: 2.95,
      w: 2.0,
      h: 0.8,
      fontSize: 11,
      color: COLORS.dark,
      align: "center",
      margin: 0,
    });
  });
}

// Slide 9 - Next Steps
{
  const slide = pres.addSlide();
  slide.background = { color: COLORS.primary };
  slide.addText("Next Steps", {
    x: 0.8,
    y: 1.0,
    w: 8.4,
    h: 0.7,
    fontSize: 36,
    bold: true,
    color: COLORS.white,
    fontFace: "Georgia",
    margin: 0,
  });
  addBullets(
    slide,
    [
      "Authenticate GitHub CLI: gh auth login",
      "Push repo: gh repo create fgmd --public --source=. --push",
      "Deploy on share.streamlit.io from GitHub",
      "Add SMTP secrets in Streamlit Cloud settings",
      "Share public demo URL with stakeholders",
    ],
    0.9,
    1.9,
    8.2,
    3.0
  );
  slide.addText("Repository: C:\\Users\\SKILLSUPPORT\\fgmd", {
    x: 0.8,
    y: 4.9,
    w: 8.4,
    h: 0.35,
    fontSize: 12,
    color: COLORS.sand,
    margin: 0,
  });
}

const outPath = path.join(__dirname, "FGMD_Development_Plan.pptx");
pres.writeFile({ fileName: outPath });
console.log("Created:", outPath);