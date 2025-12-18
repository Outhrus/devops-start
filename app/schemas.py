 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/schemas.py b/app/schemas.py
new file mode 100644
index 0000000000000000000000000000000000000000..2b0111088c729845da42043c0778bce748f4652d
--- /dev/null
+++ b/app/schemas.py
@@ -0,0 +1,63 @@
+from datetime import datetime
+from typing import List, Optional
+
+from pydantic import BaseModel, EmailStr, Field
+
+
+class InteractionBase(BaseModel):
+    subject: str = Field(..., max_length=255)
+    note: Optional[str] = None
+    channel: str = Field(default="email", max_length=50)
+
+
+class InteractionCreate(InteractionBase):
+    customer_id: int
+
+
+class InteractionRead(InteractionBase):
+    id: int
+    customer_id: int
+    created_at: datetime
+
+    class Config:
+        orm_mode = True
+
+
+class DealBase(BaseModel):
+    title: str = Field(..., max_length=255)
+    value: int = Field(..., ge=0)
+    stage: str = Field(default="prospect", max_length=100)
+
+
+class DealCreate(DealBase):
+    customer_id: int
+
+
+class DealRead(DealBase):
+    id: int
+    customer_id: int
+    created_at: datetime
+
+    class Config:
+        orm_mode = True
+
+
+class CustomerBase(BaseModel):
+    name: str = Field(..., max_length=255)
+    email: EmailStr
+    phone: Optional[str] = Field(None, max_length=50)
+    company: Optional[str] = Field(None, max_length=255)
+
+
+class CustomerCreate(CustomerBase):
+    pass
+
+
+class CustomerRead(CustomerBase):
+    id: int
+    created_at: datetime
+    interactions: List[InteractionRead] = []
+    deals: List[DealRead] = []
+
+    class Config:
+        orm_mode = True
 
EOF
)
