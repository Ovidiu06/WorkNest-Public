# Generated by Django 5.1.6 on 2025-03-09 11:44

import django.utils.timezone
import recrutare.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Angajat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nume', models.CharField(max_length=50)),
                ('prenume', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('telefon', models.CharField(max_length=10)),
                ('cnp', models.CharField(max_length=13, validators=[recrutare.models.validator_cnp])),
                ('tip_act', models.CharField(blank=True, choices=[('ci', 'Carte de identitate'), ('pasaport', 'Pasaport'), ('carnet_de_conducere', 'Carnet de conducere')], default='ci', max_length=20, null=True)),
                ('serie_act', models.CharField(blank=True, max_length=2, null=True)),
                ('numar_act', models.CharField(blank=True, max_length=20, null=True)),
                ('data_eliberat_act', models.DateField(blank=True, null=True)),
                ('act_eliberat_de', models.CharField(blank=True, max_length=50, null=True)),
                ('locul_nasterii', models.CharField(blank=True, max_length=50, null=True)),
                ('stare_civila', models.CharField(choices=[('necasatorit', 'Necasatorit'), ('casatorit', 'Casatorit'), ('divortat', 'Divortat'), ('vaduv', 'Vaduv'), ('nespecificat', 'Nespecificat')], default='nespecificat', max_length=20)),
                ('tara', models.CharField(choices=[('ZA', 'South Africa'), ('AT', 'Austria'), ('IN', 'India'), ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DE', 'Germany'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AN', 'Netherlands Antilles'), ('SA', 'Saudi Arabia'), ('DZ', 'Algeria'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AZ', 'Azerbaijan'), ('BE', 'Belgium'), ('BA', 'Bosnia and Herzegovina'), ('BS', 'Bahamas'), ('BD', 'Bangladesh'), ('BH', 'Bahrain'), ('BB', 'Barbados'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BY', 'Belarus'), ('MM', 'Burma'), ('BO', 'Bolivia'), ('BW', 'Botswana'), ('BR', 'Brazil'), ('BN', 'Brunei'), ('BG', 'Bulgaria'), ('BI', 'Burundi'), ('BF', 'Burkina Faso'), ('BT', 'Bhutan'), ('CV', 'Cape Verde'), ('CM', 'Cameroon'), ('KH', 'Cambodia'), ('CA', 'Canada'), ('QA', 'Qatar'), ('KZ', 'Kazakhstan'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CY', 'Cyprus'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo-Brazzaville'), ('CD', 'Congo-Kinshasa'), ('KP', 'North Korea'), ('KR', 'South Korea'), ('CR', 'Costa Rica'), ('CI', 'Ivory Coast'), ('HR', 'Croatia'), ('CU', 'Cuba'), ('DK', 'Denmark'), ('DM', 'Dominica'), ('EG', 'Egypt'), ('AE', 'United Arab Emirates'), ('EC', 'Ecuador'), ('ER', 'Eritrea'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('ES', 'Spain'), ('EE', 'Estonia'), ('US', 'United States'), ('ET', 'Ethiopia'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('PH', 'Philippines'), ('FI', 'Finland'), ('FR', 'France'), ('GM', 'Gambia'), ('GA', 'Gabon'), ('GH', 'Ghana'), ('GE', 'Georgia'), ('GS', 'South Georgia and the South Sandwich Islands'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GD', 'Grenada'), ('GL', 'Greenland'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GY', 'Guyana'), ('GF', 'French Guiana'), ('GN', 'Guinea'), ('GQ', 'Equatorial Guinea'), ('GW', 'Guinea-Bissau'), ('HT', 'Haiti'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('YE', 'Yemen'), ('BV', 'Bouvet Island'), ('NF', 'Norfolk Island'), ('CX', 'Christmas Island'), ('KY', 'Cayman Islands'), ('CK', 'Cook Islands'), ('FK', 'Falkland Islands'), ('HM', 'Heard Island and McDonald Islands'), ('MH', 'Marshall Islands'), ('UM', 'United States Minor Outlying Islands'), ('SB', 'Solomon Islands'), ('TC', 'Turks and Caicos Islands'), ('VI', 'U.S. Virgin Islands'), ('VG', 'British Virgin Islands'), ('CC', 'Cocos Islands'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IS', 'Iceland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('DJ', 'Djibouti'), ('JO', 'Jordan'), ('YU', 'Yugoslavia'), ('KW', 'Kuwait'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('LA', 'Laos'), ('LS', 'Lesotho'), ('LV', 'Latvia'), ('LR', 'Liberia'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MX', 'Mexico'), ('MC', 'Monaco'), ('MO', 'Macau'), ('MK', 'Macedonia'), ('MG', 'Madagascar'), ('MY', 'Malaysia'), ('MW', 'Malawi'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MP', 'ds'), ('MA', 'Morocco'), ('MQ', 'Martinique'), ('MU', 'Mauritius'), ('MR', 'Mauritania'), ('YT', 'Mayotte'), ('FM', 'Micronesia'), ('MZ', 'Mozambique'), ('MD', 'Moldova'), ('MN', 'Mongolia'), ('MS', 'Montserrat'), ('NE', 'Niger'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NI', 'Nicaragua'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NO', 'Norway'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('OM', 'Oman'), ('NL', 'Netherlands'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PK', 'Pakistan'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PF', 'French Polynesia'), ('PR', 'Puerto Rico'), ('PT', 'Portugal'), ('KE', 'Kenya'), ('KG', 'Kyrgyzstan'), ('KI', 'Kiribati'), ('RU', 'Russia'), ('GB', 'United Kingdom'), ('CF', 'Central African Republic'), ('CZ', 'Czech Republic'), ('DO', 'Dominican Republic'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('SM', 'San Marino'), ('PM', 'Saint Pierre and Miquelon'), ('ST', 'Sao Tome and Principe'), ('VC', 'Saint Vincent and the Grenadines'), ('SY', 'Syria'), ('SV', 'El Salvador'), ('WS', 'Samoa'), ('AS', 'American Samoa'), ('SH', 'Saint Helena'), ('LC', 'Saint Lucia'), ('EH', 'Western Sahara'), ('SC', 'Seychelles'), ('SN', 'Senegal'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SO', 'Somalia'), ('LK', 'Sri Lanka'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SZ', 'Swaziland'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('TH', 'Thailand'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania'), ('IO', 'British Indian Ocean Territory'), ('TF', 'French Southern Territories'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TM', 'Turkmenistan'), ('TR', 'Turkey'), ('TV', 'Tuvalu'), ('UA', 'Ukraine'), ('UG', 'Uganda'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VA', 'Vatican City'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis and Futuna'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], default='RO', max_length=50)),
                ('judet', models.CharField(blank=True, max_length=50, null=True)),
                ('localitate', models.CharField(blank=True, max_length=50, null=True)),
                ('strada', models.CharField(blank=True, max_length=50, null=True)),
                ('numar_strada', models.CharField(blank=True, max_length=50, null=True)),
                ('bloc', models.CharField(blank=True, max_length=50, null=True)),
                ('scara', models.CharField(blank=True, max_length=50, null=True)),
                ('etaj', models.CharField(blank=True, max_length=50, null=True)),
                ('apartament', models.CharField(blank=True, max_length=50, null=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cv-uri/')),
                ('poza', models.ImageField(default='documente_angajati/default_profil.jpg', upload_to='documente_angajati/')),
                ('data_angajarii', models.DateField(default=django.utils.timezone.now)),
                ('este_manager', models.BooleanField(default=False, verbose_name='Este Manager')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nr_contract', models.IntegerField(blank=True, null=True)),
                ('data_contract', models.DateField()),
                ('data_angajare', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('salariu', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('model_contract', models.CharField(choices=[('zilieri', 'Zilieri'), ('permanent', 'Permanent')], default='permanent', max_length=50)),
                ('norma_de_lucru', models.CharField(choices=[('norma_intreaga', 'Norma Intreaga (8h)'), ('jumatate_de_norma', 'Jumatate de norma (4h)')], default='norma_intreaga', help_text='Selectati norma de lucru', max_length=50)),
                ('tip_contract', models.CharField(choices=[('determinat', 'Determinat'), ('nedeterminat', 'Nedeterminat')], default='nedeterminat', help_text='Selectati tipul contractului', max_length=50)),
                ('mod_de_lucru', models.CharField(choices=[('birou', 'Birou'), ('hibrid', 'Hibrid'), ('remote', 'Remote')], default='birou', help_text='Selectati modul de lucru', max_length=50)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip_document', models.CharField(help_text='Introduceti tipul documentului (ex: CI, contract, diploma etc.)', max_length=100)),
                ('data_incarcare_document', models.DateField(auto_now_add=True)),
                ('document', models.FileField(upload_to='documente_angajati/')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticaAdaugareDocumente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ora', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StatisticaAngajare',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ora', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
