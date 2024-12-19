import markdown

def convert(md,html_file):
    with open(md,'r') as f:
        text=f.read()
    html = markdown.markdown(text)

    with open(html_file, 'w') as f:
        f.write(html)
