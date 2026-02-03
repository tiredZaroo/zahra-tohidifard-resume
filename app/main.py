#  FastAPI 
from fastapi import FastAPI, Request, Form, Cookie, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

#  SQLAlchemy
from sqlalchemy.orm import Session

#  Database
from app.database import Base, engine, SessionLocal
from app.models import Project
from . import models, schemas

#  JWT 
from jose import jwt
from datetime import datetime, timedelta



Base.metadata.create_all(bind=engine)
from fastapi.staticfiles import StaticFiles



models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resume Backend", docs_url="/docs", redoc_url="/redoc")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

SECRET_KEY = "super-secret-key"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 


app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# @app.get("/request", response_class=HTMLResponse)
# def request_page(request: Request):
#     return templates.TemplateResponse(
#         "request.html",
#         {"request": request}
#     )



from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/request")
def request_page(request: Request):
    return templates.TemplateResponse(
        "request.html",
        {"request": request}
    )



@app.get("/login")
def request_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )







def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_token():
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": "admin", "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    
#     from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse

# app = FastAPI()

# templates = Jinja2Templates(directory="templates")


# @app.get("/request", response_class=HTMLResponse)
# def admin_page(request: Request):
#     return templates.TemplateResponse(
#         "request.html",
#         {"request": request}
#     )





@app.post("/api/projects")
def create_project(project: schemas.ProjectCreate):
    print(project)
    return {"message": "project received"}





@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@app.post("/api/projects")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(
        name=project.name,
        email=project.email,
        description=project.description,
        budget=project.budget,
        deadline=project.deadline,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return {"message": "project saved", "id": db_project.id}


@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    return db.query(Project).all()


@app.delete("/api/projects/{project_id}")
def delete_project(
    project_id: int, db: Session = Depends(get_db), token: str = Depends(verify_token)
):
    project = db.query(Project).get(project_id)
    if project:
        db.delete(project)
        db.commit()
        return {"message": "Deleted"}
    raise HTTPException(status_code=404, detail="Project not found")


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    db = SessionLocal()
    project = db.query(Project).get(project_id)
    if project:
        db.delete(project)
        db.commit()
    return {"message": "Deleted"}


@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home")
def login_page(request: Request):
    return templates.TemplateResponse("resume-admin.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "1234":
        token = create_token()
        response = RedirectResponse(url="/adminPanel", status_code=302)
        response.set_cookie("access_token", token, httponly=True)

        return response
    return RedirectResponse(
            url="/login?error=invalid",
            status_code=302
        )

    
   


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("admin")
    return response


@app.get("/adminPanel")
def admin_page(request: Request, access_token: str = Depends(verify_token)):
    return templates.TemplateResponse("adminPanel.html", {"request": request})

from fastapi import WebSocket

active_users = set()

# @app.websocket("/ws")
# async def websocket_endpoint(ws: WebSocket):
#     await ws.accept()
#     user = "some_user"  
#     active_users.add(user)
#     try:
#         while True:
#             await ws.receive_text()
#     except:
#         active_users.remove(user)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
active_connections = set()

@app.websocket("/ws/online")
async def websocket_online(ws: WebSocket):
    await ws.accept()
    active_connections.add(ws)

    
    await broadcast_online_count()

    try:
        while True:
            await ws.receive_text()  # برای زنده نگه داشتن اتصال
    except WebSocketDisconnect:
        active_connections.remove(ws)
        await broadcast_online_count()
        
        
async def broadcast_online_count():
    count = len(active_connections)
    for conn in active_connections:
        await conn.send_json({"online": count})
        
        
        # در فایل main.py یا websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        # ارسال تعداد به همه کاربران
        await self.broadcast_count()
    
    async def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        await self.broadcast_count()
    
    async def broadcast_count(self):
        count = len(self.active_connections)
        message = {"online_count": count}
        # ارسال به همه اتصالات فعال
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                continue

manager = ConnectionManager()

@app.websocket("/ws/online")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # نگه داشتن اتصال باز
            await websocket.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        
        
        
        
        
        
        
        
        # websocket_manager.py
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid
from typing import Dict, List
import json
from models import OnlineUser, UserSession

class ConnectionManager:
    def __init__(self, db: Session):
        self.active_connections: Dict[str, WebSocket] = {}
        self.db = db
    
    async def connect(self, websocket: WebSocket, ip: str = None, user_agent: str = None, page_url: str = None):
        await websocket.accept()
        session_id = str(uuid.uuid4())
        
        # ذخیره در دیتابیس
        online_user = OnlineUser(
            session_id=session_id,
            ip_address=ip,
            user_agent=user_agent,
            page_url=page_url,
            last_seen=datetime.utcnow(),
            status=UserSession.ACTIVE
        )
        self.db.add(online_user)
        self.db.commit()
        
        self.active_connections[session_id] = websocket
        await self.broadcast_count()
        
        return session_id
    
    async def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            # به‌روزرسانی وضعیت در دیتابیس
            user = self.db.query(OnlineUser).filter(
                OnlineUser.session_id == session_id
            ).first()
            if user:
                user.status = UserSession.INACTIVE
                self.db.commit()
            
            del self.active_connections[session_id]
            await self.broadcast_count()
    
    async def update_last_seen(self, session_id: str):
        user = self.db.query(OnlineUser).filter(
            OnlineUser.session_id == session_id
        ).first()
        if user:
            user.last_seen = datetime.utcnow()
            self.db.commit()
    
    async def get_online_count(self) -> int:
        # فقط کاربرانی که در 5 دقیقه گذشته فعالیت داشتند
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        count = self.db.query(OnlineUser).filter(
            OnlineUser.last_seen >= five_minutes_ago,
            OnlineUser.status == UserSession.ACTIVE
        ).count()
        return count
    
    async def broadcast_count(self):
        count = await self.get_online_count()
        message = {
            "type": "online_count",
            "count": count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # ارسال به همه اتصالات فعال
        disconnected_sessions = []
        for session_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
                # به‌روزرسانی last_seen
                await self.update_last_seen(session_id)
            except:
                disconnected_sessions.append(session_id)
        
        # حذف اتصالات قطع شده
        for session_id in disconnected_sessions:
            await self.disconnect(session_id)
    
    async def cleanup_inactive_users(self):
        """پاک کردن کاربران غیرفعال قدیمی"""
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        self.db.query(OnlineUser).filter(
            OnlineUser.last_seen < one_hour_ago
        ).delete()
        self.db.commit()