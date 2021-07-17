# SpamFilter
Simple spam filter that checks if a message is spam or not.

Spam filter utilizes probability and needs to be trained.
The training set used is found at https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection.
To utilize other training sets, please follow the following format for the training file:
  1. Indicate ham or spam as the first word in the line.
  2. Only use new lines to separate messages.

Additional functions added includes returning the words that
the program found to most likely indicate spam or not.
