

# Get a post that is FOAF
```
curl http://127.0.0.1:8000/api/posts
curl -H "Accept: */*" "http://127.0.0.1:8000/api/posts/bc26fc1e-d4b8-11e4-a00b-dc85de3d02b5"
```

```
curl http://projecthub.ca/api/posts
curl 'http://projecthub.ca/api/posts/bc26fc1e-d4b8-11e4-a00b-dc85de3d02b5'
curl 'http://projecthub.ca/api/friends/7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7/11c3783f15f7ade03430303573098f0d4d20797b'
curl -d '{"query":"friends","author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e","authors":["7deee0684811f22b384ccb5991b2ca7e78abacde","31cc28a8fbc05787d0470cdbd62ea0474764b0ae","1af17e947f387a2d8c09a807271bd094e8eff077","77cb4f546b280ea905a6fdd99977cd090613994a","11c3783f15f7ade03430303573098f0d4d20797b","bd9ef9619c7241112d2a2b79505f736fc8d7f43e","0169a8ebf3cb3bd7f092603564873e12cce9d4c5","2130905fd0de94c3379e04839cd9f6889ba2b52c","b32c9e0b5fcf85f46b9ce2ba89b2068b57d4641b","fe45075b93d06c833bb25d5a6dfe669cfde3f99d","e28e59a9612c369717f66f53f3e014b341857601","b36e52d6aaee9285220f94fc321407a44e4dc622","584a9739ea459ce4aae5a88827d970196fb27769","96b3b5a70cd9591c73760bd8669aa5bd7cc689c5","6465678d0a409b96829fd64d0894132966e97eee","695c780ea2815bc94c54782f5046dfa4e325f875","8743f7511a1a569e4e9dacbb25e27395629ba5c0","539b65f2d76d0327dc45bf6354cda535d6f8ed02","c55670261253c5ce25e22b47a34629dd15e819d4"]}' "http://projecthub.ca/api/friends/9de17f29c12e8f97bcbbd34cc908f1baba40658e"


curl -d '{"query":"friendrequest","author":{"id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989","host":"http://127.0.0.1:8000/","displayname":"Greg"},"friend":{"id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e","host":"http://127.0.0.1:5454/","displayname":"Lara","url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"}}'
