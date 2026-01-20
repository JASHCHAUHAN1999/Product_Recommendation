from flask import Flask, request, jsonify
from config import openai_api_key
from Product import products
from openai import OpenAI


app = Flask(__name__)

ai = OpenAI(api_key=openai_api_key)


@app.route("/")
def home():
    return jsonify({"msg":"Welcome to Home Screen..."}), 200


@app.route("/recommend",methods = ["POST"])
def recommend():
    data = request.get_json()
    user_data = data.get("preference")

    product = product_text = "\n".join(
        [f"{p['name']} - {p['category']} - ${p['price']}" for p in products]
    )

    prompt = f"""
    User preference: {user_data}

    Available products:
    {product}
    """

    try:
        response = ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
    except:
        return jsonify({"msg":"Credit Finished..."})

    reply = response.choices[0].message.content
    recommended_names = [name.strip() for name in reply.split(",")]
    recommended_products = [
        p for p in products if p["name"] in recommended_names
    ]
    
    return jsonify(recommended_products), 201



if __name__ == "__main__":
    app.run(debug=True,port=5555)