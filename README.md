# KR ECM API

A FastAPI-based REST API for E-Commerce/Enterprise Content Management with multi-language support and advanced product management capabilities.

## Features

### Core Functionality
- 🔐 JWT Authentication & Authorization
- 🏪 Multi-merchant Support
- 🌐 Multi-language Content (translations)
- 📝 Product & Category Management
- 🍽️ Menu Management System
- 💰 Dual Currency Support (USD/KHR)

### Technical Features
- ✨ FastAPI Framework
- 🗃️ PostgreSQL Database
- 🔄 SQLAlchemy ORM
- ✅ Pydantic Data Validation
- 📚 OpenAPI Documentation
- 🔒 Secure Password Hashing
- 🧪 API Testing Support

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
\`\`\`bash
git clone git@github.com:ratanakkeo/kr-ecm-api.git
cd kr-ecm-api
\`\`\`

2. Create and activate virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Create \`.env\` file:
\`\`\`env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
API_V1_STR=/api/v1
PROJECT_NAME=KR ECM API
VERSION=1.0.0
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

## Running the Application

Development server:
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

The API will be available at \`http://localhost:8000\`

## API Documentation

After starting the server, access:
- Swagger UI: \`http://localhost:8000/docs\`
- ReDoc: \`http://localhost:8000/redoc\`

## API Endpoints

### Authentication
- POST \`/api/v1/auth/token\` - Get access token
- POST \`/api/v1/auth/users/\` - Create new user

### Menu Management
- GET \`/api/v1/menu/\` - List menu items
- POST \`/api/v1/menu/\` - Create menu item
- GET \`/api/v1/menu/{item_id}\` - Get menu item
- PUT \`/api/v1/menu/{item_id}\` - Update menu item
- DELETE \`/api/v1/menu/{item_id}\` - Delete menu item

### Categories
- GET \`/api/v1/categories/\` - List categories
- POST \`/api/v1/categories/\` - Create category
- GET \`/api/v1/categories/{category_id}\` - Get category
- PUT \`/api/v1/categories/{category_id}\` - Update category
- DELETE \`/api/v1/categories/{category_id}\` - Delete category

## Project Structure

\`\`\`plaintext
kr-ecm-api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       └── api.py
│   ├── core/
│   ├── db/
│   ├─�� models/
│   └── schemas/
├── tests/
└── requirements.txt
\`\`\`

## Contributing

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
