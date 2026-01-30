from groq import Groq
import os

def suggest_alternatives(query: str) -> str:
    """
    Suggests an alternative search query using Groq's LLM if the original
    query may have typos or uncommon words.
    """
    prompt = f"""You are an e-commerce assistant.
    Suggest a corrected or alternative version of this search query that is more likely to find relevant products.
    Keep the meaning but fix spelling, abbreviations, or missing words.
    Return ONLY the corrected query, nothing else.
    Input: "{query}"
    Output:"""
    
    # Configurar API key
    api_key = os.environ.get('GROQ_API_KEY')
    
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modelo rápido e gratuito com alta cota
            messages=[
                {"role": "system", "content": "You are a helpful e-commerce assistant that suggests better search queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # Em caso de erro, retornar a query original
        print(f"⚠️  Erro ao sugerir alternativa: {e}")
        return query