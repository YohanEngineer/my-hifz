# README.md: Quran Memorization Planner (My Hifz Planner)

### 📖 Project Overview

The **My Hifz Planner** is a web application designed to help users create a structured and manageable schedule for memorizing the Holy Quran.
By simply inputting the desired number of pages to memorize per period (day or week), the application generates a complete, downloadable schedule in PDF format.

This tool simplifies the planning phase of Hifz (memorization) by clearly outlining the specific page ranges and Surahs to be covered in each study session.

### ✨ Features

  * **Customizable Rate:** Users define their own pace (e.g., 2 pages/day or 10 pages/week).
  * **Time Period Flexibility:** Choose between **Daily** or **Weekly** planning.
  * **Flexible Starting Point:** Start from any page (1-604) in the Quran.
  * **Bidirectional Order:** Memorize in Ascending (1→604) or Descending (604→1) order.
  * **Page and Surah Mapping:** Automatically maps page numbers to corresponding Surah names (Arabic) and Juz numbers.
  * **Professional PDF:** Server-side PDF generation with proper Arabic font rendering and French interface.
  * **Accessible UI:** WCAG 2.1 AA compliant frontend with full keyboard navigation and screen reader support.
  * **Responsive Design:** Works seamlessly on desktop, tablet, and mobile devices.

### 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | **Bootstrap 5.3.2, HTML5, CSS3, Vanilla JS** | Modern, accessible, responsive interface with green/white theme. |
| **PDF Generation** | **ReportLab** (server-side) | Professional PDF generation with Arabic font support using Amiri font. |
| **Backend** | **Python 3.10+ with FastAPI** | High-performance, asynchronous API framework with Pydantic validation. |
| **Data** | **JSON** | Stores complete Quran data (604 pages) from Quran Hub API. |
| **Package Manager** | **UV** | Modern Python package manager for dependency management. |

### 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites

  * Python 3.10+
  * UV (Python package manager) - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  * A modern web browser

#### Backend Setup (FastAPI)

1.  **Clone the repository:**

    ```bash
    git clone [YOUR_REPO_URL]
    cd myhifz
    ```

2.  **Create virtual environment and install dependencies:**

    ```bash
    uv venv --python 3.10
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    uv pip install -e .
    ```

3.  **Run the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

    The API will now be running at `http://localhost:8000`.
    API documentation available at `http://localhost:8000/docs`.

#### Frontend Setup

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Start a local web server:**

    ```bash
    python3 -m http.server 8080
    ```

3.  **Open in browser:**

    Navigate to `http://localhost:8080` in your web browser.

#### Quick Start (Both Backend and Frontend)

```bash
# Terminal 1 - Backend
source .venv/bin/activate
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
python3 -m http.server 8080
```

Then open `http://localhost:8080` in your browser!

### ⚙️ Backend Architecture (FastAPI & Python)

The backend follows a clean, layered architecture:

```
app/
├── models.py              # Pydantic models for data validation
├── config.py              # Configuration and logging setup
├── services/
│   ├── quran_service.py   # Quran data management
│   ├── planning_service.py # Schedule generation logic
│   └── pdf_service.py     # PDF generation with Arabic support
└── routers/
    ├── quran.py           # Quran data API endpoints
    └── planning.py        # Planning/PDF generation endpoints
```

**Key Roles:**

1.  **Data API:** Exposes Quranic page data via `/api/v1/quran/*` endpoints.
2.  **Scheduling Logic:** Generates customized memorization schedules with flexible ordering.
3.  **PDF Generation:** Creates professional PDFs with Arabic text rendering using ReportLab.
4.  **Service Layer Pattern:** Separates business logic from API routes for maintainability.

### 📚 API Endpoints

#### Quran Data
- `GET /api/v1/quran/pages` - Get all 604 pages
- `GET /api/v1/quran/pages/{page_number}` - Get specific page
- `GET /api/v1/quran/pages/surah/{surah_number}` - Get pages by Surah
- `GET /api/v1/quran/pages/juz/{juz_number}` - Get pages by Juz

#### Planning
- `POST /api/v1/plan/generate` - Generate and download PDF schedule

Full API documentation: `http://localhost:8000/docs`

### 🎨 Frontend Features

- **Theme:** Green (#2d8659) and white color scheme
- **Framework:** Bootstrap 5.3.2 with custom CSS
- **Accessibility:** WCAG 2.1 AA compliant
  - Keyboard navigation
  - Screen reader support
  - ARIA labels and live regions
  - High contrast mode support
  - Reduced motion support
- **Responsive:** Mobile-first design (320px - 2560px+)
- **Form Validation:** Real-time client-side validation
- **Error Handling:** User-friendly error messages

See `frontend/README.md` for detailed frontend documentation.

### 🧪 Testing

Run the test suite:

```bash
source .venv/bin/activate
pytest

# With coverage report
pytest --cov=app --cov-report=term-missing
```

Current test coverage: **87%**

### 🤝 Contribution

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page].

### 📝 License

This project is open source and available under the [MIT License].