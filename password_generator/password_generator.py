from string import ascii_letters, digits, punctuation
import random
import math

cyrillic = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
greek = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
arabic = 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'
hebrew = 'אבגדהוזחטיכלמנסעפצקרשת'
devanagari = 'अआइईउऊऋएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह'
chinese_simplified = '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百做结斯消还言男边真装等五快观广间白动展己府受期支防技使领局什质该支原铁不流从老员影战按土增术又列最打外越东则量准选标突查知活米口整八文际克号压长权儿她星第条持象红变风标周布约声连则黄政段继群九且采持每叫局类划调广整热安千村叫验万件科东示重山击效布款设规'
japanese_hiragana = 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん'
japanese_katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'


additional_characters = (
    cyrillic +
    greek +
    arabic +
    hebrew +
    devanagari +
    chinese_simplified +
    japanese_hiragana +
    japanese_katakana
)

unicode_all_characters = ascii_letters + digits + punctuation + additional_characters

def calculate_entropy(n, charset_size):
    return n * math.log2(charset_size)


def password_unicode_supported(specified_length=None, min_entropy=80):
    charset_size = len(unicode_all_characters)
    n = 5 if specified_length is None else specified_length
    entropy = calculate_entropy(n, charset_size)

    if specified_length is not None and entropy < min_entropy:
        print(f"\nSpecified length of {specified_length} characters does not meet the minimum entropy requirement of {min_entropy} bits.\n")
        n = math.ceil(min_entropy / math.log2(charset_size))
        print(f"Adjusting password length to {n} characters to meet the entropy requirement.\n")

    while entropy < min_entropy:
        n += 1
        entropy = calculate_entropy(n, charset_size)

    lowercase_letters = ascii_letters[:26]
    uppercase_letters = ascii_letters[26:]

    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(punctuation),
        random.choice(additional_characters)
    ]

    for _ in range(n - 5):
        password.append(random.choice(unicode_all_characters))

    random.shuffle(password)

    return ''.join(password), entropy

def password_ascii_only(specified_length=None, min_entropy=80):
    charset_size = len(ascii_letters + digits + punctuation)
    n = 4 if specified_length is None else specified_length
    entropy = calculate_entropy(n, charset_size)

    if specified_length is not None and entropy < min_entropy:
        print(f"\nSpecified length of {specified_length} characters does not meet the minimum entropy requirement of {min_entropy} bits.\n")
        n = math.ceil(min_entropy / math.log2(charset_size))
        print(f"Adjusting password length to {n} characters to meet the entropy requirement.\n")

    while entropy < min_entropy:
        n += 1
        entropy = calculate_entropy(n, charset_size)

    lowercase_letters = ascii_letters[:26]
    uppercase_letters = ascii_letters[26:]
    ascii_all_characters = ascii_letters + digits + punctuation

    password = [
        random.choice(lowercase_letters),
        random.choice(uppercase_letters),
        random.choice(digits),
        random.choice(punctuation)
    ]

    for _ in range(n - 4):
        password.append(random.choice(ascii_all_characters))

    random.shuffle(password)

    return ''.join(password), entropy

def main():
    choice = input("Choose password type: ASCII (1) or Unicode (2): ").strip()
    
    try:
        specified_length = input("Enter the desired password length (or press Enter to auto-generate based on entropy): ").strip()
        specified_length = int(specified_length) if specified_length else None

        if choice == '1':
            pwd, entropy = password_ascii_only(specified_length=specified_length, min_entropy=80)
            print(f"\nGenerated ASCII password: {pwd}\n")
            print(f"Password entropy: {entropy:.2f} bits\n")
        elif choice == '2':
            pwd, entropy = password_unicode_supported(specified_length=specified_length, min_entropy=80)
            print(f"\nGenerated Unicode password: {pwd}\n")
            print(f"Password entropy: {entropy:.2f} bits\n")
        else:
            print("\nInvalid choice. Please enter 1 for ASCII or 2 for Unicode.\n")
    except ValueError:
        print("\nInvalid input. Please enter numeric values for the password length.\n")

if __name__ == "__main__":
    main()
