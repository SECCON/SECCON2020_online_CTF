import {MongoClient} from 'https://deno.land/x/mongo/mod.ts';
import type {ObjectId} from 'https://deno.land/x/mongo/ts/types.ts';

const client = new MongoClient();
client.connectWithUri('mongodb://mongo:27017');

const mongo = client.database('milk');

interface UserSchema {
  _id: ObjectId,
  username: string,
  password: string,
  admin: boolean,
}

const Users = mongo.collection<UserSchema>('users');

const admin = await Users.findOne({admin: true});
console.log(admin);

if (!admin) {
  await Users.insertOne({
    username: Deno.env.get('ADMIN_USER'),
    password: Deno.env.get('ADMIN_PASS'),
    admin: true,
  });
}

client.close();
