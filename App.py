from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from Product import products

app = Flask(__name__)
CORS(app)


client = OpenAI(api_key="MY_Api_key")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    preference = data.get("preference")

    product_text = "\n".join(
        [f"{p['name']} - {p['category']} - ${p['price']}" for p in products]
    )

    prompt = f"""
User preference: {preference}

Available products:
{product_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_reply = response.choices[0].message.content
    recommended_names = [name.strip() for name in ai_reply.split(",")]

    recommended_products = [
        p for p in products if p["name"] in recommended_names
    ]

    return jsonify(recommended_products)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
