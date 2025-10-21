
# refextract

## About

A library for extracting references used in scholarly communication.

## Getting Started

Note: due to the usage of `mmap` resize functionality this library cannot be locally installed on a mac

### Docker Setup:

Before the first usage, or anytime a new library/dependency is changed a new docker image must be created using:
```shell
docker build --target refextract-tests -t refextract .
```

After that, spin up a `refextract` service with:
```shell
docker run -it -v ./tests:/refextract/tests -v ./refextract:/refextract/refextract  refextract
```

### Running tests

Exec into the container via
```shell
docker exec -it refextract /bin/bash
```
Then simply run
```shell
pytest .
```

## Usage

To get structured information from a publication reference:


``` python
>>> from refextract import extract_journal_reference
>>> reference = extract_journal_reference('J.Phys.,A39,13445')
>>> print(reference)
{
'extra_ibids': [],
'is_ibid': False,
'misc_txt': '',
'page': '13445',
'title': 'J. Phys.',
'type': 'JOURNAL',
'volume': 'A39',
'year': '',

}
```

To extract references from a PDF:
``` python
>>> from refextract import extract_references_from_file
>>> references = extract_references_from_file('1503.07589.pdf')
>>> print(references[0])
{
'author': ['F. Englert and R. Brout'],
'doi': ['doi:10.1103/PhysRevLett.13.321'],
'journal_page': ['321'],
'journal_reference': ['Phys. Rev. Lett. 13 (1964) 321'],
'journal_title': ['Phys. Rev. Lett.'],
'journal_volume': ['13'],
'journal_year': ['1964'],
'linemarker': ['1'],
'raw_ref': ['[1] F. Englert and R. Brout, \u201cBroken symmetry and the mass of gauge vector mesons\u201d, Phys. Rev. Lett. 13 (1964) 321, doi:10.1103/PhysRevLett.13.321.'],
'texkey': ['Englert:1964et'],
'year': ['1964'],
}
```

To extract directly from a URL:
``` python
>>> from refextract import extract_references_from_url
>>> references = extract_references_from_url('https://arxiv.org/pdf/1503.07589.pdf')
>>> print(references[0])
{
'author': ['F. Englert and R. Brout'],
'doi': ['doi:10.1103/PhysRevLett.13.321'],
'journal_page': ['321'],
'journal_reference': ['Phys. Rev. Lett. 13 (1964) 321'],
'journal_title': ['Phys. Rev. Lett.'],
'journal_volume': ['13'],
'journal_year': ['1964'],
'linemarker': ['1'],
'raw_ref': ['[1] F. Englert and R. Brout, \u201cBroken symmetry and the mass of gauge vector mesons\u201d, Phys. Rev. Lett. 13 (1964) 321, doi:10.1103/PhysRevLett.13.321.'],
'texkey': ['Englert:1964et'],
'year': ['1964'],

}

```

## Notes
`refextract` depends on

[pdftotext](http://linux.die.net/man/1/pdftotext).

## Acknowledgments

`refextract` is based on code and ideas from the following people, who

contributed to the `docextract` module in Invenio:
- Alessio Deiana
- Federico Poli
- Gerrit Rindermann
- Graham R. Armstrong
- Grzegorz Szpura
- Jan Aage Lavik
- Javier Martin Montull
- Micha Moskovic
- Samuele Kaplun
- Thorsten Schwander
- Tibor Simko

## License
GPLv2
