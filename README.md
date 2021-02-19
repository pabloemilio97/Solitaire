# Solitaire
Implementation of solitaire encryption algorithm https://www.schneier.com/academic/solitaire/

## Usage
1. Type secret key in txt file
2. Run `python3 solitaire.py`
3. Select encryption or decryption mode
4. Enter message

## Secret key
Start with a deck ordered by value.

The text in `key.txt` will be used as a passphrase to order the inital deck. Use at least 64 characters for security.
For each character in the text, the solitaire algorithm is applied (an additional cut in step 5 is made using the character's value 1-53).


## Algorithm
How does the solitaire algorithm work? Let's use an example:

Initial deck:

    1 2 3 4 ... 52 A B

For each character in the message:

    After the first step (moving the A joker):

        1 2 3 4 ... 52 B A

    After the second step (moving the B joker):

        1 B 2 3 4 ... 52 A

    After the third step (the triple cut):

        B 2 3 4 ... 52 A 1

    After the fourth step (the count cut):

        2 3 4 ... 52 A B 1

    Then register the nth value from top to bottom where n is the value of the top card. A and B are both worth 53.

When you have your keystream, proceed to sum each value to each value of your message. If a sum is greater than 26, subtract 26 from it.

## Decryption
To decrypt an encrypted message, you need to generate the same initial deck as the one used to encrypt it.
Generate the keystream the same way as before, but now subtract the values instead of adding them. If the first number in the operation is lesser than or equal to the second, add 26 to the first one and then subtract.
