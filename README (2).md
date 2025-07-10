# AI/ML-Based Real-Time Sign Language Converter — PDF Extractor

This project extracts and visualizes structured content (text, images, tables, and links) from academic or technical PDF documents using Python and [pdfplumber](https://github.com/jsvine/pdfplumber). It was applied to the research paper:  
**"AI/ML-Based Real-Time Sign Language Converter: Enabling Seamless Communication via Audio Calls for Deaf and Mute Individuals"**

## 🔍 Features

- 📄 Extracts:
  - Full text from each page
  - Tables and links (if any)
  - Embedded images (cropped and saved)
- 🌐 Outputs:
  - A clean, styled `HTML` page with all the extracted content
- 📂 Automatically creates an `extracted_images/` directory for storing images

## 🧠 Technologies Used

- Python 3.x
- pdfplumber
- pandas
- OpenCV (optional for further gesture detection)
- HTML/CSS (for result presentation)

## 📁 Project Structure
sign-language-pdf-extractor/
│
├── sc1.pdf                    
├── python_GD.py              
├── output.html               
├── README.md                 
├── requirements.txt          
└── extracted_images/ 
          
    ├── page2_0.png
    ├── page7_0.png
    └── page7_1.png


## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/sign-language-pdf-extractor.git
cd sign-language-pdf-extractor


``bash
pip install pdfplumber pandas

``bash
python python_GD.py

