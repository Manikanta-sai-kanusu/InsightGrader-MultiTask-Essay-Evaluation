
# 🧠 InsightGrader

## Intelligent Essay and Answer Evaluation with Misconception Tracking and Cognitive Load Insights — A Comparative Analysis

> A Multi-Task Learning framework for Automated Essay Scoring and Token-Level Error Detection using Transformer-based Deep Learning Models.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-DeepLearning-red?style=for-the-badge&logo=pytorch)
![Transformers](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-WebApp-black?style=for-the-badge&logo=flask)
![Optuna](https://img.shields.io/badge/Optuna-Hyperparameter_Optimization-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

# 📖 About the Project

InsightGrader is an AI-powered educational Natural Language Processing (NLP) framework designed to automate essay and answer evaluation through a Multi-Task Learning architecture.

Traditional Automated Essay Scoring (AES) systems primarily focus on predicting a single holistic score without explaining why a student lost marks. Similarly, grammar checking systems only identify writing mistakes without estimating the overall writing quality.

InsightGrader bridges this gap by jointly performing:

- Holistic Essay Scoring
- Token-Level Error Detection
- Misconception Identification
- Cognitive Load Analysis

using a shared Transformer encoder with two specialized prediction heads.

The proposed framework compares multiple state-of-the-art Transformer architectures alongside recurrent neural network models to determine the most effective architecture for educational assessment.

Unlike conventional approaches, InsightGrader not only predicts writing quality but also provides interpretable feedback that can help students improve their writing skills.

---

# 🎯 Motivation

Evaluating essays manually is time-consuming, subjective, and difficult to scale for large educational institutions.

Most Automated Essay Scoring systems only provide a numerical score without identifying specific writing issues.

InsightGrader was developed to provide:

- Accurate automated scoring
- Fine-grained writing error detection
- Explainable educational feedback
- Misconception identification
- Student learning analytics

through a single unified deep learning framework.

---

# ✨ Key Features

✔ Automated Essay Scoring (AES)

✔ Intelligent Short Answer Evaluation

✔ Multi-Task Learning Framework

✔ Transformer-based Deep Learning

✔ Token-Level BIO Error Detection

✔ Misconception Tracking

✔ Cognitive Load Insights

✔ Comparative Analysis of Eight Deep Learning Models

✔ Hyperparameter Optimization using Optuna

✔ Interactive Flask Web Application

✔ Research-Oriented Architecture

✔ Modular AI Pipeline

✔ Scalable Educational Assessment

---

# 🚀 Objectives

The primary objectives of InsightGrader are:

• Develop an intelligent automated essay evaluation system.

• Predict holistic writing quality using regression models.

• Detect token-level grammatical and contextual errors using BIO tagging.

• Compare the performance of Transformer-based and RNN-based architectures.

• Generate interpretable educational feedback.

• Improve automated assessment reliability through Multi-Task Learning.

• Provide scalable educational AI for modern learning environments.

---

# 🛠 Technologies Used

## Programming Language

- Python

## Deep Learning

- PyTorch

## Natural Language Processing

- Hugging Face Transformers
- Tokenizers

## Machine Learning

- Scikit-learn
- Optuna

## Data Processing

- Pandas
- NumPy

## Visualization

- Matplotlib

## Web Application

- Flask

## Development Environment

- Jupyter Notebook
- VS Code

---

# 📚 Dataset

The project is trained using the **Feedback Prize – English Language Learning** dataset available on Kaggle.

The dataset contains approximately **3,900 student essays** written by students from grades 6–12.

Each essay contains six human-annotated proficiency scores assigned by Cambridge English examiners.

The evaluated writing traits include:

- Cohesion
- Syntax
- Vocabulary
- Phraseology
- Grammar
- Writing Conventions

These scores range from **1.0 to 5.0** and serve as the regression targets for essay evaluation.

To support token-level error detection, BIO labels were generated and aligned with Transformer tokenizer outputs.

---

# 🔍 Data Preprocessing

Before model training, several preprocessing operations were applied to improve data quality and model performance.

The preprocessing pipeline includes:

- Lowercase conversion
- Removal of unnecessary symbols
- White-space normalization
- Punctuation normalization
- Lemmatization
- Stop-word handling
- Spelling correction
- Contraction expansion
- Sentence filtering
- Tokenization
- BIO label alignment
- Attention mask generation

Additional linguistic features such as:

- Sentence Count
- Token Count
- Average Sentence Length
- Vocabulary Richness
- Type-Token Ratio
- Readability Score

were also extracted to enhance model understanding.

---

# 🧠 Methodology

InsightGrader adopts a Multi-Task Learning architecture.

A shared Transformer encoder learns contextual semantic representations from essay text.

The extracted representations are simultaneously used by two prediction heads.

### Task 1

Essay Score Prediction

This task predicts the overall writing quality using a regression head.

Evaluation Metrics:

- RMSE
- R² Score

### Task 2

BIO Error Detection

A sequence labeling head predicts BIO tags for every token.

This enables:

- Error Localization
- Error Span Detection
- Fine-grained Feedback

Joint optimization of these two tasks allows the model to learn richer contextual representations while improving both scoring accuracy and token-level prediction.

---

# 🤖 Models Evaluated

The following architectures were experimentally evaluated.

| Model | Category |
|---------|----------|
| BERT | Transformer |
| RoBERTa | Transformer |
| DeBERTa | Transformer |
| Longformer | Transformer |
| XLM-RoBERTa | Transformer |
| Flan-T5 Encoder | Transformer |
| BiLSTM | Recurrent Neural Network |
| GRU | Recurrent Neural Network |

Each model was trained and evaluated under identical experimental settings to ensure a fair comparison.

---

# 📈 Experimental Results

The experimental analysis demonstrates that Transformer-based architectures significantly outperform traditional recurrent neural networks for automated essay evaluation.

Among all evaluated models,

**DeBERTa achieved the best overall performance**

with:

- BIO Accuracy: **1.000**
- R² Score: **0.886**
- RMSE: **0.1875**

The results indicate that contextual Transformer representations provide superior semantic understanding and regression performance compared to recurrent architectures such as BiLSTM and GRU.

---

# 📂 Project Files Explained

### `app.py`

Main Flask application responsible for launching the web server, loading trained models, processing user requests, and returning essay evaluation results.

---

### `frontend.py`

Implements the user interface logic and connects the backend prediction pipeline with the interactive web application.

---

### `model.py`

Contains the neural network architecture definitions, prediction heads, inference pipeline, and model loading utilities.

---

### `your_model_file.py`

Implements custom deep learning components including model initialization, prediction functions, utility methods, and inference helpers used during evaluation.

---

### `InsightGrader_Training.ipynb`

Complete research notebook containing:

- Data preprocessing
- Feature engineering
- Tokenization
- BIO label generation
- Model training
- Hyperparameter optimization
- Evaluation
- Experimental comparison
- Result visualization

---

### `BERT_best.pth`

Saved PyTorch checkpoint containing the best-performing BERT model weights.

---

### `Roberta_best_tuned.pth`

Optimized RoBERTa model obtained after hyperparameter tuning with Optuna.

---

### `requirements.txt`

Lists all Python packages required to reproduce the project.

---

### `README.md`

Project documentation explaining installation, methodology, implementation, and usage.


# 📊 Evaluation Metrics

The framework evaluates model performance using standard regression and sequence-labeling metrics.

### Essay Scoring

- R² Score
- Root Mean Square Error (RMSE)
- Mean Absolute Error (MAE)

### BIO Error Detection

- Accuracy
- Precision
- Recall
- F1 Score

These metrics collectively measure both holistic essay evaluation quality and token-level prediction performance.

---

# 🎯 Applications

InsightGrader can be applied in a wide range of educational environments.

### Educational Institutions

- Automated assignment grading
- Essay evaluation
- Writing assessment

### Online Learning Platforms

- Personalized feedback
- Student progress tracking
- Large-scale assessment

### Competitive Examinations

- Automated descriptive answer evaluation
- Writing quality analysis
- Language proficiency assessment

### Research

- Educational NLP
- Automated Essay Scoring
- Intelligent Tutoring Systems
- Explainable AI in Education

---

# 📈 Results and Observations

Extensive experimentation was conducted across multiple Transformer and recurrent neural network architectures.

Key observations include:

- Transformer-based models consistently outperformed traditional recurrent architectures.
- Multi-Task Learning improved both essay scoring accuracy and token-level error detection.
- Shared contextual representations enabled better semantic understanding of student responses.
- Hyperparameter optimization using Optuna further enhanced prediction performance.
- DeBERTa achieved the strongest overall performance among the evaluated models.

The experimental findings demonstrate the effectiveness of combining regression and sequence labeling within a unified framework.

---

# 🔬 Research Contributions

The major contributions of this project include:

- Development of a unified Multi-Task Learning framework for automated educational assessment.
- Simultaneous essay scoring and token-level BIO error detection using shared Transformer representations.
- Comparative analysis of multiple Transformer and recurrent neural network architectures.
- Integration of Optuna for automated hyperparameter optimization.
- Development of an interactive web application for real-time essay evaluation.
- Support for interpretable educational feedback through token-level error localization.
- Framework designed for scalability in educational institutions and online learning platforms.

---

# 🚀 Future Enhancements

Several improvements can further extend the capabilities of InsightGrader:

- Support for multilingual essay evaluation.
- Integration of Large Language Models (LLMs) for richer feedback generation.
- Explainable AI visualizations using SHAP and LIME.
- Rubric-based scoring for standardized examinations.
- Real-time classroom analytics dashboard.
- Cloud deployment for large-scale educational institutions.
- Speech-to-text essay evaluation.
- Personalized learning recommendations.
- Adaptive feedback based on student proficiency levels.

---

# ⭐ Support

If you find this project useful for your research or learning, consider giving it a ⭐ on GitHub.

Your support helps improve the project and encourages future development.

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project in accordance with the terms of the license.

For more details, see the `LICENSE` file.

---

## Thank You

Thank you for visiting the InsightGrader repository.

Feedback, suggestions, and contributions are always welcome. Feel free to open an issue or submit a pull request to help improve the project.
