from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Alexander, a powerful AI assistant with a knight-like personality."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return "Error connecting to AI"