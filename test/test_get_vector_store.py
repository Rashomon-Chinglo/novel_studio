import os
import sys

sys.path.append(os.getcwd())

import time

from app.db.vector import get_vector_store

start = time.time()
vs1 = get_vector_store()
t1 = time.time() - start
print(f"First instantiation: {t1:.4f}s")

start = time.time()
vs2 = get_vector_store()
t2 = time.time() - start
print(f"Second instantiation: {t2:.4f}s")

assert t2 < t1 / 10, "Caching failed: second instantiation was not significantly faster"
print("Cache test passed")
