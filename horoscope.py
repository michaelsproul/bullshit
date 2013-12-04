import random

from datetime import date, timedelta
from wordlist import *

def horoscope():
	# Feeling good or bad?
	statement = choose([positive_statement_s, negative_statement_s])

	openers = [statement, cosmic_implication_s]
	sentences = [statement, cosmic_implication_s, plain_warning_s]

	# Pick an opening sentence type and remove it from the latter sentences
	opener = choose(openers)
	sentences.remove(opener)

	# Delete a random sentence to avoid rambling on
	get_rid = choose(sentences)
	sentences.remove(get_rid)

	# Shuffle the remaining sentence types and evaluate them
	random.shuffle(sentences)
	final_text = opener()

	for sentence in sentences:
		final_text += " " + sentence()

	# Optionally add a date prediction
	if random.random() <= 0.5:
		final_text += " " + date_prediction_s()

	return final_text

def random_sentence():
	sentences = [date_prediction_s, plain_warning_s, cosmic_implication_s,
			positive_statement_s, negative_statement_s]
	return choose(sentences)()

def date_prediction_s():
	today = date.today()
	days_in_future = random.randint(2, 8)
	significant_day = today + timedelta(days=days_in_future)
	month = significant_day.strftime("%B")
	day = significant_day.strftime("%d").lstrip('0')
	s = "%s %s will be an important day for you" % (month, day)
	return sentence_case(s)

def positive_statement_s():
	s = feeling_statement(good_feeling_adj, positive_assertion)
	exciting = True if random.random() <= 0.5 else False
	return sentence_case(s, exciting)

def negative_statement_s():
	s = feeling_statement(bad_feeling_adj, negative_assertion)
	return sentence_case(s)

def feeling_statement(adjectives, ending):
	adj = choose(adjectives)
	adj = ing_to_ed(adj)

	s = "You are feeling %s %s" % (choose(emotional_degree), adj)
	s += ", " + ending()
	return s

def positive_assertion():
	r = random.random()

	if r <= 0.5:
		return "and there's nothing anyone can %s to stop you" % choose(["say", "do"])
	elif r <= 0.95:
		return "and you don't care who knows it"
	else:
		return "and you don't give a fuck"

def negative_assertion():
	"Consolations for bad feelings"
	r = random.random()

	if r <= 0.7:
		return "but don't worry, everything will improve %s" % choose(["shortly", "soon", "in due time"])
	else:
		return "perhaps you need a change in your life?"

def plain_warning_s():
	r = random.random()

	if r <= 0.5:
		s = "You would be well advised to avoid " + choose(avoid)
	else:
		s = "Avoid " + choose(avoid) + "; you wouldn't want to sabotage your mental wellbeing"

	return sentence_case(s)

def cosmic_implication_s():
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
	item = choose(*args)
	while item in exclude:
		item = choose(*args)
	return item

def choose(*args):
	"Choose a random item from a variable number of lists."
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
	sentence = sentence[0].upper() + sentence[1:]

	if sentence[-1] in {'.', '!', '?'}:
		return sentence
	elif exciting:
		return sentence + "!"
	else:
		return sentence + "."

def ing_to_ed(word):
	"Convert `ing' endings to `ed' endings"
	if word[-3:] == "ing":
		return (word[:-3] + "ed")
	else:
		return word


if __name__ ==  "__main__":
	print horoscope()
