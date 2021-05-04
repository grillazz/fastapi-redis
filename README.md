# fastapi-redis

[![license](https://img.shields.io/github/license/grillazz/fastapi-redis)](https://github.com/grillazz/fastapi-redis/blob/main/LICENSE)





Working example for FastAPI with Redis.

Using latest and greatest version of redis

Data set is comming from pub chem 

fast api what it is https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087

There is so mamy chem compud set but we all are noe in times where COVID-19 Pandemy is out there
and we all want to knwo as much as possibile about cure... so that is my project background.
Show power and robusteness of Redis with speed of FastAPI and funcinality of RDKit to deliver api 
which allow quicky analyze chem molecules.

For puprose of this hackatoon i added only two cases to load checm molecules to redis cache and to compare 
all moelcule which we alredy have with new one.

This can be really quickly integrate with other projects with REST API and extended to deliver desired chem compound bakery.

You can download example from COVID-19 Disease Map here on this link: https://pubchem.ncbi.nlm.nih.gov/#query=covid-19

Project as whole is build on asyncio including REST, Redis connection and transactions and unit tests.
