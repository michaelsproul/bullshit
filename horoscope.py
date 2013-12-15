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

	discussion_s = choose_from([relationship_s, encounter_s])
	sentences = [feeling_statement_s, cosmic_implication_s, warning_s,
			discussion_s]

	# Select 2 or 3 sentences
	random.shuffle(sentences)
	final_text = sentences[0](mood)
	n = choose_from([2, 3])
	for i in range(1, n):
		final_text += " " + sentences[i](mood)

	# Optionally add a date prediction
	if random.random() <= 0.5 and n == 2:
		final_text += " " + date_prediction_s(mood)

	return final_text


def relationship_s(mood):
	"""Generate a sentence about a relationship."""
	if mood == "good":
		verb = "strengthened"
		talk = "discussion"
	else:
		verb = "strained"
		talk = "argument"

	person = choose_from(familiar_people)
	topic = choose_from(conversation_topics)
	s = "Your relationship with %s may be %s " % (person, verb)
	s += "as the result of %s about %s" % (an(talk), topic)

	return sentence_case(s)


def encounter_s(mood):
	"""Generate a few sentences about a meeting with another person."""
	person = choose_from(familiar_people, strange_people)
	location = choose_from(locations)
	prep = location[0]
	location = location[1]
	s1 = "You may meet %s %s %s." % (person, prep, location)

	if mood == "good":
		discussion = choose_from(neutral_discussions, good_discussions)
		if random.random() <= 0.5:
			feeling = choose_from(good_feeling_nouns)
			feeling = "feelings of %s" % feeling
		else:
			feeling = choose_from(good_emotive_nouns)
	else:
		discussion = choose_from(neutral_discussions, bad_discussions)
		if random.random() <= 1:
			feeling = choose_from(bad_feeling_nouns)
			feeling = "feelings of %s" % feeling
		else:
			feeling = choose_from(bad_emotive_nouns)
	topic = choose_from(conversation_topics)

	s2 = "%s about %s may lead to %s." % (an(discussion), topic, feeling)
	s2 = sentence_case(s2)
	return "%s %s" % (s1, s2)


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
		adj = choose_from(good_feeling_adjs)
		degree = choose_from(good_degrees, neutral_degrees)
		ending = positive_intensifier
		exciting = True if random.random() <= 0.5 else False
	else:
		adj = choose_from(bad_feeling_adjs)
		degree = choose_from(bad_degrees, neutral_degrees)
		ending = consolation
		exciting = False

	adj = ing_to_ed(adj)
	are = choose_from([" are", "'re"])
	s = "You%s feeling %s %s" % (are, degree, adj)
	s += ending()
	return sentence_case(s, exciting)


def positive_intensifier():
	"""Extend a statement of positive feelings."""
	r = random.random()

	if r <= 0.5:
		verb = choose_from(["say", "do"])
		return ", and there's nothing anyone can %s to stop you" % verb
	elif r <= 0.95:
		return ", and you don't care who knows it"
	else:
		return ", and you don't give a fuck"


def consolation():
	"""Provide consolation for feeling bad."""
	r = random.random()

	if r <= 0.6:
		when =  choose_from(["shortly", "soon", "in due time"])
		return ", but don't worry, everything will improve %s" % when
	elif r <= 0.9:
		return ", perhaps you need a change in your life?"
	else:
		return "..."


def warning_s(mood):
	r = random.random()
	bad_thing = choose_from(avoid_list)

	if r <= 0.27:
		s = "You would be well advised to avoid %s" % bad_thing
	elif r <= 0.54:
		s = "Avoid %s at all costs" % bad_thing
	elif r <= 0.81:
		s = "Steer clear of %s for a stress-free week"  % bad_thing
	else:
		also_bad = choose_uniq({bad_thing}, avoid_list)
		s = "For a peaceful week, avoid %s and %s" % (bad_thing, also_bad)

	return sentence_case(s)


def cosmic_implication_s(mood):
	"""Generate a sentence about the influence of a cosmic event."""
	c_event = cosmic_event()
	verb = choose_from(prediction_verbs)

	# Bad mood =  End of good, or start of bad
	# Good mood = End of bad, or start of good
	r = random.random()
	if mood == 'bad' and r <= 0.5:
		junction = choose_from(beginnings)
		e_event = emotive_event('bad')
	elif mood == 'bad':
		junction = choose_from(endings)
		e_event = emotive_event('good')
	elif mood == 'good' and r <= 0.5:
		junction = choose_from(beginnings)
		e_event = emotive_event('good')
	else:
		junction = choose_from(endings)
		e_event = emotive_event('bad')

	s = "%s %s the %s of %s" % (c_event, verb, junction, e_event)
	return sentence_case(s)


def cosmic_event():
	r = random.random()

	if r <= 0.25:
		return choose_from(planets) + " in retrograde"
	elif r <= 0.5:
		ce = "the " + choose_from(["waxing", "waning"])
		ce += " of " + choose_from(planets, ["the moon"], stars)
		return ce
	elif r <= 0.6:
		return "the " + choose_from(["New", "Full"]) + " Moon"
	elif r <= 0.75:
		return choose_from(wanky_events)
	else:
		first = choose_from(planets, stars, ["Moon"])
		second = choose_uniq({first}, planets, stars, ["Moon"])
		return "The %s/%s %s" % (first, second, choose_from(aspects))


def emotive_event(mood):
	"""Generate a sentence about a prolonged emotion."""
	if mood == 'good':
		adjectives_1 = good_feeling_adjs
		adjectives_2 = good_emotive_adjs
		nouns_1 = good_feeling_nouns
		nouns_2 = good_emotive_nouns
	else:
		adjectives_1 = bad_feeling_adjs
		adjectives_2 = bad_emotive_adjs
		nouns_1 = bad_feeling_nouns
		nouns_2 = bad_emotive_nouns

	if random.random() <= 0.5:
		adj = choose_from(adjectives_1, adjectives_2)
		return "%s %s" % (adj, choose_from(time_periods))
	else:
		noun = choose_from(nouns_1, nouns_2)
		return "%s of %s" % (choose_from(time_periods), noun)


def choose_uniq(exclude, *args):
	"""Choose a unique random item from a variable number of lists."""
	item = choose_from(*args)
	while item in exclude:
		item = choose_from(*args)
	return item

def choose_from(*args):
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


def opposite_mood(mood):
	return 'good' if (mood == 'bad') else 'bad'


def ing_to_ed(word):
	"""Convert `ing' endings to `ed' endings."""
	if word[-3:] == "ing":
		return (word[:-3] + "ed")
	else:
		return word

def an(word):
	"""Prefix with 'a' or 'an', as appropriate."""
	if word[0] in vowels:
		return "an %s" % word
	else:
		return "a %s" % word

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
