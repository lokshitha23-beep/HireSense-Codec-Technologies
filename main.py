from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import sqlite3, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DB=ROOT/'hiresense.db'
app=FastAPI(title='HireSense Original', version='1.0.0')
app.mount('/static', StaticFiles(directory=ROOT/'static'), name='static')

def connect():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    with connect() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,skills TEXT NOT NULL,experience INTEGER NOT NULL DEFAULT 0,description TEXT NOT NULL DEFAULT '');
        CREATE TABLE IF NOT EXISTS candidates(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL,skills TEXT NOT NULL,experience INTEGER NOT NULL DEFAULT 0,education TEXT NOT NULL DEFAULT '',stage TEXT NOT NULL DEFAULT 'Applied',notes TEXT NOT NULL DEFAULT '');""")
        if c.execute('SELECT COUNT(*) FROM jobs').fetchone()[0]==0:
            c.executemany('INSERT INTO jobs(title,skills,experience,description) VALUES(?,?,?,?)',[
            ('Frontend Developer','react,javascript,css,html,git',1,'Build accessible web interfaces.'),('Python API Developer','python,fastapi,sql,rest,git',1,'Build reliable APIs and services.')])
        if c.execute('SELECT COUNT(*) FROM candidates').fetchone()[0]==0:
            c.executemany('INSERT INTO candidates(name,email,skills,experience,education,stage) VALUES(?,?,?,?,?,?)',[
            ('Aarav Kumar','aarav@example.test','react,javascript,css,html,git',2,'B.Tech','Shortlisted'),('Mira Reddy','mira@example.test','python,fastapi,sql,rest,git',1,'B.Tech','Applied'),('Dev Shah','dev@example.test','javascript,html,css,python',1,'B.Sc','Interview')])
init()
class JobIn(BaseModel): title:str=Field(min_length=2,max_length=120); skills:str; experience:int=Field(ge=0,le=60); description:str=''
class CandidateIn(BaseModel): name:str=Field(min_length=2,max_length=120); email:str; skills:str; experience:int=Field(ge=0,le=60); education:str=''; stage:str='Applied'
class StageIn(BaseModel): stage:str

def rows(sql,args=()):
    with connect() as c: return [dict(x) for x in c.execute(sql,args).fetchall()]
def skillset(s): return {re.sub(r'[^a-z0-9+#.]','',x.strip().lower()) for x in s.split(',') if x.strip()}
def match(candidate, job):
    req=skillset(job['skills']); have=skillset(candidate['skills']); skill=round(100*len(req & have)/len(req)) if req else 0
    exp=100 if candidate['experience']>=job['experience'] else round(100*candidate['experience']/max(1,job['experience']))
    score=round(skill*.8+exp*.2)
    return {'score':score,'matched':sorted(req&have),'missing':sorted(req-have),'skill_score':skill,'experience_score':exp}
@app.get('/',response_class=HTMLResponse)
def home(): return (ROOT/'static/index.html').read_text(encoding='utf-8')
@app.get('/api/jobs')
def jobs(): return rows('SELECT * FROM jobs ORDER BY id DESC')
@app.post('/api/jobs')
def add_job(x:JobIn):
    with connect() as c: cur=c.execute('INSERT INTO jobs(title,skills,experience,description) VALUES(?,?,?,?)',(x.title,x.skills,x.experience,x.description)); return {'id':cur.lastrowid,'ok':True}
@app.get('/api/candidates')
def candidates(): return rows('SELECT * FROM candidates ORDER BY id DESC')
@app.post('/api/candidates')
def add_candidate(x:CandidateIn):
    with connect() as c: cur=c.execute('INSERT INTO candidates(name,email,skills,experience,education,stage) VALUES(?,?,?,?,?,?)',(x.name,x.email,x.skills,x.experience,x.education,x.stage)); return {'id':cur.lastrowid,'ok':True}
@app.patch('/api/candidates/{cid}/stage')
def stage(cid:int,x:StageIn):
    allowed={'Applied','Shortlisted','Interview','Selected','Rejected'}
    if x.stage not in allowed: raise HTTPException(400,'Invalid stage')
    with connect() as c:
        cur=c.execute('UPDATE candidates SET stage=? WHERE id=?',(x.stage,cid))
        if not cur.rowcount: raise HTTPException(404,'Candidate not found')
    return {'ok':True}
@app.get('/api/matches/{job_id}')
def matches(job_id:int):
    js=rows('SELECT * FROM jobs WHERE id=?',(job_id,))
    if not js: raise HTTPException(404,'Job not found')
    out=[]
    for c in rows('SELECT * FROM candidates'):
        out.append({**c,**match(c,js[0])})
    return sorted(out,key=lambda x:x['score'],reverse=True)
@app.get('/api/summary')
def summary():
    return {'jobs':len(rows('SELECT id FROM jobs')),'candidates':len(rows('SELECT id FROM candidates')),'interviews':len(rows("SELECT id FROM candidates WHERE stage='Interview'")),'shortlisted':len(rows("SELECT id FROM candidates WHERE stage='Shortlisted'"))}
