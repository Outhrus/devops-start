 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/app/database.py b/app/database.py
new file mode 100644
index 0000000000000000000000000000000000000000..b6603b5bf9991d1751f14d4da75e8e921802707a
--- /dev/null
+++ b/app/database.py
@@ -0,0 +1,18 @@
+from sqlalchemy import create_engine
+from sqlalchemy.orm import sessionmaker, declarative_base
+
+DATABASE_URL = "sqlite:///./crm.db"
+
+engine = create_engine(
+    DATABASE_URL, connect_args={"check_same_thread": False}
+)
+SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
+Base = declarative_base()
+
+
+def get_db():
+    db = SessionLocal()
+    try:
+        yield db
+    finally:
+        db.close()
 
EOF
)
