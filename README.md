# BeFR-Deepfake-Detection
This is our TTU Capstone project. Our team is BeFR and we developed a deepfake detection app that is focused on analyzing images of people. The app is deployed at: https://huggingface.co/spaces/enovak/BeFR-Deepfake-Detection

The backbone of our web application is our CNN model which was trained in Google Colab. It utilizes EfficientNet-b0 as a base with added data augmentation and dropout layers for training complexity. Our model is trained on the DeepDetect-2025 Kaggle dataset, which consists of over 100,000 real and fake images of human faces.

The application itself was developed in Python, HTML, and JavaScript and uses Flask API for front to backend integration and deployment. We also utilize MongoDB for database management to keep track of user reports and model predictions.

Our team's website, including information about all members and our development schedule, is deployed directly via GitHub Pages and can be accessed here: https://ennovak.github.io/BeFR-Deepfake-Detection/
