from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path
import secrets
from .database import engine, Base, get_db
from .models import User, Profile, Pact, Gift, Proof, Story, Reaction
from .schemas import UserRegister, UserLogin, Token, ProfileIn, PactIn, GiftIn, StoryIn, ReactIn
from .auth import hash_password, verify_password, create_access_token
from app import deps as deps
from .settings import get_settings

settings = get_settings()
MEDIA_ROOT = Path(settings.MEDIA_DIR); MEDIA_ROOT.mkdir(exist_ok=True, parents=True)

# Auto-create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kiss & Tell API", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"ok": True}

@app.get("/")
def root(): return {"status": "Kiss & Tell API Running"}

# ---------- Auth (Email OR Phone) ----------
from sqlalchemy import or_

@app.post("/auth/register", response_model=Token)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")
    if payload.email and db.query(User).filter(User.email==payload.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    if payload.phone and db.query(User).filter(User.phone==payload.phone).first():
        raise HTTPException(status_code=400, detail="Phone exists")
    user = User(email=payload.email, phone=payload.phone, password_hash=hash_password(payload.password), display_name=payload.display_name)
    db.add(user); db.commit()
    sub = payload.email or payload.phone
    token = create_access_token(sub)
    return {"access_token": token}

@app.post("/auth/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    if not payload.email and not payload.phone:
        raise HTTPException(status_code=400, detail="Provide email or phone")
    q = db.query(User).filter(or_(User.email==payload.email, User.phone==payload.phone)).first()
    if not q or not verify_password(payload.password, q.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    sub = payload.email or payload.phone
    token = create_access_token(sub)
    return {"access_token": token}

@app.get("/me")
def me(user: User = Depends(deps.get_current_user)):
    return {"id": user.id, "email": user.email, "phone": user.phone, "display_name": user.display_name}

# ---------- Profiles ----------
@app.post("/profile")
def upsert_profile(payload: ProfileIn, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    intentions_csv = ",".join(payload.intentions) if isinstance(payload.intentions, list) else payload.intentions
    prof = db.query(Profile).filter(Profile.user_id==user.id).first()
    if not prof:
        prof = Profile(user_id=user.id, age=payload.age, location=payload.location, bio=payload.bio, intentions=intentions_csv, trust=payload.trust, photo_url=payload.photo_url)
        db.add(prof)
    else:
        prof.age=payload.age; prof.location=payload.location; prof.bio=payload.bio; prof.intentions=intentions_csv; prof.trust=payload.trust; prof.photo_url=payload.photo_url
    db.commit()
    return {"ok": True}

@app.get("/profiles")
def list_profiles(db: Session = Depends(get_db)):
    rows = db.query(Profile).all()
    return [ {"id":p.id,"user_id":p.user_id,"age":p.age,"location":p.location,"bio":p.bio,"intentions":p.intentions.split(',') if p.intentions else [],"trust":p.trust,"photo_url":p.photo_url} for p in rows ]

# ---------- Pacts ----------
@app.post("/pacts")
def create_pact(payload: PactIn, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    code = "KT-" + secrets.token_hex(3).upper()
    pact = Pact(code=code, user_a_id=user.id, user_b_id=payload.partner_id, when=payload.when, where=payload.where, note=payload.note, status="active")
    db.add(pact); db.commit()
    return {"code": code}

# ---------- Gifts ----------
@app.post("/gifts")
def create_gift(payload: GiftIn, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    gift = Gift(pact_code=payload.pact_code, sender_id=user.id, recipient_id=payload.recipient_id, amount=payload.amount, method=payload.method, status="escrow")
    db.add(gift); db.commit()
    return {"id": gift.id, "status": gift.status}

# ---------- Proofs ----------
@app.post("/proofs")
def upload_proof(pact_code: str = Form(...), visibility: str = Form("private"), image: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    ext = ".jpg"
    if image and image.filename:
        p = Path(image.filename)
        ext = p.suffix.lower() or ".jpg"
    out = Path(settings.MEDIA_DIR); out.mkdir(exist_ok=True, parents=True)
    fname = f"{secrets.token_hex(8)}{ext}"
    fpath = out / fname
    with fpath.open("wb") as f: f.write(image.file.read())
    proof = Proof(pact_code=pact_code, user_id=user.id, visibility=visibility, image_path=str(fpath))
    db.add(proof); db.commit()
    return {"id": proof.id, "image_path": proof.image_path}

# ---------- Stories ----------
@app.post("/stories")
def create_story(payload: StoryIn, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    st = Story(pact_code=payload.pact_code, author_id=user.id, category=payload.category, location=payload.location, text=payload.text, anon=payload.anon, ratings=payload.ratings_csv)
    db.add(st); db.commit()
    return {"id": st.id}

@app.get("/stories")
def list_stories(db: Session = Depends(get_db)):
    rows = db.query(Story).order_by(Story.id.desc()).limit(100).all()
    out = []
    for s in rows:
        counts = {k: db.query(Reaction).filter(Reaction.story_id==s.id, Reaction.kind==k).count() for k in ["hot","dead","clown","villain","streets"]}
        out.append({"id":s.id,"category":s.category,"location":s.location,"text":s.text[:240],"anon":s.anon,"ratings":s.ratings,"reactions":counts})
    return out

@app.post("/stories/{story_id}/react")
def react(story_id: int, payload: ReactIn, db: Session = Depends(get_db), user: User = Depends(deps.get_current_user)):
    if payload.kind not in {"hot","dead","clown","villain","streets"}:
        raise HTTPException(status_code=400, detail="Invalid reaction kind")
    r = Reaction(story_id=story_id, user_id=user.id, kind=payload.kind)
    db.add(r); db.commit()
    return {"ok": True}
