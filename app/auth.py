@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == body.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(body.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": user.email
    }
