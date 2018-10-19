# README 
To compile crack_password.c  
- `gcc crack_password.c -o crack_password -lcrypt -lpthread -Wall`   

To run crack_password.c
- `./crack_password`

Testing Machine
- 1 processor with 6 cores  

|# of threads|System time|User time|Real time|
| -----------|-----------|---------|---------|
|1|10.878| 1.301|12.20|
|4|11.778| 1.584 |7.32|
|5|11.801| 1.591|7.30|
|6|12.009|1.567|7.06|
|9|12.457| 1.611|7.16|
|11|12.153 |1.592|7.03
|12|12.383| 1.616|7.09|

“Sweet spot"  
- 11 threads

Dataset used:
- $1$efFHd2BU$RZwRtaY7vtNT.oNyva9WR. plaintext a took 0 comparisons
- $1$aU5sC2hn$KZXWYvw31UZ23D.Ou45b6/ plaintext ab took 52 comparisons
- $1$CzeIFDJ.$rEsxZ9iglHCso11QCaYCr/ plaintext af took 156 comparisons
- $1$FC/HG0uI$JZLTCVFRHIfZH.XQaEz.l1 plaintext ah took 208 comparisons
- $1$U8TLxF7D$kW0QCt/EZ/qjjzGRDHChJ1 plaintext zda took 805 comparisons
- $1$qHI2Jfr7$wr0VhTsiSEk.bhFzb2gzF1 plaintext aa took 26 comparisons
- $1$eOaMGgQ.$QbfTrt2zmhm3kfKfO4LbK1 plaintext aa took 26 comparisons
- $1$HcIWqDwh$3Jvhs2DeVemyrZqRBg1b21 plaintext ba took 27 comparisons
- $1$KE5QvSlX$tpJ/fq7ANseXH4VrHT9WY/ plaintext ab took 52 comparisons
- $1$rweoHt19$KVkJeUS3FFC71e/MH66vy. plaintext ha took 33 comparisons
- $1$uOc54Ya0$dMBmu5QBhsGgWi3WYffpG0 plaintext la took 37 comparisons
- $1$sG7EWZDP$0kT1MziB/JWZdSTNWS7pN1 plaintext ad took 104 comparisons
- $1$cs6TFW4e$hcRh6IZR5CIdyjCkY1SDw/ plaintext fa took 31 comparisons
- $1$074MXZq5$9kzJDNa6POQN3sIYK/QhR. plaintext ga took 32 comparisons
- $1$omJrwfnq$eW6TLfJHhqU2tLuBDTTi6/ plaintext ag took 182 comparisons
- $1$itN6kdTK$39Kgyp2xFFI632rhP0faY. plaintext ha took 33 comparisons
- $1$TnP6oe3s$qLh9uSqhEZX4hm.LLJcca. plaintext ma took 38 comparisons
- $1$W34uGZ9z$3Ze1SGn4TiYThREpcq3d20 plaintext ar took 468 comparisons
- $1$WSFZXJhf$1EDTVHGTGsyqgbXYevfk5/ plaintext paa took 717 comparisons
- $1$o8ERs/wN$2KybC7nIa1FlVIUzDtW0B1 plaintext dga took 861 comparisons
- $1$vRZekyGh$iwYKzhAZBYvI9tNfv1alS. plaintext aab took 1378 comparisons
- $1$9dMYQ1Pg$yC4nX3d4yOkZnFvKwWSn3/ plaintext afs took 13000 comparisons
- $1$mizaE/18$3Imr54KGjVxUkm6khcYi./ plaintext air took 12402 comparisons
- $1$Ctcy74wu$kW59Do05QCWJIWmrhfOh00 plaintext lska took 25517 comparisons