from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
import os
import pickle

from settings import config

app = Flask(__name__)

def save_base64_to_file(base64_string, output_file_path="./Images/Test/test.jpg"):
    """Function to convert base64 to an image

    Args:
        base64_string (_type_): base64 encoded image
        output_file_path (str, optional): path of the saved image. Defaults to "./Images/Test/test.jpg".

    Returns:
       string: output_file_path
    """
    with open(output_file_path, "wb") as file:
        file.write(base64.b64decode(base64_string))
    return output_file_path


@app.route('/')
def index():
    return f"Welcome to {config.title}"

@app.route('/register_person', methods=['POST'])
def register_person():
    """API Function to generate a DeepFace representation of a person.

    Returns:
        json: log message for errors if there's any
    """
    model_name="Facenet512"
    folder = "./Images/DB/"
    try:
        image_data = request.json['image']
        person_name = request.json['name']
        image_path = save_base64_to_file(image_data, os.path.join(folder, f"{person_name}.jpg"))

        # ... processing logic ...
        embeddings = {}
        embeddings_file = os.path.join(folder, "representations_facenet512.pkl")

        if os.path.exists(embeddings_file):
            with open(embeddings_file, 'rb') as file:
                embeddings = pickle.load(file)

            if os.path.exists(image_path):
                # if the person exists, return error
                if any(image_path in embedding for embedding in embeddings):
                    return jsonify({'result': 'error','message': f'{person_name} already exists.'})
                else:
                    # Compute the embedding for the new person's image
                    new_embedding = DeepFace.represent(img_path=image_path, model_name=model_name)
                    new_embedding_data = [image_path,new_embedding[0]['embedding'], new_embedding[0]['facial_area']['x'], new_embedding[0]['facial_area']['y'],new_embedding[0]['facial_area']['w'],new_embedding[0]['facial_area']['h']]
                    embeddings.append(new_embedding_data)
                
                    # Reserialize the updated embeddings to the .pkl file
                    with open(os.path.join(folder, 'representations_facenet512.pkl'), 'wb') as file:
                        pickle.dump(embeddings, file)

        return jsonify({'result': 'success','message': 'Updated embeddings saved'})
    except Exception as e:
        return jsonify({'result': 'error','message': str(e)})

@app.route('/recognize_person', methods=['POST'])
def recognize_person():
    """API Function to recognise a person's image through DeepFace.

    Returns:
        json: DeepFace result and Name of the person.
    """
    model_name="Facenet512"
    folder = "./Images/DB/"
    try:
        image_data = request.json['image']

        image_path = save_base64_to_file(image_data)

        # ... processing logic ...
        df = DeepFace.find(img_path=image_path, db_path=folder, model_name=model_name, distance_metric='cosine')

        if df[0].empty:
            return jsonify({'error': 'could not recognise the person'})
        else:
            result= df[0].to_dict(orient='records')[0]
            result['name'] = os.path.splitext(os.path.basename(str(df[0]['identity'])))[0]

        # Delete the temporary image file
        os.remove(image_path)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host=config.host, port=config.port, debug=config.debug)
