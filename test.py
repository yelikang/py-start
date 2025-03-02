from langchain.llms import OpenAI

def generate_store_names(_features):
    prompt_template = "我正在开一家商店，它的主要特点是{}。请帮我想出10个商店的名字"
    prompt = prompt_template.format(_features)

    llm = OpenAI()
    response = llm.generate(prompt, max_tokens=50, temperature=0.8)

    store_names = [gen[0].text.strip() for gen in response.generations]
    return store_names
store_features = "时尚、创意、独特"

store_names = generate_store_names(store_features)
print(store_names)