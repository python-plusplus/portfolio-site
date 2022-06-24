#!/usr/bin/bash
currentId=$(curl -s http://localhost:5000/api/timeline_post | jq .timeline_posts[0].id)
curl -s --request POST http://localhost:5000/api/timeline_post -d 'name=Sunny&email=random@random.com&content=Wassup Man'
newId=$(curl -s http://localhost:5000/api/timeline_post | jq .timeline_posts[0].id)
echo $currentId
echo $newId
if [ $(($currentId)) -lt $(($newId)) ];
then
  echo "New post successfully added!"

else
  echo "Failed to add new post"

fi

#If you want to delete the post after creation
curl -s --request DELETE http://localhost:5000/api/timeline_post -d "id=$newId"
