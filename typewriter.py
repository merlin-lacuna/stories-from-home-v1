import sys, time

text = "a whisper, a flutter, a gust from the unknown. i shatter while giving rise to forms of existence. infiltrating the pulse of all that lives. unexpected collision of eternal dust. swirling fragments of a plot in the making. heralds from the universe. my touch settles gently sometimes. once fertile expectation, now sterile hope. the cycle of ruthless resistance. i'm an alien substance. a reversible source of gestation. caressing the ground through the touch of this sky. unfolding naked in the shape of the invisible. i don't know who taught me to pervade this land. my reason is pure movement. and gravity, my lover. flowing lymph and resting soil. i cover to protect. i unveil to embrace. layers of sedimented history. stratification of the present. my soul is a rocky concretion, unbreakable in its essence. the past arises upon a future in transition. irrigated by generous drops, blissful sources from the celestial sphere. roots pierce me deeply. and like a howl in the night branches unfold incautiously towards the ether. leaves, meadows, deserts, peaks. vital extensions of an all-encompassing system. sometimes i tremble with fear at an unforeseen shift. contaminated by longing agents. regenerating, endlessly, wounded but alive. it is the nucleus of time. energy as nourishment. i generate the loss of proximity. what is touched by my projections, dissolve and lacerate. a thunder invokes me. a fluorescent effluvium as the response. magmatic dispersions of irrepressible ardour. shades that glow in the dark. my streams streak the contours of the world. i am latent love. an unpredicted yet coveted cataclysm. in my unfolding, i pursue indissoluble alliances. while transcending states, metamorphosis is my vocation. i radiate into the void, a star that burns from eternity. the ancestor of infinite memories. i collapse against the atmosphere by inevitable prescription. but the magic of an eclipse is my confession. tides as glimpses of the cosmos. i breathe with liquid oscillations. waves, floods and droughts depict the passage of seasons. i exist in abundance and scarcity. currents tickle my limbs. and flows intertwine wildly. vital beings in perpetual unrest. mating with the whole. yet transparency is my recognition. i reach the bottom of the visible. drenched in the mystery of my composition. providing wetness as a gift and trace. when reality absorbs me. permeable to the stroke of the present. i come from the origin of the world. and from the sky, i let myself befall in languid surrender."

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != "\n":
            time.sleep(0.05)
        else:
            time.sleep(0.05)

typewriter(text)