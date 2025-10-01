---
layout: post
title: "Welcome to the Blog"
date: 2025-09-30
image: https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?w=1200&h=800&fit=crop
---

Welcome to my new blog! After years of working with WordPress on AWS Lightsail, I've migrated to a cleaner, more modern setup using Jekyll and GitHub Pages.

## What to Expect

I'll be writing about three main areas:

### Commodities
Insights from the world of commodity trading, market analysis, and quantitative approaches to understanding commodity markets.

### Machine Learning
Practical machine learning applications, from model development to deployment. I'll share code, techniques, and lessons learned from real-world projects.

### Generative AI
Exploring the rapidly evolving world of large language models, their applications, and how they're transforming software development and beyond.

## Why This Setup?

This blog is built with:
- **Jekyll**: A simple, blog-aware static site generator
- **GitHub Pages**: Free hosting with excellent performance
- **Markdown**: Clean, version-controlled content

This gives me complete control over the content and design while keeping things simple and maintainable.

## Example: A Simple ML Concept

To demonstrate the technical capabilities of this setup, here's a quick example of linear regression in Python:

```python
import numpy as np
from sklearn.linear_model import LinearRegression

# Sample data
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Create and fit model
model = LinearRegression()
model.fit(X, y)

# Predict
prediction = model.predict([[6]])
print(f"Prediction for x=6: {prediction[0]:.2f}")
```

And here's some mathematical notation using MathJax:

The formula for linear regression can be expressed as:

$$y = \beta_0 + \beta_1 x + \epsilon$$

Where:
- $y$ is the dependent variable
- $\beta_0$ is the intercept
- $\beta_1$ is the slope
- $x$ is the independent variable
- $\epsilon$ is the error term

## Moving Forward

Stay tuned for more detailed posts on machine learning projects, commodity market analysis, and explorations of generative AI capabilities.

Feel free to reach out if you have questions or topics you'd like me to cover!