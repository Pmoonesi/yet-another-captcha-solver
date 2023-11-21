# yet-another-captcha-solver

In this repository, I tried to solve simple captchas which require simple mathematic operations of + and -. The images contain salt and pepper noises and simple bars. You can see a sample here:

![the sample](https://github.com/Pmoonesi/yet-another-captcha-solver/blob/master/sample.png?raw=true)

## what-did-i-do-first

At first, I labeled 5000 captchas and then, I tried regression using a simple cnn + fc network. The results were unsatisfying as my model never really converged. It turned out I didn't have enough data for a regression task.

## how-did-i-overcome

I went back to the library I used in my other captcha solving repository [whmcs-captcha-solver](https://github.com/Pmoonesi/whmcs-captcha-solver) called [CaptchaCracker](https://github.com/WooilJeong/CaptchaCracker). I had to change the model constructor first because unlike last time when label was included in the captcha's name, it was possible for multiple captchas to represent the same equations. So, I decided to break files down to captcha files and label files and this lead to code change in model constructors. My notebook could be found in `salt_and_pepper.ipynb`.

Also, captchas contained a lot of noise and I figured removing them would help the model learn the equation patterns easier. Therefore, I tried a couple of image processing methods for noise removal. My final pre-processing pipeline included a `closing operation`, `thresholding` and finally `dilation`. You can find the codes in `salt_and_pepper_prep.ipynb`.

![the processed sample](https://github.com/Pmoonesi/yet-another-captcha-solver/blob/master/sample_processed.png?raw=true)

After I got my data processed and my model ready, I trained my model for 20 epochs and obtained 96.0% accuracy.

## dataset

I obtained the captchas using a captcha producing API and for that I used an script you can find in `util/download.sh`. After that I designed an easy-to-use labeling python app using tkinter. You may find its script in `util/annotate.py` as well.
Here are some pictures of `annotate.py`:

![annotate 1](https://github.com/Pmoonesi/yet-another-captcha-solver/blob/master/annotate1.png?raw=true)

![annotate 2](https://github.com/Pmoonesi/yet-another-captcha-solver/blob/master/annotate2.png?raw=true)

After that, I used this annotation tool to label each captcha with the answer to them, which ended up to be a waste of time because regression was not the answer to my problem. Then, I started all over again and labeled them with their respective equation. You can find my final dataset in `data`.

## webserver

I also created a tiny webserver using fastAPI for which you can find the code in `http-server`. You have to install the dependencies mentioned in the requirements.txt file before running the webserver. Also make sure you have tensorflow installed. I recommend using tensorflow on docker if you don't already have it installed.
To start the server you should just run `python main.py`. The main difference from `whmcs-captcha-solver` project was that here, I used preprocessed captchas to train my model; hence, We need to use the same pipeline to prepare each incoming request.
