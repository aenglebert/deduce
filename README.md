# DeduceD: Belgian (french & dutch) adaptation of the Deduce tool (de-identification method for Dutch medical text)

> The original Deduce repository by [Menger et al can be found here](https://github.com/vmenger/deduce)

This project contains a french & dutch belgian adaptation of Deduce (de-identification method for Dutch medical text)

1. Person names, including initials
2. Geographical locations smaller than a country
3. Names of institutions that are related to patient treatment
4. Dates
5. Ages
6. Patient numbers
7. Telephone numbers
8. E-mail addresses and URLs

The details of the development and workings of the initial method by Menger et al, and its validation can be found in:
[Menger, V.J., Scheepers, F., van Wijk, L.M., Spruit, M. (2017). DEDUCE: A pattern matching method for automatic de-identification of Dutch medical text, Telematics and Informatics, 2017, ISSN 0736-5853](http://www.sciencedirect.com/science/article/pii/S0736585316307365)

### Prerequisites

* `nltk`

### Installing

Installing can be done through pip and git: 

``` python
>>> pip install deduce
```

Or from source, simply download and use python to install:

``` python
>>> python setup.py install
```

## Getting started

The package has a method for annotating (`annotate_text`) and for removing the annotations (`deidentify_annotations`).

``` python

import deduce 

deduce.annotate_text(
        text,                       # The text to be annotated
        patient_first_names="",     # First names (separated by whitespace)
        patient_initials="",        # Initial
        patient_surname="",         # Surname(s)
        patient_given_name="",      # Given name
        patient_id="",              # Patient identification number
        names=True,                 # Person names, including initials
        locations=True,             # Geographical locations
        institutions=True,          # Institutions
        dates=True,                 # Dates
        ages=True,                  # Ages
        patient_numbers=True,       # Patient numbers
        phone_numbers=True,         # Phone numbers
        urls=True,                  # Urls and e-mail addresses
        flatten=True                # Debug option
    )    
    
deduce.deidentify_annotations(
        text                        # The annotated text that should be de-identified
    )
    
```

## Examples
``` python
>>> import deduce

>>> text_nl = """Dit is stukje tekst met daarin de naam Jan Peeters. 
                 De patient J. Peeters (e: j.peeters@email.com, t: 0471 23 45 67) is 64 jaar oud en woonachtig in Antwerpen.
                 Hij werd op 10 oktober door arts Peter de Janssens ontslagen van de UZA in Antwerpen."
                 
>>> text_fr = """Il s'agit d'un morceau de texte contenant le nom de Jean Dubois. 
                 Le patient J. Dubois (e : j.dubois@email.com, t : 0471 23 45 67) est âgé de 64 ans et vit à Namur. 
                 Il est sorti de l'Hopital Saint-Elisabeth après avoir été vu par le docteur John Dupont le 10 octobre."
                 
>>> annotated_nl = deduce.annotate_text(text_nl, patient_first_names="Jan", patient_surname="Peeters")
>>> annotated_fr = deduce.annotate_text(text_fr, patient_first_names="Jean", patient_surname="Dubois")

>>> deidentified_nl = deduce.deidentify_annotations(annotated_nl)
>>> deidentified_fr = deduce.deidentify_annotations(annotated_fr)

>>> print (annotated_nl)
Dit is stukje tekst met daarin de naam <PATIENT Jan Peeters>. De patient <PATIENT J. Peeters> (e: j.<PATIENT peeters>@<URL email.com>, t: <PHONENUMBER 0471 23 45 67>)
 is <AGE 64> jaar oud en woonachtig in <LOCATION Antwerpen>. Hij werd op <DATE 10 oktober> door arts <PERSON Peter de Janssens> ontslagen van de <INSTITUTION UZA> in <LOCATION Antwerpen>.

>>> print (annotated_fr)
Il s'agit d'un morceau de texte contenant le nom de <PATIENT Jean Dubois>. Le patient <PATIENT J. Dubois> (e : j.<PATIENT dubois>@<URL email.com>, t : <PHONENUMBER 0471 23 45 67>)
 est âgé de 64 ans et vit à <LOCATION Namur>. Il est sorti de l'<INSTITUTION Hopital Saint-Elisabeth> après avoir été vu par le <PERSON docteur John Dupont> le <DATE 10 octobre.>

>>> print (deidentified_nl)
Dit is stukje tekst met daarin de naam <PATIENT>. De patient <PATIENT> (e: j.<PATIENT>@<URL-1>, t: <PHONENUMBER-1>)
 is <AGE-1> jaar oud en woonachtig in <LOCATION-1>. Hij werd op <DATE-1> door arts <PERSON-1> ontslagen van de <INSTITUTION-1> in <LOCATION-1>.

>>> print (deidentified_fr)
Il s'agit d'un morceau de texte contenant le nom de <PATIENT>. Le patient <PATIENT> (e : j.<PATIENT>@<URL-1>, t : <PHONENUMBER-1>)
 est âgé de 64 ans et vit à <LOCATION-1>. Il est sorti de l'<INSTITUTION-1> après avoir été vu par le <PERSON-1> le <DATE-1>


```

### Configuring

The lookup lists in the `data/` folder can be tailored to the users specific needs. This is especially recommended for the list of names of institutions, since they are by default tailored to location of development and testing of the method. Regular expressions can be modified in `annotate.py`, this is for the same reason recommended for detecting patient numbers. 

## Contributing

Thanks a lot for considering to make a contribution to DEDUCE, we are very open to your help!

* If you need support, have a question, or found a bug/error, please get in touch by [creating a New Issue](https://github.com/vmenger/deduce/issues). We don't have an issue template, just try to be specific and complete, so we can tackle it. 
* If you want to make a contribution either to the code or the docs, please take a few minutes to read our [contribution guidelines](CONTRIBUTING.md). This greatly improve the chances of your work being merged into the repository.

## Changelog

You may find detailed versioning information in the [changelog](CHANGELOG.md).

## Authors

* **Vincent Menger** - *Initial work* 
* **Jonathan de Bruin** - *Code review*
* **Pablo Mosteiro** - *Bug fixes, structured annotations*

For the Belgian adaptation: Alexandre Englebert

## License

This project is licensed under the GNU LGPLv3 license - see the [LICENSE.md](LICENSE.md) file for details
