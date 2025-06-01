<h1 align="center">BOTTOT</h1>

![Image_1](readme/Implementasi.png)

# Table of Contents

[Description](#description)

[Requirements Program dan Instalasi](#requirements-program-dan-instalasi)

[Langkah-langkah](#langkah-langkah)

[Author](#author)

## Description
**BOTTOT** merupakan algoritma greedy yang cerdas dan adaptif, dirancang untuk mengumpulkan diamond secara efisien. Bot ini memprioritaskan diamond terdekat, menghindari diamond merah saat inventory ≥ 4, dan akan segera pulang ke base jika diamond sudah cukup (≥ 5) atau waktu hampir habis. Dengan dukungan strategi zig-zag, pemanfaatan teleporter, serta gerakan aman saat kondisi tidak ideal, BOTTOT mampu bergerak cepat dan efektif di berbagai situasi permainan.


## Requirements Program dan Instalasi
install program berikut
- [**Node.js**](https://nodejs.org/en)
- [**Docker Desktop**](https://www.docker.com/products/docker-desktop/)
- [**Bot Starter Pack**](tools/tubes1-IF2211-game-engine-1.1.0.zip)
- **Yarn**  
  Run di terminal  
  ```
  npm install --global yarn
  ```

## Langkah-langkah
**1. Cara Menjalankan Game Engine**
     Pastikan program dan instalasi sudah di install semua  
- **instalasi dan konfigurasi awal**  
       1) Download source code (.zip) pada [**Game Engine**](tools/tubes1-IF2211-bot-starter-pack-1.0.1.zip)  
       2) Extract zip tersebut, lalu masuk ke folder hasil extractnya dan buka terminal, disarankan pakai terminal vscode  
       3) Masuk ke root directory dari project (sesuaikan dengan nama rilis terbaru)    
          ```
          cd tubes1-IF2110-game-engine-1.1.0
          ```  
       4) Install dependencies menggunakan Yarn    
          ```
          yarn
          ```  
       5) Setup default environment variable dengan menjalankan script berikut    
          Untuk Windows    
          ```
          ./scripts/copy-env.bat
          ```  
          Untuk Linux / (possibly) macOS    
          ```
          chmod +x ./scripts/copy-env.sh
          ./scripts/copy-env.sh
          ```  
       6) Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal)    
          ```
          docker compose up -d database
          ```  
          Lalu jalankan script berikut.     
          Untuk Windows  
          ```
          ./scripts/setup-db-prisma.bat
          ```  
          Untuk Linux / (possibly) macOS  
          ```  
          chmod +x ./scripts/setup-db-prisma.sh
          ./scripts/setup-db-prisma.sh
          ```  





       
![Image_2](graphics/readme/guide.png)

<li> Install Python 3.11 or higher</li>
Run the following command to start the game:

```
python3 main.py
```
alternative command:

```
python main.py
```
## UML Diagram
![Image_3](graphics/readme/UML_Diagram.png)


## Author

| Anggota | Nama | NIM | 
| --- | ---- | --- | 
| Ketua Kelompok | Muhammad Fajri Firdaus | 123140050 | 
| Anggota 1 | Bayu Brigas Novaldi | 123140030 | 



