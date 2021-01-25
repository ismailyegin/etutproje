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

    HALTER = 'HALTER'


    BRANCH = (
        (HALTER, 'HALTER'),

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

    CIK = 'Ceza İnfaz Kurumu'
    AB = 'Adalet Binası'
    AT = 'Adli Tıp'
    BAM = 'Bölge Adliye Mahkemesi'
    BIM = 'Bölge İdare Mahkemesi'
    DS = 'Denetimli Serbestlik'
    PEM = 'Personel Eğitim Merkezi'
    BB = 'Bakanlık Binası'
    LOJMAN = 'Lojman'
    SOS = "SOSYAL TESİS "
    HAK = "HAKİM EVİ"

    DIGER = 'Diğer'

    TAHSİS_AMACİ = (
        (CIK, 'Ceza İnfaz Kurumu'),
        (AB, 'Adalet Binası'),
        (AT, 'Adli Tıp'),
        (BAM, 'Bölge Adliye Mahkemesi'),
        (BIM, 'Bölge İdare Mahkemesi'),
        (DS, 'Denetimli Serbestlik'),
        (BB, 'Bakanlık Bİnası'),
        (PEM, 'Personel Eğitim Merkezi'),
        (LOJMAN, 'Lojman'),

        (SOS, 'Sosyal Tesis'),
        (HAK, 'Hakim Evi'),
        (DIGER, 'Diğer'),
    )

    D1 = "1.DERECE"
    D2 = "2.DERECE"
    D3 = "3.DERECE"
    D4 = "4.DERECE"
    D5 = "5.DERECE"

    DEPREM_DERECE = (

        (D1, '1.DERECE'),
        (D2, '2.DERECE'),
        (D3, '3.DERECE'),
        (D4, '4.DERECE'),
        (D5, '5.DERECE'),

    )

    B1 = "1.BÖLGE"
    B2 = "2.BÖLGE"
    B3 = "3.BÖLGE"
    B4 = "4.BÖLGE"
    B5 = "5.BÖLGE"

    Yargi_bolgesi = (

        (B1, '1.BÖLGE'),
        (B2, '2.BÖLGE'),
        (B3, '3.BÖLGE'),
        (B4, '4.BÖLGE'),
        (B5, '5.BÖLGE'),
    )


