#!/usr/bin/env python

"""Random Horoscope Generator, by Michael Sproul."""

import argparse
import random

import wordlist

from datetime import date, timedelta
from wordlist import *

def horoscope():
	"""Generate a three to four sentence horoscope."""
	# Pick a mood (usually positive)
	mood = "good" if random.random() <= 0.8 else "bad"

	openers = [feeling_statement_s, cosmic_implication_s]
	sentences = [feeling_statement_s, cosmic_implication_s, warning_s]

	# Pick an opening sentence and remove it from the latter sentences
	opener = choose(openers)
	sentences.remove(opener)

	# Delete a random sentence to avoid rambling on
	get_rid = choose(sentences)
	sentences.remove(get_rid)

	# Shuffle the remaining sentence types and evaluate them
	random.shuffle(sentences)
	final_text = opener(mood)

	for sentence in sentences:
		final_text += " " + sentence(mood)

	# Optionally add a date prediction
	if random.random() <= 0.5:
		final_text += " " + date_prediction_s(mood)

	return final_text


def date_prediction_s(mood):
	"""Generate a random prediction sentence containing a date."""
	days_in_future = random.randint(2, 8)
	significant_day = date.today() + timedelta(days=days_in_future)
	month = significant_day.strftime("%B")
	day = significant_day.strftime("%d").lstrip('0')

	r = random.random()

	if r <= 0.5:
		s = "%s %s will be an important day for you" % (month, day)
	elif r <= 0.8:
		s = "Interesting things await you on %s %s" % (month, day)
	else:
		s = "The events of %s %s have the potential to" % (month, day)
		s += " change your life"

	return sentence_case(s)


def feeling_statement_s(mood):
	"""Generate a sentence that asserts a mood-based feeling."""
	if mood == 'good':
		adj = choose(good_feeling_adj)
		degree = choose(good_degree, neutral_degree)
		ending = positive_intensifier
		exciting = True if random.random() <= 0.5 else False
	else:
		adj = choose(bad_feeling_adj)
		degree = choose(good_degree, neutral_degree)
		ending = consolation
		exciting = False

	adj = ing_to_ed(adj)
	s = "You are feeling %s %s" % (degree, adj)
	s += ending()
	return sentence_case(s, exciting)


def positive_intensifier():
	"""Extend a positive statement of feeling."""
	r = random.random()

	if r <= 0.5:
		verb = choose(["say", "do"])
		return ", and there's nothing anyone can %s to stop you" % verb
	elif r <= 0.95:
		return ", and you don't care who knows it"
	else:
		return ", and you don't give a fuck"


def consolation():
	"""Extend a negative statement of feeling."""
	r = random.random()

	if r <= 0.6:
		when =  choose(["shortly", "soon", "in due time"])
		return ", but don't worry, everything will improve %s" % when
	elif r <= 0.9:
		return ", perhaps you need a change in your life?"
	else:
		return "..."


def warning_s(mood):
	r = random.random()

	if r <= 0.5:
		s = "You would be well advised to avoid " + choose(avoid)
	else:
		s = "Avoid " + choose(avoid) + " at all costs"

	return sentence_case(s)


def cosmic_implication_s(mood):
	s = cosmic_event()
	s += " " + choose(prediction_verb)
	s += " the " + choose(time_point)

	event = emotive_event()
	if event[0] in vowels:
		s += " of an " + event
	else:
		s += " of a " + event

	return sentence_case(s)


def cosmic_event():
	r = random.random()

	if r <= 0.25:
		return choose(planet) + " in retrograde"
	elif r <= 0.5:
		ce = "the " + choose(["waxing", "waning"])
		ce += " of " + choose(planet, ["the moon"], star)
		return ce
	elif r <= 0.6:
		return "the " + choose(["New", "Full"]) + " Moon"
	elif r <= 0.75:
		return choose(wanky_event)
	else:
		first = choose(planet, star, ["Moon"])
		second = choose_uniq({first}, planet, star, ["Moon"])
		return "The %s/%s %s" % (first, second, choose(aspect))


def emotive_event():
	r = random.random()

	if r <= 0.5:
		adj = choose(good_feeling_adj, good_emotive_adj,
				bad_feeling_adj, bad_emotive_adj)
		return adj + " " + choose(time_period)
	else:
		noun = choose(good_emotive_noun, bad_emotive_noun)
		return choose(time_period) + " of " + noun


def choose_uniq(exclude, *args):
	"""Choose a unique random item from a variable number of lists."""
	item = choose(*args)
	while item in exclude:
		item = choose(*args)
	return item

def choose(*args):
	"""Choose a random item from a variable number of lists."""
	num_words = 0
	for list in args:
		num_words += len(list)

	i = random.randint(0, num_words - 1)
	j = 0
	while i >= len(args[j]):
		i -= len(args[j])
		j += 1

	return args[j][i]


def sentence_case(sentence, exciting=False):
	"""Capitalise the first letter of the sentence and add a full stop."""
	sentence = sentence[0].upper() + sentence[1:]

	if sentence[-1] in {'.', '!', '?'}:
		return sentence
	elif exciting:
		return sentence + "!"
	else:
		return sentence + "."

def ing_to_ed(word):
	"""Convert `ing' endings to `ed' endings."""
	if word[-3:] == "ing":
		return (word[:-3] + "ed")
	else:
		return word


def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser(description=__doc__)

	parser.add_argument("--dirty", action='store_true',
				help="Enable offensive horoscopes")

	parser.add_argument("--starsign", type=str, metavar="starsign",
				help="Generate a starsign specific horoscope")

	arguments = vars(parser.parse_args())

	if arguments["dirty"]:
		import dirtywords

	print(horoscope())

if __name__ ==  "__main__":
	main()
