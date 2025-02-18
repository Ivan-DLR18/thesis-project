# Thesis Project Documentation

Hi, this is the code and tools I used for the thesis project for my Master's degree. 👨🏽‍💻
In this project I investigated how collective intelligence in video comment sections can be leveraged for predictive analysis. Through a rigorous research process, I designed and executed experiments to validate hypotheses, uncovering patterns in crowd wisdom that offer meaningful insights. The dissertation successfully met its objectives, contributing to the understanding of social data as a predictive tool in real-world applications.
I am trying to clean the code and I will be updating it little by little, thanks for your patience :)

## Contents
- Sentiment Analysis Folder
- Notebooks:
    - YT-API.ipynb
    - data-collection.ipynb
    - comment-translation.ipynb
    - classifiers-test.ipynb


### Data collection
The first step for this work was data collection. This was done using three main data sources using different web scraping techniques. The three sites were:
- FBREF (see `fbref-scraping.py`)
- Transfermarkt (see `transfermarkt-scraping.py`)
- Sofifa (see `sofifa-scraping.py`)


### Youtube API
The code for retrieving comments and titles from the YouTube API is found in the file `YT-API.ipynb`. This file uses a 'bank' of API keys to obtain the results, in each query it will try to obtain it with a certain API key and if the limit is exceeded, it will perform the same task again with the next API key in the 'bank'.

This code has different functions depending the type of format of the query, being either search or video. The search part works by looking for specific keywords and filtering the search using the `football_id`, `videoCategoryId`, and the `publishedBefore` and `publishedAfter` for controlling the time-frame for the search.

Then for each video found the Id of the video is used for getting the comments and view count for each of the videos found in the result using the function `.get_video_comments`.

The final part of the code is the implementation of all of this functions based on a list of players stored in a csv, and saving the titles and comments in different files for each player using the id wich the code is expecting to found in the a csv column.


### Sentiment Analysis folder
The folder `sentiment-analysis` contains the codes used for the testing in the public football-specific dataset by Aloufi et al. (2018) **(PLEASE CITE THEM IF YOU'RE PLANNING ON USING IT)**

The main code for the Sentiment Analysis is in `TP-SA-main.ipynb`. It uses the model `cardiffnlp/twitter-roberta-base-sentiment` for this taks and uses the youtube files found in the `datasets` folder.

Since it returns probabilities, the classification test plays with the threshold for defining which is the predominant senitment of a text.

For the benchmark results in the public dataset and compared with the results also find in the work by Aloufi et al. (2018), can be found in the file `benchmark-results.ipynb`

Finally, the file for obtaining the final results when including the added features from YT data, along with the dataset used for obtining them can be found in the `dataset/final-result` folder.


### Comment translation
The file `comment-translation.ipynb` uses the models `papluca/xlm-roberta-base-language-detection` for detecting the language the title or comment is written in and based on the result, one of the follwing models from OPUS-MT is used for the translation task:
- `Helsinki-NLP/opus-mt-es-en` (for spanish to english)
- `Helsinki-NLP/opus-mt-de-en` (for german to english)
- `Helsinki-NLP/opus-mt-fr-en` (for french to english)
- `Helsinki-NLP/opus-mt-it-en` (for italian to english)

If any additional language is needed, just add the corresponding model from the Helsinki-NLP Hugging face repository and add it to the `.translate_text` function.

It uses the files `youtube-database-1`, `youtube-database-2` and `youtube-database-3` for the translation obtained during the data collection process. If you need access to the datasets, please feel free to contact me.


### Classification task
The classification task is done in the `classifiers-test.ipynb`. This file uses the `players-dataset-complete.csv` file for performing the classification procedure using the Random Forest, Gradient Boosting and SVM models for classification from scikit-learn. It uses a 5-fold grid-search for the hyper-parameter combination finding and the `make_imb_pipeline` pipeline for performing cross-validation with `SMOTE` used in each of the folds for the 5-fold cross-validation.

It also returns the classification report for each model along with the confusion matrix and the AUC-ROC score for each fold and the average score for the entire procedure.

Watch out! There are two types of code for each model, one is the training and testing without cross-validation and then the cross-validation, it is important to see that the pipeline is responsible to perform all the steps for the learning process in the specific order to maintain consistency and to make sure everything is done properly according to the literature.

Finally, note that since SVM is sensitive to feature scale, the scaler is included in the pipeline, as opossed to the Random Forest and Gradient Boosting models.

### Datasets
The folder `datasets` contain the resulting datasets for all the files used and produced by the files described above.

The YouTube comments and titles are compressed in the zip files `z-youtube-database-1`, `z-youtube-database-2` and `z-youtube-database-3`.

The file `player-dataset-complete.csv` contains all the players used for the analysis with the results for the improvement factor and weighted average. This improvement factor and weighted average was obtained in a separate excel file following the instructions in the thesis document. 


## Thanks for reading

<br>

<br>


Best,

MSc. Iván Díaz de León Rodríguez :)