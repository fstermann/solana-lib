# Parsing Transactions

## Magic Eden V2

The listing price is located at bytes 20 to 36 in the hex data.

For identifying the type of transaction, use the first static bytes of the instruction data.

In base64 it's the first 10, in hex the first 16.

### Sales

* **base64:** `d6iteQtSVr`
* **hex:** `254ad99d4f312306`

* **account indices**
  * mint: 4
  * new authority: 0
  * old authority: 1
  * new token account: 7
  * old token account: 3
  

### Listings

* **base64:** `2B3vSpRNKZ`
* **hex:** `33e685a4017f83ad`

* **account indices**
  * mint: 4
  * new authority: 13 (This is always the MagicEdenV2 authority 1BWut...)
  * old authority: 0
  * new token account: 2
  * old token account: 2

### Delistings

* **base64:** `ENwHiaH9NA`
* **hex:** `c6c682cba35faf4b`

* **account indices**
  * mint: 3
  * new authority: 0
  * old authority: 9 (This is always the MagicEdenV2 authority 1BWut...)
  * new token account: 2
  * old token account: 2
