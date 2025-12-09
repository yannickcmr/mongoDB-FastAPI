// Get the correct database context
var db = db.getSiblingDB('Database');

db.createCollection("Users");

// Create a unique index on the "userId" field within the "Users" collection
db.Users.createIndex({ "userID": 1 }, { unique: true });

db.Users.insertMany([
  { userID: 1, name: "Alice", email: "alice_kitzler@gmx.de" },
  { userID: 2, name: "Pablo", email: "pablo.mendez@gmail.com" },
  { userID: 3, name: "Jänsen", email: "jaensen-freidrich-heinrichson@gmail.com" }
]);

print("Database 'Database' initialized with 'Users' collection and unique 'userId' index.");
