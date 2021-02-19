import string
DECK_LENGTH = 54
JOKER_VALUE = 53
sorted_deck = [x for x in range(1,DECK_LENGTH - 1)] + ["A", "B"] 
alphabet_values = dict(zip(string.ascii_uppercase, [i for i in range(1,27)]))
alphabet_values_flipped = dict(zip([i for i in range(1,27)], string.ascii_uppercase))


def sanitize(text):
    s = "".join(c.upper() for c in text if c.isalpha())
    return s

def read_key():
    with open("key.txt") as f:
        k = f.read()
    return k

def text_to_values(text):
    text = sanitize(text)
    text_values = [alphabet_values[char] for char in text]
    return text_values


def deck_value(index, deck):
    value = deck[index]
    if type(value) is str:
        value = JOKER_VALUE
    return value

def count_cut(count, deck):
    cut = deck[:count]
    rest = deck[count:-1]
    last = deck[-1:]
    deck = rest + cut + last
    return deck

def solitaire(deck):
    """
    Steps 1-4
    """
    def move_joker(steps, joker, deck):
        """
        Return modified deck and new position of joker
        """
        deck = deck.copy()
        joker_index = deck.index(joker)
        joker_index_insert = (joker_index + steps) % DECK_LENGTH
        deck.pop(joker_index)
        deck.insert(joker_index_insert, joker)
        joker_index = joker_index_insert
        return deck, joker_index

    # Step 1: Find A joker, switch position with card after it
    deck, a_joker = move_joker(1, "A", deck)
    
    # Step 2: Find B joker, put card 2 cards after it 
    deck, b_joker = move_joker(2, "B", deck)
    
    # Step 3: Triple cut
    first_joker = min(a_joker, b_joker)
    last_joker = max(a_joker, b_joker)
    upper_portion = deck[:first_joker]
    in_between = deck[first_joker:last_joker+1]
    lower_portion = [] if last_joker == DECK_LENGTH - 1 else deck[last_joker+1:]
    deck = lower_portion + in_between + upper_portion

    # Step 4: Count cut
    deck = count_cut(deck_value(-1, deck), deck)

    return deck

def initiate_deck():
    key_values = text_to_values(read_key())
    deck = sorted_deck.copy()
    
    for key_value in key_values:
        deck = solitaire(deck)
        # Step 5: Extra count cut
        deck = count_cut(key_value, deck)
    return deck

def add_modulo_26(a, b):
    s = a + b
    if s > 26:
        s -= 26
    return s

def subtract_modulo_26(a, b):
    if a <= b:
        a += 26
    s = a - b
    return s

def modulo_26(a):
    if a > 26:
        a -= 26
    return a

def crypt(message, func):
    """
    message: message to encrypt or decrypt
    func: add or subtract function
    """
    deck = initiate_deck()
    message_values = text_to_values(message)
    keystream = []

    for _ in message_values:
        candidate = ""
        while type(candidate) is str:
            deck = solitaire(deck)
            candidate = modulo_26(deck[deck_value(0, deck)])
        keystream.append(candidate)
    for i in range(len(keystream)):
        keystream[i] = func(message_values[i], keystream[i])
    keystream = [alphabet_values_flipped[value] for value in keystream]

    return "".join(keystream)

def run():
    mode = input("Encrypt (E) or Decrypt (D)? : ")
    message = input("What is your message? : ")
    if mode == "D":
        answer = crypt(message, subtract_modulo_26)
    else:
        answer = crypt(message, add_modulo_26)
    print(answer)
    return answer

run()

