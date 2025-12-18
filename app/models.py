 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/models.py b/app/models.py
new file mode 100644
index 0000000000000000000000000000000000000000..59b324f9c18ec0fef30a32bf5fe54a186b2335b5
--- /dev/null
+++ b/app/models.py
@@ -0,0 +1,45 @@
+from datetime import datetime
+from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
+from sqlalchemy.orm import relationship
+
+from .database import Base
+
+
+class Customer(Base):
+    __tablename__ = "customers"
+
+    id = Column(Integer, primary_key=True, index=True)
+    name = Column(String(255), nullable=False)
+    email = Column(String(255), unique=True, nullable=False, index=True)
+    phone = Column(String(50), nullable=True)
+    company = Column(String(255), nullable=True)
+    created_at = Column(DateTime, default=datetime.utcnow)
+
+    interactions = relationship("Interaction", back_populates="customer", cascade="all, delete-orphan")
+    deals = relationship("Deal", back_populates="customer", cascade="all, delete-orphan")
+
+
+class Deal(Base):
+    __tablename__ = "deals"
+
+    id = Column(Integer, primary_key=True, index=True)
+    title = Column(String(255), nullable=False)
+    value = Column(Integer, nullable=False)
+    stage = Column(String(100), default="prospect")
+    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
+    created_at = Column(DateTime, default=datetime.utcnow)
+
+    customer = relationship("Customer", back_populates="deals")
+
+
+class Interaction(Base):
+    __tablename__ = "interactions"
+
+    id = Column(Integer, primary_key=True, index=True)
+    subject = Column(String(255), nullable=False)
+    note = Column(Text, nullable=True)
+    channel = Column(String(50), default="email")
+    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
+    created_at = Column(DateTime, default=datetime.utcnow)
+
+    customer = relationship("Customer", back_populates="interactions")
 
EOF
)
