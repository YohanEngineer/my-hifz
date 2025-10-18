# README.md: Quran Memorization Planner (My Hifz Planner)

### 📖 Project Overview

The **My Hifz Planner** is a web application designed to help users create a structured and manageable schedule for memorizing the Holy Quran. 
By simply inputting the desired number of pages to memorize per period (day or week), the application generates a complete, downloadable schedule in PDF format.

This tool simplifies the planning phase of Hifz (memorization) by clearly outlining the specific page ranges and Surahs to be covered in each study session.

### ✨ Features

  * **Customizable Rate:** Users define their own pace (e.g., 2 pages/day or 10 pages/week).
  * **Time Period Flexibility:** Choose between **Daily** or **Weekly** planning.
  * **Page and Surah Mapping:** Automatically maps page numbers to corresponding Surah names and page ranges.
  * **Downloadable PDF:** Generates a professional, easy-to-read PDF schedule suitable for printing.
  * **Clear Planning Output:** Displays the complete plan in a structured table on the web interface.

### 🛠️ Technology Stack

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Frontend** | **HTML5, CSS3, Vanilla JavaScript** | Lightweight, fast, and accessible user interface. |
| **PDF Generation** | **jsPDF** (client-side) | Handles the dynamic creation and download of the planning document in the browser. |
| **Backend** | **Python 3.x with FastAPI** | High-performance, asynchronous framework for serving the core Quranic page data and handling potential future logic (e.g., user authentication, larger data processing). |
| **Data** | **JSON/Database** | Stores the definitive mapping of Quran page numbers, Surahs, and Juz. |

### 🚀 Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites

  * Python 3.8+
  * `pip` (Python package installer)
  * A web browser

#### Backend Setup (FastAPI)

1.  **Clone the repository:**

    ```bash
    git clone [YOUR_REPO_URL]
    cd myhifz
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    # (Typical dependencies would include fastapi and uvicorn)
    ```

3.  **Run the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

    The API will now be running, typically at `http://127.0.0.1:8000`.

#### Frontend Setup (HTML/JS)

1.  Navigate to the `frontend/` directory.
2.  Open the `index.html` file directly in your web browser.
3.  Ensure the JavaScript code can correctly communicate with the running FastAPI backend (e.g., fetching the page data from an endpoint like `/api/quran/pages`).

### ⚙️ Backend Architecture (FastAPI & Python)

The FastAPI application primarily serves two roles:

1.  **Data API:** Exposes the full Quranic page data as a JSON endpoint for the frontend to consume.
2.  **Core Logic:** Hosts the heavy-lifting scheduling logic.
3.  **Factory pattern:** Abstracting the creation of objects, such as database connections, external service clients, or specific planning strategies

### 🤝 Contribution

Contributions, issues, and feature requests are welcome\! Feel free to check the [issues page].