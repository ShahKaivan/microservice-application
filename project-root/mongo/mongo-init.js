// ./mongo/mongo-init.js
db.auth('${MONGO_INITDB_ROOT_USERNAME}', '${MONGO_INITDB_ROOT_PASSWORD}')

db = db.getSiblingDB('${MONGO_INITDB_DATABASE}')

db.createUser({
  user: '${MONGO_INITDB_ROOT_USERNAME}',
  pwd: '${MONGO_INITDB_ROOT_PASSWORD}',
  roles: [
    {
      role: 'readWrite',
      db: '${MONGO_INITDB_DATABASE}'
    }
  ]
});

// Create collections
db.createCollection('products');

// Add indexes if needed
db.products.createIndex({ "name": 1 });
db.products.createIndex({ "category": 1 });