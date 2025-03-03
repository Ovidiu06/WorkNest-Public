from django.contrib.auth.models import Group, User
from django.db import models
import datetime
import mimetypes
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from statistici.models import CoduriCOR


def validare_fisier_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Sunt permise doar fisiere de tip PDF.')
    mime_type, _ = mimetypes.guess_type(value.name)
    if mime_type != 'application/pdf':
        raise ValidationError('Fisier Invalid. Sunt permise doar fisiere de tip PDF.')

def validator_cnp(cnp):
    numar_verificare = "279146358279"

    judet = {"01": "Alba", "02": "Arad", "03": "Argeș", "04": "Bacău", "05": "Bihor", "06": "Bistrița-Năsăud",
             "07": "Botoșani", "08": "Brasov", "09": "Brăila", "10": "Buzău", "11": "Caraș-Severin", "12": "Cluj",
             "13": "Constanța", "14": "Covasna", "15": "Dâmbovița", "16": "Dolj", "17": "Galați", "18": "Gorj",
             "19": "Harghita", "20": "Hunedoara", "21": "Ialomița", "22": "Iași", "23": "Ilfov", "24": "Maramureș",
             "25": "Mehedinți", "26": "Mureș", "27": "Neamț", "28": "Olt", "29": "Prahova", "30": "Satu Mare",
             "31": "Sălaj", "32": "Sibiu", "33": "Suceava", "34": "Teleorman", "35": "Timiș", "36": "Tulcea",
             "37": "Vaslui", "38": "Vâlcea", "39": "Vrancea", "40": "București", "41": "București - Sector 1",
             "42": "București - Sector 2", "43": "București - Sector 3", "44": "București - Sector 4",
             "45": "București - Sector 5", "46": "București - Sector 6", "51": "Călărași", "52": "Giurgiu",
             "47": "Bucuresti - Sector 7 (desființat)", "48": "Bucuresti - Sector 8 (desființat)",
             "70": "'judet universal"}

    luna = {"01": "Ianuarie", "02": "Februarie", "03": "Martie", "04": "Aprilie", "05": "Mai", "06": "Iunie",
            "07": "Iulie", "08": "August", "09": "Septembrie", "10": "Octombrie", "11": "Noiembrie",
            "12": "Decembrie"}

    zile = (
        "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18",
        "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")

    if not cnp.isdigit():
        return False
    elif not len(cnp) == 13:
        return False
    elif cnp[0] == "0":
        return False
    elif cnp[3:5] not in luna.keys():
        return False
    elif cnp[5:7] not in zile:
        return False
    elif cnp[7:9] not in judet.keys():
        return False
    elif int(cnp[12]) in range(0, 10):
        modulo = (((int(cnp[0])) * int(numar_verificare[0]) + (int(cnp[1])) * int(numar_verificare[1]) + (
            int(cnp[2])) * int(numar_verificare[2]) + (int(cnp[3])) * int(numar_verificare[3]) + (
                       int(cnp[4])) * int(numar_verificare[4]) + (int(cnp[5])) * int(numar_verificare[5]) + (
                       int(cnp[6])) * int(numar_verificare[6]) + (int(cnp[7])) * int(numar_verificare[7]) + (
                       int(cnp[8])) * int(numar_verificare[8]) + (int(cnp[9])) * int(numar_verificare[9]) + (
                       int(cnp[10])) * int(numar_verificare[10]) + (int(cnp[11])) * int(numar_verificare[11])) % 11)
        if modulo == 10:
            modulo = 1
            if int(cnp[12]) == modulo:
                return True
            else:
                return False
        elif int(cnp[12]) == modulo:
            return True
        else:
            return False
    else:
        return False


class Companie(models.Model):
    nume = models.CharField(max_length=100)

    def __str__(self):
        return self.nume


class Departament(models.Model):
    nume = models.CharField(max_length=50, verbose_name='Departament')
    manager_group = models.OneToOneField(Group, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nume


class Oras(models.Model):
    nume = models.CharField(max_length=50, verbose_name='Oras')

    def __str__(self):
        return self.nume


class Pozitie(models.Model):
    nume = models.CharField(max_length=50)
    departament = models.ForeignKey('Departament', on_delete=models.CASCADE)
    oras = models.ForeignKey('Oras', on_delete=models.SET_NULL, null=True, blank=True)
    cod_COR = models.ForeignKey(CoduriCOR, max_length=6, on_delete=models.SET_NULL, null=True, blank=True)
    tip_contract = models.CharField(max_length=50, choices=[('determinat', 'Determinat'), ('nedeterminat', 'Nedeterminat')], default='nedeterminat')
    mod_de_lucru = models.CharField(max_length=50, choices=[('birou', 'Birou'), ('hibrid', 'Hibrid'), ('remote', 'Remote')], default='birou')
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.active:
            return f'{self.nume} / {self.oras} / {self.departament}'
        else:
            return f'{self.nume} / {self.oras} / {self.departament} / Proces de recrutare oprit!'


class Candidat(models.Model):
    nume = models.CharField(max_length=50)
    prenume = models.CharField(max_length=50)
    email = models.EmailField()
    numar_telefon = models.CharField(max_length=10)
    CNP = models.CharField(max_length=13, null=True, blank=True)
    judet_candidat = models.CharField(max_length=50, null=True, blank=True)
    localitate_candidat = models.CharField(max_length=50, null=True, blank=True)
    stare_civila = models.CharField(max_length=20, choices=[('necasatorit', 'Necasatorit'), ('casatorit', 'Casatorit'),
                                                            ('divortat', 'Divortat'), ('vaduv', 'Vaduv'),
                                                            ('nespecificat', 'Nespecificat')])
    pozitie_aplicata = models.ForeignKey('Pozitie', on_delete=models.CASCADE)
    cv = models.FileField(upload_to='cv-uri/', validators=[validare_fisier_pdf])
    poza = models.ImageField(upload_to='poze_candidati/', default='poze_candidati/default.png')
    data_aplicarii = models.DateField(auto_now_add=True)


    class StatusChoices(models.TextChoices):
        APLICAT = 'aplicat', _('Aplicat')
        INTERVIU = 'interviu', _('Interviu')
        RESPINS = 'respins', _('Respins')
        APROBAT = 'aprobat', _('Aprobat')


    status = models.CharField(max_length=50, choices=StatusChoices.choices, default='aplicat')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nume} {self.prenume}'

    @property
    def varsta(self):
        if not self.CNP:
            return 'Nespecificat'
        return self.calculeaza_varsta()

    @property
    def sexul_candidatului(self):
        if not self.CNP:
            return 'Nespecificat'
        return self.calculeaza_sexul()

    def calculeaza_sexul(self):
        sex = int(self.CNP[0:1])
        if sex in [1, 5, 7]:
            return f'Masculin'
        elif sex in [2, 4, 8]:
            return f'Feminin'

    def calculeaza_varsta(self):
        an = int(self.CNP[1:3])
        luna = int(self.CNP[3:5])
        zi = int(self.CNP[5:7])
        an_curent = str(datetime.date.today().year)
        if an < int(an_curent[2:4]):
            an += 2000
        else:
            an += 1900
        data_nasterii = datetime.date(an, luna, zi)
        today = datetime.date.today()
        varsta = today.year - data_nasterii.year - ((today.month, today.day) < (data_nasterii.month, data_nasterii.day))
        return varsta


class Logs(models.Model):
    alegeri_actiunea = (('creat', 'Creat'),
                      ('modificat', 'Modificat'),
                      ('refresh', 'Refresh'),
                      ('reactivare', 'Reactivare'),
                      ('stergere', 'Stergere'))
    creat_la = models.DateTimeField(auto_now_add=True, blank=True)
    modificat_la = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    actiunea = models.CharField(max_length=10, choices=alegeri_actiunea)
    url = models.CharField(max_length=150)


class StatisticaAdaugareCandidati(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    candidat = models.ForeignKey('Candidat', on_delete=models.SET_NULL, null=True, blank=True)
    data_ora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.candidat} - {self.data_ora}'


class Interviu(models.Model):
    candidat = models.ForeignKey('Candidat', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    data_interviu = models.DateField()
    ora_interviu = models.TimeField()
    creat_la = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Interviu cu {self.candidat} pe {self.data_interviu} la {self.ora_interviu}'

    def save(self, *args, **kwargs):
        if not self.manager and self.candidat:
            departament = self.candidat.pozitie_aplicata.departament
            group_name = f'Manager {departament.nume}'
            manager_group = Group.objects.filter(name=group_name).first()
            if manager_group:
                self.manager = User.objects.filter(groups=manager_group).first()
        super().save(*args, **kwargs)
