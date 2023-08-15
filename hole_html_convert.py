def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def write_to_html_file(file_path, html_content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('''<script>
function toggle_expand(btn) {
    var content = btn.parentElement.querySelector('.hidden-content');
    if (content.style.display === 'none') {
        content.style.display = 'block';
        btn.innerHTML = 'Less';
    } else {
        content.style.display = 'none';
        btn.innerHTML = 'More';
    }
}
</script>
<style>
.expand-container {
    position: relative;
}

.expand-btn {
    cursor: pointer;
    background-color: #f1f1f1;
    border: none;
    padding: 5px 10px;
    font-size: 12px;
}

.hidden-content {
    padding: 10px;
}

.separator {
    border-top: 1px solid #ccc;
    margin: 10px 0;
}
 .before-colon {
    font-style: italic;
    font-weight: bold;
    color: red;
}
.after-colon {
    color: blue;
}
</style>''')
        file.write(html_content)

import argparse


def split_colon(line):
    if ':' in line:
        colon_index = line.index(':')
        before_colon = line[:colon_index]
        after_colon = line[colon_index + 1:]
        return f'<p><span class="before-colon">{before_colon}:</span><span class="after-colon">{after_colon}</span></p>'
    else:
        return f'<p><span class="after-colon">{line}</span></p>'

def convert_text_to_html(text):
    lines = text.split('\n')
    html_lines = ['<div>']
    first_line = ''

    for i, line in enumerate(lines):
        if i == 0:
            first_line = line
        elif i < 5:
            html_lines.append(split_colon(line))
        elif i == 5:
            html_lines += [
                '<div class="expand-container">',
                '<button class="expand-btn" onclick="toggle_expand(this)">More</button>',
                '<div class="hidden-content" style="display: none;">'
            ]
            html_lines.append(split_colon(line))
        else:
            html_lines.append(split_colon(line))
    
    if len(lines) >= 5:
        html_lines.append('</div></div>')

    html_lines.append(f'<p>{first_line}</p>')
    html_lines.append('</div>')
    return '\n'.join(html_lines)+'\n<div class="separator"></div>\n'


def main():
    parser = argparse.ArgumentParser(description='Convert a txt file to a styled HTML file.')
    parser.add_argument('input_file', type=str, help='Path to the input txt file.', default='export_230815.txt')
    parser.add_argument('output_file', type=str, help='Path to the output HTML file.', default='output.html')
    args = parser.parse_args()

    txt_content = read_txt_file(args.input_file)
    sections = txt_content.split('\n======================\n\n')
    html_sections = [convert_text_to_html(section) for section in sections]
    html_content = '\n'.join(html_sections)
    write_to_html_file(args.output_file, html_content)

if __name__ == '__main__':
    main()