import pdfplumber
import os
import pandas as pd

def extract_pdf_content(pdf_path, img_out_dir="extracted_images"):
    os.makedirs(img_out_dir, exist_ok=True)

    data = {
        "page": [],
        "text": [],
        "links": [],
        "tables": [],
        "images": []
    }

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            print(f"Processing Page {i}...")

            text = page.extract_text() or ""
            data["page"].append(i)
            data["text"].append(text)

            links = []
            try:
                for ann in page.annots or []:
                    uri = ann.get('uri')
                    if uri:
                        links.append(uri)
            except:
                pass
            data["links"].append(links)

            try:
                tables = page.extract_tables()
                tables_df = [pd.DataFrame(table[1:], columns=table[0]) for table in tables if table]
            except:
                tables_df = []
            data["tables"].append(tables_df)

            img_paths = []
            try:
                for img in page.images:
                    bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
                    cropped = page.crop(bbox).to_image(resolution=300)
                    img_path = os.path.join(img_out_dir, f"page{i}_{len(img_paths)}.png")
                    cropped.save(img_path, format="PNG")
                    img_paths.append(img_path)
            except:
                pass
            data["images"].append(img_paths)

    return data

def generate_html(content, output_file="output.html"):
    html = """
    <html>
    <head>
        <title>Extracted PDF Content</title>
        <style>
            body { font-family: Arial; padding: 20px; background: #f9f9f9; }
            h2 { border-bottom: 2px solid #ccc; margin-top: 40px; }
            .page-block { padding: 15px; background: #fff; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
            table { border-collapse: collapse; width: 100%; margin-top: 10px; }
            table, th, td { border: 1px solid #aaa; padding: 5px; }
            img { max-width: 300px; margin: 10px 5px; }
        </style>
    </head>
    <body>
        <h1>Extracted PDF Content</h1>
    """

    for i in range(len(content["page"])):
        html += f'<div class="page-block">'
        html += f"<h2>Page {content['page'][i]}</h2>"

        html += f"<h3>Text</h3><p>{content['text'][i].replace(chr(10), '<br>') if content['text'][i] else '[No text found]'}</p>"

        html += f"<h3>Links</h3>"
        if content["links"][i]:
            for link in content["links"][i]:
                html += f'<a href="{link}" target="_blank">{link}</a><br>'
        else:
            html += "<p>[No links found]</p>"

        html += f"<h3>Tables</h3>"
        if content["tables"][i]:
            for df in content["tables"][i]:
                html += df.to_html(index=False, border=1)
        else:
            html += "<p>[No tables found]</p>"

        html += f"<h3>Images</h3>"
        if content["images"][i]:
            for img_path in content["images"][i]:
                rel_path = os.path.relpath(img_path, os.path.dirname(output_file))
                html += f'<img src="{rel_path}" alt="Image from Page {i+1}">'
        else:
            html += "<p>[No images found]</p>"

        html += '</div>'

    html += "</body></html>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ HTML output saved to: {output_file}")


def main():
    pdf_file = "sc1.pdf"
    img_dir = "extracted_images"
    output_html = "output.html"

    if not os.path.exists(pdf_file):
        print(f"❌ PDF file '{pdf_file}' not found.")
        return

    content = extract_pdf_content(pdf_file, img_dir)
    generate_html(content, output_html)

if __name__ == "__main__":
    main()
