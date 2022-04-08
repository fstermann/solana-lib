# solana-rpc


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





MagicEden Contracts: 

V1: MEisE1HzehtrDpAAT8PnLHjpSSkRYakotTuJRPjTpo8
V2: M2mx93ekt1fmXSVkTrUL9xVFHkmME8HTUi5Cyc5aF7K