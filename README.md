# 📐 Math Microservice – FastAPI + Firebase (Docker Ready)

Acest microserviciu expune 3 operații matematice printr-un API REST:

- `pow(x, y)` – ridică x la puterea y
- `fib(n)` – returnează al n-lea număr Fibonacci
- `fact(n)` – returnează factorialul unui număr n

Toate operațiile sunt salvate într-o bază Firebase Firestore, cu caching (nu recalculează dacă există deja). Aplicația este complet Dockerizată și include cheia Firebase în imagine, gata de rulare directă.

---

## 🚀 Cum rulezi aplicația din imagine Docker

### 🔹 1. Încarcă imaginea local

```bash
docker load -i math-service.tar

###🔹 2. Rulează containerul

```bash
docker run -p 8000:8000 math-service

###🔹 3. Accesează Swagger UI

```bash
http://localhost:8000/docs