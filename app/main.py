 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/main.py b/app/main.py
new file mode 100644
index 0000000000000000000000000000000000000000..afd00ab62dec09933d103bf0ae1de5bc275a9cd8
--- /dev/null
+++ b/app/main.py
@@ -0,0 +1,78 @@
+from fastapi import Depends, FastAPI, HTTPException
+from sqlalchemy.orm import Session
+
+from . import models, schemas
+from .database import Base, engine, get_db
+
+Base.metadata.create_all(bind=engine)
+
+app = FastAPI(title="Lightweight CRM API")
+
+
+@app.post("/customers", response_model=schemas.CustomerRead)
+def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
+    existing = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
+    if existing:
+        raise HTTPException(status_code=400, detail="Customer with this email already exists")
+
+    db_customer = models.Customer(**customer.dict())
+    db.add(db_customer)
+    db.commit()
+    db.refresh(db_customer)
+    return db_customer
+
+
+@app.get("/customers", response_model=list[schemas.CustomerRead])
+def list_customers(db: Session = Depends(get_db)):
+    return db.query(models.Customer).all()
+
+
+@app.get("/customers/{customer_id}", response_model=schemas.CustomerRead)
+def get_customer(customer_id: int, db: Session = Depends(get_db)):
+    customer = db.query(models.Customer).get(customer_id)
+    if not customer:
+        raise HTTPException(status_code=404, detail="Customer not found")
+    return customer
+
+
+@app.post("/deals", response_model=schemas.DealRead)
+def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
+    customer = db.query(models.Customer).get(deal.customer_id)
+    if not customer:
+        raise HTTPException(status_code=404, detail="Customer not found")
+
+    db_deal = models.Deal(**deal.dict())
+    db.add(db_deal)
+    db.commit()
+    db.refresh(db_deal)
+    return db_deal
+
+
+@app.patch("/deals/{deal_id}", response_model=schemas.DealRead)
+def update_deal_stage(deal_id: int, stage: str, db: Session = Depends(get_db)):
+    deal = db.query(models.Deal).get(deal_id)
+    if not deal:
+        raise HTTPException(status_code=404, detail="Deal not found")
+
+    deal.stage = stage
+    db.commit()
+    db.refresh(deal)
+    return deal
+
+
+@app.post("/interactions", response_model=schemas.InteractionRead)
+def log_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
+    customer = db.query(models.Customer).get(interaction.customer_id)
+    if not customer:
+        raise HTTPException(status_code=404, detail="Customer not found")
+
+    db_interaction = models.Interaction(**interaction.dict())
+    db.add(db_interaction)
+    db.commit()
+    db.refresh(db_interaction)
+    return db_interaction
+
+
+@app.get("/health")
+def health_check():
+    return {"status": "ok"}
 
EOF
)
