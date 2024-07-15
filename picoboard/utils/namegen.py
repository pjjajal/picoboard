"""
This is a simple mnemonic word generator, with naming borrowed from Urbit.

Urbit uses a mnuemonic naming system for stars, planets, and galaxies, with each being
composed of a prefix and suffix. 

This generator uses a 4 syllable prefix and suffix to generate unique names. 
This is identical to the naming of Urbit planets, i.e., composed of [prefix][suffix]-[prefix][suffix].

References:
    - Urbit Naming Source: https://github.com/urbit/urbit-ob/blob/master/src/internal/co.js
    - Urbit Address Space: https://urbit.org/blog/the-urbit-address-space
    - Azimuth 1: https://davis68.github.io/martian-computing/lessons/lesson02-azimuth-1.html
"""

import random

PREFIX = """\
dozmarbinwansamlitsighidfidlissogdirwacsabwissib\
rigsoldopmodfoglidhopdardorlorhodfolrintogsilmir\
holpaslacrovlivdalsatlibtabhanticpidtorbolfosdot\
losdilforpilramtirwintadbicdifrocwidbisdasmidlop\
rilnardapmolsanlocnovsitnidtipsicropwitnatpanmin\
ritpodmottamtolsavposnapnopsomfinfonbanmorworsip\
ronnorbotwicsocwatdolmagpicdavbidbaltimtasmallig\
sivtagpadsaldivdactansidfabtarmonranniswolmispal\
lasdismaprabtobrollatlonnodnavfignomnibpagsopral\
bilhaddocridmocpacravripfaltodtiltinhapmicfanpat\
taclabmogsimsonpinlomrictapfirhasbosbatpochactid\
havsaplindibhosdabbitbarracparloddosbortochilmac\
tomdigfilfasmithobharmighinradmashalraglagfadtop\
mophabnilnosmilfopfamdatnoldinhatnacrisfotribhoc\
nimlarfitwalrapsarnalmoslandondanladdovrivbacpol\
laptalpitnambonrostonfodponsovnocsorlavmatmipfip\
"""

SUFFIX = """\
zodnecbudwessevpersutletfulpensytdurwepserwylsun\
rypsyxdyrnuphebpeglupdepdysputlughecryttyvsydnex\
lunmeplutseppesdelsulpedtemledtulmetwenbynhexfeb\
pyldulhetmevruttylwydtepbesdexsefwycburderneppur\
rysrebdennutsubpetrulsynregtydsupsemwynrecmegnet\
secmulnymtevwebsummutnyxrextebfushepbenmuswyxsym\
selrucdecwexsyrwetdylmynmesdetbetbeltuxtugmyrpel\
syptermebsetdutdegtexsurfeltudnuxruxrenwytnubmed\
lytdusnebrumtynseglyxpunresredfunrevrefmectedrus\
bexlebduxrynnumpyxrygryxfeptyrtustyclegnemfermer\
tenlusnussyltecmexpubrymtucfyllepdebbermughuttun\
bylsudpemdevlurdefbusbeprunmelpexdytbyttyplevmyl\
wedducfurfexnulluclennerlexrupnedlecrydlydfenwel\
nydhusrelrudneshesfetdesretdunlernyrsebhulryllud\
remlysfynwerrycsugnysnyllyndyndemluxfedsedbecmun\
lyrtesmudnytbyrsenwegfyrmurtelreptegpecnelnevfes\
"""


PREFIX = [PREFIX[i : i + 3] for i in range(0, len(PREFIX), 3)]
SUFFIX = [SUFFIX[i : i + 3] for i in range(0, len(SUFFIX), 3)]


def name_generator(syllables: int = 4) -> str:
    assert syllables > 0, "Syllables must be a positive integer."
    assert syllables % 2 == 0 or syllables == 1, "Syllables > 1 must be a multiple of 2."
    if syllables == 1:
        return f"{random.choice(SUFFIX)}"
    return "-".join([f"{random.choice(PREFIX)}{random.choice(SUFFIX)}" for _ in range(syllables // 2)])