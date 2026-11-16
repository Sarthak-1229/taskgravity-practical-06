import os
import subprocess
import html
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def generate_docx():
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)

    # Header
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = p_dept.add_run("Department of Computer Engineering (Software Engineering)\n")
    r_dept.font.size = Pt(14)
    r_dept.font.bold = True
    r_dept.font.color.rgb = RGBColor(15, 23, 42)

    r_sub = p_dept.add_run("Web Technology Laboratory — Academic Year 2026-27\n")
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Practical No. 06: Full CRUD REST API with Persistence and Validation")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(37, 99, 235)

    # Metadata Table
    meta_table = doc.add_table(rows=2, cols=4)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        [("Name:", "Sarthak Bhosale"), ("PRN:", "202401100051")],
        [("Batch:", "TY SE-A2"), ("Roll No:", "A50")]
    ]
    for row_idx, row in enumerate(meta_data):
        col_offset = 0
        for label, val in row:
            cell_lbl = meta_table.cell(row_idx, col_offset)
            cell_val = meta_table.cell(row_idx, col_offset + 1)
            cell_lbl.text = label
            cell_lbl.paragraphs[0].runs[0].font.bold = True
            cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(71, 85, 105)
            cell_val.text = val
            cell_val.paragraphs[0].runs[0].font.bold = True
            cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(15, 23, 42)
            set_cell_bg(cell_lbl, "F1F5F9")
            set_cell_bg(cell_val, "FFFFFF")
            set_cell_margins(cell_lbl, 80, 80, 100, 100)
            set_cell_margins(cell_val, 80, 80, 100, 100)
            col_offset += 2

    doc.add_paragraph()

    def add_section_heading(num_str, title_str):
        h = doc.add_paragraph()
        r = h.add_run(f"{num_str}. {title_str}")
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        return h

    def add_code_block(title, code_str):
        p_t = doc.add_paragraph()
        r_t = p_t.add_run(title)
        r_t.font.bold = True
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(37, 99, 235)
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)

        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "0F172A")
        set_cell_margins(cell, 120, 120, 150, 150)
        p = cell.paragraphs[0]
        r = p.add_run(code_str)
        r.font.name = 'Consolas'
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(241, 245, 249)
        doc.add_paragraph()

    # 1. Aim
    add_section_heading("1", "Aim")
    doc.add_paragraph(
        "To design, develop, test, and deploy a comprehensive, production-grade CRUD REST API for TaskGravity using "
        "Express.js, asynchronous file-based persistence via Node.js fs/promises, schema validation, query filtering, "
        "pagination, sorting, and standardized HTTP status codes."
    )

    # 2. Problem Statement
    add_section_heading("2", "Problem Statement")
    doc.add_paragraph(
        "Construct an autonomous REST service providing complete persistence life-cycle management for tasks without third-party "
        "database dependencies. The backend must support POST (creation with validation), GET (filtering by status/priority, pagination, "
        "sorting), GET by ID, PUT (full/partial update), and DELETE (idempotent removal), persisting all state to a thread-safe "
        "JSON store file while exposing a responsive client dashboard."
    )

    # 3. Theory & Concept Review
    add_section_heading("3", "Theory & Concept Review")
    doc.add_paragraph(
        "3.1 REST Architectural Constraints\n"
        "REST (Representational State Transfer) mandates a stateless client-server protocol. Each request contains all contextual "
        "information necessary for the server to fulfill it, utilizing standard HTTP verbs (GET, POST, PUT, DELETE) and standardized "
        "status codes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Server Error)."
    )
    doc.add_paragraph(
        "3.2 Asynchronous File Persistence (fs/promises)\n"
        "Node's fs/promises API enables non-blocking file reads and writes using async/await. Writes serialize the in-memory array "
        "to disk atomically, ensuring data survives server process restarts."
    )
    doc.add_paragraph(
        "3.3 Layered Architecture (MVC Separation)\n"
        "Separating the application into Routes (HTTP routing), Controllers/Handlers (business orchestration), Models/Store "
        "(persistence abstraction), and Validators (input sanitation) guarantees code modularity and maintainability."
    )

    # 4. Software & Hardware Requirements
    add_section_heading("4", "Software & Hardware Requirements")
    req_table = doc.add_table(rows=5, cols=2)
    req_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    req_data = [
        ("Operating System", "Microsoft Windows 11 x64 / Linux x64 (Render PaaS)"),
        ("Runtime & Modules", "Node.js v20.x, Express.js v4.x, cors, dotenv, fs/promises"),
        ("Development Tools", "Antigravity IDE, Visual Studio Code"),
        ("API Testing & Diagnostics", "Postman Collection Runner, Chrome DevTools"),
        ("Deployment & Versioning", "Git, GitHub, Render Cloud Web Service")
    ]
    for idx, (lbl, val) in enumerate(req_data):
        c1, c2 = req_table.cell(idx, 0), req_table.cell(idx, 1)
        c1.text = lbl
        c1.paragraphs[0].runs[0].font.bold = True
        c2.text = val
        set_cell_bg(c1, "F8FAFC")
        set_cell_bg(c2, "FFFFFF")
        set_cell_margins(c1, 80, 80, 100, 100)
        set_cell_margins(c2, 80, 80, 100, 100)
    doc.add_paragraph()

    # 5. Design & Architectural Implementation
    add_section_heading("5", "Design & Architectural Implementation")
    doc.add_paragraph(
        "1. Store Model: taskStore.js encapsulates file reading, writing, and query operations on data/tasks.json.\n"
        "2. Routing: routes/taskRoutes.js defines REST endpoints with validation middleware mounted.\n"
        "3. Validation: taskValidator.js sanitizes titles, enforces valid priority levels, and checks allowed status transitions.\n"
        "4. Pagination & Filters: Query parameters ?status=..., ?priority=..., ?page=..., and ?limit=... slice data dynamically.\n"
        "5. Client Dashboard: public/app.js handles real-time task creation, status updates, and deletion via fetch requests."
    )

    # 6. Source Code
    add_section_heading("6", "Source Code Implementation")
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical6"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = read_code("server.js")
    task_routes_js = read_code(r"routes\taskRoutes.js")
    task_store_js = read_code(r"models\taskStore.js")
    task_val_js = read_code(r"validators\taskValidator.js")
    app_js = read_code(r"public\app.js")

    add_code_block("6.1 server.js (Express Application Entrypoint & Static Server)", server_js)
    add_code_block("6.2 routes/taskRoutes.js (RESTful CRUD Route Handlers)", task_routes_js)
    add_code_block("6.3 models/taskStore.js (Asynchronous File-Based Persistence Model)", task_store_js)
    add_code_block("6.4 validators/taskValidator.js (Input Validation Middleware)", task_val_js)
    add_code_block("6.5 public/app.js (Client Dashboard Controller)", app_js)

    # 7. Verification & Test Results
    add_section_heading("7", "Verification & Test Results")
    test_table = doc.add_table(rows=6, cols=3)
    test_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    test_headers = ["Endpoint / Operation", "Test Scenario & Observed Output", "Status"]
    for c_idx, h in enumerate(test_headers):
        cell = test_table.cell(0, c_idx)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_bg(cell, "F1F5F9")
        set_cell_margins(cell, 80, 80, 100, 100)
    
    tests = [
        ("GET /api/tasks", "Returns 200 OK with paginated list, total count, and metadata headers.", "Passed"),
        ("POST /api/tasks", "Creates new task record with ISO timestamp, persists to tasks.json, returns 201 Created.", "Passed"),
        ("GET /api/tasks/:id", "Retrieves matching task record; returns 404 Not Found for non-existent ID.", "Passed"),
        ("PUT /api/tasks/:id", "Updates specified task attributes and writes updated JSON state to disk.", "Passed"),
        ("DELETE /api/tasks/:id", "Purges task record from disk and returns 200 OK confirmation payload.", "Passed")
    ]
    for r_idx, row in enumerate(tests, start=1):
        for c_idx, val in enumerate(row):
            cell = test_table.cell(r_idx, c_idx)
            cell.text = val
            if c_idx == 2:
                cell.paragraphs[0].runs[0].font.bold = True
                set_cell_bg(cell, "DCFCE7")
            else:
                set_cell_bg(cell, "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
    doc.add_paragraph()

    # 8. Conclusion
    add_section_heading("8", "Conclusion")
    doc.add_paragraph(
        "Practical 06 successfully establishes a full-lifecycle CRUD REST API with asynchronous file persistence. "
        "By enforcing a clean architectural separation between routing, controllers, file-based data stores, and input validators, "
        "the service provides a durable, testable, and robust task management backend. The entire application is deployed "
        "and accessible live on Render Cloud."
    )

    # Links Box
    p_box = doc.add_paragraph()
    p_box.paragraph_format.space_before = Pt(14)
    tbl_links = doc.add_table(rows=1, cols=1)
    tbl_links.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_links = tbl_links.cell(0, 0)
    set_cell_bg(c_links, "F8FAFC")
    set_cell_margins(c_links, 120, 120, 150, 150)
    p_l = c_links.paragraphs[0]
    r_lh = p_l.add_run("Project Links & Deployment Information:\n")
    r_lh.font.bold = True
    r_lh.font.size = Pt(11)
    r_lh.font.color.rgb = RGBColor(15, 23, 42)

    r_gh = p_l.add_run("GitHub Link / Code Link: ")
    r_gh.font.bold = True
    p_l.add_run("https://github.com/Sarthak-1229/taskgravity-practical-06\n")

    r_live = p_l.add_run("Live Deployment Link: ")
    r_live.font.bold = True
    p_l.add_run("https://taskgravity-practical-06.onrender.com")

    docx_path = r"D:\_TY\Web-Tech\Practicals\Practical6\Practical_06_Report.docx"
    doc.save(docx_path)
    print(f"Generated DOCX: {docx_path}")

def generate_pdf():
    base_dir = r"D:\_TY\Web-Tech\Practicals\Practical6"
    def read_code(rel_path):
        fpath = os.path.join(base_dir, rel_path)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return f.read()
        return "// File not found"

    server_js = html.escape(read_code("server.js"))
    task_routes_js = html.escape(read_code(r"routes\taskRoutes.js"))
    task_store_js = html.escape(read_code(r"models\taskStore.js"))
    task_val_js = html.escape(read_code(r"validators\taskValidator.js"))
    app_js = html.escape(read_code(r"public\app.js"))

    report_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Practical 06 Report - Sarthak Bhosale</title>
<style>
  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: counter(page);
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    line-height: 1.55;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }}
  .header {{
    text-align: center;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 18px;
  }}
  .dept-title {{
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.2px;
    text-transform: uppercase;
  }}
  .sub-title {{
    font-size: 10pt;
    font-weight: 600;
    color: #64748b;
    margin-top: 2px;
  }}
  .prac-title {{
    font-size: 14pt;
    font-weight: 800;
    color: #2563eb;
    margin-top: 8px;
  }}
  .meta-grid {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    font-size: 9.5pt;
  }}
  .meta-grid td {{
    border: 1px solid #cbd5e1;
    padding: 6px 10px;
  }}
  .meta-grid .lbl {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #475569;
    width: 15%;
  }}
  .meta-grid .val {{
    font-weight: 700;
    color: #0f172a;
    width: 35%;
  }}
  h2.sec-title {{
    font-size: 11pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    margin-top: 20px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}
  h3.subsec-title {{
    font-size: 10pt;
    font-weight: 700;
    color: #2563eb;
    margin-top: 14px;
    margin-bottom: 4px;
  }}
  p, li {{
    font-size: 9.5pt;
    color: #334155;
    text-align: justify;
    margin-top: 4px;
    margin-bottom: 6px;
  }}
  ul, ol {{
    padding-left: 20px;
    margin-top: 4px;
    margin-bottom: 8px;
  }}
  .code-block {{
    background-color: #0f172a;
    color: #f8fafc;
    font-family: "Consolas", "Fira Code", monospace;
    font-size: 8pt;
    line-height: 1.4;
    padding: 10px 14px;
    border-radius: 4px;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 8px 0 14px 0;
  }}
  .data-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 9pt;
  }}
  .data-table th, .data-table td {{
    border: 1px solid #cbd5e1;
    padding: 7px 10px;
    text-align: left;
  }}
  .data-table th {{
    background-color: #f8fafc;
    font-weight: 700;
    color: #0f172a;
  }}
  .badge-pass {{
    color: #15803d;
    font-weight: 700;
    background-color: #dcfce7;
    padding: 2px 6px;
    border-radius: 3px;
    display: inline-block;
  }}
  .links-box {{
    margin-top: 20px;
    padding: 12px 14px;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}
  .links-box a {{
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>

<div class="header">
  <div class="dept-title">Department of Computer Engineering (Software Engineering)</div>
  <div class="sub-title">Web Technology Laboratory — Academic Year 2026-27</div>
  <div class="prac-title">Practical No. 06: Full CRUD REST API with Persistence and Validation</div>
</div>

<table class="meta-grid">
  <tr>
    <td class="lbl">Name:</td>
    <td class="val">Sarthak Bhosale</td>
    <td class="lbl">PRN:</td>
    <td class="val">202401100051</td>
  </tr>
  <tr>
    <td class="lbl">Batch:</td>
    <td class="val">TY SE-A2</td>
    <td class="lbl">Roll No:</td>
    <td class="val">A50</td>
  </tr>
</table>

<h2 class="sec-title">1. Aim</h2>
<p>
To design, develop, test, and deploy a comprehensive, production-grade CRUD REST API for TaskGravity using Express.js, asynchronous file-based persistence via Node.js fs/promises, schema validation, query filtering, pagination, sorting, and standardized HTTP status codes.
</p>

<h2 class="sec-title">2. Problem Statement</h2>
<p>
Construct an autonomous REST service providing complete persistence life-cycle management for tasks without third-party database dependencies. The backend must support POST (creation with validation), GET (filtering by status/priority, pagination, sorting), GET by ID, PUT (full/partial update), and DELETE (idempotent removal), persisting all state to a thread-safe JSON store file while exposing a responsive client dashboard.
</p>

<h2 class="sec-title">3. Theory & Concept Review</h2>
<p>
<strong>3.1 REST Architectural Principles:</strong> REST utilizes stateless communications and standard HTTP verbs (GET, POST, PUT, DELETE) mapping cleanly to CRUD actions. Proper status codes (200, 201, 400, 404, 500) communicate operation outcomes reliably.
</p>
<p>
<strong>3.2 Asynchronous File Persistence (fs/promises):</strong> Using non-blocking promise-based filesystem calls avoids blocking the Node.js event loop during disk writes, ensuring persistence through process restarts.
</p>
<p>
<strong>3.3 Layered MVC Modularization:</strong> Isolating routes, controllers, stores, and validators achieves strict DRY software design and ease of test automation.
</p>

<h2 class="sec-title">4. Software & Hardware Requirements</h2>
<table class="data-table">
  <tr><th style="width: 30%;">Component</th><th>Specification</th></tr>
  <tr><td>Operating System</td><td>Microsoft Windows 11 x64 / Linux x64 (Render PaaS)</td></tr>
  <tr><td>Runtime & Modules</td><td>Node.js v20.x, Express.js v4.x, cors, dotenv, fs/promises</td></tr>
  <tr><td>Development Tools</td><td>Antigravity IDE, Visual Studio Code</td></tr>
  <tr><td>API Testing & Diagnostics</td><td>Postman Collection Runner, Chrome DevTools</td></tr>
  <tr><td>Deployment & Versioning</td><td>Git, GitHub, Render Cloud Web Service</td></tr>
</table>

<h2 class="sec-title">5. Design & Architectural Implementation</h2>
<ol>
  <li>Encapsulate file read/write operations within <code>models/taskStore.js</code>.</li>
  <li>Define REST routes with input validator in <code>routes/taskRoutes.js</code>.</li>
  <li>Sanitize title, category, priority, and status fields via <code>validators/taskValidator.js</code>.</li>
  <li>Implement query filters (<code>?status=</code>, <code>?priority=</code>, <code>?page=</code>, <code>?limit=</code>).</li>
  <li>Build client dashboard in <code>public/app.js</code> with dynamic CRUD operations.</li>
</ol>

<h2 class="sec-title">6. Source Code Implementation</h2>

<h3 class="subsec-title">6.1 server.js (Express Application Entrypoint & Static Server)</h3>
<pre class="code-block">{server_js}</pre>

<h3 class="subsec-title">6.2 routes/taskRoutes.js (RESTful CRUD Route Handlers)</h3>
<pre class="code-block">{task_routes_js}</pre>

<h3 class="subsec-title">6.3 models/taskStore.js (Asynchronous File-Based Persistence Model)</h3>
<pre class="code-block">{task_store_js}</pre>

<h3 class="subsec-title">6.4 validators/taskValidator.js (Input Validation Middleware)</h3>
<pre class="code-block">{task_val_js}</pre>

<h3 class="subsec-title">6.5 public/app.js (Client Dashboard Controller)</h3>
<pre class="code-block">{app_js}</pre>

<h2 class="sec-title">7. Verification & Test Results</h2>
<table class="data-table">
  <thead>
    <tr>
      <th>Endpoint / Operation</th>
      <th>Test Scenario & Observed Output</th>
      <th>Verification Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>GET /api/tasks</strong></td>
      <td>Returns 200 OK with paginated list, total count, and metadata headers.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>POST /api/tasks</strong></td>
      <td>Creates new task record with ISO timestamp, persists to tasks.json, returns 201 Created.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>GET /api/tasks/:id</strong></td>
      <td>Retrieves matching task record; returns 404 Not Found for non-existent ID.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>PUT /api/tasks/:id</strong></td>
      <td>Updates specified task attributes and writes updated JSON state to disk.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
    <tr>
      <td><strong>DELETE /api/tasks/:id</strong></td>
      <td>Purges task record from disk and returns 200 OK confirmation payload.</td>
      <td><span class="badge-pass">Passed</span></td>
    </tr>
  </tbody>
</table>

<h2 class="sec-title">8. Conclusion</h2>
<p>
Practical 06 successfully establishes a full-lifecycle CRUD REST API with asynchronous file persistence. By enforcing a clean architectural separation between routing, controllers, file-based data stores, and input validators, the service provides a durable, testable, and robust task management backend. The entire application is deployed and accessible live on Render Cloud.
</p>

<div class="links-box">
  <div style="font-weight: 700; font-size: 11pt; margin-bottom: 6px; color: #0f172a;">Project Links & Deployment Information</div>
  <div><strong>GitHub Link / Code Link:</strong> <a href="https://github.com/Sarthak-1229/taskgravity-practical-06" target="_blank">https://github.com/Sarthak-1229/taskgravity-practical-06</a></div>
  <div style="margin-top: 4px;"><strong>Live Deployment Link:</strong> <a href="https://taskgravity-practical-06.onrender.com" target="_blank">https://taskgravity-practical-06.onrender.com</a></div>
</div>

</body>
</html>
"""
    html_report_path = r"D:\_TY\Web-Tech\Practicals\Practical6\report_temp.html"
    pdf_report_path = r"D:\_TY\Web-Tech\Practicals\Practical6\Practical_06_Report.pdf"

    with open(html_report_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    chrome_cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_report_path}",
        html_report_path
    ]
    subprocess.run(chrome_cmd, check=True)
    
    if os.path.exists(html_report_path):
        os.remove(html_report_path)
    
    print(f"Generated PDF: {pdf_report_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()
