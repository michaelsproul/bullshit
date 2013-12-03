import random

from wordlist import *

def sanitize(sentence):
        return sentence[0].upper() + sentence[1:] + "."

def prediction_sentence():
	s = cosmic_event()
	s += " " + choose(prediction_verb)
	s += " the " + choose(time_point)

	event = emotive_event()
	if event[0] in vowels:
		s += " of an " + event
	else:
		s += " of a " + event

	return sanitize(s)

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
	else:
		first = choose(planet, star, ["Moon"])
		second = choose_uniq({first}, planet, star, ["Moon"])
		return "The %s/%s %s" % (first, second, choose(aspect))

def emotive_event():
	r = random.random()

	if r <= 0.5:
		return choose(emotive_adj) + " " + choose(time_period)
	else:
		return choose(time_period) + " of " + choose(feeling)

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
