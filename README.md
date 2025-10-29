# CARA MENJALANKAN SERVER API

Standar
```bash
uvicorn main:app --reload
```

Jalankan di port tertentu (misalnya 8080):

```bash
uvicorn main:app --reload --port 8080
```

Tentukan host agar bisa diakses dari luar (misal di server/VPS):
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Jalankan dengan lebih banyak worker (production mode):
```bash
uvicorn main:app --workers 4
```

Untuk membuat server local menggunakan ngrok
bisa langsung jalankan diterminal:
```bash
ngrok http --domain=unmenaced-donald-erubescent.ngrok-free.dev 8000
```

atau bisa membuat service dengan cara:
1. Buka/buat file  
    ```bash 
    sudo nano ~/snap/ngrok/315/.config/ngrok/ngrok.yml
    ```
2. Edit/isikan seperti berikut
    ```bash
    version: "3"
    agent:
        authtoken: 1idDhPeLb9tUX0cj0PXrFBgkZSD_764MxFp2yDXh63XKBpWee
    tunnels:
    app:
        proto: http
        addr: 8000
        domain: unmenaced-donald-erubescent.ngrok-free.dev
    ```
3. Jalankan tunel/restart tunnel
    ```bash
    ngrok start --none && ngrok start app
    ```

Kalau lebih dari satu tunnel buat seperti berikut:
```bash
version: "3"
agent:
    authtoken: 1idDhPeLb9tUX0cj0PXrFBgkZSD_764MxFp2yDXh63XKBpWee
tunnels:
app:
    proto: http
    addr: 8000
    domain: unmenaced-donald-erubescent.ngrok-free.dev
frontend:
    proto: http
    addr: 3000
    domain: domain-kedua.test.dev
```

Cara menjalankan sekaligus:
```bash
ngrok start --all
```
atau salah satu saja:
```bash
ngrok start frontend
```