import ast

def validate_code(code):
    try:
        ast.parse(code)
        return True
    except:
        return False

def safe_generate(model, tokenizer, prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    outputs = model.generate(
        inputs.input_ids,
        max_new_tokens=400,
        temperature=0.2,
        do_sample=True
    )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if "```python" in text:
        text = text.split("```python")[-1].split("```")[0]

    return text

def safe_fix(original_code, generated_code):
    if validate_code(generated_code):
        return generated_code
    return original_code
