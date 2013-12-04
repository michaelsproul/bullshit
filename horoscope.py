import random

from wordlist import *

def sentence_case(sentence, exciting=False):
	if exciting:
		return "%s%s!" %(sentence[0].upper(), sentence[1:])
	else:
		return "%s%s." %(sentence[0].upper(), sentence[1:])

def horoscope():
	sentences = [statement_s, cosmic_implication_s, plain_warning_s]
	random.shuffle(sentences)
	final_text = ""
	for sentence in sentences:
		final_text += sentence() + " "
	return final_text.rstrip()

def statement_s():
	s = "You are feeling %s %s" % (choose(emotional_degree), choose(good_feeling_adj))
	s += ", and there's nothing anyone can %s to stop you" % choose(["say", "do"])
	return sentence_case(s, exciting=True)

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
		adj = choose(good_feeling_adj, good_emotive_adj, bad_emotive_adj)
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
