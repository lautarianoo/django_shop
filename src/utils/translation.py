letters = {'ь':'', 'ъ':'', 'а':'a', 'б':'b','в':'v',
       'г':'g', 'д':'d', 'е':'e', 'ё':'yo','ж':'zh',
       'з':'z', 'и':'i', 'й':'y', 'к':'k', 'л':'l',
       'м':'m', 'н':'n', 'о':'o', 'п':'p', 'р':'r',
       'с':'s', 'т':'t', 'у':'u', 'ф':'f', 'х':'h',
       'ц':'ts', 'ч':'ch', 'ш':'sh', 'щ':'sch', 'ы':'yi',
       'э':'e', 'ю':'yu', 'я':'ya', " ": "-", "/": "-", "|": "-", "[": "-",
        ']': "-", "{": "-", "'": "-", '"': "-", "+": "-", "(": "-", ")": "-", "=": "-", "_": "-"
        , ",": "-", ".": "-"}


def russian_to_engilsh(text):
    new_text = ''
    text.lower()
    english_letters = list('qwertyuiopasdfghjklzxcvbnm')
    digits = list("0123456789")
    for letter in list(text):
        if letter in english_letters or letter in digits:
            new_text += letter
            continue
        if letters.get(letter):
            new_text += letters.get(letter)
            continue
        new_text += "-"
    return new_text