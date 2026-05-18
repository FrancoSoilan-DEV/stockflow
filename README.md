<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=120&color=gradient&customColorList=2,12,24&reversal=true&text=Stockflow&fontColor=ffffff&fontSize=52&fontAlignY=35&desc=FastAPI%20%7C%20Vue%203%20%7C%20PostgreSQL%20%7C%20WebSockets%20%7C%20Docker&descAlignY=58&descSize=16" />
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Multi-branch+Inventory+Management+System;FastAPI+%2B+Vue+3+%2B+PostgreSQL;Real-time+Stock+Updates+via+WebSockets;JWT+Auth+%2B+Role-based+Access+Control;Fully+Dockerized+%E2%80%94+One+Command+Setup&center=true&width=850&height=40&color=34D399">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Vue.js-3-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-CC0000?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Alembic-Migrations-6f42c1?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/WebSockets-Real--time-010101?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/JWT-Auth-F7B731?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Tailwind-CSS-38BDF8?style=for-the-badge&logo=tailwindcss&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
</p>

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Roles and Permissions](#roles-and-permissions)
- [API Modules](#api-modules)
- [Real-time WebSockets](#real-time-websockets)
- [Database Models](#database-models)
- [Routes Overview](#routes-overview)
- [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Useful Commands](#useful-commands)
- [Version en Español](#version-en-espanol)

---

## Overview

**Stockflow** is a multi-branch inventory management system built for businesses that operate across multiple physical locations. It provides a complete solution for tracking stock, recording sales, managing inter-branch stock transfer requests, and enabling real-time communication between staff members.

The system supports two user roles:

| Role | Main Responsibility |
|---|---|
| Admin | Full access — manage branches, users, products, stock, approve/reject requests |
| Staff | Operational access — sell products, view stock, request stock from other branches, chat |

The project is built with **FastAPI**, **SQLAlchemy**, **Alembic**, **Vue 3**, **Pinia**, **Tailwind CSS**, **WebSockets**, **JWT authentication**, and **Docker Compose**.

---

## Core Features

- JWT-based authentication with role-based access control
- Multi-branch stock tracking per product
- Point-of-sale style sales recording with automatic stock deduction
- Inter-branch stock transfer request system with approval workflow
- Real-time stock update notifications via WebSockets
- Real-time private chat between users via WebSockets
- Real-time user presence (online/offline) via WebSockets
- Full CRUD for branches, users, products
- Admin-only operations protected at the API level
- Fully Dockerized — one command to run everything

---

## Tech Stack

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,fastapi,postgres,vue,tailwind,docker,github,vscode" />
</p>

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI 0.136 |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Database | PostgreSQL 16 |
| Authentication | JWT via python-jose + passlib bcrypt |
| Real-time | Native WebSockets (FastAPI) |
| Frontend Framework | Vue 3 (Composition API) |
| State Management | Pinia |
| Routing | Vue Router 4 |
| HTTP Client | Axios |
| Styling | Tailwind CSS v4 |
| Containerization | Docker + Docker Compose |
| Python Runtime | Python 3.13 |
| Node Runtime | Node 22 (Alpine) |

---

## Architecture

```text
Browser
  │
  ├── HTTP requests  (Axios → REST API)
  ├── WebSocket connections  (ws://host:8000/ws/*)
  ▼
Vue 3 Frontend  (port 5173)
  │
  ▼
FastAPI Backend  (port 8000)
  │
  ├── REST endpoints      → business logic + auth
  ├── WebSocket endpoints → real-time stock, chat, presence
  └── SQLAlchemy async    → database queries
  │
  ▼
PostgreSQL 16  (port 5432)
```

All services run inside Docker containers orchestrated by Docker Compose. The frontend container runs Vite dev server with hot reload. The backend container runs Uvicorn with hot reload.

---

## Project Structure

```text
STOCKFLOW/
│
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── core/
│   │   ├── config.py          ← settings (DATABASE_URL, JWT config)
│   │   ├── dependencies.py    ← get_current_user, require_admin
│   │   ├── security.py        ← JWT creation, password hashing
│   │   └── ws_manager.py      ← WebSocket connection manager
│   ├── db/
│   │   ├── base.py            ← SQLAlchemy declarative base
│   │   ├── engine.py          ← async engine
│   │   └── session.py         ← async session factory
│   ├── models/
│   │   └── models.py          ← all SQLAlchemy models
│   ├── routers/
│   │   ├── api.py             ← main router aggregator
│   │   ├── auth.py            ← /auth/login, /auth/me
│   │   ├── branches.py        ← /branches/
│   │   ├── products.py        ← /products/
│   │   ├── users.py           ← /users/
│   │   ├── stock.py           ← /stock/
│   │   ├── sales.py           ← /sales/
│   │   ├── stock_requests.py  ← /stock-requests/
│   │   └── ws.py              ← /ws/stock, /ws/chat, /ws/presence
│   ├── schemas/
│   │   ├── branch.py
│   │   ├── product.py
│   │   ├── sale.py
│   │   ├── stock.py
│   │   ├── stock_request.py
│   │   └── user.py
│   ├── services/              ← business logic layer
│   ├── .env
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── seed.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── axios.js       ← axios instance + interceptors
│   │   │   └── index.js       ← all API modules
│   │   ├── assets/
│   │   │   └── main.css       ← Tailwind CSS entry
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── AppLayout.vue  ← sidebar + topbar
│   │   │   └── StatCard.vue
│   │   ├── router/
│   │   │   └── index.js       ← Vue Router + auth guards
│   │   ├── stores/
│   │   │   └── auth.js        ← Pinia auth store
│   │   └── views/
│   │       ├── auth/
│   │       │   └── LoginView.vue
│   │       ├── branches/
│   │       ├── chat/
│   │       ├── products/
│   │       ├── sales/
│   │       ├── stock/
│   │       ├── stock-requests/
│   │       ├── users/
│   │       └── DashboardView.vue
│   ├── .env
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── compose.yml
├── Makefile
├── .gitignore
└── README.md
```

---

## Roles and Permissions

| Endpoint | Admin | Staff |
|---|---|---|
| GET /branches/ | ✅ | ✅ |
| POST /branches/ | ✅ | ❌ |
| PATCH/DELETE /branches/ | ✅ | ❌ |
| GET /users/ | ✅ | ✅ |
| POST /users/ | ✅ | ❌ |
| PATCH/DELETE /users/ | ✅ | ❌ |
| GET /products/ | ✅ | ✅ |
| POST /products/ | ✅ | ❌ |
| GET /stock/ | ✅ | ✅ |
| PATCH /stock/ | ✅ | ✅ |
| GET /sales/ | ✅ | ✅ |
| POST /sales/ | ✅ | ✅ |
| GET /stock-requests/ (all) | ✅ | ❌ |
| GET /stock-requests/branch/ | ✅ | ✅ |
| POST /stock-requests/ | ✅ | ✅ |
| PATCH /stock-requests/status | ✅ | ❌ |

---

## API Modules

### Auth

```text
POST /auth/login     → returns JWT token
GET  /auth/me        → returns current user
```

### Branches

```text
GET    /branches/              → list all branches
GET    /branches/{id}          → get branch by ID
POST   /branches/              → create branch (admin)
PATCH  /branches/{id}          → update branch (admin)
DELETE /branches/{id}          → delete branch (admin)
```

### Users

```text
GET    /users/                 → list all users
GET    /users/{id}             → get user by ID
POST   /users/                 → create user (admin)
PATCH  /users/{id}             → update user (admin)
DELETE /users/{id}             → delete user (admin)
```

### Products

```text
GET    /products/              → list all products
GET    /products/{id}          → get product by ID
POST   /products/              → create product (admin)
PATCH  /products/{id}          → update product (admin)
DELETE /products/{id}          → delete product (admin)
```

### Stock

```text
GET    /stock/branch/{id}                          → stock by branch
GET    /stock/product/{id}                         → stock across all branches
PATCH  /stock/branch/{branch_id}/product/{prod_id} → update quantity
```

### Sales

```text
GET  /sales/branch/{id}        → sales by branch
GET  /sales/{id}               → sale detail with items
POST /sales/branch/{id}        → create sale (validates stock, deducts automatically)
```

### Stock Requests

```text
GET   /stock-requests/                    → all requests (admin)
GET   /stock-requests/branch/{id}         → requests by branch
GET   /stock-requests/{id}                → request detail
POST  /stock-requests/                    → create request
PATCH /stock-requests/{id}/status         → approve or reject (admin, transfers stock)
```

---

## Real-time WebSockets

All WebSocket connections require a JWT token passed as a query parameter.

```text
ws://localhost:8000/ws/stock?token=<jwt>
ws://localhost:8000/ws/chat?token=<jwt>
ws://localhost:8000/ws/presence?token=<jwt>
```

### Stock channel `/ws/stock`

Receives real-time notifications whenever stock is updated anywhere in the system.

```json
{
  "type": "stock_updated",
  "product_id": "uuid",
  "product_name": "Teclado Mecánico RGB",
  "branch_id": "uuid",
  "branch_name": "Sucursal Centro",
  "quantity": 7
}
```

### Chat channel `/ws/chat`

Enables private messaging between users.

Send a message:

```json
{
  "receiver_id": "uuid",
  "content": "Hello, do you have keyboards in stock?"
}
```

Receive a message:

```json
{
  "type": "message",
  "sender_id": "uuid",
  "sender_username": "juan",
  "content": "Yes, we have 3 units.",
  "created_at": "2026-05-18T15:00:00+00:00"
}
```

### Presence channel `/ws/presence`

Tracks which users are currently online.

```json
{
  "type": "presence",
  "user_id": "uuid",
  "status": "online"
}
```

On connect, the server immediately sends the current online users list:

```json
{
  "type": "online_users",
  "users": ["uuid1", "uuid2"]
}
```

---

## Database Models

<details>
<summary><strong>Branch</strong> — Physical store location</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | String(100) | Branch name |
| address | String(255) | Physical address (optional) |

</details>

<details>
<summary><strong>User</strong> — System user</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| branch_id | UUID (FK) | Assigned branch |
| username | String(50) | Unique username |
| email | String(255) | Unique email |
| hashed_password | String | bcrypt hash |
| role | Enum | admin / staff |

</details>

<details>
<summary><strong>Product</strong> — Sellable item</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| name | String(150) | Product name |
| description | Text | Optional description |
| category | String(100) | Product category |
| price | Float | Current price |

</details>

<details>
<summary><strong>Stock</strong> — Inventory per branch</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| branch_id | UUID (FK) | Branch |
| product_id | UUID (FK) | Product |
| quantity | Integer | Available units |

</details>

<details>
<summary><strong>Sale</strong> — Sales transaction</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| branch_id | UUID (FK) | Branch where sold |
| user_id | UUID (FK) | Staff who made the sale |
| total | Float | Calculated total |
| created_at | DateTime | Timestamp |

</details>

<details>
<summary><strong>SaleItem</strong> — Line item inside a sale</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| sale_id | UUID (FK) | Parent sale |
| product_id | UUID (FK) | Product |
| quantity | Integer | Units sold |
| unit_price | Float | Price snapshot at time of sale |

</details>

<details>
<summary><strong>StockRequest</strong> — Inter-branch transfer request</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| from_branch_id | UUID (FK) | Requesting branch |
| to_branch_id | UUID (FK) | Source branch |
| product_id | UUID (FK) | Product requested |
| quantity | Integer | Units requested |
| status | Enum | pending / approved / rejected |
| created_at | DateTime | Timestamp |

When approved by an admin, stock is automatically transferred from `to_branch` to `from_branch`.

</details>

<details>
<summary><strong>Message</strong> — Private chat message</summary>

| Field | Type | Description |
|---|---|---|
| id | UUID | Primary key |
| sender_id | UUID (FK) | Sender user |
| receiver_id | UUID (FK) | Receiver user |
| content | Text | Message body |
| created_at | DateTime | Timestamp |

</details>

---

## Routes Overview

### Backend (FastAPI) — port 8000

```text
GET    /                         Health check
POST   /auth/login               Login
GET    /auth/me                  Current user

GET    /branches/
GET    /branches/{id}
POST   /branches/
PATCH  /branches/{id}
DELETE /branches/{id}

GET    /users/
GET    /users/{id}
POST   /users/
PATCH  /users/{id}
DELETE /users/{id}

GET    /products/
GET    /products/{id}
POST   /products/
PATCH  /products/{id}
DELETE /products/{id}

GET    /stock/branch/{branch_id}
GET    /stock/product/{product_id}
PATCH  /stock/branch/{branch_id}/product/{product_id}

GET    /sales/branch/{branch_id}
GET    /sales/{sale_id}
POST   /sales/branch/{branch_id}

GET    /stock-requests/
GET    /stock-requests/branch/{branch_id}
GET    /stock-requests/{request_id}
POST   /stock-requests/
PATCH  /stock-requests/{request_id}/status

WS     /ws/stock
WS     /ws/chat
WS     /ws/presence
```

### Frontend (Vue 3) — port 5173

```text
/login             Login page
/                  Dashboard
/branches          Branches management
/users             Users management (admin only)
/products          Products catalog
/stock             Stock by branch
/sales             Sales history + new sale
/stock-requests    Inter-branch requests
/chat              Real-time chat
```

---

## Docker Setup

The project runs with three containers:

| Container | Image | Port | Purpose |
|---|---|---|---|
| `stockflow-fastapi` | python:3.13-slim | 8000 | FastAPI backend |
| `stockflow-vue` | node:22-alpine | 5173 | Vue 3 frontend |
| `stockflow-db` | postgres:16 | 5432 | PostgreSQL database |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/FrancoSoilan-DEV/stockflow
cd stockflow
```

### 2. Create environment files

**`backend/.env`:**

```env
DATABASE_URL=postgresql+asyncpg://stockflow_user:stockflow_password@db:5432/stockflow_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**`frontend/.env`:**

```env
VITE_API_URL=http://localhost:8000
```

### 3. Start everything

```bash
make up-b
```

or without Make:

```bash
docker compose up --build
```

### 4. Run migrations and seed data

```bash
make migrate
make seed
```

### 5. Open the app

```text
http://localhost:5173
```

Default credentials from seed:

| Email | Password | Role | Branch |
|---|---|---|---|
| admin@stockflow.com | admin123 | Admin | Centro |
| juan@stockflow.com | juan123 | Staff | Centro |
| maria@stockflow.com | maria123 | Staff | Norte |
| carlos@stockflow.com | carlos123 | Staff | Sur |

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description |
|---|---|
| `DATABASE_URL` | Async PostgreSQL connection string |
| `SECRET_KEY` | JWT signing secret |
| `ALGORITHM` | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry in minutes |

### Frontend (`frontend/.env`)

| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend base URL for Axios |

---

## Useful Commands

```bash
# Start with rebuild
make up-b

# Start detached with rebuild
make up-b-d

# Start without rebuild
make up

# Stop containers
make down

# View backend logs
make logs

# Open backend shell
make shell

# Run database migrations
make migrate

# Create a new migration
make migration msg="your migration message"

# Rollback last migration
make downgrade

# Seed the database
make seed
```

---

## Security Notes

Before deploying to production:

- Never commit `.env` files
- Use a strong random `SECRET_KEY`
- Set a short `ACCESS_TOKEN_EXPIRE_MINUTES` for sensitive environments
- Restrict `allow_origins` in CORS middleware to your actual domain
- Use HTTPS in production
- Rotate any credentials that were ever exposed

---

<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=120&color=gradient&customColorList=2,12,24&section=footer&text=Versi%C3%B3n%20en%20Espa%C3%B1ol&fontColor=ffffff&fontSize=32&fontAlignY=55" />
</div>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Sistema+de+Inventario+Multi-sucursal;FastAPI+%2B+Vue+3+%2B+PostgreSQL;Stock+en+tiempo+real+via+WebSockets;Auth+JWT+%2B+Control+de+acceso+por+rol;Todo+en+Docker+%E2%80%94+Un+solo+comando&center=true&width=850&height=40&color=34D399">
</p>

---

# Version en Espanol

## Descripcion General

**Stockflow** es un sistema de gestión de inventario multi-sucursal pensado para empresas que operan en múltiples ubicaciones físicas. Permite hacer seguimiento de stock, registrar ventas, gestionar pedidos de transferencia de stock entre sucursales y habilitar comunicación en tiempo real entre el personal.

El sistema soporta dos roles de usuario:

| Rol | Responsabilidad principal |
|---|---|
| Admin | Acceso completo — gestionar sucursales, usuarios, productos, stock, aprobar/rechazar pedidos |
| Staff | Acceso operativo — vender, ver stock, pedir stock a otras sucursales, chatear |

---

## Funcionalidades Principales

- Autenticación JWT con control de acceso por rol
- Seguimiento de stock por sucursal y producto
- Registro de ventas con descuento automático de stock
- Sistema de pedidos de transferencia entre sucursales con flujo de aprobación
- Notificaciones de actualización de stock en tiempo real via WebSockets
- Chat privado entre usuarios via WebSockets
- Presencia de usuarios en tiempo real (online/offline) via WebSockets
- CRUD completo de sucursales, usuarios y productos
- Operaciones de admin protegidas a nivel de API
- Completamente Dockerizado — un solo comando para levantar todo

---

## Stack Tecnologico

| Capa | Tecnología |
|---|---|
| Backend | FastAPI 0.136 |
| ORM | SQLAlchemy 2.0 (async) |
| Migraciones | Alembic |
| Base de datos | PostgreSQL 16 |
| Autenticación | JWT con python-jose + passlib bcrypt |
| Tiempo real | WebSockets nativos de FastAPI |
| Frontend | Vue 3 (Composition API) |
| Estado global | Pinia |
| Ruteo | Vue Router 4 |
| Cliente HTTP | Axios |
| Estilos | Tailwind CSS v4 |
| Contenedores | Docker + Docker Compose |

---

## Arquitectura

```text
Navegador
  │
  ├── Requests HTTP  (Axios → REST API)
  ├── Conexiones WebSocket  (ws://host:8000/ws/*)
  ▼
Frontend Vue 3  (puerto 5173)
  │
  ▼
Backend FastAPI  (puerto 8000)
  │
  ├── Endpoints REST     → lógica de negocio + auth
  ├── Endpoints WS       → stock en tiempo real, chat, presencia
  └── SQLAlchemy async   → consultas a la base de datos
  │
  ▼
PostgreSQL 16  (puerto 5432)
```

---

## Roles y Permisos

| Endpoint | Admin | Staff |
|---|---|---|
| Ver sucursales, productos, stock, ventas | ✅ | ✅ |
| Crear/editar/eliminar sucursales | ✅ | ❌ |
| Crear/editar/eliminar usuarios | ✅ | ❌ |
| Crear/editar/eliminar productos | ✅ | ❌ |
| Ajustar stock | ✅ | ✅ |
| Crear ventas | ✅ | ✅ |
| Ver todos los pedidos de stock | ✅ | ❌ |
| Crear pedidos de stock | ✅ | ✅ |
| Aprobar/rechazar pedidos | ✅ | ❌ |

---

## WebSockets en Tiempo Real

Todos los WebSockets requieren token JWT como query param:

```text
ws://localhost:8000/ws/stock?token=<jwt>
ws://localhost:8000/ws/chat?token=<jwt>
ws://localhost:8000/ws/presence?token=<jwt>
```

### Canal de Stock `/ws/stock`

Recibe notificaciones cada vez que el stock cambia en cualquier sucursal.

### Canal de Chat `/ws/chat`

Permite mensajería privada entre usuarios. Los mensajes se guardan en la base de datos.

### Canal de Presencia `/ws/presence`

Informa quién está conectado en tiempo real.

---

## Modelos de Base de Datos

| Modelo | Descripción |
|---|---|
| Branch | Sucursal física |
| User | Usuario del sistema (admin o staff) |
| Product | Producto vendible |
| Stock | Inventario de un producto en una sucursal |
| Sale | Transacción de venta |
| SaleItem | Ítem dentro de una venta (con precio histórico) |
| StockRequest | Pedido de transferencia entre sucursales |
| Message | Mensaje privado entre usuarios |

---

## Inicio Rápido con Docker

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd stockflow

# Crear archivos de entorno
# backend/.env y frontend/.env (ver sección de variables)

# Levantar todo
make up-b

# Migrar y poblar la base de datos
make migrate
make seed

# Abrir en el navegador
http://localhost:5173
```

Credenciales por defecto del seed:

| Email | Contraseña | Rol | Sucursal |
|---|---|---|---|
| admin@stockflow.com | admin123 | Admin | Centro |
| juan@stockflow.com | juan123 | Staff | Centro |
| maria@stockflow.com | maria123 | Staff | Norte |
| carlos@stockflow.com | carlos123 | Staff | Sur |

---

## Variables de Entorno

### Backend (`backend/.env`)

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Conexión async a PostgreSQL |
| `SECRET_KEY` | Clave para firmar JWT |
| `ALGORITHM` | Algoritmo JWT (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de validez del token |

### Frontend (`frontend/.env`)

| Variable | Descripción |
|---|---|
| `VITE_API_URL` | URL base del backend para Axios |

---

## Comandos Útiles

```bash
make up-b          # Levantar con rebuild
make up-b-d        # Levantar en modo detached con rebuild
make up            # Levantar sin rebuild
make down          # Bajar contenedores
make logs          # Ver logs del backend
make shell         # Abrir shell del backend
make migrate       # Aplicar migraciones
make migration msg="nombre"  # Crear migración
make downgrade     # Revertir última migración
make seed          # Poblar la base de datos
```

---

## Seguridad

Antes de deployar a producción:

- Nunca subir archivos `.env` al repositorio
- Usar un `SECRET_KEY` largo y aleatorio
- Restringir `allow_origins` en CORS al dominio real
- Usar HTTPS en producción
- Rotar cualquier credencial que haya sido expuesta

---

<div align="center">
  <h3>Built with FastAPI, Vue 3, WebSockets, Docker and a lot of ☕</h3>
</div>

<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&color=gradient&customColorList=2,12,24&section=footer" />
</div>
