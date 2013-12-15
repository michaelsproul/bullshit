"""Filth up the horoscope generator with some stupid words."""

import wordlist

wordlist.avoid_list.extend([	"poor people",
				"mamallian flesh",
				"white people",
				"black people",
				"foreigners",
				"oral sex",
				"bullshit artists",
				"cats that look like Jesus",
				"anarcho-syndicalists",
				"athesists",
				"Christians",
				"Mormons",
				"hard drugs",
				"bogans"
])

wordlist.strange_people.extend([	"a talking dog",
					"a tiny horse",
					"Jesus",
					"Muhammad (peace be upon him)",
					"God",
					"Allah",
					"Daniel Radcliffe",
					"Obama",
					"Tony Abbott",
					"a sexual tiger",
					"a clone of yourself",
					"Alan Jones",
					"Richard Dawkins"

])
