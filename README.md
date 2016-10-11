# TEXer
A tool to detect temporal expression from free text


# About
Automatic translation of clinical researcher data requests to executable database queries is instrumental to an effective interface between clinical researchers and “Big Clinical Data”. A necessary step towards this goal is to parse ample temporal expressions in free-text researcher requests. This paper reports a novel algorithm called TEXer. It uses heuristic rule and pattern learning for extracting and normalizing temporal expressions in researcher requests. Based on 400 real clinical queries with human annotations, we compared our method with four baseline methods. TEXer achieved a precision of 0.945 and a recall of 0.858, outperforming all the baseline methods. We conclude that TEXer is an effective method for temporal expression extraction from free-text clinical data requests. 


# Usage
TEXer_English: the TEXer tool for English free medical text

TEXer_Chinese: the TEXer tool for English free medical text


# Data usage
training: some training instances
training_gold: the gold standard (human annotation) of the training data
training_pattern: the trained patterns
testing: some testing instances
testing_gold: the gold standard (human annotation) of the testing data


# Citation
Tianyong Hao, Alex Rusanov, Chunhua Weng. Extracting and Normalizing Temporal Expressions in Clinical Data Requests from Researchers. Lecture Notes in Computer Science, Volume 8040, pp 41-51, Springer, 2013.  
