# from flask import Flask, render_template, jsonify, request
# from flask_pymongo import PyMongo
# import openai

# openai.api_key = "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"




# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb+srv://akhilabhishek1711:Bit%401508521@mongoyoutube.7serw.mongodb.net/"
# mongo = PyMongo(app)

# @app.route("/")
# def home():
#     chats = mongo.db.chats.find({})
#     myChats = [chat for chat in chats]
#     print(myChats)
#     return render_template("index.html", myChats = myChats)

# @app.route("/api", methods=["GET", "POST"])
# def qa():
#     if request.method == "POST":
#         print(request.json)
#         question = request.json.get("question")
#         chat = mongo.db.chats.find_one({"question": question})
#         print(chat)
#         if chat:
#             data = {"question": question, "answer": f"{chat['answer']}"}
#             return jsonify(data)
#         else:
#             response = client.chat.completions.create(
#                   model="gpt-3.5-turbo-0125",
#                   messages=[question],
#                   temperature=1,
#                   max_tokens=2048,
#                   top_p=1,
#                   frequency_penalty=0,
#                   presence_penalty=0,
#                   response_format={
#     "type": "text"
#   }
# )
#             print(response)
#             data = {"question": question, "answer": response["choices"][0]["text"]}
#             mongo.db.chats.insert_one({"question": question, "answer": response["choices"][0]["text"]})
#             return jsonify(data)
#     data = {"result": "Thank you! I'm just a machine learning model designed to respond to questions and generate text based on my training data. Is there anything specific you'd like to ask or discuss? "}
        
#     return jsonify(data)

# app.run(debug=True, port=5001)

from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai

# Set OpenAI API key
openai.api_key = "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"

app = Flask(__name__)

# Set up MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://chatgpt:95y32*.h8rzAa4C@chatgpt.o3ika.mongodb.net/chatgpt"
mongo = PyMongo(app)

@app.route("/")
def home():
    try:
        # Fetch all chats from the MongoDB collection
        chats = mongo.db.chats.find({})
        myChats = [chat for chat in chats]
        print(myChats)
        return render_template("index.html", myChats=myChats)
    except Exception as e:
        print(f"Error fetching chats: {e}")
        return jsonify({"error": "Failed to fetch chats from database"}), 500

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        try:
            print(request.json)
            question = request.json.get("question")

            # Check if the question exists in the MongoDB database
            chat = mongo.db.chats.find_one({"question": question})
            print(chat)

            if chat:
                # If question is found in the database, return the stored answer
                data = {"question": question, "answer": f"{chat['answer']}"}
                return jsonify(data)
            else:
                # If question is not found, generate a response using OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": question}],
                    temperature=1,
                    max_tokens=2048,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                answer = response["choices"][0]["message"]["content"]
                print(answer)

                # Save the question and answer to the MongoDB collection
                mongo.db.chats.insert_one({"question": question, "answer": answer})

                # Return the generated answer
                data = {"question": question, "answer": answer}
                return jsonify(data)

        except Exception as e:
            print(f"Error handling request: {e}")
            return jsonify({"error": "An error occurred while processing the request"}), 500

    # Default response if no POST request is made
    data = {"result": "Thank you! I'm here to respond to your questions. Ask me anything!"}
    return jsonify(data)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5001)
