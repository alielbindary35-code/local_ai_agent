Linear regression  |  Machine Learning  |  Google for Developers







[Skip to main content](#main-content) 










* [Machine Learning](https://developers.google.com/machine-learning)




























`/`








* English
* Deutsch
* Español
* Español – América Latina
* Français
* Indonesia
* Italiano
* Polski
* Português – Brasil
* Tiếng Việt
* Türkçe
* Русский
* Українська
* עברית
* العربيّة
* فارسی
* हिंदी
* বাংলা
* ภาษาไทย
* 中文 – 简体
* 中文 – 繁體
* 日本語
* 한국어




Sign in









* [ML Concepts](https://developers.google.com/machine-learning/crash-course)
































* [Home](https://developers.google.com/)
* [Products](https://developers.google.com/products)
* [Machine Learning](https://developers.google.com/machine-learning)
* [ML Concepts](https://developers.google.com/machine-learning/crash-course)
* [Crash Course](https://developers.google.com/machine-learning/crash-course/prereqs-and-prework)







 
 
 Send feedback
 
 

# 
 Linear regression


 
 Stay organized with collections
 

 
 Save and categorize content based on your preferences.








![Spark icon](/_static/images/icons/spark.svg)
## AI-generated Key Takeaways







outlined\_flag


* This module introduces linear regression, a statistical method used to predict a label value based on its features.
* The linear regression model uses an equation (y' = b + w₁x₁ + ...) to represent the relationship between features and the label.
* During training, the model adjusts its bias (b) and weights (w) to minimize the difference between predicted and actual values.
* Linear regression can be applied to models with multiple features, each with its own weight, to improve prediction accuracy.
* Gradient descent and hyperparameter tuning are key techniques used to optimize the performance of a linear regression model.









**Estimated module length:** 70 minutes
This module introduces **linear regression** concepts.


**Learning objectives:**
* Explain a loss function and how it works.
* Define and describe how gradient descent finds the optimal model
 parameters.
* Describe how to tune hyperparameters to efficiently train a linear model.



**Prerequisites:**
This module assumes you are familiar with the concepts covered in the
 following module:


* [Introduction to Machine Learning](/machine-learning/intro-to-ml)



[**Linear regression**](/machine-learning/glossary#linear-regression) is a
statistical technique used to find the relationship between variables. In an ML
context, linear regression finds the relationship between
[**features**](/machine-learning/glossary#feature) and a
[**label**](/machine-learning/glossary#label).


For example, suppose we want to predict a car's fuel efficiency in miles per
gallon based on how heavy the car is, and we have the following dataset:




| Pounds in 1000s (feature) | Miles per gallon
 (label) |
| --- | --- |
| 3.5 | 18 |
| 3.69 | 15 |
| 3.44 | 18 |
| 3.43 | 16 |
| 4.34 | 15 |
| 4.42 | 14 |
| 2.37 | 24 |


If we plotted these points, we'd get the following graph:


![Figure 1. Data points showing downward-sloping trend from left to right.](/static/machine-learning/crash-course/linear-regression/images/car-data-points.png) 


**Figure 1**. Car heaviness (in pounds) versus miles per gallon rating. As a
car gets heavier, its miles per gallon rating generally decreases.


We could create our own model by drawing a best fit line through the points:


![Figure 2. Data points with a best fit line drawn through them representing the model.](/static/machine-learning/crash-course/linear-regression/images/car-data-points-with-model.png) 


**Figure 2**. A best fit line drawn through the data from the previous figure.


## Linear regression equation


In algebraic terms, the model would be defined as $ y = mx + b $, where


* $ y $ is miles per gallon—the value we want to predict.
* $ m $ is the slope of the line.
* $ x $ is pounds—our input value.
* $ b $ is the y-intercept.


In ML, we write the equation for a linear regression model as follows:


 $$ y' = b + w\_1x\_1 $$ 
where:


* $ y' $ is the predicted label—the output.
* $ b $ is the [**bias**](/machine-learning/glossary#bias-math-or-bias-term)
of the model. Bias is the same concept as the y-intercept in the algebraic
equation for a line. In ML, bias is sometimes referred to as $ w\_0 $. Bias
is a [**parameter**](/machine-learning/glossary#parameter) of the model and
is calculated during training.
* $ w\_1 $ is the [**weight**](/machine-learning/glossary#weight) of the
feature. Weight is the same concept as the slope $ m $ in the algebraic
equation for a line. Weight is a
[**parameter**](/machine-learning/glossary#parameter) of the model and is
calculated during training.
* $ x\_1 $ is a [**feature**](/machine-learning/glossary#feature)—the
input.


During training, the model calculates the weight and bias that produce the best
model.


![Figure 3. The equation y' = b + w1x1, with each component annotated with its purpose.](/static/machine-learning/crash-course/linear-regression/images/equation.png) 


**Figure 3**. Mathematical representation of a linear model.


In our example, we'd calculate the weight and bias from the line we drew. The
bias is 34 (where the line intersects the y-axis), and the weight is –4.6 (the
slope of the line). The model would be defined as $ y' = 34 + (-4.6)(x\_1) $, and
we could use it to make predictions. For instance, using this model, a 
4,000-pound car would have a predicted fuel efficiency of 15.6 miles per
gallon.


![Figure 4. Same graph as Figure 2, with the point (4, 15.6) highlighted.](/static/machine-learning/crash-course/linear-regression/images/model-prediction.png) 


**Figure 4**. Using the model, a 4,000-pound car has a predicted
fuel efficiency of 15.6 miles per gallon.


### Models with multiple features


Although the example in this section uses only one feature—the heaviness
of the car—a more sophisticated model might rely on multiple features,
each having a separate weight ($ w\_1 $, $ w\_2 $, etc.). For example, a model
that relies on five features would be written as follows:


$ y' = b + w\_1x\_1 + w\_2x\_2 + w\_3x\_3 + w\_4x\_4 + w\_5x\_5 $


For example, a model that predicts gas mileage could additionally use features
such as the following:


* Engine displacement
* Acceleration
* Number of cylinders
* Horsepower


This model would be written as follows:


![Figure 5. Linear regression equation with five features.](/static/machine-learning/crash-course/linear-regression/images/equation-multiple-features.png) 


**Figure 5**. A model with five features to predict a car's miles per gallon
rating.


By graphing a couple of these additional features, we can see that they also
have a linear relationship to the label, miles per gallon:


![Figure 6. Displacement in cubic centimeters graphed against miles per gallon showing a negative linear relationship.](/static/machine-learning/crash-course/linear-regression/images/displacement.png) 


**Figure 6**. A car's displacement in cubic centimeters and its miles per gallon
rating. As a car's engine gets bigger, its miles per gallon rating generally
decreases.


![Figure 7. Acceleration from zero to sixty in seconds graphed against miles per gallon showing a positive linear relationship.](/static/machine-learning/crash-course/linear-regression/images/acceleration.png) 


**Figure 7**. A car's acceleration and its miles per gallon rating. As a car's
acceleration takes longer, the miles per gallon rating generally increases.


### Exercise: Check your understanding





 What parts of the linear regression equation are updated during training?
 

The bias and weights

 During training, the model updates the bias and
 weights.
 


The prediction

 Predictions are not updated during training.
 


The feature values

 Feature values are part of the dataset, so they're not updated
 during training.
 



**Key terms:**
* [Bias](/machine-learning/glossary#bias-math-or-bias-term)
* [Feature](/machine-learning/glossary#feature)
* [Label](/machine-learning/glossary#label)
* [Linear regression](/machine-learning/glossary#linear-regression)
* [Parameter](/machine-learning/glossary#parameter)
* [Weight](/machine-learning/glossary#weight)




[Help Center](https://support.google.com/machinelearningeducation)




[Previous

 arrow\_back
 

 Exercises](/machine-learning/crash-course/exercises)


[Next

 Loss (10 min)
 

 arrow\_forward](/machine-learning/crash-course/linear-regression/loss)








 
 
 Send feedback
 
 




Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.


Last updated 2025-08-25 UTC.









 
 Need to tell us more?
 
 



 [[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-08-25 UTC."],[],[]]