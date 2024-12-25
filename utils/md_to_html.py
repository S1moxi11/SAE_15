import markdown

def convert(md, html_file):
    with open(md, 'r') as f:
        text = f.read()
    html = markdown.markdown(text)

    full_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>SAÉ 15 Pokémons</title>
        <link rel="stylesheet" href="{html_file[:-5]}.css">
    </head>
    <body>
        {html}
    </body>
    </html>
    """
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
