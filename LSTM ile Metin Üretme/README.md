# Text Generation with LSTM
## Project Overview
This project implements a text generation model using LSTM (Long Short-Term Memory) neural networks. The model learns from Turkish sentences and can generate new, meaningful text sequences based on given starting words. For example, when given "ben yarın" (I tomorrow), it can predict the next words to form a complete sentence.

## Technical Details
### Model Architecture
Embedding Layer: Converts words into numerical vectors

LSTM Layer: 100 units for sequence learning

Dense Layer: Softmax activation for word prediction

### Dataset
100 Turkish sentences about daily life

Generated using ChatGPT simulation

Contains various contexts: home, school, work, transportation, emotions, etc.

### Preprocessing Steps
Tokenization: Converting words to numerical indices

Sequence Creation: Generating n-gram sequences for training

Padding: Standardizing sequence lengths for the neural network

One-Hot Encoding: Converting target variables for classification

### Installation & Requirements

```bash
pip install -r requirements.txt
```

Required libraries:


TensorFlow

NumPy

Keras

Usage
The model can generate text by predicting the next words:

```python
generated_text = generate_text("Bugün", 5)
print(generated_text)
```

How It Works
The model processes input text and creates training sequences

Each sequence is used to predict the next word in the sentence

During generation, the model takes starting words and iteratively predicts subsequent words

The process continues until the specified number of words is generated

Model Training
Optimizer: Adam

Loss Function: Categorical Crossentropy

Epochs: 100

Metrics: Accuracy

Features
Handles Turkish language text

Generates contextually relevant sentences

Learns from diverse daily life expressions

Can be extended with more training data

Future Improvements
Expand dataset with more diverse topics

Increase vocabulary size

Add more sophisticated language modeling techniques

Implement beam search for better text generation