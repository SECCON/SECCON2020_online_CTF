# The Author's Write-up for CONVaaS

This is currently in WIP but I probably will not make it in time so I decided to quotes from my tweet.

- https://twitter.com/hhc0null/status/1315177770213728257

    > Intended solution for "CONVaaS": You could achieve RCE with `eval` or `__import__` function that are internally executed in logging.config by tampering convaas.yaml in a working directory during conversion.  
    >  
    > ref: https://github.com/python/cpython/blob/v3.8.6/Lib/logging/config.py (grep with "'()'" or "'class'")
    >  
    > #SECCON  
