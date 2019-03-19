WDerivator
===========

Wordlist generator

## Example usage

```
> python3 derivator.py -o output -w password
2019-03-19 09:42:00 ----------------------------------------------------------
2019-03-19 09:42:00 WDerivator v1.1
2019-03-19 09:42:00 Author : Aviso
2019-03-19 09:42:00 Last update : 03-2019
2019-03-19 09:42:00 GitHub : https://github.com/Aviso-hub/wderivator
2019-03-19 09:42:00 ----------------------------------------------------------
2019-03-19 09:42:00 Starting WDerivator with 5 threads
2019-03-19 09:42:00 Starting derivation for 'password'
2019-03-19 09:42:00 17152 password derivated.
2019-03-19 09:42:00 WDerivator end (time elapsed 0:00:00.153905)

> wc -l output
17152 output

> head -n 10 output
123456!PAsSwOrD
@1PAsSWOrd
PaSsWorD@1
@paSSwOrd123456
PAsSWoRd@123456
!123456PaSSworD
@pAssWoRD
pASSWord@123
1#pAsswORd
#passwORD1

```
