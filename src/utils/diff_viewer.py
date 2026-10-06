import difflib

def generate_html_diff(old_text: str, new_text: str) -> str:
    """
    Compares two strings word-by-word and generates an HTML diff.
    Additions/Corrections are highlighted in green.
    Removals/Errors are highlighted in red with a strikethrough.
    """
    old_words = old_text.split()
    new_words = new_text.split()
    
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    
    html_output = []
    
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            html_output.append(" ".join(old_words[a0:a1]))
            
        elif opcode == 'insert':
            inserted = " ".join(new_words[b0:b1])
            html_output.append(f'<span style="background-color: #d4edda; color: #155724; padding: 2px 4px; border-radius: 4px; font-weight: bold;">{inserted}</span>')
            
        elif opcode == 'delete':
            deleted = " ".join(old_words[a0:a1])
            html_output.append(f'<span style="background-color: #f8d7da; color: #721c24; text-decoration: line-through; padding: 2px 4px; border-radius: 4px; opacity: 0.7;">{deleted}</span>')
            
        elif opcode == 'replace':
            deleted = " ".join(old_words[a0:a1])
            inserted = " ".join(new_words[b0:b1])
            html_output.append(f'<span style="background-color: #f8d7da; color: #721c24; text-decoration: line-through; padding: 2px 4px; border-radius: 4px; opacity: 0.7;">{deleted}</span>')
            html_output.append(f'<span style="background-color: #d4edda; color: #155724; padding: 2px 4px; border-radius: 4px; font-weight: bold;">{inserted}</span>')
            
    # Wrap in a nice container with good line height for readability
    return f"""
    <div style="line-height: 2.0; font-family: sans-serif; font-size: 16px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; background-color: #fefefe; color: #333;">
        {" ".join(html_output)}
    </div>
    """
