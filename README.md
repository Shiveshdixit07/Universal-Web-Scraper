# Universal Web Scraper

## Overview
The **Universal Web Scraper** is an intelligent and adaptable web scraping tool designed to extract content from user-provided URLs. Powered by AI models like **gemini-1.5-flash**, the scraper processes data based on user-defined fields, offering high flexibility and precision. The tool supports downloading scraped content in various formats, including **CSV**, **JSON**, and **Excel**, ensuring seamless integration into diverse workflows. Future updates aim to incorporate additional AI models to enhance functionality and user experience.

---

## Features

### Key Capabilities
- **AI-Powered Web Scraping**: Utilizes the **gemini-1.5-flash** model for efficient and context-aware content extraction.
- **User-Defined Fields**: Enables users to specify custom fields to scrape relevant content.
- **Flexible Download Formats**: Supports exporting scraped data in **CSV**, **JSON**, and **Excel** formats.
- **Intuitive UI**: Provides a user-friendly interface built with **Streamlit**.

### Future Enhancements
- Integration with additional AI models for advanced scraping.
- Enhanced processing capabilities for complex data structures.
- Broader support for multi-page scraping and nested data extraction.

---

## Installation

### Prerequisites
- **Python 3.8+**
- Package Manager: **pip**
- Browser Driver: Compatible with your browser (e.g., ChromeDriver for Google Chrome)

### Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Shiveshdixit07/Universal-Web-Scraper.git
   cd Universal-Web-Scraper
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Browser Driver**:
   - Download the browser driver matching your browser version.
   - Place it in your system's PATH or the project folder.

4. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Enter URL**:
   Provide the URL of the webpage you want to scrape in the sidebar.

2. **Specify Fields**:
   Define the fields to extract using the tag-based input system.

3. **Scrape Content**:
   Click the "Scrape" button to process the webpage. The scraped data will be displayed on the main interface.

4. **Download Data**:
   Select your preferred format (**CSV**, **JSON**, or **Excel**) to download the scraped content.

---

## Project Structure

```
.
├── app.py             # Main application script
├── scrapper.py        # Web scraping logic using Selenium and BeautifulSoup
├── asset.py           # Configurations for headless mode and user agents
├── requirements.txt   # Python dependencies
├── output/            # Folder to store downloaded files
└── README.md          # Project documentation
```

---

## Technologies Used

- **Frontend**: Streamlit for the interactive UI
- **Backend**: Python, Selenium, BeautifulSoup
- **AI Model**: gemini-1.5-flash (future-ready for additional models)
- **Data Formats**: CSV, JSON, Excel

---

## Contribution

We welcome contributions to improve this project! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a Pull Request on GitHub.

---

## Contact

For queries or support, please reach out to [shiveshdixit8400@gmail.com](mailto:shiveshdixit8400@gmail.com).

---

## Acknowledgments

- **Streamlit**: For the excellent web app framework.
- **Selenium & BeautifulSoup**: For seamless web scraping capabilities.
- **gemini-1.5-flash**: For AI-powered content processing.

---

Thank you for using the Universal Web Scraper! 🚀
