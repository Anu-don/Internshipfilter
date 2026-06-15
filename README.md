# Internship Filter & Search Automation

An automated tool to scrape, filter, and consolidate internship listings from multiple popular platforms into a single, organized report.

## 🚀 Features

- **Multi-Platform Scraping**: Supports major internship and job boards:
  - Internshala
  - LinkedIn
  - Unstop
  - Indeed India
  - Naukri Campus
  - Wellfound
- **Smart Filtering**: Refine results based on:
  - Keywords (e.g., Python, ML, React)
  - Domain (e.g., AI, Web Development)
  - Work Mode (Remote, Hybrid, Onsite)
  - Minimum Stipend (INR/month)
  - Location
- **Dual Operating Modes**:
  - **Default Mode**: Quick search across pre-selected popular platforms (Internshala, Unstop, Indeed).
  - **Custom Mode**: Pick exactly which platforms you want to search.
- **Comprehensive Output**:
  - **JSON**: Structured data for further processing or integration.
  - **DOCX**: A clean, readable Word document summarizing all matching internships.
- **Docker Ready**: Easily containerize and run the application in any environment.

## 🛠️ Tech Stack

- **Python**: Core logic and automation.
- **Playwright**: Robust web scraping and browser automation.
- **python-docx**: Automated generation of Word reports.
- **Docker**: Containerization for consistent deployment.

## 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Anu-don/Internshipfilter.git
   cd Internshipfilter
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**:
   ```bash
   playwright install chromium
   ```

## 🖥️ Usage

Run the main script to start the interactive search:

```bash
python app.py
```

### Command Line Arguments

You can also bypass initial prompts using arguments:

- `--mode`: Set the mode (0 for Default, 1 for Custom).
- `--output`: Specify a custom name for the output `.docx` file.

**Example:**
```bash
python app.py --mode 0 --output my_internships.docx
```

### Interactive Prompts

The script will guide you through:
1. Selecting a search mode.
2. Choosing platforms (in Custom mode).
3. Entering filters like keywords, location, and minimum stipend.

## 🐳 Docker Usage

To run the application using Docker:

1. **Build the Image**:
   ```bash
   docker build -t internship-filter .
   ```

2. **Run the Container**:
   ```bash
   docker run -it internship-filter
   ```

## 📁 Project Structure

- `app.py`: Main entry point for the application.
- `Scrapers/`: Platform-specific scraping logic.
- `filterengine.py`: Logic for applying user-defined filters.
- `docxgenerator.py`: Generates the final Word document report.
- `datamodels.py`: Data structures for internships and filters.
- `platform_registry.py`: Central registry for supported platforms.

## 📝 License

[MIT](LICENSE) (or your preferred license)
