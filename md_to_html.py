import markdown

def convert(md,html):
    with open(md,'r') as f:
        text=f.read()
    html = markdown.markdown(text)

    with open(html, 'w') as f:
        f.write(html)

convert("README.md","readme.html")