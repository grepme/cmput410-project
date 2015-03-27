

# Get a post that is FOAF
```
curl -H "Content-Type: application/json" -d '{"query":"getpost","id":"ff0270a3-d42e-11e4-b1af-b8f6b116b2b7","author":{"id":"7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7","host":"http://127.0.0.1:8000/","displayname":"Admin"},"friends":["6de3acb0-d42d-11e4-b609-b8f6b116b2b7"]}' http://127.0.0.1:8000/api/posts/ff0270a3-d42e-11e4-b1af-b8f6b116b2b7
curl http://127.0.0.1:8000/api/posts
curl http://127.0.0.1:8000/api/posts/bc26fc1e-d4b8-11e4-a00b-dc85de3d02b5
```

```
curl -H "Content-Type: application/json" -d '{"query":"getpost","id":"ff0270a3-d42e-11e4-b1af-b8f6b116b2b7","author":{"id":"7a1c7226-d1e4-11e4-aa4c-b8f6b116b2b7","host":"http://127.0.0.1:8000/","displayname":"Admin"},"friends":["6de3acb0-d42d-11e4-b609-b8f6b116b2b7"]}' http://projecthub.ca/api/posts/ff0270a3-d42e-11e4-b1af-b8f6b116b2b7
curl http://projecthub.ca/api/posts
curl 'http://projecthub.ca/api/posts/bc26fc1e-d4b8-11e4-a00b-dc85de3d02b5'
```
