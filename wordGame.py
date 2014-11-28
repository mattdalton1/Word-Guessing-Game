from flask import Flask, render_template, url_for, request, redirect, flash
import time, random
from operator import itemgetter
app = Flask(__name__)

# Open file containing suitable guess words
with open('/home/daltonmatt1/Word-Guessing-Game/files/guessWords.txt') as word_file:
    english_words = set(word.strip().lower() for word in word_file)
word_file.close()

# Function to check if guess word is a real word
def is_english_word(word):
    return word.lower() in english_words

""" Given a string of letters, return a dictionary
    which associates a frequency count with each letter. """
def freq_count(letters):
	f_count = {}
	for char in letters:
		f_count.setdefault(char,0)
		f_count[char] += 1
	return f_count

""" Returns True if the letters that make up "what" are
    contained in the letters that make up "source_word",
    otherwise False is returned. """
def contains(source_word, what):
	sc = freq_count(source_word)
	wc = freq_count(what)
	for letter,count in wc.items():
		if sc.get(letter,0) < count:
			return False
	return True

@app.route('/')
def display_home():
	return render_template('home.html',
		the_title="Welcome to the Word Guessing Game",
		wordGame_url=url_for('playGame'),
		showAllScores_url=url_for('showAllScores'),
        showRules_url=url_for('displayRules') )

@app.route('/Rules')
def displayRules():
    return render_template('showRules.html',
        the_title="Rules of the Game",
        home_link=url_for("display_home"),
        word_game=url_for("playGame") )

@app.route('/Word Game')
def playGame():

	# Open file containing source words
	with open('/home/daltonmatt1/Word-Guessing-Game/files/sourceWords.txt') as srcWords:
		word=random.choice(list(srcWords)) # Randomly select one line from the file
		srcWord=word.replace('\n','')
	srcWords.close()
	start_time = time.time()

	return render_template('wordGame.html',
		starting_point = time.time(),
		the_title='Word Guessing Game',
		the_srcWrd=srcWord,
		home_link=url_for("display_home"),
        word_game=url_for("playGame"),
		starting_time = start_time,
		saveWords_url=url_for('saveformdata') )

# return and process data from the form in the wordGame.html
@app.route('/The Score', methods=['POST'])
def saveformdata():
    guessWords=[] # place posted data from input tags in a list called guessWords
    all_ok = True
    srcWord=request.form['srcWord']
    srcWord=srcWord.lower()
    guessWords.extend( [request.form['wordOne'],request.form['wordTwo'],request.form['wordThree'],request.form['wordFour'],request.form['wordFive'],request.form['wordSix'],request.form['wordSeven']] )

    guessWords = [x.lower().strip() for x in guessWords]

    for guess in guessWords:

        if guess == '': # Check for empty input
            all_ok = False
            flash("An input field is empty.")

        elif guess==srcWord: # Check if a guess word is same as source word
            all_ok = False
            flash("The guess word " + guess + " cannot be the same as the source word.")

        elif guess != '' and (len(guess) < 3): # Check for less than three characters
            all_ok = False
            flash(guess + " must be at least 3 characters long.")

        elif not contains(srcWord, guess):
            all_ok = False
            flash("Character(s) in " +  guess + " is not in the source word.")

        elif guess != '' and not is_english_word(guess): # Check if it is a real word
            all_ok = False
            flash(guess + " is not a real word.")

        elif guessWords != '' and any(guessWords.count(x) > 1 for x in guessWords): # Check for duplication
            all_ok = False
            flash("The guess word " + guess + " is duplicated.")

    if all_ok:
        del guessWords[:]
        end_time = time.time()
        starting_time = request.form['time']
        starting_time = float(starting_time)
        print_elapsed_time = "completed in %d minute(s) and %.1f seconds" % divmod(end_time - starting_time,60)

        return render_template('userScore.html',
            the_title="You're Score",
            elapsed_time=print_elapsed_time,
            home_link=url_for("display_home"),
            word_game=url_for("playGame"),
            saveNameAndTime_url=url_for('saveNameAndTime') )
    else:
        del guessWords[:] #empty list
        return redirect(url_for('playGame'))

@app.route('/', methods=['POST'])
def saveNameAndTime():
    name = request.form['user_name']
    time = request.form['user_time']
    details=' '.join([name,time])

    with open('/home/daltonmatt1/Word-Guessing-Game/files/topScores.txt', 'a') as log:
        log.write(details + '\n')
    log.close()
    # Check if current users score is in the top ten

    return showAllScores()

@app.route('/Top Ten List') # Show 10 top scores
def showAllScores():
    myfile = open('/home/daltonmatt1/Word-Guessing-Game/files/topScores.txt')
    lines = [lines.split() for lines in myfile]
    lines.sort(key=itemgetter(3,6))
    lines=lines[0:10]

    return render_template("topScores.html",
        the_title="Top Scorers List",
        home_link=url_for("display_home"),
        word_game=url_for("playGame"),
        the_data=lines)

app.secret_key = "Maybe_just_once_someone_will_call_me_Sir_without_adding_Youre_making_a_scene"
if __name__ == "_main_":
    app.run()