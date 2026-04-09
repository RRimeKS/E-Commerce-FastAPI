# E-Commerce FastAPI

Full-stack e-ticaret platformu. **FastAPI** backend, **React 18** frontend, **Redux Toolkit (RTK Query)** state yönetimi, **SQLAlchemy 2.x** ORM, **MySQL** veritabanı ve **Tailwind CSS v4** ile geliştirilmiştir.

![Ana Sayfa](docs/screenshots/homepage.png)

## Teknoloji Stack'i

| Katman | Teknolojiler |
|--------|-------------|
| **Backend** | FastAPI, SQLAlchemy 2.x, MySQL, Pydantic v2, JWT (HttpOnly Cookie), bcrypt, slowapi (rate limiting) |
| **Frontend** | React 18, Redux Toolkit (RTK Query), React Router v6, Tailwind CSS v4, shadcn/ui, Vite |
| **Altyapı** | Python 3.11+, Node.js 22+, MySQL 8.0+, Docker & Docker Compose |

## Özellikler

### Kullanıcı Tarafı
- Ürün listeleme, arama ve kategoriye göre filtreleme
- Ürün detay sayfası (görsel, açıklama, stok durumu)
- Sepet yönetimi (ekleme, miktar güncelleme, silme)
- Sipariş oluşturma (otomatik stok kontrolü)
- Sipariş geçmişi görüntüleme
- Ürün değerlendirme ve yorum sistemi (yıldız puanlama)
- Karanlık / aydınlık tema desteği

### Kimlik Doğrulama & Yetkilendirme
- Kayıt ve giriş (e-posta veya kullanıcı adı ile)
- JWT token HttpOnly cookie'de saklanır
- Sayfa yenilendiğinde oturum korunur (`GET /auth/me`)
- Rol tabanlı erişim kontrolü (admin / user)

### Güvenlik & Rate Limiting
- IP bazlı rate limiting (slowapi) tüm endpoint'lerde
- Okuma endpoint'leri: 50 istek/dakika
- Yazma endpoint'leri: 25 istek/dakika
- Auth endpoint'leri (login/register): 5 istek/dakika (brute-force koruması)
- Global exception handling (validation, integrity, genel hatalar)

### Admin Paneli
- Kontrol paneli (ürün, kategori, sipariş, gelir istatistikleri)
- Ürün CRUD (görsel yükleme desteği)
- Kategori CRUD
- Tüm siparişleri görüntüleme ve yönetme

![Admin Panel](docs/screenshots/admin.png)

## Proje Yapısı

```
e-commerce-fastapi/
├── app/                              # Backend (FastAPI)
│   ├── main.py                       # Uygulama, CORS, lifespan
│   ├── config.py                     # Ortam değişkenleri (pydantic-settings)
│   ├── database.py                   # SQLAlchemy engine & session
│   ├── limiter.py                    # Rate limiting (slowapi)
│   ├── exception_handlers.py         # Global hata yakalama
│   ├── logging_config.py             # Loglama ayarları
│   ├── models/                       # SQLAlchemy ORM modelleri
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── review.py
│   ├── schemas/                      # Pydantic request/response şemaları
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── order.py
│   │   └── review.py
│   ├── routers/                      # API endpoint'leri
│   │   ├── auth.py                   # Kimlik doğrulama
│   │   ├── product.py                # Ürün CRUD + görsel yükleme
│   │   ├── category.py               # Kategori CRUD
│   │   ├── order.py                  # Sipariş işlemleri
│   │   └── review.py                 # Değerlendirme sistemi
│   └── utils/
│       ├── security.py               # JWT & bcrypt işlemleri
│       └── dependencies.py           # Auth middleware (cookie tabanlı)
├── Dockerfile                        # Backend Docker image
├── docker-compose.yml                # Multi-container orchestration
├── requirements.txt                  # Python bağımlılıkları
├── static/images/                    # Yüklenen ürün görselleri
├── frontend/                         # Frontend (React)
│   ├── Dockerfile                    # Frontend multi-stage build
│   ├── nginx.conf                    # SPA routing için Nginx ayarı
│   └── src/
│       ├── app/                      # Redux store & RTK Query base API
│       ├── features/
│       │   ├── auth/                 # Giriş, kayıt, auth state
│       │   ├── products/             # Ürün listeleme ve detay
│       │   ├── cart/                 # Sepet (localStorage)
│       │   ├── orders/               # Sipariş geçmişi & değerlendirme
│       │   ├── categories/           # Kategori API
│       │   └── admin/                # Admin panel sayfaları
│       ├── components/               # Layout, route guard, tema
│       └── hooks/                    # Custom hook'lar
└── .env                              # Ortam değişkenleri
```

## Kurulum

### Docker ile (Önerilen)

Tek komutla tüm uygulamayı ayağa kaldırın — MySQL, Backend ve Frontend otomatik yapılandırılır.

**Gereksinimler:** Docker ve Docker Compose

```bash
git clone https://github.com/KULLANICI_ADINIZ/e-commerce-fastapi.git
cd e-commerce-fastapi
docker compose up --build
```

| Servis | Adres | Açıklama |
|--------|-------|----------|
| **Frontend** | `http://localhost` | React uygulaması (Nginx) |
| **Backend** | `http://localhost:8000` | FastAPI |
| **API Docs** | `http://localhost:8000/docs` | Swagger UI |
| **MySQL** | `localhost:3307` | Dış erişim portu (isteğe bağlı) |

```bash
# Arka planda çalıştır
docker compose up -d

# Logları izle
docker compose logs -f backend

# Durdur
docker compose down

# Durdur + veritabanını sıfırla
docker compose down -v
```

#### Docker Mimarisi

```
docker-compose.yml
├── db        → MySQL 8.0 (healthcheck ile hazırlık kontrolü)
├── backend   → Python 3.11-slim + FastAPI (db hazır olunca başlar)
└── frontend  → Node 22 build → Nginx alpine (multi-stage, ~30MB)
```

- MySQL verisi ve yüklenen görseller **named volume** ile kalıcıdır
- Container'lar Docker network üzerinden haberleşir (`backend → db:3306`)
- Frontend production build'i Nginx ile sunulur (SPA routing dahil)

---

### Manuel Kurulum

Docker kullanmadan kurmak isterseniz:

**Gereksinimler:** Python 3.11+, Node.js 22+, MySQL 8.0+

#### 1. Repoyu klonlayın

```bash
git clone https://github.com/KULLANICI_ADINIZ/e-commerce-fastapi.git
cd e-commerce-fastapi
```

#### 2. Backend kurulumu

```bash
python -m venv myenv
source myenv/Scripts/activate  # Windows
# source myenv/bin/activate    # macOS/Linux

pip install -r requirements.txt
```

`.env` dosyasını proje kök dizininde oluşturun:

```env
DB_URI=mysql+pymysql://root:SIFRENIZ@localhost:3306/e_commerce
JWT_SECRET_KEY=güçlü-bir-secret-key-buraya
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

#### 3. Veritabanını oluşturun

```sql
CREATE DATABASE e_commerce;
```

Uygulama ilk çalıştığında tablolar otomatik oluşturulur.

#### 4. Backend'i başlatın

```bash
uvicorn app.main:app --reload
```

> Backend: `http://localhost:8000` | API Docs: `http://localhost:8000/docs`

#### 5. Frontend kurulumu

```bash
cd frontend
npm install
```

`frontend/.env` dosyasını oluşturun:

```env
VITE_API_URL=http://localhost:8000
```

#### 6. Frontend'i başlatın

```bash
npm run dev
```

> Frontend: `http://localhost:5173`

## API Endpoint'leri

### Kimlik Doğrulama — `/auth`

| Method | Endpoint | Açıklama | Yetki |
|--------|----------|----------|-------|
| `POST` | `/auth/register` | Yeni hesap oluşturma | Herkese açık |
| `POST` | `/auth/login` | Giriş yapma (cookie set) | Herkese açık |
| `POST` | `/auth/logout` | Çıkış yapma (cookie sil) | Herkese açık |
| `GET` | `/auth/me` | Oturum bilgisi | Giriş yapılmış |

### Ürünler — `/product`

| Method | Endpoint | Açıklama | Yetki |
|--------|----------|----------|-------|
| `GET` | `/product/all` | Tüm ürünleri listele | Herkese açık |
| `GET` | `/product/{id}` | Ürün detayı | Herkese açık |
| `POST` | `/product/create` | Ürün oluştur | Admin |
| `PUT` | `/product/update/{id}` | Ürün güncelle | Admin |
| `DELETE` | `/product/delete/{id}` | Ürün sil | Admin |
| `POST` | `/product/{id}/upload-image` | Ürün görseli yükle | Admin |

### Kategoriler — `/category`

| Method | Endpoint | Açıklama | Yetki |
|--------|----------|----------|-------|
| `GET` | `/category/all` | Tüm kategoriler | Herkese açık |
| `POST` | `/category/create` | Kategori oluştur | Admin |
| `PUT` | `/category/update/{id}` | Kategori güncelle | Admin |
| `DELETE` | `/category/delete/{id}` | Kategori sil | Admin |

### Siparişler — `/order`

| Method | Endpoint | Açıklama | Yetki |
|--------|----------|----------|-------|
| `GET` | `/order/all` | Tüm siparişler | Admin |
| `GET` | `/order/my-orders` | Kullanıcının siparişleri | Giriş yapılmış |
| `POST` | `/order/create` | Sipariş oluştur | Giriş yapılmış |

### Değerlendirmeler — `/review`

| Method | Endpoint | Açıklama | Yetki |
|--------|----------|----------|-------|
| `GET` | `/review/product/{id}` | Ürün yorumları | Herkese açık |
| `POST` | `/review/product/{id}` | Yorum yaz (satın alma kontrolü) | Giriş yapılmış |
| `DELETE` | `/review/product/{id}` | Yorumu sil | Yorum sahibi |

## Veritabanı Şeması

```
User ──1:N──> Order ──1:N──> OrderItem <──N:1── Product <──N:1── Category
  │                                                │
  └──1:N──> Review <──N:1──────────────────────────┘
```

| Tablo | Temel Alanlar |
|-------|--------------|
| **User** | id, firstName, lastName, userName, email, password, role |
| **Product** | id, name, description, price, stock, image_url, average_rating, review_count, category_id |
| **Category** | id, name |
| **Order** | id, user_id, total_price, status |
| **OrderItem** | id, order_id, product_id, quantity, price |
| **Review** | id, rating, comment, product_id, user_id |

## Ekran Görüntüleri

| Ana Sayfa | Ürün Detay |
|:---------:|:----------:|
| ![Ana Sayfa](docs/screenshots/homepage.png) | ![Ürün Detay](docs/screenshots/product-detail.png) |

| Sepet | Giriş |
|:-----:|:-----:|
| ![Sepet](docs/screenshots/cart.png) | ![Giriş](docs/screenshots/login.png) |

| Admin Panel | Karanlık Tema |
|:-----------:|:------------:|
| ![Admin Panel](docs/screenshots/admin.png) | ![Karanlık Tema](docs/screenshots/dark-mode.png) |

## Lisans

Bu proje [MIT](LICENSE) lisansı altında lisanslanmıştır.
