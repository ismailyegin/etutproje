import enum


class EnumFields(enum.Enum):
    class LEVELTYPE2(enum.Enum):
        VISA = 1
        GRADE = 2
        BELT = 3

    class LEVELTYPECOACH(enum.Enum):
        VISA = 1
        GRADE = 2

    class BRANCH2(enum.Enum):
        TAOLU = 1
        SANDA = 2
        WUSHU = 3

    class COMPSTATUS(enum.Enum):
        PREREGISTRATIONOPEN = 1
        PREREGISTRATIONCLOSED = 2
        COMPLETED = 3

    class COMPTYPE(enum.Enum):
        NATIONAL = 1
        INTERNATIONAL = 2

    WUSHU = 'WUSHU'
    AIKIDO = 'AIKIDO'
    WINGCHUN = 'WING CHUN'
    KYOKUSHIN = 'KYOKUSHIN ASHIHARA'
    JEETKUNEDO = 'JEET KUNE DO KULELKAVIDO'

    BRANCH = (
        (AIKIDO, 'AIKIDO'),
        (WINGCHUN, 'WING CHUN'),
        (WUSHU, 'WUSHU'),
        (KYOKUSHIN, 'KYOKUSHIN ASHIHARA'),
        (JEETKUNEDO, 'JEET KUNE DO KULELKAVIDO'),
    )

    SANDA = 'SANDA'
    TAOLU = 'TAOLU'

    SUBBRANCH = (
        (SANDA, 'SANDA'),
        (TAOLU, 'TAOLU'),
    )


    VISA = 'VISA'
    GRADE = 'GRADE'
    BELT = 'BELT'

    LEVELTYPE = (
        (VISA, 'VISA'),
        (GRADE, 'GRADE'),
        (BELT, 'BELT'),

    )
