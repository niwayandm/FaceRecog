# Flask DeepFace API

This project provides a simple Flask-based API for facial recognition using DeepFace. The API includes endpoints for registering a person's image and recognizing a person from an image.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [POST /register_person](#post-register_person)
  - [POST /recognize_person](#post-recognize_person)

## Installation

1. **Clone the repository:**
  ```bash
  git clone https://github.com/niwayandm/FaceRecog .git
  cd FaceRecog
  ```
2. **Create and activate a virtual environment:**
  ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
  ```
3. **Install the required dependencies:**
  ```bash
   pip install -r requirements.txt
  ```
4. Modify settings.py file with your desired configuration settings (host, port, debug mode, title, etc.).

## Usage
Run the Flask app:
 ```bash
  python app.py
  ```
The server will start and be accessible according to the host and port specified in your `settings.py`.

## API Endpoints

### GET /
**Description:**
Returns a welcome message.

**Response:**
- `200 OK` with a welcome message.

### POST /register_person
**Description:**
Registers a person's image by generating a DeepFace representation.

**Request Body:**
- `image`: Base64 encoded image string.
- `name`: Name of the person.

**Response:**
- `200 OK` with a success or error message.

**Example:**
 ```json
  {
    "image": "base64_encoded_image_string",
    "name": "John Doe"
  }
  ```
**Response Example:**
 ```json
  {
    "result": "success",
    "message": "Updated embeddings saved"
  }
  ```

### POST /recognize_person
**Description:**
Recognizes a person from an image using DeepFace.

**Request Body:**
- `image`: Base64 encoded image string.

**Response:**
- `200 OK` with a success or error message.

**Example:**
 ```json
  {
    "image": "base64_encoded_image_string",
    "name": "John Doe"
  }
  ```
**Response Example:**
 ```json
  {
    "identity": "./Images/DB/John_Doe.jpg",
    "source_x": 0,
    "source_y": 0,
    "source_w": 100,
    "source_h": 100,
    "name": "John Doe"
  }
  ```