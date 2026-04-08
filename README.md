# Sepetteyim - E-Ticaret Uygulamasi

Fullstack e-ticaret uygulamasi. FastAPI (Python) backend, React frontend. Urun yonetimi, sepet, siparis sistemi, JWT tabanli kimlik dogrulama ve admin paneli icermektedir.

<!-- Ana sayfa ekran goruntusu -->
<!-- ![Ana Sayfa](docs/screenshots/homepage.png) -->

## Teknolojiler

### Backend
- **FastAPI** - Python web framework
- **SQLAlchemy 2.x** - ORM
- **MySQL** - Veritabani
- **JWT** - HttpOnly cookie tabanli kimlik dogrulama
- **bcrypt** - Sifre hashleme
- **Pydantic v2** - Veri dogrulama ve sema tanimlama

### Frontend
- **React 18** - UI kutuphanesi
- **Redux Toolkit (RTK Query)** - State yonetimi ve API katmani
- **React Router v6** - Sayfa yonlendirme
- **Tailwind CSS v4** - Stil
- **shadcn/ui** - UI bilesenler
- **Vite** - Build araci

## Ozellikler

**Kullanici**
- Urun listeleme, arama ve kategoriye gore filtreleme
- Urun detay sayfasi
- Sepete ekleme, miktar guncelleme, silme
- Siparis olusturma (stok kontrollu)
- Siparis gecmisi goruntuleme
- Karanlik/aydinlik tema

**Kimlik Dogrulama**
- Kayit ve giris (e-posta veya kullanici adi ile)
- JWT token HttpOnly cookie'de saklanir
- Sayfa yenilemede oturum korunur (`/auth/me`)
- Cikis yapma

**Admin Paneli**
- Kontrol paneli (urun, kategori, siparis, gelir istatistikleri)
- Urun CRUD (gorsel yukleme destegi)
- Kategori CRUD
- Tum siparisleri goruntuleme

<!-- Admin panel ekran goruntusu -->
<!-- ![Admin Panel](docs/screenshots/admin.png) -->

## Proje Yapisi

```
e-commerce-fastapi/
├── app/                          # Backend
│   ├── main.py                   # FastAPI uygulamasi, CORS, lifespan
│   ├── config.py                 # Ortam degiskenleri (pydantic-settings)
│   ├── database.py               # SQLAlchemy engine ve session
│   ├── exception_handlers.py     # Global hata yakalama
│   ├── logging_config.py         # Loglama ayarlari
│   ├── models/                   # SQLAlchemy ORM modelleri
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── order.py
│   │   └── order_item.py
│   ├── schemas/                  # Pydantic request/response semalari
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   └── order.py
│   ├── routers/                  # API endpoint'leri
│   │   ├── auth.py               # /auth (register, login, logout, me)
│   │   ├── product.py            # /product (CRUD + gorsel yukleme)
│   │   ├── category.py           # /category (CRUD)
│   │   └── order.py              # /order (olusturma, listeleme)
│   └── utils/
│       ├── security.py           # JWT & bcrypt islemleri
│       └── dependencies.py       # Auth middleware (cookie-based)
├── static/images/                # Yuklenen urun gorselleri
├── frontend/                     # React uygulamasi
│   └── src/
│       ├── app/                  # Redux store ve RTK Query base API
│       ├── features/             # Ozellik bazli moduller
│       │   ├── auth/             # Giris, kayit, auth state
│       │   ├── products/         # Urun listeleme ve detay
│       │   ├── cart/             # Sepet (localStorage)
│       │   ├── orders/           # Siparis gecmisi
│       │   ├── categories/       # Kategori API
│       │   └── admin/            # Admin panel sayfalari
│       ├── components/           # Layout, route guard, tema
│       └── hooks/                # useAuth hook
└── .env                          # Ortam degiskenleri
```

## Kurulum

### Gereksinimler
- Python 3.11+
- Node.js 18+
- MySQL 8.0+

### 1. Repoyu klonlayin

```bash
git clone https://github.com/KULLANICI_ADINIZ/e-commerce-fastapi.git
cd e-commerce-fastapi
```

### 2. Backend kurulumu

```bash
# Sanal ortam olusturun
python -m venv myenv
source myenv/Scripts/activate  # Windows
# source myenv/bin/activate    # macOS/Linux

# Bagimliliklari yukleyin
pip install fastapi uvicorn sqlalchemy pymysql pydantic pydantic-settings python-dotenv bcrypt python-jose[cryptography] python-multipart

# .env dosyasini duzelneleyin
# DB_URI=mysql+pymysql://root:SIFRENIZ@localhost:3306/VERITABANI_ADI
# JWT_SECRET_KEY=guclu-bir-secret-key
# JWT_ALGORITHM=HS256
# JWT_EXPIRE_MINUTES=30
```

### 3. MySQL veritabanini olusturun

```sql
CREATE DATABASE e_commerce;
```

### 4. Backend'i baslatin

```bash
uvicorn app.main:app --reload
```

Backend `http://localhost:8000` adresinde calisir. API dokumantasyonu: `http://localhost:8000/docs`

### 5. Frontend kurulumu

```bash
cd frontend
npm install

# .env dosyasi
# VITE_API_URL=http://localhost:8000
```

### 6. Frontend'i baslatin

```bash
npm run dev
```

Frontend `http://localhost:5173` adresinde calisir.

## API Endpoint'leri

### Kimlik Dogrulama (`/auth`)
| Method | Endpoint | Aciklama | Yetki |
|--------|----------|----------|-------|
| POST | `/auth/register` | Yeni hesap olusturma | Herkese acik |
| POST | `/auth/login` | Giris yapma (cookie set) | Herkese acik |
| POST | `/auth/logout` | Cikis yapma (cookie sil) | Herkese acik |
| GET | `/auth/me` | Oturum bilgisi | Giris yapilmis |

### Urunler (`/product`)
| Method | Endpoint | Aciklama | Yetki |
|--------|----------|----------|-------|
| GET | `/product/all` | Tum urunleri listele | Herkese acik |
| GET | `/product/{id}` | Urun detayi | Herkese acik |
| POST | `/product/create` | Urun olustur | Admin |
| PUT | `/product/update/{id}` | Urun guncelle | Admin |
| DELETE | `/product/delete/{id}` | Urun sil | Admin |
| POST | `/product/{id}/upload-image` | Urun gorseli yukle | Admin |

### Kategoriler (`/category`)
| Method | Endpoint | Aciklama | Yetki |
|--------|----------|----------|-------|
| GET | `/category/all` | Tum kategoriler | Herkese acik |
| POST | `/category/create` | Kategori olustur | Admin |
| PUT | `/category/update/{id}` | Kategori guncelle | Admin |
| DELETE | `/category/delete/{id}` | Kategori sil | Admin |

### Siparisler (`/order`)
| Method | Endpoint | Aciklama | Yetki |
|--------|----------|----------|-------|
| GET | `/order/all` | Tum siparisler | Admin |
| GET | `/order/my-orders` | Kullanicinin siparisleri | Giris yapilmis |
| POST | `/order/create` | Siparis olustur | Giris yapilmis |

## Veritabani Semasi

```
User ──1:N──> Order ──1:N──> OrderItem <──N:1── Product <──N:1── Category
```

- **User**: id, firstName, lastName, userName, email, password, role, isActive
- **Product**: id, name, description, price, stock, isActive, image_url, category_id
- **Category**: id, name
- **Order**: id, user_id, total_price, status
- **OrderItem**: id, order_id, product_id, quantity, price (siparis anindaki fiyat)

## Ekran Goruntuleri

Asagidaki goruntuleri `docs/screenshots/` klasorune ekleyin:

| Ekran | Dosya Adi |
|-------|-----------|
| Ana sayfa (urun listesi) | `homepage.png` |
| Urun detay sayfasi | `product-detail.png` |
| Sepet sayfasi | `cart.png` |
| Giris sayfasi | `login.png` |
| Admin paneli | `admin.png` |
| Admin urun yonetimi | `admin-products.png` |
| Karanlik tema | `dark-mode.png` |

Gorselleri ekledikten sonra bu README'deki yorum satirlarini (`<!-- -->`) kaldirup gorselleri aktif edin:

```markdown
![Ana Sayfa](docs/screenshots/homepage.png)
![Admin Panel](docs/screenshots/admin.png)
```

## Lisans

Bu proje MIT lisansi altinda lisanslanmistir.
