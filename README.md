# Solana Lib

A basic library focused on fetching data from the Solana blockchain.


## Setup

### Install requirements

    pip-compile requirements/common.in --output-file=- > requirements/common.txt
    pip-compile requirements/lint.in --output-file=- > requirements/lint.txt
    pip-compile requirements/test.in --output-file=- > requirements/test.txt

    pip install -r requirements/common.txt -r requirements/lint.txt -r requirements/test.txt

### Current Workflow to get NFTs

- Get Program Accounts 
    Filter with memcp and look for the creator account at offset 326 
    More info on the structure of metaplex accounts here 
    https://docs.metaplex.com/architecture/deep_dive/overview

-- pubkey of the result is the account that holds metadata info
-- parse account data to get the mint (nft address)

    data_64 = base64.b64decode(data)
    then get the mint with unpack_metatdata_account



    pubkey2data = {x["pubkey"]: unpack_metadata_account(base64.b64decode(x["account"]["data"][0])) for x in result}

-- Find associate token account
--- This account is involved in sales, as well as listings (which the mint is not)
--- See https://spl.solana.com/associated-token-account#finding-the-associated-token-account-address
with seeds
    walletAddress.toBuffer(), <- The minter
    TOKEN_PROGRAM_ID.toBuffer(),
    tokenMintAddress.toBuffer(), <- The mint

    from solana.publickey import PublicKey
    seeds = [
        base58.b58decode(str("6Y2Scqw11m2WUZ7qiS16e3Z9vsw6xsrrGzxktLrMX4BJ")),
        base58.b58decode(str("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")),
        base58.b58decode(str("FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC")),
    ]
    associate_token_account = PublicKey.find_program_address(
        seeds=seeds,
        program_id=ASSOCIATE_TOKEN_PROGRAM,
    )
    associate_token_account -> CpkL4HybWzJFqwHWZRR6kZ6SdK2exE1goQhu3Pt3JQFP


To get the Associate Token Account use getTokenLargestAccounts with mint as key
-> Problem: Multiple accounts are returned
--> Need to find the "first" account, the one that was involved in the mint




To get the metadata address if you have the mint
metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s is the Metaplex Metadata Token program

    from solana.publickey import PublicKey
    seeds = [
        'metadata'.encode(),
        base58.b58decode(str("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")),
        base58.b58decode(str("FDNXh1uCkQ3FE9BFVJMqeimQGUTAUinjdcgvaavufBzC")),
    ]
    metadata_account = PublicKey.find_program_address(
        seeds=seeds,
        program_id=PublicKey("metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"),
    )
    metadata_account -> 87PYEqehWWRPbS4JfqdY8ggzAAuoM35meCMzMScx31j4






## Problems that arrised and my solution

### How to decode unkown instruction data

I wanted to find the listing price for the MEV2 contract from the instruction data.
    
    2B3vSpRNKZZWsFek5ah7xe9uickZUbsaBjoqxVQF3Wq8ngW

First, base58 decode the instruction data and convert to hex

    base58.b58decode("2B3vSpRNKZZWsFek5ah7xe9uickZUbsaBjoqxVQF3Wq8ngW").hex()
    > 33e685a4017f83adfefa805470be010000000100000000000000ffffffffffffffff

I then went to an online hex converter (https://www.scadacore.com/tools/programming-calculators/online-hex-converter/)

- No luck

I looked at the listing price in the program logs
- listing price was 7490000000

To find out the hex representation, i wen to an online hex and little endian converter (https://www.save-editor.com/tools/wse_hex.html) and got the Hexadecimal number

- 805470BE01
- Nice! This is in the instruction data
    - 33e685a4017f83adfefa**805470be01**0000000100000000000000ffffffffffffffff

I then took the same route as the V1 contract, convert this hex to little endian and eventually to int

    price_little_endian = to_little_endian_from_hex("805470be01")
    price_lamports = int(price_little_endian, 16)