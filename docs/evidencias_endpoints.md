# Evidências de Endpoints - Sistema de Gestão de Demandas

## 1. Login JWT

**Método:** POST  
**URL:** `/user/generate_jwt/`

**Body:**
```json
{
  "cpf": "123.456.789-00",
  "password": "SenhaSegura123"
}
```

**Response:**
```json
{
  "user_id": 1,
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTk4NzY1NCwiaWF0IjoxNjg5OTAxMjU0LCJqdGkiOiI4ZjI3YzM0ZGQ0MjM0YmQxYjk4YTJlOGE1ZjcxNjY5YSIsInVzZXJfaWQiOjF9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5OTA0ODU0LCJpYXQiOjE2ODk5MDEyNTQsImp0aSI6ImY4YzQ1ZjU2ZTU0OTRhZGQ4YjJhMDU2YzM5ZDAxNTUwIiwidXNlcl9pZCI6MX0..."
}
```

**Status Code:** `200 OK`

---

**Erro - Conta não ativada:**

**Body:**
```json
{
  "cpf": "123.456.789-00",
  "password": "SenhaSegura123"
}
```

**Response:**
```json
{
  "msg": "Conta ainda não ativada"
}
```

**Status Code:** `401 UNAUTHORIZED`

---

**Erro - Credenciais incorretas:**

**Response:**
```json
{
  "msg": "Usuário ou senha incorretos"
}
```

**Status Code:** `401 UNAUTHORIZED`

---

## 2. Verificação/Refresh do Token

**Método:** POST  
**URL:** `/api/token/verify/` (Django REST Framework Simple JWT)

**Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{}
```

**Status Code:** `200 OK`

---

**Método:** POST  
**URL:** `/api/token/refresh/`

**Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg5OTA4NDU0LCJpYXQiOjE2ODk5MDQ4NTQsImp0aSI6IjZhYjM0ZTU2ZjU0OTRhZGQ4YjJhMDU2YzM5ZDAxNTUwIiwidXNlcl9pZCI6MX0..."
}
```

**Status Code:** `200 OK`

---

## 3. Cadastro de Usuário

**Método:** POST  
**URL:** `/user/create/`

**Body:**
```json
{
  "nome": "João da Silva",
  "dataNasc": "1990-05-15",
  "cpf": "987.654.321-00",
  "endereco": "Rua das Flores, 123, Centro, Ceres-GO",
  "telefone": "62999887766",
  "email": "joao.silva@exemplo.com",
  "password": "SenhaForte456"
}
```

**Response:**
```html
Confirme seu email para confirmar o registro
```

**Status Code:** `200 OK`

**Observações:**
- Usuário criado com `is_active = False`
- UserType automaticamente definido como 1 (Cidadão)
- Email enviado com link de ativação

---

**Erro - Email já existe:**

**Response:**
```json
{
  "error": "Este email já existe"
}
```

**Status Code:** `400 BAD REQUEST`

---

**Erro - CPF já existe:**

**Response:**
```json
{
  "error": "Este cpf já existe"
}
```

**Status Code:** `400 BAD REQUEST`

---

## 4. Ativação de Conta por Email

**Método:** GET  
**URL:** `/user/activate/<uidb64>/<token>/`  
**Exemplo:** `/user/activate/MQ/b7k3n9-8f5a4c3d2e1f0a9b8c7d6e5f4/`

**Response:**
```html
<h2 style="font-family: Arial, Helvetica, sans-serif;">
    Seu email foi confirmado
</h2>
```

**Status Code:** `200 OK`

**Observações:**
- Altera `is_active` para `True`
- Usuário pode fazer login após ativação

---

## 5. Recuperar Senha

**Método:** POST  
**URL:** `/user/reset_password/`

**Body:**
```json
{
  "email": "joao.silva@exemplo.com",
  "cpf": "987.654.321-00"
}
```

**Response:**
```json
{
  "msg": "A sua nova senha foi enviada para seu email"
}
```

**Status Code:** `200 OK`

**Observações:**
- Gera senha aleatória de 10 caracteres (letras + números)
- Envia nova senha por email
- Valida se email e CPF pertencem ao mesmo usuário

---

**Erro - Dados inválidos:**

**Response:**
```json
{
  "error": "Email ou cpf inválidos"
}
```

**Status Code:** `400 BAD REQUEST`

---

## 6. Criar Solicitação com Imagens

**Método:** POST  
**URL:** `/request/create/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Body:**
```json
{
  "id_user": 1,
  "request_type": 3,
  "comment": "Poste de iluminação pública queimado na esquina da Rua das Flores com Avenida Central. Está assim há 3 dias.",
  "lat": "-15.3150",
  "lon": "-49.5975",
  "img1": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIA...",
  "img2": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIA...",
  "img3": "/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAABAAEDASIA..."
}
```

**Response:**
```json
{
  "id": 42,
  "id_user": 1,
  "request_type": 3,
  "importance": null,
  "img1": "/media/fotos/21/02/2026/3f8a92c4b1e24e9f8a2d7c5e6f1a9b8c.jpg",
  "img2": "/media/fotos/21/02/2026/7b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e.jpg",
  "img3": "/media/fotos/21/02/2026/5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b.jpg",
  "comment": "Poste de iluminação pública queimado na esquina da Rua das Flores com Avenida Central. Está assim há 3 dias.",
  "lat": "-15.3150",
  "lon": "-49.5975",
  "created": "2026-02-21T14:30:25.123456Z",
  "completed": null,
  "is_canceled": false,
  "current_status": 1,
  "current_status_updated_at": "2026-02-21T14:30:25.123456Z"
}
```

**Status Code:** `200 OK`

**Observações:**
- Imagens em base64 são convertidas para JPG
- Status inicial = 1 (Em Andamento)
- Cria automaticamente registro inicial no histórico de status
- Salva imagens com UUID único + .jpg
- Caminho: `/media/fotos/DD/MM/YYYY/`

---

## 7. Listar Solicitações (Admin)

**Método:** GET  
**URL:** `/request/reqs/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 42,
    "id_user": {
      "id": 1,
      "nome": "João da Silva",
      "email": "joao.silva@exemplo.com",
      "cpf": "***.***.***.***"
    },
    "request_type": {
      "id": 3,
      "desc": "Iluminação pública",
      "title": "Poste queimado",
      "icon": "/media/assets/icon_iluminacao.png",
      "banner": "/media/assets/banner_iluminacao.png"
    },
    "current_status": {
      "id": 2,
      "desc": "Em andamento"
    },
    "importance": null,
    "comment": "Poste de iluminação pública queimado na esquina da Rua das Flores com Avenida Central.",
    "lat": "-15.3150",
    "lon": "-49.5975",
    "created": "2026-02-21T14:30:25.123456Z",
    "completed": null,
    "is_canceled": false,
    "current_status_updated_at": "2026-02-21T15:45:10.654321Z"
  },
  {
    "id": 41,
    "id_user": {
      "id": 5,
      "nome": "Maria Santos",
      "email": "maria.santos@exemplo.com",
      "cpf": "***.***.***.***"
    },
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação",
      "icon": "/media/assets/icon_buraco.png",
      "banner": "/media/assets/banner_buraco.png"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "importance": null,
    "comment": "Buraco grande na Rua Principal causando risco de acidentes.",
    "lat": "-15.3145",
    "lon": "-49.5980",
    "created": "2026-02-20T10:15:30.987654Z",
    "completed": "2026-02-21T16:20:00.123456Z",
    "is_canceled": false,
    "current_status_updated_at": "2026-02-21T16:20:00.123456Z"
  }
]
```

**Status Code:** `200 OK`

**Observações:**
- Retorna todas as solicitações ordenadas por data (mais recentes primeiro)
- Não retorna imagens em base64, apenas URLs
- Inclui dados relacionados (usuário, tipo, status)

---

## 8. Listar Minhas Solicitações (Cidadão)

**Método:** GET  
**URL:** `/request/<user_id>/user/`  
**Exemplo:** `/request/1/user/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 42,
    "id_user": {
      "id": 1,
      "nome": "João da Silva",
      "email": "joao.silva@exemplo.com",
      "cpf": "987.654.321-00"
    },
    "request_type": {
      "id": 3,
      "desc": "Iluminação pública",
      "title": "Poste queimado",
      "icon": "/media/assets/icon_iluminacao.png",
      "banner": "/media/assets/banner_iluminacao.png"
    },
    "current_status": {
      "id": 2,
      "desc": "Em andamento"
    },
    "importance": null,
    "comment": "Poste de iluminação pública queimado na esquina.",
    "lat": "-15.3150",
    "lon": "-49.5975",
    "created": "2026-02-21T14:30:25.123456Z",
    "completed": null,
    "is_canceled": false,
    "current_status_updated_at": "2026-02-21T15:45:10.654321Z"
  },
  {
    "id": 38,
    "id_user": {
      "id": 1,
      "nome": "João da Silva",
      "email": "joao.silva@exemplo.com",
      "cpf": "987.654.321-00"
    },
    "request_type": {
      "id": 5,
      "desc": "Lixo acumulado",
      "title": "Coleta de lixo",
      "icon": "/media/assets/icon_lixo.png",
      "banner": "/media/assets/banner_lixo.png"
    },
    "current_status": {
      "id": 5,
      "desc": "Cancelada"
    },
    "importance": null,
    "comment": "Acúmulo de lixo na calçada, solicitação duplicada.",
    "lat": "-15.3160",
    "lon": "-49.5985",
    "created": "2026-02-18T09:20:15.456789Z",
    "completed": null,
    "is_canceled": true,
    "current_status_updated_at": "2026-02-18T10:05:30.789012Z"
  }
]
```

**Status Code:** `200 OK`

**Observações:**
- Retorna apenas solicitações do usuário autenticado
- Ordenado por data (mais recentes primeiro)

---

## 9. Detalhar Solicitação

**Método:** GET  
**URL:** `/request/<id>/`  
**Exemplo:** `/request/42/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "id": 42,
  "id_user": {
    "id": 1,
    "nome": "João da Silva",
    "email": "joao.silva@exemplo.com",
    "cpf": "987.654.321-00",
    "telefone": "62999887766",
    "endereco": "Rua das Flores, 123, Centro, Ceres-GO",
    "dataNasc": "1990-05-15"
  },
  "request_type": {
    "id": 3,
    "desc": "Iluminação pública",
    "title": "Poste queimado",
    "icon": "/media/assets/icon_iluminacao.png",
    "banner": "/media/assets/banner_iluminacao.png"
  },
  "current_status": {
    "id": 2,
    "desc": "Em andamento"
  },
  "importance": null,
  "img1": "/media/fotos/21/02/2026/3f8a92c4b1e24e9f8a2d7c5e6f1a9b8c.jpg",
  "img2": "/media/fotos/21/02/2026/7b9c1d2e3f4a5b6c7d8e9f0a1b2c3d4e.jpg",
  "img3": "/media/fotos/21/02/2026/5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b.jpg",
  "comment": "Poste de iluminação pública queimado na esquina da Rua das Flores com Avenida Central. Está assim há 3 dias.",
  "lat": "-15.3150",
  "lon": "-49.5975",
  "created": "2026-02-21T14:30:25.123456Z",
  "completed": null,
  "is_canceled": false,
  "current_status_updated_at": "2026-02-21T15:45:10.654321Z"
}
```

**Status Code:** `200 OK`

**Observações:**
- Retorna todos os detalhes da solicitação
- URLs das imagens (não base64)
- Dados completos do usuário e tipo

---

## 10. Visualizar Histórico de Status

**Método:** GET  
**URL:** `/request/<id>/status/`  
**Exemplo:** `/request/42/status/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 128,
    "id_request": 42,
    "status_code": {
      "id": 2,
      "desc": "Em andamento"
    },
    "dateTime": "2026-02-21T15:45:10.654321Z"
  },
  {
    "id": 127,
    "id_request": 42,
    "status_code": {
      "id": 1,
      "desc": "Em análise"
    },
    "dateTime": "2026-02-21T14:30:25.123456Z"
  }
]
```

**Status Code:** `200 OK`

**Observações:**
- Ordenado por data (mais recente primeiro)
- Histórico completo de mudanças de status

---

## 11. Cancelar Solicitação

**Método:** PUT  
**URL:** `/request/<pk>/cancel/`  
**Exemplo:** `/request/42/cancel/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Sucesso):**
```json
{
  "msg": "Requisição cancelada com sucesso"
}
```

**Status Code:** `200 OK`

**Observações:**
- Apenas possível se `current_status = 1` (Em Análise)
- Altera `is_canceled` para `true`
- Altera `current_status` para `5` (Cancelado)
- Atualiza `current_status_updated_at`
- Cria registro no histórico de status

---

**Erro - Solicitação não existe:**

**Response:**
```json
{
  "msg": "Esta solicitação não existe"
}
```

**Status Code:** `404 NOT FOUND`

---

**Erro - Status não permite cancelamento:**

**Response:**
```json
{
  "msg": "A requisição não está com o status inicial, portanto não pode ser cancelada"
}
```

**Status Code:** `400 BAD REQUEST`

---

## 12. Alterar Status da Solicitação (Gestor)

**Método:** GET  
**URL:** `/request/change_status/<pk>/status/<status_code>`  
**Exemplo:** `/request/change_status/42/status/3`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Sucesso):**
```json
{
  "msg": "Status da solicitção atualizada com sucesso"
}
```

**Status Code:** `200 OK`

**Observações:**
- Apenas gestor pode alterar
- Não pode alterar para status `5` (Cancelado) - apenas via cancelamento
- Status deve ser diferente do atual
- Cria registro no histórico
- Atualiza `current_status_updated_at`

---

**Erro - Solicitação não existe:**

**Response:**
```json
{
  "msg": "Solicitação não existe"
}
```

**Status Code:** `404 NOT FOUND`

---

**Erro - Código de status não existe:**

**Response:**
```json
{
  "msg": "Código do status não existe"
}
```

**Status Code:** `404 NOT FOUND`

---

**Erro - Código de status inválido (tentativa de usar status 5):**

**Response:**
```json
{
  "msg": "Código do status inválido"
}
```

**Status Code:** `400 BAD REQUEST`

---

**Erro - Status repetido:**

**Response:**
```json
{
  "msg": "Escolha um status diferente do atual"
}
```

**Status Code:** `400 BAD REQUEST`

---

## 13. Adicionar Comentário

**Método:** POST  
**URL:** `/request/create/comment/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Body:**
```json
{
  "id_request": 42,
  "id_user": 3,
  "message": "Equipe já foi enviada ao local. Previsão de conclusão: 2 dias úteis."
}
```

**Response:**
```json
{
  "id": 85,
  "id_request": 42,
  "id_user": {
    "id": 3,
    "nome": "Carlos Gestor",
    "email": "carlos.gestor@prefeitura.go.gov.br",
    "cpf": "***.***.***.***"
  },
  "message": "Equipe já foi enviada ao local. Previsão de conclusão: 2 dias úteis.",
  "created_at": "2026-02-21T16:10:45.789012Z"
}
```

**Status Code:** `200 OK`

---

**Erro - Solicitação não existe:**

**Response:**
```json
{
  "msg": "Solicitação não existe"
}
```

**Status Code:** `404 NOT FOUND`

---

**Erro - Usuário não existe:**

**Response:**
```json
{
  "msg": "Usuário não existe"
}
```

**Status Code:** `404 NOT FOUND`

---

## 14. Listar Comentários

**Método:** GET  
**URL:** `/request/comment/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 85,
    "id_request": 42,
    "id_user": {
      "id": 3,
      "nome": "Carlos Gestor",
      "email": "carlos.gestor@prefeitura.go.gov.br",
      "cpf": "***.***.***.***"
    },
    "message": "Equipe já foi enviada ao local. Previsão de conclusão: 2 dias úteis.",
    "created_at": "2026-02-21T16:10:45.789012Z"
  },
  {
    "id": 84,
    "id_request": 41,
    "id_user": {
      "id": 3,
      "nome": "Carlos Gestor",
      "email": "carlos.gestor@prefeitura.go.gov.br",
      "cpf": "***.***.***.***"
    },
    "message": "Serviço concluído conforme solicitado.",
    "created_at": "2026-02-21T16:20:00.123456Z"
  }
]
```

**Status Code:** `200 OK`

---

## 15. Filtrar Comentários por Solicitação

**Método:** GET  
**URL:** `/request/comment/?id_request=42`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 85,
    "id_request": 42,
    "id_user": {
      "id": 3,
      "nome": "Carlos Gestor",
      "email": "carlos.gestor@prefeitura.go.gov.br",
      "cpf": "***.***.***.***"
    },
    "message": "Equipe já foi enviada ao local. Previsão de conclusão: 2 dias úteis.",
    "created_at": "2026-02-21T16:10:45.789012Z"
  },
  {
    "id": 80,
    "id_request": 42,
    "id_user": {
      "id": 1,
      "nome": "João da Silva",
      "email": "joao.silva@exemplo.com",
      "cpf": "987.654.321-00"
    },
    "message": "Obrigado pelo retorno!",
    "created_at": "2026-02-21T16:25:30.456789Z"
  }
]
```

**Status Code:** `200 OK`

---

## 16. Filtros de Busca - Por Status

**Método:** GET  
**URL:** `/request/reqs/?current_status=4`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 41,
    "id_user": {
      "id": 5,
      "nome": "Maria Santos",
      "email": "maria.santos@exemplo.com",
      "cpf": "***.***.***.***"
    },
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "comment": "Buraco grande na Rua Principal.",
    "lat": "-15.3145",
    "lon": "-49.5980",
    "created": "2026-02-20T10:15:30.987654Z",
    "completed": "2026-02-21T16:20:00.123456Z",
    "is_canceled": false
  }
]
```

**Status Code:** `200 OK`

---

## 17. Filtros de Busca - Por Tipo

**Método:** GET  
**URL:** `/request/reqs/?request_type=1`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 41,
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "comment": "Buraco grande na Rua Principal.",
    "created": "2026-02-20T10:15:30.987654Z"
  },
  {
    "id": 35,
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação"
    },
    "current_status": {
      "id": 2,
      "desc": "Em andamento"
    },
    "comment": "Buraco na Avenida Principal causando transtornos.",
    "created": "2026-02-19T08:45:20.123456Z"
  }
]
```

**Status Code:** `200 OK`

---

## 18. Filtros de Busca - Por Período

**Método:** GET  
**URL:** `/request/reqs/?start_date=2026-01-01&end_date=2026-01-31`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 30,
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "comment": "Buraco na Rua A altura do número 500.",
    "created": "2026-01-15T14:20:10.456789Z",
    "completed": "2026-01-20T16:30:00.789012Z"
  },
  {
    "id": 28,
    "request_type": {
      "id": 5,
      "desc": "Lixo acumulado",
      "title": "Coleta de lixo"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "comment": "Acúmulo de lixo na Praça Central.",
    "created": "2026-01-10T09:15:30.123456Z",
    "completed": "2026-01-12T11:45:20.456789Z"
  }
]
```

**Status Code:** `200 OK`

---

## 19. Filtros de Busca - Combinados

**Método:** GET  
**URL:** `/request/reqs/?request_type=1&current_status=4&start_date=2026-01-01&end_date=2026-01-31`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Descrição:** Busca por "Buraco na via" + "Concluída" + Janeiro/2026

**Response:**
```json
[
  {
    "id": 30,
    "request_type": {
      "id": 1,
      "desc": "Buraco na via",
      "title": "Pavimentação"
    },
    "current_status": {
      "id": 4,
      "desc": "Concluída"
    },
    "comment": "Buraco na Rua A altura do número 500.",
    "created": "2026-01-15T14:20:10.456789Z",
    "completed": "2026-01-20T16:30:00.789012Z",
    "is_canceled": false
  }
]
```

**Status Code:** `200 OK`

---

## 20. Filtrar Canceladas/Ativas

**Método:** GET  
**URL:** `/request/reqs/?is_canceled=true`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 38,
    "current_status": {
      "id": 5,
      "desc": "Cancelada"
    },
    "comment": "Acúmulo de lixo na calçada, solicitação duplicada.",
    "created": "2026-02-18T09:20:15.456789Z",
    "is_canceled": true
  }
]
```

**Status Code:** `200 OK`

---

**Para solicitações ativas:**

**URL:** `/request/reqs/?is_canceled=false`

---

## 21. Exportar Relatório XLS

**Método:** GET  
**URL:** `/request/export/xls/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```
Binary file download (application/vnd.ms-excel)
Filename: exportacao.xls
```

**Status Code:** `200 OK`

**Estrutura do arquivo XLS:**

| id | Latitude | Longitude | Descrição do problema | Nome do usuário | CPF | Tipo da solicitação | Status | Data e hora |
|----|----------|-----------|----------------------|-----------------|-----|---------------------|--------|-------------|
| 42 | -15.3150 | -49.5975 | Poste de iluminação... | João da Silva | 987.654.321-00 | Poste queimado | Em andamento | 21/02/2026 15:45:10 |
| 41 | -15.3145 | -49.5980 | Buraco grande na... | Maria Santos | 123.456.789-00 | Pavimentação | Concluída | 21/02/2026 16:20:00 |

**Observações:**
- Query SQL customizada com JOIN de 4 tabelas
- Data formatada em DD/MM/YYYY HH:MM:SS
- Inclui todos os campos principais para análise
- CPF completo (não anonymizado no export)

---

## 22. Listar Tipos de Solicitação

**Método:** GET  
**URL:** `/request/types/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
[
  {
    "id": 1,
    "icon": "/media/assets/icon_buraco.png",
    "banner": "/media/assets/banner_buraco.png",
    "desc": "Buraco na via",
    "title": "Pavimentação"
  },
  {
    "id": 2,
    "icon": "/media/assets/icon_arvore.png",
    "banner": "/media/assets/banner_arvore.png",
    "desc": "Árvore caída ou galhos perigosos",
    "title": "Poda de árvore"
  },
  {
    "id": 3,
    "icon": "/media/assets/icon_iluminacao.png",
    "banner": "/media/assets/banner_iluminacao.png",
    "desc": "Iluminação pública",
    "title": "Poste queimado"
  },
  {
    "id": 4,
    "icon": "/media/assets/icon_calcada.png",
    "banner": "/media/assets/banner_calcada.png",
    "desc": "Calçada quebrada ou irregular",
    "title": "Calçada"
  },
  {
    "id": 5,
    "icon": "/media/assets/icon_lixo.png",
    "banner": "/media/assets/banner_lixo.png",
    "desc": "Lixo acumulado",
    "title": "Coleta de lixo"
  }
]
```

**Status Code:** `200 OK`

**Observações:**
- Lista todos os tipos disponíveis
- Inclui URLs de ícone e banner para interface mobile

---

## 23. Criar Tipo de Solicitação

**Método:** POST  
**URL:** `/request/create/type/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: multipart/form-data
```

**Body (multipart):**
```
icon: [arquivo de imagem]
banner: [arquivo de imagem]
desc: "Esgoto entupido ou vazamento"
title: "Problemas de saneamento"
```

**Response:**
```json
{
  "id": 6,
  "icon": "/media/assets/icon_saneamento.png",
  "banner": "/media/assets/banner_saneamento.png",
  "desc": "Esgoto entupido ou vazamento",
  "title": "Problemas de saneamento"
}
```

**Status Code:** `201 CREATED`

**Observações:**
- Apenas gestor pode criar
- Upload de 2 imagens (ícone e banner)
- Campos obrigatórios: icon, banner, desc, title
- Requer autenticação

---

## 24. Excluir Tipo de Solicitação

**Método:** DELETE  
**URL:** `/request/<pk>/delete/type/`  
**Exemplo:** `/request/6/delete/type/`

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```
No content
```

**Status Code:** `204 NO CONTENT`

**Observações:**
- Apenas gestor pode excluir
- Cuidado: pode quebrar referências de solicitações existentes

---

## 25. Listar Códigos de Status

**Método:** GET  
**URL:** `/request/status/code`

**Response:**
```json
[
  {
    "id": 1,
    "desc": "Em análise"
  },
  {
    "id": 2,
    "desc": "Em andamento"
  },
  {
    "id": 3,
    "desc": "Aguardando material"
  },
  {
    "id": 4,
    "desc": "Concluída"
  }
]
```

**Status Code:** `200 OK`

**Observações:**
- Não retorna status `5` (Cancelada) - exclusão via query SQL
- Usado para popular dropdowns de seleção de status

---

## Resumo de Status Codes da API

| Status Code | Significado |
|-------------|-------------|
| 200 OK | Sucesso na requisição |
| 201 CREATED | Recurso criado com sucesso |
| 204 NO CONTENT | Exclusão bem-sucedida |
| 400 BAD REQUEST | Erro de validação ou regra de negócio |
| 401 UNAUTHORIZED | Não autenticado ou credenciais inválidas |
| 403 FORBIDDEN | Sem permissão para acessar o recurso |
| 404 NOT FOUND | Recurso não encontrado |

---

## Códigos de Status das Solicitações

| ID | Descrição |
|----|-----------|
| 1 | Em análise |
| 2 | Em andamento |
| 3 | Aguardando material |
| 4 | Concluída |
| 5 | Cancelada |

**Regras:**
- Status inicial: sempre `1` (Em análise)
- Cancelamento: apenas de status `1` para `5`
- Gestor não pode alterar diretamente para `5`
- Mudança de status cria registro no histórico
