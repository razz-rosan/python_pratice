@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):
    return{"status":"sucess"}