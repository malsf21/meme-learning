# meme-learning
A tensorflow-based program that attempts to recognize different memes.

**Right now, none of this works. This is all just a nice experiment.**

Sample meme from [Reddit](https://www.reddit.com/r/AdviceAnimals/comments/2ixz5f/after_having_my_2100_upvoted_meme_removed_for_not/).

## Use Setup

This just tells you how you can run the script based on some predefined models, to do some meme identifying!

*Note: this code is inspired from [here](https://github.com/eldor4do/Tensorflow-Examples/blob/master/retraining-example.py), thanks @eldor4do!*

*This is supported on Python 3.3+. I do not know if this works on Python 2.7*.

Install your python dependencies.

```
pip3 install -r requirements.txt
```

Then, run the `image-recognition.py` script, with an image parameter of the image you want to check.

```
python3 image-recognition.py -i meme.jpg
```

## Development Setup

Want to help out? Awesome! First, you need to install [`bazel`](https://github.com/bazelbuild/bazel), some python dependencies (including tensorflow), and set up your environment.

First, you're going to need Java 8. If you have homebrew on OSX, things become super easy. Just type:

```
brew cask install java
```

If you're on a Linux system, you **should** (not completely sure) be able to do this:

```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

If not, head over to [Java's Website](https://www.java.com/en/download/manual.jsp) and get the correct version of Java installed.

Next, we're going to install [`bazel`](https://github.com/bazelbuild/bazel), a build tool that we use.

If you're using homebrew, just type in:

```
brew install bazel
```

If you're on a Linux system, you **should** (not completely sure) be able to follow these instructions:

```
echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install bazel
```

You can also check [Bazel's Releases page](https://github.com/bazelbuild/bazel/releases) for binary installers.

Then, we're going to clone the [Tensorflow GitHub Repository](https://github.com/tensorflow/tensorflow) and `cd` into it:

```
git clone https://github.com/tensorflow/tensorflow.git
cd tensorflow
```

Now, we're going to build [the image retrainer](https://www.tensorflow.org/how_tos/image_retraining/#training_on_your_own_categories)

```
bazel build tensorflow/examples/image_retraining:retrain
```

Now, we're going to need to have some images to train off of.

First, make a directory in ~/ called `memes`.

Then, for each meme you want to differentiate, make a new folder with a meme label (e.g. `Success-Kid`).

I will upload my test set soon.

In the new folder, get a bunch of that meme in there! The way I got my original training set is from [Quickmeme's Meme Category Pages](http://www.quickmeme.com/memes/Success-Kid/) (shoutout to Alex Meiburg and Randy Michnovicz for helping me out here), and parsing a few pages and downloading the images.

Here's how you can do it:

```bash
curl 'http://www.quickmeme.com/memes/Success-Kid/page/[1-10]/' -o '#1.html' && grep -oh 'http://s.quickmeme.com/img/.*jpg' *.html >urls.txt && sort -u urls.txt | wget -i-

```

Replace `Success-Kid` with the meme type you want, and the [1-10] signifies how deep you go into the archive (10 images per page).

Great! Now, we can run the actual retrainer! Get back to the root directory, and run this.

```
bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ~/memes
```

Now, your training is done! You can use the resulting labels (default `/tmp/output_labels.txt`) and model (default `/tmp/output_graph.pb`) that you've created to identify some memes, or run what's in the "use setup" section.
