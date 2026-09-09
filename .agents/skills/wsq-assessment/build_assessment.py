#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the WSQ assessment set for 'Application Integration with Docker and Kubernetes' (TGS-2021010366):
  - Written Assessment (SAQ)  — 5 open-ended KNOWLEDGE questions (K1–K5), aligned to the slides
  - Practical Performance (PP) — 4 PRACTICAL tasks (LO1–LO4), aligned to the in-class activities
Each instrument is produced as a Question Paper and a matching Answer Key (4 DOCX total),
all with the WSQ house cover page (same as the Lesson Plan / Learner Guide). Page 1 is the cover;
page 2 carries Trainee Information + Instructions + Grading; the questions/tasks begin on page 3.
Body: Arial 11.
"""
import os, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# This script lives in the wsq-assessment skill (.claude/skills/wsq-assessment/) and runs in
# place — it detects the course repo root by walking up to the nearest dir that has a .git
# folder (or both courseware/ and assessment/). Override with env REPO=/path if needed.
def _find_repo():
    env = os.environ.get("REPO")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    d = os.path.dirname(os.path.abspath(__file__))
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".git")) or \
           (os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "assessment"))):
            return d
        d = os.path.dirname(d)
    return os.getcwd()

REPO = _find_repo()
# prodoc.py (WSQ cover page + version control + page numbers, same as LP/LG) ships with the
# tertiary-lesson-plan skill. Look for it at the project level first, then the user level.
for _cand in (os.path.join(REPO, ".claude/skills/tertiary-lesson-plan"),
              os.path.expanduser("~/.claude/skills/tertiary-lesson-plan")):
    if os.path.exists(os.path.join(_cand, "prodoc.py")):
        sys.path.insert(0, _cand); break
import prodoc  # cover page + version control + page numbers (same as LP/LG)

# ─── EDIT PER COURSE ────────────────────────────────────────────────────────
TITLE       = "Neo4j Professional Graph Database Course"
COURSE_CODE = "TGS-2023036640"
# ────────────────────────────────────────────────────────────────────────────
# The cover page renders prodoc's module-level TGS constant. Override it so the
# assessment cover shows THIS course's ref (works with either prodoc version —
# the older project prodoc has no course_code kwarg).
prodoc.TGS = f"TGS Ref No: {COURSE_CODE}"
OUT   = os.path.join(REPO, "assessment")

# Logos: prefer the course's own courseware/assets, else fall back to the copies bundled
# in this skill (so the assessment builds even outside this project). Replace the course
# logo per course; the Tertiary Infotech logo is the same for every WSQ course.
def _logo(name):
    here = os.path.dirname(os.path.abspath(__file__))
    for p in (os.path.join(REPO, "courseware/assets", name), os.path.join(here, "assets", name)):
        if os.path.exists(p):
            return p
    return None
ORG_LOGO    = _logo("tertiary-infotech-logo.png")
COURSE_LOGO = _logo("neo4j-course-logo.png")   # None if absent → Tertiary-only cover (as LP/LG)

Q_VER, A_VER = "v6", "v6"   # single standardised version across all four files
# Durations come from the approved Assessment Plan v5.0: WA 1 hr, PP 1 hr.
WA_DURATION = "1 hour"
PP_DURATION = "1 hour"
BRAND = RGBColor(0x1F, 0x6F, 0xEB); DARK = RGBColor(0x11, 0x18, 0x27); GREY = RGBColor(0x55, 0x5B, 0x66)
# Assessments carry the cover page only — no Document Version Control Record.

# ---------------------------------------------------------------- WRITTEN (KNOWLEDGE)
# (criterion, context, question, [model-answer points]) — each traces to the course slides.
WRITTEN = [
 ("K1",
  "Before you can install or configure a graph database you must understand what it actually stores. Neo4j "
  "implements the property graph model, which is built from a small, fixed set of elements — and it is those "
  "elements, not tables and rows, that you design with.",
  "What are three key elements essential for building a graph database, and how does each function within the "
  "database structure?",
  ["NODES — the entities in the domain (a Person, a Movie, a Course). A node is the graph equivalent of a row, "
   "drawn as a circle, and is what a query normally starts from and returns.",
   "RELATIONSHIPS — the typed, directed connections between two nodes, for example (:Person)-[:ACTED_IN]->(:Movie). "
   "A relationship must always have exactly one type and one direction, and it connects exactly two nodes. "
   "Relationships are stored data, not computed at query time from a foreign key, which is what makes traversal fast.",
   "PROPERTIES — key/value pairs holding the actual data, for example {name: 'Tom Hanks'}. Crucially, properties "
   "live on BOTH nodes and relationships — the 'roles' value belongs on the ACTED_IN relationship, not on the "
   "person or the movie.",
   "LABELS (also accepted as a key element) — tags such as :Person or :Movie that group nodes into sets. A node "
   "may carry several labels or none, and adding a label is a cheap way to narrow the starting set of a query.",
   "How they work together: labels group the nodes, properties hold the data on both nodes and relationships, and "
   "relationships connect the nodes so the engine can traverse from one to the next. "
   "(Slides: The Property Graph Model / Nodes and Labels / Relationships / Properties on Nodes and Relationships)"]),
 ("K2",
  "Storing and extracting data accurately means being able to perform the full set of data-management operations. "
  "Every database supports the same four fundamental operations, and Cypher has a clause for each.",
  "What are the four CRUD operations typically used in a database, what role does each play in managing data, and "
  "which Cypher clause performs each one in Neo4j?",
  ["CREATE — adds new data. In Cypher this is the CREATE clause, or more commonly MERGE, which is get-or-create: "
   "it matches the pattern if it already exists and creates it only if it does not.",
   "READ — retrieves existing data. In Cypher this is MATCH, normally combined with WHERE to filter and RETURN to "
   "project the columns you want back.",
   "UPDATE — changes data that already exists. In Cypher this is SET, which adds or updates properties and labels; "
   "REMOVE deletes a property or a label, and setting a property to null has the same effect as removing it.",
   "DELETE — removes data. In Cypher this is DELETE for a relationship or a childless node, and DETACH DELETE to "
   "remove a node together with all of its relationships. A node that still has relationships cannot be removed "
   "with a plain DELETE — Neo4j refuses, to protect referential integrity.",
   "Why each matters: together the four operations are how a database administrator keeps data updated, stored and "
   "extracted accurately and according to set protocols. "
   "(Slides: CRUD in Cypher / MERGE is get-or-create / Deleting Safely)"]),
 ("K3",
  "Every database system has a query language, and the language shapes how you think about the data. Neo4j's "
  "language is declarative and pattern-based rather than table-based.",
  "What is the primary query language used in Neo4j, and what are its typical functionalities?",
  ["The primary query language is CYPHER — a declarative, pattern-matching language. You describe the PATTERN you "
   "want using ASCII art and the engine decides how to find it; you do not write the traversal algorithm yourself. "
   "Cypher is now the basis of the ISO GQL standard.",
   "Pattern syntax: parentheses are nodes ( ), square brackets type a relationship [ ], dashes and an arrow give "
   "direction -->, a colon introduces a label (:Person), and braces filter by property {name: 'Tom Hanks'}.",
   "Reading data: MATCH finds the pattern, WHERE filters it, RETURN projects the columns; ORDER BY, SKIP, LIMIT and "
   "DISTINCT shape which rows come back.",
   "Writing data: CREATE, MERGE (with ON CREATE SET / ON MATCH SET), SET, REMOVE, DELETE and DETACH DELETE.",
   "Analysing data: aggregation with count(), sum(), avg(), min(), max() and collect(); pipelining with WITH; "
   "isolated CALL {} subqueries; list and pattern comprehensions; and the CASE expression.",
   "Administration and tuning: Cypher also administers the server — SHOW DATABASES, CREATE USER, GRANT/DENY, SHOW "
   "TRANSACTIONS — and tunes queries with EXPLAIN, PROFILE, indexes, constraints and $parameters. "
   "(Slides: What is Cypher? / The Cypher Pattern Syntax / Anatomy of a Read Query)"]),
 ("K4",
  "When adding nodes it matters which clause you choose, because the two available clauses behave very differently "
  "if the same script is run more than once — which has direct consequences for data integrity and for who is "
  "allowed to run imports against a production database.",
  "What are the differences between the CREATE and MERGE clauses, and when should each be used to manage data "
  "entries in the database?",
  ["CREATE always creates a new node or relationship. It does not look up whether the data already exists, so it is "
   "faster — but running the same CREATE twice produces TWO nodes and duplicates the data.",
   "MERGE is get-or-create: it first looks for the pattern, uses the existing node if it finds one, and creates it "
   "only if it does not. Running the same MERGE twice leaves exactly one node — the script is idempotent.",
   "MERGE can behave differently in each case using ON CREATE SET (runs only when the node is created) and "
   "ON MATCH SET (runs only when it already existed); a plain SET after them runs either way.",
   "Use CREATE when you are certain the data is clean and unique and you need the speed — typically a bulk first "
   "load into an empty database.",
   "Use MERGE for imports, upserts and anything that may be re-run — which in practice is most administration work, "
   "because it is what prevents duplicate data.",
   "Performance note: MERGE looks the node up first, so it needs a supporting index (normally created by a "
   "uniqueness constraint) or it will scan every node of that label. Create the constraint BEFORE the import. "
   "(Slides: CREATE vs MERGE — Choosing Correctly / MERGE with ON CREATE and ON MATCH)"]),
 ("K5",
  "Analysing database performance means measuring a query rather than guessing about it. Consider the following "
  "Cypher query:\n\n"
  "MATCH (p:Person)-[:ACTED_IN]->(m:Movie)\n"
  "WHERE  p.name = 'Tom Hanks'\n"
  "AND exists {(p)-[:DIRECTED]->(m)}\n"
  "RETURN m.title",
  "Which Cypher clause can be used to analyse the total number of rows retrieved from the graph by this query, and "
  "what else does it report that helps you improve performance?",
  ["PROFILE is the clause. Prefixing the query with PROFILE executes it and returns the full execution plan "
   "annotated with the ACTUAL number of rows and the number of 'db hits' at every operator.",
   "Rows tell you how much data each step produced; db hits tell you how many times the engine had to touch the "
   "store, and db hits are the real measure of query cost — lower is faster.",
   "EXPLAIN is the related clause: it shows the same plan with the planner's ESTIMATES but does NOT run the query. "
   "Use EXPLAIN to inspect an expensive or destructive query safely, and PROFILE to measure one for real.",
   "Reading the plan: an operator named AllNodesScan or NodeByLabelScan means every node was examined, which is the "
   "signal to add an index on the filtered property. NodeIndexSeek means the index was used.",
   "Improving this query: create an index on Person.name so the query seeks rather than scans, and note that "
   "wrapping the property in a function such as toLower() would defeat that index. "
   "(Slides: EXPLAIN vs PROFILE / PROFILE tells you the truth / Making a Slow Query Fast)"]),
 ("K6",
  "A graph data model is rarely right the first time. Maintaining a database over its life means changing the model "
  "as use cases change or as queries prove too slow, and doing so in a controlled, measurable way.",
  "What are the steps involved in refactoring a graph, and how do they contribute to better data management and "
  "performance?",
  ["Step 1 — MEASURE FIRST. PROFILE the slow query and record its db hits, so the refactoring can be justified with "
   "evidence rather than opinion.",
   "Step 2 — IDENTIFY the cause in the plan: a label scan, a property being tested on every node, or duplicated "
   "data spread across many nodes.",
   "Step 3 — CHOOSE the refactoring. The three standard ones are: (a) ADD A LABEL to a subset of nodes, e.g. "
   "SET p:Actor, which narrows the starting set; (b) TURN A REPEATED PROPERTY INTO A NODE, e.g. a duplicated "
   "language string becomes a Language node joined by IN_LANGUAGE, which turns a scan into a traversal; "
   "(c) SPECIALISE THE RELATIONSHIP TYPE, e.g. ACTED_IN_1995 instead of ACTED_IN plus a year filter.",
   "Step 4 — APPLY it with Cypher, typically MATCH + SET for a label, or UNWIND + collect() + MERGE to create the "
   "new nodes and relationships, then remove the now-redundant property so the value is stored only once.",
   "Step 5 — ADD supporting indexes or constraints on the new labels and properties.",
   "Step 6 — RE-MEASURE. PROFILE the same query again and compare the db hits; a refactoring that does not reduce "
   "them is not worth its cost.",
   "Step 7 — RE-TEST EVERY USE CASE, because a change that speeds one query can break or slow another.",
   "How it contributes: refactoring removes duplicated data (so values cannot drift out of sync), reduces the work "
   "the engine does per query, and keeps the model aligned with the questions the application actually asks. "
   "(Slides: Refactoring is expected, not exceptional / The Three Refactorings You Will Use / Turning a Property "
   "Into a Node)"]),
]

# ---------------------------------------------------------------- PRACTICAL (ACTIVITY-BASED)
SCENARIO = (
 "XYZ Streaming, a leading online streaming platform, is migrating from its existing relational database to Neo4j "
 "in order to improve the personalised movie recommendations it offers its users. You have joined the project as "
 "the database administrator and you own the work end to end: installing and configuring the Neo4j environment, "
 "migrating the movie, person and viewing-history data into the graph accurately, troubleshooting the problems "
 "that arise during and after the migration, configuring user access so that analysts can read the data without "
 "being able to change it, analysing and improving query performance so recommendations return quickly, and "
 "putting a backup and ongoing maintenance procedure in place so that user preferences and viewing histories are "
 "never lost.\n\n"
 "Complete the three tasks below. Each one mirrors a hands-on lab you completed in class. For every task, paste "
 "your Cypher (or shell commands) and a screenshot of the output as evidence.")

# (label, criterion, task prompt, box caption, model-answer build steps citing the activity)
BOX_CAP = "Paste your Cypher / commands and a screenshot of your output in the box below"
PRACTICAL = [
 ('Task 1', 'A1, A2',
  'INSTALL, CONFIGURE AND LOAD THE DATABASE. Part A — Describe how you set up the Neo4j environment for this project: state which deployment you chose (Neo4j Desktop, Sandbox or AuraDB), how you created and started the database, and give the Cypher you ran to confirm the server responds and to record its version and edition. Part B — Write the Cypher to import the supplied person data from a CSV file into the graph. Your import must create a uniqueness constraint BEFORE loading, use a clause that makes the script safe to re-run without creating duplicates, and convert the numeric CSV values to the correct type. Part C — Once the data is loaded, write the Cypher query that returns the name, born and died properties of all people who HAVE a value for their died property AND who were born after 1985. In this graph it returns 6 rows. (Labs 2, 3 and 11.)',
  BOX_CAP,
  "Part A - Environment setup (Lab 2):\nNeo4j Desktop: create a Project, Add > Local DBMS, set a\npassword, choose the version, then Start and wait for\nthe status to read ACTIVE. Open Neo4j Browser on\nhttp://localhost:7474/browser/ (Bolt on 7687).\nAuraDB alternative: console.neo4j.io > New Instance >\nAuraDB Free, and DOWNLOAD the credentials file, because\nthe generated password is shown only once.\nVerify the server responds and record what you are\nrunning:\nRETURN 'Neo4j is running' AS status, datetime() AS ts;\nCALL dbms.components() YIELD name, versions, edition\nRETURN name, versions, edition;\nSHOW DATABASES;\n\nPart B - Import the CSV (Lab 11). Create the constraint\nFIRST: it enforces\nuniqueness and creates the index that makes MERGE fast,\nnot a label scan.\nCREATE CONSTRAINT person_id_unique IF NOT EXISTS\nFOR (p:Person) REQUIRE p.id IS UNIQUE;\n\nLOAD CSV WITH HEADERS FROM 'file:///persons.csv' AS row\nMERGE (p:Person {id: toInteger(row.id)})\nSET p.name  = row.name,\n    p.born  = toInteger(row.born),\n    p.died  = toInteger(row.died);\n\nMERGE (not CREATE) makes the script idempotent:\nre-running it updates the\nexisting nodes instead of duplicating them. toInteger()\nis\nrequired because\nthe comparison in Part C would silently match nothing.\n\nPart C - The required query (Lab 7). A missing property\nis\nnull, so the test\nmust be IS NOT NULL; null never equals anything, so\np.died\n<> null is wrong:\nMATCH (p:Person)\nWHERE p.died IS NOT NULL\n  AND p.born > 1985\nRETURN p.name AS name, p.born AS born, p.died AS died\nORDER BY p.born;\n\nExpected: 6 rows. (If the dataset stores born as a date\nrather than an integer, the predicate becomes\np.born.year > 1985.)\nEvidence: a screenshot of the constraint created, the\nimport summary and the 6-row result."),
 ('Task 2', 'A3, A4, A5',
  "TROUBLESHOOT, CONTROL ACCESS AND ANALYSE PERFORMANCE. Part A — Troubleshooting. Show the total number of rows retrieved from the graph by fine-tuning the query below, and state the total. Then explain which clause you used to obtain that figure and what it told you about how the query executed.\n\nMATCH (p:Person)-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(p)\nWHERE p.name = 'Tom Hanks'\nRETURN m.title\n\nPart B — User access. An analyst at XYZ Streaming must be able to read the recommendation graph but must NOT be able to change it. Write the Cypher to create the user and a custom role, grant that role only the privileges it needs, assign it to the user, and audit exactly what the role can do. Part C — Performance. Write a Cypher query that retrieves the movies released after the year 2000 together with the set of actors for each movie, and a second query that finds all Person nodes with a born year of 1980 ordered by the born property. Then state one specific change you would make to improve the performance of the second query, and how you would prove the improvement. (Labs 6, 7, 8, 9 and 17.)",
  BOX_CAP,
  "Part A - Troubleshooting and measuring (Lab 9):\nPROFILE MATCH (p:Person)-[:ACTED_IN]->(m:Movie)\n              <-[:DIRECTED]-(p)\nWHERE p.name = 'Tom Hanks'\nRETURN m.title;\n\nPROFILE executes the query and annotates every operator\nwith the ACTUAL rows\nand db hits, so it reports the total rows retrieved. In\nthe Movie graph this\npattern - a person who both acted in AND directed the\nsame\nmovie - returns\n1 row (That Thing You Do!). State the figure your\ndataset\nreturns.\nEXPLAIN is the alternative when the query must NOT be\nrun:\nit shows the same plan with estimated rows instead.\nWhat it tells you: if the plan opens with\nNodeByLabelScan\nor AllNodesScan, every Person node was examined and\nan index on Person.name is missing.\n\nPart B - User access control (Lab 17). All user\nadministration runs on the SYSTEM database:\n:use system\nCREATE USER analyst IF NOT EXISTS\nSET PASSWORD 'ChangeMe123!' CHANGE REQUIRED;\n\nCREATE ROLE recommendation_reader IF NOT EXISTS;\nGRANT ACCESS ON DATABASE neo4j TO recommendation_reader;\nGRANT MATCH {*} ON GRAPH neo4j NODES *\n  TO recommendation_reader;\nGRANT MATCH {*} ON GRAPH neo4j RELATIONSHIPS *\n  TO recommendation_reader;\nGRANT ROLE recommendation_reader TO analyst;\n\nAudit what the role can actually do - this is the query\nyou run in a security review:\nSHOW ROLE recommendation_reader PRIVILEGES AS COMMANDS;\nSHOW USERS;\n\nOnly MATCH (read) privileges are granted, so the analyst\ncan query but cannot CREATE, SET or DELETE. To hide a\nsensitive property from an otherwise-readable role, add\na\nDENY - a DENY always overrides a GRANT:\nDENY READ {email} ON GRAPH neo4j NODES User\n  TO recommendation_reader;\nCHANGE REQUIRED forces a password change at first login.\n\nPart C - Performance queries (Labs 7 and 8):\n// Movies released after 2000 with the set of actors for\n// each\nMATCH (m:Movie)<-[:ACTED_IN]-(a:Person)\nWHERE m.released > 2000\nRETURN m.title AS movie, collect(a.name) AS actors\nORDER BY m.released DESC;\n\n// All Person nodes born in 1980, ordered by born\nMATCH (p:Person)\nWHERE p.born = 1980\nRETURN p.name AS name, p.born AS born\nORDER BY p.born;\n\nImprovement and proof: create an index on the filtered\nproperty so the planner seeks instead of scanning -\nCREATE INDEX person_born_index IF NOT EXISTS\nFOR (p:Person) ON (p.born);\nSHOW INDEXES YIELD name, state;   // wait until the\nstate\nis ONLINE, or it will not be used\nThen PROFILE the same query again and compare the db\nhits\nbefore and after. The operator should change from\nNodeByLabelScan to NodeIndexSeek and the db-hit count\nshould fall substantially. Note that wrapping the\nproperty in a function (e.g. toLower()) would defeat the\nindex.\nEvidence: both profiles, the SHOW INDEXES output and the\nprivilege audit."),
 ('Task 3', 'A6, A7',
  'BACK UP THE DATABASE AND MAINTAIN THE MODEL. Part A — Backup and recovery. Describe and give the commands for the procedure you would use to back up the XYZ Streaming database and to prove that the backup is actually usable. State clearly what must be done to the database before an offline dump, and the one verification step teams most often skip. Part B — Ongoing data maintenance. Write the Cypher query that refactors the graph to add specialised relationships using the APOC library, so that a query for the movies an actor appeared in during a particular year no longer has to filter on a property. Explain what this refactoring improves and what it costs. Part C — State two checks you would run regularly to monitor the health of the database, and what each one would tell you. (Labs 13 and 17.)',
  BOX_CAP,
  "Part A - Backup and restore (Lab 17). An offline dump\nrequires\nthe database to be STOPPED first - the step most often\nmissed:\n\n# 1. Stop the DBMS in Neo4j Desktop.\n\n# 2. Dump the database (run from the DBMS folder):\nbin/neo4j-admin database dump neo4j --to-path=./backups\n\n# 3. Verify the dump file, and note its size and\n# timestamp:\nls -lh ./backups/neo4j.dump\n\n# 4. THE STEP TEAMS SKIP - restore into a SEPARATE\n# database\n#    to prove the backup is usable:\nbin/neo4j-admin database load restored \\\n  --from-path=./backups --overwrite-destination=true\n\n# 5. Register the restored database, then compare the\n# counts:\n:use system\nCREATE DATABASE restored IF NOT EXISTS;\nSHOW DATABASES;\n:use restored\nMATCH (n) RETURN count(n) AS restoredNodeCount;\n\nA backup that has never been restored is not a backup -\nit is\nan untested assumption. On Enterprise Edition or AuraDB\nan\nONLINE backup can be taken while the database keeps\nserving\nqueries; AuraDB takes daily backups automatically. The\nrunbook\nshould record what is backed up, how often, where it is\nstored,\nhow long it is retained and who verifies the restore.\n\nPart B - Refactor to specialised relationships with APOC\n(Lab 13):\nMATCH (a:Actor)-[:ACTED_IN]->(m:Movie)\nWHERE m.released IS NOT NULL\nCALL apoc.merge.relationship(a,\n  'ACTED_IN_' + left(toString(m.released), 4),\n  {}, {}, m, {}\n) YIELD rel\nRETURN count(rel) AS `Number of relationships merged`;\n\napoc.merge.relationship creates relationship types\nwhich plain Cypher cannot do - the type name is built\nfrom the\nmovie's year. The query then becomes:\nMATCH (a:Actor)-[:ACTED_IN_1995]->(m:Movie)\nWHERE a.name = 'Tom Hanks'\nRETURN m.title AS Movie;\n\nWhat it improves: the traversal follows ONLY the\nrelationships\nof that type, so the engine never visits the actor's\nother\nmovies at all - no property filter is evaluated.\nWhat it costs: the graph now holds far more distinct\nrelationship types, storage grows, and every write must\nmaintain both the generic and the specialised\nrelationship.\nApply it only where PROFILE shows the gain is real.\n(If APOC is not installed, install it from the\ndatabase's\nPlugins tab in Neo4j Desktop and restart.)\n\nPart C - Regular monitoring checks (Lab 17), any two of:\n\n// status of every database; first check when\n// unreachable\nSHOW DATABASES;\n\n// running queries and elapsed time; stop one with\n// TERMINATE TRANSACTION '<id>'\nSHOW TRANSACTIONS;\n\n// an index stuck POPULATING silently slows its queries\nSHOW INDEXES YIELD name, state, populationPercent;\n\n// the integrity rules actually being enforced\nSHOW CONSTRAINTS;\n\n// capacity and growth reporting\nCALL apoc.meta.stats() YIELD nodeCount, relCount;\n\nEvidence: the dump file listing, the restored node count\nmatching the original, the APOC refactor count and the\noutput\nof your two monitoring checks."),
]

# ---------------------------------------------------------------- doc helpers
def base_doc():
    doc = Document()
    n = doc.styles["Normal"]; n.font.name = "Arial"; n.font.size = Pt(11)
    return doc

def para(doc, text, size=11, bold=False, italic=False, color=None, after=6, before=0, align=None):
    p = doc.add_paragraph(); r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if color: r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(after); p.paragraph_format.space_before = Pt(before)
    if align is not None: p.alignment = align
    return p

def heading(doc, text, size=13):
    para(doc, text, size=size, bold=True, color=BRAND, after=6, before=8)

def answer_box(doc, lines=None, code=None, height_pt=90):
    """1x1 bordered box. `lines` → bullet-style model answer; `code` → monospace
    code/YAML/command block (indentation preserved); neither → empty answer space."""
    t = doc.add_table(rows=1, cols=1); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    cell.paragraphs[0].text = ""
    if code:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in code.split("\n"):
            b = cell.add_paragraph(style=None)
            b.paragraph_format.space_after = Pt(0); b.paragraph_format.space_before = Pt(0)
            rr = b.add_run(ln if ln else " ")
            rr.font.name = "Consolas"; rr.font.size = Pt(9)
            rr._element.rPr.rFonts.set(qn('w:cs'), "Consolas")
            wt = rr._element.find(qn('w:t'))
            if wt is not None: wt.set(qn('xml:space'), 'preserve')
    elif lines:
        run = cell.paragraphs[0].add_run("Suggestive answers (not exhaustive):")
        run.bold = True; run.font.size = Pt(10.5)
        for ln in lines:
            b = cell.add_paragraph(style=None); b.paragraph_format.left_indent = Inches(0.15)
            rr = b.add_run("•  " + ln); rr.font.size = Pt(10.5)
    else:
        # empty answer space
        tr = t.rows[0]._tr
        trPr = tr.get_or_add_trPr(); trh = OxmlElement('w:trHeight')
        trh.set(qn('w:val'), str(int(height_pt*20))); trh.set(qn('w:hRule'), 'atLeast'); trPr.append(trh)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

FILL_GAP = 6    # extra space below each fill-in line (paired with double line spacing for writing room)

def candidate_block(doc):
    heading(doc, "Trainee Information")
    for label in ["Trainee Name (as per NRIC): ______________________________________",
                  "Last 3 digits and alphabet of NRIC/FIN: ____________________",
                  "Date: ____________________"]:
        p = para(doc, label, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

# Assessment briefing (from the course slides — "Briefing for Assessment").
BRIEFING = [
    "Place phones and other materials under the table or on the floor.",
    "No photos or recording of assessment scripts.",
    "No discussion during the assessment.",
    "Use a black/blue pen for hard-copy assessments.",
    "No liquid paper / correction tape.",
    "Scripts are collected when time is up.",
]

LMS_URL = "https://lms-tms.tertiaryinfotech.com/"

def add_hyperlink(p, url, text):
    """Add a real clickable Word hyperlink (blue, underlined) to paragraph p."""
    r_id = p.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink"); link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "22"); rPr.append(sz)  # 11pt
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    run.append(rPr)
    t = OxmlElement("w:t"); t.text = text; run.append(t)
    link.append(run); p._p.append(link)
    return link

def instructions(doc, minutes_text):
    heading(doc, "Instructions to Candidate")
    # None marks the upload instruction, which carries a clickable LMS hyperlink.
    items = [
        "This is an individual exercise.",
        "This is an open-book assessment.",
        f"A total of {minutes_text} is given to complete this assessment.",
        None,
    ] + BRIEFING
    for i, s in enumerate(items, 1):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
        if s is None:
            p.add_run(f"{i}.  Complete your answers on the document provided and "
                      "upload the completed answers to the LMS at ").font.size = Pt(11)
            add_hyperlink(p, LMS_URL, LMS_URL)
            p.add_run(".").font.size = Pt(11)
        else:
            p.add_run(f"{i}.  {s}").font.size = Pt(11)

def grading(doc, what):
    heading(doc, "Grading")
    para(doc, what, size=11, after=12)
    for ln in ["Grade: _______  (C / NYC)",
               "Assessor Name: __________________________   Assessor NRIC: ________________",
               "Date: ________________________                    Signature: ____________________"]:
        p = para(doc, ln, size=11, after=FILL_GAP)
        p.paragraph_format.line_spacing = 2.0

def finish(doc, path):
    prodoc.add_page_numbers(doc); prodoc.enable_update_fields(doc)
    doc.save(path); print("  saved:", os.path.basename(path))

# ---------------------------------------------------------------- builders
def build_wa(answers):
    doc = base_doc()
    kind = "Written Assessment (SAQ) — Answer Key" if answers else "Written Assessment (SAQ)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Written Assessment (SAQ)" if answers else "Written Assessment (SAQ)",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; questions begin on the next page.
        candidate_block(doc); instructions(doc, WA_DURATION)
        grading(doc, "Candidate has answered all written questions and demonstrated the underpinning "
                     "knowledge required for the course learning outcomes.")
        page_break(doc)
    para(doc, "Short-Answer Questions (Knowledge)", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Answer all questions in your own words. Each question tests underpinning knowledge covered in the "
              "course slides.", size=10.5, italic=True, color=GREY, after=8)
    # Pagination is EXPLICIT — two questions to a page on the paper, one model answer to a
    # page in the key. Do not swap this for Word's keepNext/cantSplit: Word pushes an
    # oversized box to the next page, but Google Docs draws the border anyway and prints the
    # question text and the page footer straight THROUGH it. See SKILL.md → Pagination.
    per_page = 1 if answers else 2
    for i, (crit, ctx, q, pts) in enumerate(WRITTEN, 1):
        para(doc, f"Question {i}:", size=11.5, bold=True, after=2, before=6)
        para(doc, ctx, size=11, after=3)
        para(doc, f"{q}  ({crit})", size=11, bold=True, after=4)
        answer_box(doc, lines=pts if answers else None)
        if i % per_page == 0 and i < len(WRITTEN):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to WA (SAQ) - {TITLE} - {suffix}.docx" if answers
            else f"WA (SAQ) - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

def build_pp(answers):
    doc = base_doc()
    kind = "Practical Performance (PP) — Answer Key" if answers else "Practical Performance (PP)"
    prodoc.add_cover_page(doc, kind, TITLE, A_VER if answers else Q_VER,
                          org_logo=ORG_LOGO, course_logo=COURSE_LOGO)
    para(doc, TITLE, size=15, bold=True, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, "Answers to Practical Performance Assessment" if answers else "Practical Performance Assessment",
         size=13, bold=True, color=BRAND, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
    para(doc, f"Course Code: {COURSE_CODE}", size=11, color=GREY, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)
    if not answers:
        # Page 2 — candidate information, instructions and grading; the problem begins on the next page.
        candidate_block(doc); instructions(doc, PP_DURATION)
        grading(doc, "Candidate has successfully completed all PP tasks and can explain the overall "
                     "functions and features used to achieve them.")
        page_break(doc)
    para(doc, "Practical Problem", size=13, bold=True, color=BRAND, after=4)
    para(doc, "Scenario", size=11.5, bold=True, after=2)
    para(doc, SCENARIO, size=11, after=8)
    # Practical tasks are long and their boxes are tall, so they get a page each — on the
    # paper AND in the key. Same rule as the WA: the page break is ours, not the renderer's.
    for i, (label, crit, prompt, cap, pts) in enumerate(PRACTICAL, 1):
        para(doc, f"{label} ({crit}):", size=11.5, bold=True, after=2, before=6)
        para(doc, prompt, size=11, after=3)
        para(doc, cap, size=10.5, italic=True, color=GREY, after=4)
        answer_box(doc, code=pts if answers else None, height_pt=150)
        if i < len(PRACTICAL):
            page_break(doc)
    suffix = A_VER if answers else Q_VER
    name = (f"Answer to PP Assessment - {TITLE} - {suffix}.docx" if answers
            else f"PP Assessment - {TITLE} - {suffix}.docx")
    finish(doc, os.path.join(OUT, name))

def _check_code_width(limit=56):
    """A monospace line longer than the rendered code-block width wraps back to
    column 0 in the printed key and can strand a command argument on its own line.
    Measured from the rendered PDF: lines wrap at 60 characters (Consolas 9pt is
    substituted by a wider mono face at render time), so cap at 58 for margin."""
    bad = []
    for lbl, _c, _t, _b, ans in PRACTICAL:
        for ln in ans.split("\n"):
            if len(ln) > limit:
                bad.append((lbl, len(ln), ln[:70]))
    if bad:
        for lbl, n, ln in bad:
            print(f"  LONG LINE {lbl} ({n} chars): {ln}")
        raise SystemExit(
            f"BUILD FAILED: {len(bad)} model-answer line(s) exceed {limit} chars.")


if __name__ == "__main__":
    _check_code_width()
    print("Building WSQ assessment set…")
    build_wa(answers=False); build_wa(answers=True)
    build_pp(answers=False); build_pp(answers=True)
    print(f"Done. WA: {len(WRITTEN)} questions · PP: {len(PRACTICAL)} tasks.")
