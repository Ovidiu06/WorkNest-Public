import datetime
from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from recrutare.models import validator_cnp, Pozitie
from django.utils.translation import gettext_lazy as _


def generator_username(nume, prenume):
    username_de_baza = f'{nume.lower()}.{prenume.lower()}'
    username = username_de_baza
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f'{username_de_baza}{counter}'
        counter += 1
    return username

lista_tari = [('ZA', 'South Africa'), ('AT', 'Austria'), ('IN', 'India'), ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DE', 'Germany'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AN', 'Netherlands Antilles'), ('SA', 'Saudi Arabia'), ('DZ', 'Algeria'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AZ', 'Azerbaijan'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BS', 'Bahamas'), ('BD', 'Bangladesh'), ('BH', 'Bahrain'), ('BB', 'Barbados'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BY', 'Belarus'), ('MM', 'Burma'), ('BO', 'Bolivia'), ('BW', 'Botswana'), ('BR', 'Brazil'), ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BI', 'Burundi'), ('BF', 'Burkina Faso'), ('BT', 'Bhutan'), ('CV', 'Cape Verde'), ('CM', 'Cameroon'), ('KH', 'Cambodia'), ('CA', 'Canada'), ('QA', 'Qatar'), ('KZ', 'Kazakhstan'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CY', 'Cyprus'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo-Brazzaville'), ('CD', 'Congo-Kinshasa'), ('KP', 'North Korea'), ('KR', 'South Korea'), ('CR', 'Costa Rica'), ('CI', 'Ivory Coast'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('EG', 'Egypt'), ('AE', 'United Arab Emirates'), ('EC', 'Ecuador'), ('ER', 'Eritrea'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('EE', 'Estonia'), ('US', 'United States'), ('ET', 'Ethiopia'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('PH', 'Philippines'), ('FI', 'Finland'), ('FR', 'France'), ('GM', 'Gambia'), ('GA', 'Gabon'), ('GH', 'Ghana'), ('GE', 'Georgia'), ('GS', 'South Georgia and the South Sandwich Islands'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GD', 'Grenada'), ('GL', 'Greenland'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GY', 'Guyana'), ('GF', 'French Guiana'), ('GN', 'Guinea'), ('GQ', 'Equatorial Guinea'), ('GW', 'Guinea-Bissau'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('YE', 'Yemen'), ('BV', 'Bouvet Island'), ('NF', 'Norfolk Island'), ('CX', 'Christmas Island'), ('KY', 'Cayman Islands'), ('CK', 'Cook Islands'), ('FK', 'Falkland Islands'), ('HM', 'Heard Island and McDonald Islands'), ('MH', 'Marshall Islands'), ('UM', 'United States Minor Outlying Islands'), ('SB', 'Solomon Islands'), ('TC', 'Turks and Caicos Islands'), ('VI', 'U.S. Virgin Islands'), ('VG', 'British Virgin Islands'), ('CC', 'Cocos Islands'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IS', 'Iceland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('DJ', 'Djibouti'), ('JO', 'Jordan'), ('YU', 'Yugoslavia'), ('KW', 'Kuwait'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('LA', 'Laos'), ('LS', 'Lesotho'), ('LV', 'Latvia'), ('LR', 'Liberia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MX', 'Mexico'), ('MC', 'Monaco'), ('MO', 'Macau'), ('MK', 'Macedonia'), ('MG', 'Madagascar'), ('MY', 'Malaysia'), ('MW', 'Malawi'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MP', 'ds'), ('MA', 'Morocco'), ('MQ', 'Martinique'), ('MU', 'Mauritius'), ('MR', 'Mauritania'), ('YT', 'Mayotte'), ('FM', 'Micronesia'), ('MZ', 'Mozambique'), ('MD', 'Moldova'), ('MN', 'Mongolia'), ('MS', 'Montserrat'), ('NE', 'Niger'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NI', 'Nicaragua'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NO', 'Norway'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('OM', 'Oman'), ('NL', 'Netherlands'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PK', 'Pakistan'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PF', 'French Polynesia'), ('PR', 'Puerto Rico'), ('PT', 'Portugal'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KI', 'Kiribati'), ('RU', 'Russia'), ('GB', 'United Kingdom'), ('CF', 'Central African Republic'), ('CZ', 'Czech Republic'), ('DO', 'Dominican Republic'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('SM', 'San Marino'), ('PM', 'Saint Pierre and Miquelon'), ('ST', 'Sao Tome and Principe'), ('VC', 'Saint Vincent and the Grenadines'), ('SY', 'Syria'), ('SV', 'El Salvador'), ('WS', 'Samoa'), ('AS', 'American Samoa'), ('SH', 'Saint Helena'), ('LC', 'Saint Lucia'), ('EH', 'Western Sahara'), ('SC', 'Seychelles'), ('SN', 'Senegal'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SO', 'Somalia'), ('LK', 'Sri Lanka'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SZ', 'Swaziland'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('TH', 'Thailand'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('IO', 'British Indian Ocean Territory'), ('TF', 'French Southern Territories'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TM', 'Turkmenistan'), ('TR', 'Turkey'), ('TV', 'Tuvalu'), ('UA', 'Ukraine'), ('UG', 'Uganda'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis and Futuna'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')]

class Angajat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    email = models.EmailField()
    telefon = models.CharField(max_length=10)
    cnp = models.CharField(max_length=13, validators=[validator_cnp])


    class ListaActe(models.TextChoices):
        CI = 'ci', _('Carte de identitate')
        PASAPORT = 'pasaport', _('Pasaport')
        CARNET_DE_CONDUCERE = 'carnet_de_conducere', _('Carnet de conducere')


    tip_act = models.CharField(max_length=20, choices=ListaActe.choices, null=True, blank=True, default='ci')
    serie_act = models.CharField(max_length=2, null=True, blank=True)
    numar_act = models.CharField(max_length=20, null=True, blank=True)
    data_eliberat_act = models.DateField(null=True, blank=True)
    act_eliberat_de = models.CharField(max_length=50, null=True, blank=True)
    locul_nasterii = models.CharField(max_length=50, null=True, blank=True)
    stare_civila = models.CharField(max_length=20, choices=[('necasatorit', 'Necasatorit'), ('casatorit', 'Casatorit'), ('divortat', 'Divortat'), ('vaduv', 'Vaduv'), ('nespecificat', 'Nespecificat')], default='nespecificat')
    tara = models.CharField(max_length=50, choices=lista_tari,default='RO')
    judet = models.CharField(max_length=50, null=True, blank=True)
    localitate = models.CharField(max_length=50, null=True, blank=True)
    strada = models.CharField(max_length=50, null=True, blank=True)
    numar_strada = models.CharField(max_length=50, null=True, blank=True)
    bloc = models.CharField(max_length=50, null=True, blank=True)
    scara = models.CharField(max_length=50, null=True, blank=True)
    etaj = models.CharField(max_length=50, null=True, blank=True)
    apartament = models.CharField(max_length=50, null=True, blank=True)
    cv = models.FileField(upload_to='cv-uri/',  null=True, blank=True)
    poza = models.ImageField(upload_to='documente_angajati/', default='documente_angajati/default_profil.jpg')
    data_angajarii = models.DateField(default=now)
    pozitie_angajat = models.ForeignKey(Pozitie, on_delete=models.CASCADE)
    este_manager = models.BooleanField(default=False, verbose_name='Este Manager')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nume} {self.prenume}'

    @property
    def varsta(self):
        if not self.cnp:
            return 'Nespecificat'
        return self.calculeaza_varsta()

    @property
    def sexul(self):
        if not self.cnp:
            return 'Nespecificat'
        return self.calculeaza_sexul()

    @property
    def data_nasterii(self):
        if not self.cnp:
            return 'Nespecificat'
        return self.calculeaza_data_nasterii()

    @property
    def vechime(self):
        if isinstance(self.data_angajarii, datetime.datetime):
            data_angajarii = self.data_angajarii.date()
        else:
            data_angajarii = self.data_angajarii
        data_astazi = date.today()
        if (data_astazi.year - data_angajarii.year - ((data_astazi.month, data_astazi.day) <
                                                      (data_angajarii.month, data_angajarii.day))) <= 0:
            return f'Mai putin de un an'
        else:
            return f'{data_astazi.year - data_angajarii.year - ((data_astazi.month, data_astazi.day) < 
                                                                (data_angajarii.month, data_angajarii.day))}'

    def calculeaza_data_nasterii(self):
        an = int(self.cnp[1:3])
        luna = int(self.cnp[3:5])
        zi = int(self.cnp[5:7])
        secolul = int(self.cnp[0:1])
        if secolul in [1, 2]:
            an += 1900
        elif secolul in [5, 6]:
            an += 2000
        elif secolul in [7, 8]:
            an_curent = str(datetime.date.today().year)
            if an < int(an_curent[2:4]):
                an += 2000
            else:
                an += 1900
        else:
            an += 1800
        return datetime.date(an, luna, zi)

    def calculeaza_sexul(self):
        sex = int(self.cnp[0:1])
        if sex in [1, 5, 7]:
            return f'Masculin'
        elif sex in [2, 4, 8]:
            return f'Feminin'

    def calculeaza_varsta(self):
        an = int(self.cnp[1:3])
        luna = int(self.cnp[3:5])
        zi = int(self.cnp[5:7])
        an_curent = str(datetime.date.today().year)
        if an < int(an_curent[2:4]):
            an += 2000
        else:
            an += 1900
        data_nasterii = datetime.date(an, luna, zi)
        today = datetime.date.today()
        varsta = today.year - data_nasterii.year - ((today.month, today.day) <
                                                    (data_nasterii.month, data_nasterii.day))
        return varsta


class Contract(models.Model):
    nr_contract = models.IntegerField(null=True, blank=True)
    data_contract = models.DateField()
    angajat = models.ForeignKey(Angajat, on_delete=models.CASCADE)
    data_angajare = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    salariu = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class ModelContract(models.TextChoices):
        ZILIERI = 'zilieri', _('Zilieri')
        PERMANENT = 'permanent', _('Permanent')


    class NormaDeLucru(models.TextChoices):
        NORMA_INTREAGA = 'norma_intreaga', _('Norma Intreaga (8h)')
        JUMATATE_DE_NORMA = 'jumatate_de_norma', _('Jumatate de norma (4h)')


    class TipContract(models.TextChoices):
        DETERMINAT = 'determinat', _('Determinat')
        NEDETERMINAT = 'nedeterminat', _('Nedeterminat')


    class ModDeLucru(models.TextChoices):
        BIROU = 'birou', _('Birou')
        HIBRID = 'hibrid', _('Hibrid')
        REMOTE = 'remote', _('Remote')

    model_contract = models.CharField(max_length=50, choices=ModelContract.choices, default=ModelContract.PERMANENT)
    norma_de_lucru = models.CharField(max_length=50, choices=NormaDeLucru.choices, default=NormaDeLucru.NORMA_INTREAGA, help_text=_('Selectati norma de lucru'))
    tip_contract = models.CharField(max_length=50, choices=TipContract.choices, default=TipContract.NEDETERMINAT, help_text=_('Selectati tipul contractului'))
    mod_de_lucru = models.CharField(max_length=50, choices=ModDeLucru.choices, default=ModDeLucru.BIROU, help_text=_('Selectati modul de lucru'))
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.angajat} - {self.mod_de_lucru} ({self.tip_contract})'


class Document(models.Model):
    angajat = models.ForeignKey('Angajat', on_delete=models.CASCADE)
    tip_document = models.CharField(max_length=100, help_text='Introduceti tipul documentului (ex: CI, contract, diploma etc.)')
    data_incarcare_document = models.DateField(auto_now_add=True)
    document = models.FileField(upload_to='documente_angajati/')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.tip_document} pentru {self.angajat} ({self.data_incarcare_document})'


class StatisticaAngajare(models.Model):
    angajat = models.ForeignKey(Angajat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_ora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.angajat} - {self.data_ora}'


class StatisticaAdaugareDocumente(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    angajat = models.ForeignKey(Angajat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_ora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.document}'

