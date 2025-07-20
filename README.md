# 🧠 Sports Celebrity Face Recognition Project

This is a **Data Science and Machine Learning** project aimed at building a facial recognition model that classifies images of famous sports personalities. The project walks through the complete machine learning pipeline — from data collection and preprocessing to model building and web integration.

---

## 🎯 Objective

The primary goal of this project is to classify a given image of a sports celebrity into one of the following five classes:

- **Maria Sharapova**
- **Serena Williams**
- **Virat Kohli**
- **Roger Federer**
- **Lionel Messi**

---


---

## 🛠️ Technologies & Libraries Used

### 🐍 Python Libraries:
- **NumPy**: Numerical operations and matrix handling
- **OpenCV**: Image processing and manipulation
- **Matplotlib & Seaborn**: Data visualization
- **scikit-learn**: Model building and evaluation
- **Pickle**: Saving and loading trained models

### 📊 Tools:
- **Jupyter Notebook**: Exploratory data analysis and model development
- **VS Code / PyCharm**: Project development environment
- **Google Images**: Source for raw training images (scraped)

### 🌐 Web Technologies:
- **Flask**: Lightweight Python web framework to serve the model
- **HTML/CSS/JavaScript**: For building the UI to upload and classify images

---

## 🚀 Key Functionalities

- 📸 **Image Collection**: Uses Google image scraping to gather training data.
- 🧼 **Preprocessing**: Images are cleaned, resized, and converted to grayscale using OpenCV.
- 🧠 **Model Training**: A machine learning classifier (SVM or KNN) is trained on facial feature data extracted from images.
- 🌐 **Web Integration**: A Flask server exposes an API to accept uploaded images and return predictions.
- 💻 **Interactive UI**: A web interface allows users to upload images and view the classified celebrity result in real-time.



🙌 Credits
Inspired by codebasics, this project is a hands-on exercise in integrating machine learning models with web apps using Flask.